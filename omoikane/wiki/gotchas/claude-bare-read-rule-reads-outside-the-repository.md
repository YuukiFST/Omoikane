---
title: Claude bare Read rule reads outside the repository
type: gotcha
summary: An allowed bare `Read` in claude -p reads ~/.ssh and .env; anchor it as Read(/**) and deny Read(/**/.env*)
tags: [claude-code, permissions, headless]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-10-01-b5b6fb27.md]
code: [omoikane/bin/headless-scope.py, tests/test_headless_scope.py]
guard: test
---

## Behaviour

The headless Claude run allowed `Read` with no path; the agent ran a probe "com as flags atuais do Claude para provar o furo do `Read` (vermelho)" (source: [[session-2026-10-01-b5b6fb27]], turn 2).
With the old flags, 6 of the 9 probe steps passed (turn 2).
From the `claude_args` docstring at merge: "a bare `Read` read `~/.ssh` and `.env`", and Read rules also govern Glob and Grep.

## Workaround

"Variante ancorada funciona: 2-6 negados, `.env` some de Glob/Grep." (source: [[session-2026-10-01-b5b6fb27]], turn 2).
`headless-scope.py claude` allows `Read(/**)`, where a leading `/` anchors at the repository root, and passes `--disallowedTools Read(/**/.env*)`; the deny also drops `.env` files from Glob and Grep results.
The probe run through `wiki-ingest.ps1` then denied `.env` and reads outside the repository and allowed a wiki page and `log.md` (turn 2).
`test_reads_only_the_repository_and_no_env_file` in `tests/test_headless_scope.py` pins the deny.
See [[headless-scope]], [[headless-runs-have-no-shell]].
