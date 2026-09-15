"""Structural checks that need no LLM.

Exit 1 on any finding so agents and CI stop on it.
Usage: python omoikane/bin/wiki-lint.py
"""
from __future__ import annotations

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


def main() -> int:
    pages = load_pages()
    findings = lint_pages(pages)
    for f in findings:
        print(f)
    print(f"wiki-lint: {len(pages)} pages, {len(findings)} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
