---
title: New system inherits conventions with --from
type: decision
summary: new-system.py --from copies another system's convention and design-system domain pages; nothing else, no sync
tags: [new-system, domain-knowledge, template, objective]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-10-02-a8b45323.md]
code: [omoikane/bin/new-system.py, tests/test_new_system.py, docs/specs/2026-10-02-cross-system-knowledge.md]
---

Chosen: `python omoikane/bin/new-system.py --from <checkout of another system>` empties the memory as [[new-system-starts-with-an-empty-memory]] does, then copies the other system's `domain` pages tagged `convention` or `design-system`, each citing one source page `wiki/sources/inherited-from-<system>.md` that names the commit they came from (issue #80, PR #85) (source: [[session-2026-10-02-a8b45323]], turn 2; `docs/specs/2026-10-02-cross-system-knowledge.md`).
The spec was written before the code, then the tests red, then the script (turn 2).

Reason: an organisation's conventions and design system, once learned in one system, were lost with the reset, so the user had to restate them in every system, the failure the objective names ([[omoikane-objective]]; `docs/specs/2026-10-02-cross-system-knowledge.md`).

Left behind (spec): `business-rule` domain pages, which belong to one system; decisions, gotchas and entities, whose `code:` paths do not exist there; practices, whose session pages stay behind; pages marked `Disputed:` or `prune:`.
No sync: a convention changed later in the other system does not follow; the next session that states it updates the page through `/distill`.

Rejected (spec): a shared organisation wiki mounted or synced into every system, the reverted #55 design ([[omoikane-holds-its-systems-domain-knowledge-itself]]); copying every page; a `scope: global` key as ai-memory has, since Omoikane has no store outside the repository ([[omoikane-references]]).

The review of #85 found, and the session fixed: read and render every page before the reset deletes anything, skip `Disputed:` and `prune:` pages, ASCII slugs, keep a link's alias when the link becomes plain text, match tags without case (turn 2).
