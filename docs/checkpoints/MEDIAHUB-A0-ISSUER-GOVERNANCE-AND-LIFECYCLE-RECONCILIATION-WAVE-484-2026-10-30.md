# Wave 484 — A0 issuer governance and lifecycle reconciliation (2026-10-30)

## Status

**SOURCE RECONCILIATION COMPLETE / OWNER GOVERNANCE DECISIONS STILL OPEN / RUNTIME BLOCKED / NOT QUALIFIED.**

Bounded documentation-only pass. No issuer option, principal, trust anchor, token format, protocol, key store, endpoint, audit retention period or availability policy is selected. No runtime code, tests, credentials, provider calls, workflow dispatch, host tasks, merge, deployment or qualification occurred.

## Immutable source target

- Repository: VlDMlNSh/mediahub-os
- Documentation base SHA: bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4
- Working branch: docs/wave484-a0-governance-reconciliation-20261030
- Source implementation snapshot previously audited: main SHA f0448f28c7cfa61e4450c38529f09afbfdbbc7c7
- Canonical map blob read by SHA: 75f62685459ec99ebf8be478f4e9096cdb842b1d (1,204,915 bytes)
- Canonical checkpoint blob read by SHA: fd312ded05dd1898bd36d776a9669bb02920720d (503,275 bytes)

## 1. Owner decision already established — do not reopen

DEC-DEV-02 Option C is already owner-approved (source blob 70376a2709e055972ceddc4a280d26992977213c):

1. Jarvis coordinates corporation-level missions.
2. ASTRA A0 owns ASTRA-internal queue, claim, lease, heartbeat, retry, cancellation, recovery and ASTRA evidence/gate transitions.
3. MediaHub Product State Authority remains the sole canonical product-state mutation authority.
4. Jarvis must not create a shadow A0 queue or directly mutate A0-owned lifecycle state.
5. No executor, provider, LLM, GitHub adapter or cloud worker gains canonical product-state mutation authority by implication.

This settled lifecycle split is not the unresolved question. WB-05 explicitly states that it does not appoint a security issuer or select trusted-context technology.

## 2. Current governance evidence

### WB-05 — issuer authority decision packet

Source blob: 1b562c6546b1216f2ee89095cd6a78427a967dc5.

Four alternatives remain PROPOSED and UNSELECTED:

- A — separately governed dedicated issuer/attester.
- B — A0-governed issuer restricted to ASTRA-internal workflow capabilities.
- C — separately accepted platform security authority with consumer-boundary verification.
- D — human-authorized issuance for the controlled initial phase, with machine-verifiable provenance.

No option is selected. No technology choice follows automatically from DEC-DEV-02 Option C.

### WB-06 — producer/consumer inventory

Source blob: 9bd850e869dbd19db9bde2ce08768aaf502c95a2.

The in-process AuthorizationContext carries only principal/capability strings and is checked against configured tuple grants. A separate HMAC command-envelope path exists. The inspected evidence does not establish that either is an issuer-backed Jarvis→A0 trusted-context chain. A typed Python object or valid HMAC on a different envelope is not interchangeable proof.

### WB-04 — lifecycle closure matrix

Source blob: dac5e9eab9ec69ab7d15ac8eea45d7a1c8922387.

The 21 lifecycle areas cover identity, issuer, issuance, binding, delegation, expiry, revocation, verifier, replay, propagation, revocation during work, audit, failures, ingress, fencing, compatibility and acceptance. They remain a source-bound gap analysis, not a normative contract or implementation.

### WB-03 — Jarvis→A0 ingress contract gap packet

Source blob: e2f13fe8250fedef02b27bb221072b582db1f3d1.

The ingress, request/response, idempotency, A0 handoff, fencing and result publication contracts remain open/draft. A transport acknowledgement must not be confused with A0 durable acceptance. A0 alone owns its queue and lease lifecycle.

### MH-12 — security architecture

Main-origin blob: cf4ebfd5bf471ca676f075c51d3a24906504e490.

Required semantics: identity, credential, session, capability and authorization are distinct; capabilities bind issuer, subject, audience, operation, resource/target, scope, constraints, provenance, lifetime and revocation context; delegation only attenuates; unknown or unverifiable authority fails closed. Technology remains UNKNOWN pending evidence and ADR.

## 3. GOV-CAP-01…07 — precise unresolved decisions

| Gate | Required owner/governance disposition | Minimum evidence |
|---|---|---|
| GOV-CAP-01 | Accountable capability issuer/attester role and permitted grant scope | Named accountable role, issuance authority and forbidden grants |
| GOV-CAP-02 | Service-principal enrollment, suspension, recovery and re-enrollment owner | Lifecycle owner and authoritative identity-status source |
| GOV-CAP-03 | Mandatory issuer/capability verifier boundaries and responsibilities | Ingress and protected-consumer check points; deny cases |
| GOV-CAP-04 | Trust-anchor custody, rotation and compromise-response owner | Accountable custody/rotation/revocation and incident process |
| GOV-CAP-05 | Expiry/revocation freshness and active-work behavior | Staleness bounds, re-check points, cancellation/containment semantics |
| GOV-CAP-06 | Exact Jarvis→A0 delegation bounds | Operation/resource mapping, audience, attenuation, explicit non-inheritance |
| GOV-CAP-07 | Required ingress acceptance evidence and independent reviewer role | Positive/negative criteria, immutable provenance, separate reviewer/qualification gate |

Owner/governance must explicitly select or reject alternatives and record rationale. No selection is inferred from /next.

## 4. R-06 audit/privacy remains open

Wave 149 matrix blob: 9c1a02dc125b37abea9284f0c0aa5deb571f13e7.

Unresolved R-06 decisions include canonical security-flow and principal/delegation-scope mapping; minimum audit fields, correlation, access controls and retention ownership; privacy classification and retention limits for principal, task, target/resource, decision and provenance data; whether audit unavailability blocks each protected operation; recording expiry, revocation, replay rejection, denial and recovery events without logging credentials, tokens, private keys or session material; and independent review/evidence integrity requirements.

No retention period, sink, access role or fail-open exception is selected.

## 5. Cross-contract invariants for the next normative proposal

Keep distinct:
- Jarvis mission identity and mission coordination;
- ASTRA A0 workflow identity and authoritative queue/claim/lease/cancel/recovery state;
- security issuer/attester identity and grant authority;
- consumer-boundary verifier and policy decision;
- MediaHub Product State Authority and canonical mutation.

The future contract must bind authorization to immutable request/task identity, exact operation and resource, audience, target revision where relevant, policy/provenance, expiry and revocation state. It must define durable replay/idempotency receipts, atomic duplicate handling, lease generation/fencing, cancellation races, recovery after crash, stale-worker rejection, result publication and audit behavior. These are required semantic dimensions, not selected wire fields or implementation choices.

## 6. Wave 482 source finding remains a hard admission block

Wave 482 source audit was authored against main SHA f0448f28c7cfa61e4450c38529f09afbfdbbc7c7; PR #594 head 923f0e38bc0d8bae3828c15af14a2dc7fe7c9803.

Finding A0-ISSUER-01 (HIGH, source-level): FileTaskIngress accepts caller-supplied approval_state=approved and passes it into AstraTaskRequest; AstraGatewayRuntime uses that value to permit classified sensitive actions. The inspected path did not establish issuer signature, authenticated principal/capability, operation/resource binding, expiry, revocation or durable replay verification.

This is an authority/provenance gap, not a confirmed exploitable vulnerability; inbox writer/attacker reachability was not established. Runtime remediation remains blocked pending accepted governance and independent review.

## 7. Admission decision

- Issuer-backed Jarvis→A0 ingress: BLOCKED.
- Runtime change to approval path: BLOCKED.
- Gemini controller dispatch / child agents: NOT RUN.
- Claude local executor: NOT RUN; latest Wave 482 record reports zero connected SentinelX hosts, enrolled Mac mini offline, two dev hosts disabled.
- Provider calls, credentials, tests and infrastructure changes: NOT RUN.
- Cloud worker admission: BLOCKED by issuer/ingress/lifecycle, R-06 and runner-target gates.
- Contour A: NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED.
- Contour B: GATED.

## 8. Next bounded step

Obtain explicit GOV-CAP-01…07 and R-06 owner/governance dispositions against existing WB-05 alternatives and WB-04 lifecycle matrix. Then prepare one versioned, technology-neutral normative contract proposal and negative-test matrix, with independent A3 review before runtime changes. Do not re-ask the already approved DEC-DEV-02 Option C lifecycle split.

## References

- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Wave 149 governance matrix](MEDIAHUB-A0-ISSUER-GOVERNANCE-DECISION-GATE-MATRIX-WAVE-149-2026-10-18.md)
- [Wave 482 source audit](MEDIAHUB-A0-INGRESS-ISSUER-SOURCE-AUDIT-WAVE-482-2026-10-30.md)
- [Wave 483 cloud-pool priority](MEDIAHUB-CLOUD-POOL-FIRST-PRIORITY-WAVE-483-2026-10-30.md)
- [Canonical map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
