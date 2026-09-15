# Ingest one source

Task: integrate the source file given as argument into the wiki. Done means: source page written, every affected entity and concept page updated, `omoikane/log.md` appended, source moved to `omoikane/raw/sources/`, `wiki-lint.py` clean.

Steps:

1. Read the source in full. If it references images under `omoikane/raw/assets/`, view each one after the text.
2. Read `omoikane/index.md` and open every existing page the source touches: same entities, same concepts, same claims.
3. Write `omoikane/wiki/sources/<slug>.md` with the page contract from `AGENTS.md`. Set `dated` to the date the source bears (commit date, publish date, report date), `unknown` when none is found; say in the body how you established it. Content: what the source says, the scope it claims (complete map, partial notes, snapshot of one date), its key claims with dates and numbers exact, what it adds beyond what the wiki already knows. Where the source contradicts itself, record both passages under `## Contradictions` on this page and append to `omoikane/_review.md`.
4. For each entity or concept in the source: update the existing page, or create one when the wiki has none and the source treats it as central. Cite the new source inline on every claim you add. Add a `## Contradictions` section where the source disagrees with a claim already on the page, and append the disagreement to `omoikane/_review.md`.
   - Omission is disagreement when the source claims completeness. A source that presents itself as the full list, the whole schema, or the thing to read instead of the code, and leaves out what another source asserts, contradicts that source. Record it as a contradiction, not as "not covered".
5. Append to `omoikane/log.md`: `## [YYYY-MM-DD] ingest | <title>` followed by the list of pages created and updated.
6. Move the source file from `omoikane/raw/inbox/` to `omoikane/raw/sources/` with `git mv` when tracked, plain move otherwise.
7. Run `python omoikane/bin/wiki-index.py` then `python omoikane/bin/wiki-lint.py`. Fix every finding.

Report: pages created, pages updated, contradictions filed, in that order. Cite `file:line` for each contradiction.
