### Pause safely

**You own a clean stop. Leave a checkpoint a cold-start agent can resume from.** This is explicit only. On "keep going", "going to bed, keep going", or "don't stop", do not pause.

1. Stop at a safe boundary. Finish the current atomic step or back out of it. Start nothing new, and cancel any nested subagents.
2. Take no irreversible action to pause. No PR and no push unless you already had one out.
3. Make the work durable. Commit uncommitted edits as one clear `wip:` commit on the current branch so nothing is lost. If the tree is broken, say so in the commit body in one line.
4. Write the resume note into `omoikane/raw/inbox/<YYYY-MM-DD>-<slug>-resume.md`. Capture intent, what you were doing, progress and what's verified, current state (branch, worktree, last commit, open PR), next steps, key files, and gotchas. The Stop hook captures the session itself into `omoikane/raw/inbox/sessions/`, so the note holds only what the transcript would bury. If a decision log exists, point at it instead of duplicating it. Never write under `omoikane/wiki/`.

**Reply:** where you are in the loop, what's on disk versus still in your head (paths, no diff dumps), the commits you made and whether the tree is clean, the resume note's path, and the first action on resume. This is a pause, not a final report.

Adapted from pstack `skills/poteto-mode/playbooks/pause-safely.md` at df58112, rewritten on Omoikane's inbox. MIT, see `../LICENSE`.
