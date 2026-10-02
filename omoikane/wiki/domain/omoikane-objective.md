---
title: Omoikane objective
type: domain
summary: Every change to this repo must improve Omoikane at holding, unprompted, the domain knowledge stated while building
tags: [convention, objective]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/2026-10-02-omoikane-objective.md, wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/2026-10-02-omoikane-references.md]
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

The user's first statement of it, in the session that found the misreading (source: [[session-2026-10-01-d4302021]], turn 7):

> O que eu tinha dito para o agente é que o Omoikane é um template baseado no LLM Wiki de Karpathy (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) + https://github.com/poteto/brainmaxxing + https://github.com/akitaonrails/ai-memory o intuito é fazer com que qualquer sistema que for desenvolvido seja feito a partir do Omoikane, com o objetivo de fazer com que de forma autonoma (sem envolvimento do usuario) o agente alimente sua base de conhecimentos com base em informaçoes importantes fornecidas pelo usuario durante o desenvolvimento do sistema.

The company toolkit was the example: "as regras de negocio da empresa, design system dos sistemas e etc são todas escritas nesse toolkit ([redacted]), e eu utilizei como um exemplo pois quero que o Omoikane tambem lembre de informações assim" (turn 7).
In turn 8 the user asked that "todo o desenvolvimento do projeto seja voltado a aperfeiçoamento da ferramenta", and that later agents know the objective.

So: every new system starts from the template; the agent feeds the knowledge base on its own, without the user's involvement, with what the user states while building, business rules, design system and organisation conventions included (source: [[2026-10-02-omoikane-objective]]).
The knowledge lives in Omoikane itself, not in an external base: [[omoikane-holds-its-systems-domain-knowledge-itself]].
When to read the three references and what each gave: [[omoikane-references]] (source: [[2026-10-02-omoikane-references]]).

## Where it applies

Any proposal, issue or PR on this repository: name how it moves the tool towards the objective before making it.
The user restated the criterion in [[session-2026-10-02-1b324082]]: "A partir desta sessão, todo desenvolvimento do repositório deve servir para aperfeiçoar a ferramenta." (turn 3).
Where it is written, and why not in `AGENTS.md`: [[objective-criterion-stays-out-of-agents-md]].
