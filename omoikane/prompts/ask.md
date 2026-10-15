# Answer a question from the wiki

Task: answer the question given as argument using wiki pages, then file the answer so it compounds.

Steps:

1. Read `omoikane/index.md`. Pick every page whose summary bears on the question. Read them.
2. If the wiki lacks what the question needs, search the captured sessions. Distill keeps only lessons; many details, the human's exact words among them, live only in a capture. Grep the words and identifiers of the question in `omoikane/raw/sources/sessions/` and `omoikane/raw/inbox/sessions/`, then read the turn around each hit.
   Cite a distilled capture by its source page and turn: `raw/sources/sessions/2026-10-08-21f37812.md` is `[[session-2026-10-08-21f37812]], turn 3` (`-part<n>` when its frontmatter `part` is above 1). Cite a capture still in the inbox, which has no source page, by its path and turn.
   Label what a capture says as raw evidence, not as a settled rule: a turn records what was said or tried that day, and a later turn or session can reverse it. When the answer rests on a rule that only a capture holds, say so in the answer and name it as an item for the next `/distill`. For a capture already under `raw/sources/sessions/`, the distill that read it missed the rule: also append `- todo <slug>: <the rule, one line> (session <id8>, turn <n>)` to `omoikane/_review.md`, under the heading `## [YYYY-MM-DD] ask | <question>`.
3. If the captures lack it too, search the history the remote already holds before you give up, never local commits: `git log origin/main --grep=<word>` and `git log origin/main -S <identifier>` for the commits that state why, `git log origin/main --follow -- <path>` and `git blame -L <start>,<end> origin/main -- <path>` for the code the question names, `gh pr view <number> --json title,body` for a PR those commits name. When the history answers it, write what you found to `omoikane/raw/inbox/<YYYY-MM-DD>-history-<slug>.md`: the question, then each commit as short SHA, date and message, each PR as number, title and the passage that answers. Copy no author name, email, `*-by:` trailer or secret: what the wiki holds is pushed. Ingest that file with `omoikane/prompts/ingest.md`, then answer from the pages it wrote. In a scheduled run (`wiki-ingest.ps1`) you have no shell: skip the search.
   When none of them holds the answer, say which pages and captures you read, which searches you ran and what is missing, and suggest which source to add. Stop there; do not fill the gap from memory.
4. Write the answer with an inline citation on every claim: `[[slug]]`, or the path and turn of an inbox capture. A reason a commit or PR does not state in words is your inference: say so. When the answer describes current state, open it with a cutoff line, "as of YYYY-MM-DD", using the `dated` of the newest source it rests on.
5. File it as `omoikane/wiki/queries/<YYYY-MM-DD>-<slug>.md` using the page contract, `type: query`, `sources:` listing every page cited. An inbox capture has no page: its citation stays in the text.
6. Append to `omoikane/log.md`: `## [YYYY-MM-DD] query | <question>`, then one line per todo filed in step 2: `- routed (todo) <slug>: <the rule, one line> (session <id8>, turn <n>)`. Distill reads these lines and does not file the same todo again.
7. Run `python omoikane/bin/wiki-index.py` then `python omoikane/bin/wiki-lint.py`. In a scheduled run (`wiki-ingest.ps1`) skip this step: you have no shell, and lint runs after you and sends its findings back.

Output: the answer, then the path of the filed page.
