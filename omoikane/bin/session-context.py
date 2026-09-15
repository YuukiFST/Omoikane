"""Print the wiki index for the harness to add to the agent's context at session start.

Runs from the SessionStart hook (see .claude/settings.json); stdout becomes context. Prints nothing when the
wiki is empty or when Omoikane is maintaining itself (OMOIKANE_NO_CAPTURE set), so those sessions pay no tokens.

Usage: python omoikane/bin/session-context.py [--budget 12000]
"""
from __future__ import annotations

import argparse
import os
import sys

from wikilib import OMOIKANE

NO_CAPTURE_ENV = "OMOIKANE_NO_CAPTURE"
HEADER = (
    "Omoikane wiki index follows. Open a page before touching the area it covers; decisions and gotchas "
    "record what earlier sessions learned the hard way. Do not write under omoikane/wiki/ during coding "
    "work: the session is captured on stop and distilled later. Rules: AGENTS.md."
)


def compact_index(text: str, budget: int) -> str:
    """Drop the generated header and cut whole sections from the end until the index fits the budget.

    Example: compact_index("# Index\\n\\nGenerated...\\n\\n## Decisions (1)\\n- [[x]] ...", 12000)
    returns "## Decisions (1)\\n- [[x]] ...".
    """
    sections = [s for s in text.split("\n## ") if s.strip()][1:]
    kept: list[str] = []
    used = 0
    for section in sections:
        block = "## " + section.rstrip()
        if used + len(block) > budget:
            kept.append(f"## Index truncated at {budget} chars; read omoikane/index.md for the remaining sections.")
            break
        kept.append(block)
        used += len(block)
    return "\n\n".join(kept)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--budget", type=int, default=12_000, help="max characters of index to inject")
    args = parser.parse_args(argv)
    if os.environ.get(NO_CAPTURE_ENV):
        return 0
    index = OMOIKANE / "index.md"
    if not index.is_file():
        return 0
    body = compact_index(index.read_text(encoding="utf-8"), args.budget)
    if body:
        # Windows consoles default to a legacy code page; the index holds UTF-8 (em dashes, non-ASCII titles).
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(HEADER + "\n\n" + body + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - context injection must never block a session from starting
        print(f"session-context: error {type(exc).__name__}: {exc}")
        sys.exit(0)
