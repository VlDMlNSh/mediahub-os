# MediaHub OS — Component Integration Boundary

Date: 2026-09-11
Status: ACCEPTED ARCHITECTURAL BASELINE

## Purpose

Define exactly where selected open-source primitives may participate in MediaHub without transferring architectural ownership to third-party products.

## Authority hierarchy

```text
MediaHub Release / Production Authority
                |
        MediaHub Update Authority
                |
        MediaHub Recovery Authority
                |
         MediaHub State Authority
                |
       MediaHub Domain Model
                |
   +------------+-------------+
   |            |             |
 PostgreSQL    etcd          NATS/JS
   |            |             |
 durable     coordination   async transport
 relational
 state
```

No infrastructure component may become the source of truth for MediaHub domain semantics.

## Integration boundaries

### PostgreSQL

Owns transactional relational persistence. MediaHub owns schema, migrations, invariants, retention and transaction boundaries.

### etcd

Owns infrastructure coordination primitives only: leases, membership, quorum-sensitive coordination and leader-election support. No user/domain state is authoritative in etcd.

### NATS / JetStream

Owns message transport and durable stream mechanics. MediaHub owns event names, schemas, ordering requirements, idempotency keys, retry policy and consumer semantics. Messages are not the authoritative database.

### Protobuf / gRPC

Protobuf defines versioned typed contracts. gRPC provides synchronous service transport. Generated code is an implementation artifact, not the domain model.

### OpenTelemetry / Prometheus

Telemetry is observational and never authoritative. Loss of telemetry must not alter business state or command semantics.

### SOPS / age

Used for encrypted configuration and secret material. Runtime components receive only the minimum required plaintext material at runtime.

### restic

Provides backup mechanics. MediaHub owns backup policy, manifests, retention, verification and disaster-recovery orchestration. A successful backup command is not evidence of recoverability until restore verification succeeds.

### Syft / Cosign / Trivy

These form release evidence gates. SBOM generation, artifact signing/verification and vulnerability scanning are mandatory for release qualification. Scanner output does not replace human or policy-based risk decisions.

### FFmpeg

Isolated media-processing primitive. Inputs, outputs, codec set, CPU/memory limits, timeout and process isolation are controlled by MediaHub.

## Runtime dependency rule

A selected component must satisfy:

- pinned version or reproducible release reference;
- explicit security review;
- explicit failure/degraded-mode semantics;
- deterministic health checks;
- upgrade and rollback procedure;
- acceptance tests;
- documented removal/replacement path.

## Forbidden coupling

The following are architectural violations:

- using NATS as the authoritative domain database;
- using etcd as the MediaHub domain database;
- making telemetry a runtime prerequisite for correctness;
- exposing third-party product data models as MediaHub public contracts;
- making a reference-only application a hidden runtime dependency;
- allowing an OTA component to bypass MediaHub Update Authority;
- allowing backup tooling to define recovery authority;
- allowing generated Protobuf/gRPC types to become the domain model;
- introducing a second subsystem that duplicates an existing selected primitive without measured justification.

## Decision rule for future dependencies

Prefer an existing selected primitive unless a new dependency demonstrates a measurable improvement in at least one of: correctness, security, recoverability, performance, interoperability or operational simplicity, while not increasing unacceptable architectural complexity.
