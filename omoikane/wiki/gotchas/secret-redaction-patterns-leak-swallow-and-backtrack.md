---
title: Secret redaction patterns leak, swallow and backtrack
type: gotcha
summary: Secret regexes in session-capture leaked quoted keys, erased turns after an unterminated PEM and took 85 s to backtrack
tags: [redaction, session-capture, regex, secrets]
created: 2026-10-02
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-02-a8b45323.md, wiki/sources/session-2026-10-06-973284b2.md]
code: [omoikane/bin/session-capture.py, tests/test_session_capture.py]
guard: test
---

`redact_secrets` in `omoikane/bin/session-capture.py` (issue #77, PR #82) replaces API keys, tokens, private keys and passwords in a capture with `[redacted]`, before the listed terms of [[redact-captures-when-they-are-written]].
Its first version passed its own tests; three subagent review rounds each found real leaks or overreach (source: [[session-2026-10-02-a8b45323]], turn 2).

Round 1, "problemas sérios" (turn 2):

- A JSON key in quotes leaked its value, as in `{"password": "hunter22"}`.
- A PEM header with no END line ran to the end of the capture and erased the turns after it.
- Backtracking: "A hyphenated run of keywords took 85 s on 8,000 characters, inside the Stop hook" (`tests/test_session_capture.py`).

The agent rewrote the pattern block and `redact_secrets` with the failing tests first, then checked the repository's real captures for false positives (turn 2).

Round 3: PGP armor leaked (its `Version:` header and blank line), a name followed by a space swallowed the next assignment, and a literal `:=` was not handled; the callback moved to named groups (turn 2).
After that round the real captures showed no change and no slowdown (turn 2).

Issue #104 let a prompt line hold 20,000 characters. The subagent review of PR #109 found that the `curl -u` and `mysql -p` patterns scanned to the end of the line: on such a line of repeated commands they took over 1 s a turn (source: [[session-2026-10-06-973284b2]], turns 2, 3).
Commit `b76c817` bounds both scans; `test_long_names_and_values_redact_in_linear_time` now also times them on 20,000-character lines (under 1 s).
Redaction must also run before any step that joins or wraps lines: [[reshaping-capture-text-before-redaction-leaks-secrets]].

Workaround, for any new secret shape: add it as a case to the tables in `Redaction`, prove it red, and keep the three guards green:

- `test_secrets_never_reach_the_capture_without_a_list`: shapes that must go, grouped by the review round that found them.
- `test_code_that_only_names_a_secret_is_kept`: code that only names a secret (`os.environ["API_TOKEN"]`, `${{ secrets.GITHUB_TOKEN }}`) stays, or distill loses the code the session talks about.
- `test_a_secret_header_without_its_end_takes_nothing_after_it` and `test_long_names_and_values_redact_in_linear_time` (under 2 s).

See [[session-capture]].
