---
title: ASD-STE100
type: concept
summary: Simplified Technical English, aerospace's controlled language; a subset of it is proposed for wiki page text
tags: [writing-style, references]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/2026-10-02-ste-and-oversight-posts.md]
---

ASD-STE100 (Simplified Technical English) is the controlled language of aerospace maintenance documentation (source: [[2026-10-02-ste-and-oversight-posts]]).
Its dictionary gives each approved word one meaning (source: [[2026-10-02-ste-and-oversight-posts]]).

## Why it came up

Karpathy recommends asking a model to write in it, so the human can oversee and understand model output; the full specification is strict, so he sometimes asks for "80% of the way" (source: [[2026-10-02-ste-and-oversight-posts]]).
Kun Chen confirmed answers get clearer with a subset, not the full rule set (source: [[2026-10-02-ste-and-oversight-posts]]).

## Proposed use in Omoikane

Not implemented as of 2026-10-02.

- Wiki page text, `summary` lines first since every session brief loads them: one term, one meaning, no synonyms; imperative in rules and procedures; active voice; at most 20 words per sentence in procedures and 25 in descriptions; at most 3 nouns in a row; one topic per paragraph (source: [[2026-10-02-ste-and-oversight-posts]]).
- The subset must live in the repository, since a scheduled headless run does not load the user's settings (source: [[2026-10-02-ste-and-oversight-posts]]); see [[user-settings-apply-to-headless-claude-runs]] for how headless runs are set to load project settings only.
- The one-meaning dictionary carries over to a system's business terms as a [[domain-glossary]] (source: [[2026-10-02-ste-and-oversight-posts]]).

## Rejected

Kun Chen's prompt, which writes STE rules mined from the user's transcripts into the user-level `AGENTS.md`, stays out of the template: it tunes one person's conversation style, and every system cloned from Omoikane would inherit it as a rule (source: [[2026-10-02-ste-and-oversight-posts]]).
