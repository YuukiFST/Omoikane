---
title: wiki-ingest
type: entity
summary: omoikane/bin/wiki-ingest.ps1, the scheduled run: one headless agent call per inbox file, then /synthesize on cadence
tags: [wiki-ingest, module, headless, autonomy-loop]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-15-e04462b2.md, wiki/sources/session-2026-09-30-c14af01e.md]
code: [omoikane/bin/wiki-ingest.ps1, omoikane/bin/synthesize-due.py, omoikane/bin/review-ticks.py]
---

`omoikane/bin/wiki-ingest.ps1` runs `/ingest` on plain sources and `/distill` on captured sessions, one headless agent call per file.

## Agents

`-Agent opencode` runs `opencode run --command distill <file>` (source: [[session-2026-09-15-e04462b2]], turn 3); see [[opencode]].

## Permissions

The `claude` call is scoped to wiki edits and two scripts: [[headless-runs-scoped-to-wiki-edits-and-two-scripts]] (source: [[session-2026-09-30-c14af01e]], turn 2).
It loads project settings only: [[user-settings-apply-to-headless-claude-runs]] (turn 2).
The headless agent may not move files; the script moves the source after the run (turn 3).

## Cross-session pass

After a number of distills since the last pass, the script runs `/synthesize` once; `synthesize-due.py` decides (source: [[session-2026-09-30-c14af01e]], turn 2).
When the run writes no log entry, the script appends the heading itself so the next run does not trigger again; the agent tested this with a fake `claude` that writes no log, and a second run did not fire (turn 2).
