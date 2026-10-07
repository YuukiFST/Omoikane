---
name: how
description: "Use for \"how does X work\", a code walkthrough before changing something, and placement questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture and runtime flow."
---
<!-- Source: cursor/plugins pstack/skills/how at df58112 (MIT, Lauren Tan); adapted for one model, see omoikane/skills.md -->

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Every spawn below is a read-only subagent on the session's model. Without a subagent tool (Pi), run the steps in sequence in the main thread: explore each area in turn, write its findings down, then write the explanation from them.

## Step 1. Assess Complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. One explainer explores and explains in a single pass. Go to Step 2b.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): spawn parallel explorers first, then hand off to the explainer. Go to Step 2a.

When in doubt, take the simple path.

## Step 2a. Explore (complex questions only)

Decompose the question into 2 to 4 areas, each a distinct slice of the subsystem (a module, a layer, a stage of the flow). Spawn one read-only subagent per area, all in a single message.

Each explorer gets the prompt in `references/explorer-prompt.md` with its area filled in. Then go to Step 3.

## Step 2b. Direct Explain (simple questions)

Spawn one read-only subagent that explores and explains in one pass.

Build its prompt from `references/explainer-prompt.md` without the explorer-findings section. Go to Step 4.

## Step 3. Synthesize (complex questions only)

Once all explorers have returned, spawn one read-only subagent to synthesize their findings into one explanation.

Build its prompt from `references/explainer-prompt.md` with every explorer's findings filled in.

## Step 4. Present

Present the explainer's output to the user. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output Format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
