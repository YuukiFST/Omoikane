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

## Design and planning

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|
| brainstorming | https://github.com/obra/superpowers `skills/brainstorming/` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` (v6.3.0) | MIT | Spec path `docs/superpowers/specs/` becomes `docs/specs/` in `SKILL.md` and `spec-document-reviewer-prompt.md`; visual companion removed (`scripts/`, `visual-companion.md`, its checklist step and section); the clarifying-questions step points at `show-me` for visual questions; references to `elements-of-style`, `frontend-design` and `mcp-builder` dropped |
| writing-plans | https://github.com/obra/superpowers `skills/writing-plans/` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` (v6.3.0) | MIT | Plan path `docs/superpowers/plans/` becomes `docs/plans/`; `superpowers:` sub-skill references become `executing-plans` or a plain subagent dispatch; worktree line made generic; Pi runs the steps in sequence |
| executing-plans | https://github.com/obra/superpowers `skills/executing-plans/` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` (v6.3.0) | MIT | Superpowers subagent note replaced, with Pi running the steps in sequence; `using-git-worktrees` and `finishing-a-development-branch` steps made generic |
| grilling | https://github.com/mattpocock/skills `skills/productivity/grilling/` | `2ffb184ffbb752faa664c0b204f3c9241b1428e9` (v1.2.0) | MIT | Pi looks facts up in the main thread; `agents/openai.yaml` not copied |
| prototype | https://github.com/mattpocock/skills `skills/engineering/prototype/` | `2ffb184ffbb752faa664c0b204f3c9241b1428e9` (v1.2.0) | MIT | `agents/openai.yaml` not copied |
| codebase-design | https://github.com/mattpocock/skills `skills/engineering/codebase-design/` | `2ffb184ffbb752faa664c0b204f3c9241b1428e9` (v1.2.0) | MIT | `DESIGN-IT-TWICE.md`: `CONTEXT.md` vocabulary becomes the `term` pages under `omoikane/wiki/domain/`, Pi writes the designs in sequence; `agents/openai.yaml` not copied |
| figure-it-out | https://github.com/cursor/plugins `pstack/skills/figure-it-out/` | `df581122cde17e6e27686b5a448bde23e4ad4318` | MIT | `disable-model-invocation` removed, description trigger names `omoikane-mode`; `poteto-mode` becomes `omoikane-mode` and principle skills become its principles; `architect`/`arena` become two structurally different sketches from one model; `show-me-your-work` becomes a decision log in the plan file; Pi runs the steps in sequence |

## Code and review

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|

## Security

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|

## Shipping and writing

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|
| git-workflow | https://github.com/YuukiFST/agent-dotfiles `skills/git-workflow/` | `cc990612aae6408aa529da6c587b1f48c0b1ffad` | Omoikane | `gh-axi` becomes `gh`; references to the global rules, `CLAUDE.md`, `CODING_STANDARDS.md` and agent-dotfiles issues replaced by a generic commit-rules section; hook and `git-safe-commit.sh` enforcement section removed; review by a fresh subagent instead of `/code-review`; `git revert` line added; description shortened |
| writing-for-agents | https://github.com/mattpocock/skills `skills/productivity/writing-for-agents/` (formerly `writing-great-skills`) | `2ffb184ffbb752faa664c0b204f3c9241b1428e9` (v1.2.0) | MIT | `agents/openai.yaml` not copied |
| show-me | https://github.com/humanlayer/skills `plugins/show-me/skills/show-me/` | `6ab9013a10c28f5046f7f999549cd5328a0b30d7` | MIT | Description states the trigger; the open step names the opener per OS; the plugin wrapper (`.claude-plugin/plugin.json`) not copied |
