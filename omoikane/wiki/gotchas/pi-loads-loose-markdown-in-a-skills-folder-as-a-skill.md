---
title: Pi loads loose Markdown in a skills folder as a skill
type: gotcha
summary: Pi 1.0.4 loads any .md placed directly in a skills folder as a skill, and stops at a folder that holds a SKILL.md
tags: [pi, skills]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-07-062e80af.md]
code: [tests/test_skills_manifest.py, docs/specs/2026-10-07-software-toolkit.md, .pi/settings.json]
guard: test
---

## Behaviour

Pi (`@earendil-works/pi-coding-agent` 1.0.4) loads a Markdown file placed directly in a skills folder as a skill (source: [[session-2026-10-07-062e80af]], turn 9; commit `4b0ba91`).
It stops at a folder that holds a `SKILL.md`, so a `SKILL.md` nested deeper inside a skill folder is not loaded (commit `4b0ba91`).

The first spec and test said the opposite: commit `9450ad6` checked that "no skill nests a SKILL.md, which Pi would load as another skill".
The review of PR #114 found the error; the agent corrected the spec, "ajusto a afirmação errada da spec sobre `SKILL.md` aninhado" (turn 9), and dropped the nested-file rule (commit `fcfcc8d`).
The source of the corrected rule is `docs/skills.md` and `dist/core/package-manager.js` of pi-coding-agent 1.0.4 (`tests/test_skills_manifest.py`).

## Workaround

Keep every file of a skill inside its own folder under `.claude/skills/`, which `.pi/settings.json` points Pi at.
`tests/test_skills_manifest.py` fails a Markdown file directly in `.claude/skills/`: "Markdown directly in the skills folder loads as a skill in Pi; move it into a skill folder".
See [[pi-coding-agent]] and [[every-system-ships-the-development-skills]].
