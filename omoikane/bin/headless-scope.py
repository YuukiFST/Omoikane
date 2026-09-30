"""What a scheduled headless run may do, rendered for each harness wiki-ingest.ps1 drives.

One scope, two renderings: the Claude Code flags and the OpenCode permission config were once written apart, and
the OpenCode run had none at all (#39). The scope: read anything in the repository, edit only the wiki, the log and
the review queue, run only the index and lint scripts, no git, nothing else.

Usage: python omoikane/bin/headless-scope.py claude|opencode
Prints JSON: the claude argument list, or the OpenCode config that wiki-ingest.ps1 passes in OPENCODE_CONFIG_CONTENT.
"""
from __future__ import annotations

import json
import sys

# Repository-relative. `**` is any depth below the directory.
EDITABLE = ("omoikane/wiki/**", "omoikane/log.md", "omoikane/_review.md")
# Named exactly: a wildcard would run a script the agent wrote into omoikane/bin/, or one reached through `..`.
SCRIPTS = ("python omoikane/bin/wiki-index.py", "python omoikane/bin/wiki-lint.py")


def claude_args() -> list[str]:
    """Flags for `claude -p`, after the prompt.

    --setting-sources project: allow rules and PreToolUse hooks in the user's own settings would otherwise apply
    too (a user-level `Bash(git checkout:*)` or a hook answering "allow" reopens AGENTS.md and omoikane/bin/).
    --tools and --strict-mcp-config keep plugins and MCP servers out. dontAsk denies whatever the list does not
    allow; acceptEdits would also auto-approve rm, mv, cp and sed anywhere in the repository (#25). Edit(...) rules
    cover the Write tool; a leading / anchors at the repository root. On Windows Claude Code runs shell commands
    through its PowerShell tool, which Bash(...) rules do not cover (#17). Git is denied outright.
    Example: claude_args()[:2] returns ["--setting-sources", "project"].
    """
    allowed = ["Read", "Glob", "Grep", *(f"Edit(/{path})" for path in EDITABLE)]
    allowed += [f"{tool}({script})" for script in SCRIPTS for tool in ("Bash", "PowerShell")]
    return ["--setting-sources", "project", "--strict-mcp-config", "--tools", "Read,Glob,Grep,Edit,Write,Bash,PowerShell",
            "--permission-mode", "dontAsk", "--allowedTools", ",".join(allowed),
            "--disallowedTools", "Bash(git *),PowerShell(git *)"]


OPENCODE_AGENT = "omoikane-headless"


def opencode_config() -> dict[str, object]:
    """OpenCode config (schema https://opencode.ai/config.json, rules https://opencode.ai/docs/permissions/),
    defining the agent wiki-ingest.ps1 runs with `--agent omoikane-headless`.

    `*` matches any run of characters, `/` included, and the last matching rule wins, so every map opens with
    `"*": "deny"`. `edit` covers the edit, write and patch tools. The `"*"` permission denies every one not named,
    among them webfetch, task (subagents) and external_directory (paths outside the repository).
    The scope is an agent's, not the top-level `permission`: OpenCode merges config maps key by key, so a user's
    `"bash": {"*": "allow", "git *": "allow"}` kept `git *` after our `"*": "deny"` and git ran again (#39);
    agent rules are evaluated after every config rule (`opencode debug agent` lists them in that order).
    Example: opencode_config()["agent"]["omoikane-headless"]["permission"]["bash"]["*"] returns "deny".
    """
    return {"agent": {OPENCODE_AGENT: {
        "mode": "primary",
        "description": "Scheduled Omoikane run: edits the wiki, runs index and lint, nothing else.",
        "permission": {
            "*": "deny",
            "read": "allow", "glob": "allow", "grep": "allow", "list": "allow", "todowrite": "allow",
            "edit": {"*": "deny", **{path.replace("**", "*"): "allow" for path in EDITABLE}},
            "bash": {"*": "deny", **{script: "allow" for script in SCRIPTS}},
        },
    }}}


def main(argv: list[str]) -> int:
    renderings = {"claude": claude_args, "opencode": opencode_config}
    if len(argv) != 1 or argv[0] not in renderings:
        print(__doc__.splitlines()[-2], file=sys.stderr)
        return 2
    print(json.dumps(renderings[argv[0]]()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
