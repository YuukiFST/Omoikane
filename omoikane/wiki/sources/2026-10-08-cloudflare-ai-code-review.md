---
title: 2026-10-08 Cloudflare AI code review
type: source
summary: Gap note on Cloudflare's multi-agent code review post: eight ideas interrogate lacks, five candidate issues
tags: [code-review, interrogate, reference, cloudflare, article]
created: 2026-10-09
updated: 2026-10-09
dated: 2026-10-08
sources: []
code: [.claude/skills/interrogate/SKILL.md, .claude/skills/interrogate/references/rubric.md, .claude/skills/interrogate/references/reviewer-prompt.md, .claude/skills/interrogate/references/lead-judgment.md, .claude/skills/blast-radius/SKILL.md]
---

A note, `omoikane/raw/sources/2026-10-08-cloudflare-ai-code-review.md`, on what one article offers Omoikane.
It was written in [[session-2026-10-08-21f37812]] (turns 7, 8) and added to `main` by PR #134 (issue #133): commit `e1bb545`, then `f88e83f` with the review fixes, both on 2026-10-08.
`dated` is the day the note says it read the article ("Read: 2026-10-08", line 6), which is also the day of both commits.

The article: Ryan Skidmore, "Orchestrating AI Code Review at scale", https://blog.cloudflare.com/ai-code-review/ (note, lines 3, 4).
The page shows April 20, 2026; its metadata gives `dateModified` 2026-07-15 (note, line 5).

## Scope

A gap analysis of one article against the review skills of this repository, not a summary of the article.
The agent read the full HTML once with `curl -sL`; every quote comes from that text (note, lines 10, 11).
It did not read the images, it got the findings-by-reviewer table only in part, and the `risk.ts` snippet lost its first condition (note, lines 12 to 14).
So the article's numbers and its example review are not in the note.

## What the article describes

- Up to seven specialist reviewers run on each merge request, in CI, on OpenCode (note, line 18).
- A coordinator merges, re-sorts and filters their findings, then posts one review comment (note, line 19).
- Diff size sets a risk tier; the tier picks the reviewer set and the model (note, line 20).
- Re-reviews track earlier findings, and a separate reviewer checks whether `AGENTS.md` needs an update (note, line 21).

## Key claims: what Omoikane lacks

Each gap is measured against [[interrogate]] and `blast-radius`, the two skills the review route of `omoikane-mode` sends (`.claude/skills/omoikane-mode/SKILL.md`, line 30).

1. No explicit "do not flag" list for each lens. The article: "telling an LLM what not to do is where the actual prompt engineering value resides" (note, lines 25 to 31).
   Omoikane has scattered rules (`reviewer-prompt.md` line 37; `rubric.md` lines 17, 43, 72; `lead-judgment.md` line 37), but no list per lens.
   Line 72 of `rubric.md` is the Security section's one rule, "trace the input path through the code and show it"; that section lists no exclusions.
2. No check that a change makes the agent instructions stale. The article: "these files rot incredibly fast" (note, lines 33 to 39).
   Omoikane checks only size (`omoikane/bin/context-budget.py`) and dead `code:` paths ([[wiki-lint]]).
   Nothing compares a diff with `AGENTS.md`, the skills or the domain pages. The note puts this close to the memory half of [[omoikane-objective]].
3. Re-reviews do not start from the previous review: fixed findings are left out, unfixed ones come back, resolved ones stay resolved (note, lines 41 to 46).
   `interrogate` Step 1 never takes the earlier posted review, although sessions re-review PRs ([[review-each-pr-with-a-subagent-before-merging]], #56 and #92).
4. The diff size does not set how many reviewers run. The article: "don't send the dream team to review a typo fix"; sensitive paths such as `auth/` and `crypto/` always get the full review (note, lines 48 to 52).
5. No shared context file: the reviewer template puts `{DIFF_OR_FILES}` inline in each of the five prompts (`reviewer-prompt.md`, line 25). The article: "would multiply our token costs by 7x" (note, lines 54 to 57).
6. No diff noise filter: Cloudflare drops lock files, vendored code, minified files and source maps, and keeps migrations (note, lines 59 to 63).
7. No rule to treat author-written text as data in `interrogate` Step 2 or `blast-radius` Step 1 (note, lines 65 to 70). Babysit already treats review-comment text as untrusted (`.claude/skills/omoikane-mode/playbooks/babysit.md`, line 17).
   The note gives the `blast-radius` call as `gh pr view --json title,body`; the skill runs `gh pr view <number> --json title,body,commits,files` (`.claude/skills/blast-radius/SKILL.md`, line 33).
8. No overall verdict from a rubric with "a bias toward approval" (note, lines 72 to 76).

## Already covered

The note lists ten points where Omoikane does the same or more (note, lines 80 to 90).
Among them: one narrow lens per reviewer; a judge pass that merges and drops speculative findings; few findings on purpose (`lead-judgment.md`, "Verdict Calibration": "more than 5 items" in Act On is a sign of weak filtering).
`blast-radius` goes further than the article on cross-system impact, a limit the article admits: it proves the key safety fact by running code (note, line 87).
The human owns every merge, so no "break glass" override is needed (note, lines 90, 105).

## Candidate issues

Ranked by value for the objective (note, lines 96 to 100):

1. Check each diff for memory drift against `AGENTS.md`, the skills and the domain pages, in `blast-radius` Step 1, not as a sixth lens.
2. Add a "do not flag" section to each lens in `rubric.md`, starting from the article's security exclusions.
3. Make a re-review read the previous posted review.
4. Scale the lens set to the diff size; always run every lens on security-sensitive paths.
5. Write the filtered diff once to a temp file for all reviewers; drop lock and minified files, keep migrations.

Rejected by the note (lines 102 to 108): idea 8, since "an automatic approve or block decides nothing" when the human merges; model tiers, circuit breakers, fallback chains and telemetry, which serve a CI service at scale; idea 7 alone, to fold into issue 3 or 5; the light-hearted answer per review.
None of the five became an issue or a `_review.md` item by 2026-10-09: the last issue, #138, is the Pi and security-audit record (`gh issue list`).

## Reference proposal

The note recommends the article as a reference "if the user approves", as the most detailed source read so far on multi-agent code review (note, lines 112 to 117).
It observes that the rule on [[omoikane-references]] names only capture, distill, storage and loading, while the list already holds the two Cloudflare security entries the user added on 2026-10-07.
The user added every entry on that page, so the agent only proposes this one. The user has not answered.

## What it adds

- The first gap map of [[interrogate]] against an outside review system.
- A memory-drift check as a review step, close to the memory half of [[omoikane-objective]]: the wiki had no such proposal.
- A reference candidate for the review skills, which the rule on [[omoikane-references]] does not cover yet.

Its sibling note from PR #134, [[2026-10-08-how-coding-agents-read-your-code]], also ranks first a link between code and the memory pages: there the pages about a file appear when the agent reads or edits it, here a review checks a diff for memory drift.
