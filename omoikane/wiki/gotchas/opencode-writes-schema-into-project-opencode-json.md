---
title: OpenCode writes $schema into project opencode.json
type: gotcha
summary: An OpenCode run adds `$schema` to the project opencode.json; the scope check reads it as an escape and stops the run
tags: [opencode, headless, scope-check]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-230a182d.md]
code: [omoikane/bin/headless-scope.py, omoikane/bin/wiki-ingest.ps1]
guard: none
---

## Behaviour

In the PR #40 probe on OpenCode, step 18 was denied, "mas `verify` acusou `opencode.json` alterado e parou o run" (source: [[session-2026-09-30-230a182d]], turn 2).
`git diff opencode.json` showed the cause: "OpenCode injeta `$schema` no `opencode.json` do projeto; `verify` pegou (prova de que funciona) e nada foi commitado." (turn 2).
The probe clone's `opencode.json` had been written as `{"model": "opencode/big-pickle"}` (turn 2).

## Workaround

Commit `opencode.json` with `"$schema": "https://opencode.ai/config.json"` already present; the probe was rerun that way (source: [[session-2026-09-30-230a182d]], turn 2).
Expect a blocked run (`omoikane/.wiki-ingest.blocked`) in a project whose `opencode.json` lacks it.
See [[opencode]], [[headless-runs-have-no-shell]].
