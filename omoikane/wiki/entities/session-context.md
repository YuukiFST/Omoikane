---
title: session-context
type: entity
summary: omoikane/bin/session-context.py, the SessionStart brief: index, undistilled sessions, open and approved review items
tags: [session-context, module, build-mode, review-queue]
created: 2026-09-30
updated: 2026-10-07
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-02-a8b45323.md, wiki/sources/session-2026-10-06-973284b2.md, wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/session-2026-10-07-9e3fae7e.md]
code: [omoikane/bin/session-context.py, tests/test_wiki_lint.py, omoikane/bin/context-budget.py, tests/test_session_capture.py]
---

`omoikane/bin/session-context.py` writes the brief injected at session start: the index filled by type priority, the sessions not yet distilled and the open items of `_review.md` (source: [[session-2026-09-30-c14af01e]], turn 2).

Since the `domain` page type (issue #64, PR #71) the brief header was adjusted for it and domain pages are listed first, so a cut brief drops them last (source: [[session-2026-10-02-1b324082]], turn 3; `docs/architecture.md`).
Since issue #75 (PR #83) the rule and lesson sections each get a floor of the budget, so domain pages cannot push decisions and gotchas out: [[brief-floors-only-the-rule-and-lesson-sections]] (source: [[session-2026-10-02-a8b45323]], turn 2).

## Counting review items

Once proposals carried diffs, lines inside a diff were counted as open items (source: [[session-2026-09-30-c14af01e]], turn 2).
The first fix ignored fenced diffs; after review a second fix parses fences like CommonMark and counts approved (`[x]`) proposals apart (turn 2).
Both are covered by `PendingNotes` in `tests/test_wiki_lint.py` (turn 2).

## Capture failures

Since issue #103 (PR #107) the brief puts one line under Pending when `omoikane/.capture-errors` exists: the count of failed captures and the last error (source: [[session-2026-10-06-973284b2]], turn 2). The line stays until the human deletes the file (commit `872319e`).
The idea is pstack's "Doctor" check, which an agent runs first; here the brief plays that part, since every session reads it (turn 2; [[pstack]]).
`write_worst_case` in `omoikane/bin/context-budget.py` includes the line in the worst-case brief.
The first version took the worst-case brief to 3968 of 4000 tokens, "margem curta demais"; the agent clipped the last error to 240 characters (`CAPTURE_ERROR_CHARS`) and shortened the text, which gave 3885 (turns 2, 3).
See [[session-capture]] for what the capture writes.

## omoikane-mode reminder

Since PR #117 (issue #111) the brief ends with "Nontrivial software task: load the omoikane-mode skill first." (`omoikane/bin/session-context.py`).
It stands in for Cursor's `reminder:` field, which no harness Omoikane supports has: [[omoikane-mode-routes-each-task-to-a-playbook]] (source: [[session-2026-10-07-062e80af]], turns 5, 9).
Commit `0c3f4cd` measured the worst-case brief at 3,792 of 4,000 tokens with the line.
With every #111 PR merged in one worktree, the worst-case brief measured 3903 of 4000, "perto do limite" (source: [[session-2026-10-07-9e3fae7e]], turn 2).
