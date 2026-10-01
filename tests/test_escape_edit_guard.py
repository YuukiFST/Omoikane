"""Headless tests for the PreToolUse hook in .claude/settings.json that blocks shell edits with escapes.
Run: python -m unittest discover -s tests

Each case runs the command registered in settings.json, as Claude Code would, with a sample hook payload (#47).
"""
from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

BLOCKED = {
    "sed -i": "sed -i 's/a/b/' omoikane/bin/wikilib.py",
    "sed -i with a backup suffix": "sed -i.bak 's/a/b/' x.py",
    "sed --in-place": "sed --in-place -e 's/a/b/' x.py",
    "sed -E -i after cd": "cd tests && sed -E -i 's/(a)/\\1\\\\n/' x.py",
    "python heredoc with \\n": "python - <<'EOF'\nfrom pathlib import Path\nPath('x').write_text('a\\nb')\nEOF",
    "python3 heredoc with \\t": "python3 - <<EOF\nprint('a\\tb')\nEOF",
    "python heredoc with \\\\": "cd x && python - << 'PY'\nprint('C:\\\\Users')\nPY",
}
ALLOWED = {
    "sed without -i": "sed -n 1,5p x.py",
    "sed to stdout": "sed 's/a/b\\n/' x.py > y.py",
    "python heredoc without escapes": "python - <<'EOF'\nprint(1)\nEOF",
    "commit message heredoc with \\n": "git commit -F - <<'EOF'\nfix: a\\nb\nEOF",
    "python -c with \\n": "python -c \"print('a\\nb')\"",
    "a word ending in sed": "echo used -i",
}


def hook_command() -> str:
    settings = json.loads((REPO / ".claude/settings.json").read_text(encoding="utf-8"))
    (entry,) = [e for e in settings["hooks"]["PreToolUse"] if e.get("matcher") == "Bash"]
    (hook,) = entry["hooks"]
    return str(hook["command"])


def run_hook(tool: str, command: str) -> subprocess.CompletedProcess[str]:
    payload = {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {"command": command}}
    # Expanded here: cmd.exe, the shell=True shell on Windows, does not expand ${VAR}.
    return subprocess.run(hook_command().replace("${CLAUDE_PROJECT_DIR}", str(REPO)), shell=True,
                          input=json.dumps(payload), capture_output=True, text=True, encoding="utf-8")


class EscapeEditGuard(unittest.TestCase):
    def test_blocks_shell_edits_that_rewrite_escapes(self) -> None:
        for name, command in BLOCKED.items():
            with self.subTest(name):
                run = run_hook("Bash", command)
                self.assertEqual(run.returncode, 2, run.stderr)
                self.assertIn("Edit tool", run.stderr)

    def test_lets_every_other_command_through(self) -> None:
        for name, command in ALLOWED.items():
            with self.subTest(name):
                run = run_hook("Bash", command)
                self.assertEqual((run.returncode, run.stderr), (0, ""))


if __name__ == "__main__":
    unittest.main()
