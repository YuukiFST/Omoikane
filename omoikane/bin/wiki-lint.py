"""Structural checks that need no LLM.

Exit 1 on any finding so agents and CI stop on it. Warnings print but keep exit 0: they need a judgement
the script cannot make, and the semantic /lint pass reads them.
Usage: python omoikane/bin/wiki-lint.py
"""
from __future__ import annotations

import posixpath
import subprocess
import sys
from pathlib import Path

from wikilib import CODE_KEY, DATE, PAGE_TYPES, REPO, REQUIRED_KEYS, SOURCE_KEYS, UNDATED, Page, load_pages


def lint_pages(pages: list[Page], repo: Path = REPO) -> list[str]:
    """Return one finding per contract violation; an empty list means clean.

    Example: lint_pages([Page(path, "x", {"type": "gotcha", "code": ["gone.py"], ...})], repo)
    returns ["...: code path `gone.py` does not exist", ...].
    """
    slugs = {p.slug for p in pages}
    inbound: dict[str, int] = {s: 0 for s in slugs}
    findings: list[str] = []
    # A wikilink names a slug, not a folder: `decisions/x.md` and `gotchas/x.md` would both answer [[x]].
    first_with_slug: dict[str, Page] = {}
    for p in pages:
        if p.slug in first_with_slug:
            findings.append(f"{p.rel}: slug `{p.slug}` is also {first_with_slug[p.slug].rel}; [[{p.slug}]] is ambiguous")
        first_with_slug.setdefault(p.slug, p)

    for p in pages:
        if not p.meta:
            findings.append(f"{p.rel}: missing frontmatter")
            continue
        for key in REQUIRED_KEYS:
            if key not in p.meta:
                findings.append(f"{p.rel}: frontmatter missing `{key}`")
        if p.meta.get("type") not in PAGE_TYPES:
            findings.append(f"{p.rel}: type must be one of {', '.join(PAGE_TYPES)}")
        if p.meta.get("type") == "source":
            for key in SOURCE_KEYS:
                if key not in p.meta:
                    findings.append(f"{p.rel}: source page missing `{key}` (date the source bears, or {UNDATED})")
        for key in ("created", "updated", "dated"):
            value = str(p.meta.get(key, ""))
            if key in p.meta and not DATE.match(value) and not (key == "dated" and value == UNDATED):
                findings.append(f"{p.rel}: `{key}` is `{value}`, expected YYYY-MM-DD")
        summary = str(p.meta.get("summary", ""))
        if len(summary) > 120:
            findings.append(f"{p.rel}: summary is {len(summary)} chars, limit 120")
        for target in p.links:
            if target in slugs:
                inbound[target] += 1
            else:
                findings.append(f"{p.rel}: broken wikilink [[{target}]]")
        # `sources:` entries are relative to omoikane/ (`wiki/sources/x.md`), matching the page contract in AGENTS.md.
        for src in p.meta.get("sources", []) or []:
            if not (str(src).startswith("wiki/") and str(src).endswith(".md")):
                findings.append(f"{p.rel}: sources entry `{src}` is not a wiki path")
        code = p.meta.get(CODE_KEY, [])
        if not isinstance(code, list):
            findings.append(f"{p.rel}: `{CODE_KEY}` must be an inline list of repository paths")
            code = []
        for path in code:
            # `code:` entries are relative to the repository root. A page about code that no longer exists is stale
            # by definition; the agent must revisit it. Paths escaping the repository are never valid.
            target = (repo / str(path)).resolve()
            if not target.is_relative_to(repo.resolve()) or not target.exists():
                findings.append(f"{p.rel}: code path `{path}` does not exist")

    for p in pages:
        if inbound.get(p.slug, 0) == 0 and p.meta.get("type") != "query":
            findings.append(f"{p.rel}: orphan page, no inbound wikilink")
    return findings


def git_path(path: object) -> str:
    """Spell a `code:` entry the way git prints paths: posix, relative, no `./` or trailing slash.

    Backslashes (a page written on Windows) become slashes.
    Example: git_path("./src/pkg/") returns "src/pkg"; git_path(".") returns ".".
    """
    return posixpath.normpath(str(path).replace("\\", "/"))


def code_paths(pages: list[Page], repo: Path = REPO) -> list[str]:
    """Every `code:` path that exists inside the repository, in git spelling.

    Paths `lint_pages` reports as missing or outside the repository are left out: git refuses a pathspec
    outside the repository, and one bad page must not hide every other finding behind a traceback.
    Example: code_paths([page with code ["./src/", "../outside.py"]], repo) returns ["src"].
    """
    root = repo.resolve()
    paths: set[str] = set()
    for p in pages:
        code = p.meta.get(CODE_KEY)
        if not isinstance(code, list):
            continue
        for path in code:
            target = (repo / str(path)).resolve()
            if target.is_relative_to(root) and target.exists():
                paths.add(git_path(path))
    return sorted(paths)


def last_changed(repo: Path, paths: list[str]) -> dict[str, str]:
    """Map each file under `paths` to the date (YYYY-MM-DD) its newest change reached the current branch.

    One `git log` call, limited to the `code:` paths so a long history outside them costs nothing.
    `--first-parent` dates a merged change at its merge, not at the side commit (this repository merges
    PRs with merge commits). Returns {} without git, outside a repository, or in a shallow clone, where
    every file would carry HEAD's date and every page would warn.
    Example: last_changed(repo, ["src"]) returns {"src/a.py": "2026-09-05"}.
    """
    if not paths:
        return {}
    git = ["git", "-C", str(repo), "-c", "core.quotePath=false"]
    try:
        shallow = subprocess.run([*git, "rev-parse", "--is-shallow-repository"], capture_output=True, text=True,
                                 check=False)
        if shallow.returncode != 0 or shallow.stdout.strip() != "false":
            return {}
        log = subprocess.run([*git, "log", "--first-parent", "--format=>%cs", "--name-only", "--", *paths],
                             capture_output=True, text=True, encoding="utf-8", check=False)
    except OSError:
        return {}
    if log.returncode != 0:
        return {}
    dates: dict[str, str] = {}
    current = ""
    for line in log.stdout.splitlines():
        if line.startswith(">"):
            current = line[1:]
        elif line:
            dates.setdefault(line, current)  # git log lists newest first
    return dates


def stale_pages(pages: list[Page], changed: dict[str, str]) -> list[str]:
    """Warn about pages whose `code:` paths have a commit dated after the page's `updated` date.

    Most code changes leave the page true, so this is a warning for /lint to judge, not a finding.
    Example: stale_pages([gotcha with updated 2026-09-15, code [src/a.py]], {"src/a.py": "2026-09-20"})
    returns ["...: `src/a.py` changed on 2026-09-20, after the page's `updated` 2026-09-15; ..."].
    """
    warnings: list[str] = []
    for p in pages:
        updated = str(p.meta.get("updated", ""))
        code = p.meta.get(CODE_KEY) or []
        if not isinstance(code, list) or not DATE.match(updated):
            continue
        for path in code:
            prefix = git_path(path)
            latest = max((d for f, d in changed.items()
                          if prefix == "." or f == prefix or f.startswith(prefix + "/")), default="")
            if latest > updated:
                warnings.append(f"{p.rel}: `{path}` changed on {latest}, after the page's `updated` {updated}; "
                                "check the page still matches the code")
    return warnings


def main() -> int:
    pages = load_pages()
    findings = lint_pages(pages)
    warnings = stale_pages(pages, last_changed(REPO, code_paths(pages)))
    for f in findings:
        print(f)
    for w in warnings:
        print(f"warning: {w}")
    print(f"wiki-lint: {len(pages)} pages, {len(findings)} findings, {len(warnings)} warnings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
