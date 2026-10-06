---
title: 2026-10-02 Omoikane references
type: source
summary: The user's rule to consult LLM Wiki, brainmaxxing and ai-memory before changing Omoikane, and what each gave
tags: [references, objective]
created: 2026-10-02
updated: 2026-10-02
dated: 2026-10-02
sources: []
code: [README.md, docs/architecture.md, omoikane/bin/bootstrap.py, docs/specs/2026-10-02-cross-system-knowledge.md]
---

A note written for ingest by the agent of an interactive session, from the user's own prompts.
`dated` comes from its first line: "Written 2026-10-02".
Scope: the three reference projects, the rule for when to read them, who the rule is for, and a list of what Omoikane took from each "so far"; not a full comparison of the projects.

## Key claims

- The rule: before changing how Omoikane captures, distills, stores or loads knowledge (`omoikane/prompts/`, `omoikane/bin/`, the page contract, the hooks), read the reference covering the same problem, say what it does there, and adopt, adapt or reject it with a reason. See [[omoikane-references]].
- The references: Karpathy's LLM Wiki (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), brainmaxxing (https://github.com/poteto/brainmaxxing), ai-memory (https://github.com/akitaonrails/ai-memory).
- Audience: only people and agents improving Omoikane in this repository, not users or agents of a system built from the template. The user: "Essas referencias não serão utilizadas por quem vai utilizar o sistema em si, a ferramenta Omoikane, e sim para nós que estamos aprimorando o Omoikane".
- Hence the rule stays out of the fixed part of `AGENTS.md`, and its page is tagged neither `convention` nor `design-system`, the tags `omoikane/bin/new-system.py --from` copies into another system.
- What was taken from each, with where it lives today: listed on [[omoikane-references]].
- Gap it closes: the links lived only in `README.md`, which no session loads, and in a spec; no page told an agent when to read the references.

## What it adds

The wiki named the three references only as the base of [[omoikane-objective]].
This note adds when an agent must read them, and maps each borrowed mechanism to its reference and its place in the repository.
