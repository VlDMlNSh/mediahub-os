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

