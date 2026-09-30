# MediaHub Compute Wire Protocol v1

Date: 2026-09-30
Status: normative architecture contract
Scope: Local MediaHub ↔ developer compute contribution plane
Production deployment: prohibited until qualification gates pass

## 1. Protocol principles

1. MediaHub-owned contracts are authoritative.
2. Transport is replaceable.
3. Every request is bound to identity, authority epoch, workload, node and lease.
4. Every state transition is monotonic.
5. Unknown fields must be ignored by receivers where the serialization format permits it.
6. Unknown enum values must fail closed when they affect authorization, routing, privacy or resource limits.
7. Duplicate delivery is expected.
8. Execution is at-least-once unless a workload explicitly defines stronger semantics.
9. User data and developer compute authorization are separate domains.
10. A node may contribute compute without exposing user storage or LAN services.

## 2. Versioning

Protocol identifier: mediahub.compute.v1

Each message carries:
- protocol_version
- message_type
- message_id
- correlation_id
- sent_at
- sender_id
- authority_epoch

Compatibility:
- additive fields are backward compatible;
- field reuse is forbidden;
- semantic changes require a new field or protocol version;
- authorization-sensitive changes require a policy version bump;
- schema changes are checked with Buf breaking-change rules when Protobuf is adopted.

## 3. Message envelope

Conceptual envelope:

Envelope {
  protocol_version
  message_type
  message_id
  correlation_id
  sender_id
  sender_role
  authority_epoch
  sent_at
  expires_at
  trace_id
  payload_digest
  payload
  signature
}

Rules:
- message_id is unique within sender epoch;
- correlation_id links request/response;
- expires_at is mandatory for request-scoped messages;
- signature covers canonical envelope fields and payload digest;
- trace_id is observability metadata only;
- no credential values are permitted in the envelope.

## 4. Identity

Sender roles:
- MEDIAHUB_NODE
- SCHEDULER
- POLICY_AUTHORITY
- EXECUTION_BACKEND
- EVIDENCE_VERIFIER
- CPRG

Identity requirements:
- stable node identity;
- proof of possession;
- expiration/revocation;
- authority epoch binding;
- replay protection.

Workload execution identity is separate from node identity.

## 5. CapabilityAdvertisement

Node -> Control:

CapabilityAdvertisement {
  node_id
  capability_epoch
  generated_at
  expires_at
  cpu
  gpu[]
  npu[]
  memory
  storage_classes[]
  runtime_classes[]
  isolation_classes[]
  network_classes[]
  max_concurrent_jobs
  current_load
  contribution_policy
  attestation_reference
  signature
}

Freshness:
- expired advertisement is unusable;
- capability_epoch must monotonically increase;
- scheduler must not infer capabilities not present in the signed advertisement.

Resource units:
- CPU: logical cores plus utilization ceiling;
- memory: bytes;
- GPU/NPU: device class + count + memory;
- storage: bytes + class;
- network: bounded egress class.

## 6. WorkloadSpec

Workload origin:
- DEVELOPER
- SYSTEM
- USER_ESCALATED

Workload class:
- LOCAL_ONLY
- LOCAL_PREFERRED
- CLOUD_DEVELOPMENT_ONLY
- CLOUD_ESCALATED_USER

Privacy class:
- PUBLIC_ENGINEERING
- DEVELOPER_CONFIDENTIAL
- USER_DERIVED_NON_PERSONAL
- USER_PERSONAL
- USER_SENSITIVE
- SECRET

Required fields:
- job_id
- workload_revision
- origin
- workload_class
- privacy_class
- required_capabilities
- resource_limits
- execution_deadline
- lease_max_duration
- network_policy
- input_policy
- output_policy
- contributor_eligibility
- partitioning_contract
- retry_contract
- artifact_digest
- artifact_signature_reference

Hard rule:
LOCAL_ONLY cannot be scheduled outside the local MediaHub execution domain.

## 7. AdmissionRequest

Scheduler -> Policy Authority:

AdmissionRequest {
  request_id
  job_id
  node_id
  workload_digest
  capability_epoch
  required_capabilities
  privacy_class
  contributor_eligibility
  authority_epoch
  requested_lease
}

The policy authority evaluates:
- identity;
- workload class;
- privacy;
- node capability;
- resource availability;
- contributor policy;
- artifact trust;
- authority epoch;
- requested lease.

## 8. AdmissionDecision

Policy Authority -> Scheduler:

AdmissionDecision {
  decision_id
  request_id
  job_id
  node_id
  decision: ADMIT | DENY
  policy_version
  authority_epoch
  capability_match
  privacy_decision
  resource_decision
  artifact_decision
  lease_max
  reason_code
  expires_at
  signature
}

A DENY decision must not contain secrets or personal payloads.

## 9. ComputeLease

Lease fields:
- lease_id
- job_id
- node_id
- authority_epoch
- issued_at
- expires_at
- resource_limits
- network_scope
- data_scope
- cancellation_token_digest
- fencing_token
- lease_state
- signature

State machine:

REQUESTED
-> ISSUED
-> ACKED
-> ACTIVE
-> RESULT_PENDING
-> CLOSED

Failure transitions:
REQUESTED -> DENIED
ISSUED -> REVOKED -> CLOSED
ACKED -> EXPIRED -> CLOSED
ACTIVE -> REVOKED -> CLOSED
ACTIVE -> FAILED -> CLOSED
RESULT_PENDING -> CLOSED

No transition may reopen CLOSED.

## 10. Fencing

Every state-changing operation carries:
- authority_epoch
- fencing_token
- lease_id
- monotonic lease_revision

The authoritative store rejects:
- old authority epochs;
- old fencing tokens;
- revisions <= current revision;
- writes against CLOSED leases.

This protects against stale scheduler/controller instances.

## 11. Dispatch

Scheduler -> Node:

JobDispatch {
  job_id
  attempt_id
  execution_id
  lease_id
  artifact_digest
  artifact_signature_reference
  resource_limits
  network_scope
  input_manifest_digest
  output_contract
  deadline
  trace_id
  signature
}

Node must verify:
1. identity;
2. lease exists;
3. lease active;
4. fencing token current;
5. artifact trusted;
6. resource limits;
7. network scope;
8. input/output policy.

Only then may execution start.

## 12. Heartbeat

Node -> Control:

Heartbeat {
  lease_id
  execution_id
  lease_revision
  observed_at
  execution_state
  resource_usage
  output_progress
  evidence_digest
}

Heartbeat is advisory.

The authoritative lease expiry remains server-side.

A heartbeat cannot extend a lease unless an explicit, authorized renewal protocol is later defined.

## 13. Result

Node -> Control:

ExecutionResult {
  job_id
  attempt_id
  execution_id
  lease_id
  state: SUCCEEDED | FAILED | CANCELLED | REVOKED | EXPIRED
  output_manifest_digest
  output_size
  output_class
  result_digest
  started_at
  finished_at
  failure_class
  evidence_digest
  signature
}

Undeclared output is rejected.

No raw user payload belongs in generic result metadata.

## 14. Evidence

ExecutionEvidence {
  job_id
  attempt_id
  execution_id
  lease_id
  node_id
  artifact_digest
  artifact_provenance
  policy_version
  authority_epoch
  start/end
  resource_usage
  network_policy_id
  input_digest
  output_digest
  final_state
  failure_class
  evidence_version
  signature
}

Evidence is metadata-first and payload-free by default.

## 15. Revocation

Policy Authority -> Node/Scheduler:

LeaseRevoke {
  lease_id
  job_id
  node_id
  authority_epoch
  fencing_token
  reason
  effective_at
  signature
}

Node behavior:
- stop accepting new work;
- terminate execution;
- close lease;
- emit final evidence.

Revocation must be idempotent.

## 16. Idempotency

Keys:
- job_id: logical workload;
- attempt_id: retry attempt;
- execution_id: concrete execution;
- message_id: transport message;
- idempotency_key: operation-specific deduplication.

Duplicate dispatch:
- same execution_id + same artifact/policy => return existing execution state;
- same execution_id + different artifact/policy => reject;
- reused closed lease => reject.

## 17. Partitioning

PartitioningContract:
- mode: NONE | MAP | MAP_REDUCE | SHARDED_STATE
- partition_key
- partition_count
- merge_contract
- retry_semantics
- deterministic_merge
- max_parallelism

Only workloads explicitly marked partitionable may execute on multiple contributors.

Merge output must be independently verifiable.

## 18. Network policy

Default:
DENY.

Allowed network must be explicit in WorkloadSpec and Lease.

A contributor execution must not access:
- MediaHub LAN;
- router/admin interfaces;
- NAS/storage control plane;
- peer MediaHub services;
- CPRG;
unless an independently authorized future contract explicitly permits it.

Compute Contribution Plane is not a bridge to the Media Data Plane.

## 19. Filesystem policy

Default:
- dedicated worker identity;
- dedicated work directory;
- no host root;
- no MediaHub storage mounts;
- temporary writable workspace;
- bounded result directory;
- cleanup after close.

OCI/container isolation may implement these properties.

## 20. Artifact trust

A developer workload must reference:
- immutable artifact digest;
- source revision;
- provenance;
- signature/verification policy.

Tag-only execution is forbidden for privileged contributor workloads.

Cosign/Sigstore is a candidate implementation for artifact signing/verification, not the MediaHub authority.

## 21. Observability

Trace context:
- trace_id
- span_id
- parent relationship

Operational identifiers:
- job_id
- attempt_id
- execution_id
- lease_id
- node_id

Sensitive payloads are never copied into traces, logs or metrics.

High-cardinality identifiers belong in traces/events, not unbounded metric labels.

## 22. Transport bindings

V1 abstract transport:

Transport.send(Envelope)
Transport.receive()
Transport.ack()
Transport.reject()
Transport.close()

Candidate bindings:
- gRPC/HTTP2 for request/response control APIs;
- NATS/JetStream for asynchronous event delivery;
- direct local IPC for node executor.

Transport choice does not alter protocol semantics.

## 23. Error model

Stable error classes:
- INVALID_MESSAGE
- INVALID_IDENTITY
- REPLAY
- STALE_EPOCH
- STALE_FENCING
- POLICY_DENIED
- CAPABILITY_MISMATCH
- PRIVACY_DENIED
- ARTIFACT_UNTRUSTED
- LEASE_EXPIRED
- LEASE_REVOKED
- RESOURCE_EXHAUSTED
- OUTPUT_VIOLATION
- NETWORK_VIOLATION
- DUPLICATE
- INTERNAL

Security-sensitive errors should not reveal policy internals beyond a stable reason code.

## 24. Failure invariants

The following are hard invariants:

F1. CLOSED lease cannot execute.
F2. Expired lease cannot execute.
F3. Revoked lease cannot execute.
F4. Stale authority epoch cannot mutate state.
F5. Stale fencing token cannot mutate state.
F6. LOCAL_ONLY cannot leave local execution domain.
F7. USER_SENSITIVE cannot move to a contributor without explicit future policy.
F8. Contributor cannot access MediaHub storage namespace.
F9. Contributor cannot access arbitrary MediaHub LAN.
F10. Undeclared output is rejected.
F11. Duplicate dispatch does not create a second execution for the same execution_id.
F12. Transport duplication cannot corrupt authoritative state.
F13. CPRG registration authority is not part of compute execution.
F14. Compute contribution does not imply developer personnel access to user data.

## 25. Qualification test matrix

Protocol tests must include:

Identity:
- unknown;
- expired;
- revoked;
- wrong authority epoch;
- invalid signature.

Lease:
- expired;
- revoked;
- duplicate;
- stale fencing;
- CLOSED reuse.

Capability:
- exact match;
- insufficient CPU;
- insufficient memory;
- missing GPU/NPU;
- stale advertisement.

Privacy:
- public engineering;
- developer confidential;
- user-derived non-personal;
- user personal;
- user sensitive;
- secret.

Network:
- allowed destination;
- LAN escape;
- CPRG escape;
- arbitrary Internet escape;
- unauthorized peer.

Artifacts:
- trusted digest;
- changed digest;
- invalid signature;
- expired provenance.

Reliability:
- duplicate delivery;
- node disappearance;
- scheduler restart;
- authority restart;
- message redelivery;
- partial partition failure.

Result:
- declared output;
- oversized output;
- undeclared channel;
- malformed evidence.

## 26. External component mapping

Buf:
- schema build;
- lint;
- breaking-change checks;
- code generation.

Protovalidate:
- message-level semantic validation.

gRPC:
- synchronous control APIs;
- deadlines;
- metadata/interceptors;
- streaming where required.

NATS/JetStream:
- asynchronous transport;
- durable event delivery;
- ack/redelivery;
- application idempotency.

Ray:
- execution backend;
- resource placement;
- task/actor execution;
- object transport.

containerd/OCI:
- isolated worker lifecycle;
- filesystem/process/resource sandbox.

SPIFFE/SPIRE:
- optional workload identity implementation.

Cosign/Sigstore:
- artifact signatures/provenance verification.

OpenTelemetry:
- trace context and observability vocabulary.

Netmaker/WireGuard:
- Development Mesh only.

SeaweedFS:
- developer storage substrate only.

OpenFGA:
- optional relationship authorization only.

## 27. Implementation boundary

Initial MediaHub code must implement the protocol independent of all external components.

Required interfaces:

IdentityVerifier
CapabilityRegistry
AdmissionPolicy
LeaseAuthority
FencingStore
Scheduler
ExecutionBackend
ArtifactVerifier
NetworkPolicyEnforcer
PrivacyPolicy
ResultVerifier
EvidenceStore
EventTransport

Each must have:
- deterministic fake;
- failure injection;
- contract tests;
- explicit authority;
- versioned API.

## 28. First implementation order

1. schema definitions;
2. validators;
3. lease state machine;
4. fencing;
5. capability matcher;
6. admission policy;
7. idempotency;
8. privacy policy;
9. network policy;
10. deterministic scheduler;
11. isolated local executor;
12. evidence verifier;
13. transport adapter;
14. external component adapters.

No production deployment is implied by this document.


## 29. Time and clock contract

Lease validity is determined by the authority, not by a contributor's wall clock.

Required:
- authority-issued issued_at/expires_at;
- local monotonic clock for execution timeout;
- bounded wall-clock skew;
- freshness window for signed capability advertisements;
- explicit behavior when time synchronization is unavailable.

A node may conservatively stop work early. It may never extend an expired lease based only on its local clock.

## 30. Schema evolution rules

When Protobuf becomes the canonical wire encoding:
- deleted field numbers are reserved;
- deleted field names are reserved where tooling requires it;
- enum values are never silently reused;
- compatibility is checked in CI;
- protocol major changes require a new package/version;
- security-sensitive semantic changes require a policy version bump even when wire-compatible.

Buf is the preferred schema-governance tool because it provides build, lint, generation and breaking-change detection.

## 31. Authoritative-state publication

A state mutation is considered committed only after the authoritative store accepts it.

For events transported through NATS/JetStream:
1. validate command;
2. transactionally persist state transition;
3. persist event/outbox record;
4. publish/ack transport event;
5. mark delivery state.

A transport acknowledgement is never proof that the state transition committed.

This is the basis for an eventual transactional-outbox implementation.

## 32. gRPC control semantics

For synchronous control RPCs:
- every call has a deadline;
- cancellation propagates to the server;
- authentication and trace context are carried in metadata;
- interceptors enforce common validation/auth/observability rules;
- retry is only permitted for explicitly idempotent operations.

Long-running execution is not represented by an unbounded RPC. Use job IDs and asynchronous state.

## 33. Sandbox escalation

Process/cgroup/namespace isolation is the v1 baseline only for trusted developer artifacts.

For untrusted or higher-risk contributor workloads, the architecture must support an isolation-class escalation:
- OCI/container baseline;
- stronger runtime class;
- microVM/KVM class where required.

The workload contract selects the minimum isolation class. The scheduler must not downgrade it.

## 34. Network enforcement principle

NetworkPolicy is enforced at the execution boundary, not only in scheduler metadata.

The scheduler supplies a policy ID; the worker runtime must enforce it locally.

Where a kernel-level policy engine is used, identity-based egress controls may be implemented with Cilium/eBPF or equivalent. The MediaHub policy remains authoritative.

## 35. Artifact verification

Artifact admission requires:
- immutable digest;
- signature/provenance verification;
- source revision;
- policy-compatible signer identity.

Cosign/Sigstore is a candidate implementation.

The artifact is verified before execution and the verified digest is bound into the lease/evidence.

## 36. Observability privacy

OpenTelemetry trace propagation is allowed for correlation.

Forbidden telemetry:
- API keys;
- private keys;
- personal media content;
- user filesystem contents;
- raw model/provider payloads unless explicitly classified as non-sensitive engineering data.

High-cardinality IDs remain event/trace fields.

## 37. Security boundary conclusion

External components implement mechanisms.
MediaHub contracts implement authority.

No component may infer authorization merely because it can:
- reach a node;
- schedule a task;
- issue a message;
- obtain an identity;
- mount storage;
- establish a VPN;
- verify an artifact.

