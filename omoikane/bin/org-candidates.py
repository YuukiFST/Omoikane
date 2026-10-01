"""List the lessons that two or more systems of one organisation learned, as proposals for its shared knowledge.

Each system distills its own sessions into its own wiki, so a gotcha that bit three systems lives in three
wikis and the organisation's knowledge base hears of none (#52, docs/specs/2026-10-01-org-knowledge.md).
Decision, gotcha and practice pages are matched across systems by their `org:` key, or by slug when they have
none; a key found in MIN_SYSTEMS or more distinct systems is a candidate. Only frontmatter leaves a system, plus
whether the page records a contradiction: page bodies and raw captures may quote customer data. Pages marked
`prune:` are left out. Read-only.

Usage: python omoikane/bin/org-candidates.py --system billing=../billing --system portal=../portal [--format json]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import TypedDict

from wikilib import GUARDS, load_pages

# One system's habit is not the organisation's rule; the same floor as a practice's two sessions.
MIN_SYSTEMS = 2
LESSON_TYPES = ("decision", "gotcha", "practice")
ORG_KEY = "org"
# Strongest first: a check that fails every time beats one that fails only when a test or hook runs.
GUARD_RANK = {guard: rank for rank, guard in enumerate(GUARDS)}
CONTRADICTIONS = "## Contradictions"


class Evidence(TypedDict):
    system: str
    key: str
    type: str
    title: str
    page: str
    summary: str
    guard: str
    updated: str
    contradictions: bool


class Candidate(TypedDict):
    key: str
    type: str
    summary: str
    guard: str
    systems: int
    evidence: list[Evidence]


def evidence(system: str, root: Path) -> list[Evidence]:
    """One entry per lesson page of the system's wiki, frontmatter only; `contradictions` says whether the body
    has a `## Contradictions` section (where a page records that the system departs), not what it says.

    Example: evidence("billing", Path("../billing"))[0]["page"] returns "omoikane/wiki/gotchas/orm-drops-time-zone.md".
    """
    entries: list[Evidence] = []
    for page in load_pages(root / "omoikane" / "wiki"):
        kind = str(page.meta.get("type", ""))
        if kind not in LESSON_TYPES or page.meta.get("prune"):
            continue
        entries.append(Evidence(system=system, key=str(page.meta.get(ORG_KEY) or page.slug), type=kind,
                                title=str(page.meta.get("title", "")), page=page.path.relative_to(root).as_posix(),
                                summary=str(page.meta.get("summary", "")), guard=str(page.meta.get("guard") or "none"),
                                updated=str(page.meta.get("updated", "")),
                                contradictions=any(line.strip() == CONTRADICTIONS for line in page.body.splitlines())))
    return entries


def repository_identity(root: Path) -> tuple[Path, str]:
    """The git common directory of `root` and its place inside the checkout, so a repository and its worktrees
    are one system while two folders of one repository stay two; the resolved path where git cannot tell (no git,
    not a repository).

    Example: repository_identity(Path("../billing-wiki-auto")) returns (Path(".../billing/.git"), "").
    """
    try:
        run = subprocess.run(["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-common-dir",
                              "--show-prefix"], capture_output=True, text=True, encoding="utf-8", check=False)
    except OSError:  # git not installed
        return root.resolve(), ""
    lines = run.stdout.split("\n") if run.returncode == 0 else []
    return (Path(lines[0]).resolve(), lines[1]) if len(lines) >= 2 and lines[0] else (root.resolve(), "")


def candidates(systems: dict[str, Path]) -> list[Candidate]:
    """The keys found in MIN_SYSTEMS or more distinct systems, each with its evidence in the order systems were
    given. The summary and type come from the page with the strongest guard. A repository given twice, under two
    names or as one of its worktrees, counts once.

    Example: candidates({"a": Path("../a"), "b": Path("../b")})[0]["systems"] returns 2.
    """
    seen: set[tuple[Path, str]] = set()
    by_key: dict[str, list[Evidence]] = {}
    for system, root in systems.items():
        identity = repository_identity(root)
        if identity in seen:
            continue
        seen.add(identity)
        for entry in evidence(system, root):
            by_key.setdefault(entry["key"], []).append(entry)
    found: list[Candidate] = []
    for key, entries in sorted(by_key.items()):
        count = len({e["system"] for e in entries})
        if count < MIN_SYSTEMS:
            continue
        best = min(entries, key=lambda e: GUARD_RANK.get(e["guard"], len(GUARD_RANK)))
        found.append(Candidate(key=key, type=best["type"], summary=best["summary"], guard=best["guard"],
                               systems=count, evidence=entries))
    return found


def markdown(found: list[Candidate]) -> str:
    """One bullet per candidate, its evidence indented below.

    Example: markdown(candidates(...)) returns "- candidate (gotcha) k: S (2 systems, guard test)\\n  - a: ...\\n".
    """
    lines: list[str] = []
    for c in found:
        lines.append(f"- candidate ({c['type']}) {c['key']}: {c['summary']} ({c['systems']} systems, guard {c['guard']})")
        for e in c["evidence"]:
            departs = ", records a contradiction" if e["contradictions"] else ""
            lines.append(f"  - {e['system']}: {e['summary']} ({e['page']}, guard {e['guard']}, updated {e['updated']}"
                         f"{departs})")
    return "\n".join(lines) + ("\n" if lines else "")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--system", action="append", required=True, metavar="NAME=PATH",
                        help="a system's repository root; repeat for each system")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    systems: dict[str, Path] = {}
    for spec in args.system:
        name, _, path = spec.partition("=")
        # An empty path is the current directory: its wiki would be counted under that name.
        if not name or not path:
            parser.error(f"--system {spec}: give NAME=PATH")
        if name in systems:
            parser.error(f"--system {spec}: the name {name} is given twice")
        root = Path(path)
        if not (root / "omoikane" / "wiki").is_dir():
            parser.error(f"{spec}: no omoikane/wiki/ under {root}")
        systems[name] = root
    found = candidates(systems)
    sys.stdout.write(json.dumps(found, indent=2) + "\n" if args.format == "json" else markdown(found))
    return 0


if __name__ == "__main__":
    sys.exit(main())
