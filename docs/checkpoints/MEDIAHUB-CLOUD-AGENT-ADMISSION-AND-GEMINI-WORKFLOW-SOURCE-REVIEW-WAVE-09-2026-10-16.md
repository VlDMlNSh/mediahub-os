# MediaHub OS — Cloud-Agent Admission and Gemini Workflow Source Review, Wave 09

- Date: 2026-10-16
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **BOUNDED SOURCE REVIEW / PROPOSED CONTROLS / RUNTIME-UNVERIFIED**
- Scope: close one documentation-only pass from Wave 08 across A0 issuer/lifecycle evidence, P0-07 R-06 governance authority, Gemini read-only workflow source, and target-profile evidence.
- Authority: accepted Functional Baseline 2.0 on `main` remains the functional authority. This report is subordinate to accepted domain contracts and owner/governance decisions.
- This report does not authorize workflow edits, dispatch, provider calls, credentials, tests, qualification, infrastructure work, deployment, branch integration, or production promotion.

## 1. Live source anchors

| Source | Ref | Blob SHA | Bounded authority / observation |
|---|---|---|---|
| A0 lifecycle and MH-12 capability issuer source trace, Wave 07 | docs branch | `49ca0b69737bf8d44fe3a42daa47fd9157c9097d` | Internal ASTRA lifecycle rules are documented; accepted Jarvis→A0 ingress/API, issuer lifecycle, and complete external replay/fencing/cancellation contract remain open. |
| MH-12 security architecture | `main` | `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Defines layered identity/authentication/trust/capability/authorization/policy/boundary semantics; does not instantiate a concrete A0 issuer. |
| ASTRA executor capability matrix | docs branch | `9ad83781a8da53d1a8f540ede54eba95281f01c0` | ASTRA-internal queue/claim/lease/heartbeat/recovery authority; not a Jarvis-facing ingress API. |
| P0-07 R-06 governance disposition template, Wave 07 | docs branch | `834fd1ab70eee88355844ba2ebba6c2b6c47ecdb` | Template remains unfilled; accountable decision authority and approval workflow are still open. |
| Gemini read-only architecture audit workflow | `main` | `0d10efdda251f2ceca43175981c919102303572b` | Static workflow-source review only. |
| Gemini read-only architecture audit retry workflow | `main` | `96fcc9ed4e45659d0118f0b9f3593a0c736200f0` | Static workflow-source review only. |
| Unified System Traceability Matrix v0.1 | docs branch | `5c9727991960f655b7b2fd6389a6ff2ce1d3f9a2` | Existing cross-domain integration register; status remains PROPOSED / NOT ACCEPTED / NOT FROZEN. |
| Canonical Source Registry and Security Evidence Ledger, Wave 03 | docs branch | `a752c0a8de254fd5a1a0211eb14643d6c5e939de` | Existing authority/evidence index through SRC-035 and EVD-017 before this pass. |

Blob SHA identifies file content. Branch HEAD and blob identity remain distinct.

## 2. A0 issuer/lifecycle disposition

The reviewed primary sources support internal ASTRA queue, claim, lease, heartbeat, recovery, bounded-admission and evidence/gate concepts. They do not establish a complete accepted external Jarvis→A0 contract.

Open interface obligations:
1. Accepted API base/path, transport, protocol version, and caller identity.
2. Trusted issuer/attester/verifier, audience, signature/key lifecycle, expiry, rotation and revocation propagation.
3. Mapping from mission/task operation to A0 capability and resource scope.
4. Immutable source/target binding, idempotency-key scope, deduplication retention and duplicate-response semantics.
5. Lease fencing/generation, cancellation races, stale claims and recovery behavior.
6. Accepted result/status contract and revision-bound evidence handoff.

The shared `AuthorizationContext(principal, capability)` shape and grant matching do not prove trusted issuance, freshness, audience, revocation or resource/revision binding. Do not promise global exactly-once execution. Preserve P0-07 as proposal-only and P0-04 as sole canonical product-state mutation authority.

**Disposition:** CAF-01 and CAF-03 remain OPEN / BLOCKED on accepted issuer and external lifecycle contract plus independent end-to-end evidence.

## 3. R-06 audit/privacy authority

The live Wave 07 template is explicitly `TEMPLATE / PROPOSED / UNFILLED / NO ACCEPTANCE IMPLIED`. Its decision authority, date, related decision IDs and per-operation dispositions remain blank. The template itself grants no authority and registers no schema.

Closure requires:
- an authoritative named decision-maker or formally delegated body, with delegation evidence;
- operation-specific event lifecycle for read, validate, propose, update, replace, reset and delete;
- audit-sink durability and outage semantics;
- minimized event schema, integrity and correlation/time provenance;
- reader access, retention/deletion, reconciliation and recovery requirements;
- linked canonical decision-register entry and independent review.

**Disposition:** R-06 remains OPEN. CAF-09 is BLOCKED. The next technical step is source reconciliation and a decision-ready evidence packet; an unfilled template cannot be promoted to a decision.

## 4. Gemini workflow source review

### Positive source-level controls

- Both workflows are manual `workflow_dispatch` only in the reviewed source.
- Workflow/job permissions are `contents: read`; no write permission is declared.
- Checkout uses `persist-credentials: false`.
- Jobs run on GitHub-hosted `ubuntu-latest` with bounded job timeouts.
- Context is assembled from explicitly supplied paths, with absolute-path, parent-path-substring, newline, workflow-directory and 200 KB checks.
- The prompt explicitly treats repository content as untrusted evidence and forbids unsupported implementation/qualification claims.
- API error bodies are suppressed in the primary workflow; the retry workflow redacts common key/bearer/query-key patterns from selected diagnostics and limits retries to four attempts for a fixed retryable status set.
- The API key is passed via an environment variable and the workflow states it is excluded from the artifact.
- `GITHUB_STEP_SUMMARY` and artifacts are used for results; artifact retention is 14 days.

### Source-level gaps and risks

1. **Mutable ref input:** `context_ref` accepts a user-provided branch/tag/ref and is passed directly to checkout. The workflow does not resolve and verify an immutable approved commit SHA before reading context or making the provider request.
2. **Context path scope:** paths are checked for common unsafe forms and workflow files are excluded, but there is no positive path allowlist or approved path-set manifest. A dispatch actor can select other repository text files available at the chosen ref.
3. **Third-party action pinning:** checkout and artifact upload use major-version tags (`actions/checkout@v4`, `actions/upload-artifact@v4`) rather than full commit SHAs.
4. **Provider secret alias:** both `GEMINI_API_KEY` and `GOOGLE_API_KEY` are accepted as fallback names. The source does not evidence secret metadata, key validity, account eligibility, quota, region, or current provider policy for this repository.
5. **Provider data boundary:** the full selected context plus the dispatch task is sent to the external Gemini API. The source does not enforce a task-level data-class allowlist, a maximum aggregate context size, or an approved immutable route/policy record.
6. **Output handling:** generated findings are appended to the workflow summary (up to 45,000 characters) and uploaded as an artifact for 14 days. Source-level controls do not establish content classification, redaction review, reviewer access policy, or deletion evidence.
7. **Retry workflow:** the four-attempt ceiling is bounded, but retry behavior and API diagnostics have not been executed or independently verified. This review makes no runtime or cost claim.
8. **Model identity:** the primary workflow has a source-defined default model; the retry workflow permits a dispatch-supplied model ID. A model allowlist and revision-bound route approval are not evidenced in these files.
9. **Workflow source immutability:** action SHA pinning, approved default-branch/source fence, task/actor capability binding, and immutable evidence binding remain required before activation.

These are static source observations and control recommendations, not evidence of exploitability or a runtime incident.

### Recommended source-qualified remediation order

- **P0:** resolve an approved ref to a commit SHA and verify the selected source revision; constrain context paths to a positive allowlist; bind actor, task, data class, provider/model, policy revision and output destination into a reviewable run envelope.
- **P0:** establish task-level data-egress authorization and a maximum aggregate context budget before any provider call.
- **P1:** pin third-party actions to verified full SHAs; define an approved model allowlist; establish artifact/summary classification, redaction, reader, retention and deletion rules.
- **P1:** retain the existing read-only token permissions and `persist-credentials: false`; do not add write capabilities to the advisory worker.
- **Separate gate:** workflow edits, dispatch, provider invocation, credential inspection, test execution and qualification require their respective explicit authorization and evidence.

**Disposition:** CAF-06 remains REQUIRED / SOURCE QUALIFICATION OPEN; CAF-07 remains PROPOSED / DESIGN ONLY; CAF-08 remains GOVERNANCE EVIDENCE OPEN. The Gemini worker is a candidate advisory workflow, not an admitted autonomous developer.

## 5. Exact target manifest

The bounded source set reviewed in this pass provides no owner-accepted, exact target-role manifest covering hardware, firmware, OS/toolchain, network/egress, storage/persistence, trust zones, worker isolation and recovery. The current matrix still records target hardware/OS/network/storage/topology as UNKNOWN. Historical hostnames and legacy machine references remain provenance only, not deployment targets.

Required evidence is an owner-accepted versioned target manifest with source/provenance, role assignment, compatibility/support lifecycle, resource limits, trust boundaries, egress rules, persistence/recovery profile and qualification scope. Until then, hosted-runner isolation, target compatibility and deployment readiness remain UNKNOWN/BLOCKED.

## 6. Integrated disposition

| Work item | Current state | Closure evidence |
|---|---|---|
| CAF-01 admission/revocation | OPEN / BLOCKED | Accepted issuer and revocation lifecycle, versioned registry/schema, independent review |
| CAF-02 immutable task envelope | PROPOSED / DESIGN ONLY | Versioned schema, immutable source/target binding, path/data-class/capability/budget fields, collision check |
| CAF-03 A0 queue/lease lifecycle | BLOCKED / A0 CONTRACT OPEN | Accepted external interface and issuer contract; replay, cancellation, fencing and recovery semantics; independent E2E evidence |
| CAF-04 hosted worker isolation | BLOCKED / TARGET UNKNOWN | Accepted target manifest and source-qualified runner profile |
| CAF-05 provider route/quota | BLOCKED / ELIGIBILITY UNKNOWN | Authorized provider/account eligibility and task-level route/data policy |
| CAF-06 workflow supply chain | REQUIRED / SOURCE QUALIFICATION OPEN | Immutable ref, positive context allowlist, full-SHA action pins, per-job authority map and approved source changes |
| CAF-07 evidence provenance | PROPOSED / DESIGN ONLY | Validated evidence manifest bound to task, source SHA, workflow run/job, policy, provider/model, output digest and reviewer |
| CAF-08 promotion/review | GOVERNANCE EVIDENCE OPEN | Current branch-protection/ruleset evidence and authorized promotion contract |
| CAF-09 audit/privacy | BLOCKED / R-06 OPEN | Accountable decision, accepted event/sink/outage/retention policy and independent disposition |
| CAF-10 capacity/retry | PROPOSED / INPUTS UNKNOWN | Authorized workload and quota inputs, bounded retry/circuit-breaker policy and evidence |
| CAF-12 Contour sequence | BLOCKED / GATE PRESERVED | Contour A deployment record and independent acceptance before Contour B admission |

## 7. Work performed and limits

- Read-only source/document review across the exact paths and blob SHAs listed above.
- No source, workflow, schema or runtime files were changed in this pass.
- No tests/scanners, workflow dispatch, provider/model calls, credential/secret access, host/runtime inspection, infrastructure changes, deployment, merge, rebase or cherry-pick occurred.
- No agent was registered, connected, dispatched or admitted by this report.
- No deployment-readiness, security qualification, or production-acceptance claim is made.

## 8. Next bounded pass

1. Continue the existing A0/MH-12 trace with any newly discoverable accepted issuer/ingress governance evidence; keep the interface open if none exists.
2. Reconcile R-06 against the canonical decision register and exact MH-12/MH-13 authority sources; preserve OPEN until accountable disposition is evidenced.
3. Prepare a separate, source-pinned Gemini workflow patch proposal with minimal changes and rollback; apply or execute only after the relevant authorization.
4. Continue searching the existing target/deployment evidence registers for an owner-accepted target manifest; retain UNKNOWN if none is located.
5. Update the existing Unified System Traceability Matrix and Canonical Source Registry; do not create another master inventory.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
