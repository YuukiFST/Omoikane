"""Turn a fresh clone of the Omoikane template into the empty memory of a new system.

A clone carries the template's own wiki, log, review queue and captures, and session-context.py would brief every
session of the new system on them (#66). This removes every page, capture and source, resets log.md and _review.md
to their headers, regenerates index.md and empties the rules block of AGENTS.md, whose rules point at pages that
are gone, and renames the `origin` remote to `template`. Prompts, scripts, hooks and tests stay. It refuses a
tree with uncommitted changes and never commits, so `git restore .` undoes a run (and `git remote rename` the
rename).

With --from, the organisation's conventions and design-system rules another system learned come along: its domain
pages tagged `convention` or `design-system`, citing one source page that names where they came from (#80,
docs/specs/2026-10-02-cross-system-knowledge.md).

Usage: python omoikane/bin/new-system.py [--from <checkout of another system>]
"""
from __future__ import annotations

import argparse
import importlib
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from wikilib import OMOIKANE, REPO, RULES_END, RULES_START, WIKILINK, load_pages

wiki_index = importlib.import_module("wiki-index")

# Everything the template learned about itself lives here; .gitkeep files keep the empty folders in git.
CLEARED = ("wiki", "raw/sources", "raw/inbox", "raw/assets")
KEEP = ".gitkeep"
ENTRY = "\n## ["
# Rules an organisation holds in every system it builds. A business rule belongs to one system's domain, and
# decisions, gotchas and practices are about code or sessions that stay behind.
INHERITED_TAGS = ("convention", "design-system")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8",
                          check=True).stdout


def detach_template(repo: Path) -> str:
    """Rename the clone's `origin`, the template, to `template`. review-gate.py fetches `origin/wiki/auto` and
    publishes to `origin`: left as it is, the new system's pages would be merged with the template's and pushed
    to the template. Returns a line for the user.

    Example: detach_template(Path(".")) returns "origin renamed to template; ..." in a fresh clone.
    """
    remotes = git(repo, "remote").split()
    if "origin" not in remotes or "template" in remotes:
        return "no remote renamed; check that origin is the new system's repository before scheduling runs"
    git(repo, "remote", "rename", "origin", "template")
    return "origin renamed to template; add the new system's repository with `git remote add origin <url>`"


def clear(folder: Path) -> int:
    """Delete every file under `folder` except .gitkeep; return how many.

    Example: clear(Path("omoikane/wiki")) returns 31 on this repository and leaves wiki/decisions/.gitkeep.
    """
    files = [p for p in folder.rglob("*") if p.is_file() and p.name != KEEP] if folder.is_dir() else []
    for path in files:
        path.unlink()
    return len(files)


def header(text: str) -> str:
    """The part of log.md or _review.md before its first `## [date]` entry.

    Example: header("# Log\\n\\nIntro.\\n\\n## [2026-09-09] init | x\\n") returns "# Log\\n\\nIntro.\\n".
    """
    cut = text.find(ENTRY)
    return (text if cut < 0 else text[:cut]).rstrip("\n") + "\n"


def empty_rules(agents: str) -> str:
    start = agents.index(RULES_START) + len(RULES_START)
    return agents[:start] + "\n" + agents[agents.index(RULES_END):]


def write(path: Path, text: str) -> None:
    # Explicit LF, as wiki-index.py writes: text mode on Windows would turn every line into a diff.
    path.write_text(text, encoding="utf-8", newline="\n")


def frontmatter(meta: dict[str, object]) -> str:
    lines = [f"{key}: [{', '.join(map(str, value))}]" if isinstance(value, list) else f"{key}: {value}"
             for key, value in meta.items()]
    return "---\n" + "\n".join(lines) + "\n---\n"


def inherit(origin: Path, omoikane: Path, day: str) -> list[str]:
    """Copy `origin`'s convention and design-system domain pages into `omoikane`'s wiki; return their slugs.

    Each copy cites one new source page, wiki/sources/inherited-from-<system>.md, and drops `code:` and the links to
    pages that stayed behind, so the new wiki passes wiki-lint.py on its own.
    Example: inherit(Path("../payroll"), Path("omoikane"), "2026-10-02") returns ["commit-messages-in-english"].
    """
    pages = [p for p in load_pages(origin / "omoikane" / "wiki" / "domain")
             if p.meta.get("type") == "domain" and set(p.meta.get("tags") or []) & set(INHERITED_TAGS)]
    if not pages:
        return []
    system = re.sub(r"[^a-z0-9]+", "-", origin.resolve().name.lower()).strip("-")
    source = f"inherited-from-{system}"
    try:
        dated, commit = git(origin, "log", "-1", "--format=%cs %h").split()
    except (OSError, subprocess.CalledProcessError, ValueError):
        dated, commit = "unknown", "unknown"
    copied = {p.slug for p in pages}

    def unlink(m: re.Match[str]) -> str:
        return m.group(0) if m.group(1).strip() in copied else m.group(1).strip()

    for p in pages:
        meta = {key: p.meta[key] for key in ("title", "type", "summary", "tags") if key in p.meta}
        meta.update(created=day, updated=day, sources=[f"wiki/sources/{source}.md"])
        body = WIKILINK.sub(unlink, p.body).rstrip("\n")
        note = f"Inherited from `{system}` at commit {commit} (source: [[{source}]])."
        write(omoikane / "wiki" / "domain" / p.path.name, frontmatter(meta) + body + f"\n\n{note}\n")
    listed = "\n".join(f"- [[{p.slug}]] — {p.meta.get('summary', '')}" for p in pages)
    write(omoikane / "wiki" / "sources" / f"{source}.md", frontmatter({
        "title": f"Inherited from {system}", "type": "source",
        "summary": f"Convention and design-system rules copied from {system} when this system started",
        "tags": ["inherited"], "created": day, "updated": day, "dated": dated, "sources": []})
        + f"\nCopied by `omoikane/bin/new-system.py --from` from the wiki of `{system}` at commit {commit}: its domain "
          f"pages tagged {' or '.join(f'`{t}`' for t in INHERITED_TAGS)}. They do not follow later changes there; a "
          f"session that states a rule differently updates the page here.\n\n{listed}\n")
    return sorted(copied)


def main(omoikane: Path = OMOIKANE, repo: Path = REPO, today: date | None = None, origin: Path | None = None) -> int:
    if origin is not None and not (origin / "omoikane" / "wiki").is_dir():
        print(f"new-system: {origin} has no omoikane/wiki; give the checkout of a system built from the template. "
              "Nothing was changed")
        return 2
    try:
        dirty = git(repo, "status", "--porcelain")
    except (OSError, subprocess.CalledProcessError):
        print("new-system: run it inside a git clone of the template, with git on PATH; nothing was changed")
        return 2
    if dirty:
        print("new-system: commit or discard these changes first, so `git restore .` can undo the reset:\n" + dirty)
        return 2
    removed = sum(clear(omoikane / folder) for folder in CLEARED)
    log = omoikane / "log.md"
    day = (today or date.today()).isoformat()
    entry = f"\n## [{day}] init | Memory reset from the Omoikane template\n"
    inherited = inherit(origin, omoikane, day) if origin is not None else []
    if inherited:
        entry += f"\n- inherited from {origin.resolve().name}: " + ", ".join(f"[[{s}]]" for s in inherited) + "\n"
    write(log, header(log.read_text(encoding="utf-8")) + entry)
    review = omoikane / "_review.md"
    write(review, header(review.read_text(encoding="utf-8")))
    write(omoikane / "index.md", wiki_index.render(load_pages(omoikane / "wiki")))
    agents = repo / "AGENTS.md"
    write(agents, empty_rules(agents.read_text(encoding="utf-8")))
    print(f"new-system: removed {removed} files from omoikane/; read `git status`, then commit")
    if origin is not None:
        print(f"new-system: inherited {len(inherited)} convention and design-system pages from {origin}")
    print(f"new-system: {detach_template(repo)}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--from", dest="origin", type=Path, help="checkout of another system to take conventions from")
    sys.exit(main(origin=parser.parse_args().origin))
