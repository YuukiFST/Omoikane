---
title: Headless runs have no shell
type: decision
summary: The scheduled agent gets no shell at all; wiki-ingest.ps1 runs index and lint and hands the findings back
tags: [headless, permissions, wiki-ingest, security, opencode]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-230a182d.md]
code: [omoikane/bin/headless-scope.py, omoikane/bin/wiki-ingest.ps1, tests/test_headless_scope.py, tests/test_wiki_ingest.py, AGENTS.md]
---

The agent that [[wiki-ingest]] starts may read the repository and edit wiki pages (`.md`), `omoikane/log.md` and `omoikane/_review.md`; it runs no command (source: [[session-2026-09-30-230a182d]], turns 2, 4).
`wiki-ingest.ps1` runs `wiki-lint.py` after the agent and hands the findings back for up to 2 rounds, then runs index and lint itself (turn 4).
`AGENTS.md` tells a scheduled run it has no shell and to skip index and lint (turn 4).

## Why

- The two exactly allowed scripts did not work: the headless agent appended `echo "lint exit $?"` to the index and lint commands and was denied, counted at 2 of 3 runs, then 3 of 4, then 4 of 5 (source: [[session-2026-09-30-230a182d]], turn 2). "O headless passou a rodar sem nenhum shell, o que também resolve os 4 de 5 runs" (turn 4).
- From the `headless-scope.py` docstring at merge, not the capture: an allowed script is code the agent can replace or shadow from a directory it writes to.
- One scope renders both harnesses, because the OpenCode run had none at all (issue #39) (turn 2). See [[headless-scope]].

## Details

- After every agent call a private copy of `headless-scope.py`, run with `python -I`, compares a snapshot of the tree with the one taken before; a change outside the scope writes `omoikane/.wiki-ingest.blocked` and every later run refuses (turn 4).
- `verify` exits 3 on a finding, not 1, so a crash cannot read as a verdict (turn 4); before the fix a crash failed open (code comment in `wiki-ingest.ps1`).
- The isolated `verify` runs before any repository script, because `review-ticks.py` imports from `omoikane/bin/` (turn 4).
- Only lint findings go back, not `warning:` lines: the first eval handed back 26 instead of 1 (turn 4).

## History

Reverses [[headless-runs-scoped-to-wiki-edits-and-two-scripts]], which allowed `wiki-index.py` and `wiki-lint.py` by exact name (source: [[session-2026-09-30-230a182d]], turn 2).
