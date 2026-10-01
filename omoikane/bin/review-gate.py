"""Keep the scheduled run's commits off the human's checkout: a worktree on wiki/auto, pushed as a PR to main.

`prepare` brings the worktree up to date (origin/wiki/auto, then origin/main, both by merge: no rebase, no
force-push) and moves the quiet captures from the human's inbox into it; wiki-ingest.ps1 then runs there and
commits each operation. `publish` pushes wiki/auto and opens the PR, or lets the push update the open one.
Merging stays the human's act (#45).

Usage: python omoikane/bin/review-gate.py prepare [--quiet-minutes 30] [--worktree DIR]   # prints the worktree
       python omoikane/bin/review-gate.py publish [--worktree DIR]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, Sequence

from wikilib import REPO

BRANCH = "wiki/auto"
INBOX = Path("omoikane/raw/inbox")
# Generated from frontmatter, so both sides of a conflict are wrong and the regenerated file is right.
INDEX = "omoikane/index.md"


class GateError(Exception):
    """The worktree cannot be brought up to date without a human: a conflict, or a run that left changes."""


def git(cwd: Path, *args: str) -> str:
    run = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, encoding="utf-8", check=False)
    if run.returncode != 0:
        raise GateError(f"git {' '.join(args)}: {run.stderr.strip()}")
    return run.stdout


def default_worktree(repo: Path) -> Path:
    """Beside the repository, so no tool that walks the checkout sees it. Example: .../omoikane-wiki-auto."""
    return repo.parent / f"{repo.name}-wiki-auto"


def run_wiki_index(worktree: Path) -> None:
    subprocess.run([sys.executable, str(worktree / "omoikane" / "bin" / "wiki-index.py")], cwd=worktree,
                   capture_output=True, check=True)


def remote_branch_exists(repo: Path) -> bool:
    return bool(git(repo, "branch", "--remotes", "--list", f"origin/{BRANCH}").strip())


def merge(worktree: Path, ref: str, regenerate: Callable[[Path], None]) -> None:
    """Merge `ref` into the worktree's branch. A conflict in the generated index alone is resolved by
    regenerating it; any other conflict is aborted, leaving the branch as it was, and raised.
    Example: merge(work, "origin/main", run_wiki_index).
    """
    run = subprocess.run(["git", "-C", str(worktree), "merge", "--no-edit", ref], capture_output=True, text=True,
                         encoding="utf-8", check=False)
    if run.returncode == 0:
        return
    conflicted = git(worktree, "diff", "--name-only", "--diff-filter=U").split()
    if conflicted == [INDEX]:
        regenerate(worktree)
        git(worktree, "add", INDEX)
        git(worktree, "commit", "--no-edit", "-q")
        return
    subprocess.run(["git", "-C", str(worktree), "merge", "--abort"], capture_output=True, check=False)
    raise GateError(f"{BRANCH} conflicts with {ref} in {', '.join(conflicted) or run.stderr.strip()}; "
                    "merge it by hand in the worktree")


def move_captures(repo: Path, worktree: Path, quiet_minutes: int, now: float) -> list[str]:
    """Move inbox files from the checkout into the worktree. A captured session modified in the last
    `quiet_minutes` may still be growing (the Stop hook rewrites it every turn) and stays.
    Example: move_captures(repo, work, 30, time.time()) returns ["omoikane/raw/inbox/sessions/<day>-<id8>.md"].
    """
    moved: list[str] = []
    inbox = repo / INBOX
    for path in sorted(p for p in inbox.rglob("*") if p.is_file() and p.name != ".gitkeep") if inbox.is_dir() else []:
        if path.parent.name == "sessions" and path.stat().st_mtime > now - quiet_minutes * 60:
            continue
        rel = path.relative_to(repo).as_posix()
        (worktree / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(worktree / rel))
        moved.append(rel)
    return moved


def prepare(repo: Path, worktree: Path, quiet_minutes: int, regenerate: Callable[[Path], None] = run_wiki_index,
            now: float | None = None) -> list[str]:
    """Bring the worktree on wiki/auto up to date with origin and move the quiet captures into it.

    Returns the moved paths. Raises GateError when the worktree holds changes a crashed run left, or a merge
    conflicts outside the index: both need the human, and running on would bury them.
    Example: prepare(Path("omoikane"), Path("omoikane-wiki-auto"), 30) returns ["omoikane/raw/inbox/a.md"].
    """
    git(repo, "fetch", "-q", "--prune", "origin")
    remote = remote_branch_exists(repo)
    if not (worktree / ".git").exists():
        git(repo, "worktree", "prune")
        git(repo, "worktree", "add", "-q", "-B", BRANCH, str(worktree), f"origin/{BRANCH}" if remote else "origin/main")
    dirty = git(worktree, "status", "--porcelain", "--untracked-files=all").strip()
    if dirty:
        raise GateError(f"the worktree has changes no run committed:\n{dirty}")
    if remote:
        merge(worktree, f"origin/{BRANCH}", regenerate)
    merge(worktree, "origin/main", regenerate)
    return move_captures(repo, worktree, quiet_minutes, time.time() if now is None else now)


def publish(worktree: Path, gh: Sequence[str] = ("gh",)) -> str:
    """Push wiki/auto when it is ahead of origin/main and open the PR, or let the push update the open one.

    Example: publish(Path("omoikane-wiki-auto")) returns "pushed; opened https://github.com/o/r/pull/9".
    """
    ahead = git(worktree, "log", "--format=- %s", "--reverse", "origin/main..HEAD").strip()
    if not ahead:
        return "nothing to publish"
    git(worktree, "push", "-q", "-u", "origin", f"HEAD:refs/heads/{BRANCH}")

    def run_gh(*args: str) -> str:
        return subprocess.run([*gh, *args], cwd=worktree, capture_output=True, text=True, encoding="utf-8",
                              check=True).stdout

    open_prs = json.loads(run_gh("pr", "list", "--head", BRANCH, "--base", "main", "--state", "open",
                                 "--json", "number,url") or "[]")
    if open_prs:
        return f"pushed; PR #{open_prs[0]['number']} updated"
    body = ("Opened by the scheduled run of `omoikane/bin/wiki-ingest.ps1 -Commit` (review gate). "
            "Read the diff before merging; the run never merges.\n\n" + ahead + "\n")
    url = run_gh("pr", "create", "--base", "main", "--head", BRANCH, "--title", "wiki: scheduled updates",
                 "--body", body).strip()
    return f"pushed; opened {url}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("action", choices=("prepare", "publish"))
    parser.add_argument("--worktree", type=Path, default=default_worktree(REPO))
    parser.add_argument("--quiet-minutes", type=int, default=30)
    args = parser.parse_args(argv)
    try:
        if args.action == "prepare":
            for rel in prepare(REPO, args.worktree, args.quiet_minutes):
                print(f"review-gate: moved {rel}", file=sys.stderr)
            print(args.worktree)
        else:
            print(f"review-gate: {publish(args.worktree)}")
    except (GateError, subprocess.CalledProcessError) as exc:
        print(f"review-gate: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
