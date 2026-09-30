# Distill one captured coding session

Task: turn the session file given as argument (written by `omoikane/bin/session-capture.py`, under `omoikane/raw/inbox/sessions/`) into wiki pages that a later agent working on this repository needs. Done means: session source page written, every decision and gotcha the session contains has a page, affected entity and concept pages updated, `omoikane/log.md` appended, session file moved to `omoikane/raw/sources/sessions/`, `wiki-lint.py` clean.

What is worth a page. Keep only what the code alone does not show:

- `decision`: a choice between alternatives, with the alternatives rejected and the reason. Skip a decision whose reason is obvious from the code or whose scope is one line.
- `gotcha`: a behaviour learned by running something: an API, library, tool or environment that acts differently from its docs or from what the agent expected, plus the workaround. A bug whose root cause took more than one attempt to find is a gotcha; the fix alone is not.
- Skip: routine edits, restatements of the prompt, anything already on a page (update that page instead), plans that were abandoned without a lesson.

Reject a candidate even when it reads like a lesson. Once on a page it becomes a rule a later agent obeys, so a wrong one costs more than a missing one:

- `missing-env`: the failure came from a binary, credential, network or environment variable missing on that machine. It says nothing about the code.
- `no-root-cause`: a broad claim that a tool, library or approach "does not work" without the cause the session found. Later agents turn it into a refusal to try.
- `self-resolved`: a failure the session fixed within a turn or two without learning why, such as a typo, a wrong path or a retry that passed.
- `one-off`: a smoke test, a throwaway check or a debug print.

Write only what the session shows. Copy paths, versions, flags and error text exactly; when the session does not give one, leave it out rather than supply it. A preference the user stated goes on the page in the user's own words, quoted, with the turn.

Steps:

1. Read the session file in full. Frontmatter gives `session`, `part`, `turns`, `started`, `branch`; `## Working tree at capture` and `## Files edited` list the code it touched.
2. Read `omoikane/index.md`. Open every decision, gotcha, entity and concept page whose `code:` paths or summary overlap the files this session touched.
3. Write `omoikane/wiki/sources/session-<YYYY-MM-DD>-<id8>.md` (append `-part<n>` when `part` is above 1) with the page contract, `type: source`, `dated` set to the `started` date. Body: what the session set out to do, what it changed, what it learned, in that order, each claim pointing at the turn it comes from (`turn 3`). Where the agent's own notes contradict each other across turns, record both under `## Contradictions` and append to `omoikane/_review.md`.
4. For each decision and gotcha: create `omoikane/wiki/decisions/<slug>.md` or `omoikane/wiki/gotchas/<slug>.md`, or update the existing page. Frontmatter: `code:` listing the repository paths the page is about (they must exist; `wiki-lint.py` fails otherwise), `sources:` including this session page. Cite the session inline on every claim. A new decision that reverses an older one links both ways under `## History` on each page and leaves the older page in place; when the session gives no reason for the reversal, append to `omoikane/_review.md`.
5. For each module, library, service or tool the session treats as central: update its entity page or create one. Recurring theme across three or more pages: concept page. Follow the ingest rules for citations and contradictions.
6. Append to `omoikane/log.md`: `## [YYYY-MM-DD] distill | session <id8>` followed by the pages created and updated, then one line per rejected candidate: `- skipped (<rule>): <candidate in one line> (turn <n>)`, where `<rule>` is one of the four names above. The same candidate skipped in several sessions is evidence that it is a real pattern; a later pass counts these lines.
7. Move the session file from `omoikane/raw/inbox/sessions/` to `omoikane/raw/sources/sessions/` with `git mv` when tracked, plain move otherwise. Keep the filename: `session-capture.py` reads it to avoid re-capturing turns already distilled.
8. Run `python omoikane/bin/wiki-index.py` then `python omoikane/bin/wiki-lint.py`. Fix every finding.

A session with nothing worth a page gets no source page: only the log entry (`## [YYYY-MM-DD] distill | session <id8> | nothing kept` with one line saying why, plus the `skipped` lines) and the move in step 7. Report: pages created, pages updated, contradictions filed, candidates skipped, in that order.
