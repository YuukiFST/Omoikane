---
title: Node on Windows lacks O_NOFOLLOW and O_NONBLOCK
type: gotcha
summary: Node on Windows defines no O_NOFOLLOW or O_NONBLOCK, so Cloudflare's security-audit validators refuse to run there
tags: [windows, node, security-audit, ci]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-07-062e80af.md]
code: [.claude/skills/security-audit/validate-findings.cjs, .claude/skills/security-audit/validate-coverage-ledger.cjs, .github/workflows/ci.yml, omoikane/skills.md]
guard: test
---

## Behaviour

`readFileWithinLimit` in the Cloudflare validators `validate-findings.cjs` and `validate-coverage-ledger.cjs` opens its input with `O_NOFOLLOW | O_NONBLOCK`. It refuses to run when Node does not define them (`docs/specs/2026-10-07-software-toolkit.md`, "Cloudflare validators on Windows").
Node on Windows defines neither, so both validators exit with `OS no-follow and nonblocking input protection is unavailable`. Linux, macOS and WSL are not affected (same section).
The agent read the upstream validator for `O_NOFOLLOW` while it surveyed the skill (source: [[session-2026-10-07-062e80af]], turn 3).
The upstream suites prove nothing on Windows: they skip every CLI test when `O_NOFOLLOW` is missing (same section).

## Workaround

The vendored copy adds a `win32` fallback (PR #115; turn 8): `lstat` refuses links and junctions, `open` reads, and `fstat` refuses a file whose identity changed between check and open.
The review of #115 added more, in commit `822d2b2` (turn 10):
- A `\\.\pipe\` or UNC path was opened before `fstat` refused it, "which can connect to a pipe server or start SMB authentication"; such paths are now refused before `lstat`.
- "ReFS IDs are not guaranteed unique and some file systems report ino 0"; the fallback refuses `ino` 0 and also compares the birth time.

The `security-audit-windows` job in `.github/workflows/ci.yml` runs both suites on `windows-latest` with the `win32` tests (turn 8).
The same fix went upstream as cloudflare/security-audit-skill#69; once it merges, the copy returns to upstream as it is (turn 10; `docs/specs/2026-10-07-software-toolkit.md`).
The changes are listed on the `security-audit` row of `omoikane/skills.md`. See [[cloudflare-security-audit-skill]].
