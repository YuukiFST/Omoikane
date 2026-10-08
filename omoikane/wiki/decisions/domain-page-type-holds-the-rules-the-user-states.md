---
title: Domain page type holds the rules the user states
type: decision
summary: User-stated business, design-system and convention rules get a domain page type; no older type fit them
tags: [domain, page-contract, distill, wiki-lint]
created: 2026-10-06
updated: 2026-10-06
sources: [wiki/sources/commits-2026-09-29-to-2026-10-06.md]
code: [omoikane/bin/wikilib.py, omoikane/bin/wiki-lint.py, omoikane/bin/session-context.py, omoikane/prompts/distill.md]
---

Chosen: a `domain` page holds one business rule, design-system rule or organisation convention the user states, its summary being the rule (source: [[commits-2026-09-29-to-2026-10-06]], `ace6fe6`).
The index and the brief list domain pages first, so the budget cuts them last (`ace6fe6`).

## Rejected

The page types were shaped for lessons about code, so such a rule had no destination (`ace6fe6`):

- a practice needs two sessions;
- a decision needs rejected alternatives;
- a concept has no source floor and is cut first from the brief;
- the `## Domain` section of `AGENTS.md` waited for the human to fill it in, which the objective rules out; the section was removed.

## Details

- `wiki-lint.py` fails a domain page that cites no source page. The first check matched any existing page, so a domain page could cite itself, a concept page, or a source slug from another folder; only a source page counts now (`ace6fe6`, `ddd79dc`).
- `distill.md` skipped "restatements of the prompt", so a rule stated inside a coding prompt tended to be dropped. It now writes the rule, quoted with its turn, and a new reject rule, `task-only`, drops instructions scoped to the current change (`c377d0d`).
- `/ingest` writes domain pages from documents that set rules; `/prune` leaves a domain page alone when only the code disagrees with it (`c377d0d`).
- The review of #72 found that a rule a check could catch lost its page to the guard route, that code breaking a rule became a dispute instead of a rule and a todo, and that a disputed rule reached the brief as settled; each was fixed (`1802d44`).
