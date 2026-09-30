# Semantic health check

Task: find what `omoikane/bin/wiki-lint.py` cannot: wrong or stale meaning, not broken structure. Done means every finding is written to `omoikane/_review.md` with `file:line` and the log has an entry. You change no wiki page in this pass.

Check, in order:

1. Contradictions: two pages asserting incompatible facts without a `## Contradictions` section. A source that claims completeness and omits what another source asserts counts.
2. Stale claims: a page cites a source whose `dated` is older than another source in `omoikane/wiki/sources/` that supersedes it.
   Also run `python omoikane/bin/wiki-lint.py`. Each `warning:` line names a page whose `code:` changed after its `updated` date. Read the page and the current code, and file a finding only when a claim no longer holds.
3. Unguarded gotchas: each `wiki-lint.py` `warning:` naming a gotcha with `guard: none`. Grep `omoikane/log.md` for `unguarded <slug>`: filed before, skip it, whether the human applied or rejected it. Otherwise propose the guard as a `- [ ] guard` entry in the format of `omoikane/prompts/distill.md` step 6, with `(lint)` in place of the session reference, or file one bullet saying why no check can catch this mistake.
4. Missing pages: an entity or concept named on three or more pages with no page of its own.
5. Thin hubs: a page with many inbound links and under ten lines of content.
6. Gaps: questions the wiki raises but no source answers. Name the source type that would close each gap.

Write findings to `omoikane/_review.md` under `## [YYYY-MM-DD] lint`, one bullet per finding, `file:line` first. Append `## [YYYY-MM-DD] lint | <n> findings` to `omoikane/log.md`, with one line `- unguarded <slug>` per gotcha filed in check 3.
