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


def run(repo: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(repo / "omoikane" / "bin" / script), *args], cwd=repo,
                          capture_output=True, text=True, encoding="utf-8")


def page(kind: str, title: str, tags: str, body: str, sources: str = "[wiki/sources/session-2026-09-01-aaaaaaaa.md]",
         extra: str = "") -> str:
    return (f"---\ntitle: {title}\ntype: {kind}\nsummary: {title}\ntags: [{tags}]\ncreated: 2026-09-01\n"
            f"updated: 2026-09-01\nsources: {sources}\n{extra}---\n\n{body}\n")


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

    def test_conventions_of_another_system_come_along(self) -> None:
        # The organisation's conventions and design-system rules had to be restated in every new system (#80).
        other = Path(self.tmp.name) / "payroll"
        wiki = other / "omoikane" / "wiki"
        pages = {
            "domain/commit-messages-in-english.md": page(
                "domain", "Commit messages in English", "convention",
                "The user, turn 2: \"commits em inglês\" (source: [[session-2026-09-01-aaaaaaaa]]). "
                "See [[buttons-use-the-primary-token]] and [[why-we-squash]].", extra="code: [src/git.py]\n"),
            "domain/buttons-use-the-primary-token.md": page("domain", "Buttons use the primary token",
                                                            "design-system, ui", "Use `color.action.primary`."),
            "domain/salaries-are-integer-cents.md": page("domain", "Salaries are integer cents", "business-rule", "x"),
            # A term usually belongs to one system's domain, so it stays behind too (#90).
            "domain/holerite-is-the-monthly-payslip.md": page("domain", "Holerite is the monthly payslip", "term", "x"),
            "decisions/why-we-squash.md": page("decision", "Why we squash", "git", "x"),
            "sources/session-2026-09-01-aaaaaaaa.md": page("source", "Session", "session", "x", sources="[]",
                                                           extra="dated: 2026-09-01\n"),
        }
        for name, text in pages.items():
            (wiki / name).parent.mkdir(parents=True, exist_ok=True)
            (wiki / name).write_text(text, encoding="utf-8")
        git(other, "init", "-q", "-b", "main")
        git(other, "add", "-A")
        git(other, "commit", "-q", "-m", "payroll wiki")

        result = run(self.repo, "new-system.py", "--from", str(other))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        domain = self.repo / "omoikane" / "wiki" / "domain"
        self.assertEqual(sorted(p.name for p in domain.glob("*.md")),
                         ["buttons-use-the-primary-token.md", "commit-messages-in-english.md"])
        self.assertFalse(list((self.repo / "omoikane" / "wiki" / "decisions").glob("*.md")))
        source = self.repo / "omoikane" / "wiki" / "sources" / "inherited-from-payroll.md"
        self.assertIn("type: source", source.read_text(encoding="utf-8"))
        copied = (domain / "commit-messages-in-english.md").read_text(encoding="utf-8")
        self.assertIn("sources: [wiki/sources/inherited-from-payroll.md]", copied)
        self.assertNotIn("code:", copied)
        self.assertIn("[[buttons-use-the-primary-token]]", copied)
        self.assertNotIn("[[why-we-squash]]", copied)
        self.assertNotIn("[[session-2026-09-01-aaaaaaaa]]", copied)
        self.assertIn("\"commits em inglês\"", copied)
        self.assertIn("[[inherited-from-payroll]]", copied)
        lint = run(self.repo, "wiki-lint.py")
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        self.assertIn("[[commit-messages-in-english]]", run(self.repo, "session-context.py").stdout)

    def test_what_is_disputed_marked_or_unclear_stays_behind_or_is_cleaned(self) -> None:
        # #85 review: a disputed page crossed without its review entry, a pruned page lost its mark, an alias and a
        # capitalised or unbracketed tag were mishandled, and a folder name with accents broke the source page.
        other = Path(self.tmp.name) / "Folha São Paulo"
        domain = other / "omoikane" / "wiki" / "domain"
        domain.mkdir(parents=True)
        for name, text in {
            "disputed.md": page("domain", "Disputed", "convention", "x").replace("summary: Disputed", "summary: Disputed: a or b"),
            "pruned.md": page("domain", "Pruned", "convention", "x", extra="prune: stale\n"),
            "capital-tag.md": page("domain", "Capital tag", "Convention", "See [[gone|the old rule]]."),
            "bare-tag.md": page("domain", "Bare tag", "x", "y").replace("tags: [x]", "tags: design-system")
                           .replace("summary: Bare tag", "summary: Bare tag  # with a hash"),
        }.items():
            (domain / name).write_text(text, encoding="utf-8")
        result = run(self.repo, "new-system.py", "--from", str(other))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        wiki = self.repo / "omoikane" / "wiki"
        self.assertEqual(sorted(p.name for p in (wiki / "domain").glob("*.md")), ["bare-tag.md", "capital-tag.md"])
        self.assertIn("See the old rule.", (wiki / "domain" / "capital-tag.md").read_text(encoding="utf-8"))
        self.assertIn("summary: Bare tag  # with a hash", (wiki / "domain" / "bare-tag.md").read_text(encoding="utf-8"))
        self.assertIn("title: Inherited from folha-sao-paulo",
                      (wiki / "sources" / "inherited-from-folha-sao-paulo.md").read_text(encoding="utf-8"))
        self.assertIn("2 other domain pages", result.stdout)
        lint = run(self.repo, "wiki-lint.py")
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)

    def test_from_a_path_it_cannot_use_changes_nothing(self) -> None:
        # #85 review: the pages were read after the wiki was deleted, so an unreadable page left a half-reset clone.
        unreadable = Path(self.tmp.name) / "unreadable"
        (unreadable / "omoikane" / "wiki" / "domain").mkdir(parents=True)
        (unreadable / "omoikane" / "wiki" / "domain" / "a.md").write_bytes(b"---\ntitle: caf\xe9\n---\n")
        for origin in (Path(self.tmp.name) / "missing", unreadable, self.repo):
            with self.subTest(origin=origin.name):
                result = run(self.repo, "new-system.py", "--from", str(origin))
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("nothing was changed", result.stdout)
                self.assertNotIn("Traceback", result.stderr)
                self.assertTrue((self.repo / "omoikane/wiki/concepts/template-concept.md").is_file())

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
