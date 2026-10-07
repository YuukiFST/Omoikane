# Skills taken from other projects

Every skill under `.claude/skills/` has one row here: where it came from, at which commit, under which licence, and what Omoikane changed.
`tests/test_skills_manifest.py` checks that each row names a skill folder, that each skill folder has a row, and that a row whose licence is not `Omoikane` ships the upstream `LICENSE`.
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
| omoikane-mode | https://github.com/cursor/plugins/tree/main/pstack/skills/poteto-mode (+ principle-* skills; 9 principles from YuukiFST/agent-dotfiles) | df58112 | MIT | Renamed; triggers route to Omoikane's skills and memory commands; 24 principles moved to `references/principles/` without `disable-model-invocation`, the user's 9 versions (agent-dotfiles cc99061) replacing pstack's; one model, no per-role model lines, Pi runs fan-out in sequence; memory section from `AGENTS.md`; reply rules keep only those that stand alone; session-pickup and pause-safely rewritten on captured sessions and inbox notes; new security-audit playbook; orchestrate, autopilot-full, autopilot-stack, worktree-cleanup and the scripts dropped; babysit and shipping use plain `gh`; Bugbot triage generalized to any automated reviewer; Cursor, Origin and unshipped-skill references removed |

## Design and planning

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|

## Code and review

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|

## Security

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|

## Shipping and writing

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|
