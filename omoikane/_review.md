# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

A bullet with a checkbox is a proposal: a guard or a prompt change, with its diff below it. Tick `[x]` to approve; an interactive session applies ticked proposals and deletes their bullets, and a scheduled run never does. Delete an unticked bullet to reject it.

## [2026-09-30] distill | session e04462b2

- todo unify-transcript-readers: merge the Claude, Pi and OpenCode readers in `session-capture.py` into one state machine (session e04462b2, turn 4)
- todo pi-live-verification: run the Pi extension live once: `pi` at the repo root, accept project trust, prompt an edit, check `omoikane/raw/inbox/sessions/` (session e04462b2, turn 4)

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
- todo pi-skill-capture-live-check: the Pi `/skill:` capture fix was never checked against a session file a real Pi run wrote; when doing `pi-live-verification`, also run `/skill:wrap-up` and check no capture appears, see [[pi-expands-a-skill-command-into-a-skill-block]] (session 062e80af, turn 6)
- todo security-audit-upstream-pr-69: when cloudflare/security-audit-skill#69 merges, return `.claude/skills/security-audit/` to upstream as it is and update its `omoikane/skills.md` row (session 062e80af, turn 10)
- todo security-audit-windows-promotion-step: the spec asks to check whether `.claude/skills/security-audit/SKILL.md`, whose artifact promotion uses no-follow descriptors and a link count of 1, needs a Windows step; the capture does not show it checked (session 062e80af, turn 3)

## [2026-10-07] distill | session 9e3fae7e

- todo close-issue-111-after-wrap-up: after this `/wrap-up` applies the toolkit note to [[omoikane-objective]] and [[omoikane-references]], close issue #111 by hand when its acceptance criteria hold; no PR closes it, all use `Refs #111` (session 9e3fae7e, turn 2)
- todo omoikane-mode-live-check: check live that `/skill:omoikane-mode` loads in Pi at the trusted repo root and that `/omoikane-mode` works in OpenCode, and write the result as a note in `omoikane/raw/inbox/`; do it with `pi-live-verification` and `pi-skill-capture-live-check` (session 9e3fae7e, turn 2)

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
- todo security-audit-pr-69-closed-unmerged: cloudflare/security-audit-skill#69 closed without a merge, so `security-audit-upstream-pr-69` never fires; read why it closed and choose between the local copy and a new upstream PR (session 0ac17a0f, turn 5)

## [2026-10-08] ingest | 2026-10-07 omoikane-mode live check

- contradiction ai-tells-folder-in-opencode-run: the note says OpenCode used the personal `ai-tells` skill "from `~/.claude/skills/`", but the run's capture calls the lint under `~/.agents/skills/ai-tells/scripts/`, and both folders hold `ai-tells`; see [[2026-10-07-omoikane-mode-live-check]] (source: `omoikane/raw/sources/2026-10-07-omoikane-mode-live-check.md:16`, `omoikane/raw/sources/sessions/2026-10-07-Q7Bpg6M5.md:80`)
- todo narrow-omoikane-mode-live-check: OpenCode lists and loads `/omoikane-mode`, and Pi lists it; only loading in Pi is left, so narrow the todo `omoikane-mode-live-check` to Pi (source: [[2026-10-07-omoikane-mode-live-check]])
