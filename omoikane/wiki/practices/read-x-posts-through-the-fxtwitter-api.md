---
title: Read X posts through the fxtwitter API
type: practice
summary: To read a post on x.com, fetch it from api.fxtwitter.com with curl; x.com blocks direct reads and the browser
tags: [procedure, research, x-com]
created: 2026-10-09
updated: 2026-10-09
sources: [wiki/sources/session-2026-10-02-680ff986.md, wiki/sources/session-2026-10-08-0ac17a0f.md, wiki/sources/2026-10-02-ste-and-oversight-posts.md]
---

## Rule

To read a post on x.com, fetch `https://api.fxtwitter.com/<user>/status/<id>` with `curl -s -A "Mozilla/5.0"`.
Do not try x.com first, directly or in the browser: it blocked both sessions.

## Evidence

- The user asked about two posts on X. The agent fetched them with `curl -s https://api.fxtwitter.com/karpathy/status/2105819303471976479`, checked `cdn.syndication.twimg.com/tweet-result`, and read both with `curl -s -A "Mozilla/5.0" "https://api.fxtwitter.com/$id"`. Its note: "Li os dois posts pelo fxtwitter, porque o X bloqueia leitura direta." (source: [[session-2026-10-02-680ff986]], turn 4). The ingested notes record the same access path (source: [[2026-10-02-ste-and-oversight-posts]]).
- For two posts on tests that agents write, the agent tried `cdn.syndication.twimg.com/tweet-result` and then `chrome-devtools-axi open https://x.com/kunchenguid/status/2108030810691629403` four times. Its note: "Os posts do X abriram pela API pública do fxtwitter; o navegador levou 403." (source: [[session-2026-10-08-0ac17a0f]], turn 7).

## Scope

Neither session found why x.com refused the read; the 2026-10-08 distill logged the 403 without a root cause.
The rule covers reading a post's text. Neither session needed anything the API does not return.
