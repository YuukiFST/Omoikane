### Multi-phase or multi-PR plan

**You own the plan, not the code. The plan is a checklist an owner runs box by box and the user audits from the evidence.** The plan is the deliverable. Do not implement.

1. When the change is one or two files with an obvious approach, skip the plan. Say so and stop.
2. Settle open questions by prototype before you write. Run `prototype.md` for each. Keep the branch, the SHA, and the screenshots for Appendix A. Ask the user only about a product or preference call that no run can settle. Give options (principle `never-block-on-the-human`).
3. Explore in fresh subagents (principle `guard-the-context-window`). Each returns file pointers, conventions, test commands, and entry points. No inlined dumps. Open the decision and gotcha pages whose `code:` lists the areas the plan touches.
4. Copy the skeleton below into the plan file and fill every placeholder. Unless the user names a path, write the file under `docs/plans/`. Keep every heading and every sub-block in the order shown. One section per PR. One PR is one change with its own evidence (principle `sequence-verifiable-units`). Name the execution playbook in **How to read this**: `autonomous-run.md` for an unattended run, or the **executing-plans** skill for a run with review checkpoints.
5. Write the body as one Diátaxis mode, how-to. Appendices hold explanation and reference. Each heading states the task or the finding. Short sentences.
6. Check the plan against the skeleton: every heading present in order, every box names its evidence, and no placeholder left. `grep -nE '<[A-Za-z][^>]*>' <plan.md>` lists the leftover placeholders. Fix every hit (principle `encode-lessons-in-structure`).
7. Hand back. Post the plan path and the check's output, then stop. Execution starts on the user's explicit go, under the execution playbook the plan names.

**Verification.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked (principle `prove-it-works`). That sentence is the verification rule. Every verification block opens with it. The live block is mandatory. Ten lanes at the PR head drive the real surface through the project's verification skill, each lane a fresh subagent; without a subagent tool the lanes run one after another. Each lane is one box with a concrete scenario, the screenshot or output it saves, and its pass predicate. One lane is the **Regression lane against trunk.** It runs the same load-bearing scenario on trunk and head. If trunk does not have the feature, the lane records that fact and gates the behavior the diff adds plus the end state the user waits for instead of inventing a trunk result. The perf gate is dual-sided. Trunk and head must both produce the named metric. If trunk lacks the feature, also isolate the work the diff adds and set an absolute budget for that work plus the end-to-end state the user waits for. Do not claim a ratio between unlike scenarios. The perf block names the metric, the interleaved probe, the trunk baseline measured first, and the rule with the number that fails. A PR that changes an interaction is review-gated. The user reviews it in chat with screenshots and a video before merge. A PR that changes no interaction writes `**Review gate.** None. <PR id> is not review-gated.` and no boxes under it.

**Verification skill.** Pick it by surface: the project's `verify-<app>` skill under `.claude/skills/`. A surface with none gets one from the **create-verification-skill** skill before the live lanes run. A PR that touches two surfaces gets lanes on both. A surface with no verification skill is a risk in Appendix C, and its live block still names how each lane drives it.

````markdown
# <Program> plan

<Under ten lines. What changes, for whom, the rule the program enforces, and the PR ids in order.>

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs <`.claude/skills/omoikane-mode/playbooks/autonomous-run.md` or the executing-plans skill>. <Who merges, and which PR ids stop at merge-ready for the user.>

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the user, then stop. Start execution only on the user's explicit go.
- [ ] Read these from trunk at program start. Re-read them at every tick.
  - [ ] `git show origin/main:.claude/skills/omoikane-mode/playbooks/<execution playbook>.md`
  - [ ] `git show origin/main:<verification skill path>`
  - [ ] `git show origin/main:.claude/skills/omoikane-mode/playbooks/opening-a-pr.md`
  - [ ] `git show origin/main:.claude/skills/<each other skill the program uses>/SKILL.md`
- [ ] On the user's go, arm the audit tick with the harness's scheduler (Claude Code `/loop 1h`), or run it at every phase boundary when the harness has none. Never leave the cadence to memory.
- [ ] Use this tick prompt, verbatim. "Re-read the execution playbook from trunk. Audit the operation against it and fix drift in this tick. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement now. Then post a short status message to the user in chat only when the audit found a tracked change that no earlier status message reported, such as a PR opened, a code-ready head, a round launched or closed, a verdict, a merge, a stuck agent and the action taken, a blocker added or cleared, or a decision only the user can make. Name every such change and nothing else. Do not repeat a table, the merged list, or an unchanged blocker. If the audit found none, end the turn with no reply text. Either way, log this tick's row in your decision log. The row names the items reported, or none."
- [ ] On the user's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR, a fresh subagent with the full lifecycle the execution playbook names.
- [ ] Follow this dependency graph. Start dependent work only after its parent merges, or base it on the parent branch when the execution playbook stacks.
  - [ ] <PR id> and <PR id> are independent and first. Both branch from `main`.
  - [ ] <PR id> after <PR id>.
- [ ] Hold the file boundaries. <PR id or class> touches only `<glob>`.
- [ ] Hold the review gate. <PR ids> change an interaction. They wait for the user's review in chat with screenshots and a video before merge.

### PR mechanics, for every PR

- [ ] Use `gh` for every PR operation. Never require `gt`.
- [ ] Open the PR ready, never draft, per **Opening a PR**. Use the harness's built-in PR tool when it has one, else `gh pr create --base <base-branch>`. A stack child targets its parent branch.
- [ ] Run the repo's lint and typecheck once before the PR-facing push. Push with hooks on.
- [ ] Run the code-simplifier skill before each commit.
- [ ] Triage every automated reviewer and security-reviewer comment per `.claude/skills/omoikane-mode/references/automated-review-triage.md`.
- [ ] Rebase onto current trunk before the code-ready report and babysit. Keep that merge base in fix rounds. Rebase again only at merge prep, on a `git merge-tree` conflict with trunk, or on a CI failure that comes from a change on trunk.

### Verdict and merge, for every PR

- [ ] At the code-ready head SHA and at each later push that changes the patch, run the verification lanes, each a fresh subagent. One gates lane. The ten live lanes from the PR's **Verify, live** block. The perf lane from its **Verify, perf** block. Two or more audit lanes, each with its own lens, that read the diff and the receipts and distrust the PR body. The root audits the receipts in the merge-ready report before the verdict.
- [ ] Clean only when every lane is `PASS`. Findings go back to the owner, including a defect that a lane filed as a note. A new head gets fresh lanes and a fresh verdict, except for results that stay valid under the patch-id rule in `.claude/skills/omoikane-mode/playbooks/shipping.md`.
- [ ] <The merge rule from the execution playbook, with the patch-id rule from `shipping.md`. Merging needs the user's authorization.>

### Boot recipe, for every live lane

Each live lane runs in its own worktree or sandbox at the PR head. Drive through the project's verification skill.

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] <Start the backend and the surface. Wait for ready.>
- [ ] <Deliver input only through the verification skill's commands. Name the read-only diagnostics.>
- [ ] Save every screenshot or output to a lane-owned scratch folder (`<scratch>/<pr-id>/lane-<n>/<slug>.png`) and return the paths with the report.

## <Task as a verb phrase> (<PR id>)

**Depends on.** <PR id, or None.>

**Files.**

- [ ] Edit `<path>`.
- [ ] Create `<path>`.
- [ ] Delete `<path>`.

**Build.**

- [ ] <One change. Name the symbol and the file.>

**You see.**

- [ ] <One observable result, with the exact log line or screen state.>

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] <Test file and the case it gains.> Run `<command>`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run <the same load-bearing scenario> at trunk and head. If trunk lacks the feature, record that and gate <the behavior the diff adds plus the end state the user waits for>. Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 2. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 3. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 4. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 5. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 6. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 7. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 8. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 9. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 10. <Scenario.> Save `<slug>.png`. Pass when <predicate>.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. <What is measured at both trunk and head. If trunk lacks the feature, also name the diff-added work and the end-to-end state the user waits for.>
- [ ] Probe. <The command or procedure, run at trunk and at the head, interleaved. Both sides must produce the metric.>
- [ ] Baseline. Record the trunk <value> first.
- [ ] Rule. <Head against trunk, with the number that fails. If the scenarios differ, add absolute budgets for the diff-added work and the user-visible end state instead of an invalid ratio.>

**Review gate.** The user reviews before merge.

- [ ] Copy lane <n> screenshots into `<media path>/<pr-id>-review-<slug>.png`.
- [ ] Record a 30 to 60 second video of the change in a lane's worktree. Save it as `<media path>/<pr-id>-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at merge-ready. Wait for the user's go.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Automated review triage done.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] <Who merges, once the user authorized it, and in which order.>

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the user with the report the execution playbook names.

## Appendix A. Prototype evidence

<Each open question a prototype answered, with the branch, the SHA, and the artifact links. Each question that stays unproven.>

## Appendix B. Alternatives rejected

<Each approach weighed and why it lost.>

## Appendix C. Risks

<Each risk with the PR it lands in and what the owner watches.>

## Appendix D. Links and reading list

<Docs and wiki pages to read before editing. Which PRs get `.claude/skills/how/SKILL.md` and `.claude/skills/interrogate/SKILL.md`. The decision log's path.>
````

**Reply:** the plan path, the PR ids with their dependencies and the review-gated set, what the prototypes proved and what stays unproven, and the placeholder check's output.

Adapted from pstack `skills/poteto-mode/playbooks/multi-phase-plan.md` at df58112. MIT, see `../LICENSE`.
