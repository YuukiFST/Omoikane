---
title: OpenCode read tool cuts lines at 2000 characters
type: gotcha
summary: OpenCode's read tool cuts each line at 2,000 characters, so session-capture wraps lines at LINE_CHARS (1900)
tags: [opencode, session-capture, distill]
created: 2026-10-07
updated: 2026-10-08
sources: [wiki/sources/session-2026-10-06-973284b2.md]
code: [omoikane/bin/session-capture.py, tests/test_session_capture.py]
guard: test
---

Issue #104 (PR #109) raised the capture's prompt limit to 20,000 characters, so that a rule at the end of a long prompt reaches [[session-capture]] (source: [[session-2026-10-06-973284b2]], turn 2).
The subagent review of #109 found that this was not enough: "o OpenCode corta cada linha em 2.000 caracteres" (turn 3).
A long one-paragraph prompt is one line, so `/distill` run in [[opencode]] would still lose its end (commit `b76c817`).

Fix: `wrap_long_lines` breaks each line longer than `LINE_CHARS = 1900` at its last space before the limit (`omoikane/bin/session-capture.py`, commit `b76c817`).
It runs after redaction: [[reshaping-capture-text-before-redaction-leaks-secrets]].
A run with no space stays whole (`wrap_long_lines` docstring).

Guard: `test_a_rule_at_the_end_of_a_long_prompt_reaches_the_capture` in `tests/test_session_capture.py` checks that no capture line is longer than 2,000 characters, for a prompt in lines and in one paragraph.
