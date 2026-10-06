---
title: Omoikane references
type: domain
summary: Before changing how Omoikane captures, distills, stores or loads knowledge, consult the matching reference project
tags: [references, objective]
created: 2026-10-02
updated: 2026-10-05
sources: [wiki/sources/2026-10-02-omoikane-references.md, wiki/sources/session-2026-10-02-680ff986.md]
code: [README.md, docs/architecture.md, omoikane/bin/bootstrap.py]
---

## The rule

Before changing how Omoikane captures, distills, stores or loads knowledge (`omoikane/prompts/`, `omoikane/bin/`, the page contract, the hooks), read the reference that covers the same problem and say what it does there; adopt, adapt or reject it with a reason (source: [[2026-10-02-omoikane-references]], "The rule").
The user: "deve estar gravado para o agente sempre os analisar quando necessario" (source: [[session-2026-10-02-680ff986]], turn 3).

- Karpathy's LLM Wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- brainmaxxing: https://github.com/poteto/brainmaxxing
- ai-memory: https://github.com/akitaonrails/ai-memory

They are the three references Omoikane is built on ([[omoikane-objective]]).

## Who it is for

Only people and agents improving Omoikane in this repository; not users or agents of a system built from the template (source: [[2026-10-02-omoikane-references]]).
The user: "Essas referencias não serão utilizadas por quem vai utilizar o sistema em si, a ferramenta Omoikane, e sim para nós que estamos aprimorando o Omoikane" (source: [[session-2026-10-02-680ff986]], turn 4).
So the rule is kept out of the fixed part of `AGENTS.md`: a `## References` section there was proposed and rejected on that ground, since every cloned system inherits the file (source: [[session-2026-10-02-680ff986]], turns 3, 4).
This page also carries neither the `convention` nor the `design-system` tag, which `new-system.py --from` copies into another system ([[new-system-starts-with-an-empty-memory]]).

## What Omoikane took from each, so far

All from [[2026-10-02-omoikane-references]], "What Omoikane took from each, so far".

- LLM Wiki: the three layers (raw sources, wiki, schema), the ingest, query and lint operations, `index.md` and the append-only `log.md` (`docs/architecture.md`, opening).
- brainmaxxing: routing what a session learned to the right kind of page (`reflect`); pruning with an early exit under three findings (`meditate`, `docs/architecture.md`); the durability test behind distill's `task-only` reject; seeding from an existing project (`/ruminate`, `omoikane/bin/bootstrap.py`).
- ai-memory: a practice needs evidence from two or more sessions; a managed rules block with a cap ([[wiki-rules]]); memory of rejected proposals; sanitising before storing ([[redact-captures-when-they-are-written]]); bootstrap from a project's docs and history (`omoikane/bin/bootstrap.py`). Its `scope: global` was considered and not adopted (`docs/specs/2026-10-02-cross-system-knowledge.md`).
