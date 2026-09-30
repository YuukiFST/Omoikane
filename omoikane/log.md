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
- routed (todo) omoikane-knowledge-for-sb360-kit: make Omoikane knowledge reusable as company knowledge in sb360-kit (turn 4)
- skipped (self-resolved) remove-item-protected-path: `Remove-Item` on `omoikane/wiki/*` blocked as a protected path, eval clones cleared with `-LiteralPath` instead (turn 2)
- skipped (one-off) eval-clone-planted-regression: `/lint` in an eval clone found a regression the agent introduced in the clone copy (turn 2)
