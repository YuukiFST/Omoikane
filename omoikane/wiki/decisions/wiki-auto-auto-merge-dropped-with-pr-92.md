---
title: wiki/auto auto-merge dropped with PR 92
type: decision
summary: PR #92 and issue #74 closed unmerged, superseded by #101; the wiki/auto PR keeps the human merge
tags: [review-gate, auto-merge, autonomy-loop, wrap-up]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/2026-10-06-pstack-skills-review-round-2.md]
code: [omoikane/bin/review-gate.py]
---

## Decision

PR #92, which turned on auto-merge for the `wiki/auto` PR, and its issue #74 were closed unmerged as superseded by #101 (source: [[session-2026-10-06-61eabe29]], turns 6, 7).
The agent recommended it and the user approved it: "Agora fecho #92 e a issue #74, que você aprovou." (turn 6).
The branch `feat/74-auto-merge-wiki-auto` stays on the remote; its worktree `omoikane-74` and the local branch were removed (turn 7).
So `review-gate.py publish` on `main` still leaves the merge of the `wiki/auto` PR to the human ([[review-gate]]).

## Reason

The agent's recommendation (turn 6):
- The auto-merge only serves the `wiki/auto` PR of the scheduled run, which is off on this machine, and `/wrap-up` leaves the commit to the user ([[wiki-is-fed-by-an-end-of-day-wrap-up-the-schedule-is-opt-in]]).
- It would not work today even with the schedule on: `allow_auto_merge` is `false` and `main` has no required status check. Without that check, `gh pr merge --auto` merges at once, before CI ([[gh-pr-merge-auto-merges-at-once-when-no-check-is-required]]).

The closing comment on #92 opens: "Closing as superseded by #101: /wrap-up is now the default path, where the human commits the wiki changes, and scheduling is opt-in." (turn 6).

## Rejected alternative

Keep #92 and merge it: see [[wiki-auto-pr-merges-itself-once-checks-pass]], the earlier choice.

## History

Reverses [[wiki-auto-pr-merges-itself-once-checks-pass]] (source: [[session-2026-10-02-a9384e33]]), made before `/wrap-up` replaced the scheduled run as the default.

## Contradictions

- This page: #92 was closed unmerged on 2026-10-06; `gh` gives `closedAt` 12:41 UTC (source: [[session-2026-10-06-61eabe29]], turn 6).
- The pstack round-2 note, dated 2026-10-06, still expects it: proposal 4 gains weight "once the `wiki/auto` PR merges itself (PR #92)" (source: [[2026-10-06-pstack-skills-review-round-2]], proposal 4). Its three other proposals became issues at 13:30 UTC, after the close.
