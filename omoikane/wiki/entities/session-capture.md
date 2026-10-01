---
title: session-capture
type: entity
summary: omoikane/bin/session-capture.py, turns a Claude Code, Pi or OpenCode transcript into an inbox session file
tags: [session-capture, module, build-mode]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-15-e04462b2.md, wiki/sources/session-2026-09-30-c14af01e.md]
code: [omoikane/bin/session-capture.py, tests/test_session_capture.py]
---

`omoikane/bin/session-capture.py` writes a coding session into `omoikane/raw/inbox/sessions/` for distill.

## Harnesses

`--harness claude|pi|opencode` selects one transcript reader; all produce the same Session/Turn objects (source: [[session-2026-09-15-e04462b2]], turn 3).

- Claude Code: the JSONL transcript, called from `.claude/settings.json` hooks (turn 2).
- [[pi-coding-agent]]: the session JSONL, a tree; the reader walks from the last entry to the root and drops dead `/tree` branches (turn 3).
- [[opencode]]: the `opencode export` document `{info, messages}`; sessions with a `parentID` (subagents) are skipped (turn 3).

## Skipped operations

Sessions that run an Omoikane operation are not captured; the operation names are read from the files in `omoikane/prompts/`, so a new prompt such as `/synthesize` is skipped without a code change (source: [[session-2026-09-30-c14af01e]], turn 2).

## Naming and continuation

Files are named by the tail of the session id and continuation matches the full id: [[session-file-name-uses-id-tail]].

## Paths

Paths are normalised to `/` before being made relative to the session cwd: [[opencode-mixes-path-separators-on-windows]].
