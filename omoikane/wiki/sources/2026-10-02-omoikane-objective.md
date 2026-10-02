---
title: 2026-10-02 Omoikane objective
type: source
summary: The user's statement of Omoikane's objective and the criterion that every repo change must serve it; reverses #55
tags: [objective, convention, domain-knowledge, org-knowledge]
created: 2026-10-02
updated: 2026-10-02
dated: 2026-10-02
sources: []
code: [AGENTS.md, README.md, docs/architecture.md, docs/specs/2026-10-02-realign-to-objective.md]
---

A note written for ingest by the agent of an interactive session, from the user's own prompt.
`dated` comes from its first line: "Written 2026-10-02".
Scope: one statement of the objective and the work criterion, with the user's Portuguese words quoted, plus the misreading it corrects; not a full design.

## Key claims

- The objective, in the user's words: "O Omoikane é um template baseado em três referências: LLM Wiki de Karpathy, brainmaxxing e ai-memory. Todo sistema novo deve nascer a partir do Omoikane. O agente deve alimentar a base de conhecimento de forma autônoma, sem envolvimento do usuário, com as informações importantes que o usuário fornece durante o desenvolvimento do sistema. Isso inclui conhecimento de domínio: regras de negócio, design system e convenções da organização." See [[omoikane-objective]].
- The criterion, from the same prompt: "A partir desta sessão, todo desenvolvimento do repositório deve servir para aperfeiçoar a ferramenta." The note's reading: a proposed change that does not improve the tool towards the objective is said so and not made.
- The misreading: the user had given a company's internal starter kit as an example of knowledge Omoikane must remember; earlier sessions read it as "integrate Omoikane with that kit" and built #55, a spec and `omoikane/bin/org-candidates.py` keeping organisation knowledge in an external base. The user: the kit "foi só um exemplo"; Omoikane "não tem nenhuma relação com esse toolkit: não integra, não alimenta, não lê". See [[omoikane-holds-its-systems-domain-knowledge-itself]].
- The kit's name must not appear in this public repository: [[company-internal-material-stays-out-of-the-public-repo]].
- Where it is recorded: the opening paragraph of `AGENTS.md`, worded to stay true in a system cloned from the template; the first lines of `README.md`; the opening of `docs/architecture.md`; the plan in `docs/specs/2026-10-02-realign-to-objective.md`, issues #60 to #66, including the revert of #55 as #61.

## What it adds

The wiki held the organisation knowledge design of [[session-2026-10-01-b5b6fb27]] (block 4, issue #52, closed by #55) as the current direction.
This note reverses it, with the user's reason, and gives the wiki its first domain page: the objective every later change is measured against.
