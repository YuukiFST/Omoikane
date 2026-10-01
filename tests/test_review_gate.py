"""Headless tests for omoikane/bin/review-gate.py against a real local git origin. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "omoikane" / "bin"))

gate = importlib.import_module("review-gate")

FAKE_GH = """import json, os, sys
state = os.environ["FAKE_GH_STATE"]
with open(os.environ["FAKE_GH_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
if sys.argv[1:3] == ["pr", "list"]:
    print(json.dumps([{"number": 7, "url": "https://example.invalid/pull/7"}] if os.path.exists(state) else []))
elif sys.argv[1:3] == ["pr", "create"]:
    open(state, "w").close()
    print("https://example.invalid/pull/7")
"""


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, encoding="utf-8",
                          check=True).stdout


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


class Gate(unittest.TestCase):
    """The scheduled run's commits go to wiki/auto in a worktree of their own, never onto the human's checkout (#45)."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.origin, self.repo, self.work = root / "origin.git", root / "repo", root / "repo-wiki-auto"
        git(root, "init", "-q", "--bare", "-b", "main", str(self.origin))
        git(root, "clone", "-q", str(self.origin), str(self.repo))
        git(self.repo, "config", "user.name", "t")
        git(self.repo, "config", "user.email", "t@example.invalid")
        write(self.repo / ".gitattributes", (REPO / ".gitattributes").read_text(encoding="utf-8"))
        for path, text in (("AGENTS.md", "# Manual\n"), ("omoikane/log.md", "# Log\n"),
                           ("omoikane/_review.md", "# Review queue\n"), ("omoikane/index.md", "# Index\n"),
                           ("omoikane/raw/inbox/sessions/.gitkeep", ""), ("omoikane/raw/sources/sessions/.gitkeep", "")):
            write(self.repo / path, text)
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "init")
        git(self.repo, "push", "-q", "-u", "origin", "main")
        self.gh_log, self.gh_state = root / "gh.log", root / "gh.state"
        fake = root / "gh.py"
        fake.write_text(FAKE_GH, encoding="utf-8")
        self.gh = (sys.executable, str(fake))
        os.environ.update(FAKE_GH_LOG=str(self.gh_log), FAKE_GH_STATE=str(self.gh_state))

    def tearDown(self) -> None:
        subprocess.run(["git", "-C", str(self.repo), "worktree", "remove", "--force", str(self.work)], capture_output=True)
        self.tmp.cleanup()

    def prepare(self) -> list[str]:
        return gate.prepare(self.repo, self.work, quiet_minutes=30)

    def commit_in_worktree(self, path: str, text: str, message: str) -> None:
        write(self.work / path, text)
        git(self.work, "add", "-A")
        git(self.work, "commit", "-q", "-m", message)

    def human_pushes_to_main(self, path: str, text: str) -> None:
        git(self.repo, "pull", "-q", "--ff-only")
        write(self.repo / path, text)
        git(self.repo, "commit", "-q", "-am", f"human edits {path}")
        git(self.repo, "push", "-q", "origin", "main")

    def gh_calls(self) -> list[list[str]]:
        return [json.loads(line) for line in self.gh_log.read_text(encoding="utf-8").splitlines()] if self.gh_log.exists() else []

    def test_the_worktree_starts_on_wiki_auto_and_the_checkout_is_untouched(self) -> None:
        write(self.repo / "notes.txt", "the human's uncommitted work\n")
        self.prepare()
        self.assertEqual(git(self.work, "branch", "--show-current").strip(), "wiki/auto")
        self.assertEqual(git(self.work, "rev-parse", "HEAD"), git(self.repo, "rev-parse", "origin/main"))
        self.assertEqual(git(self.repo, "branch", "--show-current").strip(), "main")
        self.assertEqual(git(self.repo, "status", "--short"), "?? notes.txt\n")

    def test_only_quiet_captures_move_into_the_worktree(self) -> None:
        inbox = self.repo / "omoikane/raw/inbox"
        write(inbox / "sessions/2026-09-30-aaaaaaaa.md", "old")
        write(inbox / "sessions/2026-09-30-bbbbbbbb.md", "still growing")
        write(inbox / "article.md", "a source")
        hour_ago = time.time() - 3600
        os.utime(inbox / "sessions/2026-09-30-aaaaaaaa.md", (hour_ago, hour_ago))
        moved = self.prepare()
        self.assertEqual(sorted(moved), ["omoikane/raw/inbox/article.md",
                                         "omoikane/raw/inbox/sessions/2026-09-30-aaaaaaaa.md"])
        self.assertTrue((self.work / "omoikane/raw/inbox/sessions/2026-09-30-aaaaaaaa.md").is_file())
        self.assertTrue((inbox / "sessions/2026-09-30-bbbbbbbb.md").is_file())
        self.assertFalse((inbox / "article.md").exists())

    def test_publish_pushes_and_opens_one_pr(self) -> None:
        self.prepare()
        self.assertEqual(gate.publish(self.work, self.gh), "nothing to publish")
        self.assertEqual(self.gh_calls(), [])
        self.commit_in_worktree("omoikane/log.md", "# Log\n\n## distill | a\n", "feat(wiki): distill a")
        self.assertIn("opened https://example.invalid/pull/7", gate.publish(self.work, self.gh))
        self.assertEqual(git(self.repo, "ls-remote", "--heads", "origin", "wiki/auto").split()[0],
                         git(self.work, "rev-parse", "HEAD").strip())
        self.prepare()
        self.commit_in_worktree("omoikane/log.md", "# Log\n\n## distill | a\n\n## distill | b\n", "feat(wiki): distill b")
        self.assertIn("PR #7 updated", gate.publish(self.work, self.gh))
        creates = [c for c in self.gh_calls() if c[:2] == ["pr", "create"]]
        self.assertEqual(len(creates), 1)
        self.assertIn("feat(wiki): distill a", creates[0][creates[0].index("--body") + 1])

    def test_main_comes_in_by_merge_and_the_log_by_union(self) -> None:
        self.prepare()
        self.commit_in_worktree("omoikane/log.md", "# Log\n\n## distill | a\n", "feat(wiki): distill a")
        gate.publish(self.work, self.gh)
        self.human_pushes_to_main("omoikane/log.md", "# Log\n\n## review | removed\n")
        self.prepare()
        log = (self.work / "omoikane/log.md").read_text(encoding="utf-8")
        self.assertIn("## distill | a", log)
        self.assertIn("## review | removed", log)
        self.assertEqual(git(self.work, "rev-list", "--count", "HEAD..origin/main").strip(), "0")

    def test_an_index_conflict_is_regenerated(self) -> None:
        self.prepare()
        self.commit_in_worktree("omoikane/index.md", "# Index\n\nfrom the run\n", "feat(wiki): distill a")
        self.human_pushes_to_main("omoikane/index.md", "# Index\n\nfrom main\n")
        regenerated: list[Path] = []
        gate.prepare(self.repo, self.work, 30, regenerate=lambda w: (regenerated.append(w),
                                                                     write(w / "omoikane/index.md", "# Index\n\nfresh\n")))
        self.assertEqual(regenerated, [self.work])
        self.assertEqual((self.work / "omoikane/index.md").read_text(encoding="utf-8"), "# Index\n\nfresh\n")
        self.assertEqual(git(self.work, "status", "--short"), "")

    def test_any_other_conflict_stops_and_leaves_the_branch_as_it_was(self) -> None:
        self.prepare()
        self.commit_in_worktree("AGENTS.md", "# Manual by the run\n", "feat(wiki): distill a")
        head = git(self.work, "rev-parse", "HEAD")
        self.human_pushes_to_main("AGENTS.md", "# Manual by the human\n")
        with self.assertRaisesRegex(gate.GateError, "AGENTS.md"):
            self.prepare()
        self.assertEqual(git(self.work, "rev-parse", "HEAD"), head)
        self.assertEqual(git(self.work, "status", "--short"), "")

    def test_after_the_pr_is_merged_the_branch_restarts_from_main(self) -> None:
        self.prepare()
        self.commit_in_worktree("omoikane/log.md", "# Log\n\n## distill | a\n", "feat(wiki): distill a")
        gate.publish(self.work, self.gh)
        git(self.repo, "pull", "-q", "--ff-only")
        git(self.repo, "merge", "-q", "--no-ff", "--no-edit", "origin/wiki/auto")
        git(self.repo, "push", "-q", "origin", "main")
        self.prepare()
        self.assertEqual(git(self.work, "rev-parse", "HEAD"), git(self.repo, "rev-parse", "origin/main"))
        self.assertEqual(gate.publish(self.work, self.gh), "nothing to publish")

    def test_a_dirty_worktree_stops_prepare(self) -> None:
        self.prepare()
        write(self.work / "omoikane/wiki/leftover.md", "a run that crashed")
        with self.assertRaisesRegex(gate.GateError, "leftover.md"):
            self.prepare()


if __name__ == "__main__":
    unittest.main()
