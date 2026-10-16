# MediaHub OS — Gemini Workflow Hardening Packet, Wave 33

- Date: 2026-10-17
- ID: MH-GEMINI-WRITE-AUTOMATION-HARDENING-33
- Contour: A — Developer Fabric
- Status: SOURCE-BOUND CHANGE DESIGN / NOT APPLIED / NO DISPATCH
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- MediaHub main HEAD reviewed: `149f5af85962a7a1219a4012e1f4b0b8b335a0a3`
- Workflow blob: `b81e9cf829d1272fe7ea0db8ce8e4b48adcc272a`
- Prior source review: [Wave 32](MEDIAHUB-GEMINI-AUTONOMOUS-WORKFLOW-SOURCE-REVIEW-WAVE-32-2026-10-17.md), blob `293643a745aece9dd5e2d02d32143f9c802558fe`

## 1. Purpose and boundaries

Turn Wave 32 findings into a minimal, source-bound hardening plan for the write-capable Gemini workflow. This pass reads public upstream GitHub source and MediaHub documentation, then records exact candidate pins and unresolved evidence. It does not edit executable workflows, dispatch jobs, call a model/provider, read secrets, test, qualify, inspect a host/runtime, change infrastructure, deploy or integrate branches.

## 2. Source-backed upstream findings

| Component | Current MediaHub declaration | Upstream identity observed | Assessment |
|---|---|---|---|
| Google Gemini Action | `google-github-actions/run-gemini-cli@v0` | Tag `v0` resolves to commit `f77273f4c914e4bf38440cf36a0369cb64a37489`; GitHub API reports commit signature verified | Candidate immutable ref: `google-github-actions/run-gemini-cli@f77273f4c914e4bf38440cf36a0369cb64a37489`. Review action code and trust guidance at that exact commit before adoption. |
| Checkout | `actions/checkout@v4` | Tag `v4` resolves to commit `11d5960a326750d5838078e36cf38b85af677262`; GitHub API reports commit signature verified | Candidate immutable ref: `actions/checkout@11d5960a326750d5838078e36cf38b85af677262`. |
| GitHub MCP server | `ghcr.io/github/github-mcp-server:v0.27.0` | Tag `v0.27.0` resolves to source commit `2b352ab0b914cde8c16d44200a7cace9f400be71`; annotated tag object reports signature verification `unsigned` | Source commit alone is not an OCI image digest. Registry digest and build provenance remain UNKNOWN; do not claim the container is pinned until the digest is independently obtained and verified. |
| Gemini CLI | Action input omitted; action metadata default is `latest` | Official upstream latest release at source review: `v0.64.0`; asset `gemini-cli-bundle.zip` reports SHA-256 `9d4ad33d15dcf35098919c69eb9d98b6dc640567f141d6fc4f8f053c8cbd8dae` | Workflow currently inherits mutable latest. Candidate version is `v0.64.0`, subject to independent release provenance review and a compatibility record. Asset digest is not evidence that the action installed that asset during any run. |
| Gemini CLI trust | `GEMINI_CLI_TRUST_WORKSPACE: 'true'` | Upstream `docs/cli/trusted-folders.md` at tree `ed96faedfd5571f055c44f2c9509d62321d1138d` says this variable bypasses the trust check and trusts the workspace for the session | Confirmed trust bypass, not merely an ambiguous trust setting. The project configuration/MCP dependency means removal needs a controlled configuration design; do not remove blindly without preserving the required explicit MCP setup. |

### Primary upstream references

- Action tag ref: https://api.github.com/repos/google-github-actions/run-gemini-cli/git/ref/tags/v0
- Verified action commit: https://github.com/google-github-actions/run-gemini-cli/commit/f77273f4c914e4bf38440cf36a0369cb64a37489
- Checkout tag ref: https://api.github.com/repos/actions/checkout/git/ref/tags/v4
- Verified checkout commit: https://github.com/actions/checkout/commit/11d5960a326750d5838078e36cf38b85af677262
- MCP tag metadata: https://api.github.com/repos/github/github-mcp-server/git/tags/b50870084e1120ced9b5cd4c6aa177e8916f97da
- Gemini CLI trusted-folders source: https://github.com/google-gemini/gemini-cli/blob/ed96faedfd5571f055c44f2c9509d62321d1138d/docs/cli/trusted-folders.md
- Gemini CLI sandbox source: https://github.com/google-gemini/gemini-cli/blob/ed96faedfd5571f055c44f2c9509d62321d1138d/docs/cli/sandbox.md
- Action metadata: https://github.com/google-github-actions/run-gemini-cli/blob/f77273f4c914e4bf38440cf36a0369cb64a37489/action.yml
- Gemini CLI release: https://github.com/google-gemini/gemini-cli/releases/tag/v0.64.0

## 3. Minimal change packet

### GHW-33-01 — Immutable action refs

Replace mutable action tags only after the candidate SHAs above have been reviewed against their source and accepted in the change record. Preserve the source refs, verified-signature status and update procedure. A future update is a new reviewed change, not a floating ref.

### GHW-33-02 — MCP image identity

Resolve the registry manifest digest for the intended platform and confirm that it maps to the reviewed source release. Pin `ghcr.io/github/github-mcp-server@sha256:<verified-digest>`; record source commit, image digest, platform and provenance. The placeholder is intentionally unresolved; no digest is inferred from the source commit.

### GHW-33-03 — Gemini CLI version

Set the action's `gemini_cli_version` input to an exact reviewed release rather than its `latest` default. `v0.64.0` is a candidate from the upstream release API, not yet an accepted production pin. Verify release signature/provenance, asset integrity, runtime compatibility and the action's installation behavior before adoption.

### GHW-33-04 — Workspace trust and configuration provenance

The upstream documentation explicitly states that `GEMINI_CLI_TRUST_WORKSPACE=true` bypasses the workspace trust check for the session. The workflow's MCP configuration is injected through the action's `settings` input, while project-local configuration may also exist in the checked-out tree.

Before editing:
1. Identify precisely how the pinned action writes/merges settings and starts Gemini CLI.
2. Ensure project-controlled settings, hooks, commands and extensions cannot silently add tools or alter policy.
3. Prefer a controlled settings file and explicit MCP allowlist whose provenance is outside the model-edited workspace.
4. If trust bypass remains necessary for headless operation, record the exact accepted rationale and enforce configuration isolation; the prompt alone is insufficient.
5. Keep the runtime sandbox and network policy explicit. Upstream sandbox documentation describes filesystem/network behavior as dependent on the selected sandbox profile, so no sandbox guarantee should be inferred from workspace trust.

### GHW-33-05 — Enforced write boundary

The model prompt requests one branch and one PR, but the job's GitHub token has `contents: write` and `pull-requests: write`. MCP exposes branch/file/PR creation tools. Enforce the following outside prompt text:
- dedicated branch namespace and approved base commit SHA;
- allowed-path manifest and protected-path denylist covering canonical contracts, governance decisions, workflow policy, secrets, and target/acceptance records unless the task explicitly carries authority;
- reject path traversal, symlink escape, oversized patches and out-of-scope file changes;
- cap changed files and diff bytes; reject generated binaries and credential-like content;
- validate final diff and task-to-path traceability before PR creation;
- never grant merge, deployment, secret administration or workflow modification tools to this agent tier by default.

Where GitHub permissions cannot enforce path-level restrictions, use a separate validator or trusted broker outside the model-controlled process. Repository branch protection and required review remain independent controls.

### GHW-33-06 — Task and model policy

- Validate task length, schema, acceptance criteria and referenced IDs before model invocation.
- Pin the model to an accepted exact model ID; do not allow an unreviewed repository variable to select arbitrary models.
- Bind task ID, issuer/authority reference, model ID, data classification, budget and policy revision into the run record.
- Preserve the rule that task text, issue text and repository content are untrusted data.
- Keep additional provider calls, credential changes, tests, qualification, host/runtime inspection and infrastructure operations outside this workflow's grant.

### GHW-33-07 — Evidence manifest

Create a versioned, sanitized manifest with at least:
- workflow run ID and attempt;
- workflow file blob SHA and action commit SHAs;
- base branch plus resolved base commit SHA;
- Gemini CLI version and model ID;
- MCP source commit, image digest and platform;
- task identifier and authority/policy references;
- changed path list, diff digest, diff size, validator version/result;
- PR URL/number and review state, when available;
- artifact digests, retention classification and evidence-generation timestamp.

Do not include API keys, tokens, authorization headers, environment dumps, unredacted URLs, prompts containing secrets, or provider response bodies. Agent output is untrusted until independently checked.

## 4. Admission gates

| Gate | Evidence required | Current state |
|---|---|---|
| Immutable Actions | Reviewed commit pins and update record | Candidate SHAs identified; workflow unchanged |
| MCP supply chain | Verified OCI digest and provenance | BLOCKED / UNKNOWN |
| CLI reproducibility | Exact accepted version plus verified provenance | Candidate `v0.64.0`; acceptance pending |
| Workspace configuration | Pinned action semantics and controlled config source | Source confirms trust bypass; remediation design pending |
| Write boundary | Enforced validator/broker plus repository policy evidence | BLOCKED |
| Task/model authority | Accepted task grant and model allowlist | BLOCKED |
| Target manifest | Owner-accepted exact target and immutable base | UNKNOWN / BLOCKED per Wave 10 |
| A0 / MH-12 / R-06 | Accepted issuer, secret lifecycle, governance and audit dispositions | OPEN per existing source records |
| Independent verification | Authorized static checks and subsequent separately authorized qualification | NOT PERFORMED |

## 5. Recommended execution sequence

1. Preserve this packet as the change specification; do not dispatch the current workflow.
2. Resolve MCP OCI digest and provenance using public registry/release evidence; if unavailable, keep that gate open.
3. Review the exact action source and CLI release behavior, then draft a minimal workflow diff on an isolated branch only under separately granted write/change authority.
4. Add deterministic validation outside the model-controlled tool loop and a schema-validated evidence manifest.
5. Compare the diff against accepted A0/MH-12/R-06 and target-manifest sources.
6. Request independent review; perform any tests, qualification, dispatch or runtime verification only under their separate explicit authority.
7. Keep merge, deployment and Contour B admission outside this workflow.

## 6. Status

**Design packet recorded; no implementation or runtime admission.** Exact upstream candidate refs are source-backed, but the MCP image digest/provenance, target manifest, task authority and governance dispositions remain open. No owner decision is needed to continue documentary source reconciliation.

No workflow dispatch, model/provider call, credential access, tests, qualification, host/runtime inspection, installation, infrastructure change, deployment or branch integration occurred.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
