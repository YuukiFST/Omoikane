---
title: git log --since a bare date starts at the current time of day
type: gotcha
summary: git log --since=<date> reads a bare date as that date at the current time, so morning commits drop out; add 00:00
tags: [git, wrap-up, dates]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-180e52eb.md]
code: [omoikane/prompts/wrap-up.md]
guard: none
---

## Behaviour

The end-to-end run of `/wrap-up 4` in a throwaway clone read the commits of the period with `git log --since=<date>`; the agent running it found that this missed the morning's commits (source: [[session-2026-10-06-180e52eb]], turn 6).
Cause, from the fix commit `d5eded9`: "git log --since=<date> reads a bare date as that date at the current time of day, so the end-to-end run of /wrap-up 4 missed a4e7ccd and 2ef4bdb until it retried with 00:00."

## Workaround

Give the time with the date: `--since="<period start> 00:00"`.
`omoikane/prompts/wrap-up.md` step 3 does so and says why (turn 6).
