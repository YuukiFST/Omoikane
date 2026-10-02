# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

A bullet with a checkbox is a proposal: a guard or a prompt change, with its diff below it. Tick `[x]` to approve; an interactive session applies ticked proposals and deletes their bullets, and a scheduled run never does. Delete an unticked bullet to reject it.

## [2026-09-30] distill | session e04462b2

- todo pi-omoikane-commands: add `/ingest`, `/distill`, `/ask`, `/lint` commands for Pi; today Pi only captures and distill runs through `claude` or `opencode` (session e04462b2, turn 4)
- todo unify-transcript-readers: merge the Claude, Pi and OpenCode readers in `session-capture.py` into one state machine (session e04462b2, turn 4)
- todo pi-live-verification: run the Pi extension live once: `pi` at the repo root, accept project trust, prompt an edit, check `omoikane/raw/inbox/sessions/` (session e04462b2, turn 4)

## [2026-10-02] distill | session d4302021

- todo review-gate-known-limits: four review gate limits left on PR #56: a slid hunk in a replay ends the rebase window early (medium, not verified), `settled` can stop advancing, two squashes between runs record only the first, the next PR body relists squashed commits; see [[review-gate]] (session d4302021, turn 4)

## [2026-10-02] distill | session 1b324082

- todo second-domain-distill-eval: rerun the headless distill eval over `tests/fixtures/distill-domain-session-2.md` (rule a guard would catch, rule given in an answer, code breaking the rule, replaced rule); the run was killed for low memory and never gave a result (session 1b324082, turn 5)

## [2026-10-02] distill | session a8b45323

- todo auto-merge-wiki-pr-74: gap 1, auto-merge of the `wiki/auto` PR from `review-gate.py publish` (issue #74), was blocked by the permission classifier and left for you to decide; see [[review-gate]] (session a8b45323, turn 2)
- todo close-second-domain-distill-eval: the eval the todo `second-domain-distill-eval` above asks for ran and passed all five criteria, posted on PR #72; delete both bullets (session a8b45323, turn 2)
- todo cut-realignment-prompt: the user's turn-2 prompt is cut by the capture after the list of open PRs (`[... 6697 chars cut]`); any rule stated in the cut part has no page (session a8b45323, turn 2)

## [2026-10-02] synthesize

- [ ] rule stop-and-ask-at-every-decidir-in-a-handoff-prompt: Mark each user choice DECIDIR in a handoff prompt; at a DECIDIR you receive, stop and ask (synthesize)

## [2026-10-02] distill | session 04edad59

- todo cut-continuation-prompt: the user's turn-2 continuation prompt is cut by the capture inside the PR #84 item (`[... 5710 chars cut]`), including the reason the bootstrap template base was chosen; any rule stated in the cut part has no page (session 04edad59, turn 2)
- todo close-cut-realignment-prompt: issues #79 and #87 are closed and PRs #84 and #88 merged; check whether the todo `cut-realignment-prompt` above still matters, else delete it (session 04edad59, turn 4)
