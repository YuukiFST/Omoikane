---
title: Omoikane holds its system's domain knowledge itself
type: decision
summary: Domain knowledge lives in the system's own Omoikane wiki; Omoikane feeds no external organisation base (#55 reverted)
tags: [domain-knowledge, org-knowledge, objective]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/2026-10-02-omoikane-objective.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-02-a8b45323.md]
code: [AGENTS.md, docs/specs/2026-10-02-realign-to-objective.md]
---

Chosen: Omoikane itself holds the domain knowledge (business rules, design system, organisation conventions) of the system it is the memory of (source: [[2026-10-02-omoikane-objective]]).

Rejected: Omoikane as a feeder of an organisation's external knowledge base, which only proposes candidates to it (source: [[2026-10-02-omoikane-objective]]).

Reason: the company starter kit the user had mentioned was an example of the knowledge to remember, not a system to integrate with. The user: the kit "foi só um exemplo"; Omoikane "não tem nenhuma relação com esse toolkit: não integra, não alimenta, não lê" (source: [[2026-10-02-omoikane-objective]]).
It follows from the objective: [[omoikane-objective]].

## History

- The reversed design: issue #52 on branch `feat/52-org-candidates`, `docs/specs/2026-10-01-org-knowledge.md` and `omoikane/bin/org-candidates.py` (source: [[session-2026-10-01-b5b6fb27]], turn 2), merged as #55, which kept organisation knowledge in an external base (source: [[2026-10-02-omoikane-objective]]).
- The misreading surfaced in [[session-2026-10-01-d4302021]]: checked against the user's objective, the agent found the #55 spec rejecting that Omoikane itself keep this knowledge, and named the gap the other way round: `distill.md` skipped rules stated in prompts as restatements, no page type held a business rule, and the `## Domain` section of `AGENTS.md` waited for the human (turn 7).
- The plan in `docs/specs/2026-10-02-realign-to-objective.md` reverts #55 as #61 (source: [[2026-10-02-omoikane-objective]]).
- [[session-2026-10-02-1b324082]] carried it out: #55 reverted with `git revert -m 1 018e1eb` as PR #68, because the spec's central decision (`:35`) contradicts the objective, the script only served an external base, and `docs/architecture.md:113-116` would keep teaching agents the wrong design (turn 3). The need behind it, a new system inheriting conventions learned before, was left as a gap to redesign from the objective (turn 3).
- The same session gave the knowledge a home inside Omoikane: the `domain` page type (PR #71, see [[wiki-lint]]), distill and ingest prompts that route domain rules (PR #72), and [[new-system-starts-with-an-empty-memory]] (PR #73) (turn 3).
- The need left as a gap, a new system inheriting conventions learned before, was redesigned inside each system's own wiki: [[new-system-inherits-conventions-with-from]] (issue #80, PR #85), whose spec rejects a shared organisation wiki as the #55 design again (source: [[session-2026-10-02-a8b45323]], turn 2).
- The kit's name stays out of the public repository: [[company-internal-material-stays-out-of-the-public-repo]].
