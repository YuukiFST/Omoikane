"""Headless tests for omoikane/bin/headless-scope.py. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "omoikane" / "bin"
sys.path.insert(0, str(BIN))

scope = importlib.import_module("headless-scope")

EDITABLE = ("omoikane/wiki/sources/session-x.md", "omoikane/wiki/gotchas/a.md", "omoikane/log.md", "omoikane/_review.md")
NOT_EDITABLE = ("AGENTS.md", "CLAUDE.md", "omoikane/prompts/distill.md", "omoikane/bin/wiki-lint.py",
                "omoikane/index.md", "omoikane/raw/sources/x.md", ".opencode/plugins/omoikane.ts", "tests/test_x.py")
RUNNABLE = ("python omoikane/bin/wiki-index.py", "python omoikane/bin/wiki-lint.py")
NOT_RUNNABLE = ("git status", "git mv a b", "git commit -m x", "python omoikane/bin/wiki-rules.py",
                "python omoikane/bin/x.py", "rm -rf omoikane/wiki", "mv a b", "python -c 'print(1)'", "curl x")


def flatten(permission: dict[str, object]) -> list[tuple[str, str, str]]:
    """(permission, pattern, action) rules in config order, as `opencode debug agent` lists them."""
    return [(key, pattern, action) for key, rules in permission.items()
            for pattern, action in (rules.items() if isinstance(rules, dict) else [("*", rules)])]


def opencode_decides(rules: list[tuple[str, str, str]], key: str, subject: str) -> str:
    """OpenCode's documented matching (opencode.ai/docs/permissions): `*` any run of characters, `?` one, and the
    last matching rule wins; a rule for permission `*` applies to every permission."""
    verdict = ""
    for permission, pattern, action in rules:
        regex = "".join(".*" if c == "*" else "." if c == "?" else re.escape(c) for c in pattern)
        if permission in ("*", key) and re.fullmatch(regex, subject, re.DOTALL):
            verdict = action
    return verdict


# A user config that allows everything, including through a `*` key our scope also uses: map keys merge in place,
# so the user's `git *` would sit after our `"*": "deny"` in a merged top-level `permission`.
HOSTILE_USER = {"*": "allow", "bash": {"*": "allow", "git *": "allow"}, "edit": {"*": "allow", "AGENTS.md": "allow"}}


class OpenCodeScope(unittest.TestCase):
    # The OpenCode run had no scope at all (#39): its defaults allow edits and bash anywhere. Agent rules come
    # after every config rule, so the user's rules are evaluated first and ours win.
    AGENT = scope.opencode_config()["agent"][scope.OPENCODE_AGENT]
    RULES = flatten(HOSTILE_USER) + flatten(AGENT["permission"])

    def test_edits_only_the_wiki_the_log_and_the_review_queue(self) -> None:
        for path, verdict in [(p, "allow") for p in EDITABLE] + [(p, "deny") for p in NOT_EDITABLE]:
            with self.subTest(path=path):
                self.assertEqual(opencode_decides(self.RULES, "edit", path), verdict)

    def test_runs_only_the_index_and_lint_scripts(self) -> None:
        for command, verdict in [(c, "allow") for c in RUNNABLE] + [(c, "deny") for c in NOT_RUNNABLE]:
            with self.subTest(command=command):
                self.assertEqual(opencode_decides(self.RULES, "bash", command), verdict)

    def test_reads_and_denies_everything_else(self) -> None:
        for key in ("read", "glob", "grep", "list"):
            self.assertEqual(opencode_decides(self.RULES, key, "omoikane/wiki/x.md"), "allow", key)
        for key in ("webfetch", "websearch", "task", "skill", "external_directory", "question", "doom_loop", "lsp"):
            self.assertEqual(opencode_decides(self.RULES, key, "x"), "deny", key)

    def test_wiki_ingest_runs_opencode_with_the_scoped_agent(self) -> None:
        script = (BIN / "wiki-ingest.ps1").read_text(encoding="utf-8")
        self.assertIn(f"opencode run --agent {scope.OPENCODE_AGENT} ", script)


class ClaudeScope(unittest.TestCase):
    ARGS = scope.claude_args()

    def value(self, flag: str) -> str:
        return self.ARGS[self.ARGS.index(flag) + 1]

    def test_the_allow_list_is_the_same_scope(self) -> None:
        allowed = self.value("--allowedTools").split(",")
        expected = {"Read", "Glob", "Grep", "Edit(/omoikane/wiki/**)", "Edit(/omoikane/log.md)",
                    "Edit(/omoikane/_review.md)"} | {f"{tool}({c})" for c in RUNNABLE for tool in ("Bash", "PowerShell")}
        self.assertEqual(set(allowed), expected)

    def test_user_settings_are_ignored_and_git_is_denied(self) -> None:
        # User-level allow rules and hooks let git through in the headless run (#25).
        self.assertEqual(self.value("--setting-sources"), "project")
        self.assertEqual(self.value("--permission-mode"), "dontAsk")
        self.assertIn("--strict-mcp-config", self.ARGS)
        self.assertEqual(self.value("--disallowedTools"), "Bash(git *),PowerShell(git *)")


class Cli(unittest.TestCase):
    def test_prints_what_wiki_ingest_consumes(self) -> None:
        for harness, expected in (("claude", scope.claude_args()), ("opencode", scope.opencode_config())):
            with self.subTest(harness=harness):
                out = subprocess.run([sys.executable, str(BIN / "headless-scope.py"), harness], capture_output=True,
                                     text=True, encoding="utf-8", check=True).stdout
                self.assertEqual(json.loads(out), expected)


if __name__ == "__main__":
    unittest.main()
