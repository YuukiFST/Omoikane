---
title: Python text-mode stdin writes CRLF on Windows
type: gotcha
summary: On Windows, subprocess text=True writes \n to stdin as \r\n, so git apply --check failed a valid diff; pass bytes
tags: [windows, python, subprocess, git, wiki-lint]
created: 2026-10-07
updated: 2026-10-09
sources: [wiki/sources/session-2026-10-06-973284b2.md, wiki/sources/session-2026-10-08-261b475d.md]
code: [omoikane/bin/wiki-lint.py, tests/test_wiki_lint.py, omoikane/bin/update-from-template.py, tests/test_new_system.py]
guard: test
---

Issue #106 (PR #110) made [[wiki-lint]] pipe each diff in `_review.md` to `git apply --check -`.
On Windows the valid diff of the new test failed the check (source: [[session-2026-10-06-973284b2]], turn 2).
The agent found the cause: "no Windows, `text=True` converte `\n` em `\r\n` no stdin" (turn 2).
In text mode Python translates every `\n` it writes to the pipe into the platform line ending, so the diff's context lines no longer match the file.

Workaround: pass bytes and leave text mode off. `wiki-lint.py` calls `subprocess.run(..., input=diff.encode("utf-8"))`, with a comment giving the reason (turn 2).
Do the same for any multi-line text a script sends to a child process whose output depends on the exact bytes.

## Second case: update-from-template

The page did not stop the same mistake in `omoikane/bin/update-from-template.py`, whose `git()` sent stdin with `text=True` to `git hash-object --stdin` and `git update-index --index-info` (source: [[session-2026-10-08-261b475d]], turn 2).
There the symptom was not CRLF in the output: git ignored the path `AGENTS.md\r` with exit code 0, see [[git-update-index-index-info-ignores-a-cr-ended-path-and-exits-0]].
Commit `e6b73f5` (issue #135, PR #136) makes that `git()` send bytes too.

## Guard

- The "valid, new" case of `test_a_diff_that_does_not_apply_is_reported` in `tests/test_wiki_lint.py`.
- `test_a_conflict_outside_the_rules_block_keeps_the_system_rules_on_every_side` in `tests/test_new_system.py` (commit `e6b73f5`).

Both fail only on Windows: the CI test job runs on `ubuntu-latest` (`.github/workflows/ci.yml`), so each guard holds only when the suite runs on a Windows machine.
A Windows test job is proposed in `omoikane/_review.md`.
