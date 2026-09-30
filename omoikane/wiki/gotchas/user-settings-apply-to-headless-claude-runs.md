---
title: User settings apply to headless claude runs
type: gotcha
summary: claude -p loads the user's ~/.claude/settings.json rules and hooks, which let git through; load project settings only
tags: [headless, permissions, claude-code, wiki-ingest]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-30-c14af01e.md]
code: [omoikane/bin/wiki-ingest.ps1]
guard: none
---

## Behaviour

A headless `claude` run started by [[wiki-ingest]] still applies the allow rules in the user's `~/.claude/settings.json` and the user's `rtk` hook; together they let `git` run in the headless session despite the repository's allow list (source: [[session-2026-09-30-c14af01e]], turn 2).
The subagent review of item 6 found it and rated it critical (turn 2).

## Workaround

Load project settings only; the fix commit is "fix(ingest): load project settings only and undo ticks the agent adds" (source: [[session-2026-09-30-c14af01e]], turn 2).
The agent checked the flags available in `claude` 2.1.285 with `claude --help` before choosing them (turn 2).
The probe through `wiki-ingest.ps1` afterwards had `git checkout` and `git commit` denied (turn 3).

Part of [[headless-runs-scoped-to-wiki-edits-and-two-scripts]].

## Guard

None today: no test fails when the flag is removed from `wiki-ingest.ps1`. A test is proposed in `omoikane/_review.md`.
