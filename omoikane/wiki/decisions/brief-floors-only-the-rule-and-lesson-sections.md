---
title: Brief floors only the rule and lesson sections
type: decision
summary: The session brief gives a budget floor to Domain, Decisions, Gotchas and Practices only; separators count
tags: [session-context, brief, context-budget]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-10-02-a8b45323.md]
code: [omoikane/bin/session-context.py, tests/test_wiki_lint.py]
---

Chosen: `compact_index` in `omoikane/bin/session-context.py` gives each section in `FLOORED = ("Domain", "Decisions", "Gotchas", "Practices")` its first entry and more up to a floor, half the budget shared among them, then fills the rest in index order (issue #75, PR #83) (source: [[session-2026-10-02-a8b45323]], turn 2).
Reason: domain pages are listed first, so many of them could push every decision and gotcha out of the brief (`omoikane/bin/session-context.py`).

Rejected: a floor for every section. The review of #83 found it took room from the domain rules; sources, entities, concepts and queries have none, since the omitted line sends the agent to `index.md` for them (turn 2; `omoikane/bin/session-context.py`).

Two more review findings, fixed in the same PR (turn 2):

- A first entry larger than the floor vanished; it now always comes in (`test_a_first_entry_larger_than_the_floor_still_comes_in`).
- The blank line between sections did not count and overran the budget; it counts now, and the budget test was tightened to catch the old overrun (turn 2).

See [[session-context]].
