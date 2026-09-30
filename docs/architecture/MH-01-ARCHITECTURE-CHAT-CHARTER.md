# MH-1 — Architecture Chat Charter

Status: CANDIDATE FOR AUTONOMOUS QUALIFICATION
Date: 2026-09-30

## 1. Purpose

MH-1 is the authoritative architecture chat for the MediaHub OS / MediaHub iOS System Charter. It defines the platform-level architectural constitution and preserves cross-domain invariants without absorbing the detailed architecture owned by MH-2…MH-23.

The chat is an architecture governance surface, not a development workspace.

## 2. Scope

MH-1 owns:
- product/system purpose and boundaries;
- system goals and architectural principles;
- authority model and authority separation;
- canonical domain ownership at the platform level;
- local/cloud and user/developer trust boundaries;
- platform and cluster model;
- system-wide invariants and prohibitions;
- cross-MH dependency rules;
- evolution and governance rules;
- acceptance criteria for the system charter.

MH-1 does not replace the specialized architecture of MH-2…MH-23.

## 3. Allowed work

- evidence reconciliation;
- architecture decisions and ADR preparation;
- contradiction, gap and unknown tracking;
- cross-MH interface definition;
- acceptance criteria and qualification contracts;
- maintenance of master/reverse-master prompts;
- synchronization of authoritative architecture records through GitHub Transport;
- preparation of autonomous qualification requests.

## 4. Prohibited work

- production implementation;
- feature development;
- debugging implementation;
- destructive experiments;
- deployment or production authorization;
- silent modification of frozen baselines;
- direct State Authority mutation;
- treating AI, UI, cloud, mobile, or external integrations as authority;
- using ChatGPT history as the sole durable source of truth;
- use of Desktop Commander for repository/runtime transport.

## 5. Source of truth

GitHub repository `VlDMlNSh/mediahub-os` is the durable source of record for MH-1 architecture artifacts. Chat context is supporting context only.

Canonical state transitions must remain evidence-backed:
OBSERVE → RECONCILE → SELECT → CLAIM → ISOLATE → IMPLEMENT/EXECUTE → VERIFY → RECORD → COMMIT → ADOPT → RECONCILE → RESELECT.

UNKNOWN, EVIDENCE_GAP, DEFERRED, NOT_IMPLEMENTED and NOT_FOUND must not be collapsed into LOST, REJECTED, REMOVED or NEVER_EXISTED.

## 6. System invariants

- MediaHub State Authority is the sole platform state authority.
- Home Assistant Core remains operational authority for Smart Home domain execution.
- AI is assistant/proposal/automation/analysis infrastructure, never canonical authority.
- Cloud does not replace local authority.
- Persistence is not State Authority.
- Cache is not canonical state.
- Audit is not a domain event.
- Desired state is not runtime state.
- Knowledge is not authority.
- Unknown devices fail closed or enter quarantine.
- Critical operations require authorization and policy evaluation.
- Ambiguity fails closed.
- Developer trust/data domain is separate from user trust/data domain.
- User data must not flow into Developer Compute Fabric unless an explicit, authorized architecture later establishes such a boundary.
- Thunderbolt/USB4 is transport, not shared physical RAM or a single physical address space.
- No user compute contribution is implied by cluster/distributed-compute architecture.

## 7. Platform and cluster model

MediaHub supports heterogeneous nodes and roles. Capability is qualified explicitly; unavailable capability is represented as UNAVAILABLE rather than creating a parallel architecture.

Cluster formation is:
Discovery → Hardware Qualification → Trust → Proposal → User Confirmation → Cluster Formation.

Internet ingress, compute, storage and other shared resources are cluster resources subject to policy, failover, observability and security.

## 8. AI boundary

Logical AI tiers:
Local AI → Local Cluster AI → Cloud Development AI.

Mobile Access Layer is not an AI tier.

AI-generated actions must pass the canonical mutation path:
Identity → Authorization → Policy → Contract → Authority.

## 9. Integration boundary

Canonical integration pattern:
Contract → Adapter → Validation → Integration → Qualification.

Discovery does not create trust.

## 10. Lifecycle and recovery

Updates:
Detect → Qualify → Stage → Deploy → Verify → Rollback.

Recovery:
Bootstrap → Identity Recovery → State Authority Recovery → Storage Recovery → Domain Recovery → Policy Recovery → Qualification.

Production admission:
Identity → Hardware Qualification → Software Qualification → Security Qualification → Capability Profile → Policy Admission → Production.

Backup, mirroring and replication do not by themselves establish HA, RTO or RPO.

## 11. Governance and change control

Architecture change requires:
Evidence → Contradiction analysis → Decision/ADR → Governance authorization → Implementation impact → Verification → Acceptance → Freeze.

Historical artifacts are preserved. No force-push, reset/amend, destructive rewrite, duplicate controller, duplicate worker or duplicate qualification run is permitted.

R4 remains immutable and must remain an ancestor of adopted heads.

## 12. Qualification contract

The chat is eligible for autonomous qualification only when:
1. the durable chat charter exists in GitHub;
2. scope/non-scope and authority boundaries are explicit;
3. invariants are machine- or evidence-checkable where practical;
4. current gaps are recorded rather than hidden;
5. qualification target is bound to an exact commit/tree;
6. no secrets are required or exposed;
7. GitHub Transport is the only repository/runtime transport;
8. the qualification request is placed into the canonical Astra qualification queue without creating a duplicate run;
9. PASS is granted only from fresh evidence.

This charter does not itself grant production qualification.

## 13. Known open architectural decisions

The following remain explicit open decisions and must not be silently converted to fixed architecture:
- production identity/PKI;
- final persistence architecture;
- final OTA authority and production update path;
- production network topology;
- exact external AI/provider set;
- final HA semantics;
- RTO/RPO;
- cluster failure-domain semantics;
- complete hardware qualification matrix;
- cloud-provider qualification.

## 14. Qualification truth

Current architectural state is suitable for a qualification request, but autonomous qualification evidence is not yet established by this document.

Historical evidence must not be promoted to current PASS without fresh target-bound verification.

## 15. Hand-off

MH-1 provides constraints to MH-2…MH-23. Specialized chats return architecture-affecting contradictions to MH-1 through durable GitHub records. Implementation belongs to dedicated development lanes.

