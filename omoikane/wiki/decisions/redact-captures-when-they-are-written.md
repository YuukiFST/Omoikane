---
title: Redact captures when they are written
type: decision
summary: session-capture.py replaces terms listed in the gitignored omoikane/.capture-redact before the capture is written
tags: [redaction, session-capture, public-repo, privacy]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-10-02-1b324082.md]
code: [omoikane/bin/session-capture.py, tests/test_session_capture.py]
---

Chosen: `omoikane/bin/session-capture.py` replaces every term listed in `omoikane/.capture-redact`, one per line, with `[redacted]` in the capture it writes (issue #62, PR #69) (source: [[session-2026-10-02-1b324082]], turn 3).
The list is gitignored, since it names the terms; the agent also kept the local copy out through `.git/info/exclude` (turn 3).

Rejected: cleaning captures after they land, which is what #63 had to do in the same session: rewrite the pages, the `log.md` line and the raw captures already under `omoikane/raw/sources/sessions/`, which are otherwise immutable (turn 3).

Reason: the scheduled run commits and pushes every capture to the public repository, so a term must be gone before the file exists; the code comment on `REDACT_FILE` says the same (turn 3).
The trigger was a captured session naming the company toolkit 15 times, about to be published by the next scheduled run (turn 3): [[company-internal-material-stays-out-of-the-public-repo]].

What the first version got wrong: [[capture-redaction-breaks-on-frontmatter-clips-and-encodings]].
Module: [[session-capture]].
