# Semantic health check

Task: find what `bin/wiki-lint.py` cannot: wrong or stale meaning, not broken structure. Done means every finding is written to `_review.md` with `file:line` and the log has an entry. You change no wiki page in this pass.

Check, in order:

1. Contradictions: two pages asserting incompatible facts without a `## Contradictions` section.
2. Stale claims: a page cites an older source where a newer source in `wiki/sources/` supersedes it.
3. Missing pages: an entity or concept named on three or more pages with no page of its own.
4. Thin hubs: a page with many inbound links and under ten lines of content.
5. Gaps: questions the wiki raises but no source answers. Name the source type that would close each gap.

Write findings to `_review.md` under `## [YYYY-MM-DD] lint`, one bullet per finding, `file:line` first. Append `## [YYYY-MM-DD] lint | <n> findings` to `log.md`.
