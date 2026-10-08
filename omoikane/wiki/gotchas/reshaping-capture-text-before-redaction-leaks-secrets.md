---
title: Reshaping capture text before redaction leaks secrets
type: gotcha
summary: Join or wrap capture lines only after redaction; a joined private key and a wrapped `password =` leaked their secrets
tags: [redaction, session-capture, secrets]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-973284b2.md]
code: [omoikane/bin/session-capture.py, tests/test_session_capture.py]
guard: test
---

The secret patterns of `redact_secrets` read the text's line structure, so a change to the line breaks before redaction can hide a secret from them. [[session-2026-10-06-973284b2]] met it twice.

## Joining lines

The first version of the capture error record (issue #103, PR #107) flattened the whitespace of the error message before it redacted it.
The subagent review of #107 found the leak: "achatar espaços antes de redigir vaza chave privada" (source: [[session-2026-10-06-973284b2]], turn 2).
The private key patterns read line breaks, so a key with its lines joined was not matched (commit `fff42de`).
Fix: redact the message, then join its lines.
Guard: `test_a_secret_in_the_error_message_is_redacted_before_its_lines_are_joined` in `tests/test_session_capture.py`.

## Wrapping lines

PR #109 wraps capture lines longer than `LINE_CHARS` (1900) for OpenCode: [[opencode-read-tool-cuts-lines-at-2000-characters]].
The agent moved the wrap after redaction: "quebrar antes poderia separar `password:` do valor e vazar o segredo" (source: [[session-2026-10-06-973284b2]], turn 2).
`capture()` now calls `wrap_long_lines` on the redacted text; a code comment there gives the reason.
No test fails when the order is reversed, so `guard: test` covers the joining case only. A proposed test is in `omoikane/_review.md`, guard `wrapped-line-splits-a-name-from-its-secret`.

## Workaround

Run every reshaping step (join, wrap, flatten) on text that is already redacted.
A new secret shape gets a case in the `Redaction` tables, as [[secret-redaction-patterns-leak-swallow-and-backtrack]] says.
See [[session-capture]].
