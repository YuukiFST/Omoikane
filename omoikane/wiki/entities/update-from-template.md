---
title: update-from-template
type: entity
summary: omoikane/bin/update-from-template.py merges template/main into a system and keeps the system's own memory
tags: [template, new-system, module, git]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-973284b2.md, wiki/sources/2026-10-06-pstack-skills-review-round-2.md, wiki/sources/session-2026-10-06-fd3ff955.md]
code: [omoikane/bin/update-from-template.py, tests/test_new_system.py, docs/architecture.md, README.md]
---

`omoikane/bin/update-from-template.py` lets a system born from the template take the template's later fixes to prompts, scripts and docs (issue #105, PR #108, `93c2dea`).

## Why

A plain `git merge template/main` brought the template's own capture and its source page into the system's wiki, and conflicted on `_review.md`, `index.md` and a domain page (source: [[2026-10-06-pstack-skills-review-round-2]], proposal 1; `docs/architecture.md`).
The idea comes from pstack's benny, whose refresh never overwrites the user's files: [[pstack]].
The session that recommended the issue is [[session-2026-10-06-fd3ff955]]; [[session-2026-10-06-973284b2]] built it (turn 2).

## What it does

From its docstring and `docs/architecture.md`:

- It fetches the `template` remote, which `new-system.py` names ([[new-system-starts-with-an-empty-memory]]), and merges `template/main` without committing.
- It puts back the paths the system owns (`MEMORY`: `omoikane/wiki`, `omoikane/raw`, `omoikane/log.md`, `omoikane/_review.md`) as HEAD has them, and removes what the template added there.
- It keeps the rules block of `AGENTS.md` as the system has it, and regenerates `index.md` with the merged `wiki-index.py`.
- Any other conflict stays for the human. It never commits: read `git diff --cached`, then commit, or undo with `git merge --abort`.
- Exit codes: 0 merged and staged, 1 conflicts left for the human, 2 refused before the merge, 3 failed after the merge started.

A repository made with "Use this template" shares no commit with the template.
The agent chose to find the base by tree, with a temporary graft, and to refuse when no tree matches (source: [[session-2026-10-06-973284b2]], turn 2).
`template_base` finds the template commit whose tree is the system's root tree, and the script grafts the root onto it for the merge only (`git replace`).
`docs/architecture.md` gives the rejected option: `--allow-unrelated-histories`, which has no base, so every file the template changed would conflict.

## Testing

`UpdateFromTemplate` in `tests/test_new_system.py`. The tests failed in CI first: [[git-merge-no-commit-needs-a-committer-identity]] (source: [[session-2026-10-06-973284b2]], turn 2).
The agent also ran the real case of the issue in a `$TEMP` clone reset to `e4e89e7`: "merge limpo, 0 mudança em wiki/raw/log/review, 3 arquivos do template descartados, sem graft sobrando" (turn 2).

The subagent review of #108 gave 7 findings, 2 of them medium and confirmed (turn 2), fixed in `343d584`:

- A rerun while the merge still waited for a commit reported success and merged nothing; the script now refuses while a merge, rebase, cherry-pick or revert is in progress (turn 2).
- `index.md` was rendered by the system's old `wiki-index.py`; it is now rendered by the merged one, as CI renders it (turn 2).
