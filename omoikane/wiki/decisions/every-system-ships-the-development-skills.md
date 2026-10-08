---
title: Every system ships the development skills
type: decision
summary: Every system gets the dev skills in .claude/skills, one budget, no opt-in pack; omoikane/skills.md lists each source
tags: [skills, template, objective, context-budget, pi]
created: 2026-10-07
updated: 2026-10-08
sources: [wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/2026-10-07-omoikane-objective-widens-to-a-work-toolkit.md, wiki/sources/session-2026-10-08-0ac17a0f.md]
code: [docs/specs/2026-10-07-software-toolkit.md, omoikane/skills.md, tests/test_skills_manifest.py, omoikane/bin/context-budget.py, .pi/settings.json]
---

## Chosen

Every system born from the template starts with the development skills, as ordinary folders under `.claude/skills/` next to the seven memory skills (source: [[session-2026-10-07-062e80af]], turn 5; `docs/specs/2026-10-07-software-toolkit.md`, "Layout").
There is one skill budget, and a merge of `template/main` brings skill updates as it brings prompt updates (turn 5; see [[update-from-template]]).
The agent's turn-5 note: "Todo sistema nasce com as skills de dev, com um orçamento de skills só".

- `omoikane/skills.md` holds one row per vendored skill: upstream URL, commit, SPDX licence and every change made to the upstream text (turn 6; commit `8945f68`).
- `tests/test_skills_manifest.py` fails a skill folder without a row, a row without a folder, a third-party skill without its upstream `LICENSE`, and a description over Pi's 1,024 characters (commits `9450ad6`, `fcfcc8d`).
  Only the memory skills and a system's own `verify-<app>` have no row (turn 9).
- Pi reads the same folder through `.pi/settings.json`, `"skills": ["../.claude/skills"]` (turn 6). See [[pi-coding-agent]].
- Every skill stays model-invocable, without `disable-model-invocation` (`docs/specs/2026-10-07-software-toolkit.md`, "Context budget").
- The user excluded pstack's `tdd` and `unslop`: "Ignore skills como TDD e UNSLOP" (turn 1).
- The three sources the user named, at the commits read: pstack `df58112`, the user's agent-dotfiles `cc99061` (https://github.com/YuukiFST/agent-dotfiles/tree/main/skills), Cloudflare security-audit-skill `c1c8a8c` (source: [[2026-10-07-omoikane-objective-widens-to-a-work-toolkit]]).

## Rejected

- An opt-in `--pack dev`, which the first spec proposed (turn 3). The user then narrowed the objective to software development only (turn 5), so every system needs the skills ([[omoikane-objective]]).
  The agent's turn-5 note: "Sai o uso de pesquisa e sai o opt-in `--pack dev`."
- A copy per harness (`.agents/skills/` beside `.claude/skills/`): OpenCode reads both folders and would load every skill twice (`docs/specs/2026-10-07-software-toolkit.md`, "Layout").

## Budget

`context-budget.py` capped all skill frontmatter at 600 tokens, and the agent counted about 25 skills that would exceed it (turns 1, 3).
pstack avoids the cost with `disable-model-invocation: true`; Omoikane raised the limit instead (turn 3; commit `9450ad6`, 600 to 2,600 tokens, total 7,000 to 9,000).
With every skill merged on `main`, skill frontmatter measured 1,853 tokens and the total 7,670 (turn 11).
Commit `fd5a2a8` lowered the limits to 2,100 and 8,500, "keeping room for a system's own verify-<app> skill, so the budget keeps catching growth". See [[wiki-rules]].

## History

Shipped as PRs #113, #114, #116, #118 and #115 of issue #111, merged on 2026-10-07 (source: [[session-2026-10-07-062e80af]]).
The router that picks a skill for each task: [[omoikane-mode-routes-each-task-to-a-playbook]].
PR #120 (2026-10-08) replaced TDD with E2E-only tests in the vendored skills: [[template-skills-write-e2e-tests-only]] (source: [[session-2026-10-08-0ac17a0f]], turn 9).
