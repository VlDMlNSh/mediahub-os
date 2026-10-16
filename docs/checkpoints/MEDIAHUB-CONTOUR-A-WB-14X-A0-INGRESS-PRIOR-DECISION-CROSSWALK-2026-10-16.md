# WB-14X — ASTRA A0 ingress prior-decision crosswalk

- Date: 2026-10-16
- Status: SOURCE CROSSWALK COMPLETE / INGRESS CONTRACT GAPS OPEN / NOT IMPLEMENTED OR TESTED
- Scope: distinguish accepted prior authority decisions from missing A0 ingress-specific contracts.
- Boundary: documentation-only. No owner decision inferred; no normative schema, code or runtime changed.

## Findings

The following accepted directions constrain ingress design and should not be reopened without change control:

1. **DEC-DEV-02 Option C** establishes the authority split: Jarvis owns corporation-level mission coordination; ASTRA A0 owns ASTRA-internal queue/claim/lease/retry/cancellation/evidence-gate state; Product State Authority alone mutates canonical product state. This does not define the wire protocol, issuer, authentication profile or caller edge.
2. **MH-12** requires explicit identity-bound, operation-specific, auditable, fail-closed authorization. Principal, credential, session, capability and authorization are distinct. It does not name a concrete issuer or technology.
3. **MH-06 ADR-001** is ACCEPTED / GOVERNANCE ACCEPTED for MH-06 Core Runtime Services semantics. This does not authorize implementation or deployment and does not automatically reconcile the generic domain-health schema.
4. **Owner-register D-03 is not D-ING-03.** D-03 is marked owner-accepted for its own recorded scope; it does not decide A0 ingress durable admission/idempotency.

## Residual gaps

| Item | Existing constraint | Still missing | Status |
|---|---|---|---|
| D-ING-01 issuer/principal | MH-12 identity and delegation boundaries; DEC-DEV-02 authority split | Accepted issuer/attester, verifier, enrollment, audience and revocation lifecycle | OPEN |
| D-ING-02 authentication/integrity | Explicit, fail-closed authorization | Accepted threat model/profile, payload binding, key lifecycle and replay behavior | OPEN |
| D-ING-03 admission/idempotency | A0 owns internal workflow state | Durable commit point, key/digest, duplicate/uncertain-commit and acknowledgement semantics | OPEN |
| D-ING-04 freshness | Capability lifetime/revocation are required concepts | Per-contract expiry/replay rules and trusted-time failure semantics | OPEN |
| D-ING-05a health mapping | MH-06 accepted within its scope | Owner-approved cross-scope mapping or explicit separation from generic domain health | OPEN |
| D-ING-05b probe | Probe outcome must not be conflated with health/readiness/trust | Correlation, responder identity, freshness and failure contract | OPEN |
| D-ING-06 lifecycle | Authority split already decided | Exact Jarvis-facing states, transitions, cancellation/fencing/late-result semantics | OPEN |

Wave 07's source trace reports that the inspected authorization context contains principal/capability but does not establish issuer, audience, expiry, revocation or request/resource/payload/revision binding. The inspected consumer boundary does not establish a P0-07 caller/adapter edge. These are source-level findings, not runtime claims.

A P0-05 candidate has a DRAFT-labelled contract-status discrepancy against separate implementation-acceptance evidence. The existing source trace marks the P0-07 → P0-05 accepted caller edge NOT ESTABLISHED and the exact contract-status disposition OPEN / OWNER-GOVERNANCE REQUIRED. Do not change the protected header or infer acceptance.

## Source pins

- Project map (docs ref): `f258a2fcdc4cda3d9d9e633fb1f6490baac77253`.
- Master roadmap (docs ref): `89b82eb263eb99c813ef2767886125b3d8bd9421`.
- WB-14W: `c5920437c02d98b3f4bec6a356b590a7bef9ce4e`.
- WB-14T corrected packet: `023f44b6712450a8b84e2e99e716fd3cbb2d593e`.
- Owner decision register: `1a0f4592e7335db4bca5e74ce37783e672851caf`.
- Wave 07 source trace: `49ca0b69737bf8d44fe3a42daa47fd9157c9097d`.
- MH-06 ADR-001 from main: `7dda05379bd70007dc18acd62ed14fc83f0c9226`.
- MH-12 architecture: `cf4ebfd5bf471ca676f075c51d3a24906504e490`.

## Next bounded step

Inspect the exact DEC-DEV-02 primary record and P0-05/P0-07 contract sources on their owning refs. Produce a minimal evidence request only for unresolved issuer/caller/contract-status items. Do not repeat broad owner-approval analysis or reopen the accepted authority split.

No tests, validators, code edits, credentials/provider calls, host/runtime inspection, installs, infrastructure changes, deployment, migration or branch integration occurred.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).

## WB-14Y boundary correction — engineering ingress vs canonical product mutation (2026-10-16)

This addendum supersedes only the inference in WB-14X that could place the P0-07 → P0-05 caller gap and P0-05 contract-status issue as direct acceptance gates for all Jarvis → ASTRA A0 engineering ingress. They are distinct routes:

- Jarvis → A0 is bounded engineering-mission ingress and ASTRA-internal lifecycle. The owner-approved DEC-DEV-02 Option C is already recorded in [the owner decision packet](MEDIAHUB-OWNER-DECISION-PACKET-01.md), §8. Its API/issuer/verification/idempotency/cancel/status/result contract is still not established.
- P0-07 → P0-05 → P0-04 concerns canonical product-state mutation. Its caller edge remains NOT ESTABLISHED and the P0-05 DRAFT-header disposition remains at the owner-directed defer/governance-evidence gate. These issues block relevant product mutation, not automatically every engineering task submission.

MH-12 security principles can inform both trust boundaries, but neither path may assume the other's issuer, audience, context or protocol. A0 must never bypass P0-05/P0-04 or acquire canonical product-state authority. See WB-14Y for the source-pinned correction and separate evidence matrix.
