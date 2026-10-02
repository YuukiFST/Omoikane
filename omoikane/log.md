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
