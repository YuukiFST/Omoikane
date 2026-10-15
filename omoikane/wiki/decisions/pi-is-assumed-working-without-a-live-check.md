---
title: Pi is assumed working without a live check
type: decision
summary: Treat Pi support as working without a live check; fix it when a real Pi run shows a fault
tags: [pi, verification, skills, session-capture]
created: 2026-10-09
updated: 2026-10-09
sources: [wiki/sources/2026-10-08-pi-assumed-working.md, wiki/sources/session-2026-10-08-261b475d.md]
code: [.pi/extensions/omoikane.ts, .pi/settings.json]
---

## Chosen

On 2026-10-08 the owner chose to treat Pi support as working, and to fix it when a real Pi run shows a fault (source: [[2026-10-08-pi-assumed-working]]).
The owner's words: "prossiga, eu ja considero que o PI vai estar funcionando, quando eu testar e nao estiver a gente corrige" (source: [[session-2026-10-08-261b475d]], turn 4).

- PR #139 (issue #138) removed the four `_review.md` todos that waited on a live check: `pi-live-verification`, `pi-skill-capture-live-check`, `omoikane-mode-live-check` and `narrow-omoikane-mode-live-check` (source: [[2026-10-08-pi-assumed-working]]).
- Criterion 2 of issue #111 records Pi as assumed working, not verified live (same source).

## Rejected

- Run the live Pi check now, before the toolkit work of issue #111 closes. The owner declined it in turn 3 of [[session-2026-10-08-261b475d]].
  The check the agent proposed: open `pi` at the repository root, accept project trust, send a prompt that edits a file, look in `omoikane/raw/inbox/sessions/` ([[pi-coding-agent]]).

## What is proven and what is not

- Proven: capture `af4a4869` of 2026-10-07 (`harness: pi`) shows that the extension `.pi/extensions/omoikane.ts` captures a session (source: [[2026-10-08-pi-assumed-working]]).
- Proven: Pi lists the omoikane-mode skill command while the user types it ([[2026-10-07-omoikane-mode-live-check]]).
- Not checked live: `/skill:omoikane-mode` loading in Pi ([[omoikane-mode-routes-each-task-to-a-playbook]]).
- Not checked live: the `/skill:` capture fix against a session file a real Pi run wrote ([[pi-expands-a-skill-command-into-a-skill-block]]).

When a Pi run fails, start from these two unchecked points.
