"""What a scheduled headless run may do, rendered for each harness wiki-ingest.ps1 drives, and checked after it.

One scope, two renderings: the Claude Code flags and the OpenCode permission config were once written apart, and
the OpenCode run had none at all (#39). The scope: read the repository, edit only wiki pages (`.md`), the log and
the review queue. No shell at all: an allowed script is code the agent can replace or shadow from a directory it
writes to, so wiki-ingest.ps1 runs index and lint itself and hands the findings back.
Permission rules are the harness's and have holes the harness owns, so `verify` compares the working tree before
and after the run. wiki-ingest.ps1 runs a private copy of this file with `python -I`: nothing the agent writes
into the repository is on its path. Standard library only, for the same reason.

Usage: python -I headless-scope.py --repo DIR claude
       python -I headless-scope.py --repo DIR opencode --agent-name NAME
       python -I headless-scope.py --repo DIR snapshot > before.json
       python -I headless-scope.py --repo DIR verify --before before.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Repository-relative, gitignore style.
EDITABLE = ("omoikane/wiki/**/*.md", "omoikane/log.md", "omoikane/_review.md")
# Written while the run lasts by someone other than the agent: the Stop hook of a coding session in the same tree.
WRITTEN_BY_OTHERS = ("omoikane/raw/inbox/",)


def claude_args() -> list[str]:
    """Flags for `claude -p`, after the prompt.

    --tools offers no shell: there is nothing to allow or deny for one. --setting-sources project: allow rules
    and PreToolUse hooks in the user's own settings would otherwise apply too (#25); --strict-mcp-config keeps
    MCP servers out. dontAsk denies whatever the list does not allow. Edit(...) rules cover the Write tool; a
    leading / anchors at the repository root.
    Example: claude_args()[:2] returns ["--setting-sources", "project"].
    """
    allowed = ["Read", "Glob", "Grep", *(f"Edit(/{path})" for path in EDITABLE)]
    return ["--setting-sources", "project", "--strict-mcp-config", "--tools", "Read,Glob,Grep,Edit,Write",
            "--permission-mode", "dontAsk", "--allowedTools", ",".join(allowed)]


def opencode_config(agent_name: str) -> dict[str, object]:
    """OpenCode config (schema https://opencode.ai/config.json, rules https://opencode.ai/docs/permissions/)
    defining the agent wiki-ingest.ps1 runs with `opencode run --pure --agent <agent_name>`.

    `*` matches any run of characters, `/` included, and the last matching rule wins, so every map opens with
    `"*": "deny"`; the `"*"` permission denies every one not named, bash among them. Why an agent: OpenCode
    merges config maps key by key, so a user's `"bash": {"*": "allow", "git *": "allow"}` kept `git *` after a
    top-level deny; agent rules come after the top-level ones. Why a fresh name per run: a same-named agent in
    the user's config would merge into ours the same way. `apply_patch` is denied: it checks `edit` on the source
    of a move, not on its target. `read` keeps OpenCode's `.env` protection and denies MCP resources.
    Example: opencode_config("omoikane-headless-1a2b3c4d")["agent"]["omoikane-headless-1a2b3c4d"]["mode"]
    returns "primary".
    """
    return {"agent": {agent_name: {
        "mode": "primary",
        "description": "Scheduled Omoikane run: edits wiki pages, the log and the review queue, nothing else.",
        "permission": {
            "*": "deny",
            "read": {"*": "allow", "*.env": "deny", "*.env.*": "deny", "*.env.example": "allow", "mcp:*": "deny"},
            "glob": "allow", "grep": "allow", "list": "allow", "todowrite": "allow",
            "edit": {"*": "deny", **{path.replace("**/", ""): "allow" for path in EDITABLE}},
            "apply_patch": "deny",
        },
    }}}


def in_scope(path: str) -> bool:
    """Whether a change to `path` (repository-relative, `/`) may happen during the run.

    Example: in_scope("omoikane/wiki/gotchas/a.md") returns True; in_scope("omoikane/wiki/a.py") returns False.
    """
    if path in EDITABLE or path.startswith(WRITTEN_BY_OTHERS):
        return True
    return path.startswith("omoikane/wiki/") and path.endswith(".md") and ".." not in path.split("/")


def git(repo: Path, *args: str, stdin: str | None = None) -> str:
    return subprocess.run(["git", "-C", str(repo), "-c", "core.quotePath=false", *args], input=stdin,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def snapshot(repo: Path) -> dict[str, object]:
    """HEAD, the staged tree and a content hash of every changed or untracked file (ignored files left out).

    Example: snapshot(repo) returns {"head": "<sha>", "index": "<tree sha>", "files": {"omoikane/log.md": "<sha>"}}.
    """
    entries = iter(e for e in git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all").split("\0") if e)
    paths: list[str] = []
    for entry in entries:
        paths.append(entry[3:])
        if "R" in entry[:2] or "C" in entry[:2]:  # a rename or copy is followed by its source path
            paths.append(next(entries, ""))
    files: dict[str, str] = {}
    for path in filter(None, paths):
        full = repo / path
        files[path] = (git(repo, "hash-object", "--", path).strip() if full.is_file()
                       else "directory" if full.is_dir() else "deleted")
    return {"head": git(repo, "rev-parse", "HEAD").strip(), "index": git(repo, "write-tree").strip(), "files": files}


def out_of_scope(before: dict[str, object], after: dict[str, object]) -> list[str]:
    """Every change between two snapshots the run may not make: HEAD or the staged tree moved, or a file outside
    the scope changed, appeared or went away.

    Example: out_of_scope(snap, {**snap, "files": {"AGENTS.md": "<sha>"}}) returns ["AGENTS.md"].
    """
    problems = [f"{key} moved" for key in ("head", "index") if before[key] != after[key]]
    old, new = dict(before["files"]), dict(after["files"])  # type: ignore[arg-type]
    problems += sorted(p for p in set(old) | set(new) if old.get(p) != new.get(p) and not in_scope(p))
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent.parent)
    parser.add_argument("action", choices=("claude", "opencode", "snapshot", "verify"))
    parser.add_argument("--agent-name", default="omoikane-headless")
    parser.add_argument("--before", type=Path)
    args = parser.parse_args(argv)
    if args.action == "claude":
        print(json.dumps(claude_args()))
    elif args.action == "opencode":
        print(json.dumps(opencode_config(args.agent_name)))
    elif args.action == "snapshot":
        print(json.dumps(snapshot(args.repo)))
    else:
        problems = out_of_scope(json.loads(args.before.read_text(encoding="utf-8")), snapshot(args.repo))
        for problem in problems:
            print(f"headless-scope: out of scope: {problem}")
        return 3 if problems else 0  # 3, not 1: a crash exits 1 and must not read as a verdict
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
