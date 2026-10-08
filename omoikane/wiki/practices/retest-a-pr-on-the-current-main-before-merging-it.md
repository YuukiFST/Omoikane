---
title: Retest a PR on the current main before merging it
type: practice
summary: Before a merge, merge the PR onto the current origin/main in a scratch worktree and run the CI steps there
tags: [procedure, pull-request, ci, worktrees]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/session-2026-10-07-9e3fae7e.md]
---

## Rule

Before you merge a PR, merge it, with the PRs that merge before it, onto the current `origin/main` in a scratch worktree.
Run the CI steps there: `python -m unittest discover -s tests`, `python omoikane/bin/context-budget.py`, `python omoikane/bin/wiki-lint.py`.

## Evidence

- PRs #95, #94 and #99: the agent ran `git worktree add -q --detach "$T" origin/main`, merged the three branches there and ran the CI steps (source: [[session-2026-10-06-61eabe29]], turn 2). Its finding: "**#95 quebra a main se for mergeado como está.** O CI do PR rodou contra a main de antes do #102." (turn 6).
- The #111 stack, #112 to #118: "**Checagem geral:** juntei todos os PRs sobre o `origin/main` atual e rodei tudo." (source: [[session-2026-10-07-062e80af]], turn 11).
- The merge of that stack: "montei a integração num worktree temporário: #114 + #117 + #116 + #118 + #115, sem conflitos." The run gave 194 tests OK and 0 `context-budget` findings (source: [[session-2026-10-07-9e3fae7e]], turn 2).

## Scope

The behaviour behind the rule, and how each PR was fixed: [[green-pr-ci-can-be-stale-against-the-current-main]].
When the scratch run fails, merge `main` into the PR's branch, fix it there, and let CI run again (source: [[session-2026-10-06-61eabe29]], turns 4, 6).
A stacked PR whose base moves to `main` gets a new CI run on its merge with `main`: "Depois que o GitHub mudar a base deles para main, o CI do PR roda sobre o merge com a main." (source: [[session-2026-10-07-9e3fae7e]], turn 2).
