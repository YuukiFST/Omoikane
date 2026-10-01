---
title: Windows path lookup ignores case and trailing dots
type: gotcha
summary: A code path that exists on Windows (wrong case, trailing dot) is missing on Linux CI and to git; lint spells exactly
tags: [wiki-lint, windows, ci, paths]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-230a182d.md]
code: [omoikane/bin/wiki-lint.py, tests/test_wiki_lint.py]
guard: test
---

## Behaviour

Issue #32, "wiki-lint judges code: paths differently on Windows and Linux": a page passed lint locally and failed on the Linux CI (source: [[session-2026-09-30-230a182d]], turn 2).
After the first fix the CI of PR #33 failed again (`gh run view 36735562877 --log-failed`), and the review found the rest: "grafia exata no disco (caso, ponto/espaço final no Windows)" (turn 2).
Windows resolves `SRC/keep.py` and `src/keep.py.` to `src/keep.py`; Linux and git do not (`tests/test_wiki_lint.py`, `test_code_path_is_judged_the_same_on_every_os`).

## Workaround

`wiki-lint.py` checks each path component's exact spelling on disk, normalises `\` and `./`, and reports an absolute path as its own finding (source: [[session-2026-09-30-230a182d]], turn 2).
`AGENTS.md` was updated to "`code:` paths that no longer exist or are absolute" (turn 2).
See [[wiki-lint]].
