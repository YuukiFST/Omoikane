---
title: Template skills write E2E tests only
type: decision
summary: The template's skills make each test an agent writes E2E, unit or integration only on request; TDD dropped (PR #120)
tags: [skills, testing, omoikane-mode, template]
created: 2026-10-08
updated: 2026-10-08
sources: [wiki/sources/session-2026-10-08-0ac17a0f.md, wiki/sources/2026-10-08-agent-written-tests-are-e2e-only.md]
code: [.claude/skills/writing-plans/SKILL.md, .claude/skills/test-audit/SKILL.md, .claude/skills/omoikane-mode/playbooks/bug-fix.md, .claude/skills/omoikane-mode/playbooks/refactoring.md, .claude/skills/omoikane-mode/playbooks/multi-phase-plan.md, .claude/skills/omoikane-mode/references/principles/sequence-verifiable-units.md, omoikane/skills.md]
---

## Chosen

The skills the template ships tell an agent to write E2E tests only, and unit or integration tests only when the user asks for one (source: [[session-2026-10-08-0ac17a0f]], turns 8, 9).
Issue #119 and PR #120 made the change; PR #120 merged as `ef99d30` (turn 10).

The rule the skills follow is the user's own, for every task: [[tests-an-agent-writes-are-e2e-only]].

- Copied from the user's agent-dotfiles commits `f0202c8`, `5a4c7a6` and `825c9f8`: `writing-plans`, `brainstorming`, `codebase-design`, `improve`, `test-audit` and the principle `sequence-verifiable-units` (turns 8, 9).
  The inbox note puts the rule in agent-dotfiles PRs #126 and #128 and adds a fourth commit, `97f852f` (source: [[2026-10-08-agent-written-tests-are-e2e-only]], line 7).
- Written for Omoikane (turn 9):
  - `bug-fix` step 5: the repro becomes an E2E test that fails on the parent of the fix commit and passes with the fix.
  - `refactoring` step 1: pin current behaviour through the outermost interface before the structure moves.
  - `multi-phase-plan`: the block "Verify, unit" becomes "Verify, tests", an E2E test or the existing suite (`omoikane/skills.md`).
- Each change is recorded in the skill's row of `omoikane/skills.md` (turn 8).
- Checks before the PR: 194 tests passed, `context-budget` and `wiki-lint` gave 0 findings, and no skill mentions TDD (turn 8).
  The subagent review found three medium issues, which the agent fixed; two low findings stayed as written (turns 8, 9).

## Rejected

Keep TDD in the template's skills.
The agent's turn-7 reading of one study and two posts by `kunchenguid` on X (source: [[session-2026-10-08-0ac17a0f]], turn 7):

- DeepSWE with Sonnet 5.5: a ban on tests gave 66.2% solved against 65.3% with tests, a difference that is not significant. Time fell 6% and spend 9%, both significant.
  Of 3000+ tests written, 65% were unit and 35% integration; neither group improved the result.
  The author: "both the implementation and the tests were simply the agent's interpretation of our intent".
  The run had 111 tasks and 444 runs, posted 2026-10-08. A subset of 44 tasks that ran no tests at all, existing tests included, scored 59% in both arms (source: [[2026-10-08-agent-written-tests-are-e2e-only]], lines 20, 23).
- ProgramBench with GPT 5.5, 192 tasks, TDD against baseline: easy 72.5% to 67.2% at +70% cost, medium 56.6% to 53.1% at +49%, hard 28.2% to 26.2% at +47%. The agent did not know if the differences are significant.
  The post is from 2026-06-09; the agent read its chart only, because the thread with the method did not open (source: [[2026-10-08-agent-written-tests-are-e2e-only]], line 26).
- The study, Chen et al. 2026, "Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents", arXiv 2602.07900: SWE-bench Verified, 500 tasks, six models, mini-SWE-agent (source: [[2026-10-08-agent-written-tests-are-e2e-only]], lines 14 to 19).
  - Writing tests does not separate resolved from unresolved tasks: gpt-5.2 writes a test in 0.6% of tasks and resolves 71.8%.
  - Agent tests are mostly probes that print values, not assertions.
  - With tests discouraged, kimi-k2-thinking went from 317 to 304 resolved with 49% fewer input tokens, and deepseek-v3.2-reasoner from 300 to 291 with 33% fewer.
  - With tests encouraged, gpt-5.2 stayed at 359 with 19.8% more output tokens, and gemini-3-pro-preview went from 371 to 366.
  - The authors title their conclusion "Help or Habit?".

The agent's conclusion: "TDD imposto ao agente piorou o resultado. Isso agrega ao Omoikane, porque o template ainda ensina TDD aos agentes." (turn 7).

## Scope

The DeepSWE run had almost no E2E tests (17), so it says nothing about them (turn 7). E2E tests stay.
Its author says the same of E2E tests and of tests a human describes (source: [[2026-10-08-agent-written-tests-are-e2e-only]], line 25).
None of the three sources measures E2E tests or what a kept suite gives later changes, so agents still run the existing suite before a PR (lines 30, 31).
The rule already held in the user's `CODING_STANDARDS.md` and personal skills; only the template's copies lagged (turn 9). Why that went unseen: [[personal-skills-hide-stale-template-copies-in-claude-code]].

## History

On 2026-10-07 the user had already excluded pstack's `tdd` skill: [[every-system-ships-the-development-skills]].
The playbooks this changes belong to [[omoikane-mode-routes-each-task-to-a-playbook]].
