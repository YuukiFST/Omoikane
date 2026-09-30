"""Headless tests for omoikane/bin/review-ticks.py. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "omoikane" / "bin"))

ticks = importlib.import_module("review-ticks")

BEFORE = "# Review queue\n\n- [x] guard (test) a: approved by the human (session 1, turn 1)\n- [ ] rule b: Do b. (synthesize)\n"


class UntickNew(unittest.TestCase):
    def test_a_tick_the_agent_added_is_undone_and_the_human_ones_kept(self) -> None:
        # Approval is the human's act; the scheduled run can edit _review.md, so it could approve itself.
        after = BEFORE.replace("- [ ] rule b", "- [x] rule b") + "- [X] rule c: Do c. (synthesize)\n- [ ] prompt d: new\n"
        text, undone = ticks.untick_new(BEFORE, after)
        self.assertEqual(undone, 2)
        self.assertEqual(text, BEFORE + "- [ ] rule c: Do c. (synthesize)\n- [ ] prompt d: new\n")

    def test_nothing_changes_when_the_agent_ticked_nothing(self) -> None:
        after = BEFORE + "- todo e: e\n"
        self.assertEqual(ticks.untick_new(BEFORE, after), (after, 0))


if __name__ == "__main__":
    unittest.main()
