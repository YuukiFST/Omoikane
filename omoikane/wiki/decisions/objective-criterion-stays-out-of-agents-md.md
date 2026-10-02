---
title: Objective criterion stays out of AGENTS.md
type: decision
summary: AGENTS.md states what a system's memory must hold; the "improve the tool" criterion lives in docs and the wiki
tags: [objective, agents-md, template]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-10-02-1b324082.md]
code: [AGENTS.md, docs/architecture.md, docs/specs/2026-10-02-realign-to-objective.md]
---

Chosen: the opening of `AGENTS.md` states the objective as what the memory must hold, true in any system cloned from the template; the criterion that every change to this repository must improve the tool goes in `docs/architecture.md`, `docs/specs/2026-10-02-realign-to-objective.md` and the wiki page [[omoikane-objective]] (source: [[session-2026-10-02-1b324082]], turns 3, 6).

Rejected: the criterion in `AGENTS.md`. Every cloned system inherits that file, and there the rule would be wrong (turns 3, 6).

Reason for `AGENTS.md` at all: it is the one file every session of every harness loads (turn 6).
The opening paid for itself: it replaced the "Two ways" block and the `## Domain` placeholder, and the file ended 15 tokens smaller (turns 3, 6).
The review of PR #67 asked that `AGENTS.md` describe today's mechanism (`/distill`, `/ingest`) without claiming domain capture it did not yet do; fixed in aa8bdcb (turn 3).
