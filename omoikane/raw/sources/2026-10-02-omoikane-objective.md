# Omoikane's objective, and the criterion for work in this repository

Written 2026-10-02 by the agent of an interactive session, from the user's own prompt, for ingest.

## The objective, in the user's words (Portuguese original)

> O Omoikane é um template baseado em três referências: LLM Wiki de Karpathy, brainmaxxing e ai-memory.
> Todo sistema novo deve nascer a partir do Omoikane.
> O agente deve alimentar a base de conhecimento de forma autônoma, sem envolvimento do usuário, com as informações importantes que o usuário fornece durante o desenvolvimento do sistema.
> Isso inclui conhecimento de domínio: regras de negócio, design system e convenções da organização.

English: Omoikane is a template built on Karpathy's LLM Wiki, brainmaxxing and ai-memory. Every new system starts from it. The agent feeds the knowledge base on its own, without the user's involvement, with the important information the user gives while building the system, domain knowledge included: business rules, design system, organisation conventions.

## The criterion

> A partir desta sessão, todo desenvolvimento do repositório deve servir para aperfeiçoar a ferramenta.

Every change to the Omoikane repository must improve the tool towards the objective. A proposed change that does not is said so and not made.

## The misreading it corrects

The user had given, as an example of the knowledge Omoikane must remember, a company's internal starter kit that holds the company's business rules and design system. Earlier sessions read the example as "integrate Omoikane with that kit" and built #55: a spec and `omoikane/bin/org-candidates.py` that keep organisation knowledge in an external base and only propose candidates to it. The user's words: the kit "foi só um exemplo"; Omoikane "não tem nenhuma relação com esse toolkit: não integra, não alimenta, não lê". The kit's name must not appear in this public repository.

Rejected: Omoikane as a feeder of an organisation's external knowledge base. Chosen: Omoikane itself holds the domain knowledge of the system it is the memory of.

## Where it is recorded

- `AGENTS.md`, opening paragraph: the objective, worded to stay true in a system cloned from the template.
- `README.md`, first lines; `docs/architecture.md`, opening.
- `docs/specs/2026-10-02-realign-to-objective.md`: the plan (issues #60 to #66), including the revert of #55 (#61).
