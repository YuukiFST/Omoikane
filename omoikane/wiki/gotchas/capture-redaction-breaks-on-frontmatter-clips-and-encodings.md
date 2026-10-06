---
title: Capture redaction breaks on frontmatter, clips and encodings
type: gotcha
summary: Redacting a capture must spare the frontmatter ids, catch terms cut by clip(), and read BOM and UTF-16 term lists
tags: [redaction, session-capture, encoding]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-10-02-1b324082.md]
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
