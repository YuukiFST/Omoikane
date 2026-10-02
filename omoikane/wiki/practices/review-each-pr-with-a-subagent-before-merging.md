---
title: Review each PR with a subagent before merging
type: practice
summary: Before merging a PR, post a subagent review on it and fix the real findings; merge only when the user authorized it
tags: [procedure, pull-request, code-review, git]
created: 2026-09-30
updated: 2026-10-02
sources: [wiki/sources/session-2026-09-15-e04462b2.md, wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-1b324082.md]
---

## Rule

Before merging a PR in YuukiFST/Omoikane, have a subagent review it and post the findings on the PR.
Fix the findings judged real and wait for green CI.
Merge only when the user authorized it, then with `gh pr merge <n> --merge --delete-branch`, and close the issue.

## Evidence

- Issue #7: with CI green on PR #10, the agent noted "Code review agent still running in background; will post its findings on the PR, then merge" (source: [[session-2026-09-15-e04462b2]], turn 2). The `/code-review 10 --comment` agent posted 10 findings as inline comments; the agent triaged them, "fixing the real ones", and merged PR #10 with a merge commit (source: [[session-2026-09-15-e04462b2]], turn 3).
- Phase 2: "PR #22 (item 1) aberto ... Lanço revisão do #22 por subagente", then "Review do #22: 1 alto, 3 médios, 3 baixos. Posto no GitHub", fixes pushed before `gh pr merge 22 --merge --delete-branch` (source: [[session-2026-09-30-c14af01e]], turn 2). The final report: "Cada PR teve review de subagente postada como PR review, com os achados corrigidos antes do merge", for PRs #22 and #26 to #30 (source: [[session-2026-09-30-c14af01e]], turn 3).
- Post-Phase 2: every item went through an issue, a branch and a subagent review posted on the PR; PR #36 merged after its review found unsupported claims on the pages (source: [[session-2026-09-30-230a182d]], turn 2).
- PR #40: a fourth review by a subagent, posted on the PR, found 9 more findings, fixed in `5fd7e8d`, and PR #48's review led to `--ignore-scripts` and `satisfies Hooks` (source: [[session-2026-10-01-b5b6fb27]], turn 2).
- PR #56: three more subagent review rounds, each posted on the PR with its resolution, before the merge commit `f2ba8ff`; PR #58, reviewed with CI green, was left for the user to authorise (source: [[session-2026-10-01-d4302021]], turns 3, 4).
- PRs #67 to #73: every PR got a subagent review and its findings fixed; only #58 was merged in the session (source: [[session-2026-10-02-1b324082]], turn 6).

## Scope

Every session merged into `main` with a merge commit, never a squash.
Authorisation can be given ahead in a handoff prompt: the turn-7 handoff of [[session-2026-10-02-1b324082]] let the next session merge PRs with review and green CI.
In the Phase 2 session the merge of #22 happened after "Merge do #22 autorizado" (source: [[session-2026-09-30-c14af01e]], turn 2); the push and merge confirmation rules of the user's git rules still apply.
