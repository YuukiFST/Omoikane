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

## Code and review

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|

## Security

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|
| security-audit | https://github.com/cloudflare/security-audit-skill `skills/security-audit/` | `c1c8a8c` | MIT | Windows fallback in both validators when `O_NOFOLLOW`/`O_NONBLOCK` are missing: a device or UNC path (`\\.\`, `\\?\`, `\\server`) is refused before any open, `lstat` refuses links, junctions and an `ino` of 0, `fstat` refuses a changed `dev`/`ino`/birth time or a non-file; `readFileWithinLimit` is exported, the CLI tests run on `win32`, plus tests for a symbolic link, a junction, a named pipe, a relative path and a file replaced between check and open |

## Shipping and writing

| Skill | Upstream | Commit | Licence | Changes |
|---|---|---|---|---|
