# Log

Append-only. One entry per operation. `grep "^## \[" log.md | tail -5` shows the last five.

## [2026-09-09] init | Repository created

## [2026-09-30] distill | session e04462b2

Created: [[session-2026-09-15-e04462b2]], [[session-file-name-uses-id-tail]], [[opencode-run-exits-before-plugin-event-handlers-finish]], [[opencode-mixes-path-separators-on-windows]], [[pi-coding-agent-package-moved-to-earendil-works]], [[session-capture]], [[pi-coding-agent]], [[opencode]].
Updated: none.

- routed (guard) typecheck-harness-plugins: the Pi and OpenCode `.ts` files are not typechecked in CI (turn 4)
- routed (todo) pi-omoikane-commands: Pi has no Omoikane operation commands (turn 4)
- routed (todo) wiki-lint-backslash-code-paths: `code:` paths with backslashes are not normalised in wiki-lint (turn 4)
- routed (todo) unify-transcript-readers: three readers could become one state machine (turn 4)
- routed (todo) pi-live-verification: the Pi extension never ran live (turn 4)
- skipped (missing-env) pi-not-installed: `which pi` found no `pi` on the machine (turn 2)
- skipped (one-off) opencode-sqlite-probe: ad hoc python query against the OpenCode store raised a traceback (turn 2)
- skipped (self-resolved) earendil-package-grep-paths: grep paths taken from the old Pi package missed in the new one (turn 2)
- skipped (self-resolved) bash-heredoc-unclosed-quote: `unexpected EOF while looking for matching` quote in a shell command (turn 2)
- skipped (self-resolved) docker-volume-msys-path-conversion: docker volume mount retried with `MSYS_NO_PATHCONV=1`, failure text not captured (turn 2)
- skipped (no-root-cause) auto-mode-classifier-denial: an action was denied by the auto mode classifier, the transcript does not say which (turn 3)

## [2026-09-30] distill | session c14af01e

Created: [[session-2026-09-30-c14af01e]], [[headless-runs-scoped-to-wiki-edits-and-two-scripts]], [[gotcha-guard-field-records-the-existing-check]], [[user-settings-apply-to-headless-claude-runs]], [[python-heredoc-edits-corrupt-backslash-n]], [[wiki-ingest]], [[wiki-lint]], [[wiki-rules]], [[session-context]].
Updated: [[session-capture]].

- routed (guard) user-settings-apply-to-headless-claude-runs: no test pins the headless scope flags in `wiki-ingest.ps1` (turn 2)
- routed (todo) switch-on-autonomous-loop: distill captured sessions and turn the scheduled loop on (turn 4)
- routed (todo) phase-2-pendencies: Phase 2 pendencies from the handoff prompt, list clipped by capture (turn 4)
- routed (todo) omoikane-knowledge-for-redacted: make Omoikane knowledge reusable as company knowledge in [redacted] (turn 4)
- skipped (self-resolved) remove-item-protected-path: `Remove-Item` on `omoikane/wiki/*` blocked as a protected path, eval clones cleared with `-LiteralPath` instead (turn 2)
- skipped (one-off) eval-clone-planted-regression: `/lint` in an eval clone found a regression the agent introduced in the clone copy (turn 2)

## [2026-09-30] synthesize | 2 sessions

Created: [[review-each-pr-with-a-subagent-before-merging]].
Updated: [[session-2026-09-15-e04462b2]], [[session-2026-09-30-c14af01e]] (link to the practice).

- routed (rule) review-each-pr-with-a-subagent-before-merging: subagent review posted on the PR, real findings fixed, merge commit (sessions e04462b2, c14af01e; turns 3, 3)
- dropped (one-session) headless-eval-in-temp-clone: only c14af01e ran prompt evals in a `$TEMP` clone; e04462b2 tested `opencode run` live in the repo itself
- dropped (known) tests-first: only c14af01e wrote failing tests first, and the user's global CLAUDE.md already requires a failure list before code
- dropped (known) verify-api-against-package-docs: e04462b2 read `npm pack` docs, c14af01e checked `claude` flags; the user's global CLAUDE.md already says never guess APIs or flags
- dropped (known) confirm-git-identity-before-commit: both sessions ran `git config user.name; git config user.email`, required by the user's global git rules
- dropped (coincidence) heredoc-failures: e04462b2 hit an unclosed quote in a bash heredoc, c14af01e corrupted `\n` in Python heredoc edits; different causes, the second is [[python-heredoc-edits-corrupt-backslash-n]]

## [2026-10-01] distill | session 230a182d

Created: [[session-2026-09-30-230a182d]], [[headless-runs-have-no-shell]], [[company-internal-material-stays-out-of-the-public-repo]], [[opencode-merges-user-permission-maps-into-the-headless-scope]], [[opencode-offers-apply-patch-to-gpt-models]], [[opencode-writes-schema-into-project-opencode-json]], [[powershell-function-output-becomes-its-return-value]], [[windows-path-lookup-ignores-case-and-trailing-dots]], [[headless-scope]].
Updated: [[headless-runs-scoped-to-wiki-edits-and-two-scripts]] (History), [[wiki-ingest]], [[opencode]], [[session-capture]], [[wiki-lint]], [[wiki-rules]], [[python-heredoc-edits-corrupt-backslash-n]].

- routed (todo) finish-rejection-memory-pr-44: PR #44 open at capture (turn 2)
- routed (todo) finish-review-gate-45: review gate unmerged; register the scheduled task after it lands (turn 4)
- routed (todo) close-resolved-review-items: older `_review.md` items resolved or superseded by this session's PRs (turn 2)
- skipped (no-root-cause) opencode-fails-through-wiki-ingest: OpenCode server error through `wiki-ingest.ps1`, also on `main`, while a manual run worked; cause not found in the capture (turn 2)
- skipped (no-root-cause) opencode-probe-hangs-after-init: an override probe hung after init, "suspeita: stdin", rerun with the prompt in a file and stdin closed (turn 2)
- skipped (no-root-cause) push-exit-1: a `git push` returned exit 1, outcome not captured (turn 2)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 2)
- skipped (self-resolved) opencode-schema-keyerror-properties: `KeyError: 'properties'` reading the downloaded OpenCode config schema (turn 2)
- skipped (one-off) probe-refused-by-model: the model refused one probe round (turn 2)
- skipped (one-off) background-review-agent-stopped: the PR #40 re-review agent did not finish before the session ended (turn 3)

## [2026-10-01] distill | session b5b6fb27

Created: [[session-2026-10-01-b5b6fb27]], [[claude-bare-read-rule-reads-outside-the-repository]], [[opencode-writes-its-own-files-on-first-start]], [[typescript-misnamed-plugin-hook-passes-without-satisfies]].
Updated: [[headless-runs-have-no-shell]], [[company-internal-material-stays-out-of-the-public-repo]], [[python-heredoc-edits-corrupt-backslash-n]], [[headless-scope]], [[opencode]], [[wiki-ingest]], [[wiki-rules]].

- routed (todo) merge-typecheck-plugins-pr-48: plugin typecheck in CI open as PR #48 (turn 2)
- routed (todo) merge-escape-edit-hook-pr-49: escape edit hook open as PR #49 (turn 2)
- routed (todo) merge-rule-promotion-pr-50: first rule promotion open as PR #51 for issue #50 (turn 2)
- routed (todo) open-org-knowledge-pr-52: org knowledge spec and script committed without a PR (turn 2)
- skipped (missing-env) auto-mode-classifier-no-verdict: the auto mode permission classifier gave no verdict on Agent, Bash and Write, and the session paused (turn 2)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 2)
- skipped (self-resolved) test-fixture-global-hookspath: two test details adjusted, a global `core.hooksPath` and a directory status, cause not stated beyond that (turn 2)
- skipped (self-resolved) budget-test-assumed-empty-rules-block: the context budget test went red once a rule was promoted; recorded on [[wiki-rules]], not a gotcha (turn 2)

## [2026-10-02] review | removed from _review.md

- removed (guard) typecheck-harness-plugins
- removed (todo) wiki-lint-backslash-code-paths
- removed (guard) user-settings-apply-to-headless-claude-runs
- removed (todo) phase-2-pendencies
- removed (rule) review-each-pr-with-a-subagent-before-merging
- removed (todo) finish-rejection-memory-pr-44
- removed (todo) close-resolved-review-items
- removed (todo) merge-typecheck-plugins-pr-48
- removed (todo) merge-escape-edit-hook-pr-49
- removed (todo) merge-rule-promotion-pr-50
- removed (todo) open-org-knowledge-pr-52

## [2026-10-02] distill | session b5b6fb27 | nothing kept

Part 2 holds one captured turn: a handoff prompt restating the merged PRs and the open review gate PR #56 (since merged), clipped before any new finding.
## [2026-10-02] cleanup | company-internal name removed (#63)

The user asked that the name of a company-internal starter kit appear nowhere in this public repository, and approved redacting it, once, in this log and in raw captures, which are otherwise append-only and immutable. Bodies only; frontmatter untouched. Git history still holds the name.

- updated: [[company-internal-material-stays-out-of-the-public-repo]], [[session-2026-09-30-230a182d]], [[session-2026-09-30-c14af01e]], [[session-2026-10-01-b5b6fb27]]
- redacted: the `omoikane-knowledge-for-*` todo line above (slug now `omoikane-knowledge-for-redacted`), `omoikane/raw/sources/sessions/2026-09-30-230a182d.md`, `2026-09-30-c14af01e.md`, `2026-10-01-b5b6fb27.md`

## [2026-10-02] review | removed from _review.md

- removed (todo) switch-on-autonomous-loop
- removed (todo) omoikane-knowledge-for-redacted
- removed (todo) finish-review-gate-45

## [2026-10-02] ingest | 2026-10-02 Omoikane objective

Created: [[2026-10-02-omoikane-objective]], [[omoikane-objective]], [[omoikane-holds-its-systems-domain-knowledge-itself]].
Updated: [[company-internal-material-stays-out-of-the-public-repo]], [[session-2026-10-01-b5b6fb27]].

## [2026-10-02] distill | session d4302021

Created: [[session-2026-10-01-d4302021]], [[review-gate]].
Updated: [[omoikane-objective]], [[omoikane-holds-its-systems-domain-knowledge-itself]], [[company-internal-material-stays-out-of-the-public-repo]], [[wiki-ingest]], [[wiki-rules]].

- routed (todo) review-gate-known-limits: four review gate limits recorded on PR #56 and not fixed (turn 4)
- skipped (decided) omoikane-knowledge-for-redacted: the todo to reuse Omoikane knowledge in the company kit, already removed by #58 and reversed by the user (turn 6)
- skipped (no-root-cause) gh-pr-merge-delete-branch-removes-worktree: the agent noted `gh pr merge --delete-branch` had removed the worktree and the local branch; not checked (turn 4)
- skipped (one-off) kit-draft-clone-deleted: a clean local clone of the company kit deleted after checking it had no changes (turn 3)

## [2026-10-02] distill | session 1b324082

Created: [[session-2026-10-02-1b324082]], [[redact-captures-when-they-are-written]], [[capture-redaction-breaks-on-frontmatter-clips-and-encodings]], [[new-system-starts-with-an-empty-memory]], [[objective-criterion-stays-out-of-agents-md]].
Updated: [[omoikane-objective]], [[omoikane-holds-its-systems-domain-knowledge-itself]], [[company-internal-material-stays-out-of-the-public-repo]], [[session-capture]], [[wiki-lint]], [[session-context]].

- routed (todo) second-domain-distill-eval: the second headless distill eval over `distill-domain-session-2.md` was killed for low memory and never ran (turn 5)
- skipped (missing-env) low-memory-kills-background-runs: Claude Code killed three background test and eval runs because the machine ran low on memory (turn 4)
- skipped (no-root-cause) auto-mode-classifier-denial: an action was denied by the auto mode classifier, which gave no explanation (turn 3)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 3)
- skipped (self-resolved) chained-sleep-blocked: `sleep 240` before a `tail` was blocked by the harness, which asks for Monitor or run_in_background (turn 3)

## [2026-10-02] synthesize | 6 sessions

Created: [[run-a-headless-eval-in-a-throwaway-clone-before-a-prompt-pr]], [[stop-and-ask-at-every-decidir-in-a-handoff-prompt]].
Updated: [[review-each-pr-with-a-subagent-before-merging]] (sessions 230a182d, b5b6fb27, d4302021, 1b324082), [[session-2026-10-02-1b324082]], [[session-2026-10-01-d4302021]], [[session-2026-10-01-b5b6fb27]] (links to the practices).

- routed (rule) stop-and-ask-at-every-decidir-in-a-handoff-prompt: mark user choices DECIDIR in handoff prompts, stop and ask at each one received (sessions 230a182d, b5b6fb27, d4302021, 1b324082; turns 4, 2, 3, 3)
- dropped (known) write-before-read-tool-error: skipped in three distills; the Write tool itself refuses a write before a read
- dropped (not-imperative) auto-mode-classifier-denial: denials and a missing verdict from the auto mode classifier in e04462b2, b5b6fb27 and 1b324082, with no cause an agent could act on
- dropped (known) issue-branch-worktree-pr: every session worked one issue, branch and `$TEMP` worktree per PR, the flow the user's global git rules route to the `git-workflow` skill
- dropped (known) red-test-first: every session wrote failing tests first, already required by the user's global CLAUDE.md
- dropped (known) scan-captures-before-publishing: d4302021 and 1b324082 checked captures for the company kit's name before a public push; covered by [[company-internal-material-stays-out-of-the-public-repo]]
- dropped (not-imperative) handoff-prompt-at-session-end: c14af01e, d4302021 and 1b324082 wrote a handoff prompt because the user asked for one
- dropped (one-session) kill-the-class-with-a-guard: stated only in 230a182d turn 2, and the user's global CLAUDE.md already says to automate a repeated class of problem
- dropped (not-imperative) prompt-eval-rule: [[run-a-headless-eval-in-a-throwaway-clone-before-a-prompt-pr]] governs only prompt PRs, not most tasks, so no rule is filed

## [2026-10-02] ingest | 2026-10-02 Omoikane references

Created: [[2026-10-02-omoikane-references]], [[omoikane-references]].
Updated: [[omoikane-objective]].

## [2026-10-02] distill | session a8b45323

Created: [[session-2026-10-02-a8b45323]], [[secret-redaction-patterns-leak-swallow-and-backtrack]], [[lint-findings-the-scheduled-agent-cannot-fix-are-warnings]], [[brief-floors-only-the-rule-and-lesson-sections]], [[new-system-inherits-conventions-with-from]], [[bootstrap]].
Updated: [[review-gate]], [[session-capture]], [[session-context]], [[wiki-rules]], [[wiki-lint]], [[new-system-starts-with-an-empty-memory]], [[omoikane-holds-its-systems-domain-knowledge-itself]], [[run-a-headless-eval-in-a-throwaway-clone-before-a-prompt-pr]].

- routed (todo) auto-merge-wiki-pr-74: auto-merge of the `wiki/auto` PR blocked by the permission classifier, left for the user (turn 2)
- routed (todo) close-second-domain-distill-eval: the second domain distill eval ran and passed; the older todo can go (turn 2)
- routed (todo) cut-realignment-prompt: the user's realignment prompt is cut by the capture (turn 2)
- skipped (no-root-cause) auto-mode-classifier-denial: the auto mode classifier denied an action without an explanation (turn 2)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 2)
- skipped (self-resolved) chained-sleep-blocked: `sleep 60` before a `cat` was blocked by the harness, which asks for Monitor or run_in_background (turn 2)
- skipped (self-resolved) gh-no-github-remote-in-eval-clone: `gh` could not determine the repository in a clone whose remote is a local path (turn 2)

## [2026-10-02] ingest | 2026-10-02 STE and oversight posts

Created: [[2026-10-02-ste-and-oversight-posts]], [[asd-ste100]], [[domain-glossary]].
Updated: [[omoikane-objective]].

## [2026-10-02] distill | session 04edad59

Created: [[session-2026-10-02-04edad59]].
Updated: [[bootstrap]].

- routed (todo) cut-continuation-prompt: the user's turn-2 continuation prompt is cut by the capture inside the PR #84 item (turn 2)
- routed (todo) close-cut-realignment-prompt: the realignment gaps are closed; the older cut-prompt todo may be obsolete (turn 4)
- skipped (self-resolved) sed-i-blocked-by-escape-edit-guard: `escape-edit-guard.py` blocked a `sed -i`, as designed; the agent rewrote the step (turn 3)

## [2026-10-05] distill | session 680ff986

Created: [[session-2026-10-02-680ff986]].
Updated: [[omoikane-references]].

- routed (todo) handoff-proposals-680ff986: the turn-5 handoff prompt's proposals are cut by the capture; check they were done or dropped (turn 5)
- skipped (self-resolved) x-posts-read-through-fxtwitter: X blocked direct reading of two posts; the agent read them through `api.fxtwitter.com` after retries, cause of the first failures not shown (turn 4)
## [2026-10-06] review | removed from _review.md

- removed (guard) typecheck-harness-plugins
- removed (todo) wiki-lint-backslash-code-paths
- removed (guard) user-settings-apply-to-headless-claude-runs
- removed (todo) switch-on-autonomous-loop
- removed (todo) phase-2-pendencies
- removed (todo) omoikane-knowledge-for-redacted
- removed (rule) review-each-pr-with-a-subagent-before-merging
- removed (todo) finish-rejection-memory-pr-44
- removed (todo) finish-review-gate-45
- removed (todo) close-resolved-review-items
- removed (todo) merge-typecheck-plugins-pr-48
- removed (todo) merge-escape-edit-hook-pr-49
- removed (todo) merge-rule-promotion-pr-50
- removed (todo) open-org-knowledge-pr-52

## [2026-10-06] distill | session a9384e33

Created: [[session-2026-10-02-a9384e33]], [[gh-pr-merge-auto-merges-at-once-when-no-check-is-required]], [[scheduled-task-opens-a-powershell-window]], [[wiki-auto-pr-merges-itself-once-checks-pass]], [[machine-local-paths-stay-out-of-the-public-repo]].
Updated: [[review-each-pr-with-a-subagent-before-merging]] (evidence), [[python-heredoc-edits-corrupt-backslash-n]] (recurrence), [[wiki-ingest]] (scheduling).

- routed (todo) merge-prs-92-to-95: PRs #92 to #95 reviewed and waiting for the user's merge (turn 9)
- routed (todo) capture-keeps-machine-local-path: the raw capture keeps the machine-local path the user kept out of the repo (turn 2)
- routed (todo) wiki-auto-pages-missing-on-main: the objective criterion and review-gate pages exist only on `wiki/auto` (PR #59) (turn 2)
- routed (todo) review-59-corrections-cut: the #59 review corrections are cut in the capture (turn 9)
- routed (todo) domain-glossary-stale-after-90: `domain-glossary` on `wiki/auto` goes stale when #90 merges (turn 7)
- routed (todo) persist-local-clones-memory-line: `~/.claude/CLAUDE.md` is overwritten by `agent-dotfiles` `sync-config`; the memory line must move there (turn 2)
- skipped (no-root-cause) unittest-suite-fails-under-parallel-load: the full suite failed once while other suites ran, the suspect tests passed alone, cause not found (turn 2)
- skipped (no-root-cause) s4u-task-loses-gh-and-claude-logins: a task run without the user logged on was expected to lose the `gh` and `claude` logins, not tested (turn 8)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 2)
- skipped (self-resolved) read-missing-file: `File does not exist` on one read (turn 2)
- skipped (self-resolved) stray-git-stash-hid-an-edit: a `git stash` left in a command hid the #95 `AGENTS.md` edit, restored with `git stash pop` (turn 9)
- skipped (self-resolved) background-grep-exit-1: a background run reported exit 1 from its last `grep` finding no failure (turn 9)
- skipped (one-off) stop-hook-child-survival-prototype: a throwaway probe of whether a process started by a Stop hook outlives Claude Code; result not in the capture (turn 10)
- skipped (task-only) hide-the-scheduled-task-window: "quero que a janela fique escondida caso essa seja a unica forma de alimentar o Omoikane de forma autonoma" (turn 10)

## [2026-10-06] distill | session 1de79b19

Created: [[session-2026-10-05-1de79b19]], [[ask-searches-origin-main-history-before-asking-for-a-source]], [[proposed-guards-name-the-fix-and-prefer-lint-or-test]], [[git-bash-rewrites-a-leading-slash-argument-into-a-path]], [[pstack]].
Updated: [[python-heredoc-edits-corrupt-backslash-n]] (recurrence), [[review-each-pr-with-a-subagent-before-merging]] (evidence).

- routed (todo) merge-prs-99-and-100: PRs #99 and #100 reviewed with green CI and waiting for the user's merge (turn 3)
- routed (todo) confirm-pr-99-review-is-final: the #99 "no findings" review was posted while the reviewer had not reported yet (turn 3)
- skipped (self-resolved) ask-eval-api-529: the "after" `/ask` eval failed with API 529 and the rerun passed (turn 1)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 1)
- skipped (self-resolved) eval-fixture-session-id-renamed: the eval renamed `2026-10-02-eva1d0m.md` to `2026-10-02-0eva1d0m.md` before the run, reason not stated (turn 1)

## [2026-10-06] wrap-up | 2026-09-29 to 2026-10-06

- distill omoikane/raw/inbox/sessions/2026-10-02-a9384e33.md
- distill omoikane/raw/inbox/sessions/2026-10-05-1de79b19.md
- left in inbox: omoikane/raw/inbox/sessions/2026-10-06-180e52eb.md, its session was still open (a turn landed after the human answered)
- commits: 124 read, 9 used. Created [[commits-2026-09-29-to-2026-10-06]], [[review-conflicts-keep-mains-file-plus-whole-added-runs]], [[git-config-and-info-are-shared-by-every-worktree]], [[domain-page-type-holds-the-rules-the-user-states]]. Updated [[headless-scope]], [[python-heredoc-edits-corrupt-backslash-n]]. 70 commits fall in captures on main, 4 in the open session 180e52eb; of the other 41, most are covered by pages on origin/wiki/auto (PR #59), the rest are docs, reverted (45fd881), reasons already in code comments (0109a08, 7da75d1) or waiting on #59 (40c7e37, b63a6fb, ec6aa80, 0888cb2, ece1f62)
- routed (prompt) wrap-up-commit-coverage-misses-wiki-auto-captures: step 3 misses captures distilled onto origin/wiki/auto and over-trusts the capture's branch (commit 87d956b)
- routed (todo) commits-pages-waiting-on-wiki-auto: review-gate, wiki-lint and secret-redaction pages on origin/wiki/auto lack what these commits add (commit d263fcf)
- skipped (self-resolved) review-removals-misread-lint-items: lint items without the word "guard" read as removed; parser fixed (commit 26d36c0)

## [2026-10-07] review | removed from _review.md

- removed (todo) pi-omoikane-commands

## [2026-10-07] distill | session 180e52eb

Created: [[session-2026-10-06-180e52eb]], [[wiki-is-fed-by-an-end-of-day-wrap-up-the-schedule-is-opt-in]], [[git-log-since-a-bare-date-starts-at-the-current-time-of-day]], [[wrap-up]].
Updated: [[wiki-ingest]] (opt-in, task removed), [[scheduled-task-opens-a-powershell-window]] (status), [[wiki-auto-pr-merges-itself-once-checks-pass]] (status), [[review-each-pr-with-a-subagent-before-merging]] (evidence), [[run-a-headless-eval-in-a-throwaway-clone-before-a-prompt-pr]] (evidence), [[python-heredoc-edits-corrupt-backslash-n]] (recurrence).

- skipped (no-root-cause) background-suite-left-unchecked-when-session-ended: the #96 session ended while its suite ran in background; "A causa provável é que o agente encerrou o turno esperando o job" (turn 2)
- skipped (self-resolved) agents-md-lines-over-worst-case-budget: the new `AGENTS.md` lines went 25 tokens over the worst-case budget; the suite caught it and the lines were shortened (turn 5)
- skipped (self-resolved) test-context-budget-import-error: `python -m unittest test_context_budget` named a test module that does not exist (turn 5)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 6)
- skipped (self-resolved) sleep-chain-blocked-by-harness: `sleep 60` before `gh pr checks` was blocked; the wait ran in background (turn 6)

## [2026-10-07] ingest | 2026-10-06 pstack is an Omoikane reference

Created: [[2026-10-06-pstack-is-an-omoikane-reference]].
Updated: [[omoikane-references]] (pstack as fourth reference, what it gave), [[pstack]] (reference status, unread skills, PR merges), [[omoikane-objective]] (fourth reference), [[proposed-guards-name-the-fix-and-prefer-lint-or-test]] (PR #99 merged), [[ask-searches-origin-main-history-before-asking-for-a-source]] (PR #100 merged, per git `0118646`).

## [2026-10-07] distill | session 61eabe29

Created: [[session-2026-10-06-61eabe29]], [[wiki-auto-auto-merge-dropped-with-pr-92]], [[green-pr-ci-can-be-stale-against-the-current-main]], [[gh-pr-merge-match-head-commit-needs-the-full-sha]].
Updated: [[wiki-auto-pr-merges-itself-once-checks-pass]] (reversed, history), [[gh-pr-merge-auto-merges-at-once-when-no-check-is-required]] (#92 closed, repo settings), [[wiki-is-fed-by-an-end-of-day-wrap-up-the-schedule-is-opt-in]] (consequences done), [[review-gate]] (auto-merge dropped, #59 merged), [[wiki-ingest]] (#92 closed), [[wiki-rules]] (budget at 2796 of 2800), [[review-each-pr-with-a-subagent-before-merging]] (evidence), [[omoikane-references]] (session as source), [[pstack]] (handoff prompt for the unread skills).

- routed (todo) close-merge-prs-92-to-95: #94 and #95 merged, #92 closed; the older todo can go (turn 7)
- routed (todo) close-auto-merge-wiki-pr-74: #74 and #92 closed as superseded by #101; the older todo can go (turn 6)
- routed (todo) close-wiki-auto-pages-missing-on-main: PR #59 merged; the older todo can go and two waiting todos can run (turn 7)
- routed (todo) close-merge-prs-99-and-100: #99 merged in the session, #100 merged before; the older todo can go (turn 6)
- routed (todo) local-clones-path-lost: the local reference clones line is gone from `~/.claude/CLAUDE.md` (turn 8)
- routed (todo) ste-posts-missing-from-references-list: the STE posts are not on the references list and the user did not decide (turn 8)
- skipped (self-resolved) chained-sleep-blocked: `sleep 240` before a `tail` was blocked by the harness, which asks for Monitor or run_in_background (turn 2)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 4)
- skipped (self-resolved) sed-i-blocked-by-escape-edit-guard: `escape-edit-guard.py` blocked a `sed -i`, as designed; the agent rewrote the step (turn 4)
- skipped (self-resolved) merge-abort-fails-on-an-edited-file: "error: Entry 'AGENTS.md' not uptodate. Cannot merge." in `omoikane-ste`; cleared with `git checkout -- AGENTS.md` before `git merge --abort`, cause not stated (turn 6)

## [2026-10-07] ingest | 2026-10-06 pstack skills review round 2

Created: [[2026-10-06-pstack-skills-review-round-2]].
Updated: [[pstack]] (round 2 verdicts, what proposals 1 to 3 gave, rejections reopened by #111), [[omoikane-references]] (round 2 outcomes), [[session-capture]] (capture failures), [[wiki-lint]] (review diff check, quote audit proposed), [[wiki-auto-auto-merge-dropped-with-pr-92]] (contradiction on #92).

## [2026-10-07] distill | session fd3ff955

Created: [[session-2026-10-06-fd3ff955]], [[proposals-that-add-always-loaded-text-name-what-leaves]].
Updated: [[pstack]] (turn-3 recommendation, handoff to #103 to #106), [[session-capture]] (prompt cut at 2000 characters, #104).

- routed (todo) cut-pstack-review-prompt: the user's turn-2 prompt is cut by the capture inside the "agrega" criterion (turn 2)
- skipped (task-only) read-only-pstack-review: "Esta tarefa é só leitura e análise: não altere código, prompts nem o wiki" (turn 2)
- skipped (task-only) clone-pstack-outside-the-repository: clone pstack into a temporary folder outside the repository for this review (turn 2)
- skipped (one-off) quote-audit-measurement-script: throwaway script in `$TEMP` comparing wiki quotes with raw captures, 31 of 32 matched (turn 2)

## [2026-10-07] distill | session 973284b2

Created: [[session-2026-10-06-973284b2]], [[reshaping-capture-text-before-redaction-leaks-secrets]], [[opencode-read-tool-cuts-lines-at-2000-characters]], [[python-text-mode-stdin-writes-crlf-on-windows]], [[git-merge-no-commit-needs-a-committer-identity]], [[update-from-template]].
Updated: [[session-capture]] (#107 and #109 review fixes, headless runs write no errors file, cut measurements), [[session-context]] (capture failure line, worst-case brief), [[wiki-lint]] (diff check findings and #110 review fixes), [[capture-redaction-breaks-on-frontmatter-clips-and-encodings]] (ANSI list), [[secret-redaction-patterns-leak-swallow-and-backtrack]] (curl and mysql scans), [[python-heredoc-edits-corrupt-backslash-n]] (recurrence), [[review-each-pr-with-a-subagent-before-merging]] (evidence).

- routed (guard) wrapped-line-splits-a-name-from-its-secret: wrapping before redaction leaked a `password =` value; no test fails on that order (turn 2)
- routed (todo) cut-four-issues-handoff-prompt: the turn-2 handoff prompt is cut inside item (A) by the capture (turn 2)
- skipped (task-only) context-budget-before-and-after-each-pr: "Rode `python omoikane/bin/context-budget.py` antes e depois de cada PR. Nenhum item deve mudar o `AGENTS.md` nem o page contract." (turn 2)
- skipped (self-resolved) stray-git-stash-hid-an-edit: "fiz `stash` no worktree de (C) em vez de commit", restored with `stash pop` and committed (turn 2)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 2)
- skipped (self-resolved) file-modified-since-read-tool-error: `File has been modified since read` from the Write tool (turn 2)

## [2026-10-07] distill | session 062e80af

Created: [[session-2026-10-07-062e80af]], [[every-system-ships-the-development-skills]], [[omoikane-mode-routes-each-task-to-a-playbook]], [[pi-expands-a-skill-command-into-a-skill-block]], [[pi-loads-loose-markdown-in-a-skills-folder-as-a-skill]], [[node-on-windows-lacks-o-nofollow-and-o-nonblock]], [[cloudflare-security-audit-skill]].
Updated: [[omoikane-objective]] (software-development toolkit, old rule under History), [[omoikane-references]] (two Cloudflare references, pstack restated), [[objective-criterion-stays-out-of-agents-md]] (PR #113 opening), [[new-system-starts-with-an-empty-memory]] (LICENSE moved), [[pstack]] (issue #111), [[pi-coding-agent]] (skills), [[session-capture]] (Pi skill command), [[session-context]] (omoikane-mode reminder), [[wiki-rules]] (skill budget), [[review-each-pr-with-a-subagent-before-merging]] (evidence), [[green-pr-ci-can-be-stale-against-the-current-main]] (stack of PRs).

- routed (todo) personal-skills-shadow-template-copies: 12 vendored skills also sit in `~/.claude/skills/`; keep or drop the personal copies (turn 3)
- routed (todo) pi-skill-capture-live-check: the Pi `/skill:` capture fix was never checked on a real Pi session file (turn 6)
- routed (todo) security-audit-upstream-pr-69: return the vendored copy to upstream once cloudflare/security-audit-skill#69 merges (turn 10)
- routed (todo) security-audit-windows-promotion-step: check whether the skill's POSIX artifact promotion needs a Windows step (turn 3)
- skipped (self-resolved) sed-i-blocked-by-escape-edit-guard: `escape-edit-guard.py` blocked a `sed -i`, as designed; the agent rewrote the step (turn 3)
- skipped (self-resolved) python-heredoc-blocked-by-escape-edit-guard: `escape-edit-guard.py` blocked a Python heredoc with `\n`, as designed (turn 6)
- skipped (self-resolved) edit-string-not-found: the Edit tool did not find `licence=True), "", ` in the test file; the agent read the file again (turn 6)
- skipped (self-resolved) grep-empty-filename: `grep: : No such file or directory` from an empty variable in a command (turn 6)
- skipped (self-resolved) write-before-read-tool-error: `File has not been read yet` from the Write tool (turn 8)
- skipped (self-resolved) git-c-worktree-add-relative-path: `git -C omoikane worktree add omk-112` put the worktree inside `omoikane/`, so `cd omk-112` failed; an absolute path fixed it (turn 9)
- skipped (self-resolved) integration-run-failed-cause-not-captured: the first integration run of all #111 PRs failed with exit code 1; the capture does not show why, and the next run passed (turn 11)

## [2026-10-07] ingest | 2026-10-07 Omoikane objective widens to a work toolkit

Created: [[2026-10-07-omoikane-objective-widens-to-a-work-toolkit]].
Updated: [[omoikane-references]] (author and date of the Cloudflare post), [[every-system-ships-the-development-skills]] (skill sources at their commits), [[pstack]] (the user's belief that pstack is tied to Grok Bot or Cursor).

## [2026-10-07] distill | session 9e3fae7e

Created: [[session-2026-10-07-9e3fae7e]], [[gh-pr-merge-delete-branch-closes-prs-stacked-on-it]].
Updated: [[green-pr-ci-can-be-stale-against-the-current-main]] (upper branches without the base's last commit), [[review-each-pr-with-a-subagent-before-merging]] (merge of the #111 stack, merge-commit statement, retarget first), [[session-context]] (brief at 3903 of 4000), [[cloudflare-security-audit-skill]] (#69 open, Windows job), [[session-2026-10-07-062e80af]] (link to the merge session).

- routed (guard) gh-pr-merge-delete-branch-closes-prs-stacked-on-it: `--delete-branch` on a stack's base closed #113; a hook could block it while open PRs target the branch (turn 3)
- routed (todo) close-issue-111-after-wrap-up: close #111 by hand after this wrap-up when its acceptance criteria hold (turn 2)
- routed (todo) omoikane-mode-live-check: check `/skill:omoikane-mode` in Pi and `/omoikane-mode` in OpenCode live, note the result in the inbox (turn 2)
- routed (todo) remove-stale-worktrees-103-to-106: worktrees `omoikane-103` to `-106` and the pre-pull backup remain (turn 2)
- skipped (no-root-cause) gh-pr-merge-delete-branch-removes-worktree: the worktree `.claude/worktrees/agent-a474e9bd5d71689c8` and the local branch `feat/111-design-skills` vanished during the merges; the agent did not find which step removed them (turn 3)
- skipped (no-root-cause) auto-mode-classifier-denial: the auto mode classifier blocked `git push origin --delete docs/111-dev-pack-spec` and gave no explanation; the user ran it (turn 3)
- skipped (no-root-cause) review-md-crlf-pull-conflict: the pull of `main` conflicted on the local `_review.md`, which the agent stripped of CR before merging; the capture does not show what wrote the CRs (turn 3)

## [2026-10-07] synthesize | 10 sessions

Sessions read: 9e3fae7e, 062e80af, fd3ff955, 973284b2, 61eabe29, 180e52eb, 1de79b19, a9384e33, 680ff986, 04edad59.
Created: [[recommend-an-option-and-wait-for-the-go-ahead]], [[remove-the-worktree-of-a-merged-pr-with-git-worktree-remove]], [[retest-a-pr-on-the-current-main-before-merging-it]].
Updated: [[review-each-pr-with-a-subagent-before-merging]] (session 04edad59, links to the two merge practices), [[run-a-headless-eval-in-a-throwaway-clone-before-a-prompt-pr]] (before and after runs, sessions a9384e33 and 1de79b19), [[stop-and-ask-at-every-decidir-in-a-handoff-prompt]] (link), [[green-pr-ci-can-be-stale-against-the-current-main]] (link).

- routed (guard) retest-pr-on-current-main: a hook on `gh pr merge` that blocks when the PR's head lacks the current `origin/main` (sessions 61eabe29, 062e80af, 9e3fae7e; turns 6, 10, 2)
- routed (rule) recommend-an-option-and-wait-for-the-go-ahead: recommend one option with its reason and act after the user approves (sessions 680ff986, 180e52eb, 61eabe29, fd3ff955, 062e80af, 9e3fae7e)
- routed (rule) machine-local-paths-stay-out-of-the-public-repo: domain page created since the last synthesize; any committed file can break it (session a9384e33, turn 2)
- dropped (known) write-before-read-tool-error: skipped in six more distills; the Write tool refuses the write and names the fix
- dropped (known) auto-mode-classifier-denial: a8b45323, 062e80af and 9e3fae7e left the denied action to the user; the harness permission rules already forbid working around a denial
- dropped (known) sed-i-blocked-by-escape-edit-guard: 04edad59, 61eabe29 and 062e80af; `escape-edit-guard.py` blocks it, and [[python-heredoc-edits-corrupt-backslash-n]] holds the lesson
- dropped (known) chained-sleep-blocked: 1b324082, a8b45323, 61eabe29, and 180e52eb as `sleep-chain-blocked-by-harness`; the harness blocks it and names Monitor or run_in_background
- dropped (coincidence) stray-git-stash-hid-an-edit: a stash inside a compound command (a9384e33, turn 9) and a stash typed for a commit (973284b2, turn 2); both undone with `git stash pop`
- dropped (coincidence) gh-pr-merge-delete-branch-removes-worktree: d4302021 ran its own `git worktree remove $wt` after the merge; 9e3fae7e lost a Claude Code agent worktree under `.claude/worktrees/`; no common cause shown
- dropped (not-imperative) handoff-prompt-at-session-end: seven sessions wrote one because the user asked, "Me envie um prompt para eu jogar em outra sessão"; their recurring content is the review, DECIDIR and recommendation practices
- dropped (known) cut-prompt-todos: a8b45323, 04edad59, 680ff986, fd3ff955 and 973284b2 each filed a cut-prompt todo; commit `1a946fe` raised the capture's prompt limit to 20,000 characters
- dropped (known) omoikane-objective: [[objective-criterion-stays-out-of-agents-md]] keeps the criterion out of `AGENTS.md`
- dropped (narrow) omoikane-references: governs changes to prompts, scripts, the page contract and hooks; the user rejected it in `AGENTS.md`
- dropped (narrow) proposals-that-add-always-loaded-text-name-what-leaves: governs only changes to always-loaded text, and `context-budget.py` fails CI when that text grows past its budget
- dropped (narrow) retest-pr-rule: [[retest-a-pr-on-the-current-main-before-merging-it]] governs merges only, which the promoted review rule gates; filed as a guard
- dropped (narrow) worktree-cleanup-rule: [[remove-the-worktree-of-a-merged-pr-with-git-worktree-remove]] governs the cleanup after a merge only

## [2026-10-07] wrap-up | 2026-10-06 to 2026-10-07

- distill omoikane/raw/inbox/sessions/2026-10-06-180e52eb.md
- ingest omoikane/raw/inbox/2026-10-06-pstack-is-a-reference.md
- distill omoikane/raw/inbox/sessions/2026-10-06-61eabe29.md
- ingest omoikane/raw/inbox/2026-10-06-pstack-skills-review.md
- distill omoikane/raw/inbox/sessions/2026-10-06-fd3ff955.md
- distill omoikane/raw/inbox/sessions/2026-10-06-973284b2.md
- distill omoikane/raw/inbox/sessions/2026-10-07-062e80af.md
- ingest omoikane/raw/inbox/2026-10-07-omoikane-becomes-a-toolkit.md
- distill omoikane/raw/inbox/sessions/2026-10-07-9e3fae7e.md
- commits: 37 read, 1 used. Created [[commits-2026-10-06-to-2026-10-07]]. Updated [[omoikane-mode-routes-each-task-to-a-playbook]]. All 37 fall inside captures (4 in 180e52eb, 1 in 61eabe29, 10 in 973284b2, 22 in 062e80af); only 15cbeb5 states a reason its session page lacks
- synthesize
