# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

A bullet with a checkbox is a proposal: a guard or a prompt change, with its diff below it. Tick `[x]` to approve; an interactive session applies ticked proposals and deletes their bullets, and a scheduled run never does. Delete an unticked bullet to reject it.

## [2026-09-30] distill | session e04462b2

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

## [2026-10-05] distill | session 680ff986

- todo handoff-proposals-680ff986: the turn-5 handoff prompt asks another session to carry out this session's proposals (STE-style `wiki/auto` PR body, glossary, reference clones in global memory, auto-merge #74); the capture cuts the list (`[... 5873 chars cut]`), so check they were done or dropped (session 680ff986, turn 5)

## [2026-10-06] distill | session a9384e33

- todo merge-prs-92-to-95: PRs #92 (auto-merge, #74), #93 (#89), #94 (#90) and #95 (#91) are reviewed and wait for the user's merge; #92 predates `/wrap-up` (#101), so decide whether it still applies (session a9384e33, turn 9)
- todo capture-keeps-machine-local-path: the raw capture `omoikane/raw/sources/sessions/2026-10-02-a9384e33.md` keeps the local reference clones path the user said stays out of the public repo; add it to `omoikane/.capture-redact` and decide whether to redact this file before committing (session a9384e33, turn 2)
- todo wiki-auto-pages-missing-on-main: PR #59 (`wiki/auto`) holds `omoikane-objective`, `objective-criterion-stays-out-of-agents-md` and `review-gate`, which this session restates and changes, but `main` lacks them; merge or close #59, then add this session to those pages or recreate them on `main` (session a9384e33, turn 2)
- todo review-59-corrections-cut: the session proposed corrections to `wiki/auto` pages from its review of #59; the list is cut in the capture (session a9384e33, turn 9)
- todo domain-glossary-stale-after-90: the `wiki/auto` concept `domain-glossary` says "not built yet" and goes stale when PR #94 (#90) merges (session a9384e33, turn 7)
- todo persist-local-clones-memory-line: the line about local reference clones sits in `~/.claude/CLAUDE.md`, which `agent-dotfiles` `sync-config` overwrites; move it into `agent-dotfiles` (session a9384e33, turn 2)

## [2026-10-06] distill | session 1de79b19

- todo merge-prs-99-and-100: PRs #99 (#98, distill guards name the fix) and #100 (#97, `/ask` reads `origin/main` history) have green CI and a posted subagent review and wait for the user's merge (session 1de79b19, turn 3)
- todo confirm-pr-99-review-is-final: the "no findings" review on #99 was posted while the task notification said the reviewer "has not reported yet"; check its final report and update the comment if it found something (session 1de79b19, turn 3)

## [2026-10-06] wrap-up | commits

- [ ] prompt (wrap-up.md) wrap-up-commit-coverage-misses-wiki-auto-captures: step 3 looks for captures only on the checkout and requires a `branch` match, so 46 commits whose captures the scheduled run distilled onto `origin/wiki/auto` (PR #59) read as uncovered, and sessions on `main` commit from worktrees on feature branches (commit 87d956b, 1802d44, ec69f47)
````diff
--- a/omoikane/prompts/wrap-up.md
+++ b/omoikane/prompts/wrap-up.md
@@ -8,7 +8,7 @@
 
 1. Run `python omoikane/bin/review-removals.py`, so bullets the human deleted from `omoikane/_review.md` are not filed again.
 2. List `omoikane/raw/inbox/` and `omoikane/raw/inbox/sessions/`. The inbox is a queue: process every file in it, whatever its date, since a file left there was never processed. A capture modified in the last 30 minutes may belong to a session still open, whose next turn would rewrite it while it is being distilled and lose those turns: ask the human whether every other coding session on this repository is closed, and when one is not, leave those captures for the next wrap-up. Give each file to its own subagent when your harness has them, one at a time, never two at once: every operation appends to `log.md` and `_review.md`. The subagent reads `omoikane/prompts/distill.md` for a file under `sessions/`, `omoikane/prompts/ingest.md` for any other, follows it with the file as argument, and returns the prompt's report. Without subagents, run the prompts yourself, one file after another. A capture whose turns are only an earlier `/wrap-up` run holds nothing new: distill logs it `nothing kept`.
-3. Read the commits of the period: `git fetch --quiet`, then `git log --branches --remotes --no-merges --since="<period start> 00:00" --format="%h %ad %an%n%s%n%b" --date=iso-strict -- . ":(exclude)omoikane"` (a bare date means that date at the current time of day). Skip a commit already listed on a `omoikane/wiki/sources/commits-*.md` page. A commit made during a captured session is that session's: the captures are now under `omoikane/raw/sources/sessions/`; their `started` and `ended` are UTC, so convert the commit time to UTC before comparing, and match the capture's `branch`. Skip such a commit unless its body states a reason the session page does not have. Judge each remaining commit's subject and body by the rules of `omoikane/prompts/distill.md` ("What is worth a page" and the five rejection rules): a body that gives the reason for a choice is a `decision`, a root cause found the hard way is a `gotcha`, a rule the system must follow is a `domain` page. Open the diff (`git show --stat <sha>`, then the files) only to confirm a claim, never to invent one the message does not make. When at least one commit yields a page, write the source page `omoikane/wiki/sources/commits-<period start>-to-<today>.md` with the page contract, `type: source`, `dated` set to the newest commit's date, listing each commit used (`<sha> <subject>`); when that page exists, add to it. Cite it from every page those commits fed. Route guards, prompt fixes and todos to `omoikane/_review.md` as distill step 6 does, under `## [YYYY-MM-DD] wrap-up | commits`.
+3. Read the commits of the period: `git fetch --quiet`, then `git log --branches --remotes --no-merges --since="<period start> 00:00" --format="%h %ad %an%n%s%n%b" --date=iso-strict -- . ":(exclude)omoikane"` (a bare date means that date at the current time of day). Skip a commit already listed on a `omoikane/wiki/sources/commits-*.md` page. A commit made during a captured session is that session's: the captures are now under `omoikane/raw/sources/sessions/`, and those the scheduled run distilled stay on `origin/wiki/auto` until its PR merges (`git ls-tree --name-only origin/wiki/auto omoikane/raw/sources/sessions/`). Their `started` and `ended` are UTC, so convert the commit time to UTC before comparing. The time decides: a session commits from worktrees on branches other than the capture's `branch`, which only breaks a tie between two captures. Skip such a commit unless its body states a reason the session page, on the checkout or on `origin/wiki/auto`, does not have. Judge each remaining commit's subject and body by the rules of `omoikane/prompts/distill.md` ("What is worth a page" and the five rejection rules): a body that gives the reason for a choice is a `decision`, a root cause found the hard way is a `gotcha`, a rule the system must follow is a `domain` page. Open the diff (`git show --stat <sha>`, then the files) only to confirm a claim, never to invent one the message does not make. When at least one commit yields a page, write the source page `omoikane/wiki/sources/commits-<period start>-to-<today>.md` with the page contract, `type: source`, `dated` set to the newest commit's date, listing each commit used (`<sha> <subject>`); when that page exists, add to it. Cite it from every page those commits fed. Route guards, prompt fixes and todos to `omoikane/_review.md` as distill step 6 does, under `## [YYYY-MM-DD] wrap-up | commits`.
 4. Run `python omoikane/bin/synthesize-due.py`. Exit code 0: follow `omoikane/prompts/synthesize.md` with no argument.
 5. Append to `omoikane/log.md`: `## [YYYY-MM-DD] wrap-up | <period start> to <today>`, then one line per file processed (`- distill <file>` or `- ingest <file>`), `- commits: <n> read, <n> used` with the pages created and updated, the `- routed` and `- skipped` lines of distill step 7 for the commits with `(commit <sha>)` in place of the turn, and `- synthesize` when it ran.
 6. Run `python omoikane/bin/wiki-index.py` then `python omoikane/bin/wiki-lint.py`. Fix every finding.
````
- todo commits-pages-waiting-on-wiki-auto: after PR #59 merges, apply to its pages what these commits add: `review-gate` (the branch's code never runs, `ece1f62`, `d263fcf`, `f15e1d0`, `91e82f4`; link [[review-conflicts-keep-mains-file-plus-whole-added-runs]]), `wiki-lint` (duplicate slugs and staleness warnings, `40c7e37`, `b63a6fb`), `secret-redaction-patterns-leak-swallow-and-backtrack` (rounds 1 and 2, `ec6aa80`, `0888cb2`), and link `omoikane-holds-its-systems-domain-knowledge-itself` with [[domain-page-type-holds-the-rules-the-user-states]] (commit d263fcf)

## [2026-10-07] distill | session 61eabe29

- todo close-merge-prs-92-to-95: #94 (`4626f21`) and #95 (`96f1ded`) merged and #92 closed unmerged; the capture does not show #93, which `gh` reports MERGED on 2026-10-07; delete the bullet `merge-prs-92-to-95` (session 61eabe29, turn 7)
- todo close-auto-merge-wiki-pr-74: issue #74 and PR #92 closed as superseded by #101 with the user's approval, see [[wiki-auto-auto-merge-dropped-with-pr-92]]; delete the bullet `auto-merge-wiki-pr-74` (session 61eabe29, turn 6)
- todo close-wiki-auto-pages-missing-on-main: PR #59 merged as `26f6e06`, so its pages are on `main`; delete the bullet `wiki-auto-pages-missing-on-main`, and do now what `commits-pages-waiting-on-wiki-auto` and `domain-glossary-stale-after-90` wait for (session 61eabe29, turn 7)
- todo close-merge-prs-99-and-100: #99 merged as `01f039b` in this session and #100 merged as `0118646` per [[ask-searches-origin-main-history-before-asking-for-a-source]]; delete the bullet `merge-prs-99-and-100` (session 61eabe29, turn 6)
- todo local-clones-path-lost: the line about the local reference clones is no longer in `~/.claude/CLAUDE.md`, so the path is lost; write it into your own memory per [[machine-local-paths-stay-out-of-the-public-repo]], then delete `persist-local-clones-memory-line` (session 61eabe29, turn 8)
- todo ste-posts-missing-from-references-list: the agent named the STE posts ([[2026-10-02-ste-and-oversight-posts]]) as a reference missing from [[omoikane-references]]; the user answered only for pstack, so decide whether they belong on the list (session 61eabe29, turn 8)

## [2026-10-07] ingest | 2026-10-06 pstack skills review round 2

- contradiction pr-92-merge-expected-after-close: the pstack round-2 note expects "the `wiki/auto` PR merges itself (PR #92)", but #92 closed unmerged at 12:41 UTC that day; see [[wiki-auto-auto-merge-dropped-with-pr-92]] (source: [[2026-10-06-pstack-skills-review-round-2]], proposal 4)
- todo quote-audit-proposal-not-opened: proposals 1 to 3 became #105, #103 and #106 and merged; proposal 4, a `wiki-lint.py` check that a quote cited to a session turn is in its capture, has no issue; decide whether to open one (source: [[2026-10-06-pstack-skills-review-round-2]], proposal 4)

## [2026-10-07] distill | session fd3ff955

- todo cut-pstack-review-prompt: the user's turn-2 prompt is cut by the capture inside the "agrega" criterion, after its first condition (`[... 1894 chars cut]`); any rule stated in the cut part has no page; the capture predates `1a946fe` (session fd3ff955, turn 2)

## [2026-10-07] distill | session 973284b2

- [ ] guard (test) wrapped-line-splits-a-name-from-its-secret: wrapping a capture line before redaction put `password` and `= value` on two lines and leaked the value; no test fails on that order (session 973284b2, turn 2)
````diff
--- a/tests/test_session_capture.py
+++ b/tests/test_session_capture.py
@@ -334,6 +334,13 @@ class Redaction(unittest.TestCase):
                 self.assertLessEqual(max(map(len, md.splitlines())), 2000)
         self.assertNotIn("acme", md.lower())
 
+    def test_a_wrapped_line_never_splits_a_name_from_its_secret(self) -> None:
+        # Wrapping before redaction put `password` and `= value` on two lines, and the value reached the capture.
+        prompt = "a" * (capture.LINE_CHARS - 10) + " password = hunter22hunter22" + "c" * 300
+        md = self.captured(None, [user(prompt), assistant(
+            {"type": "tool_use", "name": "Edit", "input": {"file_path": "C:/proj/a.py"}})])
+        self.assertNotIn("hunter22", md)
+
     def test_a_term_matches_either_path_separator_and_any_whitespace(self) -> None:
         session = [user("Fix"), assistant({"type": "text", "text": "Acme\n  Corp ships"},
                                           {"type": "tool_use", "name": "Bash",
````
- todo cut-four-issues-handoff-prompt: the turn-2 prompt (issues #103 to #106) is cut inside item (A) (`[... 5028 chars cut]`); any rule stated in the cut part has no page; the capture predates `1a946fe` (session 973284b2, turn 2)

## [2026-10-07] distill | session 062e80af

- todo personal-skills-shadow-template-copies: 12 of the vendored skills also sit in `~/.claude/skills/` from agent-dotfiles, and Claude Code runs the personal copy; decide whether to drop them from the global set or accept the shadowing (`docs/specs/2026-10-07-software-toolkit.md`, "Personal skills of the same name") (session 062e80af, turn 3)
- todo pi-skill-capture-live-check: the Pi `/skill:` capture fix was never checked against a session file a real Pi run wrote; when doing `pi-live-verification`, also run `/skill:wrap-up` and check no capture appears, see [[pi-expands-a-skill-command-into-a-skill-block]] (session 062e80af, turn 6)
- todo security-audit-upstream-pr-69: when cloudflare/security-audit-skill#69 merges, return `.claude/skills/security-audit/` to upstream as it is and update its `omoikane/skills.md` row (session 062e80af, turn 10)
- todo security-audit-windows-promotion-step: the spec asks to check whether `.claude/skills/security-audit/SKILL.md`, whose artifact promotion uses no-follow descriptors and a link count of 1, needs a Windows step; the capture does not show it checked (session 062e80af, turn 3)

## [2026-10-07] distill | session 9e3fae7e

- [ ] guard (hook) gh-pr-merge-delete-branch-closes-prs-stacked-on-it: `gh pr merge <n> --delete-branch` closed #113, whose base was #112's head branch; see [[gh-pr-merge-delete-branch-closes-prs-stacked-on-it]] (session 9e3fae7e, turn 3)
  No diff: the check is a new PreToolUse Bash hook beside `.claude/hooks/escape-edit-guard.py`, listed in `.claude/settings.json`. On `gh pr merge <n>` with `--delete-branch`, it reads the PR's head branch, runs `gh pr list --base <head> --state open`, and blocks when the list is not empty with "move these PRs to main first: gh pr edit <m> --base main". It calls the network on each such merge; decide whether that cost is worth it.
- todo close-issue-111-after-wrap-up: after this `/wrap-up` applies the toolkit note to [[omoikane-objective]] and [[omoikane-references]], close issue #111 by hand when its acceptance criteria hold; no PR closes it, all use `Refs #111` (session 9e3fae7e, turn 2)
- todo omoikane-mode-live-check: check live that `/skill:omoikane-mode` loads in Pi at the trusted repo root and that `/omoikane-mode` works in OpenCode, and write the result as a note in `omoikane/raw/inbox/`; do it with `pi-live-verification` and `pi-skill-capture-live-check` (session 9e3fae7e, turn 2)
- todo remove-stale-worktrees-103-to-106: the worktrees `omoikane-103` to `omoikane-106` remain; the branches of the first three merged (#107, #108, #109), `-106` was not checked; the backup `../omoikane-backup-2026-10-07/` can go too (session 9e3fae7e, turns 2, 4)

## [2026-10-07] synthesize

- [ ] guard (hook) retest-pr-on-current-main: `gh pr merge` on a PR whose head lacks the current `origin/main` trusts a green CI that never ran on that `main`; #95 would have broken the budget test (sessions 61eabe29, 062e80af, 9e3fae7e; turns 6, 10, 2)
  No diff: the check goes in the PreToolUse Bash hook that `gh-pr-merge-delete-branch-closes-prs-stacked-on-it` proposes, beside `.claude/hooks/escape-edit-guard.py`. On `gh pr merge <n>`, it runs `git fetch -q origin`, reads `gh pr view <n> --json headRefOid,baseRefName`, and blocks when the base is `main` and `git merge-base --is-ancestor origin/main <head>` fails, with "test it merged onto origin/main in a scratch worktree, or merge origin/main into the branch and let CI run again". A stacked PR just moved to `main` fails the test though GitHub reran its CI on the merge with `main`; decide whether that false positive, and a network call on each merge, are worth it. GitHub's "Require branches to be up to date before merging" does the same in every harness, but needs a required status check, which `main` lacks.
- [ ] rule recommend-an-option-and-wait-for-the-go-ahead: When a choice is the user's, recommend one option with its reason; act on it only after the user approves (synthesize)
- [ ] rule machine-local-paths-stay-out-of-the-public-repo: Keep paths that hold only on this machine out of committed files; the repository is public (synthesize)
