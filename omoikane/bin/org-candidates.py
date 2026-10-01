"""List the lessons that two or more systems of one organisation learned, as proposals for its shared knowledge.

Each system distills its own sessions into its own wiki, so a gotcha that bit three systems lives in three
wikis and the organisation's knowledge base hears of none (#52, docs/specs/2026-10-01-org-knowledge.md).
Decision, gotcha and practice pages are matched across systems by their `org:` key, or by slug when they have
none; a key found in MIN_SYSTEMS or more distinct systems is a candidate. Only frontmatter leaves a system:
page bodies and raw captures may quote customer data. Pages marked `prune:` are left out. Read-only.

Usage: python omoikane/bin/org-candidates.py --system billing=../billing --system portal=../portal [--format json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from wikilib import GUARDS, load_pages

# One system's habit is not the organisation's rule; the same floor as a practice's two sessions.
MIN_SYSTEMS = 2
LESSON_TYPES = ("decision", "gotcha", "practice")
ORG_KEY = "org"
# Strongest first: a check that fails every time beats one that fails only when a test or hook runs.
GUARD_RANK = {guard: rank for rank, guard in enumerate(GUARDS)}


def evidence(system: str, root: Path) -> list[dict[str, str]]:
    """One entry per lesson page of the system's wiki, frontmatter only.

    Example: evidence("billing", Path("../billing"))[0] returns {"system": "billing", "key": "orm-drops-time-zone",
    "type": "gotcha", "page": "omoikane/wiki/gotchas/orm-drops-time-zone.md", "summary": "...", "guard": "test",
    "updated": "2026-09-02"}.
    """
    entries: list[dict[str, str]] = []
    for page in load_pages(root / "omoikane" / "wiki"):
        kind = str(page.meta.get("type", ""))
        if kind not in LESSON_TYPES or page.meta.get("prune"):
            continue
        entries.append({"system": system, "key": str(page.meta.get(ORG_KEY) or page.slug), "type": kind,
                        "page": page.path.relative_to(root).as_posix(), "summary": str(page.meta.get("summary", "")),
                        "guard": str(page.meta.get("guard") or "none"), "updated": str(page.meta.get("updated", ""))})
    return entries


def candidates(systems: dict[str, Path]) -> list[dict[str, object]]:
    """The keys found in MIN_SYSTEMS or more distinct systems, each with its evidence in the order systems were
    given. The summary and type come from the page with the strongest guard. A path given twice counts once.

    Example: candidates({"a": Path("../a"), "b": Path("../b")}) returns [{"key": "orm-drops-time-zone",
    "type": "gotcha", "summary": "...", "guard": "test", "systems": 2, "evidence": [...]}].
    """
    seen: set[Path] = set()
    by_key: dict[str, list[dict[str, str]]] = {}
    for system, root in systems.items():
        if root.resolve() in seen:
            continue
        seen.add(root.resolve())
        for entry in evidence(system, root):
            by_key.setdefault(entry["key"], []).append(entry)
    found: list[dict[str, object]] = []
    for key, entries in sorted(by_key.items()):
        if len({e["system"] for e in entries}) < MIN_SYSTEMS:
            continue
        best = min(entries, key=lambda e: GUARD_RANK.get(e["guard"], len(GUARD_RANK)))
        found.append({"key": key, "type": best["type"], "summary": best["summary"], "guard": best["guard"],
                      "systems": len({e["system"] for e in entries}), "evidence": entries})
    return found


def markdown(found: list[dict[str, object]]) -> str:
    """One bullet per candidate, its evidence indented below.

    Example: markdown(candidates(...)) returns "- candidate (gotcha) k: S (2 systems, guard test)\\n  - a: ...\\n".
    """
    lines: list[str] = []
    for c in found:
        lines.append(f"- candidate ({c['type']}) {c['key']}: {c['summary']} ({c['systems']} systems, guard {c['guard']})")
        for e in c["evidence"]:  # type: ignore[attr-defined]
            lines.append(f"  - {e['system']}: {e['summary']} ({e['page']}, guard {e['guard']})")
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
        root = Path(path)
        if not (root / "omoikane" / "wiki").is_dir():
            parser.error(f"{spec}: no omoikane/wiki/ under {root}")
        systems[name] = root
    found = candidates(systems)
    sys.stdout.write(json.dumps(found, indent=2) + "\n" if args.format == "json" else markdown(found))
    return 0


if __name__ == "__main__":
    sys.exit(main())
