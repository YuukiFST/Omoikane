---
title: opencode
type: entity
summary: OpenCode harness; .opencode/plugins/omoikane.ts wires it to session capture, wiki-ingest can drive it
tags: [opencode, harness]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-15-e04462b2.md]
code: [.opencode/plugins/omoikane.ts, omoikane/bin/wiki-ingest.ps1]
---

OpenCode is a coding agent harness with a plugin system (`@opencode-ai/plugin`, SDK `@opencode-ai/sdk`, both read at 1.18.30) (source: [[session-2026-09-15-e04462b2]], turn 2).

## Omoikane integration

- `.opencode/plugins/omoikane.ts`: `experimental.chat.system.transform` injects the wiki index; `session.idle` and `session.status` idle trigger capture, coalesced; `dispose` captures what is pending (turn 3).
  The plugin fetches the session through the SDK, writes it as the `opencode export` document and runs `session-capture.py --harness opencode` (turn 3).
- `wiki-ingest.ps1 -Agent opencode` runs operations with `opencode run --command <name> <args>` (turn 3).
- [[session-capture]] skips OpenCode subagent sessions, identified by `parentID` (turn 3).

## Gotchas

- [[opencode-run-exits-before-plugin-event-handlers-finish]]
- [[opencode-mixes-path-separators-on-windows]]
