---
name: correct
description: "Find the mistakes agents keep repeating in this repo and make each one impossible: architecture first, then types, a lint whose error names the fix, a test, docs last. Prove each check fails on a real past mistake. Use for /correct, or when the same correction repeats."
---
<!-- Source: cursor/plugins pstack/skills/correct at df58112 (MIT, Lauren Tan); adapted, see omoikane/skills.md -->

# Correct

The operator keeps correcting agents in this repo for the same mistakes. Change the repo so the next agent can't make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Design the repo so a change that looks right from one file is right for the whole repo.

## Find the mistake classes

First, read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice.

In an Omoikane system, also read the gotcha pages with `guard: none` and the `guard` bullets in `omoikane/_review.md`. `/distill` files a guard there for a mistake one session made (`omoikane/prompts/distill.md`, step 6); `/lint` files one for a gotcha still at `guard: none`. An open `- [ ]` bullet is evidence only. Apply a bullet only when the human ticked it `[x]` or names it in this run; run the tests, then delete the bullet (`AGENTS.md`, "Coding sessions").

## Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Enforce it with types so the bad state can't be written.** If bad code still compiles, add a lint or CI check whose error names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more.
3. **Test the behavior.** Fix or delete any test that would still pass if every function it calls returned nothing.
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails when an agent skips them.

In an Omoikane system, a check you do not land in this run, or one you find outside a `/correct` run, becomes a guard proposal for the human to tick. Write it in `omoikane/_review.md` under `## [YYYY-MM-DD] correct`, with its diff, in the format of `distill.md` step 6, ending in `(correct YYYY-MM-DD)` where distill writes the session: `- [ ] guard (test) <slug>: <the mistake it catches> (correct YYYY-MM-DD)`. Append `## [YYYY-MM-DD] correct | <title>` to `omoikane/log.md`, with one line `- routed (guard) <slug>: <the mistake in one line>` per proposal. `omoikane/bin/review-removals.py` reads that line to record the human's decision, so no later `/distill` or `/lint` files the same guard again. The same ladder holds there: prefer a lint or test, which every harness and CI run, over a hook, which only one harness runs.

## Fix and prove

Then fix the most frequent classes now, one commit each. In an Omoikane system, skip a class whose fix is an open `guard` bullet the human has not ticked or named; it stays a proposal. Prove each new check fails on a real past mistake. Run the same command locally and in CI. Exceptions go on the offending line with a reason, an expiry date, and a human's approval.

## Keep the rule table

Last, keep a table in the agent instruction file that pairs each rule with what enforces it. When the operator corrects you, fix the mistake and add the rule. If the rule was already there and nothing enforces it, that's a repeat, so fix it at the highest level in the same change. Drop a rule once its mistake can't happen.

In an Omoikane system, `AGENTS.md` has no budget room for the table, and only `omoikane/bin/wiki-rules.py` writes its rules block. The gotcha pages are the table there: each one's `guard:` names what enforces it. Do not edit the page in this run: the Stop hook captures the session, and its `/distill` sets the gotcha's `guard:` to the check you landed (`distill.md` step 4).

**Reply:** each class with its evidence, the level you picked, and why a higher level didn't work.
