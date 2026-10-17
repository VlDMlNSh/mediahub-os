# MediaHub OS — A0 Issuer and Jarvis Ingress Decision Proposal, Wave 69

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Ref: `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`
- Status: **DECISION PROPOSAL / NON-NORMATIVE / NOT ACCEPTED / NOT IMPLEMENTED**
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Prior evidence: [Wave 07 A0/MH-12 source trace](MEDIAHUB-A0-LIFECYCLE-MH12-CAPABILITY-ISSUER-SOURCE-TRACE-WAVE-07-2026-10-15.md), [Wave 68 evidence reconciliation](MEDIAHUB-A0-R06-ADMISSION-GATE-EVIDENCE-RECONCILIATION-WAVE-68-2026-10-17.md)
- Purpose: make the next owner/governance decision concrete while preserving the accepted authority boundaries. This document proposes options; it does not select an issuer, grant implementation authority, or accept a wire protocol.

## 1. Decision required

Establish the authoritative issuer and ingress boundary for Jarvis mission submission to ASTRA A0, including the capability lifecycle and its relationship to GitHub-hosted ephemeral workers.

Required accountable decision fields:
- named decision authority and delegation evidence;
- independent security reviewer and privacy/data-governance reviewer;
- chosen issuer principal and trust root;
- caller identity and audience binding;
- capability representation, integrity protection and verifier;
- target repository, ref, commit SHA, workflow/task, permitted operations and data class;
- issue/expiry clock rules, rotation, revocation propagation and stale-token handling;
- replay/idempotency key scope, retention and duplicate response;
- lease generation/fencing, cancellation states/races, retry and recovery behavior;
- result/artifact provenance and publication preconditions;
- audit event, retention, sink outage and reconciliation policy under R-06;
- provider/model destination allowlist, quota/budget and data-egress constraints;
- positive/negative acceptance evidence and rollback/containment behavior.

## 2. Source-bound facts

| Source | Blob SHA | Established | Still open |
|---|---|---|---|
| `docs/checkpoints/MEDIAHUB-A0-LIFECYCLE-MH12-CAPABILITY-ISSUER-SOURCE-TRACE-WAVE-07-2026-10-15.md` | `49ca0b69737bf8d44fe3a42daa47fd9157c9097d` | ASTRA workflow owns internal dependency-aware scheduling, claims, leases, heartbeats, recovery, target-SHA binding and evidence/gate transitions. | No accepted Jarvis-facing ingress endpoint, issuer, capability wire representation, audience, expiry/revocation, replay, fencing or cancellation protocol. |
| `docs/architecture/MH-12-security-architecture.md@main` | `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Identity, authentication, trust, capability, authorization, policy and consumer boundary are distinct stages; State Authority alone mutates canonical state. | Concrete issuer and verifier lifecycle remains unspecified. |
| `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md@main` | `7be5fadd3055642e7823c7233f90e978a87e5366` | ASTRA authority and execution boundaries are defined at reference-architecture level. | Runtime conformance and the external ingress contract remain unproven. |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md@docs/mediahub-chat-tree-map-20261012` | `9ad83781a8da53d1a8f540ede54eba95281f01c0` | A0 coordinates ASTRA-internal engineering workflow and queue/claim/lease/retry/cancellation/evidence-gate state. | This is not an accepted corporation-wide Jarvis ingress API. |
| `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md` | `916df43726fb8f41038d5e9896be7e205284416f` | Draft scopes Jarvis mission submission, GitHub access, provider routing and evidence/lifecycle gates. | Explicitly a design draft, not accepted or implemented. |
| `docs/checkpoints/MEDIAHUB-P0-07-R06-GOVERNANCE-DISPOSITION-TEMPLATE-WAVE-07-2026-10-16.md` | `834fd1ab70eee88355844ba2ebba6c2b6c47ecdb` | Provides the fields for audit/privacy decisions. | Template remains unfilled; accountable authority and reviewers are absent. |
| [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) | Live issue | Sets the ordered acceptance gates and separates design, implementation, test, qualification and dispatch authority. | Current disposition is planning/source evidence only. |

## 3. Options

### Option A — A0-owned capability issuer; GitHub Actions as transport

- Authority: A0 issues or attests a narrowly scoped engineering capability under an accepted contract; GitHub Actions transports and executes only the approved bounded task.
- Advantages: preserves ASTRA's internal workflow authority and keeps the transport separate from authorization; supports ephemeral GitHub-hosted workers and direct outbound HTTPS without an owner-operated always-on server.
- Risks/dependencies: requires an accepted A0 issuer/verification lifecycle and an evidenced way for a GitHub-hosted workflow to obtain and verify that capability. No such complete path is currently evidenced.
- Compatibility: best fit with the existing A0 authority boundary, conditional on an accepted issuer implementation path.

### Option B — GitHub workflow identity as the complete authorization

- Authority: workflow dispatch actor, repository permissions and branch policy alone authorize the task.
- Advantages: low component count and native GitHub transport.
- Risks: GitHub workflow identity alone does not prove task-scoped capability, expiry/revocation, payload binding, lease fencing or result-publication authorization. Workflow inputs are request data, not a complete security capability.
- Compatibility: insufficient as a standalone authorization contract; may serve as one identity signal inside Option A.

### Option C — Jarvis issues capabilities directly to A0

- Authority: Jarvis becomes the issuer for a delegated subset of A0 operations.
- Advantages: aligns with Jarvis mission coordination and may simplify cross-domain requests.
- Risks: introduces cross-domain issuer authority, delegation, revocation, key custody and audit responsibilities. Requires explicit owner/governance delegation and strict separation from canonical product-state mutation.
- Compatibility: viable only with explicit delegation and an independently reviewed trust contract.

### Option D — External identity/authorization service

- Authority: a selected identity service issues or verifies workload identity/capabilities.
- Advantages: mature identity lifecycle may be reusable if it meets the constraints.
- Risks: adds a service/provider dependency, network/data route and availability assumptions; provider-specific OIDC support varies. It can conflict with the no-always-on-server preference if it requires a user-operated service.
- Compatibility: candidate only after exact service, trust flow, provider support, costs and data route are evidenced.

## 4. Recommendation for review

**Prefer Option A as the target authority model, with GitHub Actions as the execution/transport layer, while keeping the implementation blocked until an accepted issuer path is identified.** Treat GitHub actor, workflow permissions, protected refs and immutable task SHA as useful authorization inputs, never as a substitute for the full capability lifecycle. Keep Jarvis as mission submitter/result consumer; keep A0 authority limited to ASTRA-internal workflow state; preserve Product State Authority as the sole canonical product-state mutation authority.

This recommendation is a technical proposal only. The accountable authority must accept the issuer identity, delegation, protocol and risk disposition. If existing stable repository components already implement a compliant issuer, prefer source-pinned reuse over a new service; the current source trace has yet to identify an accepted end-to-end implementation.

## 5. Required fail-closed behavior

Before implementation, the accepted contract must define deterministic behavior for:
- absent, malformed, wrong-audience, expired or revoked capability;
- repository/ref/commit/workflow/task mismatch;
- replayed request, duplicate submission and stale lease/fencing generation;
- cancellation racing with completion or artifact publication;
- issuer/verifier unavailability, audit sink outage and recovery;
- unknown provider/model destination, exhausted quota/budget or disallowed data class;
- conflicting result or missing evidence provenance.

The safe disposition for any unresolved authority or policy condition is BLOCKED/QUARANTINED with a correlated audit record and a recovery path defined by the accepted R-06 policy. Avoid claiming global exactly-once execution; specify bounded idempotency and fencing semantics.

## 6. Separate gates

| Gate | Exit evidence | Current status |
|---|---|---|
| Issuer/ingress decision | Named authority, selected option, delegation and reviewer records | OPEN |
| Protocol contract | Versioned request/response, capability lifecycle and error semantics | OPEN |
| R-06 governance | Filled and accepted audit/privacy disposition | OPEN |
| Runner/workspace/network target | Owner-accepted exact target manifest | OPEN |
| Schema validation | Draft 2020-12 meta-validation, format assertions, positive/negative fixtures, semantic-reference review | OPEN |
| Implementation | Separate authorization, bounded scope, immutable provenance and fail-closed behavior | NOT AUTHORIZED BY THIS PROPOSAL |
| Qualification/dispatch | Separate explicit authorization and recorded run/job/artifact evidence | OPEN |

## 7. Next action

1. Resolve issuer/delegation and R-06 decision authority using the canonical decision register.
2. Inspect source-pinned existing components for an issuer/verifier implementation before any new code.
3. Accept the exact target manifest.
4. Validate the v0.2 schemas with a standards-compliant Draft 2020-12 validator after the relevant action is authorized.
5. Only then prepare the smallest read-only GitHub-hosted worker implementation and request separate authorization for tests and controlled dispatch.

## 8. Disposition

**DECISION PROPOSAL / NOT ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED.** This document adds no runtime behavior and does not authorize credentials, model/provider calls, tests, qualification, workflow dispatch, infrastructure changes, merge or deployment.
