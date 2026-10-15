# MediaHub OS — Contour A WB-05 Issuer Authority and Trusted-Context Ownership Decision Packet

- Date: 2026-10-15
- Status: **DECISION PACKET / OPTIONS NOT SELECTED / NON-NORMATIVE / NOT IMPLEMENTED**
- Purpose: identify owner/governance decisions required before defining a capability issuer and trusted-context lifecycle for Jarvis↔ASTRA A0.
- Governing decision: DEC-DEV-02 Option C, owner-decision record blob `70376a2709e055972ceddc4a280d26992977213c`.
- Project ref: `docs/mediahub-chat-tree-map-20261012`.

## 1. Decision summary

The owner-approved lifecycle split remains in force: Jarvis coordinates corporation-level missions; ASTRA A0 owns ASTRA-internal engineering workflow state; MediaHub Product State Authority alone owns canonical product-state mutation. This packet does not amend that decision.

A separate decision is still needed for the authority that issues or attests capabilities, the party that verifies them at protected boundaries, and who owns identity enrollment, revocation and trust-anchor governance. MH-12 provides semantic constraints but does not select an issuer product, protocol, token format or key store.

**No option below is selected.** The options are governance alternatives for owner review, not claims about existing implementation.

## 2. Current source evidence

| Source | Ref / blob SHA | Evidence | Limit |
|---|---|---|---|
| `docs/architecture/MH-12-security-architecture.md` | main / `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Identity → authentication → trust → capability → authorization → policy → consumer boundary → State Authority; capability is issuer/principal/operation/resource/scope/constraints/provenance/lifetime/revocation-bound; no self-grant; fail-closed. | Architecture complete / governance review required; issuer technology is unknown pending evidence and ADR. |
| `runtime/mediahub_runtime/authorization.py` | main / `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | `AuthorizationContext` contains two string fields (`principal`, `capability`); allow-list checks exact (principal, capability, operation) tuples; empty policy denies. | No issuer, audience, expiry, provenance or revocation proof in this type/policy seam. |
| `runtime/mediahub_runtime/consumer_boundary.py` | main / `98bf2da9cea85da2c82145b4baef417c20b9ae73` | `OperationRequest` carries the typed context; request factory checks the type; boundary calls the authority and sanitizes errors. | The inspected path does not establish that the context was issued or independently verified. This is not a full-repository producer/consumer inventory. |
| `runtime/mediahub_runtime/in_memory_state.py` | main / `0fbc71369d19e09944ba67a60ccb9df802f30a4b` | State Authority checks context type and uses configured authorization policy. | Does not establish issuer provenance or external ingress wiring; source-level observation only. |
| `docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-04-CAPABILITY-ISSUER-TRUSTED-CONTEXT-LIFECYCLE-MATRIX-2026-10-15.md` | docs branch / `dac5e9eab9ec69ab7d15ac8eea45d7a1c8922387` | 21 lifecycle closure areas and required questions. | Non-normative, not accepted, not implemented. |
| `docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-03-JARVIS-A0-INGRESS-CONTRACT-GAP-PACKET-2026-10-15.md` | docs branch / `e2f13fe8250fedef02b27bb221072b582db1f3d1` | Caller identity, issuer/verifier, schema, replay, handoff, fencing and audit are separate open contract surfaces. | No accepted endpoint, protocol or capability format. |
| `docs/checkpoints/MEDIAHUB-CHAT-TO-GITHUB-OWNER-DECISIONS-AND-CORPORATION-DIRECTION-WAVE-01-2026-10-15.md` | docs branch / `70376a2709e055972ceddc4a280d26992977213c` | Owner approved DEC-DEV-02 Option C and separate corporate/A0/Product State Authority responsibilities. | Does not choose issuer or verifier ownership/technology. |

## 3. Decisions required from owner/governance

| ID | Decision required | Why it matters | Acceptance evidence |
|---|---|---|---|
| GOV-CAP-01 | Who owns authority to issue/attest capabilities? | Prevents callers or workloads from self-granting privileges; establishes accountable grant authority. | Explicit owner/governance record naming role and scope, not merely a product name. |
| GOV-CAP-02 | Who owns service-principal enrollment and lifecycle? | Enrollment, suspension, recovery and identity revocation must have an accountable owner. | Accepted lifecycle ownership and status-source contract. |
| GOV-CAP-03 | Which boundary verifies issuer provenance and capability constraints? | Every protected ingress/consumer path must validate context rather than trust caller-supplied fields. | Accepted verifier responsibility and mandatory check points. |
| GOV-CAP-04 | Who owns trust anchors, issuer rotation and compromise response? | Establishes how issuer authenticity is bootstrapped and how compromise is contained. | Accepted governance/operational ownership and rotation/revocation requirements. |
| GOV-CAP-05 | How are revocation and expiry observed by active work? | Defines safe handling when a grant expires or is revoked during a long-running task. | Accepted propagation/freshness semantics and re-check points. |
| GOV-CAP-06 | What authority may Jarvis delegate to A0 or other executors? | Avoids implicit privilege inheritance or delegation that expands scope. | Accepted operation/resource mapping and attenuation constraints. |
| GOV-CAP-07 | What evidence is mandatory before an ingress contract can be accepted? | Keeps design, implementation, verification and acceptance statuses distinct. | Explicit evidence/negative-verification criteria and independent acceptance role. |

## 4. Governance alternatives — not selected

### Option A — Dedicated issuer authority, logically separate from Jarvis and A0

- **Shape:** a separately governed issuer/attester role issues bounded capabilities; ingress/consumer verifiers validate them; Jarvis remains mission coordinator and A0 remains engineering-workflow authority.
- **Benefits:** strong separation of duties; easier to reason about issuer compromise and prevent callers from issuing their own grants.
- **Costs/risks:** additional component and lifecycle to govern; issuer availability, trust-anchor distribution and revocation propagation become explicit dependencies.
- **Requires:** issuer principal, issuance authority, key custody/rotation, verifier contract and failure policy.
- **Not implied:** a particular issuer service, vendor, protocol, token format or deployment topology.

### Option B — A0-governed issuer for ASTRA-internal workflow capabilities

- **Shape:** capability issuance is constrained to ASTRA-internal operations and governed by the ASTRA workflow/security boundary; corporation-wide mission authority remains outside A0.
- **Benefits:** aligns issuance with the subsystem whose internal queue/claim/lease lifecycle is being protected; may limit authority scope.
- **Costs/risks:** can blur A0 workflow ownership with security issuer authority; must not allow A0 capabilities to imply corporate or canonical product-state privileges; external Jarvis ingress still requires authentication and independent validation.
- **Requires:** explicit proof that issuer authority is within A0's accepted scope, plus separation of issuer/verifier responsibilities and narrow resource/operation constraints.
- **Not implied:** that A0 currently has such an issuer or that an existing queue/controller can safely be repurposed.

### Option C — Existing platform security authority owns issuance; A0 and other boundaries verify

- **Shape:** a separately accepted MediaHub security authority governs identities, grants and revocation; each protected consumer boundary enforces the result. Jarvis and A0 remain callers/workflow owners, not self-issuing authorities.
- **Benefits:** consistent lifecycle policy across local and external executors; clearer central governance for revocation and audit.
- **Costs/risks:** introduces a cross-domain dependency and requires careful availability, offline behavior and trust-boundary design.
- **Requires:** evidence that the security authority exists or an approved design for it, its scope, and how boundaries verify current grants.
- **Not implied:** that MH-12 itself specifies an implemented service.

### Option D — Human-authorized issuance only for the initial controlled phase

- **Shape:** each grant is explicitly approved by a human-controlled governance path; automation consumes but does not mint or broaden grants.
- **Benefits:** simple accountability and conservative initial trust.
- **Costs/risks:** operational bottleneck; does not by itself define machine-readable provenance, verification, expiry, revocation or safe delegation.
- **Requires:** explicit approval record format, binding of approval to subject/operation/resource/constraints, and automated verification at consumers.
- **Not implied:** that human approval alone makes a caller-supplied context trustworthy.

## 5. Comparative view

| Criterion | A: Dedicated issuer | B: A0-governed internal issuer | C: Platform security authority | D: Human-authorized issuance |
|---|---|---|---|---|
| Separation of duties | High if issuer independent | Medium; requires strict A0 scope | High if governance and consumers are separate | High for grant approval, but consumer enforcement still required |
| Fit for corporation-wide identities | Potentially high | Low-to-medium; A0 scope is internal | Potentially high | Low scalability |
| Fit for ASTRA-only capabilities | High | Potentially high | High | Possible but operationally costly |
| Revocation consistency | Must be designed | Must be designed within A0 scope | Must be designed across consumers | Approval revocation still needs propagation |
| New dependency/complexity | Dedicated issuer lifecycle | Risk of conflating workflow/security duties | Shared authority dependency | Human operations and audit overhead |
| Current status | PROPOSED | PROPOSED | PROPOSED | PROPOSED |

No numerical score is assigned because target topology, threat model, offline requirements, issuer availability objectives and deployment evidence have not yet been accepted.

## 6. Recommended decision method (not an architecture selection)

Before choosing an option, the owner/governance process should confirm:

1. The trust boundaries and threat model for local, remote and cloud executors.
2. Whether issuer availability is required for every operation or whether verifiable bounded offline grants are permitted.
3. The authority responsible for identity enrollment, revocation and incident containment.
4. Whether issuer and verifier duties must be separate principals/components.
5. Required revocation latency and behavior during network or authority outages.
6. The operations/resources that Jarvis may request and A0 may execute, including explicit non-inheritance of privileges.
7. Required audit retention, secret handling and independent acceptance evidence.

**Process recommendation:** decide authority ownership and invariants first; select a concrete technology only after source evidence, threat analysis and an ADR. This recommendation does not choose A, B, C or D.

## 7. Non-negotiable invariants across all options

- No self-granting capability; no implicit privilege inheritance from human to service or from Jarvis to A0.
- Principal, credential, session, capability, authorization and policy decision remain distinct.
- Capabilities must be bound to issuer, subject, audience, operation, resource/target, scope, constraints, provenance, lifetime and revocation context.
- Delegation may narrow authority, never expand it.
- Unknown, malformed, expired, revoked or unverifiable context fails closed.
- A0 owns its internal workflow state; Jarvis must not create a competing A0 queue.
- MediaHub Product State Authority remains the sole canonical product-state mutation authority.
- External executor/controller remains one bounded executor boundary; its internal controller state does not become MediaHub authority.
- Design, implementation, tests, verification, qualification, deployment and acceptance remain distinct states.

## 8. Branch and verification boundary

At the start of this pass:
- `main` HEAD: `608d7463011798ca75e36bfce4b749a9caf4f9a0`
- documentation branch: `docs/mediahub-chat-tree-map-20261012`
- comparison: `DIVERGED`, 1377 ahead / 3 behind
- merge base: `f0f406feb9f9816b009f4e6e756813541e53b9bc`

Only GitHub source reads and documentation writes were performed. No tests, installations, credentials, provider/model calls, host/runtime inspection, security scan, qualification, infrastructure changes, deployment, merge, rebase or cherry-pick occurred. No normative contract was changed. This packet is not an owner decision; all options remain unselected.

## 9. Next bounded step

After owner/governance selects or rejects the ownership options, perform a bounded source-level producer/consumer inventory for `AuthorizationContext` and capability values, including constructors, trust-boundary entry points and call paths. Use direct file evidence; search misses alone do not prove absence. Keep Jarvis→A0 ingress blocked until issuer, verifier, audience, replay and propagation semantics are accepted.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
