---
title: TypeScript misnamed plugin hook passes without satisfies
type: gotcha
summary: tsc let a misnamed hook on the OpenCode plugin's returned object pass; `satisfies Hooks` makes it fail with TS2561
tags: [opencode, typescript, ci]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-10-01-b5b6fb27.md]
code: [.opencode/plugins/omoikane.ts, .github/workflows/ci.yml]
guard: test
---

## Behaviour

PR #48 (issue #46) typechecks the Pi and OpenCode plugins in CI (source: [[session-2026-10-01-b5b6fb27]], turn 2).
Its subagent review found that a wrongly named hook would still pass; the resolution comment on the PR: "1 fixed in `bf0f37a` (`satisfies Hooks` on the returned object; with `dispose` renamed `disposex` tsc now fails with `TS2561: Object literal" (the capture clips the rest) (turn 2).

## Workaround

Put `satisfies Hooks` on the object the plugin returns; the agent proved it red by renaming `dispose` to `disposex` (source: [[session-2026-10-01-b5b6fb27]], turn 2).
The same PR runs the install with `--ignore-scripts` (turn 2).
PR #48 has merged since: the CI step "Typecheck harness plugins" fails on a misnamed hook. See [[opencode]], [[opencode-run-exits-before-plugin-event-handlers-finish]] (why `dispose` matters).
