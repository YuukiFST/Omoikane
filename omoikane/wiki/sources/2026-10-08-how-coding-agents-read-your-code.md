---
title: 2026-10-08 How coding agents read your code
type: source
summary: Gap note on Modem's post on how agents search code: three ideas Omoikane lacks, three candidate issues, not a reference
tags: [discoverable-code, naming, reference, modem, article]
created: 2026-10-09
updated: 2026-10-09
dated: 2026-10-08
sources: []
code: [.claude/skills/omoikane-mode/references/principles/minimize-reader-load.md, .claude/skills/codebase-design/SKILL.md, omoikane/bin/session-context.py, .claude/settings.json, omoikane/prompts/distill.md]
---

A note, `omoikane/raw/sources/2026-10-08-how-coding-agents-read-your-code.md`, on what one article offers Omoikane.
It was written in [[session-2026-10-08-21f37812]] (turns 7, 8) and added to `main` by PR #134 (issue #133): commit `e1bb545`, then `f88e83f` with the review fixes, both on 2026-10-08.
Its sibling note from the same PR: [[2026-10-08-cloudflare-ai-code-review]].
`dated` is the day the note says it read the article ("Date read: 2026-10-08", line 9), which is also the day of both commits.

The article: Ben Vinegar, Modem, "How coding agents read your code (and how to write for them)", https://modem.ai/blog/how-coding-agents-read-your-code (note, lines 1, 3, 6).
The page shows July 20, 2026 (note, line 7).
The URL the user gave, `https://modem.dev/blog/how-coding-agents-read-your-code2`, redirects to modem.ai and returns 404; the note uses the URL without the trailing `2` (note, lines 4, 5).

## Scope

A gap analysis of Part 1 of the series "Writing Code for Agents" against this repository, not a summary of the article.
Part 2, "The Power of Determinism", is not read (note, line 8).

## What the article says

- Coding agents find code by text search (`rg`) and trust what names tell them (note, line 13).
- Generic names add noise to the context; each wrong candidate costs hundreds to thousands of tokens (note, line 14).
- Advice: names of two to three words with one domain word, precise types, a why-comment on the definition, one spelling per concept, test files named after their source, legacy code deprecated or removed (note, line 15).
- The author's `write-discoverable-code` skill cut tokens per question by 6% to 66% on weak-author code (note, line 16).
- A refactor of a 4,943-line file cut tokens by about a third for weaker models, and raised bug-hunt results from 23 of 32 to 32 of 32 (note, lines 17, 18).
- The author calls the results "illustrative, not definitive" (note, line 19).

## Key claims: what Omoikane lacks

1. No discoverable-naming rule ships with the template (note, lines 23 to 27). The article: "make the words in your code good search terms."
   "Grep-able names" sits only in the user's global `~/.claude/CODING_STANDARDS.md` (line 29 there), so systems built from the template do not get it.
   No principle under `.claude/skills/omoikane-mode/references/principles/` covers names; `minimize-reader-load.md` covers layers and state.
   `.claude/skills/codebase-design/SKILL.md` says "AI-navigable" in its description and gives no naming rule. See [[discoverable-code]].
2. Knowledge does not sit where a search lands (note, lines 29 to 34). The article: "it sits exactly where searches land."
   Decisions and gotchas reach an agent only if it follows the build-mode bullet of `AGENTS.md` (line 74) and the brief's header, "Open a page before touching the area it covers" (`omoikane/bin/session-context.py`, line 26).
   No hook shows the page when the agent opens or edits a file: `.claude/settings.json` has `PreToolUse` on `Bash` only (the escape-edit guard), `SessionStart`, `Stop` and `SessionEnd`. See [[session-context]].
3. Nothing records what the code deliberately does not do (note, lines 36 to 40). The article: "Grep can find code; it can't find the absence of code."
   The article saw a question with no answer get more expensive after the refactor.

## Already covered

The note lists twelve points where Omoikane does the same or more (note, lines 45 to 56).
Among them: text search over plain Markdown and git history, no vector store (`omoikane/prompts/ask.md`); long kebab-case slugs that grep finds once; `context-budget.py` capping what each session loads; `compact_index` printing "Omitted by budget" so a cut index does not fail silently (`omoikane/bin/session-context.py`, line 84).
The worst-file floor ("the new floor became the worst file left standing") is covered by `audit-playbook.md` line 65 (god modules) and [[interrogate]]'s `code-quality-review.md` line 23 (a file pushed past 1k lines), but not for a grab-bag file that is not oversized.

## Verification on 2026-10-09

Every file and line the note cites holds on the working tree of 2026-10-09: `AGENTS.md` line 74, `session-context.py` lines 26 and 84, `audit-playbook.md` line 65, `code-quality-review.md` line 23, the "Don't guess from names" line of `.claude/skills/how/references/explorer-prompt.md` (line 21), `UserId` and `OrderId` in `type-system-discipline.md` (line 14).
"Most test files follow the same pattern": 12 of the 14 `tests/test_*.py` files name a script under `omoikane/bin/` or `.claude/hooks/`; `test_powershell_scripts.py` and `test_skills_manifest.py` do not.
Two coverage claims are narrower than the note states:

- "One spelling per concept" holds for wiki text only. The term rule exempts code identifiers ("except in quotes, in that list and in code identifiers", `omoikane/prompts/distill.md`, line 39; [[domain-glossary]]), and the article is about code.
- Idea 3 is partly covered: the `domain` type already takes a prohibition the user states, as the example "never a raw colour" shows (`omoikane/prompts/distill.md`, line 7). What is missing is a step that looks for a deliberate absence, and a title that names the behaviour.

## Candidate issues

Ranked by value for [[omoikane-objective]] (note, lines 60 to 66):

1. A hook that names the decision and gotcha pages whose `code:` lists a file when the agent reads or edits it. The note asks to confirm first what hook output Claude Code adds to context.
2. A "write discoverable code" principle in `omoikane-mode`: domain-word names, one spelling, a why-comment on the definition, test names. Cite this article. See [[omoikane-mode-routes-each-task-to-a-playbook]].
3. Distill and ingest write a domain page for each deliberate absence the human states ("the system never does X"), with the behaviour in the title. See [[domain-page-type-holds-the-rules-the-user-states]].

Rejected by the note: a grab-bag file check in `/improve`, since that skill already surveys tech debt and the article shows one case; a token-per-question eval of the brief and the index, since the runs cost a lot and `context-budget.py` already caps the load (note, lines 65, 66).
None of the three became an issue or a `_review.md` item by 2026-10-09.

## Where it meets the Cloudflare note

Both notes rank first a link between a code change and the memory pages about it.
[[2026-10-08-cloudflare-ai-code-review]] checks a diff for memory drift against `AGENTS.md`, the skills and the domain pages at review time; this note shows the pages whose `code:` lists a file when the agent reads or edits it.
Both also observe that the list on [[omoikane-references]] reaches past its rule (capture, distill, storage, loading) to review-side entries.

## Reference?

No (note, lines 70 to 74).
The note: the article covers how agents read source code, not how Omoikane captures, distills, stores or loads knowledge; it is one blog post with observational data, "not a project to consult again".
It is to be cited as the source of candidate issue 2 if that issue lands. The note asks to read Part 2 before a verdict on the series.

## What it adds

- The first page on [[discoverable-code]]: how agents find code by text search, and which of its rules the template ships.
- A gap in build mode: the pages about a file reach the agent only by an instruction it must remember.
- Deliberate absence as knowledge the wiki does not ask for.
