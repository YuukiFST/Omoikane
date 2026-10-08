---
title: Green PR CI can be stale against the current main
type: gotcha
summary: A PR's green CI tested the main of its last push; #95 broke the AGENTS.md budget on the newer main. Retest on it
tags: [github, ci, pull-request, context-budget]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/session-2026-10-07-9e3fae7e.md]
code: [AGENTS.md, tests/test_wiki_rules.py, omoikane/bin/context-budget.py]
guard: none
---

## Behaviour

A PR's CI result belongs to the `main` the PR last ran against, not to the `main` it merges into.
PR #95 had green CI, but that run predates PR #102, which added lines to `AGENTS.md` (source: [[session-2026-10-06-61eabe29]], turn 6).
Merged locally onto the current `main`, #95 failed `test_a_full_block_of_long_rules_fits_the_agents_limit` in `tests/test_wiki_rules.py`: "AGENTS.md: 2811 tokens, limit 2800" (turn 6).
The agent's note: "#95 quebra a main se for mergeado como está. O CI do PR rodou contra a main de antes do #102." (turn 6).
Nothing on GitHub stops it: `main` has no required status check (turn 6).

Two PRs that each fit the [[wiki-rules]] budget can overflow it together, since the worst case leaves only a few tokens free.

## Workaround

Before a merge, merge the PR onto the current `origin/main` in a scratch worktree and run the CI steps there (`python -m unittest discover -s tests`, `context-budget.py`, `wiki-lint.py`) (turns 2, 3). Three sessions did it: [[retest-a-pr-on-the-current-main-before-merging-it]].
When one PR fails, merge `main` into its branch, fix it there, and let CI run again before the merge (turns 4, 6).
For #95 the fix cut one sentence from `AGENTS.md`, and the worst case went to 2796 of 2800 (turn 7).
Merge in an order that keeps `main` green, then recheck the later PRs on the new `main`; the agent merged #99, #94, then #95 (turns 6, 7).

## A stack of PRs

On 2026-10-07 seven stacked PRs (#112 to #118) went stale the same way: `main` moved 19 commits ahead, and the stack conflicted (source: [[session-2026-10-07-062e80af]], turn 10).
The agent merged `main` into each branch from the bottom up with merge commits, "sem force-push" (turn 10).
It then merged every PR onto the current `origin/main` in one scratch worktree and ran the CI steps there (turns 10, 11).
The first run failed with exit code 1; the capture does not show the cause (turn 11).
The second run passed: 194 tests, `context-budget` with no findings, `wiki-lint` clean (turn 11).

Before the merges, #117, #116, #118 and #115 lacked `fd5a2a8`, the last commit of #114, which lowered the budget limits (source: [[session-2026-10-07-9e3fae7e]], turn 2).
Their own green CI never ran against those limits.
The agent merged #114, #117, #116, #118 and #115 in a temporary worktree and ran the checks there: 194 tests OK, `context-budget` with 0 findings, `wiki-lint` with 0 findings and 106 warnings (turn 2).
It did not merge #114 into the upper branches: once GitHub moves their base to `main`, each PR's CI runs on its merge with `main` (turn 2).
#113's CI ran again after its base moved, and passed before its merge (turn 3).
After the merges, CI on `main` passed on `7d6bd37`, `50c93f8` and `63cc729` (turn 3).
Moving the base before a merge is also what keeps the upper PRs open: [[gh-pr-merge-delete-branch-closes-prs-stacked-on-it]].
