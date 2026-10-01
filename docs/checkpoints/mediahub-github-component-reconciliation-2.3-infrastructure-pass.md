# MediaHub OS — GitHub Component Reconciliation 2.3 / Storage · Network · Workflow · Supply Chain · Developer Fabric

Date: 2026-10-01
Parent: docs/checkpoints/mediahub-github-component-reconciliation-2.2-knowledge-engineering-ai-pass.md
Status: QUALIFIED INFRASTRUCTURE DEEP-PASS

## 1. Storage

### S3-compatible object storage — SELECTED INTERFACE
MediaHub defines the object-storage contract; implementation remains replaceable.

### SeaweedFS — TARGET-GATED IMPLEMENTATION
Repository: https://github.com/seaweedfs/seaweedfs
Use: distributed object/file/S3 storage.
Boundary: storage mechanics only; MediaHub owns object identity, lifecycle, retention, policy and recovery authority.
Gate: durability, erasure coding/replication, backup/restore, failure domains, security, performance, upgrade/rollback.

### restic — RETAIN / TARGET-GATED
Repository: https://github.com/restic/restic
Use: backup/restore mechanics.
Boundary: backup is not authority. Recovery acceptance is controlled by MediaHub qualification.
Gate: restore tests, corruption tests, retention, encryption, key recovery and cross-node recovery.

### Syncthing — REFERENCE / CONDITIONAL
Repository: https://github.com/syncthing/syncthing
Use: peer file synchronization.
Rule: never use as canonical State Authority replication. Activate only for non-authoritative file synchronization.

### Btrfs / OpenZFS — REFERENCE / PLATFORM
Filesystem/storage-platform choices only. Neither becomes MediaHub domain authority.

## 2. Network

### WireGuard — REFERENCE / PLATFORM PRIMITIVE
Repository: https://github.com/WireGuard/wireguard-go
Important: GitHub repository is a mirror; official upstream is referenced by that repository.
Use: cryptographic tunnel primitive where explicitly required.
Boundary: does not replace CPRG semantics or MediaHub identity/policy.

### Caddy — REFERENCE / TARGET-GATED EDGE
Repository: https://github.com/caddyserver/caddy
Use: HTTP/HTTPS reverse proxy/edge mechanics.
Boundary: TLS/HTTP transport only; not identity, authorization or policy authority.
Gate: routing, certificate lifecycle, auth integration, failure and reload behavior.

No second network control plane is added by default.

## 3. Workflow / messaging

### Temporal — FUTURE-GATED
Repository: https://github.com/temporalio/temporal
Use: durable workflow execution.
Decision: no default deployment until MediaHub/Astra demonstrates a workflow durability gap that cannot be met by MediaHub-owned control logic.
Reason: introducing Temporal early creates another durable workflow state subsystem.

### NATS JetStream — FUTURE-GATED
Repository: https://github.com/nats-io/nats-server
Use: asynchronous messaging/streams.
Decision: no default message broker. Activate only for proven decoupling/stream throughput requirements.
Rule: messages/events are not canonical state.

### etcd — FUTURE-GATED
Repository: https://github.com/etcd-io/etcd
Use: leases/membership/coordination.
Decision: no default second coordination authority. Activate only for a specific coordination gap that cannot be implemented inside the existing MediaHub State Authority model.
Rule: never store MediaHub domain state in etcd.

## 4. Supply chain / artifacts

### Cosign — SELECTED
Repository: https://github.com/sigstore/cosign
Artifact signing/verification.

### Syft — SELECTED
Repository: https://github.com/anchore/syft
SBOM generation.

### Trivy — SELECTED
Repository: https://github.com/aquasecurity/trivy
Vulnerability/secrets/filesystem scanning.

### Harbor — TARGET-GATED REGISTRY
Repository: https://github.com/goharbor/harbor
Use: self-hosted OCI artifact/container registry.
Decision: target interface, not mandatory foundation dependency.
Gate: registry need, identity, signing/verification, retention, backup/restore and operational burden.

### Kubernetes / K3s — REFERENCE ONLY
Repositories: https://github.com/kubernetes/kubernetes ; https://github.com/k3s-io/k3s
Decision: orchestration is not a MediaHub prerequisite. Do not force Kubernetes into the architecture merely to deploy sidecars.

### Argo CD — REFERENCE ONLY
Repository: https://github.com/argoproj/argo-cd
Decision: no second deployment authority. MediaHub retains update/release authority.

### RAUC — RETAIN / TARGET-GATED UPDATE MECHANISM
Repository: https://github.com/rauc/rauc
Decision: atomic embedded-Linux update mechanism where platform qualification permits.
Boundary: MediaHub remains lifecycle/update authority.

## 5. Developer Fabric

Developer Fabric remains a corporate development domain and is not user-data infrastructure.

Selected implementation principles:
- heterogeneous Linux/macOS developer nodes;
- at least one macOS node for iOS development;
- dynamic Primary Development Node;
- capability-based scheduling;
- HIGH_SPEED developer fabric where qualified;
- request-scoped, lease-based compute contribution;
- isolation between developer workloads and Media Data Plane;
- no raw user data;
- artifact provenance and signed outputs;
- CI/CD remains under MediaHub/corporate release authority.

No orchestration platform is made mandatory. The fabric may use native processes, containers or a future qualified orchestrator behind MediaHub-owned scheduling/contracts.

## 6. Infrastructure non-adoption

No new default foundation dependency for:
- second object store;
- second backup system;
- general-purpose VPN gateway;
- mandatory reverse-proxy authority;
- default workflow engine;
- default message broker;
- default distributed KV store;
- mandatory Kubernetes/K3s;
- second deployment authority.

## 7. Result

Storage:
S3 interface + PostgreSQL/object contracts foundation; SeaweedFS and restic target-gated; Syncthing/filesystems conditional/reference.

Network:
MediaHub network contracts remain authoritative; WireGuard/Caddy are mechanisms, not authorities.

Workflow:
Temporal/NATS/etcd remain future-gated.

Supply chain:
Cosign/Syft/Trivy selected; Harbor target-gated; Kubernetes/K3s/Argo CD reference only; RAUC target-gated.

Developer Fabric:
architecture is closed; implementation should remain lightweight and capability-driven, with macOS/iOS development support and no user-data mixing.

No architecture change was made.
