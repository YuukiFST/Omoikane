---
title: Review conflicts keep main's file plus whole added runs
type: decision
summary: Merging main into wiki/auto resolves _review.md as main's file plus each run the branch added, whole; not merge=union
tags: [review-gate, review-queue, git, wiki-auto]
created: 2026-10-06
updated: 2026-10-06
sources: [wiki/sources/commits-2026-09-29-to-2026-10-06.md]
code: [omoikane/bin/review-gate.py, tests/test_review_gate.py]
---

`review-gate.py prepare` merges `main` into the `wiki/auto` worktree before a scheduled run.
In `omoikane/_review.md` the human decides by deleting and ticking bullets, while a run only appends, so a conflict there must keep the human's side.

Chosen: main's file plus each run of lines the branch added, kept or skipped whole and placed after its anchor (source: [[commits-2026-09-29-to-2026-10-06]], `f15e1d0`).
The anchor is up to three base lines (`ANCHOR_LINES = 3`), not one ambiguous closing fence (`91e82f4`).
A failed conflict resolution aborts the merge (`91e82f4`).

## Rejected

- A `merge=union` driver: the review of #56 found it brought back bullets the human deleted and duplicated ticked ones (`d263fcf`; the comment above the review-file constant in `review-gate.py` says the same).
- Resolving the conflict line by line: the re-review found it dropped the fences and headers of a diff proposal and a repeated heading (`f15e1d0`).

## Tests

`test_a_bullet_the_human_deleted_stays_deleted`, `test_a_bullet_the_human_ticked_is_not_duplicated` and `test_a_multi_line_proposal_and_a_repeated_heading_survive_a_review_conflict` in `tests/test_review_gate.py`.
