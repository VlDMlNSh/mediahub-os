# MediaHub Historical Corpus Reconciliation Matrix — 2026-09-05

STATUS: IN PROGRESS — FORENSIC RECONCILIATION
BRANCH: recovery/full-functional-spec

## Purpose
Consolidated pass over MH-01…MH-23 Git-backed evidence. Historical material is evidence, not automatic accepted architecture. No capability is retired because a historical chat is unavailable from the current searchable corpus.

## Evidence matrix

| MH | Git evidence state | Forensic disposition | Master-architecture consequence |
|---|---|---|---|
| MH-01 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |
| MH-02 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |
| MH-03 | Strong multi-artifact corpus | RETAIN / REMAP | Runtime, lifecycle, events, health, observability, degraded mode, recovery, service boundaries preserved |
| MH-04 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |
| MH-05 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |
| MH-06 | Strong multi-artifact corpus | RETAIN / REMAP | Health/readiness semantic contract, runtime, lifecycle, IPC, failure/recovery, observability and resource governance preserved |
| MH-07 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |
| MH-08 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |
| MH-09 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |
| MH-10 | Strong AI architecture corpus | RETAIN / REMAP | AI intelligence and authority boundaries preserved under Local Assistant + controlled cloud development |
| MH-11 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |
| MH-12 | Strong security architecture corpus | RETAIN / REMAP | Identity, authentication, authorization, trust, PKI/crypto, segmentation, incident response, secure defaults and supply-chain security preserved |
| MH-13 | Strong privacy/data governance corpus + MH-18 provenance | RETAIN / REMAP | Privacy/data governance and MH-18 provenance remain cross-cutting |
| MH-14 | Strong development interface/persistence corpus | RETAIN / REMAP | Development interface, persistence and acceptance boundaries preserved; ordinary-user/cloud separation remains |
| MH-15 | Strong canonical OS appliance corpus | RETAIN / RECONCILE | Appliance/runtime model is evidence; canonical capability architecture remains authoritative |
| MH-16 | Strong installer/recovery/update corpus | RETAIN / REMAP | Installer, recovery and update lifecycle preserved |
| MH-17 | Strong device/integration corpus | RETAIN / REMAP | Device scope, groups, replacement, firmware, protocol selection, compatibility, safety, offline and integration backpressure preserved |
| MH-18 | Provenance pinned; historical media architecture evidence | RETAIN / REMAP | Media provenance, privacy and media architecture must survive reconciliation |
| MH-19 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |
| MH-20 | Automation governance evidence | RETAIN / REMAP | Automation authority, governance and orchestration remain represented |
| MH-21 | Very strong distributed AI/security/cloud corpus | RETAIN / REMAP | Cloud boundary, distributed AI, model/provider trust, RAG, agents, egress, residency, remote compute, safe degradation and observability remain mandatory |
| MH-22 | Strong production qualification corpus | RETAIN / REMAP | Production gates, qualification, readiness, acceptance and maturity remain verification requirements |
| MH-23 | UNKNOWN / no matching commit search result | UNKNOWN | Do not infer loss |

## Cross-MH semantic reconciliation

### RETAIN
The following historical concepts are confirmed as compatible with the accepted baseline and must remain represented:
- capability-centric runtime and service boundaries;
- explicit state, command, identity, authorization and trust boundaries;
- observation-only Health and operation-scoped Readiness;
- local-first/offline-safe operation and controlled degradation;
- recovery, persistence, update and migration boundaries;
- device integration lifecycle and protocol-selection gates;
- security defense in depth, PKI/cryptography, segmentation, audit and incident response;
- privacy, data classification, retention, egress and residency governance;
- Local Assistant first, controlled external/cloud escalation;
- distributed compute/AI with workload placement and resource governance;
- media provenance, storage separation, routing and lifecycle;
- automation governance;
- production qualification and acceptance evidence.

### REMAP
Historical component/service decomposition is remapped behind canonical capabilities and contracts. It does not create new user-facing product entities and does not redefine the accepted functional baseline.

### RECONCILE
Where historical technical choices conflict or are more specific than the accepted baseline, preserve the evidence and open a technical reconciliation item rather than silently selecting or deleting a design.

### REPLACE
No historical capability was found in this pass that must be replaced at the functional level. Technical implementation choices may later be replaced after evidence/technology evaluation.

### RETIRE
No historical canonical capability is retired by this pass.

### UNKNOWN
MH-01, MH-02, MH-04, MH-05, MH-07, MH-08, MH-09, MH-11, MH-19 and MH-23 have no matching direct commit-search evidence in the accessible GitHub search surface used in this pass. This means UNKNOWN, not loss.

## Newly strengthened architecture requirements
Historical MH-06/MH-10/MH-12/MH-14/MH-16/MH-17/MH-20/MH-21/MH-22 evidence collectively strengthens the need for explicit contracts for:
1. runtime lifecycle/startup/shutdown and IPC;
2. health/readiness/observability/recovery;
3. AI authority and provider/model trust;
4. identity/authentication/authorization/PKI/cryptography;
5. persistence and filesystem recovery;
6. installer/update/recovery lifecycle;
7. device integration, protocol selection, compatibility and failure;
8. automation governance;
9. distributed AI/cloud boundaries, workload placement and egress;
10. production qualification and acceptance.

## Gate state
Historical reconciliation is materially advanced but cannot be declared exhaustive because direct machine-readable full chat corpus for all 23 historical chats is still unavailable.

MASTER ARCHITECTURE: DRAFT / NOT ACCEPTED
MH-01…MH-23 DISTRIBUTION: BLOCKED
PRODUCTION IMPLEMENTATION: BLOCKED
