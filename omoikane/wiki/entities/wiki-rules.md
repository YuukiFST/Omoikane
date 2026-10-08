---
title: wiki-rules
type: entity
summary: omoikane/bin/wiki-rules.py promotes ticked rule proposals into AGENTS.md; context-budget.py caps what sessions load
tags: [wiki-rules, context-budget, module, rules]
created: 2026-09-30
updated: 2026-10-07
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-a8b45323.md, wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/session-2026-10-07-062e80af.md]
code: [omoikane/bin/wiki-rules.py, omoikane/bin/context-budget.py, tests/test_wiki_rules.py]
---

`/synthesize` proposes `- [ ] rule` bullets in `_review.md`; after the human ticks one, `python omoikane/bin/wiki-rules.py` writes it into the managed rules block of `AGENTS.md` (source: [[session-2026-09-30-c14af01e]], turn 2).
In the eval, promotion worked and was idempotent (turn 2).
The subagent review found that a `- [x] rule` bullet was treated as a diff; fixed before merge (turn 2).

## Domain rules

Since issue #76 (PR #86) a ticked rule may point at a `domain` page as well as a practice: a domain rule is valid from one statement, so it reaches the block without a second session (source: [[session-2026-10-02-a8b45323]], turn 2; `omoikane/bin/wiki-rules.py`).
A slug that is both a practice and a domain page is refused, and a rule whose page became `Disputed:` or `prune:` between proposal and tick is held back (`omoikane/bin/wiki-rules.py`).
The headless eval in a clone: `/synthesize` proposed `rule` for `tenant_id` and for money in cents, and logged "total nunca abaixo de zero" and the button as `dropped (narrow)`; `wiki-rules.py` then promoted the ticked ones end to end (turn 2).
A promoted rule whose page later disappears or is disputed is a `wiki-lint.py` warning, not a finding: [[lint-findings-the-scheduled-agent-cannot-fix-are-warnings]].

## Context budget

`omoikane/bin/context-budget.py` fails CI when `AGENTS.md`, the skill descriptions or the session brief outgrow their budget (source: [[session-2026-09-30-c14af01e]], turn 2).
The review found that a brief that crashed still passed the gate; fixed before merge (turn 2).
A real rule costs about 65 tokens because of its page pointer, so 15 of them exceed 2,600 tokens; the agent added a test with a full block and adjusted the limit (turn 2).

The first real promotion, the subagent review rule (PR #51 for issue #50, open at capture), took 1 of 15 slots with the budget green; it turned the budget test red, because the test assumed an empty rules block. The test now empties the block before filling it, the worst case (source: [[session-2026-10-01-b5b6fb27]], turn 2).

With one rule promoted, the measured budget was `AGENTS.md` 1929 / 2800 tokens, skill frontmatter 251 / 600, session brief 3760 / 4000, total 5940 / 7000 (source: [[session-2026-10-01-d4302021]], turn 5).

On 2026-10-06 PR #95, green on its own CI, pushed the worst-case `AGENTS.md` to "2811 tokens, limit 2800" once merged onto the `main` that had PR #102: [[green-pr-ci-can-be-stale-against-the-current-main]] (source: [[session-2026-10-06-61eabe29]], turn 6).
Cutting the synthesize cadence sentence from `AGENTS.md` brought it to 2796 of 2800, 4 tokens of headroom (turn 7).

Issue #111 made every system ship the development skills ([[every-system-ships-the-development-skills]]).
Before it the session measured 6,007 of 7,000 tokens in total (source: [[session-2026-10-07-062e80af]], turn 4).
The skill frontmatter limit went from 600 to 2,600 tokens and the total from 7,000 to 9,000 (commit `9450ad6`).
With every skill merged, skill frontmatter measured 1,853 and the total 7,670, so commit `fd5a2a8` lowered the limits to 2,100 and 8,500 (turn 11).

CI never measured a full session brief (issue #37); since PR #38 the brief is measured on a generated worst case that fills every bound, without the repository wiki (source: [[session-2026-09-30-230a182d]], turn 2).
