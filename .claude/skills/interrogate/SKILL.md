---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"challenge this\", \"stress test this code\", \"find blind spots\", \"tear this apart\", or a review before merge. Reviewers with different lenses challenge a change; the lead sorts their findings."
---
<!-- Source: cursor/plugins pstack/skills/interrogate at df58112 (MIT, Lauren Tan); reviewers by lens instead of by model, see omoikane/skills.md -->

# Interrogate

Spawn one reviewer per lens to adversarially review code changes. Each reviewer gets the same intent and code, plus the rubric sections of its own lens. The adversarial signal comes from lens diversity: every reviewer runs on the same model, so what differs is where each one looks.

The deliverable is a synthesized verdict. Do NOT auto-apply changes.

Without a subagent tool (Pi), run the steps in sequence in the main thread: review through one lens at a time, write its findings down before you start the next lens, then synthesize.

## Step 1, Determine Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset
- If the user's message references recent work, gather the relevant files

Package the diff (or file contents) plus any surrounding context files the reviewers need to understand the code.

## Step 2, State the Intent

Before spawning reviewers, state the intent explicitly. Derive this from:

- The user's message
- Commit messages
- PR description if one exists
- The code itself

Write one clear paragraph. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Launch all reviewers in a single message, each a read-only subagent. One reviewer per lens:

| Reviewer | Lens | Rubric sections (`references/rubric.md`) |
|----------|------|------------------------------------------|
| Correctness | Does the code do what the intent says, on the sad path too? | Correctness; Root Causes vs. Symptoms |
| Security | Can an input reach a dangerous sink or skip a check? | Security |
| Code quality | Is the structure as simple as it can be? | Structural Integrity; Complexity Budget; plus all of `references/code-quality-review.md` |
| Tests | Can you tell from the tests that the code works? | Verification |
| Blast radius | What does the change break outside the diff? | Blast Radius |

Skip a lens only when the change gives it nothing to review (no input, auth or secret handling for Security; no tests and no testable behavior for Tests), and name the skipped lens and the reason in the verdict.

Read `references/reviewer-prompt.md` and fill in the template for each reviewer with:
1. The stated intent
2. The diff or file contents
3. The reviewer's lens, from the table
4. The rubric sections of that lens, copied from `references/rubric.md`
5. For the Code quality reviewer only, the contents of `references/code-quality-review.md`

## Step 4, Synthesize

As results come back, build a unified picture:

1. **Parse all findings** from the reviewers
2. **Identify consensus**. Findings raised independently by 2+ reviewers, from different lenses, are highest signal.
3. **Identify lone-reviewer findings**. Still worth reading, but weight accordingly.
4. **Deduplicate**. Different reviewers may describe the same issue differently. Merge these and note which reviewers raised it.
5. **Note disagreements**. If one reviewer flags something and another explicitly says the opposite, that's useful context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator.

Read `references/lead-judgment.md` for the full framework.

Categorize every finding using these buckets:

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. These would block a real PR.
- **Consider**. Legitimate points, but you're not sure they outweigh the cost of addressing them right now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact given the current stage.
- **Dismissed**. Wrong, nitpicky, or missing context. Brief explanation why.

For each finding, include:
- Which reviewer(s) raised it
- The category (act on / consider / noted / dismissed)
- A one-line rationale for the categorization

## Output Format

Present the verdict in this structure:

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [lens]: [N findings] (one bullet per reviewer; name any skipped lens and why)

### Act On
[Findings that should be addressed. For each: description, which reviewers raised it, why it matters.]

### Consider
[Findings worth thinking about. For each: description, which reviewers raised it, tradeoff involved.]

### Noted
[Valid but low-priority. Brief list.]

### Dismissed
[Rejected findings with brief rationale.]

### Agreement Map
[Where did the lenses agree, where did they diverge, and what does the pattern of agreement/disagreement tell us?]
