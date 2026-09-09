# Answer a question from the wiki

Task: answer the question given as argument using wiki pages, then file the answer so it compounds.

Steps:

1. Read `index.md`. Pick every page whose summary bears on the question. Read them.
2. If the wiki lacks what the question needs, say exactly which pages you read and what is missing. Suggest which source to add. Stop there; do not fill the gap from memory.
3. Write the answer with an inline `[[slug]]` citation on every claim. When the answer describes current state, open it with a cutoff line, "as of YYYY-MM-DD", using the `dated` of the newest source it rests on.
4. File it as `wiki/queries/<YYYY-MM-DD>-<slug>.md` using the page contract, `type: query`, `sources:` listing every page cited.
5. Append to `log.md`: `## [YYYY-MM-DD] query | <question>`.
6. Run `python bin/wiki-index.py` then `python bin/wiki-lint.py`.

Output: the answer, then the path of the filed page.
