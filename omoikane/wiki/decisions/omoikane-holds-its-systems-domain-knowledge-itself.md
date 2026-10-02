---
title: Omoikane holds its system's domain knowledge itself
type: decision
summary: Domain knowledge lives in the system's own Omoikane wiki; Omoikane feeds no external organisation base (#55 reverted)
tags: [domain-knowledge, org-knowledge, objective]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/2026-10-02-omoikane-objective.md, wiki/sources/session-2026-10-01-b5b6fb27.md]
code: [AGENTS.md, docs/specs/2026-10-02-realign-to-objective.md]
---

Chosen: Omoikane itself holds the domain knowledge (business rules, design system, organisation conventions) of the system it is the memory of (source: [[2026-10-02-omoikane-objective]]).

Rejected: Omoikane as a feeder of an organisation's external knowledge base, which only proposes candidates to it (source: [[2026-10-02-omoikane-objective]]).

Reason: the company starter kit the user had mentioned was an example of the knowledge to remember, not a system to integrate with. The user: the kit "foi só um exemplo"; Omoikane "não tem nenhuma relação com esse toolkit: não integra, não alimenta, não lê" (source: [[2026-10-02-omoikane-objective]]).
It follows from the objective: [[omoikane-objective]].

## History

- The reversed design: issue #52 on branch `feat/52-org-candidates`, `docs/specs/2026-10-01-org-knowledge.md` and `omoikane/bin/org-candidates.py` (source: [[session-2026-10-01-b5b6fb27]], turn 2), merged as #55, which kept organisation knowledge in an external base (source: [[2026-10-02-omoikane-objective]]).
- The plan in `docs/specs/2026-10-02-realign-to-objective.md` reverts #55 as #61 (source: [[2026-10-02-omoikane-objective]]).
- The kit's name stays out of the public repository: [[company-internal-material-stays-out-of-the-public-repo]].
