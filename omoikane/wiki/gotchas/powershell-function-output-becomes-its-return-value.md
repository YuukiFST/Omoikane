---
title: PowerShell function output becomes its return value
type: gotcha
summary: Anything a PowerShell function writes to the pipeline joins its return value; a Log call made a failed run look ok
tags: [powershell, wiki-ingest]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-230a182d.md]
code: [omoikane/bin/wiki-ingest.ps1, tests/test_wiki_ingest.py]
guard: test
---

## Behaviour

A real `/ingest` eval of the new lint loop in `wiki-ingest.ps1` found that "o `Log` dentro da função polui o valor de retorno (um run com falha pareceria sucesso)" (source: [[session-2026-09-30-230a182d]], turn 4).
`Log` pipes through `Tee-Object`, so its line reaches the pipeline; inside `Invoke-Operation` that line joined the `$ok` it returns, and a non-empty array is truthy.

## Workaround

Send every in-function write to the host: `Log ... | Out-Host`, `... | Tee-Object -FilePath $log -Append | Out-Host` (`omoikane/bin/wiki-ingest.ps1`, comments "Out-Host: anything this function writes to the pipeline becomes part of its return value").
The agent wrote the test first and saw it red (turn 4): `test_an_agent_that_fails_after_a_lint_round_fails_the_operation` in `tests/test_wiki_ingest.py`, which drives the script with a fake `claude`.
See [[wiki-ingest]].
