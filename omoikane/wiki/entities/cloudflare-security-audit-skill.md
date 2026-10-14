---
title: cloudflare-security-audit-skill
type: entity
summary: Cloudflare's MIT security-audit skill, vendored as .claude/skills/security-audit with a Windows fallback (PR #115)
tags: [security-audit, skills, reference, cloudflare]
created: 2026-10-07
updated: 2026-10-09
sources: [wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/session-2026-10-07-9e3fae7e.md, wiki/sources/session-2026-10-08-0ac17a0f.md, wiki/sources/session-2026-10-08-21f37812.md, wiki/sources/session-2026-10-08-261b475d.md, wiki/sources/2026-10-08-security-audit-stays-a-local-copy.md]
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
  YuukiFST closed it, not a maintainer: the fork `YuukiFST/security-audit-skill` was deleted, and the PR closed with it (source: [[session-2026-10-08-21f37812]], turn 7).
  On 2026-10-08 the owner decided: the copy stays local for good, a permanent divergence from upstream (#138): [[security-audit-stays-a-local-copy]] (source: [[2026-10-08-security-audit-stays-a-local-copy]]).
  The local copy is identical to the head of #69, `0232a9c` (same source).
- Before its merge, #115 also passed the `security-audit-windows` CI job (source: [[session-2026-10-07-9e3fae7e]], turn 2).
- In the integration run of all #111 PRs, its suites gave 69 passed, 0 failed, 6 skipped (turn 11).
- `omoikane-mode` has a security audit playbook that routes to it: [[omoikane-mode-routes-each-task-to-a-playbook]].
- Its full audit mode needs parallel subagents, so Pi runs only its guidance mode (`docs/specs/2026-10-07-software-toolkit.md`).
- The spec rejects the user's `security-review` and `security-bounty-hunter` skills: "`security-audit` covers both" (same file, "Rejected").

## In agent-dotfiles

The user asked for the skill in https://github.com/YuukiFST/agent-dotfiles too: "Caso não estiver, coloque" (source: [[session-2026-10-08-261b475d]], turn 6).

- agent-dotfiles PR #130 (issue #129) adds `skills/security-audit/`: the 21 files of the Omoikane copy, Windows fallback and Cloudflare `LICENSE` included. The agent checked the commit is identical, file by file, to the Omoikane folder (turn 6).
- The validator tests on Windows: of 75, 69 passed, 0 failed, 6 skipped, the skipped ones Linux-only (turn 6).
- The user merged #130 before its review fixes reached the branch. They went to PR #132 (issue #131): the `security-review` and `security-bounty-hunter` descriptions send a review of existing code to `security-audit`, and a CI job runs the validator tests on Ubuntu and Windows (turn 6).
- After a sync both copies exist, in `~/.claude/skills/security-audit/` and in the repository: [[personal-skills-hide-stale-template-copies-in-claude-code]] (turn 6).

The agent's turn-5 answer: the skill is versioned in Omoikane, 21 files under `.claude/skills/security-audit/`, and every system made from the template gets it (turn 5).
Its earlier term "cópia local" made the user ask whether the skill leaves the repository; the agent's correction: "O repo que a skill não alcança é o da Cloudflare, não o seu" (turn 5).
