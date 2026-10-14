---
title: Discoverable code
type: concept
summary: Code whose names, types and comments are good search terms for an agent that finds code by text search
tags: [discoverable-code, naming, skills, omoikane-mode]
created: 2026-10-09
updated: 2026-10-09
sources: [wiki/sources/2026-10-08-how-coding-agents-read-your-code.md]
code: [.claude/skills/omoikane-mode/references/principles/minimize-reader-load.md, .claude/skills/codebase-design/SKILL.md]
---

Coding agents find code by text search (`rg`) and trust what names tell them; a generic name returns wrong candidates, and each costs hundreds to thousands of tokens (source: [[2026-10-08-how-coding-agents-read-your-code]]).
The article behind it: Ben Vinegar, Modem, "How coding agents read your code (and how to write for them)", July 20, 2026.

## The rules the article gives

- Names of two to three words, with one domain word: "make the words in your code good search terms."
- Precise types.
- A why-comment on the definition, where a search lands.
- One spelling per concept.
- Test files named after their source.
- Legacy code deprecated or removed.

Its data: tokens per question fell by 6% to 66% on weak-author code; a refactor of a 4,943-line file took bug-hunt results from 23 of 32 to 32 of 32. The author calls them "illustrative, not definitive" (same source).

## What the template ships

- No naming rule. "Grep-able names" and "Comments carry the *why*" sit in the user's global `~/.claude/CODING_STANDARDS.md`, which a system built from the template does not get (same source).
- No principle under `.claude/skills/omoikane-mode/references/principles/` covers names; `minimize-reader-load.md` covers layers and state.
- `.claude/skills/codebase-design/SKILL.md` names "AI-navigable" code in its description and gives no naming rule.
- Branded types: `type-system-discipline.md`. Legacy removal: `migrate-callers-then-delete-legacy-apis.md`.
- One spelling per concept holds for wiki text through `term` pages ([[domain-glossary]]), which exempt code identifiers.

## Proposed

Vendor a "write discoverable code" principle into `omoikane-mode`: domain-word names, one spelling, a why-comment on the definition, test names; cite the article (source: [[2026-10-08-how-coding-agents-read-your-code]], candidate issue 2).
It is not an issue yet. See [[omoikane-mode-routes-each-task-to-a-playbook]] for the principles the mode indexes.

## The same idea in the wiki

The wiki applies it to knowledge: page slugs are full sentences that grep finds once (same source).
The article: "Grep can find code; it can't find the absence of code." So the note proposes a domain page for each deliberate absence the human states; see [[domain-page-type-holds-the-rules-the-user-states]].
