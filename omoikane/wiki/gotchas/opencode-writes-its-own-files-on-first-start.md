---
title: OpenCode writes its own files on first start
type: gotcha
summary: OpenCode's first start writes .opencode/.gitignore and, without --pure, plugin deps; start it before the snapshot
tags: [opencode, headless, scope-check]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-10-01-b5b6fb27.md]
code: [omoikane/bin/wiki-ingest.ps1, tests/test_wiki_ingest.py]
guard: test
---

## Behaviour

The fourth review of PR #40 raised "install do `.opencode` dentro da janela": OpenCode writes under `.opencode/` while the run is being watched, so the scope check reads the write as the agent's (source: [[session-2026-10-01-b5b6fb27]], turn 2).
The agent checked it with the real binary, deleting `.opencode/.gitignore` and running `opencode --pure debug config`, then listing `.opencode` (turn 2).
From the `wiki-ingest.ps1` comment at merge: OpenCode writes `.opencode/` (its `.gitignore`; plugin deps without `--pure`) on start, and the first run in a fresh clone would block.

The test fake got this wrong first: "Fake reescrevia o `.gitignore` toda vez; real só cria se falta." (turn 2).

## Workaround

`wiki-ingest.ps1 -Agent opencode` runs `opencode --pure debug config` once before the first snapshot.
"Real: fresh clone com warm-up, verify=0." (source: [[session-2026-10-01-b5b6fb27]], turn 2).
`test_the_opencode_run_carries_the_scope_in_a_fresh_agent_and_restores_the_user_config` in `tests/test_wiki_ingest.py` starts from a fresh clone; its fake writes `.opencode/.gitignore` only when missing.
Same class as [[opencode-writes-schema-into-project-opencode-json]]. See [[opencode]].
