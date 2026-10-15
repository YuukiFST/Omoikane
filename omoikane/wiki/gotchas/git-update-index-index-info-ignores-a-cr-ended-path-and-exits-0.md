---
title: git update-index --index-info ignores a CR-ended path and exits 0
type: gotcha
summary: Fed "AGENTS.md\r", git update-index --index-info printed "Ignoring path" and exited 0; git's own stages stayed
tags: [git, windows, python, subprocess, template]
created: 2026-10-09
updated: 2026-10-09
sources: [wiki/sources/session-2026-10-08-261b475d.md]
code: [omoikane/bin/update-from-template.py, tests/test_new_system.py]
guard: test
---

## Behaviour

[[update-from-template]] writes its own conflict stages for `AGENTS.md` through `git update-index --index-info`, and the blobs through `git hash-object --stdin`.
Both got their stdin from `git()` in text mode, so on Windows each line ended in `\r\n`: [[python-text-mode-stdin-writes-crlf-on-windows]] (source: [[session-2026-10-08-261b475d]], turn 2).

The user expected CRLF in the paths or blobs, and asked for a test that checks both (turn 2).
That test passed before the fix (turn 2).
The agent's note while it debugged: "os blobs vieram sem `\r`; suspeito que as entradas com CRLF ficaram num path `AGENTS.md\r` que o pathspec não pega" (turn 2).
It reproduced the case in a scratch repository with `printf "100644 $b 2\tAGENTS.md\r\n" | git update-index --index-info; echo "exit=$?"` (turn 2).

The result, in the agent's report: "o `git update-index --index-info` recebe `AGENTS.md\r`, imprime `Ignoring path AGENTS.md` e sai com 0. As stages do script somem e ficam as do próprio git, que são LF." (turn 2).
So the script reported success and the index held git's own merge stages.
The real defect: "as stages 1 e 3 trazem o bloco de regras do template, que é o que `git checkout --theirs` traria" (turn 2).
A human who resolved the conflict with `git checkout --theirs AGENTS.md` got the template's rules block over the system's.

## Workaround

- Send stdin to git as bytes, and decode its output yourself. Commit `e6b73f5` (issue #135, PR #136) makes `git()` in `omoikane/bin/update-from-template.py` pass `stdin.encode("utf-8")` without `text=True`.
- Do not trust exit code 0 from `git update-index --index-info`. Check the stages it wrote.
- Read `git ls-files -z --stage` as bytes in a test. The test comment in `e6b73f5` gives the reason: "on Windows text mode reads a `\r` as a line end and would hide it".
- Test the effect, not the expected symptom. The agent strengthened the test to check that each stage holds the system's rules block; it then failed for that reason and passed after the fix (turn 2).

## Guard

`test_a_conflict_outside_the_rules_block_keeps_the_system_rules_on_every_side` in `tests/test_new_system.py` (commit `e6b73f5`).
It fails only on Windows: the CI test job runs on `ubuntu-latest` (`.github/workflows/ci.yml`).
A Windows test job is proposed in `omoikane/_review.md`.
