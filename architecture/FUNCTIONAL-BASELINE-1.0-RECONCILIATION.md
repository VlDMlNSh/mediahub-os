# MediaHub OS 11.x LTS / MediaHub iOS — Functional Baseline 1.0 Reconciliation

Date: 2026-09-11
Status: ACCEPTED INPUT / ARCHITECTURAL RECONCILIATION RECORD
Source: MediaHub Functional Baseline 1.0 supplied as the canonical functional product passport.

## 1. Authority of the passport

Functional Baseline 1.0 is the authoritative functional target for downstream capability, contract and implementation planning.

It does not silently override frozen lower-level governance decisions. Where the passport describes target persistence, HA, storage, OTA or cluster capabilities while the current MH-03 runtime foundation explicitly remains single-node, in-memory and non-persistent, the target capability is recorded as a future implementation phase and requires its own architecture/acceptance gate.

## 2. Canonical authority model

- MediaHub State Authority = canonical authority for platform state.
- Home Assistant Core = authority for Smart Home domain state.
- No AI, cloud, mobile application, external ecosystem, automation engine, backup system, OTA mechanism or infrastructure component may become a competing MediaHub authority.
- Recovery is bounded lifecycle authority, not state authority.
- Observability is non-mutating.

## 3. Current foundation versus target architecture

### Current frozen foundation

- Single node.
- State Authority is in-memory.
- No HA.
- Physical persistence is not authorized by the current MH-03 runtime foundation.
- Deterministic local operation must not depend on Internet, cloud, external AI, RAG, paid APIs or physical persistence.

### Functional target

The passport additionally requires PostgreSQL, pgvector, object storage, backup/recovery, cluster compute, OTA, mobile-local Core, documents, Digital Twin, engineering, Local AI, Local Cluster AI and Cloud Development AI.

These are implementation targets. Each target that conflicts with current frozen runtime constraints must enter the governance sequence rather than being introduced implicitly.

## 4. Component reconciliation

### Confirmed target components

The passport explicitly names the following mature OSS foundations or priority candidates:

- Home Assistant Core
- IfcOpenShell
- web-ifc
- PaddleOCR
- OpenCV
- ONNX Runtime
- llama.cpp
- PostgreSQL
- pgvector
- Temporal
- OpenTelemetry
- Prometheus
- Cosign
- Syft
- Trivy
- restic
- RAUC
- OpenBao
- S3-compatible object storage
- OCI registry

P1/reference components remain conditional on capability gap, benchmark and qualification.

### Existing registry components requiring status correction

NATS and etcd remain technically useful primitives, but they are not named as foundational components in Functional Baseline 1.0 and are not permitted to override the current single-node/no-HA foundation. Their status is therefore FUTURE-CANDIDATE / GOVERNANCE-GATED rather than current runtime foundation.

PostgreSQL remains a target persistence primitive, but its runtime activation is gated by the persistence architecture and acceptance criteria; it must not silently replace the current in-memory State Authority model before that gate passes.

RAUC remains the preferred target OTA mechanism. Mender is reference-only and must not create a second production OTA authority.

Temporal remains reference-first until a concrete durable-workflow capability gap is demonstrated.

Redis remains excluded as a foundational dependency unless measured evidence demonstrates a non-overlapping requirement that cannot be met by the selected architecture.

Kafka remains excluded as a foundational dependency unless measured throughput/retention requirements demonstrate a material gap.

Kubernetes/K3s remains conditional P1 infrastructure, not a mandatory MediaHub prerequisite.

## 5. Contract-first decomposition

Every passport capability must map to:

`Capability → Contract → Authority → Adapter/Runtime → Validation → Qualification`

No implementation may establish a hidden direct connection that bypasses this chain.

## 6. Domain authority map

| Domain | Authority |
|---|---|
| Platform state | MediaHub State Authority |
| Smart Home | Home Assistant Core |
| User identity/trust | MediaHub Security/Trust layer |
| Media domain | MediaHub Media domain |
| Documents | MediaHub Document domain |
| Digital Twin | MediaHub Digital Twin domain |
| Engineering | MediaHub Engineering domain |
| Network | MediaHub Network domain |
| AI execution | MediaHub AI Gateway + governed runtime |
| Cloud compute | Cloud Development AI boundary |
| Backup/recovery policy | MediaHub Recovery Authority |
| OTA policy | MediaHub Update Authority |
| Evidence/provenance | MediaHub-owned evidence/provenance model |
| Telemetry | MediaHub observability policy |

## 7. AI invariants

Local AI, Local Cluster AI and Cloud Development AI are execution/capability layers, not authority layers.

All state-changing AI actions must re-enter the normal governed command path. Cloud escalation requires authorization, policy, data classification, residency/egress checks, audit and revocation capability.

## 8. Mobile invariants

Mobile Access Layer consists of exactly two applications:

1. MediaHub Core for iOS/iPadOS — minimal local MediaHub Core.
2. MediaHub iOS Remote — remote access application.

The applications must not converge into a single ambiguous authority model.

## 9. Recovery and update invariants

Backup, restore, migration and disaster recovery restore authoritative state but never become authority themselves.

The update chain is:

`User Confirmation → Eligibility → Integrity → Compatibility → Provenance → Authorization → Secure Install → Health Verification → Activation → Rollback/Recovery if required`

RAUC is the target atomic update mechanism. Production OTA authority remains MediaHub-owned.

## 10. Qualification consequence

Functional Baseline 1.0 is not equivalent to production authorization.

The implementation sequence remains:

`Passport → Capability Reconciliation → Contract Reconciliation → Architecture Reconciliation → Implementation → Unit → Integration → Negative Path → Security/Regression → Independent Review → MH-05/T5/F-03 → Release Authorization → Production Authorization`

AI/autonomous development cannot self-authorize independent qualification, release or production.

## 11. Immediate engineering priority

The next implementation-planning wave must reconcile, in order:

1. Security / Identity / Trust / Authorization.
2. Recovery Authority / Backup / Restore.
3. Update Authority / RAUC / supply-chain evidence.
4. Home Assistant Core integration boundary.
5. Media / Document / Digital Twin / Engineering contracts.
6. AI Gateway and escalation policy.
7. Mobile Core and Remote contracts.
8. Cluster and Cloud Development boundaries.
9. Qualification matrix covering every passport capability.

No new infrastructure dependency should be added merely to satisfy an implementation preference. A component enters the runtime only after a demonstrated capability gap, license/security/provenance review, integration boundary, benchmark where applicable, and acceptance tests.
