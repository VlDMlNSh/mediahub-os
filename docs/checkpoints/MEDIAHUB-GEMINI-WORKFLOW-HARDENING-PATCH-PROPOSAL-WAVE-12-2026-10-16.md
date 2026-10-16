# MediaHub OS — Gemini Read-only Workflow Hardening Patch Proposal, Wave 12

- Date: 2026-10-16
- ID: MH-GWF-PATCH-12
- Status: **SOURCE-BOUND PATCH PROPOSAL / NOT APPLIED / NOT TESTED / NOT QUALIFIED**
- Contour: A — Developer Fabric
- Parent: [Gemini workflow source review, Wave 09](MEDIAHUB-GEMINI-WORKFLOW-SOURCE-QUALIFICATION-PLAN-WAVE-09-2026-10-16.md)
- Operational evidence: [Wave 10](MEDIAHUB-CLOUD-AGENT-FABRIC-GEMINI-OPERATIONAL-EVIDENCE-WAVE-10-2026-10-16.md)
- Task contract: [Wave 11](MEDIAHUB-CLOUD-AGENT-FABRIC-QUEUE-AND-TASK-CONTRACT-WAVE-11-2026-10-16.md)
- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Exact source revisions reviewed

| Source | Ref | Blob SHA | Role |
|---|---|---|---|
| `.github/workflows/gemini-readonly-audit.yml` | `main` | `0d10efdda251f2ceca43175981c919102303572b` | Read-only audit, no retry |
| `.github/workflows/gemini-readonly-audit-retry.yml` | `main` | `96fcc9ed4e45659d0118f0b9f3593a0c736200f0` | Read-only audit with bounded retry and caller-supplied model ID |

Source read-back confirmed these exact blobs during Wave 12. The proposed changes below are scoped to these files; no file was changed by this review.

## 2. Patch goals

Preserve the existing successful read-only Gemini path while adding deterministic source provenance, narrow input scope, stable model selection, action supply-chain controls and untrusted-output quarantine. Keep both workflows read-only. The patch must preserve current secret names and API call behavior unless an independently reviewed compatibility change is proposed.

## 3. Proposed change set

### P0 — immutable source provenance

Apply to both workflows:
1. Resolve `context_ref` to a single commit SHA before checkout; check out the resolved SHA, not the mutable input ref.
2. Record requested ref and resolved SHA in the step summary and machine-readable manifest.
3. Record selected paths in normalized order and SHA-256 each file after validation.
4. Fail closed if the ref cannot be resolved, the resolved commit differs from the checked-out commit, or the manifest is incomplete.
5. Add a task/run identity and an evidence-manifest schema version.

Acceptance: manifest source SHA equals the actual checkout; every selected file digest matches the bytes sent in the prompt; moving refs cannot change the inputs after resolution.

### P0 — bounded input and strict allowlists

Apply to both workflows:
1. Replace arbitrary comma-separated paths with a normalized, bounded list. Enforce a maximum path count, aggregate bytes, individual bytes, task length and model-output bytes.
2. Use a task-specific path allowlist or a small reviewed manifest of allowed paths. Reject duplicate paths and paths outside the allowlist.
3. Resolve each candidate path and verify it remains inside the repository workspace; reject symlinks and non-regular files for context.
4. Normalize and validate ref names, reject option-like values and disallow ref expressions outside the explicitly accepted ref policy.
5. Preserve the current workflow-directory exclusion and expand exclusions to secret-bearing configuration and credential stores.

Acceptance: traversal, symlink escape, duplicate path, disallowed file, oversized aggregate context and malformed ref cases all fail before the provider step.

### P0 — model and provider policy

Retry workflow:
1. Replace free-form `inputs.model` with a reviewed allowlist bound to the provider policy revision.
2. Bind the selected model and task data class to an explicit authorization record in the task envelope.
3. Fail before the provider request when the model is unknown or authorization evidence is missing.
4. Keep fallback disabled unless each alternate destination has its own authorization, eligibility evidence, data-policy revision and quota bucket.

Acceptance: caller-supplied unknown model IDs fail before network access; quota events cannot add destinations.

### P1 — action supply chain and runtime provenance

1. Replace `actions/checkout@v4` and `actions/upload-artifact@v4` with verified full commit SHA pins.
2. Verify each pin against the canonical upstream repository and record the resolved action revision in the evidence manifest.
3. Record runner OS/image metadata and Node runtime version.
4. Keep `contents: read`, `persist-credentials: false`, job timeout and artifact retention bounds. Any permission increase requires a separate reviewed change.

Acceptance: all third-party actions are pinned to verified full SHAs; effective permissions remain read-only; manifest records exact action and runner identities.

### P1 — output quarantine and provenance

1. Write provider output only to a bounded artifact file with restrictive file permissions.
2. Calculate an output digest and include it in the manifest with run/job IDs, workflow source SHA, context digests, model ID, policy revision, timestamps, status and retry count.
3. Mark all model output as untrusted advisory data.
4. Avoid appending raw model-generated Markdown directly to the GitHub step summary. The summary should show a short fixed notice and manifest/artifact references; reviewers may open the quarantined artifact separately.
5. Upload the manifest alongside the report. Keep retention explicit and consistent with the approved privacy policy.

Acceptance: the artifact and manifest are digest-linked; model output cannot create misleading privileged workflow instructions or become a promotion decision by itself.

### P1 — consistent error and retry behavior

1. Retain bounded retry for explicitly retryable statuses only.
2. Bound error text, sanitize diagnostic metadata and suppress raw response bodies.
3. Add an explicit total request deadline and cancellation behavior.
4. Record retry attempt count, final HTTP class, request ID when available and terminal disposition without logging the API key.
5. Keep authentication/authorization failures non-retryable unless provider policy explicitly states otherwise.

Acceptance: transient, permanent, malformed-response, timeout and cancellation cases have deterministic terminal statuses and safe logs.

### P2 — remove implementation drift

After P0/P1 review, factor shared prompt-building, input validation and manifest code into a reviewed local action or script. Keep the no-retry and bounded-retry behavior as explicit policy inputs to one implementation rather than allowing prompt/security logic to drift between two workflows.

Acceptance: parity review shows identical source/path/model/output security controls in both entry points; retry behavior differs only by the documented retry policy.

## 4. Proposed evidence manifest fields

- schema version;
- repository, requested ref and resolved commit SHA;
- workflow path/blob SHA, run ID, attempt, job ID;
- normalized task ID and task digest;
- selected input paths and per-file digests;
- provider/model identity and policy revision;
- action full SHAs, runner image and runtime metadata;
- start/end timestamps, timeout and retry count;
- result status, sanitized error class and provider request ID if available;
- output path, byte count, SHA-256 digest and retention class;
- reviewer disposition and next-gate reference.

Exclude credentials, raw API keys, authentication headers, unrestricted provider error payloads and unnecessary personal data.

## 5. Execution and promotion gates

1. Patch proposal review against the exact source SHAs.
2. Explicit authorization to edit workflow source on a designated working branch.
3. Static schema/YAML/workflow validation and targeted negative-path tests.
4. Independent security review of effective permissions, action pins, path policy, provider route and evidence manifest.
5. A separately authorized read-only workflow dispatch after policy and eligibility gates are satisfied.
6. Artifact/run provenance review and comparison with the historical successful run.
7. Independent qualification decision before any worker is admitted beyond read-only advisory scope.

A successful workflow run proves only that execution. It does not close source-hardening findings or authorize write-capable work.

## 6. Public source basis

- GitHub Actions secure-use guidance recommends least privilege, action-source review and full-length SHA pins; it also distinguishes the isolation properties of hosted ephemeral runners from self-hosted environments: https://docs.github.com/en/actions/reference/security/secure-use
- GitHub documents its cloud agent as an asynchronous task path that can produce branches and pull requests, subject to plan and repository configuration: https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/kick-off-a-task
- GitHub's responsible-use overview describes the different permission and execution characteristics of cloud agents and other agentic features: https://docs.github.com/en/copilot/responsible-use/agents

## 7. Disposition

This is an exact-source remediation proposal, not a patch. The existing Gemini workflow remains operationally proven for one historical read-only run. The workflow sources retain actionable gaps in immutable provenance, input allowlists, model authorization, action pinning, output quarantine and manifest completeness.

No workflow was edited or dispatched. No provider call, credential access, test suite, scanner, host/runtime inspection, infrastructure change, qualification, deployment or branch integration occurred in this wave.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
