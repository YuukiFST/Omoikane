# Ingest one source

Task: integrate the source file given as argument into the wiki. Done means: source page written, every affected entity and concept page updated, `log.md` appended, source moved to `raw/sources/`, `wiki-lint.py` clean.

Steps:

1. Read the source in full. If it references images under `raw/assets/`, view each one after the text.
2. Read `index.md` and open every existing page the source touches: same entities, same concepts, same claims.
3. Write `wiki/sources/<slug>.md` with the page contract from `AGENTS.md`. Content: what the source says, its key claims with dates and numbers exact, what it adds beyond what the wiki already knows.
4. For each entity or concept in the source: update the existing page, or create one when the wiki has none and the source treats it as central. Cite the new source inline on every claim you add. Add a `## Contradictions` section where the source disagrees with a claim already on the page, and append the disagreement to `_review.md`.
5. Append to `log.md`: `## [YYYY-MM-DD] ingest | <title>` followed by the list of pages created and updated.
6. Move the source file from `raw/inbox/` to `raw/sources/` with `git mv` when tracked, plain move otherwise.
7. Run `python bin/wiki-index.py` then `python bin/wiki-lint.py`. Fix every finding.

Report: pages created, pages updated, contradictions filed, in that order. Cite `file:line` for each contradiction.
