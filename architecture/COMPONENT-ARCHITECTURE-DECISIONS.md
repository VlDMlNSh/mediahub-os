# MediaHub OS — Component Architecture Decisions

Date: 2026-09-11
Status: ACCEPTED BASELINE
Registry: `components/COMPONENT-REGISTRY.yaml`

## Governing decision

MediaHub does not adopt complete third-party products by default. Third-party projects are evaluated as sources of stable implementation blocks, protocols, schemas, algorithms, lifecycle semantics and interoperability patterns.

MediaHub retains ownership of:

- domain model;
- State Authority;
- event semantics;
- authorization policy;
- device model;
- update authority;
- recovery authority;
- release gates;
- production authorization.

## Selected foundational primitives

### Messaging — NATS

Use NATS/JetStream for asynchronous commands, events and durable streams. Define MediaHub subjects, schemas, idempotency and retry semantics independently.

### Coordination — etcd

Use etcd for quorum-sensitive coordination, leases, membership and distributed coordination. It is not the MediaHub State Authority.

### Persistence — PostgreSQL

Use PostgreSQL for transactional relational persistence. MediaHub owns schema and invariants.

### Contracts — Protobuf + gRPC

Use Protobuf for stable typed contracts and gRPC for synchronous internal RPC. NATS remains the preferred asynchronous transport.

### Observability — OpenTelemetry + Prometheus

Standardize telemetry before committing to a visualization vendor. Correlation IDs and trace context are mandatory across service boundaries.

### Secrets — SOPS + age

Production secrets/configuration are encrypted at rest. Plaintext production secrets must never be committed to Git.

### Backup — restic

Use encrypted snapshot/deduplication/restore mechanics. Backup success is insufficient without periodic restore verification.

### Supply chain — Syft + Cosign + Trivy

Every release candidate must have an SBOM, artifact signature and security scan evidence. Deployment must verify the release artifact before execution.

### Media — FFmpeg

Use FFmpeg as a controlled media-processing primitive. Codec/build configuration is pinned and resource-limited.

## Reference-only projects

Temporal, Caddy, Jellyfin, SeaweedFS, Paperless-ngx, Immich, RAUC and Mender are reference implementations. Their concepts may be incorporated when they improve MediaHub, but they do not become implicit architectural dependencies.

## Explicit exclusions from the foundational stack

Redis, Kafka and Kubernetes are not foundational dependencies at this stage. They may be reconsidered only after measured requirements demonstrate that the selected primitives cannot satisfy MediaHub acceptance criteria.

## Acceptance gate for future components

A new dependency may enter `selected` status only when all are satisfied:

1. clear functional benefit to MediaHub;
2. no redundant subsystem already covering the requirement;
3. compatible license and distribution model;
4. active upstream or justified long-term maintenance path;
5. security review completed;
6. failure/degraded-mode behaviour defined;
7. upgrade and rollback path defined;
8. deterministic acceptance tests exist;
9. no violation of State Authority ownership;
10. dependency can be removed or replaced without architectural collapse.

## Review rule

Component selection is not permanent. Each major release reviews upstream health, security advisories, license changes, dependency drift and whether the component still materially improves MediaHub.
