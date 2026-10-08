---
title: Git config and info are shared by every worktree
type: gotcha
summary: A worktree's .git config and info/ are shared; git push -u, branch -u or gc elsewhere tripped the scope check
tags: [git, worktree, headless-scope, wiki-ingest]
created: 2026-10-06
updated: 2026-10-06
sources: [wiki/sources/commits-2026-09-29-to-2026-10-06.md]
code: [omoikane/bin/headless-scope.py, tests/test_headless_scope.py]
guard: test
---

## Behaviour

The scope check of a scheduled run ([[headless-scope]]) snapshots the git config and `info/` before and after the agent runs.
Those files belong to the common git directory, shared by every worktree of the repository.
So `git push -u` or `git branch -u` in another worktree, or a `git gc`, changed them and blocked a run (source: [[commits-2026-09-29-to-2026-10-06]], `87d956b`).

## Workaround

The snapshot hashes the config without the `branch.`, `remote.`, `gc.` and `maintenance.` keys (`ROUTINE_CONFIG`), and reads only `info/exclude`, `info/attributes` and `info/sparse-checkout` (`GIT_INFO`) (`87d956b`).

## Guard

`tests/test_headless_scope.py` pins it.
