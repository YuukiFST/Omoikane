"""Headless tests for omoikane/bin/wiki-rules.py and context-budget.py. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "omoikane" / "bin"))

from wikilib import MAX_RULES, RULES_END, RULES_START, managed_rules  # noqa: E402

rules = importlib.import_module("wiki-rules")
budget = importlib.import_module("context-budget")


def agents_md(*lines: str) -> str:
    return "# Manual\n\n## Rules\n\n" + "\n".join([RULES_START, *lines, RULES_END]) + "\n\n## Domain\n"


REVIEW = """# Review queue

Intro.

## [2026-10-01] synthesize

- [x] rule eval-in-clone: Run the headless eval in a throwaway clone before a prompt PR. (synthesize)
- [ ] rule english-commits: Write commit messages in English. (synthesize)
- todo other: something else (synthesize)
"""


class Promote(unittest.TestCase):
    def test_ticked_rule_moves_into_the_block_and_leaves_the_queue(self) -> None:
        agents, review, problems = rules.promote(agents_md(), REVIEW, {"eval-in-clone", "english-commits"})
        self.assertEqual(problems, [])
        self.assertEqual(managed_rules(agents), [
            "- Run the headless eval in a throwaway clone before a prompt PR. "
            "(omoikane/wiki/practices/eval-in-clone.md)"])
        self.assertNotIn("eval-in-clone", review)
        self.assertIn("- [ ] rule english-commits", review)
        self.assertIn("- todo other", review)
        self.assertTrue(agents.startswith("# Manual\n\n## Rules\n\n") and agents.endswith("\n\n## Domain\n"))

    def test_at_the_cap_nothing_enters_and_the_proposal_stays(self) -> None:
        full = agents_md(*[f"- rule {i} (omoikane/wiki/practices/r{i}.md)" for i in range(MAX_RULES)])
        agents, review, problems = rules.promote(full, REVIEW, {"eval-in-clone"})
        self.assertEqual(agents, full)
        self.assertEqual(review, REVIEW)
        self.assertEqual(problems, [f"eval-in-clone: the block holds {MAX_RULES} rules, the cap; remove one from "
                                    "AGENTS.md first"])

    def test_refuses_a_rule_without_its_practice_page(self) -> None:
        agents, review, problems = rules.promote(agents_md(), REVIEW, set())
        self.assertEqual((agents, review), (agents_md(), REVIEW))
        self.assertEqual(problems, ["eval-in-clone: no page omoikane/wiki/practices/eval-in-clone.md"])

    def test_refuses_a_rule_longer_than_one_short_line(self) -> None:
        review = f"- [x] rule long: {'x' * (rules.MAX_RULE_CHARS + 1)} (synthesize)\n"
        _, left, problems = rules.promote(agents_md(), review, {"long"})
        self.assertEqual(left, review)
        self.assertEqual(problems, [f"long: rule is {rules.MAX_RULE_CHARS + 1} chars, limit {rules.MAX_RULE_CHARS}"])

    def test_a_rule_already_promoted_is_not_added_twice(self) -> None:
        once, _, _ = rules.promote(agents_md(), REVIEW, {"eval-in-clone"})
        twice, review, problems = rules.promote(once, REVIEW, {"eval-in-clone"})
        self.assertEqual(managed_rules(twice), managed_rules(once))
        self.assertNotIn("eval-in-clone", review)
        self.assertEqual(problems, [])

    def test_missing_block_is_an_error(self) -> None:
        with self.assertRaises(ValueError):
            rules.promote("# Manual\n", REVIEW, {"eval-in-clone"})


class ContextBudget(unittest.TestCase):
    LIMITS = {"AGENTS.md": 100, "skill frontmatter": 50, "session brief": 100, "total": 200}

    def test_within_budget_is_clean(self) -> None:
        self.assertEqual(budget.check(agents_md(), ["name: a"], "brief", self.LIMITS), [])

    def test_a_part_over_its_limit_is_a_finding(self) -> None:
        findings = budget.check(agents_md() + "x" * 400, [], "", self.LIMITS)
        self.assertEqual(len(findings), 1)
        self.assertRegex(findings[0], r"^AGENTS\.md: \d+ tokens, limit 100")

    def test_parts_under_their_limits_can_exceed_the_total(self) -> None:
        findings = budget.check(agents_md() + "x" * 250, ["x" * 170], "x" * 340, self.LIMITS)
        self.assertEqual(len(findings), 1)
        self.assertRegex(findings[0], r"^total: \d+ tokens, limit 200")

    def test_block_over_the_cap_or_missing_is_a_finding(self) -> None:
        over = agents_md(*[f"- r{i}" for i in range(MAX_RULES + 1)])
        self.assertIn(f"AGENTS.md: managed block holds {MAX_RULES + 1} rules, cap {MAX_RULES}",
                      budget.check(over, [], "", {k: 10_000 for k in self.LIMITS}))
        self.assertIn(f"AGENTS.md: managed block markers `{RULES_START}` ... `{RULES_END}` not found",
                      budget.check("# Manual\n", [], "", self.LIMITS))


if __name__ == "__main__":
    unittest.main()
