---
title: Python text-mode stdin writes CRLF on Windows
type: gotcha
summary: On Windows, subprocess text=True writes \n to stdin as \r\n, so git apply --check failed a valid diff; pass bytes
tags: [windows, python, subprocess, git, wiki-lint]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-973284b2.md]
code: [omoikane/bin/wiki-lint.py, tests/test_wiki_lint.py]
guard: test
---

Issue #106 (PR #110) made [[wiki-lint]] pipe each diff in `_review.md` to `git apply --check -`.
On Windows the valid diff of the new test failed the check (source: [[session-2026-10-06-973284b2]], turn 2).
The agent found the cause: "no Windows, `text=True` converte `\n` em `\r\n` no stdin" (turn 2).
In text mode Python translates every `\n` it writes to the pipe into the platform line ending, so the diff's context lines no longer match the file.

Workaround: pass bytes and leave text mode off. `wiki-lint.py` calls `subprocess.run(..., input=diff.encode("utf-8"))`, with a comment giving the reason (turn 2).
Do the same for any multi-line text a script sends to a child process whose output depends on the exact bytes.

Guard: the "valid, new" case of `test_a_diff_that_does_not_apply_is_reported` in `tests/test_wiki_lint.py`.
It fails only on Windows: the CI test job runs on `ubuntu-latest` (`.github/workflows/ci.yml`), so the guard holds only when the suite runs on a Windows machine.
