# MediaHub Architecture Gaps and Pushback Register

Date: 2026-09-30
Status: pre-implementation review

## P0 — must close before real distributed compute

### G1 — Node identity format
Need exact cryptographic representation, storage, rotation and revocation semantics.

Decision required:
- key algorithm;
- node identity encoding;
- proof-of-possession protocol;
- expiration;
- revocation distribution.

### G2 — Capability attestation
Self-reported CPU/GPU/NPU is insufficient for trusted scheduling.

Need:
- signed capability snapshot;
- freshness;
- source of hardware facts;
- resource reservation semantics;
- health status;
- anti-overcommit policy.

### G3 — Execution isolation
The architecture states isolation requirements but does not yet define the concrete worker boundary.

Need:
- process vs OCI vs VM;
- uid/gid;
- cgroup limits;
- filesystem namespace;
- network namespace;
- seccomp/AppArmor profile where available;
- cleanup guarantees.

### G4 — Authoritative state store
We have defined that NATS is not State Authority, but the authoritative persistent store is not yet selected.

Need:
- SQLite/PostgreSQL/etc decision;
- transaction boundaries;
- lease persistence;
- fencing tokens;
- crash recovery;
- backup/restore.

### G5 — Scheduler fencing
A stale scheduler must not issue a valid lease after authority loss.

Need:
- scheduler epoch;
- lease fencing token;
- monotonic version;
- rejection of stale controller writes.

## P0 — privacy/security

### G6 — User-data classification
Privacy boundary requires explicit classes.

Minimum:
- PUBLIC_ENGINEERING
- DEVELOPER_CONFIDENTIAL
- USER_DERIVED_NON_PERSONAL
- USER_PERSONAL
- USER_SENSITIVE
- SECRET

Each class needs allowed execution domains and transfer rules.

### G7 — Developer operator boundary
Technical isolation alone does not prevent an administrator from inspecting a worker host.

Need:
- operational access model;
- encrypted/pseudonymized inputs where feasible;
- no personal payload logging;
- host-level access policy;
- evidence proving developer personnel cannot access user data.

### G8 — Result confidentiality
A worker can leak data through output.

Need:
- result schema;
- size limits;
- output type allowlist;
- content policy;
- digest/evidence;
- rejection of undeclared output channels.

### G9 — Local-network boundary
Compute contribution must not create arbitrary access to the MediaHub LAN.

Need explicit network namespace + egress ACL + negative tests against:
- router;
- NAS;
- MediaHub services;
- local discovery;
- arbitrary LAN IPs.

## P0 — correctness

### G10 — Idempotency and retry
At-least-once delivery means duplicate dispatch is normal.

Need:
- global job ID;
- attempt ID;
- execution ID;
- idempotency key;
- duplicate suppression;
- safe retry policy;
- poison-job quarantine.

### G11 — Partitioned job semantics
“Distributed compute” is meaningless until the system defines which workloads are partitionable.

Need explicit classes:
- embarrassingly parallel;
- map/reduce;
- actor/stateful;
- non-partitionable;
- GPU-exclusive;
- data-local.

Each class needs merge/retry semantics.

### G12 — Clock model
Leases depend on time.

Need:
- server-authoritative expiry;
- monotonic clocks locally;
- bounded clock skew;
- behavior under NTP failure;
- no client-controlled lease extension.

## P1 — operations

### G13 — node churn
MediaHub contributors can disappear.

Need:
- heartbeat;
- health states;
- lease loss;
- requeue;
- backoff;
- capacity hysteresis.

### G14 — heterogeneous hardware
CPU/GPU/NPU cannot be represented as one generic “compute unit”.

Need resource taxonomy and scheduler normalization.

### G15 — WAN cost/latency
Distributed execution can be slower than local execution.

Need placement model including:
- transfer bytes;
- RTT;
- available bandwidth;
- serialization cost;
- expected execution time;
- locality score.

### G16 — contributor fairness
Idle capacity must not be consumed without policy.

Need:
- contributor opt-in;
- maximum CPU/GPU share;
- thermal/power policy;
- charging/battery policy for mobile nodes;
- quiet hours;
- user override;
- revocation.

### G17 — developer workload provenance
Developer code executed on user devices requires supply-chain controls.

Need:
- signed workload artifact;
- source revision;
- dependency manifest;
- provenance;
- allowed runtime image;
- rollback.

## P1 — external component boundaries

### G18 — Ray boundary
Ray must not become the security authority.

Need adapter:
MediaHub Lease -> Ray placement/resource request -> Ray execution -> MediaHub evidence.

### G19 — NATS boundary
NATS is transport, not authority.

Need durable state transition before/with event publication and idempotent consumers.

### G20 — SPIRE boundary
SPIRE may solve workload identity but does not solve MediaHub authorization or privacy.

Need mapping document before adoption.

### G21 — Netmaker boundary
Netmaker controls network connectivity but must not define MediaHub data authorization.

Need route/ACL contract independent of Netmaker.

### G22 — SeaweedFS boundary
Storage substrate must not grant compute contributors storage namespace access.

Need separate storage credentials and namespaces.

### G23 — OpenFGA boundary
OpenFGA can answer relationship authorization but cannot replace hard local safety checks.

Need fail-closed local policy for leases, routing and data classes.

## P1 — CPRG

### G24 — CPRG message protocol
Current architecture has state machines but not the exact wire-level contract.

Must define:
- request;
- challenge;
- authentication proof;
- admission;
- lease;
- registration;
- result;
- close;
- revoke;
- error;
- evidence.

### G25 — CPRG audit failure
Architecture says silent success is prohibited but does not select exact behavior.

Need explicit choice:
- fail registration if audit cannot be durably recorded;
- or bounded local buffer with later proof.

### G26 — migration transaction
Need exact atomicity mechanism preventing two active authorities.

### G27 — recovery quorum
Need custody and approval policy for emergency replacement.

## P2 — scale

### G28 — multi-node result merge
Need deterministic merge contract.

### G29 — backpressure
Need admission limits at:
- scheduler;
- node;
- message bus;
- storage;
- result path.

### G30 — observability cardinality
Do not use job_id/node_id as unbounded metric labels.

Use traces/events for high-cardinality identities; metrics remain bounded.

## Architectural pushback

1. “Supercomputer” is a useful product metaphor but a dangerous engineering abstraction. Treat the system as a heterogeneous distributed compute fabric. Network partitions, trust boundaries, device churn and data locality remain fundamental.

2. More nodes do not automatically mean more performance. A workload should move to contributors only when expected useful work exceeds transfer, scheduling and failure overhead.

3. Free/idle compute is not free from the user's perspective. It has power, heat, battery, bandwidth and privacy costs. Contribution must be opt-in and revocable.

4. A developer can execute code on a contributor without being allowed to inspect the contributor's user data. This requires isolation stronger than process naming or ACLs alone.

5. “Exactly once” should not be used as an architectural promise. The safe contract is at-least-once transport + idempotent execution + deterministic result verification.

6. A central scheduler is not the same thing as a central authority. Admission and lease authority must be explicit and cryptographically enforceable.

7. A VPN is not a security boundary by itself. CPRG must enforce the registration-only policy at the server/firewall level.

8. Adding many third-party components early would increase rather than decrease risk. First stabilize MediaHub-owned contracts and deterministic tests.

## Implementation gate

No external component should be deployed until P0 gaps G1-G12 have deterministic tests or explicit justified exceptions.



## P0 additions found during 13 review passes

### G31 — Clock/freshness contract
Capability and lease expiry require an explicit skew/freshness model.
Need:
- authority clock;
- local monotonic timeout;
- maximum accepted skew;
- stale advertisement threshold;
- NTP/time-source failure behavior.

### G32 — Transactional state/event publication
The architecture must prevent a published event from claiming a state transition that was never committed.
Need:
- transactional outbox or equivalent;
- event sequence/version;
- replay-safe consumers;
- recovery of unpublished committed events.

### G33 — Protocol schema evolution
Need formal compatibility policy:
- reserved fields;
- enum non-reuse;
- major versioning;
- Buf breaking checks;
- policy-version coupling for security semantics.

### G34 — RPC timeout/cancellation semantics
Synchronous control calls need explicit deadlines and cancellation propagation.
Need:
- default deadlines by operation;
- maximum deadlines;
- idempotent retry classification;
- no unbounded control RPC.

### G35 — Isolation-class escalation
OCI isolation is not sufficient for every untrusted workload.
Need:
- trust classification;
- minimum isolation class;
- container/OCI baseline;
- microVM escalation;
- scheduler prohibition on isolation downgrade.

### G36 — Kernel network enforcement
Scheduler metadata alone is insufficient.
Need:
- execution-boundary network enforcement;
- default deny;
- explicit egress allowlist;
- negative LAN/CPRG tests;
- proof that policy remains after scheduler restart.

## External component selection update

The GitHub review added four reusable primitives to the candidate set:

- **Buf** — schema build/lint/breaking-change governance.
- **Protovalidate** — semantic validation rules attached to Protobuf schemas.
- **containerd + OCI Runtime Spec** — lifecycle and portable isolation model.
- **Cosign/Sigstore** — artifact signature/provenance verification.

Additional mechanism references:
- gRPC metadata/deadlines/interceptors;
- OpenTelemetry stable tracing API;
- Cilium identity-based network policy concepts.

These are mechanism candidates, not authority replacements.

## 13-pass review outcome

Passes performed:
1. fencing/stale authority
2. idempotency
3. schema evolution
4. RPC deadline/cancellation
5. OCI isolation
6. untrusted workload sandboxing
7. heterogeneous scheduling
8. message acknowledgement/redelivery
9. workload identity
10. observability/privacy
11. artifact provenance
12. network enforcement
13. distributed storage boundary

Corrections were incorporated into the compute wire protocol:
- clock/freshness contract;
- transactional state/event publication;
- schema evolution rules;
- gRPC timeout/cancellation semantics;
- isolation escalation;
- execution-boundary network enforcement;
- artifact verification binding;
- telemetry privacy constraints.

No contradiction was found with the previously fixed Local Cluster / Cloud Development Cluster / CPRG architecture.


## P0 additions — Cloud Development Fabric

### G37 — High-speed interconnect qualification
Thunderbolt/USB4 capability varies by Mac mini hardware, OS, controller, firmware and topology.
Need a node-class qualification record covering:
- physical link;
- negotiated link;
- IP interface;
- throughput;
- RTT;
- packet loss;
- MTU;
- reconnect;
- sleep/wake;
- peer authorization.

### G38 — High-speed topology
Point-to-point Thunderbolt links must not be mistaken for a general multi-node fabric.
Need explicit topology discovery and scheduler representation.

### G39 — High-speed security
Physical adjacency does not establish trust.
Need peer identity, host firewall, dedicated subnet, default-deny forwarding and unauthorized-peer quarantine.

### G40 — RDMA qualification
RDMA is optional and must not become a correctness dependency.
Need exact hardware/OS/driver matrix, transport security, failure semantics and benchmark evidence.

### G41 — Performance-aware placement
Scheduler currently needs measured network cost.
Need bandwidth, RTT, transfer size, serialization cost and failure penalty in placement decisions.

### G42 — Mac mini node classes
Need explicit hardware classes because Thunderbolt/USB4, GPU/NPU capabilities and OS support differ.

## Pushback — Cloud Development Fabric

- A high-speed interconnect is not shared memory.
- A cluster of Mac minis is not automatically a single pooled CPU/GPU.
- Remote execution still has serialization, scheduling and failure overhead.
- RDMA should optimize large-object movement only after measurements demonstrate benefit.
- User MediaHub traffic must never be opportunistically routed over the developer high-speed fabric.
