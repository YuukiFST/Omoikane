---
title: pi-coding-agent-package-moved-to-earendil-works
type: gotcha
summary: Pi package @mariozechner/pi-coding-agent is deprecated; extensions import @earendil-works/pi-coding-agent
tags: [pi, npm, dependencies]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-15-e04462b2.md]
code: [.pi/extensions/omoikane.ts]
guard: none
---

## Behaviour

Issue #7 and the pi-mono link name the package `@mariozechner/pi-coding-agent` (source: [[session-2026-09-15-e04462b2]], turn 2).
That package is deprecated and the repository moved to `earendil-works/pi` (turn 3).
The session packed `@mariozechner/pi-coding-agent` 0.73.1 first, then `@earendil-works/pi-coding-agent` 0.85.1, whose `dist/` layout differs: paths such as `core/extensions/types.d.ts` taken from the old package were not found in the new one (turn 2).

## Workaround

`.pi/extensions/omoikane.ts` imports `ExtensionAPI` and `ExtensionContext` from `@earendil-works/pi-coding-agent` (turn 3).
Read the [[pi-coding-agent]] docs and types from the `@earendil-works` package, not the one the issue links.
