# Two posts on ASD-STE100 and reading model output, and what Omoikane takes from them

Written 2026-10-02 by the agent of an interactive session, from the user's analysis, for ingest.
Only the people and agents improving Omoikane itself use this note; it states no rule for a system built from the template.

## Sources

- Andrej Karpathy, 2026-10-02: https://x.com/karpathy/status/2105819303471976479
- Kun Chen, 2026-10-02: https://x.com/kunchenguid/status/2105931853815296295

X blocks direct reads; both posts were read through `curl -s -A "Mozilla/5.0" https://api.fxtwitter.com/<user>/status/<id>`.

## What the posts say

Karpathy: as models do more of the work, the human's work moves up to oversight and understanding of what the model produced.
One tip for that: ask the model to write in ASD-STE100, the controlled language of aerospace maintenance documentation.
He finds the result more readable.
The full specification is strict, so he sometimes asks for "80% of the way to ASD-STE100".

Kun Chen tested the tip and found that it makes model answers clearer, also inside HTML artifacts.
The full rule set is too strict; a subset works.
His prompt samples 10 interactive session transcripts from the past week, checks which STE rules would have made the assistant's answers clearer, and writes those rules into the user-level `AGENTS.md`.

## What applies to Omoikane

1. **The controlled dictionary becomes a domain glossary.**
   In STE each approved word has one meaning.
   For a system's domain, the same idea gives a glossary: when the user fixes what a business term means, the wiki records the term, its definition and the words rejected for it.
   Without that record an agent swaps synonyms, names entities wrongly, and one idea becomes two pages that grep does not join.
2. **A subset of STE for the text of wiki pages.**
   The page `summary` lines go into the brief of every session, so their clarity counts in every session.
   The subset: one term, one meaning, no synonyms; imperative in rules and procedures; active voice; sentences of at most 20 words in procedures and 25 in descriptions; at most 3 nouns in a row; one topic per paragraph.
   The rules must live in the repository, because a scheduled headless run does not load the user's own settings.
3. **Kun Chen's prompt stays out of Omoikane.**
   It tunes the user's own conversation style, which belongs to the user level (`~/.claude`, the user's `AGENTS.md`), not to a system's memory.
   Put into the template, every system cloned from it would inherit one person's style as a rule.
