---
title: New system starts with an empty memory
type: decision
summary: new-system.py clears the template's wiki, captures and rules and renames origin to template; it does not refuse
tags: [new-system, template, objective]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-02-a8b45323.md]
code: [omoikane/bin/new-system.py, tests/test_new_system.py]
---

Chosen: `python omoikane/bin/new-system.py` turns a fresh clone of the template into the empty memory of a new system (issue #66, PR #73) (source: [[session-2026-10-02-1b324082]], turn 3).
It removes the pages, captures and sources, resets `log.md` and `_review.md` to their headers, regenerates `index.md`, empties the rules block of `AGENTS.md` and renames the `origin` remote to `template` (`omoikane/bin/new-system.py`).

Reason: every new system starts from Omoikane ([[omoikane-objective]]), and a clone would otherwise brief each session of the new system on the template's own wiki (turn 3).
The remote rename came from the PR review, commit "fix(bin): keep a new system's pages away from the template's remote" (turn 3): `review-gate.py` publishes to `origin`, so the new system's pages would be pushed to the template ([[review-gate]]).

Rejected: refusing a tree whose origin is the Omoikane repository, the issue's first acceptance criterion. A fresh clone always has that origin, so the check would refuse every legitimate run; the change was recorded on issue #66 (turn 3).

The test clones the tree, runs the reset and checks the result is an empty memory; it was red for the right reason before the script existed (turn 3).

Extended, not reversed: with `--from`, the reset keeps the organisation's conventions and design-system rules another system learned, [[new-system-inherits-conventions-with-from]] (issue #80, PR #85) (source: [[session-2026-10-02-a8b45323]], turn 2).
