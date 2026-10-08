---
title: git merge --no-commit needs a committer identity
type: gotcha
summary: git merge --no-commit still wants user.name and user.email; the CI runner has none, so a merge test passed only locally
tags: [git, ci, testing, template]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-973284b2.md]
code: [omoikane/bin/update-from-template.py, tests/test_new_system.py]
guard: test
---

`omoikane/bin/update-from-template.py` merges `template/main` with `git merge --no-commit` (see [[update-from-template]]).
Its tests passed on the developer's machine, and CI of PR #108 failed (source: [[session-2026-10-06-973284b2]], turn 2).
The cause: "`git merge --no-commit` exige identidade de committer e o runner não tem. Usuário real tem" (turn 2).
The merge stops for a missing identity even though it writes no commit.

Workaround: a test that runs a merge sets an identity in the repository it creates.
`UpdateFromTemplate` in `tests/test_new_system.py` runs `git config user.name` and `git config user.email` in each system repository, with a comment giving the reason (commit `e65278a`).
The test helper `git()` in the same file passes `-c user.name=t -c user.email=t@example.invalid` for its own commands, but that does not reach the git commands the script runs.

Guard: the CI test job, which has no git identity, fails any such test that lacks one.
