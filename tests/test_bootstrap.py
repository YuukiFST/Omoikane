"""Headless tests for omoikane/bin/bootstrap.py against real local git repositories.
Run: python -m unittest discover -s tests"""
from __future__ import annotations

import importlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "omoikane" / "bin"))

bootstrap = importlib.import_module("bootstrap")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def commit(repo: Path, files: dict[str, str], message: str) -> None:
    for name, text in files.items():
        write(repo / name, text)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)


class Bootstrap(unittest.TestCase):
    # A project that adopts Omoikane, or a system that replaces one, started with an empty wiki although its README,
    # docs, rule files and history already state its rules (#79).
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.project, self.omoikane = root / "shop", root / "new" / "omoikane"
        git(root, "init", "-q", "-b", "main", str(self.project))
        commit(self.project, {
            "README.md": "# Shop\n\nPrices are integer cents.\n",
            "docs/adr/0001-tenancy.md": "# Every table has a tenant_id\n",
            "CLAUDE.md": "Use the primary token for buttons.\n",
            ".cursor/rules/style.mdc": "No hex colours in components.\n",
            "src/total.py": "def total(): ...\n",
            "omoikane/wiki/domain/x.md": "an Omoikane page\n",
        }, "feat: start the shop\n\nCents because floats lost a cent on refunds.")
        commit(self.project, {"src/total.py": "def total(): return 0\n"}, "fix: clamp the total at zero")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def inbox(self) -> dict[str, str]:
        folder = self.omoikane / "raw" / "inbox"
        return {p.name: p.read_text(encoding="utf-8") for p in folder.glob("*.md")} if folder.is_dir() else {}

    def test_docs_rules_and_history_land_in_the_inbox(self) -> None:
        written = bootstrap.bootstrap(self.project, self.omoikane)
        files = self.inbox()
        self.assertEqual(sorted(files), sorted(written))
        self.assertEqual(sorted(files), ["bootstrap-claude-md.md", "bootstrap-cursor-rules-style-mdc.md",
                                         "bootstrap-docs-adr-0001-tenancy-md.md", "bootstrap-git-history.md",
                                         "bootstrap-readme-md.md"])
        readme = files["bootstrap-readme-md.md"]
        self.assertIn("Prices are integer cents.", readme)
        # /ingest dates a source by the date it bears: the file's last commit.
        self.assertIn("`README.md`", readme)
        self.assertRegex(readme, r"last changed \d{4}-\d{2}-\d{2}")
        history = files["bootstrap-git-history.md"]
        self.assertIn("feat: start the shop", history)
        self.assertIn("Cents because floats lost a cent on refunds.", history)
        self.assertIn("fix: clamp the total at zero", history)

    def test_a_second_run_writes_nothing_new(self) -> None:
        bootstrap.bootstrap(self.project, self.omoikane)
        ingested = self.omoikane / "raw" / "sources" / "bootstrap-readme-md.md"
        write(ingested, "ingested")
        (self.omoikane / "raw" / "inbox" / "bootstrap-readme-md.md").unlink()
        write(self.omoikane / "raw" / "inbox" / "bootstrap-claude-md.md", "edited by the human")
        self.assertEqual(bootstrap.bootstrap(self.project, self.omoikane), [])
        self.assertEqual(self.inbox()["bootstrap-claude-md.md"], "edited by the human")
        self.assertNotIn("bootstrap-readme-md.md", self.inbox())

    def test_what_the_template_shipped_is_skipped(self) -> None:
        # A system born from the template still holds the template's README, manual and history until it changes
        # them; they describe Omoikane, not the system (new-system.py renames origin to template).
        template = Path(self.tmp.name) / "template"
        git(Path(self.tmp.name), "clone", "-q", str(self.project), str(template))
        system = Path(self.tmp.name) / "system"
        git(Path(self.tmp.name), "clone", "-q", "-o", "template", str(template), str(system))
        commit(system, {"README.md": "# Store\n\nRefunds go back to the card.\n"}, "docs: describe the store")
        bootstrap.bootstrap(system, self.omoikane)
        files = self.inbox()
        self.assertEqual(sorted(files), ["bootstrap-git-history.md", "bootstrap-readme-md.md"])
        self.assertIn("Refunds go back to the card.", files["bootstrap-readme-md.md"])
        self.assertIn("docs: describe the store", files["bootstrap-git-history.md"])
        self.assertNotIn("feat: start the shop", files["bootstrap-git-history.md"])

    def test_outside_a_git_repository_it_says_why(self) -> None:
        plain = Path(self.tmp.name) / "plain"
        plain.mkdir()
        result = subprocess.run([sys.executable, str(Path(bootstrap.__file__)), "--from", str(plain)],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not a git repository", result.stderr)


if __name__ == "__main__":
    unittest.main()
