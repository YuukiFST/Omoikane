---
title: opencode-run-exits-before-plugin-event-handlers-finish
type: gotcha
summary: opencode run exits before async plugin event handlers finish; capture must be awaited in dispose
tags: [opencode, plugin, session-capture]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-15-e04462b2.md]
code: [.opencode/plugins/omoikane.ts]
guard: none
---

## Behaviour

[[opencode]] plugin event handlers are fire-and-forget: `opencode run` exits right after the session goes idle, before a handler started on `session.idle` has finished (source: [[session-2026-09-15-e04462b2]], turn 3).
The first live `opencode run` test of the capture plugin wrote nothing to `omoikane/raw/inbox/sessions/` (turns 2, 3).

## Workaround

`.opencode/plugins/omoikane.ts` tracks sessions with pending messages and captures in flight; its `dispose` hook awaits the in-flight captures and captures every session whose idle event never came (turn 3).

Related: `session.idle` and `session.status` with `{type: "idle"}` both exist in SDK 1.18.30 and can announce the same moment, so the plugin coalesces captures requested within a short window (turn 3).

No automated check covers this; only a live `opencode run` shows it.
