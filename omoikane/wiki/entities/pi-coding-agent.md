---
title: pi-coding-agent
type: entity
summary: Pi coding agent harness; .pi/extensions/omoikane.ts wires it to session capture and the wiki index
tags: [pi, harness]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-15-e04462b2.md]
code: [.pi/extensions/omoikane.ts]
---

Pi is a coding agent harness, published as `@earendil-works/pi-coding-agent`: [[pi-coding-agent-package-moved-to-earendil-works]] (source: [[session-2026-09-15-e04462b2]], turn 3).

## Omoikane integration

- `.pi/extensions/omoikane.ts`: `before_agent_start` appends the output of `session-context.py` to the system prompt, computed once per session; `agent_end` and `session_shutdown` run `session-capture.py --harness pi` (turn 3).
- Pi loads `.pi/extensions/*.ts` only once the project is trusted (turn 4).
- Pi only captures sessions; distill runs through `claude` or `opencode`, since there are no `/ingest` `/distill` `/ask` `/lint` commands for Pi (turn 4).
- [[session-capture]] reads Pi's session JSONL as a tree (turn 3).

## Not verified

The extension was never run live: `pi` was not installed on the machine (turn 4).
The check the agent proposed: open `pi` at the repository root, accept project trust, send a prompt that edits a file, look in `omoikane/raw/inbox/sessions/` (turn 4).
