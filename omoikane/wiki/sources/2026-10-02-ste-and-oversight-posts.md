---
title: 2026-10-02 STE and oversight posts
type: source
summary: Karpathy's and Kun Chen's posts on ASD-STE100 for model output, and the three ideas the user took for Omoikane
tags: [references, writing-style, glossary]
created: 2026-10-02
updated: 2026-10-02
dated: 2026-10-02
sources: []
---

A note written for ingest by the agent of an interactive session, from the user's analysis of two posts on X.
`dated` comes from its second line, "Written 2026-10-02", and both posts carry the same date.
Scope: a summary of two short posts and the user's reading of what applies to Omoikane; partial notes, not a study of ASD-STE100.
The note says it is for people and agents improving Omoikane itself and states no rule for a system built from the template.

## The posts

- Andrej Karpathy, 2026-10-02 (https://x.com/karpathy/status/2105819303471976479): as models do more of the work, the human's work moves up to oversight and understanding of what the model produced. His tip: ask the model to write in [[asd-ste100]]; he finds the result more readable, and since the full specification is strict he sometimes asks for "80% of the way to ASD-STE100".
- Kun Chen, 2026-10-02 (https://x.com/kunchenguid/status/2105931853815296295): tested the tip and found answers clearer, also inside HTML artifacts; the full rule set is too strict, a subset works. His prompt samples 10 interactive session transcripts from the past week, checks which STE rules would have made the assistant's answers clearer, and writes those rules into the user-level `AGENTS.md`.
- Access: X blocks direct reads; both posts were read through `curl -s -A "Mozilla/5.0" https://api.fxtwitter.com/<user>/status/<id>`.

## Key claims for Omoikane

1. STE's controlled dictionary, where each approved word has one meaning, becomes a [[domain-glossary]]: when the user fixes what a business term means, the wiki records the term, its definition and the words rejected for it. Without it an agent swaps synonyms, names entities wrongly, and one idea becomes two pages that grep does not join.
2. A subset of STE for the text of wiki pages, because the `summary` lines go into the brief of every session: one term, one meaning, no synonyms; imperative in rules and procedures; active voice; at most 20 words per sentence in procedures and 25 in descriptions; at most 3 nouns in a row; one topic per paragraph. The rules must live in the repository, because a scheduled headless run does not load the user's own settings. See [[asd-ste100]].
3. Kun Chen's prompt stays out of Omoikane: it tunes the user's own conversation style, which belongs to the user level (`~/.claude`, the user's `AGENTS.md`). Put into the template, every system cloned from it would inherit one person's style as a rule.

## What it adds

The wiki had no page on writing style, glossaries or synonyms.
Neither idea 1 nor idea 2 is implemented at ingest time: no prompt under `omoikane/prompts/` and no line of `AGENTS.md` mentions a glossary or a style subset (checked by grep on 2026-10-02).
Idea 1 serves [[omoikane-objective]]: a term's meaning is domain knowledge the user states while building.
