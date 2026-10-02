# The three reference projects, for whoever improves Omoikane

Written 2026-10-02 by the agent of an interactive session, from the user's own prompts, for ingest.

## The rule

Before changing how Omoikane captures, distills, stores or loads knowledge (`omoikane/prompts/`, `omoikane/bin/`, the page contract, the hooks), read the reference that covers the same problem and say what it does there; adopt, adapt or reject it with a reason.

- Karpathy's LLM Wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- brainmaxxing: https://github.com/poteto/brainmaxxing
- ai-memory: https://github.com/akitaonrails/ai-memory

## Who it is for

Only the people and agents improving Omoikane itself, in this repository.
Not the users of a system built from the template, nor that system's agents: their sessions build the system, not the tool.
That is why the rule is not written into the fixed part of `AGENTS.md`, which every cloned system inherits; the wiki and the `AGENTS.md` rules block are emptied by `omoikane/bin/new-system.py`, so a rule kept there stays in this repository.
For the same reason its page is tagged neither `convention` nor `design-system`: `new-system.py --from` copies pages with those tags into another system.

The user, in Portuguese:

> Quero saber se está registrado para os agentes os projetos que iremos pegar como referencia, deve estar gravado para o agente sempre os analisar quando necessario

> Essas referencias não serão utilizadas por quem vai utilizar o sistema em si, a ferramenta Omoikane, e sim para nós que estamos aprimorando o Omoikane

## What Omoikane took from each, so far

- LLM Wiki: the three layers (raw sources, wiki, schema), the ingest, query and lint operations, `index.md` and the append-only `log.md` (`docs/architecture.md`, opening).
- brainmaxxing: routing what a session learned to the right kind of page (`reflect`); pruning with an early exit under three findings (`meditate`, `docs/architecture.md`); the durability test behind distill's `task-only` reject ("would I include this in a prompt for a different task?"); seeding from an existing project (`/ruminate`, `omoikane/bin/bootstrap.py`).
- ai-memory: a practice needs evidence from two or more sessions; a managed rules block with a cap; memory of rejected proposals; sanitising at the privacy boundary before storing (`session-capture.py` redaction); bootstrap from a project's docs and history (`omoikane/bin/bootstrap.py`); its `scope: global` was considered and not adopted (`docs/specs/2026-10-02-cross-system-knowledge.md`).

## What was missing before this note

The links lived only in `README.md` (no session loads it) and in a spec; no page told an agent when to read the references or what each one contributed.
