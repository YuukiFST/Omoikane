"""Headless tests for omoikane/bin/new-system.py, run on a copy of this repository as a user would after cloning.
Run: python -m unittest discover -s tests"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "omoikane" / "bin"))

from wikilib import RULES_END, RULES_START, managed_rules  # noqa: E402


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
                          capture_output=True, text=True, check=True).stdout


def run(repo: Path, script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(repo / "omoikane" / "bin" / script)], cwd=repo, capture_output=True,
                          text=True, encoding="utf-8")


class NewSystem(unittest.TestCase):
    # A clone of the template carried Omoikane's own wiki, log, review queue and captures, and the brief injected
    # them into every session of the new system (#66).
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "shop"
        tracked = git(REPO, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split("\0")
        for name in filter(None, tracked):
            source = REPO / name
            if source.is_file():
                (self.repo / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, self.repo / name)
        # A capture and a page the template's own history left behind, of the kinds a clone carries.
        (self.repo / "omoikane/raw/inbox/sessions/2026-10-01-abcdef12.md").write_text("capture", encoding="utf-8")
        (self.repo / "omoikane/wiki/concepts/template-concept.md").write_text("---\ntitle: x\n---\n", encoding="utf-8")
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "clone of the template")
        # A clone's origin is the template; the review gate fetches and pushes wiki/auto there.
        git(self.repo, "remote", "add", "origin", "https://example.invalid/template.git")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_a_fresh_clone_becomes_an_empty_memory(self) -> None:
        omoikane = self.repo / "omoikane"
        prompts = {p.name: p.read_text(encoding="utf-8") for p in (omoikane / "prompts").glob("*.md")}
        agents = (self.repo / "AGENTS.md").read_text(encoding="utf-8")

        result = run(self.repo, "new-system.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        for folder in ("wiki", "raw/sources", "raw/inbox", "raw/assets"):
            left = [p.relative_to(omoikane).as_posix() for p in (omoikane / folder).rglob("*") if p.is_file()]
            self.assertTrue(all(name.endswith("/.gitkeep") for name in left), left)
        self.assertTrue((omoikane / "wiki/decisions/.gitkeep").is_file())
        log = (omoikane / "log.md").read_text(encoding="utf-8")
        self.assertTrue(log.startswith("# Log\n\nAppend-only."), log)
        self.assertEqual(log.count("## ["), 1, log)
        self.assertIn(f"## [{date.today().isoformat()}] init |", log)
        review = (omoikane / "_review.md").read_text(encoding="utf-8")
        self.assertTrue(review.startswith("# Review queue\n"))
        self.assertNotIn("## [", review)
        self.assertNotIn("[[", (omoikane / "index.md").read_text(encoding="utf-8"))

        new_agents = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(managed_rules(new_agents), [])
        outside = lambda text: text[:text.index(RULES_START)] + text[text.index(RULES_END):]  # noqa: E731
        self.assertEqual(outside(new_agents), outside(agents))
        self.assertEqual({p.name: p.read_text(encoding="utf-8") for p in (omoikane / "prompts").glob("*.md")},
                         prompts)

        lint = run(self.repo, "wiki-lint.py")
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        self.assertNotIn("[[", run(self.repo, "session-context.py").stdout)
        self.assertEqual(run(self.repo, "context-budget.py").returncode, 0)
        # The new system's pages must never be published to the template (review-gate.py publishes to origin).
        self.assertEqual(git(self.repo, "remote").split(), ["template"])

    def test_refuses_a_tree_with_uncommitted_changes(self) -> None:
        # Nothing is committed by the script, so git restore undoes a run; that holds only from a clean tree. An
        # untracked capture is the worst case: git restore cannot bring it back.
        for path, text in (("AGENTS.md", "edited\n"), ("omoikane/raw/inbox/sessions/2026-10-02-new00000.md", "x")):
            with self.subTest(path=path):
                (self.repo / path).write_text(text, encoding="utf-8")
                result = run(self.repo, "new-system.py")
                self.assertEqual(result.returncode, 2)
                self.assertIn(Path(path).name, result.stdout)
                self.assertTrue((self.repo / "omoikane/wiki/concepts/template-concept.md").is_file())
                git(self.repo, "checkout", "-q", "--", ".")
                git(self.repo, "clean", "-q", "-f")

    def test_outside_a_git_clone_it_explains_and_stops(self) -> None:
        shutil.rmtree(self.repo / ".git", onerror=lambda f, p, e: (Path(p).chmod(0o700), f(p)))
        result = run(self.repo, "new-system.py")
        self.assertEqual(result.returncode, 2)
        self.assertIn("git clone", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        self.assertTrue((self.repo / "omoikane/wiki/concepts/template-concept.md").is_file())


if __name__ == "__main__":
    unittest.main()
