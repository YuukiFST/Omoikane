---
title: Recommend an option and wait for the go-ahead
type: practice
summary: When a choice is the user's, recommend one option with its reason; act on it only after the user approves
tags: [preference, decisions, handoff]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-02-680ff986.md, wiki/sources/session-2026-10-06-180e52eb.md, wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/session-2026-10-06-fd3ff955.md, wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/session-2026-10-07-9e3fae7e.md]
---

## Rule

When a choice is the user's, give one recommendation and the reason for it.
Act on it only after the user approves; the user's usual answer is "prossiga de acordo com a sua recomendação".

## Evidence

- The user: "Me envie um prompt para eu jogar em outra sessão para que o agente prossiga com tudo que voce recomenda, todas suas propostas" (source: [[session-2026-10-02-680ff986]], turn 5).
- The agent ended its report with "**Pendências que dependem de você:**", the merge of PR #102 first. The user answered "prossiga de acordo com a sua recomendação", and only then the agent merged #102 and closed #96 (source: [[session-2026-10-06-180e52eb]], turns 7, 8). Next the user asked for a prompt "para prosseguir com o restante de acordo com a sua recomendação" (turn 9).
- The handoff the user pasted asked: "Leia o PR e me recomende fechar ou manter, com o motivo. Não feche sem eu confirmar." The agent answered "**#92: recomendo fechar.**" with the reason, and closed #92 after the user approved (source: [[session-2026-10-06-61eabe29]], turns 2, 6).
- The user: "Qual a sua recomendação ?" The agent: "Minha recomendação é abrir três agora (#1, #2 e #3), segurar a #4 e abrir a issue do corte de prompts junto." (source: [[session-2026-10-06-fd3ff955]], turn 3).
- After the agent's account of the revised spec, the user: "prossiga com a sua recomendação, da melhor forma possivel, escolha as alternativas mais inteligente possiveis" (source: [[session-2026-10-07-062e80af]], turn 6).
- The agent checked CI on seven PRs and stopped: "Ainda não fiz nenhum merge: preciso da sua autorização para começar." It merged them after "prossiga de acordo com a sua recomendação" (source: [[session-2026-10-07-9e3fae7e]], turns 2, 3). The user answered the same way to the next report (turn 4).

## Scope

The approval covers what the recommendation named: in [[session-2026-10-07-9e3fae7e]] it covered seven merges (turn 3).
It does not override the permission classifier: after "prossiga com a sua recomendação" the classifier still denied the merge of #112 as "[Merge Without Review]", and the agent left the merge to the user (source: [[session-2026-10-07-062e80af]], turn 6).
For a destructive step, ask in the recommendation itself: "Nada destrutivo sem eu confirmar." (source: [[session-2026-10-06-61eabe29]], turn 2).
A prompt marked DECIDIR asks the same of a handoff: [[stop-and-ask-at-every-decidir-in-a-handoff-prompt]].
