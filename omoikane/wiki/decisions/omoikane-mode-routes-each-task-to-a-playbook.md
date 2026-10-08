---
title: omoikane-mode routes each task to a playbook
type: decision
summary: omoikane-mode, poteto-mode for one model, routes each task to a playbook, skills and principles; the brief reminds it
tags: [skills, omoikane-mode, pstack, session-context]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/commits-2026-10-06-to-2026-10-07.md]
code: [.claude/skills/omoikane-mode/SKILL.md, omoikane/bin/session-context.py, omoikane/skills.md, docs/specs/2026-10-07-software-toolkit.md]
---

## The request

The user, in turn 5 of [[session-2026-10-07-062e80af]]: "eu gosto do pstack, gosto de habilitar poteto-mode e deixar o agente seguir utilizando a melhor skill para tal tarefa, quero que no omoikane tenha isso tambem".

## Chosen

`.claude/skills/omoikane-mode/` is the counterpart of pstack's `poteto-mode` (source: [[session-2026-10-07-062e80af]], turn 5; PR #117).

- The user turns it on with `/omoikane-mode` in Claude Code and OpenCode, `/skill:omoikane-mode` in Pi; it holds to the end of the session (turn 5).
- It indexes the 24 pstack principles under `references/principles/`, the user's 9 adapted versions replacing pstack's (`omoikane/skills.md`).
  It is the one principles router: the agent's turn-5 note says "é o roteador único que você escolheu, sem skill `principles` separada".
- It carries the `poteto-mode` playbooks adapted to one model; session pickup and pause safely use Omoikane's memory, and a new playbook routes to `security-audit` (turn 5).
- The session brief ends with "Nontrivial software task: load the omoikane-mode skill first." (`omoikane/bin/session-context.py`).
  Reason: "o campo `reminder:` do Cursor não existe nas três harnesses" (turn 5); commit `0c3f4cd` adds the line, and the worst-case brief stays at 3,792 of 4,000 tokens. See [[session-context]].
- The skill is model-invocable, so an agent loads it on its own too (`omoikane/skills.md`, omoikane-mode row).
- A coding session under the mode reads `omoikane/index.md`, the wiki pages and git history directly, and does not run `/ask` (source: [[commits-2026-10-06-to-2026-10-07]], `15cbeb5`).
  It tells the user to run `/wrap-up` in a fresh session. Reason: both write under `omoikane/wiki/`.
- The mode pauses before it merges any PR the user did not authorize, not only a merge to `main`. An autonomous run stops at merge-ready, so stacked PRs never merge unasked (`15cbeb5`).

## Rejected

- Always on through `AGENTS.md`: the file has no budget room, and the user turns the mode on, as with `poteto-mode` (`docs/specs/2026-10-07-software-toolkit.md`, "omoikane-mode").
- The playbooks orchestrate, autopilot-full and autopilot-stack: they depend on Cursor cloud agents (turn 5).
- Per-role model lines: one model runs everything, and in Pi, which has no subagents, fan-out steps run one after another (`omoikane/skills.md`).

## Order

`figure-it-out` (PR #116) reads the principles of `omoikane-mode`, so #117 had to merge before #116 (turn 11).
The skill set it routes to: [[every-system-ships-the-development-skills]]. Where it comes from: [[pstack]].
