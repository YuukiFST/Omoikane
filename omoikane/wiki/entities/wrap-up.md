---
title: wrap-up
type: entity
summary: omoikane/prompts/wrap-up.md, the end-of-day pass: inbox through distill and ingest, commits of the period, synthesize
tags: [wrap-up, module, prompts, operation]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-180e52eb.md]
code: [omoikane/prompts/wrap-up.md, .claude/skills/wrap-up/SKILL.md]
---

`/wrap-up [days]` is the end-of-day pass that feeds the wiki by default (source: [[session-2026-10-06-180e52eb]], turns 4, 7); why: [[wiki-is-fed-by-an-end-of-day-wrap-up-the-schedule-is-opt-in]].
The prompt is `omoikane/prompts/wrap-up.md`; `.claude/skills/wrap-up/SKILL.md` and an OpenCode command point to it (turn 4).

## What it does

The agent processes every captured session and every source in the inbox, reads the commits of the period for what no session recorded, and runs `/synthesize` when it is due (turn 7).
It commits nothing: the user reviews the diff and commits (turn 7).
Each inbox file goes to its own subagent, one at a time, since every operation appends to `log.md` and `_review.md` (`omoikane/prompts/wrap-up.md`).

## How it was checked

- Full suite: one failure, the agent's own `AGENTS.md` lines over the budget, fixed in `0f1e6a1` (turn 5).
- End-to-end run of `/wrap-up 4` in a throwaway clone with no `origin`: 16 pages, lint clean, and one bug found: [[git-log-since-a-bare-date-starts-at-the-current-time-of-day]] (turn 6).
- A subagent review of PR #102 found 8 problems, all fixed: proposal bullets that came back after the human deleted them, UTC against local time when matching commits to sessions, and commits made on another machine, among others (turns 6, 7).
- The end-to-end run was not repeated after the review fixes (turn 7).

## Use

Update the checkout to `main` first, then open a fresh session and send `/wrap-up` as its first prompt (turns 9, 10).
In the user's next session `/wrap-up` gave "Unknown command": the checkout was still on `feat/98-guard-error-names-fix`, which lacks the skill (turn 10).
