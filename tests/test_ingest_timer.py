"""Headless tests for omoikane/bin/ingest-timer.py with a fake clock. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import importlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "omoikane" / "bin"))

timer = importlib.import_module("ingest-timer")
MINUTE = 60.0


class Clock:
    """Fake time: sleep advances it and fires the turns scheduled for the moment it reaches."""

    def __init__(self) -> None:
        self.t = 1_000_000.0
        self.events: list[tuple[float, object]] = []

    def now(self) -> float:
        return self.t

    def at(self, t: float, action: object) -> None:
        self.events.append((t, action))

    def sleep(self, seconds: float) -> None:
        self.t += seconds
        for when, action in sorted(self.events, key=lambda e: e[0]):
            if when <= self.t:
                self.events.remove((when, action))
                action()  # type: ignore[operator]


class IngestTimer(unittest.TestCase):
    """The scheduled ingest starts when a session goes quiet, counted from its last turn, one run at a time (#96)."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.state = Path(self.tmp.name)
        self.clock = Clock()
        self.runs: list[tuple[float, str]] = []
        self.spawned = 0

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def arm(self, delay: float = 31 * MINUTE, agent: str = "claude") -> None:
        def spawn() -> None:
            self.spawned += 1
        timer.arm(self.state, delay, agent, now=self.clock.now, spawn=spawn)

    def wait(self) -> str:
        def run(agent: str) -> None:
            self.runs.append((self.clock.now(), agent))
        return timer.wait(self.state, run, now=self.clock.now, sleep=self.clock.sleep)

    def test_each_turn_postpones_the_run_to_the_end_of_the_quiet_period(self) -> None:
        start = self.clock.t
        self.arm()
        self.clock.at(start + 20 * MINUTE, self.arm)
        self.wait()
        self.assertEqual(len(self.runs), 1)
        self.assertGreaterEqual(self.runs[0][0], start + 51 * MINUTE)
        self.assertEqual(self.spawned, 2)

    def test_a_second_waiter_leaves_while_the_first_holds_the_lock(self) -> None:
        self.arm()
        held = timer.try_lock(self.state)
        self.assertIsNotNone(held)
        try:
            self.assertEqual(self.wait(), "another waiter holds the lock")
        finally:
            held.close()  # type: ignore[union-attr]
        self.assertEqual(self.runs, [])

    def test_a_turn_during_a_run_leads_to_one_more_run(self) -> None:
        self.arm(0)

        def run(agent: str) -> None:
            self.runs.append((self.clock.now(), agent))
            if len(self.runs) == 1:
                self.arm()
        timer.wait(self.state, run, now=self.clock.now, sleep=self.clock.sleep)
        self.assertEqual(len(self.runs), 2)
        self.assertGreaterEqual(self.runs[1][0] - self.runs[0][0], 31 * MINUTE)

    def test_the_daily_start_neither_advances_nor_drops_a_pending_session(self) -> None:
        start = self.clock.t
        self.arm(agent="opencode")
        self.arm(0)
        self.wait()
        self.assertEqual(self.runs, [(start + 31 * MINUTE, "opencode")])

    def test_a_due_time_already_past_runs_at_once(self) -> None:
        start = self.clock.t
        self.arm(0)
        self.assertEqual(self.wait(), "ran 1")
        self.assertEqual(self.runs, [(start, "claude")])

    def test_no_due_time_means_no_run(self) -> None:
        self.assertEqual(self.wait(), "ran 0")
        self.assertEqual(self.runs, [])


if __name__ == "__main__":
    unittest.main()
