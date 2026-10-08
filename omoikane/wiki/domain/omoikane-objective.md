---
title: Omoikane objective
type: domain
summary: Every change must improve Omoikane as a toolkit for software development: domain memory, dev skills, omoikane-mode
tags: [convention, objective]
created: 2026-10-02
updated: 2026-10-07
sources: [wiki/sources/2026-10-02-omoikane-objective.md, wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/2026-10-02-omoikane-references.md, wiki/sources/2026-10-02-ste-and-oversight-posts.md, wiki/sources/2026-10-06-pstack-is-an-omoikane-reference.md, wiki/sources/session-2026-10-07-062e80af.md]
---

## The objective since 2026-10-07

Omoikane is a toolkit for software development: every new software system starts from it with its own memory, a set of development skills and `omoikane-mode`, which picks the best skill for each task (source: [[session-2026-10-07-062e80af]], turns 1, 5).
Generic research is no longer a use.
The memory part below does not change: the agent still feeds the wiki on its own from what the user states.

The user first widened the objective (turn 1):

> O objetivo do Omoikane vai ser mais amplo, quero pegar como referência o https://github.com/cursor/plugins/tree/main/pstack e trazer para o Omoikane, ele vai ser mais que um sistema de memória, vai ser uma ferramenta de trabalho, um toolkit para iniciar o trabalho encima dele, e caso o usuario for utilizar para desenvolvimento de software e não apenas pesquisas genericas e universais, ele vai ter diversas skills.

Then made it narrower, in the same session (turn 5):

> Eu quero deixar mais preciso na verdade o objetivo do Omoikane, não vai ser para pesquisas genericas, vai ser para desenvolvimento de software.

In the same turn the user asked for a counterpart of pstack's `poteto-mode`: [[omoikane-mode-routes-each-task-to-a-playbook]].
The skills every system ships, and the ones the user excluded ("Ignore skills como TDD e UNSLOP", turn 1): [[every-system-ships-the-development-skills]].
The new references: [[omoikane-references]].
`README.md`, `docs/architecture.md` and the opening of `AGENTS.md` state the new objective since PR #113 (turn 6).

## The rule

Every change to the Omoikane repository must improve the tool towards its objective; a proposed change that does not is said so and not made (source: [[2026-10-02-omoikane-objective]]).
The user: "A partir desta sessão, todo desenvolvimento do repositório deve servir para aperfeiçoar a ferramenta." (source: [[2026-10-02-omoikane-objective]], "The criterion").

## The memory part of the objective

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
On 2026-10-06 the user added pstack as a fourth reference, listed on the same page (source: [[2026-10-06-pstack-is-an-omoikane-reference]]).
A business term's meaning is part of that knowledge; a [[domain-glossary]] to hold it is proposed, not built (source: [[2026-10-02-ste-and-oversight-posts]]).

## Where it applies

Any proposal, issue or PR on this repository: name how it moves the tool towards the objective before making it.
The user restated the criterion in [[session-2026-10-02-1b324082]]: "A partir desta sessão, todo desenvolvimento do repositório deve servir para aperfeiçoar a ferramenta." (turn 3).
Where it is written, and why not in `AGENTS.md`: [[objective-criterion-stays-out-of-agents-md]].

## History

- 2026-10-02 to 2026-10-07: "Every change to this repo must improve Omoikane at holding, unprompted, the domain knowledge stated while building" (source: [[2026-10-02-omoikane-objective]]). The memory was the whole objective, and `README.md` gave generic research as a second use (`docs/specs/2026-10-07-software-toolkit.md`).
- 2026-10-07: the user replaced it with the software-development toolkit above (source: [[session-2026-10-07-062e80af]], turns 1, 5).
