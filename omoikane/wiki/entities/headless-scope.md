---
title: headless-scope
type: entity
summary: omoikane/bin/headless-scope.py, the one scope of a scheduled run rendered for Claude and OpenCode, and its tree check
tags: [headless-scope, module, headless, permissions]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md]
code: [omoikane/bin/headless-scope.py, tests/test_headless_scope.py]
---

`omoikane/bin/headless-scope.py` was added in PR #40 for issue #39, "The OpenCode headless run has no permission scope" (source: [[session-2026-09-30-230a182d]], turn 2).
The agent's first plan: "Implementando `headless-scope.py`" once the test was written, after reading the official OpenCode `permission` schema (turn 2).

## Actions

From the module docstring at merge:

- `claude`: the `claude -p` flags, no shell offered; `Read` anchored to the repository since the third review of #40: [[claude-bare-read-rule-reads-outside-the-repository]] (source: [[session-2026-10-01-b5b6fb27]], turn 2).
- `opencode --agent-name NAME`: the `OPENCODE_CONFIG_CONTENT` defining a fresh agent: [[opencode-merges-user-permission-maps-into-the-headless-scope]].
- `opencode-tools --resolved FILE`: exits 3 when OpenCode offers a tool beyond the scope: [[opencode-offers-apply-patch-to-gpt-models]].
- `snapshot` and `verify --before FILE`: compare the tree before and after the run; `verify` exits 3 on a change outside the scope (source: [[session-2026-09-30-230a182d]], turn 4). The snapshot also covers ignored files and the `.git` config and hooks (source: [[session-2026-10-01-b5b6fb27]], turn 2).

`wiki-ingest.ps1` runs a private copy with `python -I`, and the isolated `verify` runs before any repository script (turn 4).
Why there is no shell: [[headless-runs-have-no-shell]]. Driven by [[wiki-ingest]].
