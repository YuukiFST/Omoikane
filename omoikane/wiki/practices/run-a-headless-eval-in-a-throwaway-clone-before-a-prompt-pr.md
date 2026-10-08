---
title: Run a headless eval in a throwaway clone before a prompt PR
type: practice
summary: Before opening or merging a PR that changes an Omoikane prompt, run the operation for real in a $TEMP clone
tags: [procedure, eval, prompts, headless, pull-request]
created: 2026-10-02
updated: 2026-10-07
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-02-a8b45323.md, wiki/sources/session-2026-10-02-a9384e33.md, wiki/sources/session-2026-10-05-1de79b19.md, wiki/sources/session-2026-10-06-180e52eb.md]
---

## Rule

When a PR changes an Omoikane prompt or how `wiki-ingest.ps1` runs one, clone the branch into `$TEMP`, run the operation headless there, and check its pages, log and commit before the PR merges.
Run the same input on a clone of `main` too, and compare the two runs.
Never run the eval in the working checkout.

## Evidence

- Phase 2: each item ran an eval in a clone such as `$eval = Join-Path $env:TEMP "omoikane-eval-19"; ... git clone -q -b feat/19-distill-routing . $eval`; the `/distill` eval gave 7 pages, 1 guard and 4 todos, and `/synthesize` was re-run "com prompt revisado no mesmo clone para checar dedup" (source: [[session-2026-09-30-c14af01e]], turn 2).
- PR #40: "Eval real: `/ingest` de uma nota curta num clone, pelo `wiki-ingest.ps1 -Commit` novo (Claude), para ver o agente sem shell e o laço de lint", which found two bugs in the lint loop (source: [[session-2026-09-30-230a182d]], turn 4).
- PR #40 after the prompts were told to skip index and lint: "Eval do prompt num clone: o agente não tentou rodar index nem lint, e o commit saiu limpo." (source: [[session-2026-10-01-b5b6fb27]], turn 2).
- PR #72, the domain routing in `distill.md` and `ingest.md`: "Clone de eval pronto. Rodando o `wiki-ingest.ps1` headless sobre a fixture", run as `wiki-ingest.ps1 -Agent claude -QuietMinutes 0` with `OMOIKANE_NO_CAPTURE=1`; "Eval passou: duas páginas `domain` e a instrução `task-only` registrada como skipped" (source: [[session-2026-10-02-1b324082]], turns 3, 6).
- PR #72 again, the second eval over both fixtures: "Eval do #72 passou em todos os 5 critérios. Postando resultado no PR e mergeando."; PR #86, `/synthesize` in a clone, run twice, the second time with the prompts the review changed: "Eval do #86 (prompts novos) OK" (source: [[session-2026-10-02-a8b45323]], turn 2).
- PRs #94 and #95: `run-eval.sh main ... term-before`, then `run-eval.sh feat/90-domain-term-tag ... term-after`, in `$TEMP/omoikane-evals`; before, the run made up tags, after, the page had the `term` tag (source: [[session-2026-10-02-a9384e33]], turns 2, 3).
- PRs #99 and #100: "Rodando eval antes/depois em paralelo." The clones `/tmp/omoikane-eval-correct-before` and `-after` ran `OMOIKANE_NO_CAPTURE=1 pwsh -NoProfile -File omoikane/bin/wiki-ingest.ps1 -QuietMinutes 0 -SynthesizeEvery 0`. The "before" run showed `main` already did one planned change, so the agent dropped it: "Removendo parágrafo de escalação (redundante, eval provou)" (source: [[session-2026-10-05-1de79b19]], turn 1).
- PR #102, the new `/wrap-up` prompt: "suíte e E2E do `/wrap-up` rodando num clone descartável, sem `origin`"; the run wrote 16 pages with lint clean and found a bug the tests did not, [[git-log-since-a-bare-date-starts-at-the-current-time-of-day]]. After the review fixes the run was not repeated: "Ficou validado só pelo CI e pelos testes." (source: [[session-2026-10-06-180e52eb]], turns 4, 6, 7).

## Scope

The eval checks the prompt's behaviour on a real run; it does not replace the unit tests, which every session above also ran.
One run on each side is "a direction, not a measurement" (PR #99 body; source: [[session-2026-10-05-1de79b19]]). A run that fails on an API error, such as 529, is run again, not counted (turn 1).
When the machine is short of memory, a killed eval is reported as not run, not as passed: the second eval of PR #72 was killed and filed as a todo (source: [[session-2026-10-02-1b324082]], turn 5).
