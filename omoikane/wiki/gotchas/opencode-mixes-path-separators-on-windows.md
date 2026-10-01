---
title: opencode-mixes-path-separators-on-windows
type: gotcha
summary: OpenCode on Windows mixes C:/ and C:\ paths; normalise separators before relativising
tags: [opencode, windows, paths, ci]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-15-e04462b2.md]
code: [omoikane/bin/session-capture.py, tests/fixtures/opencode-export.json]
guard: test
---

## Behaviour

[[opencode]] on Windows mixes `C:/x` and `C:\x` between the session directory and tool input paths (source: [[session-2026-09-15-e04462b2]], turn 3).
The OpenCode fixture carried backslash paths; tests passed on Windows, but the first CI run on PR #10 failed on them on the Linux runner (turns 2, 3).

## Workaround

`relative_to` in [[session-capture]] replaces `\` with `/` in both the path and the cwd before resolving, so a transcript captured on Windows reads the same on a Linux CI runner (commit `fix(capture): normalise path separators before relativising`, turn 2).
The agent reproduced the Linux run locally with `MSYS_NO_PATHCONV=1 docker run ... python:3.11-slim python -m unittest discover -s tests` (turn 2).

## Guard

`tests/test_session_capture.py` reads `tests/fixtures/opencode-export.json` and asserts relative file paths; CI runs it on `ubuntu-latest`.
