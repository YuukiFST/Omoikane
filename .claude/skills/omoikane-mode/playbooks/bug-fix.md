### Bug fix

**You own this task. Plan, review, verify.** Delegate investigation and the fix to subagents, stay in the lead.

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix. It does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

1. Reproduce it yourself on the matching surface via the project's verification skill (`verify-<app>`; none yet → the **create-verification-skill** skill), even when a debug or instrumentation protocol says to ask the user to reproduce. Ask the user only with a stated, specific reason the verification skill cannot reach the target, and only after driving it as far as it goes. If it won't reproduce directly, synthesize the trigger, tighten conditions, or instrument until it fires.
2. Binary-search the cause. Form the candidate hypotheses, then rule them out until one survives. Seed them with `how` over the affected subsystem, the gotcha pages whose `code:` lists the area, the wiki pages `omoikane/index.md` lists, and `git log origin/main` / `git blame` / `gh pr view` for regression history (not `/ask`, which writes the wiki). Each pass, take the split that cuts the most remaining problem space, get runtime evidence, eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. Drive a long or stubborn hunt per the Autonomous run playbook (`autonomous-run.md`). Confirm the surviving *mechanism* with runtime evidence before planning the fix.
3. Plan the fix. If it crosses a module boundary, run the **codebase-design** skill first. Delegate implementation to a fresh subagent with a specific scope.
4. Verify on the same surface. The original repro now passes. "Inconclusive" or wrong-surface is not a pass. Flag it. Unit tests show branch behavior, not bug absence.
5. Stage the commits so the failing repro lands before the fix in git history. Write the repro as an E2E test through the surface step 1 used, watch it go red on the pre-fix code, then fix (the **test-audit** skill gates the test). Once green, it is the bug's one regression test. Write no unit or integration test unless the user asks for one. Skip the test when an E2E test would be expensive or flaky, and paste the step 1 repro output as the evidence instead.
   This is the canonical principle `sequence-verifiable-units`, the reproduction first and the fix on top.
6. Run **Opening a PR**.

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.

Adapted from pstack `skills/poteto-mode/playbooks/bug-fix.md` at df58112. MIT, see `../LICENSE`.
