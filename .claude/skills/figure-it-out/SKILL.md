---
name: figure-it-out
description: "Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Use for /figure-it-out, 'figure it out', a large migration, or when no omoikane-mode playbook applies."
---

# Figure it out

When the task matches no playbook, design one. The deliverable before any code is the workflow itself: a sequence of phases that scales rigor to the task, runs the scientific method, and leaves a decision trail a human can audit after stepping away.

## Start

Open a todolist whose first item is to read the Principles section of the **omoikane-mode** skill. Then add the phases below as todos. Each principle named below is one of omoikane-mode's principles.

## Phase A: Frame

Ground first, then commit. Don't start the run until you can state:

- The definition of done as a falsifiable predicate (the **prove-it-works** principle).
- Scope, quantified: rough units and effort, plus the blockers grounding surfaced.
- The rigor level, biased high. One-way doors and high blast radius get more. Reversible low-stakes steps get less. Rigor is gates and artifacts, not "try harder".

Present the framing and tradeoffs before committing to a long run. Reversible work proceeds (the **never-block-on-the-human** principle), but a multi-hour run earns one checkpoint.

## Phase B: Design the workflow

Decompose into atomic, independently-landable units. Sequence riskiest-unknown-first. Scaffold and verification come before features (the **foundational-thinking** principle).

- Build the verification harness before the work, with the baseline captured from the pre-change state, so the check reads as "old value vs new value".
- For one-way-door design decisions, write two structurally different sketches from one model and compare them before choosing (the **codebase-design** skill's design-it-twice method). Skip it for mechanical work whose shape is already concrete. A second round of sketches over a settled design is over-engineering (the **laziness-protocol** principle).
- Decide what fans out. Parallelize only across seams, and give each worker its own worktree or branch (the **separate-before-serializing-shared-state** principle). Don't over-fan. Without a subagent tool (Pi), run the steps in sequence in the main thread.
- Write the designed phase list down. That list is what the human reviews.

Then execute the design. Add its steps to the todolist as concrete items, after the Phase C entry and before Phase D. Run each under the Phase C loop discipline, and weave the Phase D log through them, a row as each step lands, rather than saving the whole trail for the end.

## Phase C: Run the loop

Each unit is an experiment. State the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep it if it advanced, revert it if it didn't.
Apply the **sequence-verifiable-units** principle, verifying each unit before starting the next instead of batching checks at the end.

- Verify by inspecting the artifact, never a self-report. When something passes too easily, suspect the observation method before the system.
- Pair delegated work with a judge. If a worker games the gate, reset and harden the contract. If the gate itself is wrong, fix the gate in its own change rather than routing around it.
- A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Don't hide a negative.

## Phase D: Keep the decision log

Keep a plain decision log in the plan file: one row per decision, with what was decided, the alternatives, the reason, and the evidence. figure-it-out's work is usually ambitious enough to commit the plan file so the reviewer can read it in the PR. The log plus the diff is what lets the human come back and trust the work.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real product, not just the harness. Encode any recurring correction as a gate, a lint rule, a check, or a script (the **encode-lessons-in-structure** principle).

**Reply:** the playbook you designed, the rigor level and why, the plan file path, what's verified against the predicate, and what's still open.
