# Wave 486 — Owner-directed A0 issuer governance disposition and recommended contract

- Date: 2026-10-30
- Source target: Wave 485 head `37254c9f4ff09c39943f6924534a63dd44b5a431`
- Status: **OWNER-DIRECTED TARGET DECISIONS SELECTED / NORMATIVE ACCEPTANCE PENDING / RUNTIME BLOCKED**
- Authority: owner instruction in this conversation (2026-10-30) delegates selection of the most appropriate answers based on prior MediaHub discussions; Bootstrap §8 already directs autonomous technical decision-making.
- Purpose: close the decision-selection gap left by Wave 484 without inventing real-world people, deployed services, credentials, keys, or implementation evidence.

## 1. Decision summary

Select **WB-05 Option A: a separately governed, dedicated security issuer/attester**, logically and operationally separate from Jarvis, ASTRA A0, executors, provider adapters and MediaHub Product State Authority.

This is the safest fit for the established three-authority split and the multi-pool target. Option C assumes an existing platform security authority whose implementation was not evidenced in the inspected sources. Option B conflates A0 workflow ownership with grant issuance. Option D is useful as a human approval control but is not a scalable issuer architecture by itself.

The issuer is an accountable security role/service boundary, not a named person or a claim that a deployed issuer already exists. A concrete product, protocol, token format, key store, endpoint or principal name remains subject to source research and a separate ADR.

## 2. Fixed authority boundaries (preserve DEC-DEV-02 Option C)

1. Jarvis coordinates corporation-level missions and submits bounded requests; it does not own or shadow A0's internal queue and does not mint its own grants.
2. The dedicated Security Issuer Authority owns capability issuance, issuer identity, service-principal admission, grant policy and revocation governance.
3. ASTRA A0 verifies incoming authority and owns its internal queue, claim, lease, heartbeat, retry, cancellation, recovery and ASTRA evidence/gate transitions.
4. Every protected consumer verifies the authority evidence it relies on. A0 verification is not a transferable approval for downstream consumers.
5. MediaHub Product State Authority remains the sole authority for canonical product-state mutation and must independently enforce its own boundary.
6. Executors, LLMs, GitHub Actions, cloud workers, provider adapters and transport acknowledgements acquire no authority by implication.

## 3. Selected dispositions

| Gate | Selected target disposition | Required controls |
|---|---|---|
| GOV-CAP-01 — issuer/attester | Dedicated Security Issuer Authority, separate from Jarvis and A0; issue only policy-approved, bounded capabilities. Human governance approves issuer policy and exceptional grants; workloads cannot self-issue. | Separation of duties; no self-grant; explicit issuer identity, grant scope and exclusions; issuance/revocation audit. |
| GOV-CAP-02 — service principals | Security Issuer Authority governs enrollment, suspension, recovery and re-enrollment. Enrollment requires verified workload identity, owner/purpose, environment, allowed audiences and bounded scope. | Default deny; distinct principals per workload/environment; dual approval for privileged enrollment/recovery; immediate suspension on compromise; re-enrollment creates a new identity generation. |
| GOV-CAP-03 — verification | Verify at Jarvis ingress, A0 ingress, and every protected consumer before the protected effect. Use one reviewed verifier implementation/library where practical, but each consumer makes its own decision against its own audience and policy. | Validate issuer, subject, audience, operation, resource/target, scope, constraints, provenance, lifetime, revocation and delegation; reject caller-supplied approval flags and unverified typed objects. |
| GOV-CAP-04 — trust anchors | Custody belongs to a Security Trust Custodian role separate from issuer operators, A0 operators and application developers. Prefer a managed KMS/HSM-backed root with dual control; keep private signing material non-exportable where supported. | Quorum/dual control for root operations; versioned key IDs; overlap rotation; emergency revoke; tested recovery; no private keys in GitHub repository, prompts, logs or artifacts. Vendor/product selection remains a separate ADR. |
| GOV-CAP-05 — expiry/revocation | Short-lived capabilities; target maximum lifetime 5 minutes and maximum revocation-state staleness 30 seconds. If freshness cannot be established, deny new protected effects. Re-check before each protected side effect and lifecycle transition. | Revocation immediately blocks new effects; active tasks are fenced, moved to A0-owned cancellation/containment, and may perform only explicitly permitted safe cleanup. No silent offline fail-open. Clock uncertainty outside the accepted bound denies. |
| GOV-CAP-06 — Jarvis→A0 delegation | Jarvis may submit a mission-scoped request, not transfer or mint an A0 capability. The issuer grants A0 a separately bound capability only after policy evaluation. Delegation is attenuating and bound to exact subject, audience=A0, operation set, resource/target, constraints, task identity, expiry and provenance. | No wildcard resource, privilege inheritance, scope broadening, arbitrary product-state mutation or delegation to an unregistered executor. A0 may only perform admitted ASTRA workflow operations; downstream authority is separately checked. |
| GOV-CAP-07 — ingress acceptance | Acceptance requires a durable A0 receipt tied to immutable request digest, issuer proof, policy decision, principal, audience, operation/resource, expiry/revocation version and idempotency key. | Positive, negative, replay, concurrency, crash-recovery and race tests; exact-head CI; source-bound independent A3 security review by a reviewer who did not author, issue or implement the change; separate qualification and acceptance records. Transport ACK is not acceptance. |
| R-06 — audit/privacy | A separately accountable Security Audit function owns security-event integrity/access; the Privacy/Data Governance function owns classification and retention policy. Emit minimum correlated evidence for issuance, enrollment, verification, denial, expiry, revocation, replay, delegation, cancellation, recovery and privileged effects. | Append-only/tamper-evident evidence; least-privilege audit access; no secrets, credentials, private keys or bearer tokens in logs. Audit unavailable/integrity-failed means deny new privileged ingress and protected mutations; active work is fenced/contained, not silently continued. |

## 4. Initial policy defaults

These values are selected as conservative engineering defaults for the first controlled cloud-pool phase, not as claims about current implementation:

- Capability maximum lifetime: **5 minutes**.
- Maximum revocation-state age at a protected decision: **30 seconds**.
- Re-check: at ingress and immediately before every protected side effect or authority-changing lifecycle transition.
- Audit outage: fail closed for new privileged ingress and protected mutations; permit only explicitly defined non-mutating safe containment.
- Retention baseline: **365 days** for security decision/issuer/revocation/audit evidence and **90 days** for routine task-operational metadata, subject to stricter legal, contractual or privacy requirements and an approved deletion/legal-hold process. Do not retain credential material.
- Clock uncertainty: reject when the verifier cannot establish validity within the accepted clock-skew bound; the exact skew bound must be fixed in the implementation ADR and tested.

The 5-minute/30-second values must be load-tested against the cloud-pool control path before qualification. A failure to meet these bounds is a reason to improve revocation propagation or deny work, not to silently widen the trust window.

## 5. Mandatory failure semantics

Fail closed before protected action for missing, malformed, ambiguous, untrusted, suspended, expired, revoked, replayed, wrong-audience, wrong-subject, wrong-operation, wrong-resource, over-broad, stale or unverifiable authority. Reject schema downgrade and ambiguous canonicalization. Do not treat `approval_state=approved`, a caller-supplied enum, a Python type, a transport ACK, a valid HMAC from a different protocol, or a GitHub workflow identity as issuer proof.

Replay handling must use an atomic durable receipt/claim. Same idempotency key plus same payload digest returns the existing receipt; same key with a different digest is rejected and audited. A0 lease generations must fence stale workers. Revocation/cancellation/recovery races must not allow stale workers to commit effects.

## 6. R-06 privacy and retention implementation rules

- Separate security-event records from task payloads; store references/digests rather than copying sensitive payloads.
- Record stable principal/issuer IDs, capability ID or digest, policy/version, audience, operation/resource classification, decision, reason code, correlation ID, timestamps, revocation generation and A0 receipt/lease generation.
- Do not record raw tokens, authorization headers, API keys, passwords, private keys, session cookies or full sensitive task payloads.
- Restrict audit read access; log and review audit access itself.
- Integrity failure, audit sink outage or unverifiable event sequence blocks new privileged work.
- Retention defaults above are not permission to retain personal or sensitive data beyond applicable legal/privacy limits. Data minimization and deletion must be tested.

## 7. What is decided vs what remains open

**Selected by this owner-directed engineering disposition:** WB-05 Option A; authority-role separation; service-principal lifecycle ownership; mandatory verifier boundaries; trust-anchor custody role and dual control; short-lived grants and revocation freshness defaults; attenuating Jarvis→A0 delegation; durable ingress acceptance evidence and independent A3 review; fail-closed audit outage; initial retention defaults.

**Still requires evidence/ADR or named operational assignment:** actual accountable individuals/teams in the organization; existence and deployment of the issuer and audit services; specific KMS/HSM/provider; cryptographic protocol and token/schema format; identity source and enrollment integration; exact clock-skew bound; data-classification/legal review of retention; concrete audit sink; endpoint and network topology; cost/quota and availability objectives.

No person, repository secret, GitHub variable, provider, key identifier or deployed service is invented by this record.

## 8. Admission and implementation gates

This disposition does **not** authorize runtime changes or agent dispatch by itself. Before implementation:
1. Independently review this decision against MH-12, WB-03…06, Wave 149 and the current source finding.
2. Convert the accepted role/invariant decisions into a versioned technology-neutral normative contract and schemas.
3. Perform the separate protocol/KMS/identity/audit ADR with threat model, data-flow and cost/provider review.
4. Add executable positive/negative, mutation, replay, concurrency, crash-recovery, expiry/revocation and audit-outage tests.
5. Prove every protected consumer verifies authority; remove caller-controlled approval as an authority source.
6. Pass exact-head required CI and independent security review before any runtime integration.
7. Keep qualification, deployment and production acceptance separate.

Current Wave 482 A0-ISSUER-01 remains a HIGH source-level provenance gap, not a confirmed exploit. Until the above gates pass: issuer-backed ingress BLOCKED; runtime remediation BLOCKED; Gemini/Claude dispatch NOT AUTHORIZED BY THIS RECORD; Contour A NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED; Contour B GATED.

## 9. Source basis

- WB-05 blob: `1b562c6546b1216f2ee89095cd6a78427a967dc5` (four options and their trade-offs).
- Wave 149 governance matrix blob: `9c1a02dc125b37abea9284f0c0aa5deb571f13e7`.
- Wave 484 reconciliation: [report](MEDIAHUB-A0-ISSUER-GOVERNANCE-AND-LIFECYCLE-RECONCILIATION-WAVE-484-2026-10-30.md).
- Wave 485 contract skeleton: [contract](../architecture/MEDIAHUB-A0-ISSUER-INGRESS-LIFECYCLE-CONTRACT-SKELETON-WAVE-485-2026-10-30.md).
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md).
