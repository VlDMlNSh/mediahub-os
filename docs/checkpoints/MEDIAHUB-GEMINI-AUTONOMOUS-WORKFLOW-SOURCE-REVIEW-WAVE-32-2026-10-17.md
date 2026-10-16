# MediaHub OS — Gemini Autonomous Engineering Workflow Source Review, Wave 32

- Date: 2026-10-17
- ID: MH-GEMINI-AUTONOMOUS-DISPATCH-SOURCE-REVIEW-32
- Contour: A — Developer Fabric
- Status: STATIC SOURCE REVIEW / DESIGN GAPS RECORDED / NO DISPATCH / NO QUALIFICATION
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Reviewed main HEAD: `149f5af85962a7a1219a4012e1f4b0b8b335a0a3`
- Workflow blob: `b81e9cf829d1272fe7ea0db8ce8e4b48adcc272a`
- Agent rules blob: `4c431143aa5c46776e80893bf3c0e5f202e3b76d`
- Prior source review: [Wave 09](MEDIAHUB-GEMINI-WORKFLOW-SOURCE-QUALIFICATION-PLAN-WAVE-09-2026-10-16.md), blob `accbe4d3725ac308378b73ed78d9ecf10dc8b19e`
- Prior hardening proposal: [Wave 12](MEDIAHUB-GEMINI-WORKFLOW-HARDENING-PATCH-PROPOSAL-WAVE-12-2026-10-16.md), blob `11106dcbb26c2a54643c8727732ef56c63510c7f`

## 1. Scope and authority

Read-only source inspection of the new `.github/workflows/gemini-autonomous-engineering.yml`, `GEMINI.md`, the commit diff, the canonical bootstrap instruction, Master Roadmap, latest checkpoint, prior Gemini source reviews, target-manifest reconciliation and R-06 governance template.

No workflow was dispatched. No model/provider was invoked. No credentials or secret values were read. No tests, qualification, host/runtime inspection, installation, infrastructure change, deployment, merge, rebase or cherry-pick occurred.

## 2. Workflow behavior observed

The new workflow is manually triggered by `workflow_dispatch`, with a required task string and constrained `base_ref=main` and `scope=contour-a` choices. It checks out the selected base with `persist-credentials: false`, invokes `google-github-actions/run-gemini-cli@v0`, injects `secrets.GEMINI_API_KEY`, and configures a GitHub MCP server at `ghcr.io/github/github-mcp-server:v0.27.0`.

The allowed MCP tool list includes branch creation, repository file writes, PR creation, code search, commit/PR listing and issue read/search. Core Gemini tools are configured as an empty list. The prompt directs one bounded pass, a dedicated branch and PR, no merge/deploy, evidence-bound claims, and no tests/qualification or host/infrastructure operations.

The job-level permissions are `contents: write`, `pull-requests: write`, and `issues: read`; workflow-level permissions default to `contents: read`. The job uses `ubuntu-latest`, a 30-minute timeout, `actions/checkout@v4`, and action reference `google-github-actions/run-gemini-cli@v0`. The GitHub MCP container is specified by a version tag, rather than an immutable image digest.

These are static YAML observations, not proof of actual effective token scopes, action behavior, provider access, workflow execution or successful PR creation.

## 3. Positive controls

1. Manual dispatch only; no schedule or issue/comment trigger is declared in this workflow.
2. The base branch input is constrained to `main`; the contour input is constrained to `contour-a`.
3. The prompt explicitly disallows merge and deployment, calls repository/task content untrusted, and requires source-linked evidence.
4. The workflow declares a bounded 30-minute job and a bounded MCP tool list.
5. Checkout disables persisted Git credentials.
6. `GEMINI.md` preserves Baseline 2.0 authority, historical ID continuity, Product State Authority boundary and separation of design, implementation, testing, verification, qualification, release, deployment and acceptance.

## 4. Security and contract gaps

### GWF-32-01 — mutable third-party action references

The workflow uses `google-github-actions/run-gemini-cli@v0` and `actions/checkout@v4`. Version tags are not immutable content identities. The source does not provide verified full commit SHA pins or a reviewed action-update process.

**Required closure:** verify upstream action commits and provenance, pin full SHAs, and document the controlled update path. Do not infer safety from the organization name or action title.

### GWF-32-02 — mutable MCP image tag

The MCP container uses `ghcr.io/github/github-mcp-server:v0.27.0`. The YAML does not bind the image to a digest or record resolved image provenance in a run evidence manifest.

**Required closure:** pin an approved digest and record it in run evidence; review image updates separately.

### GWF-32-03 — write-capable repository token in model-directed tool loop

The job grants content and PR write permissions and passes `github.token` to the GitHub MCP server. The MCP allowlist includes file writes, branch creation and PR creation. This is consistent with the stated PR-preparation goal but is a privileged write capability controlled through model-directed tool calls.

The prompt is a behavioral guard, not a hard security boundary. It cannot by itself enforce path-level policy, protected-file exclusions, canonical-contract checks, branch-name constraints, or proof that every write is limited to the declared task.

**Required closure:** restrict permissions and write targets as narrowly as the platform supports; enforce a reviewed path allowlist and protected-path denylist outside the prompt; require immutable base SHA and bounded change manifest; ensure branch/PR-only behavior through tool and repository policy; keep merge and deployment capabilities absent. Confirm effective permissions with a static permission review and separately authorized verification.

### GWF-32-04 — trusted workspace mode

The workflow sets `GEMINI_CLI_TRUST_WORKSPACE: 'true'`. The checked-out repository is project-controlled input, but repository files may include agent configuration and prompt-like content. The prompt says to treat repository content as untrusted, while workspace trust enables a broader trust posture in the CLI.

**Required closure:** establish the exact CLI semantics for this setting from the pinned upstream implementation; default to untrusted workspace unless a documented requirement demonstrates necessity. If trust remains enabled, constrain hooks, extensions, MCP configuration, filesystem and execution capabilities through enforceable policy. Static review did not verify the CLI's runtime behavior.

### GWF-32-05 — task input and repository prompt-injection boundary

The required task is interpolated into the final prompt, and repository files/issues are retrieved as agent context. Instructions to ignore embedded instructions are useful but cannot establish isolation against all prompt injection.

**Required closure:** validate task length/schema; represent task data separately from policy instructions where supported; apply source trust labels; prevent repository content from changing tool policy; limit context to task-specific paths and byte budgets; require a deterministic post-generation diff/contract review before PR creation.

### GWF-32-06 — provenance and evidence manifest

The workflow requests artifact upload and local telemetry, but the reviewed YAML does not define a MediaHub evidence manifest binding run ID, workflow commit SHA, base commit SHA, action SHAs, MCP image digest, model ID, policy revision, changed paths, diff digest, PR URL and review outcome.

**Required closure:** emit a versioned, sanitized manifest; record requested and resolved base refs; hash the final diff and evidence; label Gemini output as untrusted advisory data. Never include secret values, full environment dumps, or unredacted credential-bearing URLs.

### GWF-32-07 — target and authority remain unresolved

The latest target-manifest reconciliation (Wave 10, blob `1f748bf80e08067fd85a7e1b0821cc4d12bda676`) found no owner-accepted exact clean deployment target. The A0/MH-12 trace (Wave 07, blob `49ca0b69737bf8d44fe3a42daa47fd9157c9097d`) leaves the trusted issuer lifecycle, exact ingress interface, revocation and replay semantics open. The R-06 disposition template (Wave 07, blob `834fd1ab70eee88355844ba2ebba6c2b6c47ecdb`) remains unfilled and does not imply acceptance.

**Required closure:** keep autonomous code-changing workflow admission limited to a documented Contour A change packet with accepted task authority, exact base target, data/secret policy and audit requirements. No target or governance acceptance is inferred from workflow presence.

### GWF-32-08 — model policy and provider authorization

The model is selected through `vars.GEMINI_MODEL` with a default value. The workflow does not itself bind model selection to a MediaHub provider-eligibility record, data classification, budget, or an accepted task grant. The task prompt limits additional provider calls, but that remains a prompt-level rule.

**Required closure:** use an owner-approved model allowlist and explicit provider/task policy. Do not dispatch until model/provider invocation is separately authorized and the secret/configuration prerequisites have been reviewed.

### GWF-32-09 — runner and artifact boundary

The workflow uses `ubuntu-latest` and requests action artifact upload. The source does not define a controlled runner image, explicit artifact retention in the workflow input, artifact sensitivity classification, or independent evidence validation.

**Required closure:** document runner provenance, artifact contents/retention/access, output-size limits and redaction; verify what the official action uploads and whether telemetry can contain sensitive context. Avoid treating local telemetry as a durable audit record.

## 5. Relation to prior Gemini hardening work

Wave 09 and Wave 12 concern the existing read-only audit workflows. Their proposals include immutable source provenance, action SHA pins, bounded task/context input, model allowlists, output quarantine and evidence manifests. Those proposals were explicitly NOT APPLIED and NOT TESTED in the reviewed records.

The new write-capable workflow is a separate trust tier. It must not inherit a read-only workflow's review status, and its added repository write authority requires a separate security admission record. No prior proposal is treated as implemented by this report.

## 6. Recommended disposition

**SOURCE REVIEW COMPLETE FOR THE THREE NEW FILES / RUNTIME ADMISSION BLOCKED / NO DISPATCH.**

Do not launch the workflow in this pass. First prepare a source-bound hardening packet that:
1. Pins the Google action, checkout action and MCP image to verified immutable identities.
2. Removes or justifies trusted-workspace mode using pinned CLI source.
3. Reduces and enforces repository write scope outside prompt instructions.
4. Binds run, base SHA, model, changed paths, diff digest and PR to a sanitized evidence manifest.
5. Defines task/path limits, protected-path rules and deterministic pre-PR checks.
6. Reconciles the task's model call and credential use with the project's explicit authority rules.
7. Keeps R-06 governance and target-manifest status visibly open until accepted evidence exists.

No owner decision is needed to document these technical closure criteria. Actual dispatch, model invocation, tests, qualification, or repository settings changes remain separately gated by the project authority rules.

## 7. Verification boundary

Evidence is limited to read-only GitHub source retrieval at `main@149f5af85962a7a1219a4012e1f4b0b8b335a0a3`, the workflow blob SHA above, `GEMINI.md`, and current documentation-branch source reads. No action runtime, effective token permissions, secret values, provider calls, artifacts, runner state or actual workflow outcome was inspected.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
