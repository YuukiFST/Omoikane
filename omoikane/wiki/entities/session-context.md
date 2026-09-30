---
title: session-context
type: entity
summary: omoikane/bin/session-context.py, the SessionStart brief: index, undistilled sessions, open and approved review items
tags: [session-context, module, build-mode, review-queue]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-30-c14af01e.md]
code: [omoikane/bin/session-context.py, tests/test_wiki_lint.py]
---

`omoikane/bin/session-context.py` writes the brief injected at session start: the index filled by type priority, the sessions not yet distilled and the open items of `_review.md` (source: [[session-2026-09-30-c14af01e]], turn 2).

## Counting review items

Once proposals carried diffs, lines inside a diff were counted as open items (source: [[session-2026-09-30-c14af01e]], turn 2).
The first fix ignored fenced diffs; after review a second fix parses fences like CommonMark and counts approved (`[x]`) proposals apart (turn 2).
Both are covered by `PendingNotes` in `tests/test_wiki_lint.py` (turn 2).
