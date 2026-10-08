---
title: gh pr merge --match-head-commit needs the full SHA
type: gotcha
summary: gh pr merge --match-head-commit rejects a short SHA ("Could not coerce value"); pass git rev-parse of the branch
tags: [gh, github, pull-request]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-06-61eabe29.md]
guard: none
---

## Behaviour

`gh pr merge 99 --merge --match-head-commit be2061c` failed with exit code 1 and did not merge (source: [[session-2026-10-06-61eabe29]], turn 6):

```
GraphQL: Variable $input of type MergePullRequestInput! was provided invalid value for expectedHeadOid (Could not coerce value "be2061c" to GitObjectID)
```

The flag goes to GitHub as `expectedHeadOid`, which takes only a full commit id (turn 6).
The short SHA came from `gh pr view --json headRefOid --jq '.headRefOid[0:7]'`, cut for display (turn 6).

## Workaround

Pass the full id: `gh pr merge <n> --merge --match-head-commit $(git rev-parse origin/<branch>)` after `git fetch` (turn 6).
The session merged #99, #94, #95 and #59 that way (turns 6, 7).
