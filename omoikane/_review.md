# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

A bullet with a checkbox is a proposal: a guard or a prompt change, with its diff below it. Tick `[x]` to approve; an interactive session applies ticked proposals and deletes their bullets, and a scheduled run never does. Delete an unticked bullet to reject it.

## [2026-09-30] distill | session e04462b2

- todo pi-omoikane-commands: add `/ingest`, `/distill`, `/ask`, `/lint` commands for Pi; today Pi only captures and distill runs through `claude` or `opencode` (session e04462b2, turn 4)
- todo unify-transcript-readers: merge the Claude, Pi and OpenCode readers in `session-capture.py` into one state machine (session e04462b2, turn 4)
- todo pi-live-verification: run the Pi extension live once: `pi` at the repo root, accept project trust, prompt an edit, check `omoikane/raw/inbox/sessions/` (session e04462b2, turn 4)
