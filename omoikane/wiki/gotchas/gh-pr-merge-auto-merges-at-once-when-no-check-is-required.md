---
title: gh pr merge --auto merges at once when no check is required
type: gotcha
summary: On a PR GitHub sees as mergeable, `gh pr merge --auto` merges at once, before CI; call enablePullRequestAutoMerge
tags: [gh, github, auto-merge, review-gate]
created: 2026-10-06
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-02-a9384e33.md, wiki/sources/session-2026-10-06-61eabe29.md]
code: [omoikane/bin/review-gate.py]
guard: none
---

## Behaviour

`gh pr merge --auto` does not always turn on auto-merge.
When the PR is already CLEAN, with no required check left to wait for, it merges the PR at once, before CI runs (source: [[session-2026-10-02-a9384e33]], turn 4).
The agent's note: "faz merge direto quando o PR já está CLEAN, ou seja, antes do CI. É exatamente o caso deste repositório hoje." (turn 4).
The subagent review of PR #92 found it, and the agent confirmed it in the `gh` source: the comment in the fix names `gh merge.go`, `isImmediatelyMergeable` (turn 4; commit `0f405ac` on `feat/74-auto-merge-wiki-auto`).

## Workaround

Call the GraphQL mutation `enablePullRequestAutoMerge` directly; GitHub refuses it on a PR that is mergeable now, instead of merging (turn 4).
The agent read the input fields from the schema first (`__type(name:"EnablePullRequestAutoMergeInput")`) (turn 4).
PR #92 passes `pullRequestId`, `mergeMethod: MERGE` and `expectedHeadOid`, the commit `publish` pushed, and turns a refusal into an error that names what the repository needs: "Allow auto-merge" and a required status check on `main` (branch `feat/74-auto-merge-wiki-auto`).
See [[wiki-auto-pr-merges-itself-once-checks-pass]].

## Guard

PR #92 changes `tests/test_review_gate.py` so its fake `gh` takes the mutation (`test_publish_pushes_and_opens_one_pr`) and adds a refusal case, `test_a_refused_auto_merge_fails_the_publish_and_later_ones_report_it` (turn 4; branch `feat/74-auto-merge-wiki-auto`).
They are not on `main` until PR #92 merges, so the guard is `none` today.
PR #92 was closed unmerged on 2026-10-06, so these tests never reached `main` ([[wiki-auto-auto-merge-dropped-with-pr-92]]; source: [[session-2026-10-06-61eabe29]], turns 6, 7).
On that date the repository still had `allow_auto_merge` set to `false` and no required status check on `main` (turn 6).
