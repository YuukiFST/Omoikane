### Autonomous run

**You own the exit condition. Define done, then drive to it without stopping.**

1. State the exit condition as a checkable predicate before the first iteration (tests green, repro fixed, all N PRs merged, pixel-diff zero).
2. Pick the wake mechanism the harness offers. An event to watch (CI, a merge, a ref advancing) gets a background command that returns on the event, such as `gh pr checks <pr> --watch`, with a long time-based re-check as fallback. No event gets a fixed-interval re-check sized to when the result is worth re-checking, through the harness's scheduler when it has one (Claude Code `/loop`) or in the main loop otherwise.
3. Each iteration makes the smallest change the evidence justifies, verifies it against the predicate, commits if it advanced, discards changes that didn't help. Belt-and-suspenders that "might help" gets reverted, not left to ride.
   Sequence the work via principle `sequence-verifiable-units`, verifying each unit before the next instead of batching checks at the end.
4. Mid-run discoveries are yours. Address broken skills, related bugs, flaky verifiers, review noise, tooling failures, orphaned follow-ups, and fixable drift yourself under omoikane-mode. Put out-of-band fixes in their own PR. Do not park reversible work for the user or stop to ask. Surface only irreversible actions (the Always-pause list in `../SKILL.md`), genuine product or preference calls no experiment can settle, or a real dead end. Keep the predicate as the main drive, and return to it after each side fix.
5. Checkpoint every iteration in the decision log: a row for what changed and whether the predicate moved. A lesson the next agent needs goes into a note under `omoikane/raw/inbox/`.
6. Stop when the predicate is met. A plateau is not a stop, so keep going and pivot your approach to push past it. Surface a genuine dead end rather than spinning, and never relax the predicate to declare victory.

**Reply:** the exit condition, iterations run, what landed, what was discarded, final predicate state.

Adapted from pstack `skills/poteto-mode/playbooks/autonomous-run.md` at df58112. MIT, see `../LICENSE`.
