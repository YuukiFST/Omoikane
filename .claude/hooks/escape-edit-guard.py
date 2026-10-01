"""PreToolUse hook for the Bash tool: block shell edits that rewrite the escapes in their text.

Three times an agent here edited a file through the shell and `\\n` in the text became a real line break: twice
through a Python heredoc script, once through a `sed` replacement; one corrupted docstring reached main (#47).
The Edit tool writes the text as given. Exit 2 blocks the call and shows stderr to the agent.

Blocked: `sed -i` (or `gsed`, `--in-place`) where a command starts, and a heredoc fed to Python whose body holds
`\\n`, `\\t` or `\\\\`. Quoted text and heredoc bodies are data, not commands: a commit message or a `grep` about
`sed -i` passes.
Usage (from .claude/settings.json): python .claude/hooks/escape-edit-guard.py < hook-payload.json
"""
from __future__ import annotations

import json
import re
import shlex
import sys

# `<<`, `<<-`, quoted or bare delimiter; not the `<<<` here-string.
HEREDOC = re.compile(r"(?<!<)<<(?!<)-?[ \t]*(['\"]?)([A-Za-z_][\w-]*)\1")
PYTHON = re.compile(r"(?<![\w.-])(?:\S*[/\\])?(?:python(?:3(?:\.\d+)?)?|py)(?:\.exe)?(?![\w.-])")
# A script argument: the heredoc is that script's input, not Python source.
SCRIPT_ARG = re.compile(r"\S\.py\b")
ESCAPE = re.compile(r"\\[nt\\]")
SEPARATORS = {";", ";;", "&", "&&", "|", "||", "|&", "(", ")"}
PREFIXES = {"sudo", "xargs", "env", "command", "nohup", "time", "exec"}
SED = {"sed", "gsed", "sed.exe"}
IN_PLACE = re.compile(r"-[a-zA-Z]*i|--in-place")


def split_heredocs(command: str) -> tuple[str, list[tuple[str, str]]]:
    """The command with heredoc bodies taken out, and (line that opens it, body) for each heredoc.

    Example: split_heredocs("cat <<EOF\\nx\\nEOF\\nls") returns ("cat <<EOF\\nls", [("cat <<EOF", "x")]).
    """
    lines = command.split("\n")
    shell: list[str] = []
    docs: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        shell.append(line)
        i += 1
        for m in HEREDOC.finditer(line):
            body: list[str] = []
            while i < len(lines) and lines[i].strip() != m.group(2):
                body.append(lines[i])
                i += 1
            i += 1  # the delimiter line
            docs.append((line, "\n".join(body)))
    return "\n".join(shell), docs


def runs_sed_in_place(shell: str) -> bool:
    """Whether a command of `shell` (heredoc bodies already out) is sed with an in-place option.

    Example: runs_sed_in_place("cd x && sed -i 's/a/b/' f") returns True; runs_sed_in_place("grep 'sed -i' f")
    returns False.
    """
    for line in shell.replace("\\\n", " ").split("\n"):
        lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        try:
            tokens = list(lexer)
        except ValueError:  # unbalanced quotes: bash refuses the line too
            continue
        at_start, in_sed = True, False
        for token in tokens:
            if token in SEPARATORS:
                at_start, in_sed = True, False
            elif at_start:
                if token in PREFIXES or token.startswith("-") or re.match(r"[A-Za-z_]\w*=", token):
                    continue
                in_sed, at_start = token.replace("\\", "/").rsplit("/", 1)[-1] in SED, False
            elif in_sed and IN_PLACE.match(token):
                return True
    return False


def reason(command: str) -> str:
    """Why `command` is blocked, or "" when it may run.

    Example: reason("sed -i 's/a/b/' x.py") returns "sed -i rewrites escapes in its replacement".
    """
    shell, docs = split_heredocs(command)
    if runs_sed_in_place(shell):
        return "sed -i rewrites escapes in its replacement"
    for line, body in docs:
        if PYTHON.search(line) and not SCRIPT_ARG.search(line) and ESCAPE.search(body):
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
