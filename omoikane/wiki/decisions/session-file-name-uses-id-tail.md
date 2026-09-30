---
title: session-file-name-uses-id-tail
type: decision
summary: Captured session files are named by the last 8 chars of the session id; continuation matches the full id
tags: [session-capture, naming, continuation]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-15-e04462b2.md]
code: [omoikane/bin/session-capture.py]
---

## Decision

[[session-capture]] names a captured file `<day>-<short_id>.md`, where `short_id` is `session_id[-8:]`, the tail of the id (source: [[session-2026-09-15-e04462b2]], turn 3).
Continuation (`ingested_parts`) finds earlier distilled parts by the full `session:` value in their frontmatter, not by file name (turn 3).

## Alternatives rejected

- Head of the id (`session_id[:8]`), the earlier scheme: Pi ids are UUIDv7 and OpenCode ids are time-ordered, so their heads collide for sessions started close together; the tail is random in all three harnesses (turn 3).
- Matching continuation by file name: the `/code-review` pass on PR #10 found that flipping the file-name id from head to tail with name-based matching finds no distilled part of an existing session, so capture re-emits every distilled turn and `wiki-ingest.ps1` distills them again, duplicating pages (turn 3).
  Matching by full id lets the file-name scheme change without losing continuation.
