---
title: Run a headless eval in a throwaway clone before a prompt PR
type: practice
summary: Before opening or merging a PR that changes an Omoikane prompt, run the operation for real in a $TEMP clone
tags: [procedure, eval, prompts, headless, pull-request]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-02-1b324082.md]
---

## Rule

When a PR changes an Omoikane prompt or how `wiki-ingest.ps1` runs one, clone the branch into `$TEMP`, run the operation headless there, and check its pages, log and commit before the PR merges.
Never run the eval in the working checkout.

## Evidence

- Phase 2: each item ran an eval in a clone such as `$eval = Join-Path $env:TEMP "omoikane-eval-19"; ... git clone -q -b feat/19-distill-routing . $eval`; the `/distill` eval gave 7 pages, 1 guard and 4 todos, and `/synthesize` was re-run "com prompt revisado no mesmo clone para checar dedup" (source: [[session-2026-09-30-c14af01e]], turn 2).
- PR #40: "Eval real: `/ingest` de uma nota curta num clone, pelo `wiki-ingest.ps1 -Commit` novo (Claude), para ver o agente sem shell e o laço de lint", which found two bugs in the lint loop (source: [[session-2026-09-30-230a182d]], turn 4).
- PR #40 after the prompts were told to skip index and lint: "Eval do prompt num clone: o agente não tentou rodar index nem lint, e o commit saiu limpo." (source: [[session-2026-10-01-b5b6fb27]], turn 2).
- PR #72, the domain routing in `distill.md` and `ingest.md`: "Clone de eval pronto. Rodando o `wiki-ingest.ps1` headless sobre a fixture", run as `wiki-ingest.ps1 -Agent claude -QuietMinutes 0` with `OMOIKANE_NO_CAPTURE=1`; "Eval passou: duas páginas `domain` e a instrução `task-only` registrada como skipped" (source: [[session-2026-10-02-1b324082]], turns 3, 6).

## Scope

The eval checks the prompt's behaviour on a real run; it does not replace the unit tests, which every session above also ran.
When the machine is short of memory, a killed eval is reported as not run, not as passed: the second eval of PR #72 was killed and filed as a todo (source: [[session-2026-10-02-1b324082]], turn 5).
