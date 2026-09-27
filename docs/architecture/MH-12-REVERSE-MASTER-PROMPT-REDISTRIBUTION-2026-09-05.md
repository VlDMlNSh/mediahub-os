# MH-12 — REVERSE MASTER PROMPT

Date: 2026-09-05
Status: RECONCILED / GOVERNANCE REVIEW REQUIRED

## 1. MH identifier
MH-12 — SECURITY ARCHITECTURE

## 2. Historical scope
Identity, authentication, authorization, trust, capability security, security boundaries, human/service separation, secrets, cryptography, PKI/certificates/mTLS, API/network security, device/plugin/AI/cloud security, supply-chain/update/recovery security, audit, incident response, secure defaults, defense in depth, failure domains, security observability and security testing.

## 3. Source evidence / provenance
Primary canonical source: recovery/full-functional-spec control point and canonical registries. Historical MH-12 architecture-chat material supplied to this reconciliation is treated as evidence, not as independent canonical authority. Durable MH-12 architecture record exists under docs/architecture/MH-12-*. GitHub is persistent source of record.

## 4. CAP mapping
Primary: CAP-040 security_core defense-in-depth/trust/authentication/authorization/secure remote access; CAP-058 security_core security/safety invariant.
Cross-cutting references: CAP-023 network_core networking; CAP-039 privacy_security privacy/data governance; CAP-030 command authorization boundary; CAP-031/032/033 observability/health/diagnostics; CAP-034/042 recovery; CAP-044 update lifecycle; CAP-049 extensibility; CAP-050 verification; CAP-052 device lifecycle; CAP-056 authorized export.

No capability is deleted, retired or reassigned by MH-12.

## 5. Requirement mapping
Canonical security requirements are preserved as: explicit identity; authentication distinct from authorization; contextual revocable trust; operation-specific authorization; bounded capabilities; fail-closed behavior; boundary enforcement; human/service separation; secure secret lifecycle; cryptographic integrity; protected network/API/device/plugin/AI/cloud/update/recovery boundaries; auditable security decisions; incident containment; defense in depth; no silent privilege expansion.

## 6. Contract mapping
Primary contracts: CTR-003 identity-authentication-authorization; CTR-004 trust; CTR-002 consumer-boundary; CTR-006 device-command; CTR-016 network; CTR-018 cloud-development-boundary; CTR-019 assistant-escalation; CTR-022 diagnostics; CTR-023 recovery; CTR-024 update-lifecycle; CTR-026 privacy; CTR-028 mobile-endpoint; CTR-029 ecosystem-projection; CTR-032 export; CTR-033 telemetry; CTR-036 verification-acceptance.

## 7. Invariant mapping
Primary canonical invariants: INV-002 security by design; INV-003 discovery != trust; INV-004 presence != authentication; INV-005 authentication != authorization; INV-006 remote access != increased authorization; INV-007 ordinary user != cloud development; INV-009 offline-first where possible; INV-020 physical connection != authorization; INV-021 security system-level/cross-cutting; INV-022 health observation-only; INV-023 readiness operation-scoped; INV-024 health/readiness/liveness/trust/authorization distinct; INV-026 historical evidence preserved; INV-027 unique canonical function; INV-029 cloud-development cluster distinct from local cluster.

MH-12 candidate security invariants SI-01…SI-30 remain a security projection and are NOT silently promoted to canonical registry invariants.

## 8. Decision mapping
Accepted: DEC-001…DEC-012, with direct MH-12 relevance especially DEC-002, DEC-005, DEC-006, DEC-007, DEC-008, DEC-009, DEC-011, DEC-012.
Draft architecture decisions: DEC-A-001…DEC-A-004. MH-12 supports their security implications but does not accept them.

## 9. Architecture / boundary mapping
Canonical security flow:
External/Input → Integration Boundary → Consumer Contract → Identity → Authentication → Trust → Capability → Authorization → Policy → Command/Proposal → Consumer Boundary → State Authority → Event → Audit/Observability.

Security controls trust and authorization; State Authority remains the sole canonical mutation authority; Consumer Boundary remains mandatory; observability reports security state and does not enforce it.

Failure-domain boundaries: UI, AI, plugin, device adapter, cloud, diagnostics, update and recovery components must not automatically inherit State Authority.

## 10. Classification
- RETAIN: security authority separation, identity/auth/authz distinction, fail-closed semantics, trust model, capability constraints, boundary model, threat model, secure defaults, audit/incident response.
- REMAP: security responsibilities are projected into canonical security_core/privacy_security/network_core and related contracts rather than historical subsystem ownership.
- RECONCILE: security authorization with P0-05 transaction authorization; P0-07 capability authorization gap; recovery/update/diagnostic authority boundaries; cross-MH security ownership.
- REPLACE: none by MH-12.
- RETIRE: none.
- UNKNOWN: exact technology stack, cryptographic algorithms/parameters, PKI topology, secret store, hardware-backed security, exact network topology/firewall, exact recovery/update roots, exact cloud identity, threat probabilities and operational performance limits.

## 11. Contradictions
C-01: security authorization vs P0-05 transaction authorization — OPEN architectural compatibility point.
C-02: P0-07 capability authorization vs P0-04 transaction authorization — OPEN; known governance/API gap; no bypass authorized.
C-03: recovery privilege vs State Authority — requires explicit gate/authorization contract.
C-04: update authority vs runtime authority — must prevent silent privilege expansion.
C-05: diagnostics vs sensitive mutation — diagnostics cannot bypass normal authorization.
C-06: observability vs enforcement — RESOLVED architecturally: observability reports; security enforces.

## 12. Missing evidence
Exact implementation technology and deployment topology remain evidence-gated. Absence is not loss.

## 13. Dangling / stale references
Potentially dangling until central reconciliation: historical technology names without canonical ADRs; exact adapter/security implementation references; any direct security-to-State-Authority shortcut not represented by approved contract. These are GAP/OPEN, not deletion candidates.

## 14. Proposed technical decisions
No technology is made canonical. Candidate ADRs are required for identity, authentication, authorization, capability representation, trust, secrets, PKI, network security, device enrollment, plugin security, AI security, cloud boundary, supply chain, update trust, recovery trust and incident response.

## 15. Contract impacts
CTR-003/004 need explicit lifecycle and revocation semantics. CTR-002/006/023/024/026/028/029/032/033 require security-context binding and audit where applicable. No frozen P0-03…P0-06 contract is changed by this reconciliation.

## 16. Invariant impacts
No canonical invariant change proposed. SI-01…SI-30 remain proposed MH-12 security invariants pending governance and central reconciliation.

## 17. Dependency impacts
MH-12 depends on MH-02 boundaries, MH-03/MH-06 runtime, MH-04 security foundation, MH-05 consumer boundary, MH-07 policy, MH-08 plugins, MH-09 UI, MH-10 AI, MH-11 observability, MH-13 privacy, MH-16 recovery/update, MH-17 devices, MH-21 distributed AI/cloud, MH-22 verification.

## 18. Verification requirements
Negative authorization tests; forged identity/capability; replay; stale/expired credentials; malformed security context; ambiguity; privilege escalation; confused deputy; plugin/AI boundary tests; cloud egress; device enrollment/revocation; secret leakage scans; update/recovery trust tests; audit integrity; cross-domain isolation; supply-chain verification; regression against P0-03…P0-07.

## 19. Acceptance evidence
Required evidence: traceability FUNCTION→REQUIREMENT→CONTRACT→ARCHITECTURE→IMPLEMENTATION BOUNDARY→TEST→ACCEPTANCE; security test results; evidence register; ADRs; contradiction closure; compatibility proof with P0-03…P0-07; governance approval.

## 20. Acceptance authority
MH-12 architecture chat has no unilateral acceptance authority. Central reconciliation prepares the Master Architecture Acceptance Request; explicit human acceptance is required before Master Architecture acceptance/freeze.

## 21. Remaining OPEN items
Exact auth stack; capability representation; authorization implementation; PKI/CA topology; secret storage; hardware-backed security; network segmentation implementation; device enrollment trust root; update signing root; recovery trust root; cloud identity; threat likelihood methodology; performance/resource limits; P0-07 authorization bridge.

## 22. Anti-loss confirmation
PASS. No CAP-001…CAP-058 is removed, retired or declared lost by MH-12. Unknown/evidence gaps remain explicit. Canonical baseline remains 58/58 preserved.

## 23. Suggested canonical registry changes
None applied. Proposed only: formalize security contract details and, after central reconciliation, consider promoting selected MH-12 security invariants to canonical INV entries if governance accepts them. Every such change requires evidence, affected CAP/CTR/INV/DEC, dependency impact, verification impact and acceptance authority.

## 24. Authority statement
MH-12 has no unilateral authority to modify canonical registries, accepted decisions, capability ownership or invariants.

## Final gate
MH-12 RECONCILED. Architecture complete; governance review required; implementation not authorized by this record; production not qualified; acceptance/freeze not granted.
