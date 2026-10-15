---
title: 2026-10-08 Pi assumed working
type: source
summary: The owner's decision of 2026-10-08 to treat Pi support as working without a live check, and fix it on a real fault
tags: [pi, verification, decision]
created: 2026-10-09
updated: 2026-10-09
dated: 2026-10-08
sources: []
code: [.pi/extensions/omoikane.ts, .pi/settings.json]
---

A short note, `omoikane/raw/sources/2026-10-08-pi-assumed-working.md`, written in [[session-2026-10-08-261b475d]] (turn 4) for the next `/wrap-up`.
Its first list item says "Date: 2026-10-08"; commit `4fcf261` added it to `main` on 2026-10-08 (PR #139, "Closes #138"), and `fda7362` extended it the same day.

## Scope

One decision by the owner, taken in an interactive session, with what it proves and what it leaves unchecked.
It lists the wiki lines the decision makes stale and asks the next wrap-up to change them.
It does not say how to check Pi live; [[pi-coding-agent]] holds the check the agent proposed on 2026-09-30.

## Key claims

- The owner will not run the live Pi check now: "eu ja considero que o PI vai estar funcionando, quando eu testar e nao estiver a gente corrige" (note, line 10).
  So the rule: treat Pi support as working, and fix it when a real Pi run shows a fault (note, line 11).
- Proven: capture `af4a4869` of 2026-10-07 shows that the Pi extension captures a session (note, line 15).
- Proven: OpenCode lists and loads `/omoikane-mode`, and Pi lists it; see [[2026-10-07-omoikane-mode-live-check]] (note, line 16).
- Not checked live: `/skill:omoikane-mode` loading in Pi, and the `/skill:` capture fix against a session file a real Pi run wrote; see [[pi-expands-a-skill-command-into-a-skill-block]] (note, line 17).
- Issue #138 removes the todos `pi-live-verification`, `pi-skill-capture-live-check`, `omoikane-mode-live-check` and `narrow-omoikane-mode-live-check` (note, line 21).
  `omoikane/log.md` records the four removals under "[2026-10-08] review | removed from _review.md".
- Criterion 2 of issue #111 now records Pi as assumed working, not verified live (note, line 22).

## What it adds

- The decision itself: [[pi-is-assumed-working-without-a-live-check]].
- First live evidence that the Pi extension captures a session, capture `af4a4869`. The wiki said until now that the extension "was never run live" ([[pi-coding-agent]]).
- The note asks that the source page [[2026-10-07-omoikane-mode-live-check]] stay as it is, since it describes its source as of its date (note, line 30).
