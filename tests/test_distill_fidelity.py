"""Headless tests for omoikane/bin/distill-fidelity.py. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import importlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "omoikane" / "bin"
FIXTURES = ROOT / "tests" / "fixtures"
SCRIPT = BIN / "distill-fidelity.py"
sys.path.insert(0, str(BIN))

fidelity = importlib.import_module("distill-fidelity")

DOMAIN = FIXTURES / "distill-domain-session.md"
SOURCE = "wiki/sources/session-2026-10-02-0eva1d0m.md"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def page(kind: str, sources: str, body: str) -> str:
    return (f"---\ntitle: t\ntype: {kind}\nsummary: s\ntags: []\ncreated: 2026-10-15\nupdated: 2026-10-15\n"
            f"sources: [{sources}]\n---\n{body}\n")


class Prepare(unittest.TestCase):
    def test_inbox_copy_drops_the_answer_key_and_keeps_every_other_byte(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            done = run("prepare", d, str(DOMAIN))
            self.assertEqual(done.returncode, 0, done.stderr)
            copy = (Path(d) / "raw" / "inbox" / "sessions" / "2026-10-02-0eva1d0m.md").read_bytes()
        original = DOMAIN.read_bytes()
        self.assertNotIn(b"must_", copy)
        expected = b"".join(line for line in original.splitlines(keepends=True) if not line.startswith(b"must_"))
        self.assertEqual(copy, expected)


class Score(unittest.TestCase):
    def test_lost_string_and_must_not_on_a_rule_page_fail(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            # A must_not string on the source page is history, not a rule: it must not count.
            write(root, SOURCE, page("source", "", "The user said: Deixa esse botão azul por enquanto (turn 2)."))
            # The line wrap inside the first string is not a paraphrase.
            write(root, "wiki/domain/money-in-integer-cents.md", page(
                "domain", SOURCE, "todo valor monetário é guardado e calculado em centavos\n  inteiros (turn 1).\n"
                "Never use float: nunca float. The button got variant=\"info\" (turn 2)."))
            write(root, "log.md", "## [2026-10-15] distill | session 0eva1d0m\n"
                  "- botão primário sempre usa o token `color.action.primary`\n"
                  "## [2026-10-15] ingest | other\n- nunca cor hex direto no componente\n")
            done = run("score", d, str(DOMAIN))
        self.assertEqual(done.stdout, "distill-domain-session.md: kept 3/4\n"
                                      '  lost: "nunca cor hex direto no componente"\n'
                                      '  must_not: "variant="info"" on wiki/domain/money-in-integer-cents.md\n'
                                      "total: kept 3/4, must_not hits 1, fixture errors 0\n")
        self.assertEqual(done.returncode, 1)

    def test_every_string_kept_and_no_must_not_passes(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write(root, SOURCE, page("source", "", "todo valor monetário é guardado e calculado em centavos inteiros, "
                                     "nunca float (turn 1)."))
            write(root, "_review.md", "## [2026-10-15] distill | session 0eva1d0m\n- todo button-colour: botão "
                  "primário sempre usa o token `color.action.primary`, nunca cor hex direto no componente\n")
            done = run("score", d, str(DOMAIN))
        self.assertEqual(done.stdout, "distill-domain-session.md: kept 4/4\n"
                                      "total: kept 4/4, must_not hits 0, fixture errors 0\n")
        self.assertEqual(done.returncode, 0)

    def test_unwinnable_key_and_undistilled_session_are_fixture_errors(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            fixture = Path(d) / "distill-x.md"
            write(Path(d), "distill-x.md", "---\nsession: abc-12345678\nstarted: 2026-10-15T09:00:00Z\n"
                  "must_mention: [said once]\nmust_not_mention: []\n---\nThe user never said it.\n")
            done = run("score", str(Path(d) / "omoikane"), str(fixture))
        self.assertEqual(done.stdout, "distill-x.md: kept 0/1\n"
                                      '  lost: "said once"\n'
                                      '  error: must_mention not in the fixture body: "said once"\n'
                                      "  error: not distilled: no source page and no log section for session 12345678\n"
                                      "total: kept 0/1, must_not hits 0, fixture errors 2\n")
        self.assertEqual(done.returncode, 1)


class Fixtures(unittest.TestCase):
    def test_every_distill_fixture_has_a_winnable_answer_key(self) -> None:
        paths = sorted(FIXTURES.glob("distill-*.md"))
        self.assertEqual(len(paths), 6)
        for path in paths:
            fx = fidelity.parse_fixture(path.name, path.read_text(encoding="utf-8"))
            with self.subTest(fixture=path.name):
                self.assertTrue(fx.must_mention)
                for s in fx.must_mention:
                    self.assertTrue(fidelity.contains(fx.body, s), s)

    def test_key_strings_survive_the_frontmatter_parser_verbatim(self) -> None:
        # wikilib splits inline lists on commas only: quotes, backticks and colons stay in the string.
        domain = fidelity.parse_fixture(DOMAIN.name, DOMAIN.read_text(encoding="utf-8"))
        self.assertIn("botão primário sempre usa o token `color.action.primary`", domain.must_mention)
        self.assertEqual(domain.must_not_mention, ["Deixa esse botão azul por enquanto", 'variant="info"'])
        path = FIXTURES / "distill-domain-session-3.md"
        shipping = fidelity.parse_fixture(path.name, path.read_text(encoding="utf-8"))
        self.assertEqual(shipping.must_not_mention, ["shipping_fee(subtotal: float) -> float"])


if __name__ == "__main__":
    unittest.main()
