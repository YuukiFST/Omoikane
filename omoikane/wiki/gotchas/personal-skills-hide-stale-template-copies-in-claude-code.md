---
title: Personal skills hide stale template copies in Claude Code
type: gotcha
summary: Claude Code runs ~/.claude/skills over the template's copy of the same name, so a stale template skill looks current
tags: [skills, claude-code, template, agent-dotfiles]
created: 2026-10-08
updated: 2026-10-08
sources: [wiki/sources/session-2026-10-08-0ac17a0f.md, wiki/sources/2026-10-08-agent-written-tests-are-e2e-only.md]
code: [docs/specs/2026-10-07-software-toolkit.md, omoikane/skills.md]
guard: none
---

## Behaviour

Claude Code runs a personal skill in `~/.claude/skills/` over the project skill of the same name (`docs/specs/2026-10-07-software-toolkit.md`, "Personal skills of the same name").
On the user's machine, 12 template skills also exist as personal copies from agent-dotfiles (same file).

On 2026-10-08 the user's agent-dotfiles already taught E2E-only tests, in `CODING_STANDARDS.md` and in the personal skills (source: [[session-2026-10-08-0ac17a0f]], turn 9).
The template's copies still taught TDD (turn 9).
The agent's note: "No Claude Code desta máquina você não percebia, porque a cópia pessoal tem prioridade sobre a do projeto. Mas o OpenCode, o Pi e todo sistema criado a partir do template ainda recebiam TDD." (turn 9).
The user's note on the change states it too: before PR #120, Claude Code on the user's machine ran the updated personal copies; OpenCode, Pi and every system made from the template got TDD (source: [[2026-10-08-agent-written-tests-are-e2e-only]], line 36).
The user had suspected the opposite, that the global files were out of date: "eu estava com o claude 'atrasado' então talvez algo tenha mudado" (turn 8).

## Workaround

- Do not take a Claude Code run on the user's machine as proof of how a template skill behaves. The spec runs its checks under a clean `HOME` (`docs/specs/2026-10-07-software-toolkit.md`).
- When agent-dotfiles changes a skill the template vendors, port the change: the session found commits `f0202c8`, `5a4c7a6` and `825c9f8` there and ported them (turn 8). The note names a fourth, `97f852f`, from agent-dotfiles PRs #126 and #128 (source: [[2026-10-08-agent-written-tests-are-e2e-only]], line 7). See [[template-skills-write-e2e-tests-only]].
- The rows of `omoikane/skills.md` that PR #120 changed name the agent-dotfiles commits they follow; start the comparison there.

The open question, drop the 12 personal copies or accept the shadowing, is the `_review.md` todo `personal-skills-shadow-template-copies`.
A test that fails when a template skill mentions TDD is proposed in `omoikane/_review.md`; it catches this one rule, not drift in general.
