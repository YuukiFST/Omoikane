---
title: Proposals that add always-loaded text name what leaves
type: domain
summary: A proposal that adds text every session loads (AGENTS.md, the session brief) must name the text it removes to make room
tags: [convention, context-budget]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-fd3ff955.md]
code: [AGENTS.md, omoikane/bin/context-budget.py]
---

## Rule

A proposal that adds text a session always loads must say which text leaves to make room for it (source: [[session-2026-10-06-fd3ff955]], turn 2).
The user, in the prompt for the pstack review: "Orçamento de contexto apertado: o `AGENTS.md` está em cerca de 2796 de 2800 tokens no pior caso, e o brief de sessão tem limite de 4000. Rode `python omoikane/bin/context-budget.py`. Qualquer proposta que acrescente texto sempre carregado precisa dizer o que sai para abrir espaço." (turn 2).

## Where it applies

- `AGENTS.md`, the session brief and anything else `omoikane/bin/context-budget.py` measures.
- Issue drafts, review proposals and PRs: run `python omoikane/bin/context-budget.py` before and after, and name the removal in the proposal.

The `context-budget.py` comment already says text added to `AGENTS.md` "must now pay for itself with a removal"; the user's statement covers every always-loaded text, not only `AGENTS.md`.
The handoff prompt the session wrote carried the rule as "Rode `python omoikane/bin/context-budget.py` antes e depois de cada PR. Nenhum item deve mudar o `AGENTS.md` nem o page contract." (turn 4).

Related: [[wiki-rules]], which holds the budget figures.
