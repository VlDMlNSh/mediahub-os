# MediaHub Cloud Development Fabric — Reference Architecture v2

Date: 2026-09-30
Status: normative reference architecture for subsequent implementation
Scope: permanent developer/company environment
Production deployment: not authorized by this document

## 1. Objective

The Cloud Development Fabric is the permanent developer/company environment composed of developer servers, CI/CD, engineering storage, Astra, and explicitly admitted MediaHub compute contributors.

It is a heterogeneous distributed compute fabric, not a literal single-machine supercomputer.

Hard invariant:

Compute Contribution != User Data Access != Developer Personnel Access

## 2. Developer network planes

- Developer Control Plane: GitHub, Astra, scheduler, policy, authoritative state, evidence.
- Developer Compute Plane: developer servers, Ray/ExecutionBackend, contributed workers.
- Developer Storage Plane: source, builds, models, approved datasets, evidence.
- Development Mesh: private management/discovery, encrypted, direct P2P preferred.
- Compute Contribution Plane: capability, admission, lease, dispatch, heartbeat, result, revocation.
- High-Speed Interconnect Plane: direct developer-node links using Thunderbolt/USB4 networking.
- Developer Egress Plane: ordinary Internet connectivity for developer nodes.
- Optional Developer Shared Egress: explicit IP forwarding/NAT through a peer over HIGH_SPEED.
- Media Data Plane: local MediaHub LAN/P2P; never exported by default.
- Protected Registration Plane: MediaHub -> CPRG -> exact provider registration; VPN-backed registration only.

## 3. Developer node interface model

Each developer node publishes a measured interface inventory:

- INTERNET
- DEV_MESH
- HIGH_SPEED
- optional DEV_STORAGE
- optional CPRG registration interface/path

Each interface has:
- address;
- link state;
- MTU;
- measured bandwidth;
- measured RTT;
- loss;
- route class;
- allowed destinations;
- trust state.

No interface is trusted merely because it is physically present.

HIGH_SPEED and DEV_MESH never become default gateways automatically.

## 4. Primary Development Node

Primary is a dynamic role, not a permanent hardware identity.

Selection score is based on measured:
- CPU;
- GPU/NPU;
- RAM;
- NVMe;
- available capacity;
- high-speed bandwidth;
- RTT;
- storage bandwidth;
- reliability/uptime;
- control-plane readiness.

The primary may host scheduler/control roles but must not be the only copy of authoritative developer state.

Primary loss must permit role migration.

## 5. Mac mini high-speed fabric

Baseline:

Mac mini A <== Thunderbolt/USB4 == > Mac mini B

Linux mainline provides USB4/Thunderbolt IP networking through USB4_NET/thunderbolt_net and documents interoperability with Apple ThunderboltIP hosts including macOS and Windows.

This establishes the technology as a valid V1 IP-link candidate.

It does not establish:
- arbitrary multi-node Ethernet switching;
- shared memory;
- automatic cluster membership;
- trust;
- automatic Internet routing.

Use a dedicated high-speed subnet and model every physical edge.

For N nodes:
- point-to-point links are represented as graph edges;
- topology is discovered;
- each edge has measured capacity/RTT/loss;
- scheduler uses the graph when placing distributed workloads.

## 6. Shared Internet over HIGH_SPEED

A HIGH_SPEED interface is an IP network interface, so a developer node may forward Internet traffic through a peer.

Example:

Node A INTERNET
     |
   router/NAT
     |
 HIGH_SPEED
     |
Node B developer traffic

This is supported only as an explicit developer-network capability.

V1 default:
- each developer node has independent Internet when possible;
- each node keeps its own default route;
- HIGH_SPEED has no default route.

Optional shared egress:
- explicit enablement;
- forwarding/NAT firewall policy;
- capability advertisement;
- bandwidth quota;
- audit;
- failure detection;
- no forwarding of user MediaHub traffic.

The primary node is not automatically the Internet gateway because it has more compute.

## 7. High-speed compute

HIGH_SPEED is preferred for:
- large developer objects;
- model shards;
- build artifacts;
- distributed task coordination;
- intermediate results;
- developer storage traffic where justified.

Placement cost includes:
- compute;
- serialization;
- input transfer;
- output transfer;
- bandwidth;
- RTT;
- contention;
- failure/retry penalty.

## 8. Execution architecture

Execution path:

Scheduler
 -> AdmissionPolicy
 -> ComputeLease
 -> ExecutionBackend
 -> isolated worker
 -> result/evidence

Candidate backend:
- Ray.

Candidate worker runtime:
- containerd/OCI;
- stronger isolation class for higher-risk workloads.

Network policy is enforced at execution boundary.

## 9. Control transport

Synchronous:
- gRPC with deadlines/cancellation.

Asynchronous:
- NATS/JetStream with durable delivery where needed.

Authoritative state:
- MediaHub-owned persistent state.

Transport acknowledgements are never authoritative commit evidence.

## 10. Developer Mesh

Development Mesh is a private encrypted management/discovery network.

Primary candidate:
- Netmaker/WireGuard.

Alternative:
- Headscale/WireGuard.

HIGH_SPEED remains preferred for bulk developer traffic when the direct link is healthy.

Development Mesh is not a replacement for the local Media Mesh and is not a user LAN bridge.

## 11. Routing

Rules:

- INTERNET -> ordinary developer Internet.
- DEV_MESH -> private management/discovery only.
- HIGH_SPEED -> developer peer traffic only by default.
- DEV_STORAGE -> storage traffic only.
- shared developer egress -> explicit route/policy only.
- Media Mesh -> never forwarded through developer HIGH_SPEED.
- CPRG -> registration-only protected path.
- no automatic route redistribution across planes.

## 12. Storage

Three separate classes:

1. Local MediaHub storage — personal media/data.
2. Developer engineering storage — source/build/model/approved datasets/evidence.
3. Ephemeral execution workspace — lease-scoped.

No contributor worker receives a shared mount to local MediaHub storage.

## 13. Compute Contribution

MediaHub nodes may contribute otherwise unused CPU/GPU/NPU capacity.

Contribution is:
- opt-in;
- capability-scoped;
- admission-controlled;
- lease-bound;
- isolated;
- network-restricted;
- result-bounded;
- auditable;
- revocable.

Contribution traffic uses ordinary network connectivity and the Compute Contribution Plane.

It does not require a flat network connection to the user's Media Mesh.

## 14. Privacy boundary

Developer compute may receive only data allowed by the workload's privacy class.

Default:
- public engineering data may execute in the developer fabric;
- developer confidential data requires authorized developer nodes;
- user-derived non-personal data requires explicit policy;
- user personal/sensitive data remains local unless a future explicit policy and protection contract permits movement;
- secrets never move to contributed MediaHub workers by default.

Developer personnel access to user data is a separate prohibition.

## 15. CPRG

CPRG remains outside the compute path.

CPRG VPN-backed connectivity is used exclusively for API-key registration.

CPRG is not:
- Internet gateway;
- developer compute;
- storage;
- MediaHub data gateway;
- HIGH_SPEED transit;
- general VPN.

## 16. High-speed security

Required:
- cryptographic peer identity;
- authenticated control;
- dedicated interface/subnet;
- host firewall;
- default-deny forwarding;
- explicit service allowlist;
- unauthorized-peer quarantine;
- no bridge to Media Mesh;
- no trust from physical attachment.

## 17. Failure model

HIGH_SPEED:
UNKNOWN -> PROBING -> UP -> DEGRADED -> DOWN -> QUARANTINED

When down:
- remove edge from placement;
- use DEV_MESH if available;
- re-place partitionable work;
- preserve authoritative state;
- do not modify default Internet routing.

Primary down:
- elect/migrate primary role;
- continue from replicated durable state;
- preserve node identity semantics.

Developer WAN down:
- local developer-to-developer execution may continue;
- WAN-dependent tasks pause/fail according to workload policy.

## 18. Mac mini shared-egress qualification

A dedicated qualification phase must verify:

1. A has Internet.
2. A and B have HIGH_SPEED IP connectivity.
3. B can reach Internet through A only when explicit shared-egress mode is enabled.
4. B's ordinary default route remains unchanged when shared mode is disabled.
5. MediaHub user subnets cannot use A as transit.
6. Firewall blocks unauthorized forwarding.
7. Egress failure is detected.
8. Compute jobs continue or fail safely according to policy.
9. Scheduler does not mistake shared egress for compute bandwidth.
10. Audit evidence identifies the egress node and policy.

## 19. External components

- Linux thunderbolt_net / USB4_NET: high-speed IP transport reference.
- iperf3: bandwidth/RTT/loss qualification.
- Ray: execution backend.
- NATS/JetStream: asynchronous transport.
- gRPC: control RPC.
- containerd/OCI: isolation.
- Buf/Protovalidate: schemas/validation.
- SPIRE: optional workload identity.
- Cosign/Sigstore: artifact verification.
- OpenTelemetry: telemetry.
- Netmaker/WireGuard: Development Mesh.
- Headscale/WireGuard: alternative Development Mesh.
- CoreDNS: developer DNS.
- FRR: optional dynamic routing.
- SeaweedFS: optional developer storage.
- OpenWrt/OpenWISP: local network/AP management mechanisms.

External components remain replaceable mechanisms. MediaHub contracts remain authoritative.

## 20. Qualification sequence

A. two-node HIGH_SPEED IP qualification.
B. shared-egress controlled qualification.
C. three+ node topology.
D. scheduler cost-aware placement.
E. link failure/recovery.
F. developer WAN failure.
G. primary role migration.
H. MediaHub compute contribution.
I. privacy and network negative tests.
J. evidence reproducibility.
K. optional RDMA benchmark.

RDMA remains optional and never a correctness dependency.

## 21. Acceptance gates

- developer interfaces inventoried;
- HIGH_SPEED links measured;
- no accidental default route;
- shared Internet is opt-in;
- user MediaHub traffic cannot use developer egress;
- topology is represented explicitly;
- placement uses measured network cost;
- primary migration works;
- developer state survives link loss;
- contributor cannot reach MediaHub LAN/storage;
- CPRG remains outside compute;
- privacy boundary is enforceable;
- evidence is machine-verifiable.

## 22. Final principle

Mac mini servers can form a high-speed developer compute fabric using direct Thunderbolt/USB4 IP links.

Those links can also carry controlled developer Internet traffic when one node is deliberately configured as an egress router.

Neither capability changes the fundamental hierarchy:
- MediaHub local network remains user-facing;
- Cloud Development Fabric remains developer-facing;
- Compute Contribution is request-scoped;
- CPRG is registration-only;
- MediaHub-owned contracts remain authoritative.
