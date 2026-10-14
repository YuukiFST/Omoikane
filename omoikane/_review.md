# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

A bullet with a checkbox is a proposal: a guard or a prompt change, with its diff below it. Tick `[x]` to approve; an interactive session applies ticked proposals and deletes their bullets, and a scheduled run never does. Delete an unticked bullet to reject it.

## [2026-09-30] distill | session e04462b2

- todo unify-transcript-readers: merge the Claude, Pi and OpenCode readers in `session-capture.py` into one state machine (session e04462b2, turn 4)

## [2026-10-02] distill | session d4302021

- todo review-gate-known-limits: four review gate limits left on PR #56: a slid hunk in a replay ends the rebase window early (medium, not verified), `settled` can stop advancing, two squashes between runs record only the first, the next PR body relists squashed commits; see [[review-gate]] (session d4302021, turn 4)

## [2026-10-02] synthesize

- [ ] rule stop-and-ask-at-every-decidir-in-a-handoff-prompt: Mark each user choice DECIDIR in a handoff prompt; at a DECIDIR you receive, stop and ask (synthesize)

## [2026-10-05] distill | session 680ff986

- todo handoff-proposals-680ff986: the turn-5 handoff prompt asks another session to carry out this session's proposals (STE-style `wiki/auto` PR body, glossary, reference clones in global memory, auto-merge #74); the capture cuts the list (`[... 5873 chars cut]`), so check they were done or dropped (session 680ff986, turn 5)

## [2026-10-06] distill | session a9384e33

- todo persist-local-clones-memory-line: the line about local reference clones sits in `~/.claude/CLAUDE.md`, which `agent-dotfiles` `sync-config` overwrites; move it into `agent-dotfiles` (session a9384e33, turn 2)

## [2026-10-07] distill | session 61eabe29

- todo local-clones-path-lost: the line about the local reference clones is no longer in `~/.claude/CLAUDE.md`, so the path is lost; write it into your own memory per [[machine-local-paths-stay-out-of-the-public-repo]], then delete `persist-local-clones-memory-line` (session 61eabe29, turn 8)
- todo ste-posts-missing-from-references-list: the agent named the STE posts ([[2026-10-02-ste-and-oversight-posts]]) as a reference missing from [[omoikane-references]]; the user answered only for pstack, so decide whether they belong on the list (session 61eabe29, turn 8)

## [2026-10-07] ingest | 2026-10-06 pstack skills review round 2

- contradiction pr-92-merge-expected-after-close: the pstack round-2 note expects "the `wiki/auto` PR merges itself (PR #92)", but #92 closed unmerged at 12:41 UTC that day; see [[wiki-auto-auto-merge-dropped-with-pr-92]] (source: [[2026-10-06-pstack-skills-review-round-2]], proposal 4)
- todo quote-audit-proposal-not-opened: proposals 1 to 3 became #105, #103 and #106 and merged; proposal 4, a `wiki-lint.py` check that a quote cited to a session turn is in its capture, has no issue; decide whether to open one (source: [[2026-10-06-pstack-skills-review-round-2]], proposal 4)

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

## [2026-10-07] distill | session 062e80af

- todo personal-skills-shadow-template-copies: 12 of the vendored skills also sit in `~/.claude/skills/` from agent-dotfiles, and Claude Code runs the personal copy; decide whether to drop them from the global set or accept the shadowing (`docs/specs/2026-10-07-software-toolkit.md`, "Personal skills of the same name") (session 062e80af, turn 3)
- todo security-audit-windows-promotion-step: the spec asks to check whether `.claude/skills/security-audit/SKILL.md`, whose artifact promotion uses no-follow descriptors and a link count of 1, needs a Windows step; the capture does not show it checked (session 062e80af, turn 3)

## [2026-10-07] distill | session 9e3fae7e

- todo close-issue-111-after-wrap-up: after this `/wrap-up` applies the toolkit note to [[omoikane-objective]] and [[omoikane-references]], close issue #111 by hand when its acceptance criteria hold; no PR closes it, all use `Refs #111` (session 9e3fae7e, turn 2)

## [2026-10-07] synthesize

- [ ] rule recommend-an-option-and-wait-for-the-go-ahead: When a choice is the user's, recommend one option with its reason; act on it only after the user approves (synthesize)
- [ ] rule machine-local-paths-stay-out-of-the-public-repo: Keep paths that hold only on this machine out of committed files; the repository is public (synthesize)

## [2026-10-08] distill | session 0ac17a0f

- [ ] guard (test) template-skills-teach-no-tdd: the template's `brainstorming` and `writing-plans` taught TDD after the user's rule made agent-written tests E2E only, and no check failed; a skill vendored again from upstream brings it back, see [[template-skills-write-e2e-tests-only]] (session 0ac17a0f, turns 7, 8; commit 7d6bd37)
  The changed `findings` runs in `test_repository_skills_match_the_manifest`; on `7d6bd37`, before PR #120, it fails on `brainstorming/SKILL.md` and `writing-plans/SKILL.md`, and on `main` it passes. No new unit case, since tests an agent writes are E2E only.
````diff
--- a/tests/test_skills_manifest.py
+++ b/tests/test_skills_manifest.py
@@ -26,6 +26,8 @@ OWN = "Omoikane"
 ROW = re.compile(r"^\|\s*([a-z][a-z0-9-]*)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|\s*$")
 NAME = re.compile(r"^name:\s*(.+?)\s*$", re.M)
 DESCRIPTION = re.compile(r"^description:\s*(.*?)\s*$", re.M)
+# Tests an agent writes are E2E only (#119); a skill vendored again from upstream can bring TDD back.
+TDD = re.compile(r"\bTDD\b|test-driven", re.I)
 
 
 def manifest_rows(text: str) -> dict[str, str]:
@@ -57,6 +59,8 @@ def findings(skills: Path, manifest: str, memory: frozenset[str] = MEMORY) -> list[str]:
             out.append(f"{name}: licence {licence} but no LICENSE file in the folder")
     out += [f"{f.name}: Markdown directly in the skills folder loads as a skill in Pi; move it into a skill folder"
             for f in sorted(skills.glob("*.md"))]
+    out += [f"{f.relative_to(skills).as_posix()}: teaches TDD; tests an agent writes are E2E only, write the E2E wording of omoikane/skills.md"
+            for f in sorted(skills.rglob("*.md")) if TDD.search(f.read_text(encoding="utf-8"))]
     for skill_md in sorted(skills.glob("*/SKILL.md")):
         folder = skill_md.parent
         if folder.name not in rows and folder.name not in memory and not SYSTEM_OWN.fullmatch(folder.name):
````

## [2026-10-08] ingest | 2026-10-07 omoikane-mode live check

- contradiction ai-tells-folder-in-opencode-run: the note says OpenCode used the personal `ai-tells` skill "from `~/.claude/skills/`", but the run's capture calls the lint under `~/.agents/skills/ai-tells/scripts/`, and both folders hold `ai-tells`; see [[2026-10-07-omoikane-mode-live-check]] (source: `omoikane/raw/sources/2026-10-07-omoikane-mode-live-check.md:16`, `omoikane/raw/sources/sessions/2026-10-07-Q7Bpg6M5.md:80`)

## [2026-10-09] distill | session 21f37812

- [ ] guard (test) git-add-omoikane-stages-the-running-sessions-own-capture: `git add omoikane/` committed the running session's capture from `omoikane/raw/inbox/sessions/`; the agent unstaged it by hand before the push, see [[git-add-omoikane-stages-the-running-sessions-own-capture]] (session 21f37812, turn 3)
  No diff: the check goes in a new case under `tests/` that runs `git ls-files omoikane/raw/inbox/sessions` and fails on any file but `.gitkeep`, with an error that names `git rm --cached <file>`. On `main` only `.gitkeep` is tracked there today. Check first that `omoikane/bin/review-gate.py`, which moves inbox captures into the `wiki/auto` worktree, never commits one that a run left undistilled.

## [2026-10-09] distill | session 261b475d

- [ ] guard (test) run-the-tests-on-windows-in-ci: `update-from-template.py` sent git its stdin in text mode, and the `AGENTS.md` stages were lost on Windows only; the CI test job runs on `ubuntu-latest`, so the test that catches it never runs there, see [[git-update-index-index-info-ignores-a-cr-ended-path-and-exits-0]] (session 261b475d, turn 2)
  On `e6b73f5^` with the new test of `e6b73f5`, this job fails; the session saw that test fail on Windows before the fix. The full suite has run on the user's Windows machine, not yet on `windows-latest`; read the first run.
````diff
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -52,3 +52,15 @@
           node-version: "22"
       - name: Security-audit validators
         run: node --test .claude/skills/security-audit/validate-findings.test.cjs .claude/skills/security-audit/validate-coverage-ledger.test.cjs
+
+  # Python's text mode writes "\n" to a child's stdin as "\r\n" on Windows only, so some tests fail only there
+  # (update-from-template, #135).
+  tests-windows:
+    runs-on: windows-latest
+    steps:
+      - uses: actions/checkout@v4
+      - uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+      - name: Tests
+        run: python -m unittest discover -s tests
````
- [ ] prompt (ingest.md) ingest-logs-a-routed-line-for-each-todo: `/ingest` logs the todos it files as "Filed: ...", which `review-removals.py` does not read, so deleting `narrow-omoikane-mode-live-check` left no `- removed` line (session 261b475d, turn 4)
  The open todo `quote-audit-proposal-not-opened`, filed by an `/ingest`, has no `- routed` line in `log.md` either.
````diff
--- a/omoikane/prompts/ingest.md
+++ b/omoikane/prompts/ingest.md
@@ -10,7 +10,7 @@
 4. For each entity or concept in the source: update the existing page, or create one when the wiki has none and the source treats it as central. Cite the new source inline on every claim you add. Add a `## Contradictions` section where the source disagrees with a claim already on the page, and append the disagreement to `omoikane/_review.md`.
    - Omission is disagreement when the source claims completeness. A source that presents itself as the full list, the whole schema, or the thing to read instead of the code, and leaves out what another source asserts, contradicts that source. Record it as a contradiction, not as "not covered".
    - A rule the source sets for the system being built (a business rule, a design-system rule, an organisation convention) goes on a `domain` page under `omoikane/wiki/domain/`, as `omoikane/prompts/distill.md` step 4 describes, quoting the source with where it says so. One page per topic a later agent works on (a component, an area of the business), holding that topic's rules, with `summary` stating its main rule: the brief lists domain pages first, and one page per rule of a long guide would push every decision and gotcha out of it. Terms the source defines (a glossary, a "we call X ...") follow the same rule: one `term` page per topic, listing each term with its definition and the words rejected for it. A term the source pairs with a rejected word gets a `term` page of its own, as distill step 4 describes: that is the term an agent gets wrong.
-5. Append to `omoikane/log.md`: `## [YYYY-MM-DD] ingest | <title>` followed by the list of pages created and updated.
+5. Append to `omoikane/log.md`: `## [YYYY-MM-DD] ingest | <title>` followed by the list of pages created and updated, then one line per todo you filed in `omoikane/_review.md`: `- routed (todo) <slug>: <the work left, one line>`. `review-removals.py` reads only `- routed` lines, so a todo without one leaves no `- removed` line when the human deletes its bullet.
 6. Move the source file from `omoikane/raw/inbox/` to `omoikane/raw/sources/` with `git mv` when tracked, plain move otherwise. A scheduled run may not move files: when `git mv` is denied, do not try another way; leave the file, `wiki-ingest.ps1` moves it after the run.
 7. Run `python omoikane/bin/wiki-index.py` then `python omoikane/bin/wiki-lint.py`. Fix every finding. In a scheduled run (`wiki-ingest.ps1`) skip this step: you have no shell, and lint runs after you and sends its findings back.
 
````

## [2026-10-09] synthesize

- [ ] guard (hook) pr-merged-before-its-review-fixes: the user merged a PR while its review ran, and the agent pushed the fixes to the merged branch, where they missed `main` (sessions 21f37812, 261b475d; turns 8, 6)
  No diff: the check goes in a new PreToolUse `Bash` hook beside `.claude/hooks/escape-edit-guard.py`, registered in `.claude/settings.json`. On `git push`, it runs `gh pr list --head <branch> --state merged --json number` and blocks with a message that names the merged PR and says to put the commits on a new PR. Both pushes ran after a `cd` into a worktree, one in agent-dotfiles, so the hook must resolve the repository from the command. It costs one `gh` call per push and covers Claude Code only. See [[review-each-pr-with-a-subagent-before-merging]].
- [ ] rule tests-an-agent-writes-are-e2e-only: Write each test through the outermost interface the caller touches; unit or integration tests only when the user asks (synthesize)
