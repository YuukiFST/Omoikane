"""Turn a fresh clone of the Omoikane template into the empty memory of a new system.

A clone carries the template's own wiki, log, review queue and captures, and session-context.py would brief every
session of the new system on them (#66). This removes every page, capture and source, resets log.md and _review.md
to their headers, regenerates index.md and empties the rules block of AGENTS.md, whose rules point at pages that
are gone, and renames the `origin` remote to `template`. Prompts, scripts, hooks and tests stay. It refuses a
tree with uncommitted changes and never commits, so `git restore .` undoes a run (and `git remote rename` the
rename).

Usage: python omoikane/bin/new-system.py
"""
from __future__ import annotations

import importlib
import subprocess
import sys
from datetime import date
from pathlib import Path

from wikilib import OMOIKANE, REPO, RULES_END, RULES_START, load_pages

wiki_index = importlib.import_module("wiki-index")

# Everything the template learned about itself lives here; .gitkeep files keep the empty folders in git.
CLEARED = ("wiki", "raw/sources", "raw/inbox", "raw/assets")
KEEP = ".gitkeep"
ENTRY = "\n## ["


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


def main(omoikane: Path = OMOIKANE, repo: Path = REPO, today: date | None = None) -> int:
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
    write(log, header(log.read_text(encoding="utf-8")) + f"\n## [{day}] init | Memory reset from the Omoikane template\n")
    review = omoikane / "_review.md"
    write(review, header(review.read_text(encoding="utf-8")))
    write(omoikane / "index.md", wiki_index.render(load_pages(omoikane / "wiki")))
    agents = repo / "AGENTS.md"
    write(agents, empty_rules(agents.read_text(encoding="utf-8")))
    print(f"new-system: removed {removed} files from omoikane/; read `git status`, then commit")
    print(f"new-system: {detach_template(repo)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
