---
title: review-gate
type: entity
summary: omoikane/bin/review-gate.py keeps the scheduled run on a wiki/auto worktree and publishes it as a PR to main
tags: [review-gate, module, autonomy-loop, git]
created: 2026-10-02
updated: 2026-10-08
sources: [wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-a8b45323.md, wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/commits-2026-09-29-to-2026-10-06.md]
code: [omoikane/bin/review-gate.py, tests/test_review_gate.py, docs/architecture.md]
---

`omoikane/bin/review-gate.py` (issue #45, PR #56) moves the scheduled run of [[wiki-ingest]] off the human's checkout: `prepare` brings a worktree on `wiki/auto` up to date and moves quiet captures into it, `publish` pushes it as a PR to `main`. Merging stays the human's act.
PR #56 merged as `f2ba8ff` (source: [[session-2026-10-01-d4302021]], turn 4).

## The scheduled run goes through the gate

`wiki-ingest.ps1 -Commit` prepares the `wiki/auto` worktree and runs that worktree's own `wiki-ingest.ps1` with `-Commit -NoGate`.
It publishes the branch as one PR only when the run exits 0, so the human's checkout never gets a commit (source: [[commits-2026-09-29-to-2026-10-06]], commit `ece1f62`).

The first three review rounds on #56 each found faults; each fault now has a test (same source):

- Round 1 (commit `d263fcf`): a union merge of `_review.md` brought back bullets the human deleted and duplicated ticked ones. One failed agent call stopped every later `prepare`. `worktree add -B` dropped unpushed commits. The scheduler would run whatever code `wiki/auto` held. A squash merge or a rejected PR made every run open a new PR.
- Round 2 (commit `f15e1d0`): a `_review.md` conflict resolved line by line dropped the fences and headers of a diff proposal. An index conflict ran the branch's own `wiki-index.py` before the code refusal. A PR rejected by closing came back once `main` moved.
- Round 3 (commit `91e82f4`): after a squash merge, a clean merge undid the human's later decision on a squashed bullet, because the merge base stayed before it.

The fixes: the scheduled run refuses to run code the branch changed (`d263fcf`). That refusal runs before any merge and counts only what the branch changed (`f15e1d0`, `91e82f4`).
A review run is kept or skipped whole, after up to three base lines of context: [[review-conflicts-keep-mains-file-plus-whole-added-runs]].
`prepare` finds a squash by patch id and records it as merged (`91e82f4`).
A closed head that HEAD contains blocks the publish, unless its commits reached `main` (`f15e1d0`, `91e82f4`).

## Landing detection

When the human lands `wiki/auto` by squash or rebase merge, the gate must record it, or the next merge of `main` brings back a bullet the human deleted from `_review.md` afterwards.
`find_landed` / `take_landed` replaced `find_squash` / `take_squash`, which did not recognise a rebase merge (a high finding) nor a squash of an earlier head (medium) (source: [[session-2026-10-01-d4302021]], turns 3, 4).
They look on `main` for a run of consecutive non-merge commits whose combined `-U0` patch equals what the branch changed up to one of its commits, then merge `first^` normally and `last` with `-s ours` (turn 3).

Each later review round tightened it, with a red test first (turns 3, 4):

- a rebase is recorded whole, and a human revert on `main` is not taken for a landing (`632bc7f`);
- `settled` bounds the candidates, keeping subprocess calls per `prepare` at 24, where they ranged from 21 to 84 (`632bc7f`);
- `settled` only accepts a merge whose tree is main's, and the rebase window only accepts replays of branch commits (`4223240`);
- the window is capped by commit count, not by distinct patches (`2ef4bdb`).

The agent declined a reviewer's suggested fix because it "reabriria o achado da review 6 (o revert humano)" (turn 3).

## Known limits

Recorded on PR #56 and not fixed (turn 4): a slid hunk in a replay ends the window early (medium, not verified); `settled` can stop advancing (low); two squashes between runs record only the first (low); after a squash the next PR body lists the old commits again (low).

## Captures main already holds

`move_captures` leaves in the human's checkout an inbox file that `origin/main` holds byte for byte: the worktree gets it from `main`, and moving it left a deletion in the checkout (issue #78, PR #81, merged) (source: [[session-2026-10-02-a8b45323]], turn 2; `omoikane/bin/review-gate.py`).
The review of #81 sent more findings back, reproduced by a red test and fixed in `move_captures` (turn 2); the test is `test_only_quiet_captures_move_into_the_worktree`.

## Auto-merge

Gap 1 of the realignment plan, issue #74: `publish` would enable auto-merge on the `wiki/auto` PR with `gh pr merge --auto --merge --match-head-commit`. The permission classifier blocked the action, and the agent dropped its worktree and branch and left the choice to the user (source: [[session-2026-10-02-a8b45323]], turn 2).
The user chose auto-merge in PR #92 ([[wiki-auto-pr-merges-itself-once-checks-pass]]), then approved closing #92 and #74 unmerged, superseded by #101: [[wiki-auto-auto-merge-dropped-with-pr-92]] (source: [[session-2026-10-06-61eabe29]], turns 6, 7).
The `wiki/auto` PR #59 merged as `26f6e06`, and the branch `wiki/auto` and its worktree were removed (turn 7).
