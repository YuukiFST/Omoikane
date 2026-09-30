"""Measure what every Claude Code session loads before its first prompt, and fail above the budget.

Parts: AGENTS.md (CLAUDE.md only imports it), the frontmatter of each .claude/skills/*/SKILL.md (the harness
injects every skill description), and the output of session-context.py. Also fails when the managed rules
block of AGENTS.md is missing or holds more than MAX_RULES. Runs in CI; nothing grows silently.

Tokens are estimated at 3.5 characters each, no tokenizer dependency. English prose runs nearer 4, so the
estimate errs high and the budget stays conservative.
Usage: python omoikane/bin/context-budget.py
"""
from __future__ import annotations

import math
import os
import subprocess
import sys

from wikilib import FRONTMATTER, MAX_RULES, OMOIKANE, REPO, RULES_END, RULES_START, managed_rules

CHARS_PER_TOKEN = 3.5
# AGENTS.md is ~1,550 tokens; 15 promoted rules of ~40 tokens each add ~600. The brief is bounded by
# session-context.py's own 12,000-character index budget (~3,430 tokens) plus its header and pending notes.
LIMITS = {"AGENTS.md": 2_500, "skill frontmatter": 600, "session brief": 4_000, "total": 6_500}


def tokens(text: str) -> int:
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def measure(agents: str, frontmatters: list[str], brief: str) -> dict[str, int]:
    """Estimated tokens per part, plus their total.

    Example: measure("x" * 35, [], "") returns {"AGENTS.md": 10, "skill frontmatter": 0, "session brief": 0,
    "total": 10}.
    """
    parts = {"AGENTS.md": tokens(agents), "skill frontmatter": sum(map(tokens, frontmatters)),
             "session brief": tokens(brief)}
    parts["total"] = sum(parts.values())
    return parts


def check(agents: str, frontmatters: list[str], brief: str, limits: dict[str, int] = LIMITS) -> list[str]:
    """Return one finding per part over its limit, and per problem with the managed rules block.

    Example: check("x" * 10_000, [], "") returns ["AGENTS.md: 2858 tokens, limit 2500; ...", "AGENTS.md: managed
    block markers ... not found"].
    """
    parts = measure(agents, frontmatters, brief)
    findings = [f"{name}: {used} tokens, limit {limits[name]}; move text to a page or skill read on demand "
                "before adding more" for name, used in parts.items() if used > limits[name]]
    block = managed_rules(agents)
    if block is None:
        findings.append(f"AGENTS.md: managed block markers `{RULES_START}` ... `{RULES_END}` not found")
    elif len(block) > MAX_RULES:
        findings.append(f"AGENTS.md: managed block holds {len(block)} rules, cap {MAX_RULES}")
    return findings


def session_brief() -> str:
    """Run session-context.py as the SessionStart hook does, without the variable that silences it."""
    env = {k: v for k, v in os.environ.items() if k != "OMOIKANE_NO_CAPTURE"}
    run = subprocess.run([sys.executable, str(OMOIKANE / "bin" / "session-context.py")], capture_output=True,
                         text=True, encoding="utf-8", env=env, check=False)
    return run.stdout


def main() -> int:
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    frontmatters = []
    for skill in sorted((REPO / ".claude" / "skills").glob("*/SKILL.md")):
        m = FRONTMATTER.match(skill.read_text(encoding="utf-8"))
        frontmatters.append(m.group(1) if m else "")
    brief = session_brief()
    findings = check(agents, frontmatters, brief)
    for name, n in measure(agents, frontmatters, brief).items():
        print(f"{name:<18} {n:>6} / {LIMITS[name]} tokens (estimated)")
    for f in findings:
        print(f)
    print(f"context-budget: {len(findings)} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
