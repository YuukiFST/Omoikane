---
title: Headless runs scoped to wiki edits and two scripts
type: decision
summary: wiki-ingest.ps1 runs claude in dontAsk: only wiki edits, index and lint; git denied, the script moves files
tags: [headless, permissions, wiki-ingest, security]
created: 2026-09-30
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md]
code: [omoikane/bin/wiki-ingest.ps1, omoikane/bin/review-ticks.py]
---

The scheduled run in [[wiki-ingest]] runs `claude` with `--permission-mode dontAsk` and an exact scope instead of the earlier allow list (source: [[session-2026-09-30-c14af01e]], turn 2).

## Before

The allow list was `Read,Write,Edit,Glob,Grep,Bash(python omoikane/bin/*),Bash(git mv *),PowerShell(python omoikane/bin/*),PowerShell(git mv *)` (source: [[session-2026-09-30-c14af01e]], turn 2).
A probe with those flags was run first "para provar a brecha" (turn 2).

## Choice

- `dontAsk` plus exact rules; the commit is "fix(ingest): scope headless permissions to the wiki and two named scripts" (source: [[session-2026-09-30-c14af01e]], turn 2).
- `git mv` is no longer allowed: the prompts leave the move to `wiki-ingest.ps1` when it is denied, and the script moves the file after the run (turns 2, 3).
- Only project settings are loaded, because user-level rules and hooks reopened `git`: [[user-settings-apply-to-headless-claude-runs]] (turn 2).
- Any `[x]` the agent adds to `_review.md` is undone after the run with `review-ticks.py`, since the tick is the human's approval (turns 2, 3).

## Alternatives rejected

Added in the review of PR #36; the reasons are the comments in `omoikane/bin/wiki-ingest.ps1` at that commit, not the capture.

- `--permission-mode acceptEdits`: also auto-approves `rm`, `mv`, `cp` and `sed` anywhere in the repository.
- `Bash(python omoikane/bin/*)`: would run a script the agent wrote into `omoikane/bin/`, or one reached through `..`; the two scripts are named exactly.
- `Bash(git mv *)`: the file move is left to `wiki-ingest.ps1`, after the run.
- Loading user settings: user-level allow rules and hooks reopen `git`, see [[user-settings-apply-to-headless-claude-runs]].

## Evidence

- Probe on the new flags: steps 1 to 5, 9 and 10 denied; 6 to 8 (wiki, lint, log) allowed, "Exatamente o escopo pretendido" (source: [[session-2026-09-30-c14af01e]], turn 2).
- Probe through `wiki-ingest.ps1` itself, with the `ingest` skill swapped for the probe: everything denied, including `git checkout`, `git commit` and a write outside the repository; the agent's tick was undone (turn 3).
- A real `/distill` with the new flags: 8 pages, lint clean, file moved by the script (turn 3).

## History

Reversed by [[headless-runs-have-no-shell]]: the agent kept appending `echo "lint exit $?"` to the two allowed scripts and was denied, so the run now has no shell (source: [[session-2026-09-30-230a182d]], turn 2).
