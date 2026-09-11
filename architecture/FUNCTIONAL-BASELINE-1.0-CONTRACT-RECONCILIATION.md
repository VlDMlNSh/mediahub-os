# MediaHub OS 11.x LTS / MediaHub iOS
# Functional Baseline 1.0 — Contract Reconciliation

Date: 2026-09-11
Status: ACCEPTED RECONCILIATION ARTIFACT
Source: FUNCTIONAL BASELINE 1.0 + current MH-03 foundation

## Purpose

This document reconciles the Functional Baseline with the existing MH-03 authority, command, event, recovery and runtime contracts before implementation.

## Governing rule

Every capability follows:

`Capability → Contract → Authority → Adapter/Runtime → Validation → Qualification`

No capability may introduce an implicit mutation path.

## Canonical execution contract

`Command → Validation → Authorization/Policy → Consumer Contract → State Authority → Canonical Mutation → Event → Observers`

This remains the only platform mutation path.

## Event contract

`Event = fact that something happened.`

Events are observational/coordination artifacts. They do not grant mutation authority. Any event-driven state change must generate a governed Command and re-enter the canonical command path.

## Authority reconciliation

| Area | Authority | Non-authority dependencies |
|---|---|---|
| Platform state | MediaHub State Authority | DB, cache, broker, cloud, AI |
| Smart Home | Home Assistant Core | MediaHub UI/API/AI |
| Security/trust | MediaHub Security/Trust Layer | SOPS, age, OpenBao, identity adapters |
| Media | MediaHub Media Domain | FFmpeg, OpenCV, external endpoints |
| Documents | MediaHub Document Domain | OCR/index/storage primitives |
| Digital Twin | MediaHub Digital Twin Domain | IFC/geometry runtimes |
| Engineering | MediaHub Engineering Domain | calculation/tool adapters |
| Network | MediaHub Network Domain | vendor APIs |
| AI execution | MediaHub AI Gateway | local/cluster/cloud runtimes |
| Recovery | MediaHub Recovery Authority | restic and storage backends |
| Update | MediaHub Update Authority | RAUC and supply-chain evidence |
| Observability | MediaHub Observability Policy | OTel/Prometheus |
| Release | MediaHub Release Governance | Cosign/Syft/Trivy/CI |

## Current-foundation reconciliation

The current MH-03 runtime foundation remains:

- single node;
- in-memory State Authority;
- no HA;
- physical persistence not authorized;
- deterministic local operation without mandatory cloud/Internet/AI/RAG;
- no fallback authority.

Therefore the passport's persistence, HA, cluster and durable recovery capabilities are target phases, not implicit changes to the current foundation.

## Contract requirements by capability

### State Authority

Must define command envelope, validation result, authorization context, mutation transaction semantics, event emission, version/concurrency semantics, provenance and audit linkage.

### Smart Home

Must define normalized device/entity representation, integration identity, capability model, command mapping, event mapping, discovery/onboarding lifecycle and failure semantics while preserving Home Assistant Core as Smart Home authority.

### Security / Trust

Must define identity, authentication, authorization, capability/scope, device trust, quarantine, revocation, credential rotation, audit and egress policy.

### Media

Must define asset identity, source/endpoint identity, codec/capability negotiation, playback intent, processing job contract, resource limits and provenance.

### Documents

Must define document identity, ingestion, OCR artifact provenance, metadata, indexing, retention and access-control semantics.

### Digital Twin / Engineering

Must define model/project identity, IFC/geometry provenance, deterministic processing, entitlement, calculation artifact provenance and audit.

### AI

Must define task identity, model identity/provenance, tool permissions, data classification, escalation policy, result provenance and re-entry into the canonical command path for mutations.

### Cloud

Must define egress request, authorization, data classification, residency, workload identity, quotas, metering, revocation and local fallback.

### Mobile

Must define session/device identity, authorization, contract versioning, offline operation, synchronization/conflict behavior, revocation and distinction between Core and Remote applications.

### Recovery

Must define backup manifest, snapshot identity, integrity evidence, restore plan, migration semantics, recovery authorization and post-restore reconciliation. Recovery must restore authority, never become authority.

### Update

Must define user confirmation, eligibility, artifact identity, provenance, signature verification, compatibility, activation, health gate and rollback. RAUC is the target mechanism; MediaHub remains update authority.

### Observability

Must define correlation IDs, trace/metric/log linkage, privacy/redaction, retention and failure semantics. Telemetry remains non-authoritative.

## Reconciliation findings

1. No second platform State Authority is required.
2. Home Assistant Core and MediaHub State Authority have distinct domains and must not be merged.
3. PostgreSQL is a target persistence primitive, not current runtime authority until the persistence gate passes.
4. NATS/etcd are future candidates and cannot be runtime prerequisites of the frozen foundation.
5. Recovery and OTA have policy authorities owned by MediaHub; external tools provide mechanics only.
6. AI, mobile and cloud actions must re-enter governed contracts.
7. Reference products cannot become hidden runtime dependencies.
8. Storage/search overlap requires benchmark evidence before adding another authority.

## Remaining contract gaps

Before implementation of each target subsystem, the following must be specified and tested:

- canonical schemas;
- command/event envelopes;
- versioning and compatibility;
- identity and authorization context;
- idempotency and concurrency semantics;
- failure/degraded behavior;
- provenance/audit linkage;
- recovery semantics;
- acceptance tests;
- qualification evidence.

## Gate

Contract Reconciliation is complete only when every Functional Baseline capability has an explicit contract, authority, boundary, failure model and qualification mapping. Until then, Release remains LOCKED and Production remains NOT AUTHORIZED.
