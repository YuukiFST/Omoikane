"""Seed the inbox from an existing project: its README, docs, agent rule files and git history, for /ingest.

A project that adopts Omoikane, or a system that replaces one, already states many of its rules in writing; without
this they reach the wiki only when the user restates them in a session (#79; after ai-memory's `bootstrap` and
brainmaxxing's `/ruminate`). Each source becomes one inbox file, headed with where it came from and when it last
changed, so /ingest can date it. Only tracked files are read, nothing under omoikane/, and nothing still identical
to the template's copy (remote `template`, which new-system.py names): that describes Omoikane, not the system.
A second run writes nothing that is already in the inbox or in raw/sources/.

Usage: python omoikane/bin/bootstrap.py [--from PATH]     # default: this repository
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

from wikilib import OMOIKANE, REPO

# What a project writes down for people and agents, not code. Patterns match the path from the repository root.
SOURCES = ("README*", "docs/*.md", "docs/**/*.md", "docs/*.mdx", "docs/**/*.mdx", "AGENTS.md", "CLAUDE.md",
           "GEMINI.md", "CONTRIBUTING.md", ".cursorrules", ".windsurfrules", ".clinerules", ".cursor/rules/*",
           ".github/copilot-instructions.md")
TEMPLATE_REF = "template/main"
HISTORY_COMMITS = 300  # newest first; a long history past this adds little a rule needs
BODY_CHARS = 1000
PREFIX = "bootstrap-"


class BootstrapError(Exception):
    """The project cannot be read: not a git repository, or git is missing."""


def git(repo: Path, *args: str) -> str:
    try:
        run = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8")
    except FileNotFoundError as exc:
        raise BootstrapError("git is not installed") from exc
    if run.returncode != 0:
        raise BootstrapError(run.stderr.strip() or f"git {' '.join(args)} failed")
    return run.stdout


def slug(path: str) -> str:
    """Example: slug(".cursor/rules/Style.mdc") returns "cursor-rules-style-mdc"."""
    return re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")


def sources(project: Path) -> list[str]:
    """Tracked files a project writes its rules in, minus omoikane/ and what the template shipped unchanged."""
    tracked = [p for p in git(project, "ls-files", "-z").split("\0") if p and not p.startswith("omoikane/")]
    picked = [p for p in tracked if any(fnmatch.fnmatchcase(p, pattern) for pattern in SOURCES)]
    if not has_template(project):
        return picked
    changed = set(git(project, "diff", "--name-only", "-z", TEMPLATE_REF, "--", *picked).split("\0")) if picked else set()
    shipped = set(git(project, "ls-tree", "-r", "--name-only", "-z", TEMPLATE_REF).split("\0"))
    return [p for p in picked if p in changed or p not in shipped]


def has_template(project: Path) -> bool:
    try:
        git(project, "rev-parse", "--verify", "--quiet", TEMPLATE_REF)
    except BootstrapError:
        return False
    return True


def source_note(project: Path, path: str) -> str:
    changed = git(project, "log", "-1", "--format=%cs %h", "--", path).split()
    when = f"last changed {changed[0]} in commit {changed[1]}" if changed else "never committed"
    text = (project / path).read_text(encoding="utf-8", errors="replace")
    return (f"# {path} of {project.name} (bootstrap)\n\nCopied by `omoikane/bin/bootstrap.py` from `{path}` in "
            f"`{project.name}`, {when}.\n\n---\n\n{text}")


def history_note(project: Path) -> str | None:
    """The first-parent commits of HEAD after the template's, newest first, subject and body."""
    rev = ["HEAD", f"^{TEMPLATE_REF}"] if has_template(project) else ["HEAD"]
    try:
        log = git(project, "log", "--first-parent", f"-{HISTORY_COMMITS}", "--format=%x00%cs %h %s%n%b", *rev)
    except BootstrapError:
        return None  # no commit yet
    entries = []
    for entry in filter(None, (e.strip() for e in log.split("\0"))):
        head, _, body = entry.partition("\n")
        body = body.strip()
        body = body if len(body) <= BODY_CHARS else body[:BODY_CHARS].rstrip() + " [...]"
        entries.append(f"## {head}\n\n{body}" if body else f"## {head}")
    if not entries:
        return None
    return (f"# Git history of {project.name} (bootstrap)\n\nCopied by `omoikane/bin/bootstrap.py`: the "
            f"first-parent commits of `{project.name}`, newest first, at most {HISTORY_COMMITS}, as date, commit "
            "and subject, then the body. A body often holds the reason for a change.\n\n" + "\n\n".join(entries) + "\n")


def bootstrap(project: Path, omoikane: Path = OMOIKANE) -> list[str]:
    """Write one inbox file per source of `project` and one for its history; return the names written.

    Example: bootstrap(Path("../shop")) returns ["bootstrap-readme-md.md", ..., "bootstrap-git-history.md"].
    """
    inbox, ingested = omoikane / "raw" / "inbox", omoikane / "raw" / "sources"
    notes = {f"{PREFIX}{slug(p)}.md": (lambda p=p: source_note(project, p)) for p in sources(project)}
    notes[f"{PREFIX}git-history.md"] = lambda: history_note(project)
    written = []
    for name, render in notes.items():
        if (inbox / name).exists() or (ingested / name).exists():
            continue
        text = render()
        if text is None:
            continue
        inbox.mkdir(parents=True, exist_ok=True)
        (inbox / name).write_text(text, encoding="utf-8", newline="\n")
        written.append(name)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--from", dest="project", type=Path, default=REPO, help="the project to read")
    args = parser.parse_args(argv)
    try:
        git(args.project, "rev-parse", "--git-dir")
        written = bootstrap(args.project.resolve())
    except BootstrapError as exc:
        print(f"bootstrap: {args.project} is not a git repository, or git failed: {exc}", file=sys.stderr)
        return 2
    for name in written:
        print(f"bootstrap: wrote omoikane/raw/inbox/{name}")
    print(f"bootstrap: {len(written)} files for /ingest; the scheduled run ingests them, or run /ingest on each")
    return 0


if __name__ == "__main__":
    sys.exit(main())
