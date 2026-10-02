---
title: wiki-lint
type: entity
summary: omoikane/bin/wiki-lint.py, the deterministic check on the page contract that every wiki operation ends with
tags: [wiki-lint, module, page-contract]
created: 2026-09-30
updated: 2026-10-02
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-02-a8b45323.md]
code: [omoikane/bin/wiki-lint.py, omoikane/bin/wikilib.py, tests/test_wiki_lint.py]
---

`omoikane/bin/wiki-lint.py` checks the page contract; shared parsing lives in `omoikane/bin/wikilib.py`.

Phase 2 added three checks (source: [[session-2026-09-30-c14af01e]]):

- `guard:` on gotchas: missing or invalid fails, `guard: none` older than 14 days warns, and `guard:` outside gotchas fails (turns 2, 3). See [[gotcha-guard-field-records-the-existing-check]].
- The `practice` type with a two-session floor; after review only session pages that exist count toward it (turn 2).
- The `prune:` mark in the page contract (turn 2).

`code:` paths are judged the same on Windows and Linux and an absolute one is a finding, since PR #33: [[windows-path-lookup-ignores-case-and-trailing-dots]] (source: [[session-2026-09-30-230a182d]], turn 2).
In the scheduled run the agent no longer runs lint; `wiki-ingest.ps1` runs it and hands the findings back: [[headless-runs-have-no-shell]] (turn 4).

The `domain` page type (issue #64, PR #71) fails a domain page that cites no existing source page (source: [[session-2026-10-02-1b324082]], turn 3).
The first version accepted any existing page as the statement behind the rule, the page itself or a concept included; the subagent review rated it high, and the fix, red test first, accepts only a source page (turn 3).

`rule_pointers` (PR #86) warns about a promoted rule in `AGENTS.md` whose page is gone, `Disputed:` or marked `prune:`. It began as a finding and failed CI, because the scheduled agent cannot edit `AGENTS.md`: [[lint-findings-the-scheduled-agent-cannot-fix-are-warnings]] (source: [[session-2026-10-02-a8b45323]], turn 2).
