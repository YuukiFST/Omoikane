---
title: pstack
type: entity
summary: Cursor plugin of agent skills, an Omoikane reference since 2026-10-06; every skill judged in two review rounds
tags: [reference, agent-memory, pstack, brainmaxxing]
created: 2026-10-06
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-05-1de79b19.md, wiki/sources/2026-10-06-pstack-is-an-omoikane-reference.md, wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/2026-10-06-pstack-skills-review-round-2.md, wiki/sources/session-2026-10-06-fd3ff955.md, wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/2026-10-07-omoikane-objective-widens-to-a-work-toolkit.md]
---

pstack lives at https://github.com/cursor/plugins/tree/main/pstack (source: [[session-2026-10-05-1de79b19]], turn 1).
The agent read it as the successor of brainmaxxing, which the `README.md` names as one of Omoikane's references (turn 1).
It read the skills `recall`, `reflect`, `correct`, `why`, `principle-encode-lessons-in-structure` and the `poteto-mode` session-pickup playbook (turn 1).

## Reference status

On 2026-10-06 the user made pstack an Omoikane reference in its own right, not only through brainmaxxing: "Sim, pstack deve ser utilizado como referência https://github.com/cursor/plugins/tree/main/pstack existe muita conteudo valioso nessas skills" (source: [[2026-10-06-pstack-is-an-omoikane-reference]]).
The rule on [[omoikane-references]] now covers its skills.
The user says the skills not read yet hold valuable content too (source: [[2026-10-06-pstack-is-an-omoikane-reference]]).
Round 2 read them on 2026-10-06, see below.
The user said it in [[session-2026-10-06-61eabe29]] (turn 9), then asked for a prompt for another session to read the other skills and bring "apenas o que pode agregar o Omoikane" (turn 10).
That prompt makes the task read only, skips the six skills already read, judges each skill against [[omoikane-objective]] and [[omoikane-references]], and asks for issue drafts (turn 10).

## What Omoikane already has

The agent's mapping in its final report (turn 3):
- `/reflect` matches `/distill` with its guard, prompt, page and todo routing.
- `/automate-me` matches `/synthesize`.
- `principle-encode-lessons-in-structure`: Omoikane already prefers a guard to a page.
- `show-me-your-work` and `pause-safely`: session capture and inbox notes already cover them.

Round 2 narrows the `show-me-your-work` match: its audit of the log against the transcript has no counterpart, since no check finds a quote missing from the capture it cites (source: [[2026-10-06-pstack-skills-review-round-2]], proposal 4).

## Round 2 review

On 2026-10-06 an agent read every skill not read in round 1, at pstack commit `df58112`, and gave each a verdict (source: [[2026-10-06-pstack-skills-review-round-2]]).
It reads only each `SKILL.md`, not the `references/` files, the benny templates or `docs/guide/`.
- Proposed: four gaps, from benny's file ownership, the two verification skills, `principle-prove-it-works` and `show-me-your-work`.
- Already in Omoikane: `automate-me`, the `maintain-verification-skill` drift check, `tdd`, `technical-writing`, `unslop`, `interrogate`, five principles and benny's fail-closed rule.
- Rejected: `principle-never-block-on-the-human`, `principle-separate-before-serializing-shared-state`, `principle-explain-the-number` (uncertain), and every skill or principle with "no memory link".

The session that wrote the note is [[session-2026-10-06-fd3ff955]].
Asked for a recommendation, its agent advised opening proposals 1 to 3, holding proposal 4 until PR #92 was decided, and opening an issue for the capture's prompt cut, which pstack did not suggest (turn 3).
The user asked for a handoff prompt with those four issues, which became #103 to #106 (turn 4).

The "no memory link" rejections were reopened on 2026-10-07, when the user made Omoikane a software-development toolkit (issue #111).
`docs/specs/2026-10-07-software-toolkit.md`: "the verdicts about memory gaps stand".
Issue #111 vendored `how`, `blast-radius`, `figure-it-out`, `create-verification-skill`, `maintain-verification-skill`, `interrogate` and `correct`, and turned `poteto-mode` into `omoikane-mode` (commits `8b21a90`, `64023b3`, `fe01af5`).

## Issue #111

The session that did it is [[session-2026-10-07-062e80af]]; PRs #112 to #118 merged on 2026-10-07.
The user: "eu gosto do pstack, gosto de habilitar poteto-mode e deixar o agente seguir utilizando a melhor skill para tal tarefa, quero que no omoikane tenha isso tambem" (turn 5).
The user excluded `tdd` and `unslop` (turn 1).
The user believed pstack is tied to one harness: "acredito que o pstack é para o grok bot ou cursor em especifico" (source: [[2026-10-07-omoikane-objective-widens-to-a-work-toolkit]]).
The agent's diagnosis found that true for only part of it (turn 3):
- Tied to Cursor: the flow skills that use per-call `model` on `Task`, Custom Modes, `/loop`, `~/.cursor/rules/pstack-models.mdc` and transcripts under `~/.cursor/projects/`.
- Grok Bot or Slack only: `make-bot-ui` and the benny pack.
- Agnostic: the 24 `principle-*` skills, `blast-radius`, `correct`, `benchmark-checklist`, `technical-writing` and the two verification skills, where only the `.cursor/skills/` path changes.
- Portable with one change: `interrogate`, `how` and `arena` run on one model with "um revisor por lente" in place of one reviewer per model.

What came of it: [[omoikane-mode-routes-each-task-to-a-playbook]] and [[every-system-ships-the-development-skills]].

## What it gave

- `/correct`: a guard's error names what to use instead, proven on a real past mistake: [[proposed-guards-name-the-fix-and-prefer-lint-or-test]] (issue #98, PR #99, merged 2026-10-06; source: [[2026-10-06-pstack-is-an-omoikane-reference]]).
- `/why` and `/recall`: read source control and PRs before guessing a reason: [[ask-searches-origin-main-history-before-asking-for-a-source]] (issue #97, PR #100, merged 2026-10-06 as `0118646`).
- benny's file ownership: a system takes template updates and keeps its own memory, `omoikane/bin/update-from-template.py` (issue #105, PR #108, `93c2dea`; source: [[2026-10-06-pstack-skills-review-round-2]], proposal 1).
- The verification skills' health check: a failed capture goes to `omoikane/.capture-errors` and the session brief names it (issue #103, PR #107, `872319e`; proposal 2).
- `create-verification-skill` with `principle-prove-it-works`: `wiki-lint.py` checks that every diff in `_review.md` applies (issue #106, PR #110, `4000448`; proposal 3).
- `show-me-your-work`: the quote audit has no issue yet (proposal 4).
