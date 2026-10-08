---
title: cloudflare-security-audit-skill
type: entity
summary: Cloudflare's MIT security-audit skill, vendored as .claude/skills/security-audit with a Windows fallback (PR #115)
tags: [security-audit, skills, reference, cloudflare]
created: 2026-10-07
updated: 2026-10-08
sources: [wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/session-2026-10-07-9e3fae7e.md, wiki/sources/session-2026-10-08-0ac17a0f.md]
code: [.claude/skills/security-audit/SKILL.md, omoikane/skills.md, .github/workflows/ci.yml]
---

The Cloudflare security-audit-skill lives at https://github.com/cloudflare/security-audit-skill; the user named it as a source of skills and as a reference (source: [[session-2026-10-07-062e80af]], turns 1, 5).
The user also made the Cloudflare post https://blog.cloudflare.com/build-your-own-vulnerability-harness/ a reference (turn 5). See [[omoikane-references]].

## In Omoikane

- Vendored at commit `c1c8a8c`, MIT, as `.claude/skills/security-audit/` with its `LICENSE` (PR #115; `omoikane/skills.md`).
- Its two Node validators did not run on Windows: [[node-on-windows-lacks-o-nofollow-and-o-nonblock]]. The copy adds a `win32` fallback and a Windows CI job (turn 8).
- The fix went upstream as cloudflare/security-audit-skill#69, which the user had approved (turn 10).
  On 2026-10-07, after #115 merged as `7d6bd37`, #69 was still open with no review (source: [[session-2026-10-07-9e3fae7e]], turns 3, 4).
  #69 was then closed without a merge, on 2026-10-07 at 23:39 UTC (source: [[session-2026-10-08-0ac17a0f]], turn 5).
  So no upstream version exists to return the copy to; the user decides between keeping the local copy and proposing the fix upstream again, after reading why #69 closed (turns 5, 6).
- Before its merge, #115 also passed the `security-audit-windows` CI job (source: [[session-2026-10-07-9e3fae7e]], turn 2).
- In the integration run of all #111 PRs, its suites gave 69 passed, 0 failed, 6 skipped (turn 11).
- `omoikane-mode` has a security audit playbook that routes to it: [[omoikane-mode-routes-each-task-to-a-playbook]].
- Its full audit mode needs parallel subagents, so Pi runs only its guidance mode (`docs/specs/2026-10-07-software-toolkit.md`).
- The spec rejects the user's `security-review` and `security-bounty-hunter` skills: "`security-audit` covers both" (same file, "Rejected").
