---
title: Review each PR with a subagent before merging
type: practice
summary: Before merging a PR, post a subagent review on it and fix the real findings; merge only when the user authorized it
tags: [procedure, pull-request, code-review, git]
created: 2026-09-30
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-15-e04462b2.md, wiki/sources/session-2026-09-30-c14af01e.md]
---

## Rule

Before merging a PR in YuukiFST/Omoikane, have a subagent review it and post the findings on the PR.
Fix the findings judged real and wait for green CI.
Merge only when the user authorized it, then with `gh pr merge <n> --merge --delete-branch`, and close the issue.

## Evidence

- Issue #7: with CI green on PR #10, the agent noted "Code review agent still running in background; will post its findings on the PR, then merge" (source: [[session-2026-09-15-e04462b2]], turn 2). The `/code-review 10 --comment` agent posted 10 findings as inline comments; the agent triaged them, "fixing the real ones", and merged PR #10 with a merge commit (source: [[session-2026-09-15-e04462b2]], turn 3).
- Phase 2: "PR #22 (item 1) aberto ... Lanço revisão do #22 por subagente", then "Review do #22: 1 alto, 3 médios, 3 baixos. Posto no GitHub", fixes pushed before `gh pr merge 22 --merge --delete-branch` (source: [[session-2026-09-30-c14af01e]], turn 2). The final report: "Cada PR teve review de subagente postada como PR review, com os achados corrigidos antes do merge", for PRs #22 and #26 to #30 (source: [[session-2026-09-30-c14af01e]], turn 3).

## Scope

Both sessions merged into `main` with a merge commit, never a squash.
In the Phase 2 session the merge of #22 happened after "Merge do #22 autorizado" (source: [[session-2026-09-30-c14af01e]], turn 2); the push and merge confirmation rules of the user's git rules still apply.
