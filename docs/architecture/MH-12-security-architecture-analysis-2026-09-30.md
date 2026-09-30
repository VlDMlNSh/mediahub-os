# MH-12 — Security Architecture Analysis — 2026-09-30

Status: ARCHITECTURE RECONCILED / ETALON BASELINE / AUTONOMOUS QUALIFICATION QUEUED / CLOSURE PENDING EVIDENCE

## 1. Scope

Independent security reconciliation of MH-4 and MH-12 against the current authoritative GitHub branch `engineering/mh21-sandbox-lifecycle-20260910` at the latest verified branch revision recorded after this reconciliation.

This document does not create a second Security Architecture and does not replace MH-4.

## 2. Security baseline confirmed

The following architectural invariants are consistently represented:
- State Authority is the sole canonical mutation authority.
- HA/Smart Home operational authority remains behind the MediaHub governed boundary.
- AI, cloud, plugins, observability and diagnostics are non-authoritative.
- Authentication is distinct from authorization.
- Reachability, localhost and VPN are not trust or authorization.
- Capabilities are bounded and cannot self-expand.
- Unknown/ambiguous security states fail closed or enter quarantine/safe degradation.
- Recovery and update are separate security boundaries.
- Secrets are distinct from ordinary configuration/telemetry.
- Security enforcement is distinct from observation/audit/diagnostics.
- R4 remains an ancestor of the current authoritative branch.

## 3. Principal threat classes

Covered by the existing model and current reconciliation: remote/local attacker, compromised client/node/service, malicious plugin, compromised dependency, compromised AI/model, prompt/indirect prompt injection, malicious documents/RAG context, compromised Smart Home integration, external API/provider compromise, cloud/developer-domain compromise, credential theft, excessive insider privilege, physical attacker, rogue device/node, network attacker, replay, downgrade, malicious update, ransomware/destructive operator error and misconfiguration.

## 4. Trust-boundary result

The architecture has the correct logical boundaries for:
user/UI/mobile; API/consumer boundary; identity/authentication; policy; State Authority; core services; Smart Home; devices/integrations; plugins; AI/local AI; storage; network/egress; cloud; developer fabric; backup/recovery; update; external providers.

The remaining gap is not absence of the boundary model. It is qualification of concrete protocols, endpoint inventories, identity enrollment, revocation semantics and enforcement coverage for every production path.

## 5. Identity / authentication / authorization

Architecture is coherent: human, service, device, plugin, AI/model, workload, recovery, update/signing and audit principals are separated.

Material gap: mobile authenticated-session/authz contract is explicitly ABSENT in P5.2. Generic session and credential infrastructure does not close mobile authentication, offline authorization or revocation.

Material gap: concrete credential/key technology and lifecycle evidence remain non-canonical / verification-dependent.

## 6. Capability / policy

Capability fields, attenuation, revocation and confused-deputy protections are defined. Policy is logically centralized with local enforcement.

Material gap: concrete policy-cache TTL, stale-policy behavior by operation class, privileged JIT lease semantics and cross-domain policy enforcement evidence are not fully qualified.

## 7. API / event security

API schema validation, authorization, limits, audit and fail-closed behavior are architecturally required. State Authority requires authenticated/authorized command context and rejects malformed/ambiguous/stale requests.

Material gap: complete public API inventory and end-to-end replay/idempotency qualification are not demonstrated.

External-event security is defined conceptually, but comprehensive production event-source qualification remains open.

## 8. Network / egress / CPRG

Default-deny egress and destination validation are implemented for reviewed development surfaces. P9.3 nevertheless remains OPEN because repository evidence does not prove that every production-relevant egress path is covered.

CPRG registration must remain a narrow registration capability and must not become a general proxy/NAT/data-plane path.

Material gap: complete CPRG implementation/qualification and exhaustive egress-path inventory are not established by the current evidence.

## 9. State Authority / Smart Home

MH-04 State Authority contract is accepted for the authorized in-memory scope. Security boundary and negative-test requirements are explicit.

Material gap: durable persistence, HA, cross-node consensus/failover, rollback/split-brain protection and production recovery remain outside the accepted in-memory scope.

Smart Home security remains dependent on a fully qualified MediaHub → HA Core → device authorization chain; generic architecture alone does not prove every integration is admitted through it.

## 10. AI / plugin / cloud

AI is correctly treated as untrusted/non-authoritative and capability-scoped. Plugin provenance/signature is correctly separated from runtime authorization. Cloud is external/untrusted by default.

P8.5 remains OPEN: a single independently verifiable request → artifact → execution-result → evidence provenance chain is not established.

Developer Fabric isolation is architecturally explicit, but production qualification must prove that user data and operational authority cannot cross into developer workloads.

## 11. Secrets / keys / supply chain

Secret lifecycle and exclusion from logs/telemetry/AI context are defined.

P9.2 remains OPEN: repository review identified two secret-related keyword locations with values omitted; no complete transitive dependency/license provenance was established from repository manifests; external advisory scanning was not claimed.

Key separation, hardware-backed protection and exact cryptographic profile remain technology/ADR/verification decisions rather than accepted implementation facts.

## 12. Recovery / backup / ransomware

Recovery is correctly a separate privileged boundary and current restore tamper-evidence was strengthened.

P9.7 explicitly does not qualify durable backup/restore, cross-node disaster recovery or production persistence. Backup isolation, separate keys and immutable/offline recovery points therefore remain qualification requirements.

Backup existence must not be treated as proof of recoverability.

## 13. Mobile / physical / HIGH_SPEED / developer fabric

Mobile security architecture is stated, but P5.2 shows the executable mobile auth/session/authz contract is absent.

Physical attack classes and HIGH_SPEED/Thunderbolt/USB4 trust separation are architecturally required, but concrete platform mitigation and admission evidence remain to be qualified.

Developer Fabric has the correct trust-domain separation; operational proof of zero user-data access and no privileged operational backdoor remains required.

## 14. Update / bootstrap / node admission

Update provenance, signing, downgrade protection, compatibility, rollback and recovery gates are defined.

Material gap: complete bootstrap and node-admission evidence is not demonstrated for every node class, including cryptographic identity enrollment, attestation where available, revocation and requalification.

## 15. Observability / incident response / automation

Separation of security enforcement, audit, observability and diagnostics is coherent. Incident lifecycle and bounded automated containment actions are defined.

Material gap: attack-timeline completeness, evidence preservation guarantees and end-to-end incident automation qualification remain open.

## 16. Supply-chain and qualification state

Architecture covers source/dependency/build/artifact/sign/registry/deployment/runtime. Current repository evidence does not establish full reproducible build provenance, complete SBOM coverage, transitive vulnerability state or independent security qualification.

## 17. Cross-MH contradictions / unresolved security gates

C-01: Security authorization vs MH-05 consumer-boundary authorization — OPEN.
C-02: MH-07 capability authorization vs State Authority transaction authorization — OPEN.
C-03: Recovery privilege vs State Authority authority — OPEN.
C-04: Update authority vs runtime authority — OPEN.
C-05: Diagnostics vs sensitive mutation — OPEN.
Observability/enforcement separation is resolved.

These must be reconciled before MH-12 closure.

## 18. Security strengths

1. Single canonical mutation authority is explicit.
2. AI/cloud/plugin non-authority is explicit.
3. Identity/authentication/authorization/trust are semantically separated.
4. Capability attenuation and no-self-grant rules are explicit.
5. Fail-closed and quarantine semantics are explicit.
6. Egress is policy-controlled and development egress has executable negative tests.
7. Recovery/update are separated from runtime authority.
8. Security/observability/diagnostics authority separation is explicit.
9. Existing negative security testing covers State Authority, sandbox, native execution, malformed input and recovery tamper evidence.

## 19. Security gaps requiring qualification

G-01 Mobile authentication/session/authorization contract and tests.
G-02 Complete production egress inventory and qualification.
G-03 CPRG implementation and registration/data-plane separation evidence.
G-04 Complete key-management/root-of-trust profile.
G-05 Durable State Authority/HA security model and split-brain/rollback qualification.
G-06 End-to-end provenance chain.
G-07 Complete dependency/SBOM/advisory/license provenance.
G-08 Bootstrap/node admission/revocation qualification.
G-09 Physical/HIGH_SPEED platform mitigation qualification.
G-10 Developer Fabric user-data isolation qualification.
G-11 Backup/restore/ransomware recovery qualification.
G-12 Incident evidence/timeline and security automation qualification.
G-13 Cross-contract authorization reconciliation C-01…C-05.

## 20. Immutable MH-12 security invariants

SI-01 State Authority is the sole canonical mutation authority.
SI-02 Authentication is not authorization.
SI-03 Identity is not privilege.
SI-04 Reachability/localhost/VPN is not authorization.
SI-05 Capability cannot self-grant or expand.
SI-06 AI/plugin/cloud cannot become authority.
SI-07 Unknown or unverifiable entities are denied/quarantined.
SI-08 Critical ambiguity fails closed.
SI-09 Recovery/update cannot silently bypass security or State Authority.
SI-10 Secrets never become ordinary telemetry/context.
SI-11 Security enforcement, audit, observability and diagnostics remain distinct.
SI-12 A compromised failure domain cannot automatically compromise another protected domain.
SI-13 Security boundary cannot become a hidden State Authority, Smart Home Authority or Developer/User Data isolation bypass.

## 21. Closure status

MH-12 analysis is substantively complete, but MH-12 closure is NOT GRANTED.

Closure requires explicit governance decisions for the unresolved authority/recovery/mobile/credential/key and risk-acceptance questions, followed by reconciliation evidence. Architecture text alone is insufficient for closure.

## 22. Evidence basis

- MH-12 Security Architecture and security subdocuments.
- MH-04 State Authority Contract v1.0.
- MH-06 security/recovery invariants.
- MH-21 security/data-egress/cloud boundary.
- P5.2, P7.5, P7.6, P8.5, P9.1–P9.7 reconciliation records.
- GitHub branch `engineering/mh21-sandbox-lifecycle-20260910`, current verified HEAD `91f841b1b00f412e218892732c645cae0f1935d8` before the queue-record write.
