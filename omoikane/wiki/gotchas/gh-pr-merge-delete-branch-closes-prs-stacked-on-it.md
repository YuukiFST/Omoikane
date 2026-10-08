---
title: gh pr merge delete-branch closes PRs stacked on it
type: gotcha
summary: gh pr merge --delete-branch on a stack's base closed PR #113 instead of retargeting it; retarget upper PRs to main first
tags: [gh, github, pull-request, git]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-07-9e3fae7e.md]
guard: none
---

## Behaviour

The handoff for issue #111 expected GitHub to move the next PR's base to `main` after each merge: "Depois de cada merge, confira que o GitHub mudou a base do PR seguinte para main" (source: [[session-2026-10-07-9e3fae7e]], turn 2).
It did not.
`gh pr merge 112 --merge --delete-branch` merged #112 and deleted `docs/111-dev-pack-spec`, and GitHub closed #113, whose base was that branch (turn 3).
The agent's note: "o `gh pr merge --delete-branch` apaga o branch pela API, e nesse caso o GitHub fecha os PRs que apontam para ele em vez de mudar a base" (turn 3).

An earlier stack merged #72 "after retargeting it to `main`" ([[session-2026-10-02-a8b45323]]); that page does not say why.

## Workaround

Before you merge a PR with `--delete-branch`, move each open PR whose base is its head branch to `main`: `gh pr edit <n> --base main` (turn 3).
The session did this for #114 before it merged #113, and for #117, #116, #118 and #115 before it merged #114; no other PR closed (turn 3).

When a PR is already closed this way (turn 3):

1. Recreate the deleted branch at the merged head: `git push -q origin <sha>:refs/heads/<branch>`.
2. Reopen the PR and move its base: `gh pr reopen <n> && gh pr edit <n> --base main`.
3. Wait for the PR's CI to run again on the new base; #113's run passed.
4. Delete the recreated branch: `git push origin --delete <branch>`.

The auto mode classifier blocked step 4 for the agent; the user ran it from the prompt with `!` (turns 3, 5).

The rule in [[review-each-pr-with-a-subagent-before-merging]] merges with `gh pr merge <n> --merge --delete-branch`, so this applies to every stack of PRs.
