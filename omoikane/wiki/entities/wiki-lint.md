---
title: wiki-lint
type: entity
summary: omoikane/bin/wiki-lint.py, the deterministic check on the page contract that every wiki operation ends with
tags: [wiki-lint, module, page-contract]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-30-c14af01e.md]
code: [omoikane/bin/wiki-lint.py, omoikane/bin/wikilib.py, tests/test_wiki_lint.py]
---

`omoikane/bin/wiki-lint.py` checks the page contract; shared parsing lives in `omoikane/bin/wikilib.py`.

Phase 2 added three checks (source: [[session-2026-09-30-c14af01e]]):

- `guard:` on gotchas: missing or invalid fails, `guard: none` older than 14 days warns, and `guard:` outside gotchas fails (turns 2, 3). See [[gotcha-guard-field-records-the-existing-check]].
- The `practice` type with a two-session floor; after review only session pages that exist count toward it (turn 2).
- The `prune:` mark in the page contract (turn 2).
