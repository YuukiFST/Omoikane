"""What a scheduled headless run may do, rendered for each harness wiki-ingest.ps1 drives, and checked after it.

One scope, two renderings: the Claude Code flags and the OpenCode permission config were once written apart, and
the OpenCode run had none at all (#39). The scope: read the repository, edit only wiki pages (`.md`), the log and
the review queue, run only the index and lint scripts, no git, nothing else.
Permission rules are the harness's and have holes the harness owns (an OpenCode `apply_patch` may move a wiki page
onto any path), so `verify` compares the working tree before and after the run and fails on any change outside
the scope, whichever harness ran.

Usage: python omoikane/bin/headless-scope.py claude
       python omoikane/bin/headless-scope.py opencode --agent-name NAME
       python omoikane/bin/headless-scope.py snapshot > before.json
       python omoikane/bin/headless-scope.py verify --before before.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from wikilib import REPO

# Repository-relative, gitignore style. Pages only: a `.py` under omoikane/wiki/ would run as
# `python omoikane/bin/wiki-index.py` from inside omoikane/wiki/ (#39).
EDITABLE = ("omoikane/wiki/**/*.md", "omoikane/log.md", "omoikane/_review.md")
# Named exactly: a wildcard would run a script the agent wrote into omoikane/bin/, or one reached through `..`.
SCRIPTS = ("python omoikane/bin/wiki-index.py", "python omoikane/bin/wiki-lint.py")
# Written by an allowed script (wiki-index.py), so a change there is in scope too.
GENERATED = ("omoikane/index.md",)


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


def opencode_config(agent_name: str) -> dict[str, object]:
    """OpenCode config (schema https://opencode.ai/config.json, rules https://opencode.ai/docs/permissions/)
    defining the agent wiki-ingest.ps1 runs with `opencode run --pure --agent <agent_name>`.

    `*` matches any run of characters, `/` included, and the last matching rule wins, so every map opens with
    `"*": "deny"`; `edit` covers the edit, write and patch tools; the `"*"` permission denies every one not named.
    Why an agent: OpenCode merges config maps key by key, so a user's `"bash": {"*": "allow", "git *": "allow"}`
    kept `git *` after a top-level `"*": "deny"` and git ran again; agent rules come after every top-level rule.
    Why a fresh name per run: an agent of the same name in the user's config would merge into ours the same way.
    `read` keeps OpenCode's `.env` protection and denies MCP resources (`mcp:<server>:<uri>`), which the plain
    string "allow" would grant.
    Example: opencode_config("omoikane-headless-1a2b3c4d")["agent"]["omoikane-headless-1a2b3c4d"]["mode"]
    returns "primary".
    """
    return {"agent": {agent_name: {
        "mode": "primary",
        "description": "Scheduled Omoikane run: edits wiki pages, runs index and lint, nothing else.",
        "permission": {
            "*": "deny",
            "read": {"*": "allow", "*.env": "deny", "*.env.*": "deny", "*.env.example": "allow", "mcp:*": "deny"},
            "glob": "allow", "grep": "allow", "list": "allow", "todowrite": "allow",
            "edit": {"*": "deny", **{path.replace("**/", ""): "allow" for path in EDITABLE}},
            "bash": {"*": "deny", **{script: "allow" for script in SCRIPTS}},
        },
    }}}


def in_scope(path: str) -> bool:
    """Whether a change to `path` (repository-relative, `/`) is one the headless run may make.

    Example: in_scope("omoikane/wiki/gotchas/a.md") returns True; in_scope("omoikane/wiki/a.py") returns False.
    """
    if path in EDITABLE or path in GENERATED:
        return True
    return path.startswith("omoikane/wiki/") and path.endswith(".md") and ".." not in path.split("/")


def git(repo: Path, *args: str, stdin: str | None = None) -> str:
    return subprocess.run(["git", "-C", str(repo), "-c", "core.quotePath=false", *args], input=stdin,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def snapshot(repo: Path = REPO) -> dict[str, object]:
    """HEAD, the staged tree and a content hash of every changed or untracked file (ignored files left out).

    Example: snapshot(repo) returns {"head": "<sha>", "index": "<tree sha>", "files": {"omoikane/log.md": "<sha>"}}.
    """
    entries = [e for e in git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all").split("\0") if e]
    paths: list[str] = []
    skip = False
    for entry in entries:
        if skip:  # the second path of a rename entry names its source
            skip = False
            paths.append(entry)
            continue
        skip = entry[0] in "RC"
        paths.append(entry[3:])
    present = [p for p in paths if (repo / p).is_file()]
    hashes = git(repo, "hash-object", "--stdin-paths", stdin="\n".join(present) + "\n").split() if present else []
    files: dict[str, str] = {p: "deleted" for p in paths}
    files.update(zip(present, hashes))
    return {"head": git(repo, "rev-parse", "HEAD").strip(), "index": git(repo, "write-tree").strip(), "files": files}


def out_of_scope(before: dict[str, object], after: dict[str, object]) -> list[str]:
    """Every change between two snapshots the headless run may not make: HEAD or the staged tree moved, or a
    file outside the scope changed, appeared or went away.

    Example: out_of_scope(snap, {**snap, "files": {"AGENTS.md": "<sha>"}}) returns ["AGENTS.md"].
    """
    problems = [f"{key} moved" for key in ("head", "index") if before[key] != after[key]]
    old, new = dict(before["files"]), dict(after["files"])  # type: ignore[arg-type]
    problems += sorted(p for p in set(old) | set(new) if old.get(p) != new.get(p) and not in_scope(p))
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("action", choices=("claude", "opencode", "snapshot", "verify"))
    parser.add_argument("--agent-name", default="omoikane-headless")
    parser.add_argument("--before", type=Path)
    args = parser.parse_args(argv)
    if args.action == "claude":
        print(json.dumps(claude_args()))
    elif args.action == "opencode":
        print(json.dumps(opencode_config(args.agent_name)))
    elif args.action == "snapshot":
        print(json.dumps(snapshot()))
    else:
        problems = out_of_scope(json.loads(args.before.read_text(encoding="utf-8")), snapshot())
        for problem in problems:
            print(f"headless-scope: out of scope: {problem}")
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
