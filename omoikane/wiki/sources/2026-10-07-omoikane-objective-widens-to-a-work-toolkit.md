---
title: 2026-10-07 Omoikane objective widens to a work toolkit
type: source
summary: The user's two statements that make Omoikane a software-development toolkit, and the skill sources at their commits
tags: [objective, references, skills, pstack]
created: 2026-10-07
updated: 2026-10-07
dated: 2026-10-07
sources: []
code: [README.md, docs/architecture.md, docs/specs/2026-10-07-software-toolkit.md]
---

A note written for ingest by the agent of [[session-2026-10-07-062e80af]] (turn 3), raw file `omoikane/raw/sources/2026-10-07-omoikane-becomes-a-toolkit.md`.
`dated` comes from its frontmatter and its first line: "On 2026-10-07 the user widened Omoikane's objective".
Scope: the user's two statements, quoted in Portuguese with an English translation, and a list of the wiki and doc edits they ask for; a snapshot taken before the issue #111 PRs.

## Key claims

- The user widened the objective: Omoikane is "mais que um sistema de memória", a toolkit "para iniciar o trabalho encima dele", with many skills for software development. See [[omoikane-objective]].
- The user believed pstack is specific to Grok Bot or Cursor: "acredito que o pstack é para o grok bot ou cursor em especifico". See [[pstack]].
- Later in the same session the user made it narrower: "não vai ser para pesquisas genericas, vai ser para desenvolvimento de software".
- The user wants a counterpart of `poteto-mode`: "deixar o agente seguir utilizando a melhor skill para tal tarefa". See [[omoikane-mode-routes-each-task-to-a-playbook]].
- Three references: pstack, Cloudflare security-audit-skill, and the post "Build your own vulnerability harness" (Grant Bourzikas, 2026-06-18). See [[omoikane-references]].
- The "no memory link" verdicts of [[2026-10-06-pstack-skills-review-round-2]] are reopened for a software-development skill set; the verdicts about memory gaps stay.
- Excluded by the user: pstack `tdd` and `unslop`.
- Skill sources at their commits: pstack `df58112`, the user's agent-dotfiles `cc99061` (https://github.com/YuukiFST/agent-dotfiles/tree/main/skills), Cloudflare security-audit-skill `c1c8a8c`, MIT. See [[every-system-ships-the-development-skills]].

## Status of the claims at ingest

The note lists edits still to make: [[omoikane-objective]], [[objective-criterion-stays-out-of-agents-md]], `docs/architecture.md`, `README.md` and [[omoikane-references]].
All are made: PR #113 rewrote `README.md` and `docs/architecture.md` ("Omoikane is for software development, not generic research (#111)", `README.md` line 15), and the distill of [[session-2026-10-07-062e80af]] updated the wiki pages.
The note counts pstack among three new references.
pstack has been a reference since 2026-10-06 ([[2026-10-06-pstack-is-an-omoikane-reference]]); the user's words are conditional, "caso não tenha colocado como referencia", so the note restates it.

## What it adds

The session page and the pages it fed already hold the quotes, the exclusions and the reopened verdicts.
This note adds the author and date of the Cloudflare post, the agent-dotfiles commit, and the user's belief about where pstack runs.
