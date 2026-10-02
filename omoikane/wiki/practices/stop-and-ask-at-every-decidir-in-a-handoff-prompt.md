---
title: Stop and ask at every DECIDIR in a handoff prompt
type: practice
summary: Mark each choice the user must make DECIDIR in a handoff prompt; at a DECIDIR you receive, stop and ask
tags: [preference, handoff, decisions]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-1b324082.md]
---

## Rule

At every point a prompt marks DECIDIR, stop and ask the user; decide the rest yourself and justify it in the report.
When you write a handoff prompt for another session, mark DECIDIR on each choice that is the user's to make.

## Evidence

- The agent, writing the handoff prompt, recommended registering the scheduled task only after #45 landed: "No prompt abaixo isso ficou marcado como DECIDIR." (source: [[session-2026-09-30-230a182d]], turn 4).
- The user: "Ao enviar este prompt, eu aprovo as recomendações da seção "Aprovado". Onde eu escrevi DECIDIR, pare e me pergunte." (source: [[session-2026-10-01-b5b6fb27]], turn 2).
- The user: "Onde está escrito DECIDIR, pare e me pergunte." (source: [[session-2026-10-01-d4302021]], turn 3).
- The user: "Onde estiver escrito DECIDIR, pare e me pergunte. Para o resto, decida você e justifique no relatório." (source: [[session-2026-10-02-1b324082]], turn 3).

## Scope

A prompt that grants authority instead overrides the marker for what it names: the turn-7 handoff of [[session-2026-10-02-1b324082]] authorised the next session to "decidir, mudar código, mergear PRs e reativar a tarefa agendada sem me perguntar, dentro das restrições abaixo".
