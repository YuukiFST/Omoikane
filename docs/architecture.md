# Architecture

Three layers, as in Karpathy's LLM Wiki pattern, plus one rule that makes it run unattended: bookkeeping is code, only meaning goes through the LLM.

## Layers

| Layer | Path | Owner |
|---|---|---|
| Raw sources | `raw/` | Human. Immutable once in `raw/sources/`. |
| Wiki | `wiki/` | Agent. Every page, every cross-reference. |
| Schema | `AGENTS.md`, `prompts/` | Human and agent together. |

`CLAUDE.md` contains only `@AGENTS.md`, so Claude Code and OpenCode read one manual.

## Autonomy loop

```
raw/inbox/*  --Task Scheduler (bin/install-schedule.ps1)-->  bin/wiki-ingest.ps1
   for each file:  claude -p "/ingest <file>"   (or opencode run)
                   python bin/wiki-index.py      regenerate index.md
                   python bin/wiki-lint.py       structure check, non-zero on findings
                   git commit                    one commit per source
```

The agent's semantic pass (`/lint`) runs on demand or weekly and writes to `_review.md`.
It changes no page, so an unattended run cannot damage the wiki.

## What is deterministic and why

- `index.md` is generated from frontmatter. An LLM-maintained index drifts; a generated one cannot.
- `wiki-lint.py` catches broken links, orphans, missing keys, malformed dates and source pages without `dated`. It runs after every ingest, and its non-zero exit makes the agent fix its own mistakes inside the same call.
- `wiki-ingest.ps1` moves the source file itself if the agent forgot. A re-run with an empty inbox is a no-op.

## Where the human stays

- Curating what enters `raw/inbox/`.
- `_review.md`: contradictions and gaps the agent refuses to resolve alone.
- `AGENTS.md` Domain section: what the wiki is about, what to emphasise.
- Reading the wiki in Obsidian. The graph view shows hubs and orphans faster than any script.

## Growing it

- Search: when `index.md` passes a few hundred pages, add qmd or a small BM25 script and mention it in `AGENTS.md`.
- Review gate: switch `wiki-ingest.ps1` to commit on a `wiki/auto` branch and merge after reading the diff.
- Capture: point Obsidian Web Clipper, a synced phone folder, or an RSS fetcher at `raw/inbox/`.
