"""Merge the template's later prompts, scripts and docs into a system, keeping the system's own memory.

A system born from the template had no path to take later fixes: a plain `git merge template/main` brought the
template's own captures and pages into the system's wiki and conflicted on _review.md and index.md (#105). This
fetches the `template` remote, merges template/main without committing, puts back the paths the system owns
(MEMORY) as HEAD has them, removes what the template added there, keeps the rules block of AGENTS.md as the
system has it and regenerates index.md. Any other conflict stays for the human. It refuses a tree with
uncommitted changes and never commits: read `git diff --cached`, then commit, or undo with `git merge --abort`.

A repository made with "Use this template" shares no commit with the template, and its root commit holds the
template's tree as it was. The template commit with that tree is grafted under the root for the merge only, so
the merge finds the base a clone would; the merge commit then relates the histories for every later update.

Usage: python omoikane/bin/update-from-template.py [--branch main]
"""
from __future__ import annotations

import argparse
import importlib
import subprocess
import sys
import tempfile
from pathlib import Path

from wikilib import REPO, RULES_END, RULES_START, load_pages

wiki_index = importlib.import_module("wiki-index")

TEMPLATE_REMOTE = "template"
# What the system learned about itself; the template's own copies of these are its memory, not a fix.
MEMORY = ("omoikane/wiki", "omoikane/raw", "omoikane/log.md", "omoikane/_review.md")
INDEX = "omoikane/index.md"
AGENTS = "AGENTS.md"


class Refused(Exception):
    """A reason to stop before the tree is changed."""


def git(repo: Path, *args: str, ok: tuple[int, ...] = (0,)) -> str:
    run = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8")
    if run.returncode not in ok:
        raise subprocess.CalledProcessError(run.returncode, ["git", *args], run.stdout, run.stderr)
    return run.stdout


def tracked(repo: Path, rev: str | None) -> set[str]:
    """Files under MEMORY in `rev`, or in the index when `rev` is None (unmerged paths included)."""
    listed = (git(repo, "ls-tree", "-r", "-z", "--name-only", rev, "--", *MEMORY) if rev
              else git(repo, "ls-files", "-z", "--", *MEMORY))
    return set(filter(None, listed.split("\0")))


def template_base(repo: Path, target: str) -> str | None:
    """The template commit whose tree is the tree of HEAD's root commit, for a history the template does not share.

    Example: template_base(Path("."), "template/main") returns the sha "Use this template" copied, or None.
    """
    roots = git(repo, "rev-list", "--max-parents=0", "HEAD").split()
    trees = {git(repo, "rev-parse", f"{root}^{{tree}}").strip(): root for root in roots}
    for line in git(repo, "log", "--format=%H %T", target).splitlines():
        commit, tree = line.split()
        if tree in trees:
            return commit
    return None


def with_rules(text: str, rules_from: str) -> str:
    """`text` with its managed rules block replaced by the one in `rules_from`; unchanged when either lacks one.

    Example: with_rules("a\\n<s>\\n- t\\n<e>\\nb", "<s>\\n- r\\n<e>") returns "a\\n<s>\\n- r\\n<e>\\nb" (markers
    abbreviated).
    """
    def block(t: str) -> tuple[int, int] | None:
        start, end = t.find(RULES_START), t.find(RULES_END)
        return (start, end + len(RULES_END)) if 0 <= start < end else None

    here, there = block(text), block(rules_from)
    if here is None or there is None:
        return text
    return text[:here[0]] + rules_from[there[0]:there[1]] + text[here[1]:]


def merge_agents(repo: Path, base: str, target: str) -> bool:
    """Merge AGENTS.md again with every side holding HEAD's rules block, so the template's own rules neither
    conflict nor arrive. Returns False when a conflict outside the block is left for the human.
    """
    def show(rev: str) -> str | None:
        text = git(repo, "show", f"{rev}:{AGENTS}", ok=(0, 128))
        return text or None

    ours, ancestor, theirs = show("HEAD"), show(base), show(target)
    if ours is None or ancestor is None or theirs is None:
        return True
    with tempfile.TemporaryDirectory() as tmp:
        files = []
        for name, text in (("ours", ours), ("base", with_rules(ancestor, ours)), ("theirs", with_rules(theirs, ours))):
            (Path(tmp) / name).write_text(text, encoding="utf-8", newline="\n")
            files.append(str(Path(tmp) / name))
        merged = subprocess.run(["git", "merge-file", "-p", "-L", "HEAD", "-L", "base", "-L", target, *files],
                                capture_output=True, text=True, encoding="utf-8")
    # The exit code counts the conflicts, up to 127; an error is negative, 255 as a process status.
    if not 0 <= merged.returncode <= 127:
        raise subprocess.CalledProcessError(merged.returncode, ["git", "merge-file"], merged.stdout, merged.stderr)
    (repo / AGENTS).write_text(merged.stdout, encoding="utf-8", newline="\n")
    if merged.returncode:
        return False
    git(repo, "add", "--", AGENTS)
    return True


def keep_memory(repo: Path) -> int:
    """Put MEMORY back as HEAD has it and drop what the merge added there; return how many files were dropped."""
    added = sorted(tracked(repo, None) - tracked(repo, "HEAD"))
    for start in range(0, len(added), 100):
        git(repo, "rm", "-q", "-f", "--", *added[start:start + 100])
    kept = [path for path in MEMORY if git(repo, "ls-tree", "--name-only", "HEAD", "--", path).strip()]
    if kept:
        git(repo, "checkout", "HEAD", "--", *kept)
    return len(added)


def update(repo: Path, branch: str) -> int:
    if TEMPLATE_REMOTE not in git(repo, "remote").split():
        raise Refused(f"no `{TEMPLATE_REMOTE}` remote; add the template with `git remote add {TEMPLATE_REMOTE} <url>`")
    if git(repo, "status", "--porcelain"):
        raise Refused("commit or discard these changes first, so `git merge --abort` can undo the update:\n"
                      + git(repo, "status", "--short"))
    git(repo, "fetch", "-q", TEMPLATE_REMOTE)
    target = f"{TEMPLATE_REMOTE}/{branch}"
    git(repo, "rev-parse", "--verify", "-q", target)
    grafted = None
    if not git(repo, "merge-base", "HEAD", target, ok=(0, 1)).strip():
        base = template_base(repo, target)
        if base is None:
            raise Refused(f"HEAD shares no history with {target}, and no commit of {target} has the tree of HEAD's "
                          "first commit; merge it by hand")
        grafted = git(repo, "rev-list", "--max-parents=0", "HEAD").split()[0]
        git(repo, "replace", "--graft", grafted, base)
    try:
        base = git(repo, "merge-base", "HEAD", target).strip()
        merged = subprocess.run(["git", "-C", str(repo), "merge", "--no-commit", "--no-ff", target],
                                capture_output=True, text=True, encoding="utf-8")
    finally:
        if grafted:
            git(repo, "replace", "-d", grafted)
    if not git(repo, "rev-parse", "-q", "--verify", "MERGE_HEAD", ok=(0, 1)).strip():
        if merged.returncode:  # stopped before merging, e.g. an untracked file the merge would overwrite
            raise subprocess.CalledProcessError(merged.returncode, merged.args[3:], merged.stdout, merged.stderr)
        print(f"update-from-template: nothing to merge from {target}")
        return 0
    dropped = keep_memory(repo)
    agents_merged = merge_agents(repo, base, target)
    (repo / INDEX).write_text(wiki_index.render(load_pages(repo / "omoikane" / "wiki")), encoding="utf-8",
                              newline="\n")
    git(repo, "add", "--", INDEX)
    left = git(repo, "diff", "--name-only", "--diff-filter=U").split()
    print(f"update-from-template: merged {target}; kept the system's memory as HEAD has it and dropped {dropped} "
          f"files the template added there{'' if agents_merged else '; AGENTS.md has a conflict outside the rules block'}")
    if left:
        print("update-from-template: resolve these, `git add` them, then commit:\n" + "\n".join(left))
        return 1
    print("update-from-template: read `git diff --cached`, then `git commit`; `git merge --abort` undoes it")
    return 0


def main(argv: list[str] | None = None, repo: Path = REPO) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--branch", default="main", help="template branch to merge (default: main)")
    args = parser.parse_args(argv)
    try:
        return update(repo, args.branch)
    except Refused as exc:
        print(f"update-from-template: {exc}; nothing was changed")
        return 2
    except subprocess.CalledProcessError as exc:
        print(f"update-from-template: `{' '.join(exc.cmd)}` failed: {(exc.stderr or exc.stdout).strip()}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
