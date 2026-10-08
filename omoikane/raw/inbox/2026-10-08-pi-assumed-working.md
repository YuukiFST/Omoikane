# Pi is assumed to work without a live check

- Date: 2026-10-08.
- Decided by: the owner, in an interactive session.
- Issue: #138.

## Decision

The owner will not run the live Pi check now.
The owner's words: "eu ja considero que o PI vai estar funcionando, quando eu testar e nao estiver a gente corrige".
Treat Pi support as working; fix it when a real Pi run shows a fault.

## What is proven and what is not

- Proven: capture `af4a4869` of 2026-10-07 shows that the Pi extension captures a session.
- Proven: OpenCode lists and loads `/omoikane-mode`, and Pi lists it (source: the 2026-10-07 omoikane-mode live check).
- Not checked live: `/skill:omoikane-mode` loading in Pi, and the `/skill:` capture fix against a session file a real Pi run wrote (see the gotcha `pi-expands-a-skill-command-into-a-skill-block`).

## Effect

- #138 removes the todos `pi-live-verification`, `pi-skill-capture-live-check`, `omoikane-mode-live-check` and `narrow-omoikane-mode-live-check`.
- Criterion 2 of issue #111 now records Pi as assumed working, not verified live.
