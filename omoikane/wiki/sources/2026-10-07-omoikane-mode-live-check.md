---
title: 2026-10-07 omoikane-mode live check
type: source
summary: The user's live check of omoikane-mode: listed in OpenCode and Pi, loading confirmed in OpenCode only
tags: [omoikane-mode, opencode, pi, skills, verification]
created: 2026-10-08
updated: 2026-10-08
dated: 2026-10-07
sources: []
code: [.claude/skills/omoikane-mode/SKILL.md, .claude/skills/omoikane-mode/playbooks/investigation.md, .opencode/command/omoikane-mode.md, .pi/settings.json]
---

A short note, `omoikane/raw/sources/2026-10-07-omoikane-mode-live-check.md`, that records one live check by the user.
Its frontmatter bears `date: 2026-10-07`, and its first line says "On 2026-10-07 the user checked omoikane-mode in both harnesses"; commit `a7b6b78` added it to `main` on 2026-10-08.

## Scope

A snapshot of one day and two harnesses, OpenCode and Pi.
It answers the `_review.md` todo `omoikane-mode-live-check` (session 9e3fae7e, turn 2) and says what it leaves open.
It does not cover Claude Code.

## Key claims

- The user first said: "eu ja verifiquei no OpenCode, esta funcionando perfeitamente, no PI tambem".
  The user then narrowed the claim: "quando eu digo que eles estão funcionando é que eles apareceram quando eu fui digitar omoikane-mode".
- OpenCode lists `/omoikane-mode` in the command list while the user types.
- Pi lists the omoikane-mode skill command in the command list while the user types.
- OpenCode loads the skill: the user ran `/omoikane-mode`, asked for an AI-slop audit of `README.md`, and pasted the reply.
  - The reply opens with `throughput checkpoint: n/a, read-only investigation`, step 2 of `.claude/skills/omoikane-mode/playbooks/investigation.md`. So the agent routed the task to the Investigation playbook.
  - It ends with "Princípios aplicados: prove-it-works ... minimize-reader-load", two files under `references/principles/`.
  - It follows the skill's "Writing the reply" rules: short sentences, one paragraph for the consumer and one for the maintainer, evidence labelled automatic or manual.
  - It used the user's personal `ai-tells` skill, which Omoikane does not ship; OpenCode loaded both skills.
- Pi loading: not checked yet.
- The todo `omoikane-mode-live-check` now holds only for Pi; the todos `pi-live-verification` and `pi-skill-capture-live-check` stay open.

## What it adds

- First live evidence that the OpenCode command `.opencode/command/omoikane-mode.md` runs the skill and that its playbook routing works there: [[omoikane-mode-routes-each-task-to-a-playbook]], [[opencode]].
- First evidence that Pi runs on the user's machine and reads the project skills of `.pi/settings.json`: [[pi-coding-agent]].
- The OpenCode run is in the raw capture `omoikane/raw/sources/sessions/2026-10-07-Q7Bpg6M5.md` (started 2026-10-07T15:25:46Z, distilled `nothing kept`).
  Its prompt is the command text, "Read `.claude/skills/omoikane-mode/SKILL.md` and follow it for the rest of this session"; line 92 holds the checkpoint line and line 114 the principles line.

## Contradictions

- The note says OpenCode used "the user's personal `ai-tells` skill from `~/.claude/skills/`" (note, line 16).
- The capture of that run calls the lint under `~/.agents/skills/ai-tells/scripts/` (`omoikane/raw/sources/sessions/2026-10-07-Q7Bpg6M5.md:80`, turn 1, Commands).
  On 2026-10-08 both `~/.claude/skills/ai-tells/` and `~/.agents/skills/ai-tells/` exist, so the run does not show which folder OpenCode loaded the skill from.
