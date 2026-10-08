---
title: Tests an agent writes are E2E only
type: domain
summary: Each test an agent writes drives the outermost interface; write unit or integration tests only when the user asks
tags: [convention, testing]
created: 2026-10-08
updated: 2026-10-08
sources: [wiki/sources/2026-10-08-agent-written-tests-are-e2e-only.md]
---

## Rule

Write each test through the outermost interface the caller touches: a browser flow, an HTTP request, a CLI run, or a library's public API.
Write a unit or integration test only when the user asks for one.
Reproduce a bug as the end user hits it; once it passes, that test is the bug's one regression test.

The user's global `CODING_STANDARDS.md` holds the rule, from agent-dotfiles PRs #126 and #128 (source: [[2026-10-08-agent-written-tests-are-e2e-only]], line 7):

> E2E only: every test you write drives the outermost interface the caller touches (browser flow, HTTP request, CLI run, a library's public API); unit and integration tests are written only when the user asks for one.
> Bug repro is E2E: reproduce as the end user hits it; once green, that red test is the bug's one regression test.

## Where it applies

- Every task: the rule sits in the user's global standards, so it holds in this repository too.
  Every system made from the template gets it through the template's skills since PR #120: [[template-skills-write-e2e-tests-only]].
- Run the existing suite before a PR; the rule limits the tests you write, not the tests you run (source: [[2026-10-08-agent-written-tests-are-e2e-only]], line 31).
- The rule does not touch E2E tests or tests the user describes: the evidence behind it measured neither (lines 25, 30).
