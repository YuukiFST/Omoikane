"""Keep the scheduled run's commits off the human's checkout: a worktree on wiki/auto, pushed as a PR to main.

`prepare` brings the worktree up to date (origin/wiki/auto, then origin/main, both by merge: no rebase, no
force-push) and moves the quiet captures from the human's inbox into it; wiki-ingest.ps1 then runs there and
commits each operation. `publish` pushes wiki/auto and opens the PR, or lets the push update the open one.
Merging stays the human's act (#45).

Usage: python omoikane/bin/review-gate.py prepare [--quiet-minutes 30] [--worktree DIR]
       python omoikane/bin/review-gate.py publish [--worktree DIR] [--gh PATH]
"""
from __future__ import annotations

import argparse
import difflib
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
# The human decides here by deleting and ticking bullets, the run only appends: a conflict is resolved as main's
# file plus the bullets the branch added. Not merge=union, which brought deleted bullets back (#56 review).
REVIEW = "omoikane/_review.md"
# All that -Commit commits. The scheduler runs the worktree's own scripts, so wiki/auto may differ from main in
# nothing else: it is not a protected branch (#56 review).
COMMITTED = ("omoikane/wiki", "omoikane/raw", "omoikane/log.md", REVIEW, INDEX)
BLOCKED = "omoikane/.wiki-ingest.blocked"


class GateError(Exception):
    """The worktree cannot be brought up to date without a human: a conflict, or a run that left changes."""


def git(cwd: Path, *args: str) -> str:
    run = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, encoding="utf-8", check=False)
    if run.returncode != 0:
        raise GateError(f"git {' '.join(args)}: {run.stderr.strip()}")
    return run.stdout


def git_ok(cwd: Path, *args: str) -> bool:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, check=False).returncode == 0


def default_worktree(repo: Path) -> Path:
    """Beside the repository, so no tool that walks the checkout sees it. Example: .../omoikane-wiki-auto."""
    return repo.parent / f"{repo.name}-wiki-auto"


def run_wiki_index(worktree: Path) -> None:
    subprocess.run([sys.executable, str(worktree / "omoikane" / "bin" / "wiki-index.py")], cwd=worktree,
                   capture_output=True, check=True)


def remote_branch_exists(repo: Path) -> bool:
    return bool(git(repo, "branch", "--remotes", "--list", f"origin/{BRANCH}").strip())


def added_hunks(base: list[str], ours: list[str]) -> list[tuple[str | None, list[str]]]:
    """Each run of lines `ours` inserted relative to `base`, with the base line it follows (None at the top).

    Example: added_hunks(["a\\n", "b\\n"], ["a\\n", "x\\n", "b\\n"]) returns [("a\\n", ["x\\n"])].
    """
    return [(base[i1 - 1] if i1 else None, ours[j1:j2])
            for tag, i1, _, j1, j2 in difflib.SequenceMatcher(None, base, ours, autojunk=False).get_opcodes()
            if tag in ("insert", "replace")]


def contains(lines: list[str], run: list[str]) -> bool:
    return any(lines[i:i + len(run)] == run for i in range(len(lines) - len(run) + 1))


def resolve_review(worktree: Path, ref: str) -> None:
    """Write _review.md as `ref`'s file plus each run of lines the branch added since the merge base, placed after
    the line it followed when that line is still there, at the end otherwise. A run already present as a whole is
    skipped; runs are compared whole, not line by line, so a diff proposal keeps its fences and headers.

    Example: base "a b", branch "a b c", main "a" (b rejected) gives "a c".
    """
    def show(rev: str) -> list[str]:
        text = git(worktree, "show", f"{rev}:{REVIEW}")
        return (text if text.endswith("\n") or not text else text + "\n").splitlines(keepends=True)

    base = git(worktree, "merge-base", "HEAD", ref).strip()
    result = show(ref)
    at = 0  # insertion point after the previous hunk, so hunks keep their order
    for anchor, run in added_hunks(show(base), show("HEAD")):
        if contains(result, run):
            continue
        found = next((i for i in range(at, len(result)) if result[i] == anchor), None) if anchor else -1
        at = len(result) if found is None else found + 1
        result[at:at] = run
        at += len(run)
    (worktree / REVIEW).write_text("".join(result), encoding="utf-8", newline="\n")


def merge(worktree: Path, ref: str, regenerate: Callable[[Path], None]) -> None:
    """Merge `ref` into the worktree's branch. A conflict in the generated index is resolved by regenerating it,
    one in _review.md by `resolve_review`; any other conflict is aborted, leaving the branch as it was, and raised.
    Example: merge(work, "origin/main", run_wiki_index).
    """
    run = subprocess.run(["git", "-C", str(worktree), "merge", "--no-edit", ref], capture_output=True, text=True,
                         encoding="utf-8", check=False)
    if run.returncode == 0:
        return
    conflicted = git(worktree, "diff", "--name-only", "--diff-filter=U").split()
    if conflicted and set(conflicted) <= {INDEX, REVIEW}:
        if REVIEW in conflicted:
            resolve_review(worktree, ref)
            git(worktree, "add", REVIEW)
        if INDEX in conflicted:
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
        if git_ok(repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{BRANCH}"):
            # Never -B over an existing branch: commits a failed publish left unpushed would be dropped.
            git(repo, "worktree", "add", "-q", str(worktree), BRANCH)
        else:
            git(repo, "worktree", "add", "-q", "-b", BRANCH, str(worktree),
                f"origin/{BRANCH}" if remote else "origin/main")
    if (worktree / BLOCKED).exists():
        raise GateError(f"{worktree / BLOCKED} is there: read the worktree and its .wiki-ingest.log, then delete it")
    # A source whose operation failed stays untracked in the inbox and is retried; it is not a crashed run's leftover.
    dirty = git(worktree, "status", "--porcelain", "--untracked-files=all", "--", ".", f":!{INBOX.as_posix()}").strip()
    if dirty:
        raise GateError(f"the worktree has changes no run committed:\n{dirty}")
    # Before any merge: resolving an index conflict runs the worktree's own wiki-index.py.
    for ref in ("HEAD", *((f"origin/{BRANCH}",) if remote else ())):
        refuse_code(worktree, f"origin/main...{ref}")
    if remote:
        merge(worktree, f"origin/{BRANCH}", regenerate)
    merge(worktree, "origin/main", regenerate)
    refuse_code(worktree, "origin/main", "HEAD")
    return move_captures(repo, worktree, quiet_minutes, time.time() if now is None else now)


def refuse_code(worktree: Path, *revs: str) -> None:
    """Raise GateError when the diff of `revs` touches anything -Commit does not commit.

    Example: refuse_code(work, "origin/main...HEAD") raises on a wiki/auto that edited omoikane/bin/wiki-index.py.
    """
    beyond = git(worktree, "diff", "--name-only", *revs, "--", ".", *(f":!{path}" for path in COMMITTED)).split()
    if beyond:
        raise GateError(f"{BRANCH} differs from main outside the wiki, and the scheduler would run it: "
                        f"{', '.join(beyond)}")


def publish(worktree: Path, gh: Sequence[str] = ("gh",)) -> str:
    """Push wiki/auto when it is ahead of origin/main and open the PR, or let the push update the open one.

    Example: publish(Path("omoikane-wiki-auto")) returns "pushed; opened https://github.com/o/r/pull/9".
    """
    ahead = git(worktree, "log", "--format=- %s", "--reverse", "origin/main..HEAD").strip()
    # After a squash merge the commits stay ahead of main, but their content is in it.
    if not ahead or git_ok(worktree, "diff", "--quiet", "origin/main", "HEAD"):
        return "nothing to publish"

    def run_gh(*args: str) -> str:
        run = subprocess.run([*gh, *args], cwd=worktree, capture_output=True, text=True, encoding="utf-8")
        if run.returncode != 0:  # gh's stderr says why, e.g. "gh auth login"
            raise GateError(f"gh {' '.join(args[:2])}: {run.stderr.strip()}")
        return run.stdout

    # `--state closed` also lists merged PRs. A rejected head that HEAD contains would go out again in a new PR,
    # whatever commits a later run or a merge from main put on top of it.
    closed = json.loads(run_gh("pr", "list", "--head", BRANCH, "--base", "main", "--state", "closed",
                               "--json", "number,headRefOid,state") or "[]")
    rejected = [pr for pr in closed if pr.get("state") == "CLOSED"
                and git_ok(worktree, "merge-base", "--is-ancestor", str(pr.get("headRefOid")), "HEAD")]
    if rejected:
        return (f"PR #{rejected[0]['number']} was closed unmerged and {BRANCH} still holds its commits; nothing "
                f"opened. To start over, reset {BRANCH} to origin/main in the worktree and delete the remote branch")
    git(worktree, "push", "-q", "-u", "origin", f"HEAD:refs/heads/{BRANCH}")
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
    parser.add_argument("--gh", default="gh", help="the gh executable, by path on Windows (wiki-ingest.ps1 resolves it)")
    args = parser.parse_args(argv)
    try:
        if args.action == "prepare":
            for rel in prepare(REPO, args.worktree, args.quiet_minutes):
                print(f"review-gate: moved {rel}", file=sys.stderr)
        else:
            print(f"review-gate: {publish(args.worktree, (args.gh,))}")
    except (GateError, subprocess.CalledProcessError) as exc:
        print(f"review-gate: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
