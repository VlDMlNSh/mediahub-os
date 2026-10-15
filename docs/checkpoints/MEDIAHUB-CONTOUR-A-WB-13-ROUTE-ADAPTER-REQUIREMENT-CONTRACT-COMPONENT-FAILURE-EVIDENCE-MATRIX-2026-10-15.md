# MediaHub OS — Contour A WB-13: Route-Adapter Requirement / Contract / Component / Failure / Evidence Matrix

- Date: 2026-10-15
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **SOURCE-BOUND DESIGN MATRIX / PARTIAL / PROPOSED / NOT ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED**
- Scope: bounded documentary pass for the proposed Jarvis route-adapter seam. Preserve Option A (ASTRA A0-governed route) as the current source-aligned reference; keep direct Alamo routing optional and unaccepted.
- No normative contract is amended by this document. No runtime, host, credential, provider, test, installation, deployment or infrastructure action was performed.

## 1. Live source and branch state

- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Main HEAD observed: `608d7463011798ca75e36bfce4b749a9caf4f9a0`
- Compare `main...`docs/mediahub-chat-tree-map-20261012`: **DIVERGED**, documentation branch ahead 1410 / behind 3; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No integration attempted.
- WB-11 source trace: blob `b34b50dc749cade5b32e6ed369fe5b430d1a788e`.
- WB-12 options matrix: blob `87ce2d51c81d3e5c8dfe2517f61878d91a0e069a`.
- ASTRA/Jarvis D-03 reconciliation: blob `a21bd84a16086e82bc623e3c711ef010a13ac7db`.
- Component crosswalk: blob `d6b2a09f5281b7c843f85f3b50264259af16548f`.
- Latest lifecycle/authority trace: blob `dc60ccc0af29a74ca3cf88584d66821350b20b9f`.

These blob SHAs identify the reviewed documentation-branch files, not the underlying main-branch sources. WB-11 contains the individual main-source pins for its bounded trace.

## 2. Authority boundary

- **Jarvis:** corporation-level mission coordination, request formulation, and route request/mission-result tracking within an accepted contract.
- **ASTRA A0:** sole owner of ASTRA-internal queue, claim/lease, heartbeat, retry/cancellation, recovery, and ASTRA evidence/gate transitions under the accepted scope.
- **Alamo execution domain:** candidate only; no accepted host identity, queue lifecycle owner, local/cloud execution mode, media backend, or end-to-end ingress is established.
- **Route adapter:** proposed non-authoritative seam. It must not own either execution domain's queue lifecycle, issue capabilities, bypass sensitive-action approval, promote qualification, or mutate canonical MediaHub product state.
- **MediaHub Product State Authority:** sole canonical product-state mutation authority in Contour B.

## 3. Requirement-to-contract-to-component matrix

| ID | Requirement / invariant | Existing source / contract evidence | Candidate component seam | Failure control required | Verification evidence required | Current status |
|---|---|---|---|---|---|---|
| WB13-R01 | Stable mission identity across routing and result | WB-12 §5 requires common mission identity; corporation-wide task/result envelope remains draft-only per Wave 05 | Jarvis mission envelope + adapter correlation metadata | Reject missing/duplicate identity; idempotent replay semantics must be explicit | Schema review; duplicate/replay cases; correlated audit records | OPEN |
| WB13-R02 | Route decision is policy-bounded and auditable | WB-12 §5/§6; owner TD-07 unresolved | Jarvis route request + separately governed policy decision point | Deny unknown route; no implicit route switch or fallback | Decision table, policy version, allow/deny evidence, route audit | PROPOSED / OWNER DECISION |
| WB13-R03 | ASTRA queue lifecycle stays exclusively with A0 | D-03 reconciliation R-01; canonical executor policy source-pinned in WB-11 | Existing ASTRA A0 ingress/queue contract | Adapter must not claim, lease, retry, cancel, or recover ASTRA jobs independently | Authority/sequence review and negative tests at future authorized stage | SOURCE-ALIGNED DESIGN; RUNTIME UNVERIFIED |
| WB13-R04 | Any Alamo queue has exactly one named lifecycle owner | WB-11/WB-12: Alamo absent from inspected permanent executor pool; WB-10 direct route has no accepted end-to-end contract | Alamo adapter to a separately named local queue, if owner selects it | No dispatch until owner, durable state, claim/lease/fencing and recovery contract exist | Owner decision; interface contract; lifecycle/recovery evidence | BLOCKED |
| WB13-R05 | Caller identity and authorization are independently verifiable | Wave 05 A-01/A-02: ingress and capability issuer/lifecycle OPEN | Authenticated Jarvis principal + accepted ingress verifier | Fail closed on absent/expired/revoked/mismatched identity or capability | AuthN/AuthZ sequence, issuer contract, revocation and denial evidence | BLOCKED |
| WB13-R06 | Sensitive approval is bound to task/action/resource | WB-12 §5; WB-09 direction says a task-supplied approval boolean is not proof | Approval attestation verifier, not the adapter itself | Reject untrusted approval fields and mismatched scope/audience/expiry | Attestation schema and provenance; tamper/expiry/replay evidence | BLOCKED |
| WB13-R07 | “Claude local” vs external provider is explicit | WB-11 source trace distinguishes external Anthropic API-key path from Ollama-backed Claude-compatible endpoint; neither is proven deployed on Alamo | Executor/provider adapter with explicit provider/runtime identity | Block local-only requests when provider/egress is unknown; no silent cloud fallback | Pinned endpoint/runtime/model/provider, data-flow and egress evidence | UNKNOWN / BLOCKING |
| WB13-R08 | Heavy media work has a real backend and resource envelope | WB-11/WB-12: video-generation backend and exact Alamo host unknown | Media executor adapter only after backend admission | Reject unsupported task/resource class; quotas, timeout, cancellation and backpressure | Host profile, backend identity/version/license, capacity and workload qualification | BLOCKED |
| WB13-R09 | Results are normalized without inventing evidence | WB-12 §5 requires task/route/executor/provider/input revision/artifact digests; qualification remains independent | Shared result/evidence envelope; domain-specific result adapters | Reject unbound artifacts, missing digests, executor self-qualification and partial results treated as success | Schema, provenance chain, artifact-integrity and negative-case evidence | DRAFT CONTRACT NEEDED |
| WB13-R10 | Failure/retry/cancellation semantics remain domain-owned | Wave 05 notes replay/recovery semantics open; WB-12 requires one owner per execution domain | Adapter passes cancellation/deadline intent; domain queue executes lifecycle | No competing retry loops; distinguish accepted, running, cancelled, failed, unknown | State-transition table, timeout/cancel/restart/replay evidence | OPEN |
| WB13-R11 | Adapter cannot become a second State Authority | Bootstrap invariants; D-03 split; WB-12 §5 | Stateless or minimally stateful routing seam with bounded audit metadata | Deny canonical mutation and authority escalation; fail closed on unknown policy | Capability review, dependency graph, negative authorization evidence | REQUIRED INVARIANT |
| WB13-R12 | Contour A readiness gates remain separate from product acceptance | Master roadmap §§0, 3; generated current truth on main reports G0–G11 BLOCKED | Existing evidence and qualification governance | No deployment/acceptance claim from design documents or workflow presence | Independent qualification and owner acceptance artifacts | BLOCKED / NOT PROVEN |

## 4. Component disposition

1. **Reuse as source-aligned references, not as proof of runtime readiness:** Jarvis coordination contract, ASTRA A0 queue lifecycle, existing executor/provider-routing seams, and existing result/evidence schemas where their actual scope matches.
2. **Do not add a new workflow engine, broker, database, or model runtime in this pass.** Canonical Component Manifest 2.0 requires an evidenced gap before adding future-gated alternatives.
3. **Do not treat the existing Anthropic worker or Ollama-backed Claude-compatible workflow as Alamo deployment evidence.** The local client, inference runtime, provider identity, model, host, and media backend are separate facts.
4. **New design artifacts needed before implementation:** versioned route request/decision contract; common mission/result/audit envelope; domain ownership and state-transition table; provider/egress policy binding; resource admission contract; evidence-promotion contract.
5. No source indicates a complete accepted Jarvis → adapter → ASTRA/Alamo end-to-end contract today.

## 5. Failure-control acceptance checklist

Before implementation authorization, the owner/governance process must settle:
- topology TD-01; exact Alamo host TD-02; Claude execution/provider mode TD-03; video backend TD-04;
- local queue lifecycle owner TD-05; eligible task classes TD-06; route/failover authority TD-07;
- Jarvis→A0 ingress, capability issuer/delegation/revocation, approval provenance, canonical command envelope, and task/result schema;
- idempotency, claim/lease/fencing, cancellation, retry ownership, crash recovery and artifact provenance;
- hardware/software compatibility and local/cloud data-flow profile.

Future verification must be independently authorized and evidenced. This matrix itself is not a test plan approval and authorizes no test, qualification, installation, host inspection, provider invocation, deployment, migration or merge.

## 6. Decision and next bounded step

**Recommendation (not accepted decision):** continue designing a narrow route-adapter contract, while preserving ASTRA A0 as the only currently source-aligned governed autonomous execution route. Keep Alamo direct execution optional and fail-closed until host identity, provider/runtime mode, media backend, queue owner, ingress, approval and evidence contracts are accepted.

Next bounded step: WB-14, read-only source reconciliation of the exact Jarvis→A0 ingress and direct-local-executor candidate contracts against WB13-R01…R12; produce a discrepancy/decision packet without changing normative sources. If a required contract is absent, record the gap rather than inventing an endpoint or claiming an implementation.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
