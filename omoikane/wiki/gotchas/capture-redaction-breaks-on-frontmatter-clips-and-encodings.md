---
title: Capture redaction breaks on frontmatter, clips and encodings
type: gotcha
summary: Redaction must spare frontmatter ids, catch clipped terms, read BOM and UTF-16 lists; an ANSI list still fails
tags: [redaction, session-capture, encoding]
created: 2026-10-02
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-06-973284b2.md]
code: [omoikane/bin/session-capture.py, tests/test_session_capture.py]
guard: test
---

The first version of [[redact-captures-when-they-are-written]] passed its own tests; the subagent review of PR #69 found real defects (source: [[session-2026-10-02-1b324082]], turn 3):

- A term list saved with a BOM or as UTF-16 (rated high and medium) was not read as written (turn 3).
- Redaction ran over the frontmatter too; fixed so `harness`, `session`, `part`, `turns`, `started` and `ended` are never redacted (turn 3). The code says why: `ingested_parts()` matches distilled parts by `session:` and reads `turns:`, so a redacted id re-captured a distilled session as a new part and a redacted count crashed every later turn (`redact_capture` in `omoikane/bin/session-capture.py`).
- The readers clip long text before redaction runs, so a term cut by the `[... N chars cut]` marker left its start in the capture (turn 3).
- The agent also wrote cases for a term in the session id, path separators and line breaks inside a term (turn 3).

Fix: commit "fix(capture): redact whatever spelling and encoding the terms come in" (0780d8b), seven cases red before the fix (turn 3).
Guard: the redaction tests in `tests/test_session_capture.py`, such as `test_the_list_is_read_whatever_editor_wrote_it`, `test_frontmatter_ids_survive_so_continuation_still_matches` and `test_a_term_cut_by_a_clip_leaves_no_prefix`.
The limits left were added to `docs/architecture.md` (turn 3).

## ANSI code page

A list in the ANSI code page is still not read. The subagent review of PR #107 found that "um `.capture-redact` em ANSI quebrava a captura e também o registro do erro, então nada chegava ao brief" (source: [[session-2026-10-06-973284b2]], turn 3).
The test names the writer: PowerShell 5.1 `Set-Content` writes the list in the ANSI code page (`CaptureFailure` in `tests/test_session_capture.py`).
Since `fff42de` the capture still fails, but the failure reaches `omoikane/.capture-errors` with the message withheld, since it may hold a listed term: "[message withheld: omoikane/.capture-redact unreadable (UnicodeDecodeError)]".
Workaround: save the list as UTF-8, with or without a BOM, or UTF-16. Guard: the "unreadable list" case of `test_a_failed_capture_is_named_in_the_next_brief`.
