# Skills taken from other projects

Every skill under `.claude/skills/` that Omoikane took from another project has one row here: where it came from, at which commit, under which licence, and what Omoikane changed.
`tests/test_skills_manifest.py` checks that each row names a skill folder, that each folder with a third-party `LICENSE` has a row, and that a row whose licence is not `Omoikane` ships that `LICENSE`.
The memory skills (`ask`, `distill`, `ingest`, `lint`, `prune`, `synthesize`, `wrap-up`) and the skills a system writes for itself (`verify-<app>`) have no row.
Plan and the skills rejected, with the reason: `docs/specs/2026-10-07-software-toolkit.md`.

Columns:

- Skill: folder name under `.claude/skills/`.
- Upstream: the repository and path the text was first written in, not an intermediate copy.
- Commit: the upstream commit the copy was taken at.
- Licence: SPDX id of the upstream licence, or `Omoikane` for a skill first written for Omoikane or by its owner.
- Changes: what Omoikane changed in the upstream text; `none` when it is copied as it is.

## Mode

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|

## Design and planning

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|

## Code and review

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|
| how | https://github.com/cursor/plugins `pstack/skills/how` | `df58112` | MIT | `disable-model-invocation` and the `why` pointer dropped; per-model `Task` spawns (`model`, `readonly`, `subagent_type`, `pstack-models.mdc`) replaced by read-only subagents on one model; explorers split by area; Pi runs the steps in sequence; the explorer prompt also reads Omoikane decision and gotcha pages; description reworded ("ownership / layering" and "onboarding mental models" dropped); `Read`, `Grep` and `Glob` in the explorer and explainer prompts replaced by read and search tools |
| blast-radius | https://github.com/cursor/plugins `pstack/skills/blast-radius` | `df58112` | MIT | `why` replaced by `git log`, `git blame`, `gh pr view` and `gh pr list --search`; `arena` replaced by a second read-only subagent, run in sequence in Pi; `unslop` dropped; step 1 also reads Omoikane decision and gotcha pages; description shortened, `disable-model-invocation` dropped |
| improve | https://github.com/shadcn/improve `skills/improve` | `cac56e1` | MIT | The agent-dotfiles copy matched upstream byte for byte. Description shortened, `metadata` dropped; advisor and executor split stated without model tiers; `Explore` agents, `general-purpose` with `isolation`, the default executor model and `SendMessage` replaced by harness-neutral subagent wording with a `git worktree add` fallback; Pi audits in sequence; recon also reads Omoikane decision, domain and gotcha pages; example executor skill is `test-audit`; Hard Rule 2 allows the `git worktree add -b` fallback as a third exception; "security" dropped from the description |
| code-simplifier | https://github.com/anthropics/claude-plugins-official `plugins/code-simplifier/agents/code-simplifier.md` | `aecd4c8` | Apache-2.0 | Through agent-dotfiles: converted from a subagent to a skill; persona opening replaced by the task; fixed JS/React standards replaced by the target project's rules; scope narrowed to the changed lines; existing comments kept and pre-existing dead code flagged; checks run before and after; autonomy paragraph replaced by a report. Omoikane: change notice added; "or after finishing a change" dropped from the description; provenance link pinned to `aecd4c8`. Upstream has no NOTICE file |
| test-audit | https://github.com/openclaw/openclaw `.agents/skills/test-audit` | `80930af` | MIT | Through agent-dotfiles: Vitest, `$openclaw-*` and `$crabbox` commands replaced by the target project's own commands; default audit target added; discovery lanes generalised; `CLAUDE.md` read beside `AGENTS.md`; landing through `git-workflow`. Omoikane: review through `interrogate` instead of `/code-review`; one subagent per lane, in sequence in Pi; provenance comment pinned. `CAMPAIGN.md` unchanged |
| correct | https://github.com/cursor/plugins `pstack/skills/correct` | `df58112` | MIT | Description shortened, `disable-model-invocation` dropped, triggers on `/correct` or a repeated correction; in an Omoikane system it reads open `guard` bullets as evidence only and applies one only when ticked or named, then deletes it; files a check it does not land as a `_review.md` guard proposal ending `(correct YYYY-MM-DD)`, with a `- routed (guard)` line in `log.md`; keeps the rule table in gotcha pages, whose `guard:` the session's `/distill` updates, instead of `AGENTS.md` |
| create-verification-skill | https://github.com/cursor/plugins `pstack/skills/create-verification-skill` | `df58112` | MIT | Output path `.claude/skills/verify-<app>/` instead of `.cursor/skills/`; the generated skill gets no row here; its description is capped at 300 characters and its folder holds one `SKILL.md`; `disable-model-invocation` dropped |
| maintain-verification-skill | https://github.com/cursor/plugins `pstack/skills/maintain-verification-skill` | `df58112` | MIT | Target path `.claude/skills/verify-*/` instead of `.cursor/skills/`; the target gets no row here; Pi runs the source wave in sequence; `disable-model-invocation` dropped |
| interrogate | https://github.com/cursor/plugins `pstack/skills/interrogate` | `df58112` | MIT | One reviewer per lens (correctness, security, code quality, tests, blast radius) instead of per model; model table, slug fallbacks and `Task` parameters removed; each reviewer gets its lens's rubric sections; Blast Radius rubric section added; the code-quality lens goes to one reviewer instead of every reviewer; synthesis weights findings by evidence and severity, cross-lens agreement as a bonus; lead judgment names reviewers, not models; `Read, Grep, Glob` in the rubric replaced by read and search tools; Pi runs the lenses in sequence; description changed, `disable-model-invocation` dropped |

## Security

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|

## Shipping and writing

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|
