# MediaHub OS 11.x LTS / MediaHub iOS
# Functional Baseline 1.0 — Architecture Reconciliation

Date: 2026-09-11
Status: PROPOSED RECONCILIATION ARTIFACT
Source: FUNCTIONAL BASELINE 1.0 + MH-03 + component architecture records

## 1. Purpose

Reconcile the accepted functional target with the existing MH-03 runtime foundation and component architecture without silently changing frozen decisions.

## 2. Governing hierarchy

1. Functional Baseline 1.0 defines the product capability target.
2. Frozen MH-03/P0 decisions constrain the current runtime.
3. Future target capabilities that conflict with the current foundation require an explicit governance and acceptance gate.
4. Third-party components never become MediaHub authority merely by being selected.
5. R4 immutable baseline remains unchanged.

## 3. Current architecture state

CURRENT / FROZEN FOUNDATION:
- single node;
- in-memory MediaHub State Authority;
- no HA;
- no physical persistence;
- deterministic local operation without mandatory Internet/cloud/external AI/RAG/paid APIs;
- no fallback State Authority;
- command/event authority path remains canonical.

MH-03 is still PROPOSED and therefore is not represented as production-authorized architecture. Its acceptance criteria require authority-path, lifecycle, failure/degraded-mode, security, historical reconciliation and contradiction review.

## 4. Target architecture state

TARGET / FUTURE-GATED extensions:
- PostgreSQL + pgvector persistence;
- S3-compatible object storage;
- backup/restore and DR;
- RAUC-based atomic update mechanism;
- HA/cluster compute;
- Local Cluster AI;
- Cloud Development AI boundary;
- MediaHub Core iOS/iPadOS;
- MediaHub iOS Remote;
- Documents;
- Digital Twin;
- Engineering;
- qualified Smart Home integration with Home Assistant Core.

These are not implicitly active in the current runtime.

## 5. Canonical authority graph

```text
                 MediaHub Release / Production Governance
                                  |
                         MediaHub Update Authority
                                  |
                        MediaHub Recovery Authority
                                  |
                         MediaHub State Authority
                                  |
                         MediaHub Domain Contracts
              +-------------------+--------------------+
              |                   |                    |
       Smart Home Domain      Media Domain       Other MediaHub Domains
              |                   |                    |
      Home Assistant Core     FFmpeg/OpenCV       Domain adapters

AI / Mobile / Cloud / Voice / External Devices
                 |
                 v
          Governed MediaHub Contracts
                 |
                 v
          Canonical authority path
```

Home Assistant Core is authoritative only inside the Smart Home domain. It does not become platform State Authority. Database, broker, coordination, AI, cloud, mobile and backup components are non-authoritative infrastructure or capability layers.

## 6. Component classification

| Component | Current role | Target role | Activation |
|---|---|---|---|
| PostgreSQL | not active | transactional persistence | future-gated |
| pgvector | not active | vector capability inside PostgreSQL | future-gated/benchmark |
| NATS/JetStream | not active | asynchronous transport if gap proven | future-candidate |
| etcd | not active | HA/cluster coordination if required | future-candidate |
| Protobuf/gRPC | contract primitives | typed service contracts | governed adoption |
| OpenTelemetry/Prometheus | observability foundation | telemetry/metrics | governed adoption |
| SOPS/age | configuration/secret primitives | encrypted deployment material | governed adoption |
| restic | not active as authority | backup mechanics | future-gated |
| RAUC | not active as authority | update mechanism | future-gated |
| Cosign/Syft/Trivy | release evidence primitives | release/security gates | governed adoption |
| FFmpeg | media primitive | isolated media processing | governed adoption |
| Home Assistant Core | not active in MH-03 foundation | Smart Home domain authority | target/qualification |
| Temporal | reference | durable workflow candidate | capability-gap gate |
| K3s/Kubernetes | excluded as prerequisite | optional cluster infrastructure | conditional P1 |
| Mender | reference | no production OTA authority | reference-only |

## 7. Architecture contradictions and disposition

### A01 — PostgreSQL vs in-memory State Authority

Disposition: NOT a defect. PostgreSQL is a future persistence mechanism. It cannot become active until persistence architecture, migration, rollback, recovery and acceptance gates pass.

### A02 — NATS/etcd vs single-node foundation

Disposition: GOVERNANCE-GATED. Existing component records that describe NATS/etcd as foundational must be interpreted as target architecture, not current runtime prerequisites. No activation before the HA/event-scale capability gap is demonstrated and accepted.

### A03 — Home Assistant Core vs MediaHub State Authority

Disposition: RESOLVED BY DOMAIN SEPARATION. Home Assistant Core owns Smart Home domain state; MediaHub owns platform state. MediaHub Smart Home Layer is the integration boundary.

### A04 — RAUC vs MediaHub Update Authority

Disposition: RESOLVED BY SEPARATION. RAUC provides update mechanics; MediaHub owns policy, authorization, provenance, activation and rollback semantics.

### A05 — restic vs Recovery Authority

Disposition: RESOLVED BY SEPARATION. restic provides backup mechanics; MediaHub owns backup policy, manifests, verification and restore orchestration.

### A06 — AI/cloud/mobile mutation paths

Disposition: RESOLVED BY CONTRACT RE-ENTRY. All state-changing actions re-enter the governed command path. AI/cloud/mobile cannot create an alternate authority.

### A07 — Observability as dependency

Disposition: RESOLVED. Health/telemetry are observational and cannot become canonical domain state or direct mutation paths.

### A08 — Reference products becoming hidden dependencies

Disposition: PROHIBITED. Jellyfin, Immich, Paperless-ngx, Temporal, Mender and other reference projects cannot silently become required runtime authorities/dependencies.

## 8. Lifecycle reconciliation

The existing MH-03 lifecycle remains:

`ABSENT → INITIALIZING → STARTING → READY ↔ DEGRADED/RECOVERING → STOPPING → STOPPED`

Target components must enter this lifecycle through explicit dependency classification. A future-gated component cannot be classified as critical for the current deterministic core before its architecture gate passes.

## 9. Recovery reconciliation

Recovery remains bounded lifecycle authority. It may detect, isolate, restart/reinitialize and verify capabilities, but it cannot mutate canonical state outside State Authority or create a shadow authority.

Target backup/restore/DR mechanisms must preserve this invariant.

## 10. Architecture dependency rule

A dependency may become active only after:

`Capability Gap → Architecture Contract → Authority Boundary → License/Security/Provenance Review → Failure/Degraded Model → Acceptance Tests → Qualification → Activation`

A component may be removed or replaced without architectural collapse.

## 11. Remaining architecture gates

1. Accept/freeze MH-03 after its stated acceptance criteria are satisfied.
2. Formal persistence architecture gate for PostgreSQL/pgvector/object storage.
3. Formal HA/cluster architecture gate for etcd/NATS and distributed compute.
4. Smart Home integration qualification with Home Assistant Core.
5. Security/Identity/Trust architecture gate.
6. Recovery/backup/restore architecture gate.
7. Update/RAUC/supply-chain architecture gate.
8. AI Gateway/local-cluster/cloud boundary gate.
9. Mobile Core/Remote architecture gate.
10. Domain contracts for Media/Documents/Digital Twin/Engineering/Network.

## 12. Release status

Architecture Reconciliation does not authorize implementation completion, release or production. Release remains LOCKED. Production remains NOT AUTHORIZED until the independent qualification chain is completed.

## 13. Conclusion

No architectural replacement of the MediaHub State Authority is required. The principal remaining work is controlled evolution from the current single-node/in-memory foundation to the passport target architecture through explicit gates, while preserving domain authority separation and fail-closed behavior.
