---
title: security-audit stays a local copy
type: decision
summary: Keep the patched security-audit skill as a permanent local divergence; it does not return to upstream
tags: [security-audit, cloudflare, windows, skills]
created: 2026-10-09
updated: 2026-10-09
sources: [wiki/sources/2026-10-08-security-audit-stays-a-local-copy.md, wiki/sources/session-2026-10-08-261b475d.md, wiki/sources/session-2026-10-08-0ac17a0f.md]
code: [.claude/skills/security-audit/SKILL.md, omoikane/skills.md, docs/specs/2026-10-07-software-toolkit.md]
---

## Chosen

On 2026-10-08 the owner chose to keep the patched `.claude/skills/security-audit/` as a permanent divergence from cloudflare/security-audit-skill. It does not return to upstream (source: [[2026-10-08-security-audit-stays-a-local-copy]]).
Issue #138 records it; PR #139 changed `docs/specs/2026-10-07-software-toolkit.md` to say so (source: [[session-2026-10-08-261b475d]], turn 4).

- The copy keeps the Windows fallback of [[node-on-windows-lacks-o-nofollow-and-o-nonblock]]. `omoikane/skills.md` lists every change to the upstream text.
- The local copy is identical to the head of #69, `0232a9cc986fe692ad0b2d1e4523b1b8623f6773` (source: [[2026-10-08-security-audit-stays-a-local-copy]]).
- PR #139 removed the todos `security-audit-upstream-pr-69` and `security-audit-pr-69-closed-unmerged` from `_review.md` (same source).

## Rejected

- Return the copy to upstream once #69 merges. That was the plan of PR #115, but the owner's account closed #69 unmerged on 2026-10-07 at 23:39:30Z (same source).
- Propose the fix upstream again. The 2026-10-08 handoff offered it after #69 closed (source: [[session-2026-10-08-0ac17a0f]], turns 5, 6). The owner kept the local copy instead (source: [[session-2026-10-08-261b475d]], turns 3, 4).

## Why

- The owner deleted the fork `YuukiFST/security-audit-skill` on purpose, and #69 closed with it (source: [[2026-10-08-security-audit-stays-a-local-copy]]).
  The owner did not see why the fork existed: "eu exclui o fork de proposito, eu não entendi o porque ele foi feito" (source: [[session-2026-10-08-261b475d]], turn 3).
  A pull request from an account without write access to the upstream repository needs a branch in a fork (turn 3).
- Upstream issue #53, "Validator CLIs cannot read any input on Windows", has two comments and none from a maintainer (source: [[2026-10-08-security-audit-stays-a-local-copy]]).

## Consequences

- The `security-audit-windows` CI job and the `win32` tests stay with the copy ([[node-on-windows-lacks-o-nofollow-and-o-nonblock]]).
- agent-dotfiles holds the same patched copy (PR #130); see [[cloudflare-security-audit-skill]].
- The todo `security-audit-windows-promotion-step` in `omoikane/_review.md` is not settled by this decision.
