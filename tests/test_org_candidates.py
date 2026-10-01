"""Headless tests for omoikane/bin/org-candidates.py. Run: python -m unittest discover -s tests

Each system is a throwaway repository with an Omoikane wiki; the script runs as the organisation would run it (#52).
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "omoikane" / "bin" / "org-candidates.py"
SECRET = "customer ACME-0042 invoice"


def page(root: Path, folder: str, slug: str, kind: str, summary: str, **extra: str) -> None:
    path = root / "omoikane/wiki" / folder / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = "".join(f"{k.replace('_', '-')}: {v}\n" for k, v in extra.items())
    path.write_text(f"---\ntitle: {slug}\ntype: {kind}\nsummary: {summary}\ntags: []\ncreated: 2026-09-01\n"
                    f"updated: 2026-09-02\nsources: [wiki/sources/session-2026-09-01-aaaa0001.md]\n{keys}---\n"
                    f"Body that quotes the session: {SECRET}.\n", encoding="utf-8")


class OrgCandidates(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.billing, self.portal, self.stock = (self.root / n for n in ("billing", "portal", "stock"))
        page(self.billing, "gotchas", "orm-drops-time-zone", "gotcha", "The ORM drops the time zone", guard="test")
        page(self.portal, "gotchas", "orm-drops-time-zone", "gotcha", "Timestamps lose their zone", guard="none")
        page(self.billing, "decisions", "money-as-integer-cents", "decision", "Money is stored as integer cents",
             org="money-in-cents")
        page(self.stock, "practices", "store-amounts-in-cents", "practice", "Store amounts in cents",
             org="money-in-cents")
        page(self.billing, "gotchas", "only-billing-knows", "gotcha", "One system only", guard="lint")
        page(self.portal, "gotchas", "pruned-twice", "gotcha", "Marked for deletion", guard="none", prune="stale")
        page(self.stock, "gotchas", "pruned-twice", "gotcha", "Marked for deletion", guard="none", prune="stale")
        page(self.portal, "concepts", "orm", "concept", "Concepts are not lessons")
        page(self.stock, "concepts", "orm", "concept", "Concepts are not lessons")
        raw = self.portal / "omoikane/raw/sources/sessions/2026-09-01-aaaa0001.md"
        raw.parent.mkdir(parents=True)
        raw.write_text(f"orm-drops-time-zone {SECRET}\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_script(self, *systems: Path, fmt: str = "json") -> subprocess.CompletedProcess[str]:
        args = [arg for s in systems for arg in ("--system", f"{s.name}={s}")]
        return subprocess.run([sys.executable, str(SCRIPT), *args, "--format", fmt], capture_output=True, text=True,
                              encoding="utf-8")

    def candidates(self, *systems: Path) -> dict[str, dict[str, object]]:
        run = self.run_script(*systems)
        self.assertEqual(run.returncode, 0, run.stderr)
        return {c["key"]: c for c in json.loads(run.stdout)}

    def test_a_lesson_in_two_systems_is_a_candidate_with_the_evidence_of_each(self) -> None:
        found = self.candidates(self.billing, self.portal, self.stock)
        self.assertEqual(set(found), {"orm-drops-time-zone", "money-in-cents"})
        self.assertEqual([(e["system"], e["page"], e["guard"]) for e in found["orm-drops-time-zone"]["evidence"]],  # type: ignore[index,union-attr]
                         [("billing", "omoikane/wiki/gotchas/orm-drops-time-zone.md", "test"),
                          ("portal", "omoikane/wiki/gotchas/orm-drops-time-zone.md", "none")])

    def test_the_org_key_joins_pages_of_different_names(self) -> None:
        evidence = self.candidates(self.billing, self.stock)["money-in-cents"]["evidence"]
        self.assertEqual([e["page"] for e in evidence], ["omoikane/wiki/decisions/money-as-integer-cents.md",  # type: ignore[union-attr,index]
                                                         "omoikane/wiki/practices/store-amounts-in-cents.md"])

    def test_the_strongest_guard_any_system_has_is_reported(self) -> None:
        # The organisation's guard starts from the best check one system already runs.
        self.assertEqual(self.candidates(self.billing, self.portal)["orm-drops-time-zone"]["guard"], "test")

    def test_one_system_named_twice_is_one_system(self) -> None:
        self.assertEqual(self.candidates(self.billing, self.billing), {})

    def test_only_distilled_summaries_leave_the_system(self) -> None:
        # Raw captures and page bodies may quote customer data; the organisation gets summaries and paths only.
        for fmt in ("json", "markdown"):
            with self.subTest(fmt):
                run = self.run_script(self.billing, self.portal, self.stock, fmt=fmt)
                self.assertNotIn(SECRET, run.stdout)

    def test_markdown_lists_each_candidate_with_its_systems(self) -> None:
        out = self.run_script(self.billing, self.portal, fmt="markdown").stdout
        self.assertIn("- candidate (gotcha) orm-drops-time-zone: The ORM drops the time zone (2 systems, guard test)", out)
        self.assertIn("  - portal: Timestamps lose their zone (omoikane/wiki/gotchas/orm-drops-time-zone.md, guard none)", out)

    def test_a_path_without_a_wiki_is_an_error(self) -> None:
        run = self.run_script(self.billing, self.root / "nowhere")
        self.assertEqual(run.returncode, 2)
        self.assertIn("nowhere", run.stderr)


if __name__ == "__main__":
    unittest.main()
