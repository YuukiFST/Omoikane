---
title: pstack skills reviewed for Omoikane, round 2
dated: 2026-10-06
---

# pstack skills reviewed for Omoikane, round 2

On 2026-10-06 an agent read every pstack skill not read on 2026-10-05, at pstack commit `df58112` (2026-10-05), and judged each one against `omoikane/wiki/domain/omoikane-objective.md`.
A skill counts only when it serves the objective, closes a gap Omoikane has, and works in a system born from the template.
This note records every verdict, the rejected ones included, so that no later session proposes them again without new evidence.

Round 1 (2026-10-05): `recall`, `reflect`, `correct`, `why`, `principle-encode-lessons-in-structure`, `poteto-mode`. Results are on `omoikane/wiki/entities/pstack.md`.

## Proposed, waiting for the user to choose which issues to open

1. `automations/benny` (`FOR_AGENTS.md`, `setup-benny`): keep the files the pack owns apart from the files the user owns, so a refresh never overwrites or pollutes them. Gap: a system has no path to take template updates. A simulated `git merge template/main` into a system reset on 2026-10-03 added the template's own capture `raw/sources/sessions/2026-10-02-680ff986.md` and its source page to the system's wiki, and conflicted on `_review.md`, `index.md` and `omoikane-references.md`. Proposal: a script that merges the template but keeps every system-owned path (wiki, raw, log, review queue, index, the rules block) as the system has it.
2. `create-verification-skill` (the "Doctor" check) and `maintain-verification-skill` (health-check before driving): Gap: `session-capture.py` swallows every exception and exits 0 (lines 684-688), so a capture that crashes on every turn loses sessions with no signal. A redaction defect once did crash every later turn; a PR review caught it before merge. Proposal: record capture errors and have the session brief name them.
3. `create-verification-skill` step 4 ("a generated skill that was never executed is a draft") with `principle-prove-it-works` ("script the check"): Gap: no code checks that a diff in `_review.md` applies. A headless distill could not run `git apply --check` (commit `43423c4`), and a later diff went stale once its target changed. Proposal: `wiki-lint.py` runs `git apply --check` on each proposal diff.
4. `show-me-your-work` (audit the log against the transcript): Gap: no check that a quote a page attributes to a session turn is in that capture. Measured on 2026-10-06: 31 of 32 such quotes are verbatim in the capture; the miss is a commit subject the capture does not hold. Proposal: `wiki-lint.py` flags a quote cited to a session that its capture lacks. Weight grows once the `wiki/auto` PR merges itself (PR #92): checks become the only review.

## Already in Omoikane

- `automate-me`: `/synthesize` mines sessions and keeps a pattern only with two or more sessions (`omoikane/prompts/synthesize.md` line 14). Its step that asks the user directly goes against "without the user's involvement".
- `maintain-verification-skill` (drift check): the `code:` staleness warning plus `/lint` (`docs/architecture.md` line 144, `omoikane/prompts/lint.md` line 9). Its "doc drift or product regression" split matches `omoikane/prompts/prune.md` line 11 and the distill rule that the code may be what breaks a rule.
- `tdd`: the distill guard test, "the mistake this session made is an input on which the check fails" (`omoikane/prompts/distill.md` line 24).
- `technical-writing`, `unslop`: the ASD-STE100 subset of the page contract (`AGENTS.md` line 46). Recent pages show no compressed prose.
- `interrogate`: the promoted rule "post a subagent review on each PR" (`AGENTS.md` line 85).
- `principle-build-the-lever`: "bookkeeping is code, only meaning goes through the LLM" (`docs/architecture.md` line 5).
- `principle-make-operations-idempotent`: captures are rewritten whole on every turn and an empty inbox is a no-op (`docs/architecture.md` lines 65, 145).
- `principle-guard-the-context-window`: `context-budget.py` limits and the brief budget (`docs/architecture.md` line 139).
- `principle-fix-root-causes`, `principle-prove-it-works`: distill rejects `no-root-cause` and writes only what the session shows (`omoikane/prompts/distill.md` lines 15, 31).
- benny's fail-closed rule: a check that gives no verdict blocks the scheduled run (`docs/architecture.md` line 149).

## Rejected, with the reason

- `principle-never-block-on-the-human`: guards, prompt fixes and rules wait for the human's tick on purpose (`docs/architecture.md` lines 54, 138). Pages already need no approval.
- `principle-separate-before-serializing-shared-state`: `/wrap-up` runs one subagent at a time because `log.md` and `_review.md` are shared. Per-file log fragments would allow parallel runs, but no failure of the serial rule was seen; speed is not the objective.
- `principle-explain-the-number`: uncertain. Prompt changes are proven by one headless eval run (`_review.md`, todo `close-second-domain-distill-eval`), but no run-to-run variance was measured, so there is no concrete gap yet.
- `architect`, `arena`, `swarm`, `figure-it-out`, `setup-pstack`, `poteto-help`, `poteto-agent`: multi-model work routing in Cursor; nothing about capturing or delivering knowledge.
- `how`, `teach`, `blast-radius`, `benchmark-checklist`, `bro`: explaining or reviewing code; no memory gap.
- `create-verification-skill` as a whole: an app-driving harness is useful to a system but is not memory.
- `no-comments` and the Comment Sicko agent: deletes code comments; conflicts with the user's rule to keep an agent's comments.
- `typescript-best-practices`, `make-bot-ui`, benny's triage and reproduce flows: language rules, a Grok Bot webhook UI, Slack bug triage.
- Coding principles with no memory link: `attack-the-premise`, `boundary-discipline`, `exhaust-the-design-space`, `experience-first`, `foundational-thinking`, `laziness-protocol`, `migrate-callers-then-delete-legacy-apis`, `minimize-reader-load`, `model-the-domain`, `outcome-oriented-execution`, `redesign-from-first-principles`, `sequence-verifiable-units`, `subtract-before-you-add`, `test-behavior-not-implementation`, `type-system-discipline`.

## Not read

The `references/` files of the skills (only each `SKILL.md`), the benny templates and references, and `docs/guide/`.
