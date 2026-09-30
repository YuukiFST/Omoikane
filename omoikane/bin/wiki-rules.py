"""Promote the rule proposals the human ticked in _review.md into the managed block of AGENTS.md.

Only a ticked `- [x] rule <slug>: <rule> (...)` bullet is promoted, and only while the block holds fewer than
MAX_RULES; the applied bullet leaves _review.md. The human runs this, never the scheduled headless run: its
permissions do not include this script, so an agent cannot tick a box and promote in the same run.
Usage: python omoikane/bin/wiki-rules.py
"""
from __future__ import annotations

import re
import sys

from wikilib import MAX_RULES, OMOIKANE, REPO, RULES_END, managed_rules

# One short imperative line; a rule that needs a paragraph is a page, not an always-loaded rule.
MAX_RULE_CHARS = 160
TICKED_RULE = re.compile(r"- \[[xX]\] rule ([a-z0-9-]+): (.+?)(?: \([^()]*\))?\s*$")


def promote(agents: str, review: str, practices: set[str]) -> tuple[str, str, list[str]]:
    """Move each ticked rule proposal of `review` into the managed block of `agents`.

    `practices` holds the slugs of the existing practice pages; a rule points at its page. Returns the new
    AGENTS.md, the new _review.md, and one line per proposal left in place with the reason. Raises ValueError
    when AGENTS.md has no managed block.
    Example: promote(agents, "- [x] rule s: Do y. (synthesize)\\n", {"s"}) returns
    (agents with "- Do y. (omoikane/wiki/practices/s.md)" in the block, "", []).
    """
    block = managed_rules(agents)
    if block is None:
        raise ValueError("AGENTS.md has no managed rules block")
    added: list[str] = []
    kept: list[str] = []
    problems: list[str] = []
    for line in review.splitlines(keepends=True):
        m = TICKED_RULE.match(line)
        if not m:
            kept.append(line)
            continue
        slug, rule = m.group(1), m.group(2).strip()
        entry = f"- {rule} (omoikane/wiki/practices/{slug}.md)"
        problem = ""
        if slug not in practices:
            problem = f"no page omoikane/wiki/practices/{slug}.md"
        elif len(rule) > MAX_RULE_CHARS:
            problem = f"rule is {len(rule)} chars, limit {MAX_RULE_CHARS}"
        elif entry not in block + added and len(block) + len(added) >= MAX_RULES:
            problem = f"the block holds {MAX_RULES} rules, the cap; remove one from AGENTS.md first"
        if problem:
            problems.append(f"{slug}: {problem}")
            kept.append(line)
        elif entry not in block + added:
            added.append(entry)
    if not added:
        return agents, "".join(kept), problems
    end = agents.find(RULES_END)
    return agents[:end] + "".join(f"{e}\n" for e in added) + agents[end:], "".join(kept), problems


def main() -> int:
    agents_path, review_path = REPO / "AGENTS.md", OMOIKANE / "_review.md"
    practices = {p.stem for p in (OMOIKANE / "wiki" / "practices").glob("*.md")}
    agents, review = agents_path.read_text(encoding="utf-8"), review_path.read_text(encoding="utf-8")
    new_agents, new_review, problems = promote(agents, review, practices)
    if new_agents != agents:
        agents_path.write_text(new_agents, encoding="utf-8", newline="\n")
    if new_review != review:
        review_path.write_text(new_review, encoding="utf-8", newline="\n")
    for problem in problems:
        print(f"not promoted: {problem}")
    print(f"wiki-rules: {len(managed_rules(new_agents) or [])} of {MAX_RULES} rules in AGENTS.md")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
