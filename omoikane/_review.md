# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

A bullet with a checkbox is a proposal: a guard or a prompt change, with its diff below it. Tick `[x]` to approve; an interactive session applies ticked proposals and deletes their bullets, and a scheduled run never does. Delete an unticked bullet to reject it.

## [2026-09-30] distill | session e04462b2

- [ ] guard (test) typecheck-harness-plugins: `.pi/extensions/omoikane.ts` and `.opencode/plugins/omoikane.ts` are never typechecked, so a wrong import or hook signature reaches `main` (session e04462b2, turn 4)
  No diff: the session typechecked them only in a scratch `/tmp/tscheck` project whose `tsconfig.json` is not in the transcript. The check goes in `.github/workflows/ci.yml` as a step that installs `typescript`, `@opencode-ai/plugin@1.18.30` and `@earendil-works/pi-coding-agent` and runs `tsc` over both files.
- todo pi-omoikane-commands: add `/ingest`, `/distill`, `/ask`, `/lint` commands for Pi; today Pi only captures and distill runs through `claude` or `opencode` (session e04462b2, turn 4)
- todo wiki-lint-backslash-code-paths: normalise backslashes in `code:` paths in `wiki-lint.py`, as `session-capture.py` now does (session e04462b2, turn 4)
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
- todo switch-on-autonomous-loop: distill the captured sessions and turn the scheduled loop on, first front of the handoff prompt (session c14af01e, turn 4)
- todo phase-2-pendencies: resolve the Phase 2 pendencies listed in the turn 4 handoff prompt; the capture clipped the list, so the human's copy of that prompt is the only full record (session c14af01e, turn 4)
- todo omoikane-knowledge-for-sb360-kit: design how Omoikane knowledge becomes company knowledge reusable across sb360-kit systems, such as database rules (session c14af01e, turn 4)
