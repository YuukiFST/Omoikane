---
title: wiki/auto PR merges itself once checks pass
type: decision
summary: Reversed: the user chose auto-merge for the wiki/auto PR (PR #92); #92 was later closed unmerged
tags: [review-gate, auto-merge, autonomy-loop]
created: 2026-10-06
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-02-a9384e33.md, wiki/sources/session-2026-10-06-180e52eb.md, wiki/sources/session-2026-10-06-61eabe29.md]
code: [omoikane/bin/review-gate.py, tests/test_review_gate.py]
---

## Decision

`review-gate.py publish` opens the `wiki/auto` PR with auto-merge on, and GitHub merges it once the required checks pass; the human can disable auto-merge or close the PR to hold it (source: [[session-2026-10-02-a9384e33]], turns 2, 4; issue #74, PR #92).
The user decided it when asked at the start of the session; the agent's summary: "Auto-merge: aplicado no #92." (turn 9).

## Rejected alternative and reason

The human merging every `wiki/auto` PR, as `review-gate.py` says on `main` ("Merging stays the human's act (#45)").
The handoff prompt gave the reason: "Hoje o conhecimento só chega às sessões depois que eu faço o merge do PR do `wiki/auto`, o que contraria o 'sem envolvimento'." (turn 2).
It also noted that the permission classifier had refused this change once, and that the decision was the user's (turn 2).

## How

- Auto-merge is requested once, when `publish` opens the PR; a later push leaves it as the human last set it (branch `feat/74-auto-merge-wiki-auto`).
- Through the GraphQL mutation, not `gh pr merge --auto`: [[gh-pr-merge-auto-merges-at-once-when-no-check-is-required]] (turn 4).
- No retry when GitHub reports the PR state as UNKNOWN right after it is created: the risk was not verified, and the agent left retry out because the user's rules admit defensive code only when asked; a stuck PR shows as "auto-merge off" (turn 9).

## Status

At capture PR #92 was open, reviewed twice by subagents with the real findings fixed, not merged (turn 9).
On `main` at `887725a` it is still open, and `docs/architecture.md` now makes `/wrap-up` the default way to feed the wiki, with the scheduled run that publishes `wiki/auto` as an opt-in (#101).
The session that merged #102 noted that #92 "só tem valor para quem usa a execução agendada" and asked the user to decide whether it still makes sense (source: [[session-2026-10-06-180e52eb]], turn 8); see [[wiki-is-fed-by-an-end-of-day-wrap-up-the-schedule-is-opt-in]].
On 2026-10-06 the user approved closing #92 and issue #74 unmerged, as superseded by #101 (source: [[session-2026-10-06-61eabe29]], turns 6, 7).

## History

Reversed by [[wiki-auto-auto-merge-dropped-with-pr-92]]: the auto-merge only served the opt-in scheduled run, and the repository lacks "Allow auto-merge" and a required check (source: [[session-2026-10-06-61eabe29]], turn 6).
