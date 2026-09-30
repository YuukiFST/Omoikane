# Synthesize practices across sessions

Task: find what no single `/distill` can see, because each reads one session: a workflow repeated across sessions, a preference the user states again and again, a candidate skipped as a one-off that keeps returning. Done means: every pattern with evidence from two or more sessions is a `practice` page or an update to one, guard and prompt proposals are filed in `omoikane/_review.md`, `omoikane/log.md` is appended, `wiki-lint.py` is clean.

Argument: how many sessions to read, 10 when none is given.

A practice is one of:

- procedure: steps an agent repeats for one kind of task in this repository, in an order that matters. Example: "Run the headless eval in a throwaway clone with `OMOIKANE_NO_CAPTURE=1` before opening a PR that changes a prompt."
- preference: a way of working the user stated, quoted in the user's own words with the session and turn.

Keep a pattern only when all of these hold:

- Two or more sessions show it, each cited `(source: [[session-<date>-<id8>]], turn <n>)`. Two parts of one session are one session. A pattern from one session is distill's job, not yours; `wiki-lint.py` fails a practice page citing fewer than two sessions.
- It is imperative and falsifiable: you could catch an agent breaking it.
- It is not already in `AGENTS.md`, an Omoikane prompt, a practice page, or enforced by a check. Update the existing practice page with the new evidence instead of writing a second one.
- The sessions did the same thing for the same reason. The same command run for two unrelated reasons is a coincidence.

Route each pattern like `omoikane/prompts/distill.md` routes a lesson: a check could catch it, propose a `guard`; it is about how an Omoikane operation runs, propose a `prompt` fix; work nobody did, a `todo`. You never apply a guard or prompt proposal. A guard proposal does not replace the practice page: until the guard lands, the page is the only record.

Steps:

1. List `omoikane/wiki/sources/session-*.md` and read the newest ones, as many as the argument says, by `dated`. Open the raw capture under `omoikane/raw/sources/sessions/` when you need a turn's exact words.
2. Read `omoikane/log.md`. Group the `- routed (...)` and `- skipped (...)` lines by slug. A slug in two or more distill entries is a candidate however it was judged the first time: a `missing-env` or `one-off` that recurs is not an accident, so judge it again with every session in view.
3. Read `AGENTS.md`, `omoikane/index.md` and every practice page, and grep `omoikane/log.md` for `dropped` lines of earlier synthesize runs: a slug dropped before comes back only with a session newer than that run.
4. For each kept pattern, write or update `omoikane/wiki/practices/<slug>.md` with the page contract, `type: practice`. `summary`: the rule as one imperative line. `sources`: every session page cited. Body: `## Rule` (the rule, imperative, one or two lines), `## Evidence` (one bullet per session: what it did or what the user said, with the turn), `## Scope` (where the rule stops applying, when a session shows it).
5. File guard, prompt and todo proposals in `omoikane/_review.md` in the format of `omoikane/prompts/distill.md` step 6, under the heading `## [YYYY-MM-DD] synthesize`, with `(synthesize)` in place of the session reference.
6. Append to `omoikane/log.md`: `## [YYYY-MM-DD] synthesize | <n> sessions` followed by the pages created and updated, the proposals filed as `- routed (<guard|prompt|todo>) <slug>: <one line>`, and one line per candidate you dropped: `- dropped (<one-session|coincidence|known|not-imperative>) <slug>: <one line>`.
7. Run `python omoikane/bin/wiki-index.py` then `python omoikane/bin/wiki-lint.py`. Fix every finding.

Write only what the sessions show. Copy commands, paths and the user's words exactly. When no pattern clears the bar, write no page: the log entry with the `dropped` lines is the result. Report: pages created, pages updated, proposals filed, candidates dropped, in that order.
