"""Print the wiki brief for the harness to add to the agent's context at session start: pending work, then the index.

Runs from the SessionStart hook (see .claude/settings.json); stdout becomes context. Prints nothing when there is
nothing to say or when Omoikane is maintaining itself (OMOIKANE_NO_CAPTURE set), so those sessions pay no tokens.

Usage: python omoikane/bin/session-context.py [--budget 12000]
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from wikilib import OMOIKANE

NO_CAPTURE_ENV = "OMOIKANE_NO_CAPTURE"
# Undistilled captures listed by path; older ones are only counted. A stalled scheduler must not flood the brief.
PENDING_SESSIONS_SHOWN = 5
HEADER = (
    "Omoikane wiki brief follows: pending work, then the index. Open a page before touching the area it covers; "
    "decisions and gotchas "
    "record what earlier sessions learned the hard way. Do not write under omoikane/wiki/ during coding "
    "work: the session is captured on stop and distilled later. Rules: AGENTS.md."
)


def compact_index(text: str, budget: int) -> str:
    """Drop the generated header and fill the budget entry by entry, sections in index order (PAGE_TYPES).

    A section larger than the budget keeps its first entries instead of vanishing, so decisions and gotchas
    survive a long list of sources (#11). A last line names how many entries each section lost.

    Example: compact_index("# Index\\n\\nGenerated...\\n\\n## Decisions (2)\\n\\n- [[x]] — a\\n- [[y]] — b", 40)
    returns "## Decisions (2)\\n\\n- [[x]] — a\\n\\nOmitted by budget: Decisions 1. Read omoikane/index.md for them."
    """
    kept: list[str] = []
    omitted: list[str] = []
    used = 0
    for section in [s for s in text.split("\n## ") if s.strip()][1:]:
        heading, *lines = section.rstrip().splitlines()
        entries = [line for line in lines if line.startswith("- ")]
        cost = len(heading) + 4  # "## " plus the blank line after the heading
        fit = 0
        for entry in entries:
            if used + cost + len(entry) + 1 > budget:
                break
            cost += len(entry) + 1
            fit += 1
        if fit:
            kept.append("\n".join(["## " + heading, "", *entries[:fit]]))
            used += cost
        if fit < len(entries):
            omitted.append(f"{heading.split(' (')[0]} {len(entries) - fit}")
    if omitted:
        kept.append(f"Omitted by budget: {', '.join(omitted)}. Read omoikane/index.md for them.")
    return "\n\n".join(kept)


def pending_notes(omoikane: Path) -> str:
    """Name what is known but not in the wiki yet: captured sessions waiting for /distill, open review items.

    The newest undistilled capture is where the previous session stopped; pointing at it lets the agent resume
    without waiting for the scheduled distill.

    Example: pending_notes(Path("omoikane")) returns
    "## Pending\\n\\nCaptured sessions not yet distilled, ...\\n- `omoikane/raw/inbox/sessions/2026-09-15-e04462b2.md`".
    """
    lines: list[str] = []
    # File names start with the capture date, so name order is date order.
    sessions = sorted((omoikane / "raw" / "inbox" / "sessions").glob("*.md"))
    if sessions:
        lines.append("Captured sessions not yet distilled, oldest first; the last one is where the previous "
                     "session stopped:")
        if len(sessions) > PENDING_SESSIONS_SHOWN:
            lines.append(f"- ... {len(sessions) - PENDING_SESSIONS_SHOWN} older")
        lines += [f"- `{p.relative_to(omoikane.parent).as_posix()}`" for p in sessions[-PENDING_SESSIONS_SHOWN:]]
    review = omoikane / "_review.md"
    if review.is_file():
        open_items = sum(1 for line in review.read_text(encoding="utf-8").splitlines() if line.startswith("- "))
        if open_items:
            lines.append(f"{open_items} open items in omoikane/_review.md are waiting on the human.")
    return "## Pending\n\n" + "\n".join(lines) if lines else ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--budget", type=int, default=12_000, help="max characters of index to inject")
    args = parser.parse_args(argv)
    if os.environ.get(NO_CAPTURE_ENV):
        return 0
    index = OMOIKANE / "index.md"
    body = compact_index(index.read_text(encoding="utf-8"), args.budget) if index.is_file() else ""
    parts = [part for part in (pending_notes(OMOIKANE), body) if part]
    if parts:
        # Windows consoles default to a legacy code page; the index holds UTF-8 (em dashes, non-ASCII titles).
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(HEADER + "\n\n" + "\n\n".join(parts) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - context injection must never block a session from starting
        # stderr: the Pi extension and the OpenCode plugin inject stdout into the system prompt
        print(f"session-context: error {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(0)
