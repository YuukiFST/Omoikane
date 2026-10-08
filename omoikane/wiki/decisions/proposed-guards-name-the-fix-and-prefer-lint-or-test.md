---
title: Proposed guards name the fix and prefer lint or test
type: decision
summary: A guard /distill proposes fails on the session's mistake, prefers lint or test to a hook, names the fix; PR #99 merged
tags: [distill, guards, prompts, pstack]
created: 2026-10-06
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-05-1de79b19.md, wiki/sources/2026-10-06-pstack-is-an-omoikane-reference.md]
code: [omoikane/prompts/distill.md, docs/architecture.md]
---

## Decision

The `guard` destination in `distill.md` changes in three ways (source: [[session-2026-10-05-1de79b19]], turn 1; issue #98, PR #99):
- the test of a guard becomes "the mistake this session made is an input on which the check fails", where `main` says "you can name an input on which the check fails";
- a lint or test is preferred over a hook;
- the check's error names what to write instead.

The idea comes from pstack's `/correct`: "a lint or CI check whose error names the file, type, or function to use instead" (issue #98): [[pstack]].

## Reasons

- A later agent that trips the check reads its error, not the wiki page behind it (issue #98; `docs/architecture.md` on the branch).
- CI and every harness run a lint or a test, while a hook runs in one harness only (issue #98). The reviewer checked that hooks are per harness: `.claude/hooks`, `.opencode/plugins`, `.pi/extensions` (PR #99 review comment, turn 3).
- A check proven on the mistake the session made, not on an input invented for it (commit `be2061c`).

## Rejected alternative

A paragraph telling `/distill` that a rule already on a page and broken again becomes a guard proposal, after pstack's `/correct` (turn 1, branch first named `feat/tmp-escalate`).
The eval showed `main` already does it: both the before and after runs routed the broken integer-cents rule to a guard, so the agent dropped the paragraph and the matching `synthesize.md` edit as redundant (turn 1; PR #99 body).

## Status

At capture PR #99 was open, CI green, with a subagent review comment of no findings, not merged (turn 3).
The eval fixture `tests/fixtures/distill-domain-session-3.md` exists only on the branch.
PR #99 merged on 2026-10-06 (source: [[2026-10-06-pstack-is-an-omoikane-reference]]; merge commit `01f039b`).
