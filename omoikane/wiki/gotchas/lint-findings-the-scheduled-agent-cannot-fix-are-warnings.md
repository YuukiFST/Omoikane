---
title: Lint findings the scheduled agent cannot fix are warnings
type: gotcha
summary: A wiki-lint finding goes back to the headless agent; one it may not fix (AGENTS.md) fails the run, so make it a warning
tags: [wiki-lint, headless, scheduled-run, rules]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-10-02-a8b45323.md]
code: [omoikane/bin/wiki-lint.py, tests/test_wiki_lint.py, omoikane/bin/wiki-ingest.ps1]
guard: none
---

PR #86 (issue #76) added a lint check for a promoted rule in `AGENTS.md` that points at a page gone, `Disputed:` or marked `prune:`, first as a finding (source: [[session-2026-10-02-a8b45323]], turn 2).
CI failed: "o novo achado de lint (ponteiro de regra para página ausente) volta para o agente headless, que não pode editar `AGENTS.md`" (turn 2).
Root cause: in a scheduled run `wiki-ingest.ps1` runs lint and sends its findings back to the agent ([[headless-runs-have-no-shell]]), and the agent's scope does not reach `AGENTS.md`, so a finding about it cannot be fixed by the only one who sees it.

Workaround: `rule_pointers` in `omoikane/bin/wiki-lint.py` reports it as a `warning:`, which does not fail; `/lint` reads warnings and only the human edits the rules block (`omoikane/bin/wiki-lint.py`; turn 2).
Before adding a finding to `wiki-lint.py`, check the scheduled agent can fix it inside its scope; if not, it is a warning.

Guard: none names this class; the test covering the check is `RulePointers` in `tests/test_wiki_lint.py`.
See [[wiki-lint]] and [[wiki-rules]].
