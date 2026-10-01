---
title: wiki-rules
type: entity
summary: omoikane/bin/wiki-rules.py promotes ticked rule proposals into AGENTS.md; context-budget.py caps what sessions load
tags: [wiki-rules, context-budget, module, rules]
created: 2026-09-30
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md]
code: [omoikane/bin/wiki-rules.py, omoikane/bin/context-budget.py, tests/test_wiki_rules.py]
---

`/synthesize` proposes `- [ ] rule` bullets in `_review.md`; after the human ticks one, `python omoikane/bin/wiki-rules.py` writes it into the managed rules block of `AGENTS.md` (source: [[session-2026-09-30-c14af01e]], turn 2).
In the eval, promotion worked and was idempotent (turn 2).
The subagent review found that a `- [x] rule` bullet was treated as a diff; fixed before merge (turn 2).

## Context budget

`omoikane/bin/context-budget.py` fails CI when `AGENTS.md`, the skill descriptions or the session brief outgrow their budget (source: [[session-2026-09-30-c14af01e]], turn 2).
The review found that a brief that crashed still passed the gate; fixed before merge (turn 2).
A real rule costs about 65 tokens because of its page pointer, so 15 of them exceed 2,600 tokens; the agent added a test with a full block and adjusted the limit (turn 2).

CI never measured a full session brief (issue #37); since PR #38 the brief is measured on a generated worst case that fills every bound, without the repository wiki (source: [[session-2026-09-30-230a182d]], turn 2).
