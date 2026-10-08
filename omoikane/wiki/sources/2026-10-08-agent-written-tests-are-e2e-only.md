---
title: 2026-10-08 agent-written tests are E2E only
type: source
summary: The user's E2E-only test rule, the study and two posts behind it, and its port into the template's skills (PR #120)
tags: [testing, skills, template, agent-dotfiles]
created: 2026-10-08
updated: 2026-10-08
dated: 2026-10-08
sources: []
code: [.claude/skills/writing-plans/SKILL.md, .claude/skills/test-audit/SKILL.md, .claude/skills/omoikane-mode/playbooks/bug-fix.md, .claude/skills/omoikane-mode/playbooks/refactoring.md, omoikane/skills.md]
---

A short note, `omoikane/raw/sources/2026-10-08-agent-written-tests-are-e2e-only.md`, titled "Tests an agent writes are E2E only".
Its frontmatter bears `date: 2026-10-08`, and its first line says "On 2026-10-08 the user asked how two posts and one study could help Omoikane"; commit `a7b6b78` added it to `main` on 2026-10-08.

## Scope

A record of one change and its evidence: the rule, three sources with their numbers, and the PR that ported the rule.
It covers what session [[session-2026-10-08-0ac17a0f]] did in turns 7 to 10, with the study details that capture cuts.
It claims no full list of the changed files.

## Key claims

- The user approved the recommendation to make the template's skills E2E-only (line 6).
- The user's global `CODING_STANDARDS.md` already holds the rule, from agent-dotfiles PRs #126 and #128, commits `f0202c8`, `5a4c7a6`, `825c9f8` and `97f852f` (line 7). The rule, quoted:
  > E2E only: every test you write drives the outermost interface the caller touches (browser flow, HTTP request, CLI run, a library's public API); unit and integration tests are written only when the user asks for one.
  > Bug repro is E2E: reproduce as the end user hits it; once green, that red test is the bug's one regression test.
- Chen et al. 2026, arXiv 2602.07900, on SWE-bench Verified: 500 tasks, six models, mini-SWE-agent (line 14).
  - Writing tests does not separate resolved from unresolved tasks. gpt-5.2 writes a test in 0.6% of tasks and resolves 71.8%.
  - Agent tests are mostly probes that print values, not assertions.
  - With tests discouraged: kimi-k2-thinking went from 317 to 304 resolved with 49% fewer input tokens; deepseek-v3.2-reasoner from 300 to 291 with 33% fewer.
  - With tests encouraged: gpt-5.2 stayed at 359 with 19.8% more output tokens; gemini-3-pro-preview went from 371 to 366.
  - The authors title their conclusion "Help or Habit?".
- Kun Chen, DeepSWE with Sonnet 5.5, 111 tasks, 444 runs, posted 2026-10-08 (line 20).
  - A ban on agent-written tests: 65.3% to 66.2% solved, not significant; 6% less agent time and 9% less spend, both significant.
  - Of 3000+ tests written, 65% were unit and 35% integration, and neither group helped. Only 17 were E2E.
  - A subset of 44 tasks that ran no tests at all, existing tests included, scored 59% in both arms.
  - The author: "both the implementation and the tests were simply the agent's interpretation of our intent".
  - The author says the eval tells nothing about E2E tests or tests a human describes.
- Kun Chen, ProgramBench with GPT 5.5, 192 tasks, posted 2026-06-09, read from the post's chart only; the thread with the method did not open (line 26).
  - TDD against baseline: easy 72.5% to 67.2%, medium 56.6% to 53.1%, hard 28.2% to 26.2%.
  - Cost per task rose 70%, 49% and 47%.
- None of the three measures E2E tests or the value a kept suite gives to later changes. So the rule keeps E2E tests and keeps the run of the existing suite before a PR (lines 30, 31).
- Issue #119 and PR #120 port the rule into `writing-plans`, `brainstorming`, `codebase-design`, `improve`, `test-audit` and `omoikane-mode`: `bug-fix` step 5, `refactoring` step 1, principle `sequence-verifiable-units` (line 35).
- Before the PR, Claude Code on the user's machine already ran the updated personal copies in `~/.claude/skills/`; OpenCode, Pi and every system made from the template still got TDD (line 36).
- The user had already excluded pstack's `tdd` skill on 2026-10-07 (line 37).

## What it adds

- The study details the capture of session 0ac17a0f cut, the 44-task no-tests subset, the run count of DeepSWE, and the date of each post: [[template-skills-write-e2e-tests-only]].
- The user's rule, quoted from `CODING_STANDARDS.md`, for every task: [[tests-an-agent-writes-are-e2e-only]].
- A fourth agent-dotfiles commit, `97f852f`, and the two agent-dotfiles PRs, #126 and #128.
- A note on the shadowing: [[personal-skills-hide-stale-template-copies-in-claude-code]].
- The note's list of changed skills leaves out `multi-phase-plan`, which commit `e4ce3f7` of PR #120 also changed. The note does not claim a full list, so this is not a contradiction.
