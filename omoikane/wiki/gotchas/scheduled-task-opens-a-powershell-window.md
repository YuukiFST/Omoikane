---
title: Scheduled task opens a PowerShell window
type: gotcha
summary: OmoikaneIngest runs pwsh.exe in the user's interactive session, so each run opens a window; pythonw.exe has no console
tags: [task-scheduler, windows, powershell, wiki-ingest]
created: 2026-10-06
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-02-a9384e33.md, wiki/sources/session-2026-10-06-180e52eb.md]
code: [omoikane/bin/install-schedule.ps1]
guard: none
---

## Behaviour

The user: "Fica abrindo um script powershell do Omoikane no meu PC, por que ?" (source: [[session-2026-10-02-a9384e33]], turn 8).
It was the task `OmoikaneIngest` that `omoikane/bin/install-schedule.ps1` registers: `pwsh.exe -NoProfile -File ...\wiki-ingest.ps1 -Agent claude -Commit` every 30 minutes (turn 8).
The task runs in the user's session (`LogonType: Interactive`) and is not marked hidden, and `install-schedule.ps1` starts `pwsh.exe` without `-WindowStyle Hidden`, so every run shows a console window (turn 8).

## Options the session weighed

- `-WindowStyle Hidden` in the task arguments: one line; the agent noted the window still flashes for a moment before it hides (turn 8, not tested).
- "Run whether user is logged on or not" (S4U): no window, but the agent expected it to break the run, since the `gh` and `claude` logins live in the user's session; not tested (turn 8).
- Start the run through `pythonw.exe`, which has no console (turn 10). On branch `feat/96-ingest-when-session-quiet` the task runs `pythonw.exe` with `ingest-timer.py`; the end-to-end run in a throwaway clone showed the waiter alive with `MainWindowHandle 0` and `wiki-ingest` started with no window (turn 10).
- Stop the task: `Disable-ScheduledTask -TaskName OmoikaneIngest`; the wiki is then not fed until it is turned on again (turn 8).

## Status

`main` still registers `pwsh.exe` every 30 minutes with a window (`install-schedule.ps1`).
Issue #96 (the windowless timer) was closed as not planned on 2026-10-06, superseded by #101: `/wrap-up` feeds the wiki by default and the scheduled run is opt-in; `docs/architecture.md` gives this window as one reason. The `pythonw.exe` work stays on branch `feat/96-ingest-when-session-quiet`, pushed before the close (source: [[session-2026-10-06-180e52eb]], turn 8). See [[wiki-is-fed-by-an-end-of-day-wrap-up-the-schedule-is-opt-in]].
That session removed the task from the user's machine with `install-schedule.ps1 -Remove`: "O PowerShell não abre mais." (turns 4, 7).
A task registered by an older `install-schedule.ps1` keeps its old action until the script runs again (turn 10).
