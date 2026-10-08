---
title: Domain glossary
type: concept
summary: Record of each business term the user defines, built as domain pages tagged `term` (PR #94): definition, rejected words
tags: [glossary, domain]
created: 2026-10-02
updated: 2026-10-08
sources: [wiki/sources/2026-10-02-ste-and-oversight-posts.md, wiki/sources/session-2026-10-02-a9384e33.md, wiki/sources/session-2026-10-06-61eabe29.md]
code: [omoikane/prompts/distill.md, omoikane/prompts/ingest.md]
---

The idea, taken from the controlled dictionary of [[asd-ste100]]: when the user fixes what a business term means, the system's wiki records the term, its definition and the words rejected for it (source: [[2026-10-02-ste-and-oversight-posts]]).

## Why

Without that record an agent swaps synonyms, names entities wrongly, and one idea becomes two pages that grep does not join (source: [[2026-10-02-ste-and-oversight-posts]]).
A term's meaning is domain knowledge stated while building, which [[omoikane-objective]] says the wiki must hold.

## Status

Built by issue #90, PR #94: distill and ingest record the meaning the user gives a domain term, with a `term` tag (source: [[session-2026-10-02-a9384e33]], turns 2, 9).
PR #94 merged as `4626f21` (source: [[session-2026-10-06-61eabe29]], turns 6, 7).

The glossary has no page of its own. A term is a `domain` page tagged `term` (`omoikane/prompts/distill.md`, step 4):

- `summary` is the definition in one line, starting with the term.
- The body lists the words the user rejected for the term, if the user rejected any.
- Every page uses the term as defined, except in quotes, in that list and in code identifiers.

A glossary that a source defines goes one `term` page per topic, so the brief keeps room for decisions and gotchas. A term the source pairs with a rejected word gets a page of its own (`omoikane/prompts/ingest.md`).

## History

- 2026-10-02: not implemented; no prompt under `omoikane/prompts/` mentioned a glossary, and where it would live was open (source: [[2026-10-02-ste-and-oversight-posts]]).
