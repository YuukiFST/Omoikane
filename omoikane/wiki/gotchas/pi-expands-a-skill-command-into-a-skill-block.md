---
title: Pi expands a skill command into a skill block
type: gotcha
summary: Pi stores /skill:distill as typed or as a <skill name="distill" location=...> block; capture must skip both forms
tags: [pi, session-capture, skills]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-07-062e80af.md]
code: [omoikane/bin/session-capture.py, tests/test_session_capture.py]
guard: test
---

## Behaviour

Pi runs a skill as `/skill:<name>`. The session file holds the prompt as typed, or as the block Pi expands it into: `<skill name="distill" location="...">` with the skill body, then the argument (commit `6a280c8`).
The agent found the format in Pi's own code, `@earendil-works/pi-coding-agent` 1.0.4, `dist/core/agent-session.js`, and noted "Formato do Pi confirmado (`<skill name="..." location="...">`)" (source: [[session-2026-10-07-062e80af]], turn 6).
Neither form matched `SLASH_COMMAND` or `COMMAND_TEMPLATE` in `omoikane/bin/session-capture.py`.
Once `.pi/settings.json` loads `.claude/skills`, a Pi `/skill:distill` or `/skill:wrap-up` session would be captured and later distilled into itself (commit `6a280c8`).

## Workaround

`PI_SKILL` in `omoikane/bin/session-capture.py` matches both forms at the start of the first prompt, and `command_of` returns the skill as a command, so [[session-capture]] skips the operation.
A block pasted inside prose and a skill that is not an Omoikane operation, such as `/skill:how`, still get captured.
`test_pi_skill_command` in `tests/test_session_capture.py` covers the four cases; it failed before the fix and passed after (turn 6).

The fix was not checked against a session file a real Pi run wrote (`docs/specs/2026-10-07-software-toolkit.md`). See [[pi-coding-agent]].
