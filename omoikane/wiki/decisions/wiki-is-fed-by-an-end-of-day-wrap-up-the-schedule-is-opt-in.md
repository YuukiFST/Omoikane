---
title: Wiki is fed by an end-of-day wrap-up, the schedule is opt-in
type: decision
summary: The user runs /wrap-up when the day's work ends; the scheduled wiki-ingest.ps1 run is opt-in, never both (#101)
tags: [wrap-up, wiki-ingest, scheduling, autonomy-loop]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-180e52eb.md, wiki/sources/session-2026-10-06-61eabe29.md]
code: [omoikane/prompts/wrap-up.md, docs/architecture.md, README.md, AGENTS.md, omoikane/bin/install-schedule.ps1]
---

## Decision

The default way to feed the wiki is `/wrap-up [days]`, which the user runs in an interactive session when the day's work ends (source: [[session-2026-10-06-180e52eb]], turns 4, 7; issue #101, PR #102, merged as `887725a`).
The scheduled run of `omoikane/bin/wiki-ingest.ps1` stays available as an opt-in. Install it or use `/wrap-up`, not both: the two would distill the same capture (`docs/architecture.md`).
Session capture is unchanged: it runs on every turn, with no window and no LLM (turn 7).
How the pass runs: [[wrap-up]].

## Reason

The user: "Tem um defeito que não gosto no omoikane, [...] é referente a um script powershell que fica abrindo. Talvez isso pudesse ser alterado de outra forma, atraves de uma skill que o proprio usuario utiliza após um dia de trabalho" (turn 3).
The defect is [[scheduled-task-opens-a-powershell-window]].
The commit `29abf08` adds that the task opened the window every 30 minutes "whether or not any work happened", and `docs/architecture.md` adds that the user wants to choose when the wiki is fed.

## Rejected alternatives

- Issue #96, a windowless timer that starts the run through `pythonw.exe` (branch `feat/96-ingest-when-session-quiet`, commit `b695a3b`): closed as "not planned", superseded by #101; the branch was pushed so the work is kept (turn 8).
- Keeping the scheduled run as the default: the agent removed the task `OmoikaneIngest` from this machine, so "O PowerShell não abre mais" (turns 4, 7).

## Consequences

- PR #92, which lets the `wiki/auto` PR merge itself, only has value for a user of the scheduled run; the agent asked the user to decide whether it still makes sense (turn 8). See [[wiki-auto-pr-merges-itself-once-checks-pass]].
  The next session closed #92 and issue #74 unmerged with the user's approval: [[wiki-auto-auto-merge-dropped-with-pr-92]] (source: [[session-2026-10-06-61eabe29]], turns 6, 7).
- The `omoikane-wiki-auto` worktree, where the scheduled run works, stays idle with uncommitted changes and PR #59 open (turn 8).
  The next session discarded that work, which "duplicava o /wrap-up de hoje", merged #59 (`26f6e06`) and removed the worktree and the branch `wiki/auto` (source: [[session-2026-10-06-61eabe29]], turn 7).
- Run `/wrap-up` as the first prompt of a fresh session: the first prompt is not captured, while a later turn of a coding session is (turn 9; `docs/architecture.md`).
