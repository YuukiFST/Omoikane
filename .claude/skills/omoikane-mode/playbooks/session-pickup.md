### Session pickup

**You own the resume point. Read the prior trail, don't redo it.**

1. Locate the prior trail in Omoikane's memory and in live state:
   - The session brief lists the captured sessions not yet distilled. Read the last one under `omoikane/raw/inbox/sessions/`: metadata and last messages first, then scan back for the decision points.
   - Resume notes and other notes a prior agent left under `omoikane/raw/inbox/` (the Pause safely playbook writes them there).
   - Distilled sessions under `omoikane/wiki/sources/`, and the decision and gotcha pages whose `code:` lists the area you resume.
   - Live state: `git status`, `git log`, `git branch -a`, `git worktree list`, and `gh pr list --author @me` / `gh pr view <pr>` for a pushed branch.

   Parse a long session file in a subagent and keep the reduced timeline in the main thread (principle `guard-the-context-window`).
2. Reconstruct operational state. The branch and worktree, what already landed (`git log`, `git diff` against the base), the open todos, the decisions made. The prior trail is authoritative input. Resist the bias to re-derive it.
3. Diff done vs pending. Compare what shipped against what was planned, name the resume point, do not re-run the prior repro or redo completed work. A "let me verify from scratch" pass means you're treating the trail as untrustworthy when it's authoritative.
4. Route the remaining work to the matching playbook and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. The pickup playbook ends here. The routed playbook owns the rest.
5. Verify the inherited claims against the original goal on the real artifact (principle `prove-it-works`). A passing prior self-report is not the proof.

**Reply:** where the prior session stopped, what you inherited vs redid (ideally nothing redone), the resume point, and the outcome.

Adapted from pstack `skills/poteto-mode/playbooks/session-pickup.md` at df58112, rewritten on Omoikane's captured sessions. MIT, see `../LICENSE`.
