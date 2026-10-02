---
title: Omoikane objective
type: domain
summary: Every change to this repo must improve Omoikane at holding, unprompted, the domain knowledge stated while building
tags: [convention, objective]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/2026-10-02-omoikane-objective.md]
---

## The rule

Every change to the Omoikane repository must improve the tool towards its objective; a proposed change that does not is said so and not made (source: [[2026-10-02-omoikane-objective]]).
The user: "A partir desta sessão, todo desenvolvimento do repositório deve servir para aperfeiçoar a ferramenta." (source: [[2026-10-02-omoikane-objective]], "The criterion").

## The objective

The user, in the source's "The objective" section:

> O Omoikane é um template baseado em três referências: LLM Wiki de Karpathy, brainmaxxing e ai-memory.
> Todo sistema novo deve nascer a partir do Omoikane.
> O agente deve alimentar a base de conhecimento de forma autônoma, sem envolvimento do usuário, com as informações importantes que o usuário fornece durante o desenvolvimento do sistema.
> Isso inclui conhecimento de domínio: regras de negócio, design system e convenções da organização.

So: every new system starts from the template; the agent feeds the knowledge base on its own, without the user's involvement, with what the user states while building, business rules, design system and organisation conventions included (source: [[2026-10-02-omoikane-objective]]).
The knowledge lives in Omoikane itself, not in an external base: [[omoikane-holds-its-systems-domain-knowledge-itself]].

## Where it applies

Any proposal, issue or PR on this repository: name how it moves the tool towards the objective before making it.
