---
title: wiki-rules
type: entity
summary: omoikane/bin/wiki-rules.py promotes ticked rule proposals into AGENTS.md; context-budget.py caps what sessions load
tags: [wiki-rules, context-budget, module, rules]
created: 2026-09-30
updated: 2026-10-02
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-01-d4302021.md]
code: [omoikane/bin/wiki-rules.py, omoikane/bin/context-budget.py, tests/test_wiki_rules.py]
---

`/synthesize` proposes `- [ ] rule` bullets in `_review.md`; after the human ticks one, `python omoikane/bin/wiki-rules.py` writes it into the managed rules block of `AGENTS.md` (source: [[session-2026-09-30-c14af01e]], turn 2).
In the eval, promotion worked and was idempotent (turn 2).
The subagent review found that a `- [x] rule` bullet was treated as a diff; fixed before merge (turn 2).

## Context budget

`omoikane/bin/context-budget.py` fails CI when `AGENTS.md`, the skill descriptions or the session brief outgrow their budget (source: [[session-2026-09-30-c14af01e]], turn 2).
The review found that a brief that crashed still passed the gate; fixed before merge (turn 2).
A real rule costs about 65 tokens because of its page pointer, so 15 of them exceed 2,600 tokens; the agent added a test with a full block and adjusted the limit (turn 2).

The first real promotion, the subagent review rule (PR #51 for issue #50, open at capture), took 1 of 15 slots with the budget green; it turned the budget test red, because the test assumed an empty rules block. The test now empties the block before filling it, the worst case (source: [[session-2026-10-01-b5b6fb27]], turn 2).

With one rule promoted, the measured budget was `AGENTS.md` 1929 / 2800 tokens, skill frontmatter 251 / 600, session brief 3760 / 4000, total 5940 / 7000 (source: [[session-2026-10-01-d4302021]], turn 5).

CI never measured a full session brief (issue #37); since PR #38 the brief is measured on a generated worst case that fills every bound, without the repository wiki (source: [[session-2026-09-30-230a182d]], turn 2).
