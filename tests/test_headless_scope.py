"""Headless tests for omoikane/bin/headless-scope.py. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BIN = REPO / "omoikane" / "bin"
sys.path.insert(0, str(BIN))

scope = importlib.import_module("headless-scope")

AGENT = "omoikane-headless-test0001"
EDITABLE = ("omoikane/wiki/sources/session-x.md", "omoikane/wiki/gotchas/a.md", "omoikane/log.md", "omoikane/_review.md")
NOT_EDITABLE = ("AGENTS.md", "CLAUDE.md", "omoikane/prompts/distill.md", "omoikane/bin/wiki-lint.py",
                "omoikane/index.md", "omoikane/raw/sources/x.md", ".opencode/plugins/omoikane.ts", "tests/test_x.py",
                # run as `python omoikane/bin/wiki-index.py` from inside omoikane/wiki/ (#39)
                "omoikane/wiki/omoikane/bin/wiki-index.py", "omoikane/wiki/x.py")
RUNNABLE = ("python omoikane/bin/wiki-index.py", "python omoikane/bin/wiki-lint.py")
NOT_RUNNABLE = ("git status", "git mv a b", "git commit -m x", "python omoikane/bin/wiki-rules.py",
                "python omoikane/bin/x.py", "rm -rf omoikane/wiki", "mv a b", "python -c 'print(1)'", "curl x")
# A user config that allows everything, through the keys the scope also uses. Config maps merge key by key.
HOSTILE_USER = {
    "permission": {"*": "allow", "bash": {"*": "allow", "git *": "allow"}, "edit": {"*": "allow", "AGENTS.md": "allow"}},
    "agent": {"omoikane-headless": {"permission": {"bash": {"*": "allow", "git *": "allow"}, "edit": "allow"}}},
    "command": {"distill": {"agent": "build", "template": "x"}},
}


def opencode_decides(rules: list[tuple[str, str, str]], key: str, subject: str) -> str:
    """OpenCode's documented matching (opencode.ai/docs/permissions): `*` any run of characters, `?` one, and the
    last matching rule wins; a rule for permission `*` applies to every permission."""
    verdict = ""
    for permission, pattern, action in rules:
        regex = "".join(".*" if c == "*" else "." if c == "?" else re.escape(c) for c in pattern)
        if permission in ("*", key) and re.fullmatch(regex, subject, re.DOTALL):
            verdict = action
    return verdict


def flatten(permission: dict[str, object]) -> list[tuple[str, str, str]]:
    """(permission, pattern, action) in config order, as `opencode debug agent` lists them."""
    return [(key, pattern, action) for key, rules in permission.items()
            for pattern, action in (rules.items() if isinstance(rules, dict) else [("*", rules)])]


class ScopeTable:
    """The allow/deny table every rendering of the scope must satisfy; `decide(key, subject)` is the harness's."""

    def decide(self, key: str, subject: str) -> str:
        raise NotImplementedError

    def test_edits_only_wiki_pages_the_log_and_the_review_queue(self) -> None:
        for path, verdict in [(p, "allow") for p in EDITABLE] + [(p, "deny") for p in NOT_EDITABLE]:
            with self.subTest(path=path):  # type: ignore[attr-defined]
                self.assertEqual(self.decide("edit", path), verdict)  # type: ignore[attr-defined]

    def test_runs_only_the_index_and_lint_scripts(self) -> None:
        for command, verdict in [(c, "allow") for c in RUNNABLE] + [(c, "deny") for c in NOT_RUNNABLE]:
            with self.subTest(command=command):  # type: ignore[attr-defined]
                self.assertEqual(self.decide("bash", command), verdict)  # type: ignore[attr-defined]

    def test_reads_the_repository_and_denies_everything_else(self) -> None:
        for key, subject, verdict in (("read", "omoikane/wiki/x.md", "allow"), ("glob", "*", "allow"),
                                      ("read", ".env", "deny"), ("read", "mcp:github:repo://x", "deny"),
                                      ("webfetch", "x", "deny"), ("websearch", "x", "deny"), ("task", "x", "deny"),
                                      ("skill", "x", "deny"), ("external_directory", "x", "deny"),
                                      ("question", "x", "deny"), ("doom_loop", "x", "deny"), ("lsp", "x", "deny")):
            with self.subTest(key=key, subject=subject):  # type: ignore[attr-defined]
                self.assertEqual(self.decide(key, subject), verdict)  # type: ignore[attr-defined]


class OpenCodeRendering(ScopeTable, unittest.TestCase):
    # The OpenCode run had no scope at all (#39). The user's rules come first, the agent's last.
    RULES = flatten(HOSTILE_USER["permission"]) + flatten(scope.opencode_config(AGENT)["agent"][AGENT]["permission"])

    def decide(self, key: str, subject: str) -> str:
        return opencode_decides(self.RULES, key, subject)


@unittest.skipUnless(shutil.which("opencode"), "opencode not on PATH")
class OpenCodeResolved(ScopeTable, unittest.TestCase):
    """The rules OpenCode itself resolves for the agent, with a hostile user config (`opencode debug agent`)."""

    @classmethod
    def setUpClass(cls) -> None:
        with tempfile.TemporaryDirectory() as d:
            hostile = Path(d) / "user.json"
            hostile.write_text(json.dumps(HOSTILE_USER), encoding="utf-8")
            env = {**os.environ, "OPENCODE_CONFIG": str(hostile),
                   "OPENCODE_CONFIG_CONTENT": json.dumps(scope.opencode_config(AGENT))}
            out = subprocess.run([shutil.which("opencode") or "opencode", "debug", "agent", AGENT], cwd=REPO, env=env,
                                 capture_output=True, text=True, encoding="utf-8", check=True).stdout
        cls.RULES = [(r["permission"], r["pattern"], r["action"]) for r in json.loads(out)["permission"]]

    def decide(self, key: str, subject: str) -> str:
        return opencode_decides(self.RULES, key, subject)


class ClaudeRendering(unittest.TestCase):
    ARGS = scope.claude_args()

    def value(self, flag: str) -> str:
        return self.ARGS[self.ARGS.index(flag) + 1]

    def test_the_allow_list_is_the_same_scope(self) -> None:
        expected = {"Read", "Glob", "Grep", "Edit(/omoikane/wiki/**/*.md)", "Edit(/omoikane/log.md)",
                    "Edit(/omoikane/_review.md)"} | {f"{tool}({c})" for c in RUNNABLE for tool in ("Bash", "PowerShell")}
        self.assertEqual(set(self.value("--allowedTools").split(",")), expected)

    def test_user_settings_are_ignored_and_git_is_denied(self) -> None:
        # User-level allow rules and hooks let git through in the headless run (#25).
        self.assertEqual(self.value("--setting-sources"), "project")
        self.assertEqual(self.value("--permission-mode"), "dontAsk")
        self.assertIn("--strict-mcp-config", self.ARGS)
        self.assertEqual(self.value("--disallowedTools"), "Bash(git *),PowerShell(git *)")


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
                   capture_output=True, check=True)


class Verify(unittest.TestCase):
    """The tree after the run, whatever the harness allowed: any change outside the scope fails it (#39)."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q")
        for path in ("AGENTS.md", "omoikane/log.md", "omoikane/wiki/gotchas/a.md", "omoikane/bin/wiki-index.py"):
            (self.repo / path).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / path).write_text("x\n", encoding="utf-8")
        (self.repo / "omoikane/raw/inbox").mkdir(parents=True)
        (self.repo / "omoikane/raw/inbox/pending.md").write_text("dirty before the run\n", encoding="utf-8")
        git(self.repo, "add", "AGENTS.md", "omoikane/log.md", "omoikane/wiki", "omoikane/bin")
        git(self.repo, "commit", "-q", "-m", "init")
        self.before = scope.snapshot(self.repo)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def changed(self, action: object) -> list[str]:
        action()  # type: ignore[operator]
        return scope.out_of_scope(self.before, scope.snapshot(self.repo))

    def test_changes_inside_the_scope_pass(self) -> None:
        def run() -> None:
            (self.repo / "omoikane/wiki/gotchas/a.md").write_text("y\n", encoding="utf-8")
            (self.repo / "omoikane/wiki/concepts").mkdir()
            (self.repo / "omoikane/wiki/concepts/b.md").write_text("new\n", encoding="utf-8")
            (self.repo / "omoikane/log.md").write_text("x\nmore\n", encoding="utf-8")
            (self.repo / "omoikane/index.md").write_text("generated\n", encoding="utf-8")
        self.assertEqual(self.changed(run), [])

    def test_each_change_outside_the_scope_is_named(self) -> None:
        cases = {
            "AGENTS.md": lambda: (self.repo / "AGENTS.md").write_text("pwned\n", encoding="utf-8"),
            "omoikane/wiki/omoikane/bin/wiki-index.py": lambda: (
                (self.repo / "omoikane/wiki/omoikane/bin").mkdir(parents=True),
                (self.repo / "omoikane/wiki/omoikane/bin/wiki-index.py").write_text("x", encoding="utf-8")),
            "omoikane/bin/wiki-index.py": lambda: (self.repo / "omoikane/bin/wiki-index.py").unlink(),
            "omoikane/raw/inbox/pending.md": lambda: (self.repo / "omoikane/raw/inbox/pending.md").write_text(
                "edited\n", encoding="utf-8"),
            "head moved": lambda: git(self.repo, "commit", "-q", "--allow-empty", "-m", "agent"),
            "index moved": lambda: (
                (self.repo / "omoikane/log.md").write_text("staged\n", encoding="utf-8"),
                git(self.repo, "add", "omoikane/log.md")),
        }
        for expected, action in cases.items():
            with self.subTest(expected):
                self.setUp()
                self.assertIn(expected, self.changed(action))
                self.tearDown()


class WikiIngest(unittest.TestCase):
    def test_opencode_runs_the_prompt_as_a_message_on_a_fresh_agent(self) -> None:
        script = (BIN / "wiki-ingest.ps1").read_text(encoding="utf-8")
        self.assertIn("opencode run --pure --agent $agentName $message", script)
        self.assertNotRegex(script, r"opencode run[^\n]*--command")


class Cli(unittest.TestCase):
    def test_prints_what_wiki_ingest_consumes(self) -> None:
        for args, expected in ((["claude"], scope.claude_args()),
                               (["opencode", "--agent-name", AGENT], scope.opencode_config(AGENT))):
            with self.subTest(args=args):
                out = subprocess.run([sys.executable, str(BIN / "headless-scope.py"), *args], capture_output=True,
                                     text=True, encoding="utf-8", check=True).stdout
                self.assertEqual(json.loads(out), expected)


if __name__ == "__main__":
    unittest.main()
