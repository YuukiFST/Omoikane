---
title: pi-coding-agent
type: entity
summary: Pi coding agent harness; .pi/extensions/omoikane.ts wires it to session capture and the wiki index
tags: [pi, harness]
created: 2026-09-30
updated: 2026-10-07
sources: [wiki/sources/session-2026-09-15-e04462b2.md, wiki/sources/session-2026-10-07-062e80af.md]
code: [.pi/extensions/omoikane.ts, .pi/settings.json]
---

Pi is a coding agent harness, published as `@earendil-works/pi-coding-agent`: [[pi-coding-agent-package-moved-to-earendil-works]] (source: [[session-2026-09-15-e04462b2]], turn 3).

## Omoikane integration

- `.pi/extensions/omoikane.ts`: `before_agent_start` appends the output of `session-context.py` to the system prompt, computed once per session; `agent_end` and `session_shutdown` run `session-capture.py --harness pi` (turn 3).
- Pi loads `.pi/extensions/*.ts` only once the project is trusted (turn 4).
- Pi only captures sessions; distill runs through `claude` or `opencode`, since there are no `/ingest` `/distill` `/ask` `/lint` commands for Pi (turn 4).
- [[session-capture]] reads Pi's session JSONL as a tree (turn 3).

## Skills

Since PR #114 (issue #111) `.pi/settings.json` holds `"skills": ["../.claude/skills"]`, so Pi runs the memory skills and the development skills as `/skill:<name>` (source: [[session-2026-10-07-062e80af]], turn 6; `README.md`).
That ends the earlier gap above: Pi now has the memory commands too.
The agent read Pi's skill rules in `docs/skills.md` and `docs/settings.md` of `@earendil-works/pi-coding-agent` 1.0.4, unpacked with `npm pack` (turn 3).
- The settings path resolves from `.pi/`; the first skill found wins a name clash; a description is capped at 1,024 characters (`docs/specs/2026-10-07-software-toolkit.md`).
- Pi has no subagents, so a skill's fan-out steps run one after another (same spec).
- Pi does not read `~/.claude/skills/`, so a personal skill of the same name does not shadow the project's copy (`README.md`).
- Pi expands `/skill:<name>` into a block the capture had to learn: [[pi-expands-a-skill-command-into-a-skill-block]].
- Pi loads a Markdown file placed directly in a skills folder as a skill: [[pi-loads-loose-markdown-in-a-skills-folder-as-a-skill]].

## Not verified

The extension was never run live: `pi` was not installed on the machine (turn 4).
The check the agent proposed: open `pi` at the repository root, accept project trust, send a prompt that edits a file, look in `omoikane/raw/inbox/sessions/` (turn 4).
