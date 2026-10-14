---
title: interrogate
type: entity
summary: The review skill: one read-only reviewer per lens on the same model, then a lead sorts findings into four buckets
tags: [code-review, skills, pstack]
created: 2026-10-09
updated: 2026-10-09
sources: [wiki/sources/2026-10-08-cloudflare-ai-code-review.md]
code: [.claude/skills/interrogate/SKILL.md, .claude/skills/interrogate/references/rubric.md, .claude/skills/interrogate/references/reviewer-prompt.md, .claude/skills/interrogate/references/lead-judgment.md, omoikane/skills.md]
---

`.claude/skills/interrogate/` is the adversarial review skill every system ships ([[every-system-ships-the-development-skills]]).
It comes from [[pstack]] `pstack/skills/interrogate` at `df58112`, MIT; Omoikane runs one reviewer per lens instead of one per model (`omoikane/skills.md`, row `interrogate`).
The review route of [[omoikane-mode-routes-each-task-to-a-playbook]] sends every PR or diff review to it and to `blast-radius` (`.claude/skills/omoikane-mode/SKILL.md`, line 30).

## How it works

From `.claude/skills/interrogate/SKILL.md`:

1. Step 1 sets the scope: the files or diff the user names, or `git diff main...HEAD` on a feature branch.
2. Step 2 states the intent in one paragraph, from the user's message, the commits, the PR description and the code.
3. Step 3 spawns five read-only reviewers in one message: Correctness, Security, Code quality, Tests, Blast radius. Each gets the rubric sections of its lens. A lens is skipped only when the change gives it nothing to review.
4. Steps 4 and 5: the lead deduplicates, weights each finding by evidence and severity, and sorts it into Act on, Consider, Noted or Dismissed.

Without a subagent tool (Pi), the lenses run in sequence in the main thread.
Severities are `critical`, `warning` and `nit` (`references/reviewer-prompt.md`, line 41).
`references/lead-judgment.md`, "Verdict Calibration", says more than five Act On items means weak filtering.

## Gaps against Cloudflare's review system

The gap note on Cloudflare's "Orchestrating AI Code Review at scale" (2026-04-20) finds these gaps (source: [[2026-10-08-cloudflare-ai-code-review]]):

- No explicit "do not flag" list per lens; the Security section of `references/rubric.md` lists no exclusions.
- A re-review does not take the previous posted review as input (Step 1).
- The lens set does not scale with the diff size.
- Each of the five prompts holds the diff inline (`{DIFF_OR_FILES}`), not one shared file.
- Step 1 runs `git diff main...HEAD` with no noise filter (lock files, minified files).
- Step 2 reads the PR description with no rule to treat it as data.
- No overall verdict; the note rejects that one, since the human merges.

The note ranks a memory-drift check first: compare a diff with `AGENTS.md`, the skills and the domain pages, in `blast-radius` Step 1 rather than as a sixth lens here (same source).
None of these is an issue yet.
