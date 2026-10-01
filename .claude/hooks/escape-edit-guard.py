"""PreToolUse hook for the Bash tool: block shell edits that rewrite the escapes in their text.

Three times an agent here edited a file through the shell and `\\n` in the text became a real line break: twice
through a Python heredoc script, once through a `sed` replacement; one corrupted docstring reached main (#47).
The Edit tool writes the text as given. Exit 2 blocks the call and shows stderr to the agent.
Usage (from .claude/settings.json): python .claude/hooks/escape-edit-guard.py < hook-payload.json
"""
from __future__ import annotations

import json
import re
import sys

SED_IN_PLACE = re.compile(r"(?<![\w-])sed\s+(?:[^|;&\n]*\s)?(?:-[a-zA-Z]*i|--in-place)")
PYTHON_HEREDOC = re.compile(r"(?<![\w-])python3?(?:\.exe)?\s+(?:-\s*)?<<")
ESCAPE = re.compile(r"\\[nt\\]")


def reason(command: str) -> str:
    """Why `command` is blocked, or "" when it may run.

    Example: reason("sed -i 's/a/b/' x.py") returns "sed -i rewrites escapes in its replacement".
    """
    if SED_IN_PLACE.search(command):
        return "sed -i rewrites escapes in its replacement"
    if PYTHON_HEREDOC.search(command) and ESCAPE.search(command):
        return r"a Python heredoc with \n, \t or \\ in its text rewrites them on the way to the file"
    return ""


def main() -> int:
    payload = json.load(sys.stdin)
    why = reason(str(payload.get("tool_input", {}).get("command", ""))) if payload.get("tool_name") == "Bash" else ""
    if not why:
        return 0
    print(f"Blocked: {why}. Use the Edit tool (or Write for a new file).", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
