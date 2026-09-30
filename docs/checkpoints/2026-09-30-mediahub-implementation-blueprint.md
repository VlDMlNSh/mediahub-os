# MediaHub Implementation Blueprint

Date: 2026-09-30
Status: architecture-to-implementation baseline
Scope: implementation preparation only; no production deployment

## 1. Target architecture

MediaHub is a hierarchical system with two deployment domains:

- Local MediaHub Cluster: user-facing LAN/P2P media, storage, compute and wireless-coverage extension.
- Cloud Development Cluster: developer/company infrastructure, CI/CD, engineering storage, Astra and distributed development compute.

A MediaHub node may contribute idle CPU/GPU/NPU capacity to the developer compute fabric without becoming a permanent cloud-cluster member and without granting developer access to personal data.

Hard separation:

Compute Contribution != User Data Access != Developer Personnel Access

CPRG is a separate logical authority for request-scoped API-key registration. Its VPN capability is registration-only and must never become general transit.

## 2. Plane model

1. Control Plane
   - GitHub
   - Astra
   - durable commands/results
2. Identity Plane
   - node identity
   - CPRG authority identity
   - developer infrastructure identity
3. Authorization Plane
   - deterministic policy decision
   - workload class
   - capability checks
   - lease checks
   - privacy/data-class checks
4. Compute Contribution Plane
   - capability advertisement
   - admission
   - lease
   - job dispatch
   - execution
   - result/evidence
   - revocation
5. Developer Mesh
   - management/discovery only
   - encrypted
   - direct P2P preferred
6. Media Data Plane
   - direct LAN/P2P
   - never routed through CPRG
7. Storage Fabric
   - local-cluster storage
   - developer-cluster engineering storage
8. Protected Registration Plane
   - MediaHub -> CPRG -> exact provider registration endpoint
   - request scoped
   - short lease
   - fail closed

## 3. Recommended component decomposition

### Compute scheduler/executor

Primary candidate: Ray.

Use Ray as the execution substrate for developer workloads:
- tasks for stateless partitionable work;
- actors for stateful workers;
- object store for bounded intermediate results;
- cluster resource labels for CPU/GPU/NPU classes.

Do not make Ray the security authority. MediaHub owns admission, identity, lease and privacy policy; Ray receives only already-admitted work.

Secondary candidate: Nomad.

Use Nomad only if we need a general-purpose non-Python workload orchestrator or VM/container/executable scheduling. Its current repository license is BUSL-1.1, so legal/licensing review is required before embedding or distributing it as a product dependency.

### Identity

Primary design candidate: SPIFFE/SPIRE patterns.

Reuse:
- workload identity abstraction;
- short-lived identities;
- attestation concept;
- trust bundles;
- rotation;
- mTLS/JWT proof where appropriate.

Do not force SPIRE into every MediaHub node in v1. First define MediaHub's identity contract independently, then map it to SPIFFE/SPIRE where operationally justified.

### Authorization

Primary implementation direction: a small deterministic MediaHub policy layer for v1.

OpenFGA is a strong later component for relationship-based authorization when policy relationships become complex:
- node -> cluster;
- node -> capability;
- principal -> workload;
- workload -> data class;
- service -> operation.

Do not make OpenFGA the only gate for safety-critical lease/routing invariants. Local enforcement must remain deny-by-default even if an external authorization service is unavailable.

### Messaging / control bus

Primary candidate: NATS + JetStream.

Use it for:
- job offers;
- job leases;
- heartbeats;
- result notifications;
- capability updates;
- revocation propagation;
- durable control events.

Semantics:
- at-least-once transport;
- explicit message IDs;
- application idempotency;
- bounded redelivery;
- dead-letter/quarantine path;
- no claim of magical exactly-once execution.

Critical state transitions remain persisted in the authoritative control store; NATS is transport/event infrastructure, not State Authority.

### Development Mesh

Primary candidate: Netmaker/WireGuard.

Use only for the Development Mesh:
- developer nodes;
- cluster management;
- service discovery;
- private control traffic.

Do not use it for:
- ordinary MediaHub media traffic;
- local storage traffic;
- CPRG general routing;
- default Internet egress.

The implementation must explicitly enforce split routing and default-deny access between planes.

### Storage

Primary candidate: SeaweedFS for developer/cluster storage experiments.

Useful architectural pieces:
- master/volume/filer separation;
- node-local disk scaling;
- S3-compatible interface;
- replication;
- incremental scale-out.

Do not make SeaweedFS the first dependency of the compute-contribution PoC. Compute and storage must be qualified independently.

### Observability

Use OpenTelemetry-compatible concepts for:
- trace ID;
- span ID;
- job/request correlation;
- state-transition evidence;
- latency/error metrics.

Never emit:
- API keys;
- private keys;
- personal media payloads;
- raw provider payloads;
- unrestricted filesystem paths from user data.

## 4. MediaHub-owned protocol layer

External components are subordinate to MediaHub contracts.

Canonical objects:

### NodeCapability
- node_id
- capability_epoch
- cpu
- gpu
- npu
- memory
- local_storage_class
- runtime_classes
- isolation_classes
- network_classes
- availability
- max_concurrent_jobs
- contribution_policy
- attestation_reference
- expires_at

### WorkloadSpec
- job_id
- workload_class
- origin
- privacy_class
- locality
- required_capabilities
- resource_limits
- execution_deadline
- lease_max
- network_policy
- input_policy
- output_policy
- contributor_eligibility
- partitioning_contract
- deterministic/idempotency contract

### AdmissionDecision
- decision_id
- job_id
- node_id
- policy_version
- capability_match
- privacy_decision
- resource_decision
- lease
- authority_epoch
- reason_code
- expires_at
- signature/reference

### ComputeLease
- lease_id
- job_id
- node_id
- issued_at
- expires_at
- resource_limits
- network_scope
- data_scope
- cancellation_token
- authority_epoch

### ExecutionEvidence
- job_id
- lease_id
- node_id
- start/end
- execution_state
- resource_usage
- output_digest
- evidence_digest
- failure_class
- revocation_state

## 5. Canonical compute protocol

Capability publication:
NODE -> CAPABILITY_ADVERTISEMENT -> CONTROL

Admission:
SCHEDULER -> ADMISSION_REQUEST -> POLICY
POLICY -> ADMISSION_DECISION

Lease:
SCHEDULER -> LEASE_ISSUE -> NODE
NODE -> LEASE_ACK

Execution:
SCHEDULER -> JOB_DISPATCH
NODE -> JOB_ACCEPTED
NODE -> HEARTBEAT*
NODE -> RESULT
NODE -> EVIDENCE
NODE -> LEASE_CLOSED

Failure:
any invalid/stale/revoked state -> DENIED or CLOSED

Revocation:
AUTHORITY -> LEASE_REVOKED
NODE -> EXECUTION_TERMINATED
NODE -> LEASE_CLOSED

No execution may begin without:
identity + admission + capability match + active lease + privacy decision.

## 6. Developer privacy boundary

Default policy:
- developer workloads may execute on contributed MediaHub compute;
- personal data remains local;
- user-originated workloads use local execution whenever feasible;
- only minimum transformed/bounded input may cross the boundary;
- contributor runtime cannot enumerate user storage or local network;
- developer personnel have no data-plane access;
- evidence contains metadata/digests, not personal payloads.

If a job requires raw personal data and the privacy boundary cannot be preserved, it remains local or is denied.

## 7. Execution isolation contract

A contributed node must expose a dedicated worker runtime.

Minimum v1:
- separate Unix user;
- dedicated working directory;
- resource limits;
- bounded filesystem mounts;
- no host filesystem mount;
- no access to MediaHub storage namespaces;
- outbound network deny-by-default;
- explicit allowed destinations;
- process tree cleanup on lease close;
- hard timeout;
- cancellation;
- result size limit.

Container/OCI isolation may be used where available. It is an implementation mechanism, not the security contract.

## 8. Scheduler model

Scheduler separates:
- placement decision;
- authorization decision;
- execution mechanism.

Placement inputs:
- workload class;
- CPU/GPU/NPU;
- memory;
- locality;
- network;
- privacy;
- contributor eligibility;
- lease;
- expected transfer cost;
- node health.

Preferred placement:
1. local when locality/privacy/latency requires it;
2. developer servers for company workloads;
3. admitted contributed MediaHub capacity;
4. distributed partitioning when the workload is explicitly partitionable.

The scheduler must never silently move a LOCAL_ONLY workload to cloud or contributed nodes.

## 9. CPRG implementation boundary

CPRG accepts exactly one operation family in v1:

api_key_registration

Authorization tuple:

(node_identity, request_id, operation, provider, destination, lease, credential_scope, authority_epoch)

Required state:

REQUESTED
-> AUTHENTICATED
-> POLICY_APPROVED
-> LEASE_ACTIVE
-> TUNNEL_ACTIVE
-> REGISTRATION_IN_PROGRESS
-> REGISTRATION_VERIFIED
-> CLOSED

Any failure converges to CLOSED after lease creation.

CPRG has:
- no MediaHub storage;
- no Astra;
- no CI runner;
- no developer compute;
- no general VPN gateway;
- no default route;
- no unrestricted provider API access.

## 10. State authority rules

Astra/GitHub:
- command/result coordination.

MediaHub control store:
- authoritative job/lease/admission state.

NATS:
- transport and durable event stream.

Ray:
- execution substrate.

Netmaker/WireGuard:
- encrypted development connectivity.

SeaweedFS:
- storage substrate.

OpenFGA:
- optional authorization substrate.

SPIRE:
- optional identity substrate.

No external component becomes State Authority by convenience.

## 11. Evidence-first implementation sequence

Wave 1 — pure deterministic protocol
- typed schemas;
- state machines;
- admission;
- capability matching;
- lease;
- revocation;
- idempotency;
- evidence.

Wave 2 — isolated local worker
- real process execution;
- resource limits;
- filesystem/network boundary;
- cancellation;
- evidence.

Wave 3 — scheduler simulation
- heterogeneous nodes;
- placement;
- partitioning;
- failure;
- stale capability;
- lease expiry.

Wave 4 — NATS transport
- durable events;
- dedupe;
- retry;
- DLQ/quarantine;
- reconnect behavior.

Wave 5 — identity integration
- MediaHub node identity;
- short-lived workload identity mapping;
- rotation/revocation.

Wave 6 — Development Mesh
- Netmaker/WireGuard PoC;
- direct P2P;
- ACLs;
- split routing;
- negative routing tests.

Wave 7 — real contributed compute
- one MediaHub contributor;
- one developer node;
- one bounded workload;
- no user data.

Wave 8 — multi-node distributed compute
- two or more contributors;
- partitionable job;
- partial results;
- deterministic merge;
- node loss/retry.

Wave 9 — storage
- independent SeaweedFS qualification;
- data locality;
- replication;
- recovery.

Wave 10 — CPRG
- protocol implementation only after trust/identity decisions close;
- negative routing tests;
- replay;
- lease teardown;
- emergency kill;
- migration/recovery.

Wave 11 — end-to-end qualification
- local -> admission -> contributor -> execution -> result -> evidence;
- privacy boundary;
- failure recovery;
- audit;
- performance.

## 12. Acceptance gates

A compute contributor is qualified only if:
- identity verified;
- capabilities verified;
- admission explicit;
- lease enforced;
- isolation verified;
- user storage inaccessible;
- local network inaccessible except declared endpoints;
- lease expiry terminates work;
- revocation terminates work;
- result bounded;
- evidence independently verifiable.

A scheduler is qualified only if:
- LOCAL_ONLY never escapes local domain;
- privacy-incompatible jobs are denied;
- stale capabilities are rejected;
- expired leases cannot execute;
- duplicate dispatch is idempotent;
- node loss does not corrupt authoritative state;
- partitioned jobs have deterministic merge semantics.

CPRG is qualified only if:
- exact operation is enforced;
- exact destination is enforced;
- no general routing exists;
- replay is rejected;
- lease closes;
- credentials do not leak;
- migration has one active authority;
- emergency kill works;
- MediaHub data plane remains operational.

## 13. First implementation interfaces

The first code should expose stable interfaces rather than immediately adopting all external systems:

- NodeIdentityProvider
- CapabilityProvider
- AdmissionPolicy
- LeaseAuthority
- JobScheduler
- ExecutionBackend
- ResultVerifier
- EvidenceSink
- EventBus
- RoutingPolicy
- PrivacyPolicy
- CPRGRegistrationAdapter

Every interface must have:
- deterministic test implementation;
- failure semantics;
- explicit authority boundary;
- versioned schema;
- no hidden global state.

## 14. GitHub component findings

The following repositories were inspected directly:

- ray-project/ray — distributed runtime with tasks, actors and objects; strong match for heterogeneous developer compute.
- hashicorp/nomad — general workload orchestrator with resource scheduling and GPU/device plugins; useful alternative, but current repository is BUSL-1.1.
- spiffe/spire — mature workload identity, attestation and short-lived SVID model; useful pattern/component for identity plane.
- openfga/openfga — Zanzibar-inspired relationship authorization with HTTP/gRPC, multiple storage backends and SDKs; useful when authorization relationships outgrow a local policy engine.
- nats-io/nats-server — secure distributed communications substrate suitable for control/event transport; JetStream semantics still require application idempotency.
- gravitl/netmaker — WireGuard network automation with ACLs and P2P/site-to-site capabilities; candidate only for Development Mesh.
- seaweedfs/seaweedfs — distributed file system with S3/POSIX/lakehouse interfaces and scale-out volume servers; candidate storage substrate.

Reference principle:
reuse stable primitives, not their entire control planes. MediaHub retains the authority contracts.

## 15. Immediate implementation target

Implement only the MediaHub-owned deterministic core first:

1. CapabilityAdvertisement schema.
2. WorkloadSpec schema.
3. AdmissionDecision schema.
4. ComputeLease state machine.
5. ExecutionEvidence schema.
6. AdmissionPolicy.
7. CapabilityMatcher.
8. LeaseAuthority.
9. Idempotency guard.
10. PrivacyPolicy.
11. deterministic scheduler simulator.
12. negative security tests.

Do not deploy Ray, Netmaker, SPIRE, NATS, SeaweedFS or CPRG yet.

The first external integration should be selected only after the deterministic contract passes.

## 16. Non-negotiable pushback encoded as architecture

- Do not call the aggregate system a literal single-machine supercomputer. It is a heterogeneous distributed compute fabric with different trust domains and network characteristics.
- Do not treat idle MediaHub compute as unrestricted remote shell access.
- Do not use a VPN as a general bridge between user and developer domains.
- Do not send user data to developer compute merely because compute capacity is available.
- Do not put provider credentials into node metadata.
- Do not make the scheduler a security authority.
- Do not make Ray/NATS/Netmaker/SeaweedFS/SPIRE/OpenFGA a replacement for MediaHub's own contracts.
- Do not promise exactly-once execution from message delivery alone.
- Do not begin production deployment before the deterministic security gates pass.


## 17.5 — Refined implementation stack after 13-pass review

Schema/tooling:
- Protobuf as candidate canonical wire representation.
- Buf for schema compilation, linting, generation and breaking-change gates.
- Protovalidate for semantic message validation.

Control transport:
- gRPC for bounded synchronous control calls with deadlines/cancellation.
- NATS/JetStream for asynchronous durable events and redelivery.

Execution:
- MediaHub-owned ExecutionBackend interface.
- Ray adapter for distributed developer workloads.
- containerd/OCI adapter for isolated Linux execution.

Identity/security:
- MediaHub identity contract first.
- SPIFFE/SPIRE mapping only where it reduces implementation risk.
- Cosign/Sigstore for artifact verification where applicable.

Network:
- MediaHub NetworkPolicy contract first.
- Development Mesh may use Netmaker/WireGuard.
- Execution-boundary enforcement may use Cilium/eBPF or another kernel policy mechanism where justified.

Observability:
- OpenTelemetry trace context and stable semantic conventions.
- Evidence remains MediaHub-owned.

Storage:
- authoritative state store remains an explicit design decision.
- SeaweedFS is an optional developer-storage adapter, not job state authority.

## 17.6 — Transactional state rule

Authoritative state transition:
validate -> transaction -> state commit -> durable outbox/event -> transport publication.

Never:
transport ACK -> assume state committed.

## 17.7 — Trust-to-isolation mapping

Workload trust determines minimum isolation class:

TRUSTED_ENGINEERING
-> process/OCI baseline

UNTRUSTED_ENGINEERING
-> stronger sandbox

HIGH_RISK_UNTRUSTED
-> microVM-capable execution class where available

Scheduler must reject placement when the node cannot satisfy the requested isolation class.

## 17.8 — Schema governance

Every protocol schema change must pass:
- formatting;
- lint;
- semantic validation;
- backward-compatibility check;
- security-policy review when semantics affect authorization.

Deleted Protobuf fields are reserved; enum values are not reused.

## 17.9 — Implementation sequence correction

Before any real Ray/NATS integration, implement:
1. protocol schemas;
2. validators;
3. authoritative state abstraction;
4. transactional outbox abstraction;
5. lease/fencing;
6. deterministic scheduler;
7. local isolated executor;
8. evidence verification.

Then integrate transports and external execution components.

