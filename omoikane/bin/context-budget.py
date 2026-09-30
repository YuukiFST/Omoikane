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
# AGENTS.md is ~1,700 tokens with an empty rules block; a full block (15 rules of at most 120 characters plus a
# page pointer of up to ~90, ~65 tokens each) adds ~950, which tests/test_wiki_rules.py checks against the real
# file. The brief is bounded by session-context.py's own 12,000-character index budget (~3,430 tokens) plus its
# header and pending notes. In CI the wiki is empty, so the brief limit bites in a repository with a real wiki,
# where this script also runs.
LIMITS = {"AGENTS.md": 2_800, "skill frontmatter": 600, "session brief": 4_000, "total": 7_000}


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


def check(agents: str, frontmatters: list[str], brief: str, limits: dict[str, int] = LIMITS,
          brief_error: str = "") -> list[str]:
    """Return one finding per part over its limit, per problem with the managed rules block, and for a brief
    that failed: session-context.py always exits 0, so its stderr is the only sign a crash measured 0 tokens.

    Example: check("x" * 10_000, [], "") returns ["AGENTS.md: 2858 tokens, limit 2800; ...", "AGENTS.md: managed
    block markers ... not found"].
    """
    parts = measure(agents, frontmatters, brief)
    findings = [f"{name}: {used} tokens, limit {limits[name]}; move text to a page or skill read on demand "
                "before adding more" for name, used in parts.items() if used > limits[name]]
    if brief_error.strip():
        findings.append(f"session brief: session-context.py failed: {brief_error.strip()}")
    block = managed_rules(agents)
    if block is None:
        findings.append(f"AGENTS.md: managed block markers `{RULES_START}` ... `{RULES_END}` not found")
    elif len(block) > MAX_RULES:
        findings.append(f"AGENTS.md: managed block holds {len(block)} rules, cap {MAX_RULES}")
    return findings


def session_brief() -> tuple[str, str]:
    """Run session-context.py as the SessionStart hook does, without the variable that silences it.

    Returns (stdout, stderr). Example: session_brief() returns ("Omoikane wiki brief follows: ...", "").
    """
    env = {k: v for k, v in os.environ.items() if k != "OMOIKANE_NO_CAPTURE"}
    run = subprocess.run([sys.executable, str(OMOIKANE / "bin" / "session-context.py")], capture_output=True,
                         text=True, encoding="utf-8", env=env, check=False)
    return run.stdout, run.stderr


def main() -> int:
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    frontmatters = []
    for skill in sorted((REPO / ".claude" / "skills").glob("*/SKILL.md")):
        m = FRONTMATTER.match(skill.read_text(encoding="utf-8"))
        frontmatters.append(m.group(1) if m else "")
    brief, error = session_brief()
    findings = check(agents, frontmatters, brief, brief_error=error)
    for name, n in measure(agents, frontmatters, brief).items():
        print(f"{name:<18} {n:>6} / {LIMITS[name]} tokens (estimated)")
    for f in findings:
        print(f)
    print(f"context-budget: {len(findings)} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
