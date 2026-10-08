# security-audit stays a local copy

- Date: 2026-10-08.
- Decided by: the owner, in an interactive session.
- Issue: #138.

## Decision

The patched `.claude/skills/security-audit/` is a permanent divergence from cloudflare/security-audit-skill.
It does not return to upstream.

## Facts

- cloudflare/security-audit-skill#69 offered the Windows fallback upstream.
  The owner's account closed it unmerged on 2026-10-07 at 23:39:30Z, head `0232a9cc986fe692ad0b2d1e4523b1b8623f6773`.
- The owner deleted the fork `YuukiFST/security-audit-skill` on purpose.
  The owner did not see why the fork existed.
  The agent explained: a pull request from an account without write access to the upstream repository needs a branch in a fork.
- The local copy is identical to the head of #69, and `omoikane/skills.md` lists its changes.
- Upstream issue #53, "Validator CLIs cannot read any input on Windows", has two comments and none from a maintainer.

## What the next wrap-up must change

- The gotcha `node-on-windows-lacks-o-nofollow-and-o-nonblock` still says, in the last paragraph of its Workaround section: "The same fix went upstream as cloudflare/security-audit-skill#69; once it merges, the copy returns to upstream as it is".
  Replace that sentence: #69 closed unmerged and the copy stays local.
- `docs/specs/2026-10-07-software-toolkit.md` already says so (#138).
- The todos `security-audit-upstream-pr-69` and `security-audit-pr-69-closed-unmerged` are removed in #138.
