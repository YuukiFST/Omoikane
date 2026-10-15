# How coding agents read your code (and how to write for them)

- URL read: https://modem.ai/blog/how-coding-agents-read-your-code
- URL given: https://modem.dev/blog/how-coding-agents-read-your-code2. It redirects (307) to modem.ai and returns 404.
- The URL without the trailing `2` opens. modem.dev redirects to modem.ai. That is the version this note uses.
- Author: Ben Vinegar, Modem.
- Date on the page: July 20, 2026.
- Series: Part 1 of "Writing Code for Agents". Part 2 is "The Power of Determinism". This note does not cover Part 2.
- Date read: 2026-10-08.

## What the article says

Coding agents find code by text search (`rg`) and trust what names tell them.
Generic names add noise to the context, and each wrong candidate costs hundreds to thousands of tokens.
Advice: names of two to three words with one domain word, precise types, a why-comment on the definition, one spelling per concept, test files named after their source, and legacy code deprecated or removed.
The author's `write-discoverable-code` skill cut tokens per question by 6% to 66% on weak-author code.
A refactor of a 4,943-line file cut tokens by about a third for weaker models.
It raised bug-hunt results from 23 of 32 to 32 of 32.
The author calls the results "illustrative, not definitive".

## Ideas Omoikane lacks

1. **A discoverable-naming rule shipped with the template.**
   Quote: "make the words in your code good search terms."
   Omoikane has "Grep-able names" only in the user's global `~/.claude/CODING_STANDARDS.md`, so it is machine-local, and systems built from the template do not get it.
   No principle under `.claude/skills/omoikane-mode/references/principles/` covers names. `minimize-reader-load.md` covers layers and state, not search terms.
   Affects: `.claude/skills/omoikane-mode/references/principles/`, `.claude/skills/codebase-design/SKILL.md` (its description says "AI-navigable" but gives no naming rule).

2. **Knowledge at the place where search lands.**
   Quote: "it sits exactly where searches land."
   Omoikane keeps decisions and gotchas in wiki pages, linked to code only by the page's `code:` list.
   The agent gets to them only if it follows the `AGENTS.md` build-mode bullet "open the decision and gotcha pages whose `code:` lists it".
   That bullet is an instruction to remember, and so is the brief's header, "Open a page before touching the area it covers". Nothing shows the agent the page when it opens or edits the file.
   Affects: `AGENTS.md` (build mode), `.claude/settings.json` (hooks), `omoikane/bin/session-context.py` (the pending work and the index, at session start; nothing per file).

3. **Record what the code deliberately does not do.**
   Quote: "Grep can find code; it can't find the absence of code."
   The article saw a question with no answer get more expensive after the refactor.
   Omoikane decision pages record rejected alternatives. No page type or distill step records "this system never does X" for a behaviour a reader would expect.
   Affects: `omoikane/prompts/distill.md`, `omoikane/prompts/ingest.md`, the `domain` page type in `AGENTS.md`.


## Already covered, same or better

- **Text search, no embeddings.** The wiki is plain Markdown with an index. `/ask` reads pages and git history; no vector store. See `omoikane/prompts/ask.md`, `omoikane/index.md`.
- **Unique, long, searchable names for knowledge.** Page slugs are kebab-case full sentences, so a grep for the slug finds one page. See the page contract in `AGENTS.md`.
- **One spelling per concept.** The page contract demands "one word, one meaning", and `term` domain pages define terms. See `AGENTS.md`, `omoikane/wiki/domain/`.
- **Record conventions in AGENTS.md.** Domain pages tagged `convention`, the managed rules block and the SessionStart brief do this, with a budget. See `AGENTS.md`, `omoikane/bin/wiki-rules.py`, `omoikane/bin/session-context.py`.
- **Context noise costs tokens.** `omoikane/bin/context-budget.py` caps what every session loads. `.claude/skills/omoikane-mode/references/principles/guard-the-context-window.md` routes bulk reads to subagents.
- **Prebuilt maps can fail silently.** The article warns that "Prebuilt indexes bring a failure mode of their own." `compact_index` in `omoikane/bin/session-context.py` prints an "Omitted by budget" line and points to `omoikane/index.md`. `wiki-lint.py` fails when a `code:` path is gone.
- **Precise and branded types, compiler feedback.** `.claude/skills/omoikane-mode/references/principles/type-system-discipline.md` brands semantic primitives (`UserId`, `OrderId`).
- **Deprecate or remove legacy code.** `.claude/skills/omoikane-mode/references/principles/migrate-callers-then-delete-legacy-apis.md`.
- **Test files named after their source.** `tests/test_wiki_lint.py` covers `omoikane/bin/wiki-lint.py`, and most test files follow the same pattern.
- **The worst file sets the floor.** Quote: "the new floor became the worst file left standing." `.claude/skills/improve/references/audit-playbook.md` line 65 flags god modules, and `.claude/skills/interrogate/references/code-quality-review.md` line 23 flags a file pushed past 1k lines. Not covered: a generic grab-bag file that is not oversized.
- **Do not trust a misleading name.** The `how` explorer prompt says "Don't guess from names. Read the code." See `.claude/skills/how/references/explorer-prompt.md`.
- **Why-comments.** The global `CODING_STANDARDS.md` says comments carry the why. It is user-level, so idea 1 applies to it too.

## Candidate issues

Ranked by value for the objective in `omoikane/wiki/domain/omoikane-objective.md`.

1. Add a hook that names the decision and gotcha pages whose `code:` lists a file when the agent reads or edits it. First confirm what hook output Claude Code adds to context.
2. Vendor a "write discoverable code" principle into `omoikane-mode` principles: domain-word names, one spelling, why-comment on the definition, test names. Cite this article.
3. Make distill and ingest write a domain page for each deliberate absence the human states ("the system never does X"). Put the behaviour in the page title.
4. Not worth it now: a grab-bag file check in `/improve`. That skill already surveys tech debt, and the article shows one case only.
5. Not worth it now: a token-per-question eval of the brief and the index. The runs cost a lot, and the article calls its own data illustrative. `context-budget.py` already caps the load.

## Reference?

No, not as a standing entry in `omoikane/wiki/domain/omoikane-references.md`.
The rule on that page covers how Omoikane captures, distills, stores or loads knowledge; the list already reaches past it to review-side entries. This article covers how agents read source code.
It is one blog post with observational data, and it is not a project to consult again.
Cite it as the source of candidate issue 2, if that issue lands, and ingest it then through `omoikane/raw/inbox/`.
Read Part 2, "The Power of Determinism", before you decide on the series as a whole.
