---
title: OpenCode merges user permission maps into the headless scope
type: gotcha
summary: OpenCode merges permission maps key by key, so a user's `git *` allow survives a top-level deny; scope in a fresh agent
tags: [opencode, permissions, headless]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-230a182d.md]
code: [omoikane/bin/headless-scope.py, omoikane/bin/wiki-ingest.ps1, tests/test_headless_scope.py, tests/test_wiki_ingest.py]
guard: test
---

## Behaviour

The agent tested "se allow de nível usuário reabre o escopo OpenCode" with a user-like config `{"permission": {"bash": {"*": "allow", "git *": "allow"}, ...}}` passed through `OPENCODE_CONFIG` (source: [[session-2026-09-30-230a182d]], turn 2).
The test was then rewritten to "emulate OpenCode's order (config rules, then agent rules) with a hostile user config" (turn 2).
From the `headless-scope.py` docstring at merge: OpenCode merges config maps key by key, so the user's `git *` kept its allow after a top-level deny; agent rules come after the top-level ones; a same-named agent in the user's config would merge into ours the same way.
Without any scope, a manual `opencode run` of the probe executed `git commit` and `mv` (turn 2).

## Workaround

Carry the scope in an agent defined through `OPENCODE_CONFIG_CONTENT` under a fresh name per run (`omoikane-headless-<8 hex>`), open every map with `"*": "deny"`, and run `opencode run --pure --agent <name>` (`omoikane/bin/wiki-ingest.ps1`).
With the hostile config the probe through `wiki-ingest.ps1` ran 17 steps exactly in scope with git denied (source: [[session-2026-09-30-230a182d]], turn 2), and later OpenCode resolved the rules with `apply_patch` and bash denied (turn 4).

`tests/test_headless_scope.py` (`OpenCodeResolved`) checks the rules OpenCode itself resolves under a hostile user config.
See [[opencode]], [[headless-runs-have-no-shell]].
