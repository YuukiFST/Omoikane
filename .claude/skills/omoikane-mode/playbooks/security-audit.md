### Security audit

**You own the trust boundary. Confirm a finding from source before you call it one, and stay inside the sandbox.**

The **security-audit** skill holds the method. This playbook picks its mode and routes what it finds.

1. Pick the mode before you load anything else.
   - **Guidance mode** is the default: a security question, a focused review of a change that touches auth, input handling, secrets or permissions, methodology, or triage of one finding.
   - **Full audit mode** only on an explicit request to audit or pen-test the codebase, a request for a full, comprehensive or end-to-end security review, or a request for report artifacts.
   - If the request could mean either, ask one focused question before you create files or start the full workflow.
2. Load the **security-audit** skill and follow the chosen mode. In guidance mode, use only the parts that apply: no output directory, no audit artifacts. Full audit mode runs every phase with parallel subagents. Without a subagent tool (Pi), run guidance mode only and say that a full audit needs a harness with subagents.
3. Hold the skill's execution-safety rules. Run target code only inside the sandbox it requires. Never probe deployed endpoints, shared services or real identities. When the sandbox cannot be enforced, report the check as needs-validation with a safe plan instead of running it.
4. Open the gotcha and decision pages whose `code:` lists the area under review. A past security decision is context, not proof that the code is still safe.
5. Route each confirmed finding to the Bug fix playbook (`bug-fix.md`): one PR per finding, with a red-first proof. Keep a candidate without a concrete affected principal, resource or outcome as needs-validation, not as a finding.
6. Run **Opening a PR** for each fix.

**Reply:** the mode and why, the scope covered and what was left out, each confirmed finding with its evidence, priority and smallest fix, the needs-validation items, and the PRs opened.

Written for Omoikane; the modes come from the Cloudflare security-audit skill (https://github.com/cloudflare/security-audit-skill).
