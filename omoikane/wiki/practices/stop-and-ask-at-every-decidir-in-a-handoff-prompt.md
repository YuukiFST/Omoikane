---
title: Stop and ask at every DECIDIR in a handoff prompt
type: practice
summary: Mark each choice the user must make DECIDIR in a handoff prompt; at a DECIDIR you receive, stop and ask
tags: [preference, handoff, decisions]
created: 2026-10-02
updated: 2026-10-09
sources: [wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-08-0ac17a0f.md, wiki/sources/session-2026-10-08-21f37812.md, wiki/sources/session-2026-10-08-261b475d.md]
---

## Rule

At every point a prompt marks DECIDIR, stop and ask the user; decide the rest yourself and justify it in the report.
When you write a handoff prompt for another session, mark DECIDIR on each choice that is the user's to make.

## Evidence

- The agent, writing the handoff prompt, recommended registering the scheduled task only after #45 landed: "No prompt abaixo isso ficou marcado como DECIDIR." (source: [[session-2026-09-30-230a182d]], turn 4).
- The user: "Ao enviar este prompt, eu aprovo as recomendações da seção "Aprovado". Onde eu escrevi DECIDIR, pare e me pergunte." (source: [[session-2026-10-01-b5b6fb27]], turn 2).
- The user: "Onde está escrito DECIDIR, pare e me pergunte." (source: [[session-2026-10-01-d4302021]], turn 3).
- The user: "Onde estiver escrito DECIDIR, pare e me pergunte. Para o resto, decida você e justifique no relatório." (source: [[session-2026-10-02-1b324082]], turn 3).
- The agent marked the todo `security-audit-upstream-pr-69` DECIDIR in the handoff file, and its turn-11 handoff prompt says: "Cada ponto marcado **DECIDIR** é uma escolha minha: pare nele, recomende uma opção com o motivo e espere eu aprovar." (source: [[session-2026-10-08-0ac17a0f]], turns 6, 11).
- The user pasted that prompt. The agent stopped: "Parei no **DECIDIR** do passo 2." Its turn-10 handoff prompt marks each choice the same way: "Os itens que dependem de você estão marcados **DECIDIR**" (source: [[session-2026-10-08-21f37812]], turns 2, 10).
- The user pasted that prompt, with the same sentence (source: [[session-2026-10-08-261b475d]], turn 2). The agent asked the DECIDIR points together: "Juntando os fatos dos pontos DECIDIR para perguntar tudo de uma vez." (turn 2).

## Scope

Outside a handoff, a choice that is the user's gets a recommendation: [[recommend-an-option-and-wait-for-the-go-ahead]].
A prompt that grants authority instead overrides the marker for what it names: the turn-7 handoff of [[session-2026-10-02-1b324082]] authorised the next session to "decidir, mudar código, mergear PRs e reativar a tarefa agendada sem me perguntar, dentro das restrições abaixo".
