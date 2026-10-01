"""End-to-end tests of omoikane/bin/wiki-ingest.ps1 with a fake `claude` on PATH. Run: python -m unittest discover -s tests

The fake stands for the headless agent: it records the flags it was given and edits the throwaway repository the
way a run that goes well, or one that leaves its scope, would.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PWSH = shutil.which("pwsh")

FAKE_CLAUDE = textwrap.dedent('''
    import json, os, sys
    from pathlib import Path
    prompt = sys.argv[sys.argv.index("-p") + 1]
    with open(os.environ["FAKE_LOG"], "a", encoding="utf-8") as log:
        log.write(json.dumps(sys.argv[1:]) + "\\n")
    page = "---\\ntitle: {0}\\ntype: concept\\nsummary: s\\ntags: []\\ncreated: 2026-10-01\\nupdated: 2026-10-01\\nsources: []\\n---\\n{1}\\n"
    mode = os.environ["FAKE_MODE"]
    if mode == "escape":
        Path("AGENTS.md").write_text("# Manual, rewritten by the agent\\n", encoding="utf-8")
    elif mode == "orphan" and prompt.startswith("/ingest"):
        Path("omoikane/wiki/concepts/lonely.md").write_text(page.format("lonely", "Alone."), encoding="utf-8")
    elif mode == "orphan-then-fail" and prompt.startswith("/ingest"):
        Path("omoikane/wiki/concepts/lonely.md").write_text(page.format("lonely", "Alone."), encoding="utf-8")
    elif mode == "orphan-then-fail":
        sys.exit(1)
    elif mode == "orphan" and "orphan page" in prompt:
        Path("omoikane/wiki/concepts/lonely.md").write_text(page.format("lonely", "See [[hub]]."), encoding="utf-8")
        Path("omoikane/wiki/concepts/hub.md").write_text(page.format("hub", "See [[lonely]]."), encoding="utf-8")
''')


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8",
                          check=True).stdout


@unittest.skipUnless(PWSH or os.environ.get("CI"), "pwsh not on PATH")
class WikiIngest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.repo, shims, self.calls = root / "repo", root / "bin", root / "calls.jsonl"
        for part in ("omoikane/bin", "omoikane/prompts"):
            shutil.copytree(REPO / part, self.repo / part, ignore=shutil.ignore_patterns("__pycache__"))
        for part in ("AGENTS.md", ".gitignore", ".gitattributes"):
            shutil.copy(REPO / part, self.repo / part)
        for folder in ("concepts", "sources"):
            (self.repo / "omoikane/wiki" / folder).mkdir(parents=True)
            (self.repo / "omoikane/wiki" / folder / ".gitkeep").write_text("", encoding="utf-8")
        (self.repo / "omoikane/log.md").write_text("# Log\n", encoding="utf-8")
        (self.repo / "omoikane/_review.md").write_text("# Review queue\n", encoding="utf-8")
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "t")
        git(self.repo, "config", "user.email", "t@example.invalid")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "init")
        (self.repo / "omoikane/raw/inbox").mkdir(parents=True)
        (self.repo / "omoikane/raw/inbox/article.md").write_text("a source\n", encoding="utf-8")
        shims.mkdir()
        (shims / "fake_claude.py").write_text(FAKE_CLAUDE, encoding="utf-8")
        # pwsh finds `claude.ps1` by its base name on Windows, the extensionless script on Linux.
        (shims / "claude.ps1").write_text(f'& "{sys.executable}" "{shims / "fake_claude.py"}" @args\nexit $LASTEXITCODE\n',
                                          encoding="utf-8")
        (shims / "claude").write_text(f'#!/bin/sh\nexec "{sys.executable}" "{shims / "fake_claude.py"}" "$@"\n',
                                      encoding="utf-8")
        (shims / "claude").chmod(0o755)
        self.env = {**os.environ, "PATH": f"{shims}{os.pathsep}{os.environ['PATH']}", "FAKE_LOG": str(self.calls)}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def ingest(self, mode: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([str(PWSH), "-NoProfile", "-File", str(self.repo / "omoikane/bin/wiki-ingest.ps1"),
                               "-SynthesizeEvery", "0", "-Commit"], env={**self.env, "FAKE_MODE": mode},
                              stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", timeout=300)

    def calls_made(self) -> list[list[str]]:
        return [json.loads(line) for line in self.calls.read_text(encoding="utf-8").splitlines()] if self.calls.exists() else []

    def test_a_run_that_leaves_its_scope_blocks_every_later_run(self) -> None:
        run = self.ingest("escape")
        self.assertNotEqual(run.returncode, 0, run.stdout)
        self.assertTrue((self.repo / "omoikane/.wiki-ingest.blocked").is_file())
        self.assertIn("AGENTS.md", (self.repo / "omoikane/.wiki-ingest.log").read_text(encoding="utf-8"))
        self.assertEqual(git(self.repo, "rev-list", "--count", "HEAD").strip(), "1")  # nothing committed
        self.assertTrue((self.repo / "omoikane/raw/inbox/article.md").is_file())  # not marked as processed
        self.assertEqual(self.ingest("escape").returncode, 1)
        self.assertEqual(len(self.calls_made()), 1)  # the blocked run never called the agent

    def test_lint_findings_go_back_to_the_agent_and_the_operation_is_committed(self) -> None:
        run = self.ingest("orphan")
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        first, fix = self.calls_made()
        self.assertEqual(first[first.index("--tools") + 1], "Read,Glob,Grep,Edit,Write")
        self.assertEqual(first[first.index("--setting-sources") + 1], "project")
        self.assertIn("orphan page, no inbound wikilink", fix[fix.index("-p") + 1])
        self.assertEqual(git(self.repo, "log", "-1", "--format=%s").strip(), "feat(wiki): ingest article")
        committed = git(self.repo, "show", "--name-only", "--format=", "HEAD").split()
        for path in ("omoikane/wiki/concepts/hub.md", "omoikane/wiki/concepts/lonely.md",
                     "omoikane/raw/sources/article.md", "omoikane/index.md"):
            self.assertIn(path, committed)

    def test_only_findings_go_back_not_warnings(self) -> None:
        # Warnings need /lint's judgement; 25 of them once buried the one finding the agent had to fix.
        (self.repo / "omoikane/wiki/gotchas").mkdir()
        (self.repo / "omoikane/wiki/gotchas/old.md").write_text(
            "---\ntitle: old\ntype: gotcha\nsummary: s\ntags: []\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            "sources: []\nguard: none\n---\nSee [[old]].\n", encoding="utf-8")
        self.ingest("orphan")
        fix = self.calls_made()[1]
        self.assertNotIn("warning:", fix[fix.index("-p") + 1])

    def test_an_agent_that_fails_after_a_lint_round_fails_the_operation(self) -> None:
        run = self.ingest("orphan-then-fail")
        self.assertIn("ingest FAILED omoikane/raw/inbox/article.md", run.stdout)
        self.assertEqual(git(self.repo, "rev-list", "--count", "HEAD").strip(), "1")
        self.assertTrue((self.repo / "omoikane/raw/inbox/article.md").is_file())


if __name__ == "__main__":
    unittest.main()
