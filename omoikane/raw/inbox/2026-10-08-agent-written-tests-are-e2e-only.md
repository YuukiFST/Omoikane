---
title: Tests an agent writes are E2E only
date: 2026-10-08
---

On 2026-10-08 the user asked how two posts and one study could help Omoikane, and approved the recommendation to make the template's skills E2E-only.
The user's global `CODING_STANDARDS.md` already holds the rule, from agent-dotfiles PRs #126 and #128 (commits f0202c8, 5a4c7a6, 825c9f8, 97f852f):

> E2E only: every test you write drives the outermost interface the caller touches (browser flow, HTTP request, CLI run, a library's public API); unit and integration tests are written only when the user asks for one.
> Bug repro is E2E: reproduce as the end user hits it; once green, that red test is the bug's one regression test.

## Sources

- Chen et al. 2026, "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", https://arxiv.org/abs/2602.07900 (SWE-bench Verified, 500 tasks, six models, mini-SWE-agent).
  - Writing tests does not separate resolved from unresolved tasks; gpt-5.2 writes a test in 0.6% of tasks and resolves 71.8%.
  - Agent tests are mostly value-printing probes, not assertions.
  - Discouraging tests: kimi-k2-thinking 317 to 304 resolved with 49% fewer input tokens; deepseek-v3.2-reasoner 300 to 291 with 33% fewer.
  - Encouraging tests: gpt-5.2 359 to 359 with 19.8% more output tokens; gemini-3-pro-preview 371 to 366.
  - The authors' conclusion is titled "Help or Habit?".
- Kun Chen, DeepSWE, Sonnet 5.5, 111 tasks, 444 runs, https://x.com/kunchenguid/status/2108030810691629403 (2026-10-08).
  - Banning agent-written tests: 65.3% to 66.2% solved (not significant), 6% less agent time and 9% less spend (significant).
  - Of 3000+ tests written, 65% were unit and 35% integration; neither bucket helped. Only 17 were E2E.
  - A 44-task subset that ran no tests at all, existing ones included, scored 59% against 59%.
  - The author: "both the implementation and the tests were simply the agent's interpretation of our intent".
  - The author states the eval says nothing about E2E tests or tests a human describes.
- Kun Chen, ProgramBench, GPT 5.5, 192 tasks, https://x.com/kunchenguid/status/2064196342248030352 (2026-06-09), read from the post's chart only; the thread with the method did not open.
  - TDD against baseline: easy 72.5% to 67.2%, medium 56.6% to 53.1%, hard 28.2% to 26.2%.
  - Cost per task rose 70%, 49% and 47%.

None of the three measures E2E tests or the value a kept suite gives later changes.
So the rule keeps E2E tests and keeps running the existing suite before a PR.

## Change

Issue #119 and PR #120 port the rule into the template's `writing-plans`, `brainstorming`, `codebase-design`, `improve`, `test-audit` and `omoikane-mode` (`bug-fix` step 5, `refactoring` step 1, principle `sequence-verifiable-units`).
Before the PR, Claude Code on the user's machine already ran the updated personal copies from `~/.claude/skills/`, which shadow the template's; OpenCode, Pi and every system born from the template still got TDD.
The user had already excluded pstack's `tdd` skill on 2026-10-07.
