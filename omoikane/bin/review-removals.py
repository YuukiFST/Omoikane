"""Record in log.md the proposals and todos whose bullet the human deleted from _review.md.

Deleting a bullet is how the human rejects a proposal, and how an interactive session clears one it applied.
Either way the item is decided and must not be filed again, but the deletion left no trace, so the next /distill
of a session with the same lesson filed it again (#41). wiki-ingest.ps1 runs this before any operation; /distill
and /synthesize read the `- removed` lines.
Usage: python omoikane/bin/review-removals.py [--omoikane DIR]
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

from wikilib import OMOIKANE, review_bullets

# `- routed (<kind>) <slug>:` from /distill and /synthesize, `- removed (<kind>) <slug>` from this script.
EVENT = re.compile(r"^- (routed|removed) \((guard|prompt|todo|rule)\) ([\w.-]+)", re.MULTILINE)
# `- [ ] guard (test) <slug>:`, `- [x] prompt (distill.md) <slug>:`, `- [ ] rule <slug>:`, `- todo <slug>:`
BULLET = re.compile(r"- (?:\[[ xX]\] )?(?:guard|prompt|rule|todo)(?: \([^)]*\))? ([\w.-]+):")


def removed(log: str, review: str) -> list[tuple[str, str]]:
    """(kind, slug) for each slug whose last log event is `routed` and that has no bullet left in _review.md.

    Example: removed("- routed (guard) a: x\\n", "# Review queue\\n") returns [("guard", "a")].
    """
    last: dict[str, tuple[str, str]] = {}
    for event, kind, slug in EVENT.findall(log):
        last[slug] = (event, kind)
    open_slugs = {m.group(1) for line in review_bullets(review) if (m := BULLET.match(line))}
    return [(kind, slug) for slug, (event, kind) in last.items() if event == "routed" and slug not in open_slugs]


def record(log: str, items: list[tuple[str, str]], today: str) -> str:
    """`log` with one entry listing `items` appended.

    Example: record("# Log\\n", [("rule", "a")], "2026-10-01") returns
    "# Log\\n\\n## [2026-10-01] review | removed from _review.md\\n\\n- removed (rule) a\\n".
    """
    lines = [f"- removed ({kind}) {slug}" for kind, slug in items]
    return log.rstrip("\n") + f"\n\n## [{today}] review | removed from _review.md\n\n" + "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--omoikane", type=Path, default=OMOIKANE)
    args = parser.parse_args(argv)
    log_path, review_path = args.omoikane / "log.md", args.omoikane / "_review.md"
    if not log_path.is_file() or not review_path.is_file():
        return 0
    log = log_path.read_text(encoding="utf-8")
    items = removed(log, review_path.read_text(encoding="utf-8"))
    if items:
        log_path.write_text(record(log, items, date.today().isoformat()), encoding="utf-8", newline="\n")
        print(f"review-removals: {len(items)} item(s) removed from _review.md recorded in log.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
