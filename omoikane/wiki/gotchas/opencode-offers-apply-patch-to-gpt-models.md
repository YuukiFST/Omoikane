---
title: OpenCode offers apply_patch to gpt models
type: gotcha
summary: OpenCode 1.18 gives gpt- models apply_patch, whose move target no edit rule checks; refuse the run before it starts
tags: [opencode, permissions, headless]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md]
code: [omoikane/bin/headless-scope.py, omoikane/bin/wiki-ingest.ps1, tests/test_headless_scope.py, tests/test_wiki_ingest.py]
guard: test
---

## Behaviour

A reviewer of PR #40 checked `apply_patch` while the redesign went in (source: [[session-2026-09-30-230a182d]], turn 2), and the agent probed an OpenCode agent config with `"tools":{"apply_patch":false}` (turn 2).
From the `headless-scope.py` docstring at merge: OpenCode 1.18 offers `apply_patch` in place of edit and write to a gpt- model whatever the rules say; the permission `apply_patch` maps onto `edit`, and its `*** Move to:` target is never checked against the edit rules, so a wiki page could be moved onto `AGENTS.md`.
The session ran OpenCode 1.18.32 (turn 2).
The next session tested it with the real binary: "Testando empiricamente como o OpenCode expõe `apply_patch` com modelo `gpt-`" (source: [[session-2026-10-01-b5b6fb27]], turn 2).

## Workaround

Before the run, `wiki-ingest.ps1` writes `opencode --pure debug agent <name>` to a file and `headless-scope.py opencode-tools` exits 3 when the agent is offered any tool outside `read, glob, grep, list, edit, write, todowrite`; the run then stops with "pin a model that is not gpt-".
Tests: `test_apply_patch_offered_to_a_gpt_model_is_refused` in `tests/test_headless_scope.py` and `test_an_opencode_agent_offered_apply_patch_never_runs` in `tests/test_wiki_ingest.py`.
See [[opencode]].
