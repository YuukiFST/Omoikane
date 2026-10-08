---
title: 2026-10-06 pstack skills review round 2
type: source
summary: Verdict on every pstack skill not read on 2026-10-05: four gaps proposed, ten already covered, the rest rejected
tags: [references, pstack]
created: 2026-10-07
updated: 2026-10-07
dated: 2026-10-06
sources: []
code: [omoikane/bin/session-capture.py, omoikane/bin/wiki-lint.py, omoikane/bin/update-from-template.py, docs/specs/2026-10-07-software-toolkit.md]
---

A note written for ingest by the agent that read the pstack skills, raw file `omoikane/raw/sources/2026-10-06-pstack-skills-review.md`.
`dated` comes from its frontmatter and its first line: "On 2026-10-06 an agent read every pstack skill not read on 2026-10-05".
Scope: a complete verdict list for every pstack skill not read in round 1, at pstack commit `df58112` (2026-10-05). It reads only each `SKILL.md`; it skips the `references/` files, the benny templates and references, and `docs/guide/`.
Its stated aim: "so that no later session proposes them again without new evidence".

## The test it applies

A skill counts only when it serves [[omoikane-objective]], closes a gap Omoikane has, and works in a system born from the template.
Round 1 (2026-10-05) read `recall`, `reflect`, `correct`, `why`, `principle-encode-lessons-in-structure` and `poteto-mode`; see [[pstack]].

## Proposed: four gaps

1. `automations/benny` (`FOR_AGENTS.md`, `setup-benny`): keep the files the pack owns apart from the files the user owns. Gap: a system has no path to take template updates. A simulated `git merge template/main` into a system reset on 2026-10-03 added the template's capture `raw/sources/sessions/2026-10-02-680ff986.md` and its source page to the system's wiki. It conflicted on `_review.md`, `index.md` and `omoikane-references.md`. Proposal: a script that merges the template and keeps every system-owned path as the system has it.
2. `create-verification-skill` ("Doctor" check) and `maintain-verification-skill` (health check before driving). Gap: `session-capture.py` swallowed every exception and exited 0 (lines 684-688), so a capture that crashes on every turn loses sessions with no signal. A redaction defect once crashed every later turn; a PR review caught it before merge. Proposal: record capture errors and name them in the session brief.
3. `create-verification-skill` step 4 ("a generated skill that was never executed is a draft") with `principle-prove-it-works` ("script the check"). Gap: no code checks that a diff in `_review.md` applies. A headless distill could not run `git apply --check` (commit `43423c4`), and a later diff went stale once its target changed. Proposal: `wiki-lint.py` runs `git apply --check` on each proposal diff.
4. `show-me-your-work` (audit the log against the transcript). Gap: no check that a quote a page cites to a session turn is in that capture. Measured on 2026-10-06: 31 of 32 such quotes are verbatim in the capture; the miss is a commit subject the capture does not hold. Proposal: `wiki-lint.py` flags a quote cited to a session that its capture lacks. The note says its weight grows "once the `wiki/auto` PR merges itself (PR #92)".

## Already in Omoikane

The note maps ten pstack items to what Omoikane has, with file and line:
- `automate-me` is `/synthesize` with its two-session floor; its step that asks the user goes against "without the user's involvement".
- `maintain-verification-skill` drift check is the `code:` staleness warning plus `/lint`; its "doc drift or product regression" split matches `prune.md` line 11.
- `tdd` is the distill guard test; `technical-writing` and `unslop` are the ASD-STE100 subset of the page contract.
- `interrogate` is the promoted rule [[review-each-pr-with-a-subagent-before-merging]].
- `principle-build-the-lever`, `principle-make-operations-idempotent`, `principle-guard-the-context-window`, `principle-fix-root-causes` and `principle-prove-it-works` each match a line of `docs/architecture.md` or `distill.md`.
- benny's fail-closed rule: a check that gives no verdict blocks the scheduled run.

## Rejected, with the reason

- `principle-never-block-on-the-human`: guards, prompt fixes and rules wait for the human's tick on purpose.
- `principle-separate-before-serializing-shared-state`: `/wrap-up` runs one subagent at a time because `log.md` and `_review.md` are shared; no failure of the serial rule was seen, and speed is not the objective.
- `principle-explain-the-number`: uncertain; no run-to-run variance of the headless eval was measured, so no concrete gap yet.
- Multi-model routing in Cursor (`architect`, `arena`, `swarm`, `figure-it-out`, `setup-pstack`, `poteto-help`, `poteto-agent`), code explanation and review (`how`, `teach`, `blast-radius`, `benchmark-checklist`, `bro`), `create-verification-skill` as a whole: no memory gap.
- `no-comments` and the Comment Sicko agent: they conflict with the user's rule to keep an agent's comments.
- `typescript-best-practices`, `make-bot-ui`, benny's triage and reproduce flows, and fifteen coding principles with no memory link.

## What it adds

The wiki knew pstack's round-1 skills only, and recorded that the other skills were unread ([[pstack]]).
This note gives a verdict for each of them, the rejected ones included, and four gaps measured against the code.

## Status of the claims at ingest

Checked with `gh` and `git` on 2026-10-07:
- The user opened three of the four proposals as issues on 2026-10-06 at 13:30 UTC, and each closed the same day through a merged PR. Proposal 1 is #105, PR #108, commit `93c2dea`, which adds `omoikane/bin/update-from-template.py`. Proposal 2 is #103, PR #107, commit `872319e`, which writes `omoikane/.capture-errors` for the brief. Proposal 3 is #106, PR #110, commit `4000448` in `wiki-lint.py`.
- Proposal 4 (quote audit) has no issue; filed as a todo in `omoikane/_review.md`.
- `session-capture.py` lines 684-688 no longer hold the swallowing handler; since `872319e` the handler records the failure (line 739).
- The rejection "no memory link" no longer holds as stated: on 2026-10-07 the user widened the objective, and `docs/specs/2026-10-07-software-toolkit.md` says "The verdicts in `omoikane/raw/inbox/2026-10-06-pstack-skills-review.md` that rejected a skill for 'no memory link' are reopened here; the verdicts about memory gaps stand." Issue #111 then vendored `how`, `blast-radius`, `figure-it-out`, `create-verification-skill`, `maintain-verification-skill`, `interrogate` and `correct` (commits `8b21a90`, `64023b3`). The same spec records that the user excluded `tdd` and `unslop`.
- PR #92 was closed unmerged on 2026-10-06 at 12:41 UTC, before the issues above were opened from this note; see the contradiction on [[wiki-auto-auto-merge-dropped-with-pr-92]].
