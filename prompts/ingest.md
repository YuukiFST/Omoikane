# Ingest one source

Task: integrate the source file given as argument into the wiki. Done means: source page written, every affected entity and concept page updated, `log.md` appended, source moved to `raw/sources/`, `wiki-lint.py` clean.

Steps:

1. Read the source in full. If it references images under `raw/assets/`, view each one after the text.
2. Read `index.md` and open every existing page the source touches: same entities, same concepts, same claims.
3. Write `wiki/sources/<slug>.md` with the page contract from `AGENTS.md`. Set `dated` to the date the source bears (commit date, publish date, report date), `unknown` when none is found; say in the body how you established it. Content: what the source says, the scope it claims (complete map, partial notes, snapshot of one date), its key claims with dates and numbers exact, what it adds beyond what the wiki already knows. Where the source contradicts itself, record both passages under `## Contradictions` on this page and append to `_review.md`.
4. For each entity or concept in the source: update the existing page, or create one when the wiki has none and the source treats it as central. Cite the new source inline on every claim you add. Add a `## Contradictions` section where the source disagrees with a claim already on the page, and append the disagreement to `_review.md`. Omission counts as disagreement when the source claims to be complete: a source that presents itself as the full list, the whole schema or the thing to read instead of the code, and leaves out what another source asserts, contradicts that source rather than staying silent on it.
5. Append to `log.md`: `## [YYYY-MM-DD] ingest | <title>` followed by the list of pages created and updated.
6. Move the source file from `raw/inbox/` to `raw/sources/` with `git mv` when tracked, plain move otherwise.
7. Run `python bin/wiki-index.py` then `python bin/wiki-lint.py`. Fix every finding.

Report: pages created, pages updated, contradictions filed, in that order. Cite `file:line` for each contradiction.
