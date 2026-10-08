# Cloudflare, "Orchestrating AI Code Review at scale": what it offers Omoikane

- URL: https://blog.cloudflare.com/ai-code-review/
- Author: Ryan Skidmore.
- Date on the page: April 20, 2026. Page metadata gives `dateModified` 2026-07-15.
- Read: 2026-10-08.

## How it was read

WebFetch returned a summary, not the full text.
`curl -sL` fetched the full HTML once. Every quote below comes from that text.
The page's images were not read. They may include an example review and charts.
The findings-by-reviewer table came through only in part.
The `risk.ts` snippet lost its first condition during text conversion. The tier table next to it is intact.

## What the article describes

Cloudflare runs up to seven specialist reviewers on each merge request, in CI, on OpenCode.
A coordinator merges, re-sorts and filters their findings, then posts one review comment.
Diff size sets the risk tier, and the tier picks the reviewer set and the model.
Re-reviews track earlier findings. A separate reviewer checks whether AGENTS.md needs an update.

## Ideas Omoikane lacks

1. **A "do not flag" list for each lens.**
   Quote: "telling an LLM what not to do is where the actual prompt engineering value resides."
   The security prompt excludes "Theoretical risks that require unlikely preconditions" and issues "in unchanged code".
   Omoikane already holds scattered do-not-flag rules: `reviewer-prompt.md` line 37, `rubric.md` lines 17, 43 and 72.
   `lead-judgment.md` line 37 drops changes to code the author did not write, but only at the lead step.
   The gap: no explicit do-not-flag list per lens, and the Security section of `rubric.md` (lines 70-77) has none.
   Affects: `.claude/skills/interrogate/references/reviewer-prompt.md`, `.claude/skills/interrogate/references/rubric.md`.

2. **A reviewer that checks whether the change makes the agent instructions stale.**
   Quote: "these files rot incredibly fast."
   It rates each change as high, medium or low materiality for an AGENTS.md update.
   Omoikane checks only size (`omoikane/bin/context-budget.py`) and dead `code:` paths (`omoikane/bin/wiki-lint.py`).
   `blast-radius` Step 1 already opens the decision and gotcha pages whose `code:` lists a changed file, and the review route always runs it.
   The gap: nothing checks a diff against `AGENTS.md`, the skills or the domain pages, and no step asks "does the diff contradict it".
   Affects: `.claude/skills/blast-radius/SKILL.md` Step 1, or the lens table in `.claude/skills/interrogate/SKILL.md`, Step 3. It is close to the memory half of `omoikane/wiki/domain/omoikane-objective.md`.

3. **Re-reviews that start from the previous review.**
   Quote: "an incremental re-review that is aware of its own previous findings."
   In a re-review, fixed findings are left out and unfixed ones come back. Findings the user resolved stay resolved.
   Omoikane re-reviews PRs, for example #92 and #56 in `omoikane/wiki/practices/review-each-pr-with-a-subagent-before-merging.md`.
   But `interrogate` Step 1 never takes the earlier posted review as input.
   Affects: `.claude/skills/interrogate/SKILL.md` Step 1, and that practice page.

4. **The diff size sets how many reviewers run.**
   Quote: "don't send the dream team to review a typo fix".
   Changes to sensitive paths such as `auth/` and `crypto/` always get the full review.
   `interrogate` always runs five lenses. It skips one only when the change gives that lens nothing to review.
   Affects: `.claude/skills/interrogate/SKILL.md` Step 3. The review route in `.claude/skills/omoikane-mode/SKILL.md` (line 30) always sends both skills.

5. **One shared context file for all reviewers.**
   Quote: "would multiply our token costs by 7x."
   Omoikane's reviewer template puts `{DIFF_OR_FILES}` inline in each of the five prompts.
   Affects: `.claude/skills/interrogate/references/reviewer-prompt.md`, `.claude/skills/interrogate/SKILL.md` Step 3.

6. **Diff noise filtering, with migrations exempt.**
   Quote: "we explicitly exempt database migrations from this rule".
   Lock files, vendored code, minified files and source maps are removed before review.
   `interrogate` Step 1 runs `git diff main...HEAD` with no filter.
   Affects: `.claude/skills/interrogate/SKILL.md` Step 1. This matters more in systems built from the template than in this repo.

7. **Strip prompt boundary tags from author-written text.**
   Quote: "never underestimate the creativity of Cloudflare engineers".
   Babysit treats comment text as untrusted (`.claude/skills/omoikane-mode/playbooks/babysit.md`, line 17).
   `interrogate` Step 2 takes the PR description into the intent, and no rule says to treat it as data.
   `blast-radius` Step 1 also reads the PR body (`gh pr view --json title,body`) with no treat-as-data rule.
   Affects: `.claude/skills/interrogate/SKILL.md` Step 2, `.claude/skills/interrogate/references/reviewer-prompt.md`, `.claude/skills/blast-radius/SKILL.md` Step 1.

8. **An overall verdict that follows a rubric, with a bias toward approval.**
   Quote: "The bias is explicitly toward approval".
   Each severity mix maps to approve, approve with comments, unapprove, or request changes.
   `interrogate` sorts findings into act on, consider, noted and dismissed, but gives no overall verdict.
   Affects: the output format in `.claude/skills/interrogate/SKILL.md`.

## Already covered, same or better

- Reviewers that each look through one narrow lens: `.claude/skills/interrogate/SKILL.md`, Step 3 (five lenses).
- A judge pass that merges duplicates and drops speculative findings: `interrogate` Steps 4 and 5, and `.claude/skills/interrogate/references/lead-judgment.md`.
- When unsure, the lead reads the code to check: `lead-judgment.md`, "Hypothetical vs. Actual", says "Trace the call site."
- Few findings on purpose (about 1.2 per review): `lead-judgment.md`, "Verdict Calibration", which caps Act On near five.
- Severity levels critical, warning, suggestion: `.claude/skills/interrogate/references/reviewer-prompt.md` uses critical, warning, nit.
- One review posted on the PR: `omoikane/wiki/practices/review-each-pr-with-a-subagent-before-merging.md`, and `.claude/skills/omoikane-mode/SKILL.md` line 30.
- Respecting a "won't fix" reply: `.claude/skills/omoikane-mode/references/automated-review-triage.md`, "Owner-declared follow-up or deferred cleanup".
- Cross-system impact, a limitation the article admits: `.claude/skills/blast-radius/SKILL.md` goes further. It proves the key safety fact by running code.
- Missing architectural context, also admitted: `blast-radius` Step 1 opens the decision and gotcha pages whose `code:` lists a changed file.
- A local command for a full review: `interrogate` already runs in the session. The article added `/fullreview` for local use.
- A human override: the human already owns every merge in Omoikane. See the practice page and `omoikane-mode` line 100.

## Candidate issues

Ranked by value for the objective.

1. Check each diff for memory drift: against `AGENTS.md`, the skills and the domain pages, asking whether the diff contradicts them. Extend `blast-radius` Step 1, which already opens the decision and gotcha pages, rather than add a sixth `interrogate` lens.
2. Add a "do not flag" section to each lens in `rubric.md`, starting from the article's security exclusions.
3. Make a re-review read the previous posted review: leave out fixed findings, repeat unfixed ones, respect resolved ones.
4. Scale the lens set to the diff size, and always run every lens on security-sensitive paths.
5. Write the filtered diff once to a temp file for all reviewers to read. Drop lock files and minified files, keep migrations.

Not worth it:

- Idea 8, the approval verdict: Omoikane posts a comment and the human merges, so an automatic approve or block decides nothing.
- "break glass": the human already holds every merge, so no gate needs an override.
- Model tiers, circuit breakers, fallback chains, the Workers KV control plane, telemetry: these serve a CI service at scale. Omoikane reviews in-session on one model.
- Idea 7 alone: it is small. Fold it into issue 3 or 5 when someone edits Step 1 or Step 2.
- The one light-hearted answer per review: it does not serve the objective.

## Reference?

Yes, if the user approves. It is the most detailed source read so far on multi-agent code review.
The rule text on `omoikane/wiki/domain/omoikane-references.md` (line 14) still names only capture, distill, storage and loading.
The list itself already holds review-side entries the user added on 2026-10-07: the Cloudflare security-audit-skill and "Build your own vulnerability harness" (lines 21-22).
So the rule text lags the list, and this post fits the list's current practice.
The user added every entry on that page, so the agent should only propose this one, through `omoikane/_review.md` or an inbox note.
The reason to add it: `interrogate` and the review triage would gain a reference to check before they change.
