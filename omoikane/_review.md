# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

A bullet with a checkbox is a proposal: a guard or a prompt change, with its diff below it. Tick `[x]` to approve; an interactive session applies ticked proposals and deletes their bullets, and a scheduled run never does. Delete an unticked bullet to reject it.

## [2026-09-30] distill | session e04462b2

- [ ] guard (test) typecheck-harness-plugins: `.pi/extensions/omoikane.ts` and `.opencode/plugins/omoikane.ts` are never typechecked, so a wrong import or hook signature reaches `main` (session e04462b2, turn 4)
  No diff: the session typechecked them only in a scratch `/tmp/tscheck` project whose `tsconfig.json` is not in the transcript. The check goes in `.github/workflows/ci.yml` as a step that installs `typescript`, `@opencode-ai/plugin@1.18.30` and `@earendil-works/pi-coding-agent` and runs `tsc` over both files.
- todo pi-omoikane-commands: add `/ingest`, `/distill`, `/ask`, `/lint` commands for Pi; today Pi only captures and distill runs through `claude` or `opencode` (session e04462b2, turn 4)
- todo wiki-lint-backslash-code-paths: the `code:` existence check in `wiki-lint.py` still reads the raw path; `git_path()` already normalises it for staleness (session e04462b2, turn 4)
- todo unify-transcript-readers: merge the Claude, Pi and OpenCode readers in `session-capture.py` into one state machine (session e04462b2, turn 4)
- todo pi-live-verification: run the Pi extension live once: `pi` at the repo root, accept project trust, prompt an edit, check `omoikane/raw/inbox/sessions/` (session e04462b2, turn 4)

## [2026-09-30] distill | session c14af01e

- [ ] guard (test) user-settings-apply-to-headless-claude-runs: dropping `--setting-sources project`, `dontAsk` or the git deny from `wiki-ingest.ps1` reopens `git` in the headless run and no test fails (session c14af01e, turn 2)
  Not checked with `git apply --check`: the distill run could not write a scratch file. It only adds a new file.
````diff
--- /dev/null
+++ b/tests/test_wiki_ingest.py
@@ -0,0 +1,19 @@
+"""Headless tests for omoikane/bin/wiki-ingest.ps1. Run: python -m unittest discover -s tests"""
+from __future__ import annotations
+
+import unittest
+from pathlib import Path
+
+SCRIPT = (Path(__file__).resolve().parent.parent / "omoikane" / "bin" / "wiki-ingest.ps1").read_text(encoding="utf-8")
+
+
+class HeadlessScope(unittest.TestCase):
+    def test_the_claude_call_ignores_user_settings_and_denies_git(self) -> None:
+        # User-level allow rules and hooks let git through in the headless run (#25).
+        for flag in ("--setting-sources project", "--permission-mode dontAsk",
+                     '--disallowedTools "Bash(git *),PowerShell(git *)"'):
+            self.assertIn(flag, SCRIPT)
+
+
+if __name__ == "__main__":
+    unittest.main()
````
- todo switch-on-autonomous-loop: turn the scheduled loop on; the captured sessions are distilled in PR #36 (session c14af01e, turn 4)
- todo phase-2-pendencies: resolve the Phase 2 pendencies listed in the turn 4 handoff prompt; the capture clipped the list, the full list is in the Claude Code transcript of session 8d85e27b-aca9-4ada-83a4-be17c14af01e (session c14af01e, turn 4)
- todo omoikane-knowledge-for-sb360-kit: design how Omoikane knowledge becomes company knowledge reusable across sb360-kit systems, such as database rules (session c14af01e, turn 4)

## [2026-10-01] distill | session 230a182d

- todo finish-rejection-memory-pr-44: PR #44 (`review-removals.py`, issue #41) was open at capture and `review-removals.py` is not in this checkout (session 230a182d, turn 2)
- todo finish-review-gate-45: the review gate (`review-gate.py`, branch `feat/45-review-gate`, worktree `omoikane-wiki-auto` on `wiki/auto`) was unmerged at capture; register the scheduled task with `install-schedule.ps1` only after it lands (session 230a182d, turn 4)
- todo close-resolved-review-items: PR #33 resolved `wiki-lint-backslash-code-paths`; `tests/test_headless_scope.py` (`test_user_settings_and_mcp_servers_are_ignored`) now pins what the unticked `user-settings-apply-to-headless-claude-runs` guard proposed, and its diff no longer applies since `tests/test_wiki_ingest.py` exists; `phase-2-pendencies` was worked through in this session. Delete the bullets that are done (session 230a182d, turn 2)

## [2026-10-01] distill | session b5b6fb27

- todo merge-typecheck-plugins-pr-48: PR #48 (issue #46, `test/46-typecheck-plugins`) typechecks the plugins in CI and was open at capture; once merged, delete the `typecheck-harness-plugins` bullet above and set `guard: test` on [[typescript-misnamed-plugin-hook-passes-without-satisfies]] (session b5b6fb27, turn 2)
- todo merge-escape-edit-hook-pr-49: PR #49 (issue #47, `feat/47-escape-hook`) adds `.claude/hooks/escape-edit-guard.py` and was open at capture; once merged, set `guard: hook` on [[python-heredoc-edits-corrupt-backslash-n]] (session b5b6fb27, turn 2)
- todo merge-rule-promotion-pr-50: PR #50 promotes `review-each-pr-with-a-subagent-before-merging` into `AGENTS.md` and was open at capture; once merged, delete the synthesize `rule` bullet below (session b5b6fb27, turn 2)
- todo open-org-knowledge-pr-52: `docs/specs/2026-10-01-org-knowledge.md` and `omoikane/bin/org-candidates.py` are committed on `feat/52-org-candidates` (issue #52) with no PR; the session left it for after Block 2 (#44, #45) (session b5b6fb27, turn 2)
