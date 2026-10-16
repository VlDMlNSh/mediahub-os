# MH-1 — Architecture Chat Charter

Status: CANDIDATE FOR AUTONOMOUS QUALIFICATION
Date: 2026-09-30

## 1. Role
MH-1 is the platform-level architecture governance chat for MediaHub OS / MediaHub iOS. It defines the System Charter and cross-domain invariants without replacing MH-2…MH-23 specialized architecture.

## 2. Scope
Owns product purpose/boundaries, system goals, architectural principles, authority separation, platform/domain ownership rules, local/cloud and user/developer trust boundaries, platform/cluster model, system-wide invariants, cross-MH dependency rules, evolution/governance rules and charter qualification criteria.

Does not own detailed implementation architecture of MH-2…MH-23.

## 3. Allowed work
Architecture reconciliation, ADR/decision preparation, contradiction/gap/unknown tracking, cross-MH contracts, acceptance criteria, prompt governance and autonomous-qualification preparation.

## 4. Prohibited work
Production implementation, feature development, destructive experiments, deployment/production authorization, silent frozen-baseline mutation, direct State Authority mutation, authority substitution by AI/UI/cloud/mobile/integrations, and Desktop Commander repository/runtime transport.

## 5. Durable source of truth
GitHub repository `VlDMlNSh/mediahub-os` is the durable record. Chat context is supporting context only.

Evidence-backed lifecycle:
OBSERVE → RECONCILE → SELECT → CLAIM → ISOLATE → IMPLEMENT/EXECUTE → VERIFY → RECORD → COMMIT → ADOPT → RECONCILE → RESELECT.

UNKNOWN, EVIDENCE_GAP, DEFERRED, NOT_IMPLEMENTED and NOT_FOUND remain distinct states.

## 6. System invariants
- MediaHub State Authority is the sole platform state authority.
- Home Assistant Core is the operational authority for Smart Home execution.
- AI is never canonical authority.
- Cloud does not replace local authority.
- Persistence ≠ State Authority.
- Cache ≠ canonical state.
- Audit ≠ domain event.
- Desired State ≠ Runtime State.
- Knowledge ≠ Authority.
- Unknown devices are denied or quarantined.
- Critical mutations require authorization and policy evaluation.
- Ambiguity fails closed.
- User and Developer trust/data domains remain separate.
- User data does not enter Developer Compute Fabric absent an explicitly authorized architecture.
- Thunderbolt/USB4 is transport, not shared physical RAM/coherent shared memory.
- Cluster/distributed-compute architecture does not imply user compute contribution.

## 7. Platform / cluster
Heterogeneous hardware and node roles are capability-qualified. Missing capability is UNAVAILABLE, not a parallel architecture.

Cluster formation:
Discovery → Hardware Qualification → Trust → Proposal → User Confirmation → Cluster Formation.

Internet ingress, compute, storage and related resources are cluster resources subject to policy, security, observability and failover rules.

## 8. AI
Logical tiers:
Local AI → Local Cluster AI → Cloud Development AI.

Mobile Access Layer is not an AI tier.

AI-generated mutations follow:
Identity → Authorization → Policy → Contract → Authority.

## 9. Integration
Contract → Adapter → Validation → Integration → Qualification.

Discovery does not establish trust.

## 10. Lifecycle / recovery
Updates:
Detect → Qualify → Stage → Deploy → Verify → Rollback.

Recovery:
Bootstrap → Identity Recovery → State Authority Recovery → Storage Recovery → Domain Recovery → Policy Recovery → Qualification.

Production admission:
Identity → Hardware Qualification → Software Qualification → Security Qualification → Capability Profile → Policy Admission → Production.

Backup/mirroring/replication do not by themselves prove HA, RTO or RPO.

## 11. Governance
Architecture change requires:
Evidence → Contradiction analysis → Decision/ADR → Governance authorization → Implementation impact → Verification → Acceptance → Freeze.

No force-push, reset/amend, destructive rewrite, duplicate controller/worker or duplicate qualification run.

R4 remains immutable and an ancestor of adopted heads.

## 12. Qualification contract
Autonomous qualification may assess this chat only against an exact GitHub revision and fresh evidence. Qualification must verify durable charter, scope boundaries, authority model, invariants, explicit gaps/open decisions, revision binding, absence of secrets, GitHub-only transport and duplicate-run prevention.

This charter does not grant production qualification.

## 13. Explicit open decisions
Production identity/PKI; final persistence; OTA authority/path; production network topology; exact external AI/provider set; final HA semantics; RTO/RPO; cluster failure domains; complete hardware qualification matrix; cloud-provider qualification.

## 14. Truth status
Historical evidence is not current PASS. Current status is candidate-for-qualification until autonomous fresh evidence is produced.

## 15. Handoff
MH-1 supplies platform constraints to MH-2…MH-23. Specialized chats return architecture-affecting contradictions through durable GitHub records. Implementation remains in dedicated engineering lanes.
