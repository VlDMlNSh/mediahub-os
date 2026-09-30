# MediaHub Cloud Development Fabric — Reference Architecture

Date: 2026-09-30
Status: reference architecture for implementation

## 1. Objective

The Cloud Development Fabric is the permanent developer/company environment composed of developer servers, CI/CD, engineering storage, Astra, and explicitly admitted MediaHub compute contributors.

It is a heterogeneous distributed compute fabric, not a literal single-machine supercomputer.

Hard invariant: Compute Contribution != User Data Access != Developer Personnel Access.

## 2. Planes

- Developer Control Plane: GitHub, Astra, scheduler, policy, authoritative state, evidence.
- Developer Compute Plane: developer servers, Ray/ExecutionBackend, contributed workers.
- Developer Storage Plane: source, builds, models, approved datasets, evidence.
- Development Mesh: private management/discovery, encrypted, direct P2P preferred.
- Compute Contribution Plane: capability, admission, lease, dispatch, heartbeat, result, revocation.
- Media Data Plane: local MediaHub LAN/P2P; never exported by default.
- Protected Registration Plane: MediaHub -> CPRG -> exact provider registration; VPN-backed registration only.
- High-Speed Interconnect Plane: direct developer-node links using Thunderbolt/USB4 networking, with optional RDMA after qualification.

## 3. Mac mini high-speed fabric

When developer servers are Mac mini systems, treat each as a normal developer node with a dedicated high-speed interface and subnet.

Linux mainline provides USB4/Thunderbolt networking through CONFIG_USB4_NET and the thunderbolt_net module. Its kernel configuration explicitly describes networking between computers over USB4/Thunderbolt and interoperability with hosts implementing Apple ThunderboltIP, including macOS and Windows. citeturn0search0

Therefore the baseline high-speed design is:

Mac mini A <== Thunderbolt/USB4 ==> Mac mini B

Use a dedicated point-to-point IP subnet. Do not assume Thunderbolt cabling creates an arbitrary multi-node Ethernet fabric. For more nodes, use multiple controlled links or an appropriate high-speed Ethernet/fabric.

Example logical subnet: 10.30.0.0/24.

## 4. RDMA

RDMA is an optimization candidate, not a correctness dependency.

A GitHub project, exo, contains an optional macOS RDMA path and notes OS-version compatibility constraints. This is useful implementation evidence, but not sufficient qualification evidence for MediaHub. citeturn0search0

V1: ordinary IP over Thunderbolt/USB4 + gRPC/NATS/Ray.
V2: optional RDMA-aware tensor/object transport after measured qualification.

## 5. Routing

Developer nodes may have:
- HIGH_SPEED: Thunderbolt/USB4 or validated RDMA interface.
- DEV_MESH: encrypted management network.
- INTERNET: ordinary Internet.
- optional STORAGE network.

Rules:
- developer compute traffic may prefer HIGH_SPEED;
- control traffic may use DEV_MESH;
- ordinary Internet remains INTERNET;
- MediaHub user traffic never uses HIGH_SPEED;
- CPRG is not reachable through HIGH_SPEED unless a future explicit contract requires it;
- default route must not move to HIGH_SPEED.

## 6. Scheduler

Placement cost must include:
- compute time;
- input transfer time;
- output transfer time;
- scheduling overhead;
- failure penalty.

Preferred hierarchy:
1. same developer node;
2. developer peer over HIGH_SPEED;
3. developer peer over Development Mesh;
4. admitted MediaHub contributor;
5. external cloud provider only when explicitly authorized.

This is a performance policy. Security authorization remains independent.

## 7. Developer node model

Logical roles:
- CONTROL
- SCHEDULER
- COMPUTE
- STORAGE
- EVIDENCE
- CI

Small installations may co-locate roles. CPRG remains a separate security domain and must not become a developer compute node.

## 8. Execution

Developer cluster resources:
- CPU;
- GPU;
- NPU where supported;
- memory;
- NVMe;
- high-speed links.

Execution remains behind the MediaHub ExecutionBackend contract.

Ray is an execution substrate, not a security authority.

containerd/OCI is an isolation mechanism, not a policy authority.

## 9. Storage

Three separate storage classes:

1. Local MediaHub storage — personal media/data; never automatically exported.
2. Developer engineering storage — source, builds, models, approved datasets, evidence.
3. Ephemeral execution workspace — per lease, bounded, destroyed after close.

No shared mount is permitted between contributor workers and user MediaHub storage.

## 10. High-speed security

Thunderbolt/USB4 is a physical interconnect, not an authorization system.

Required:
- peer identity;
- dedicated subnet;
- host firewall;
- authenticated control protocol;
- no trust based on MAC address alone;
- no default forwarding;
- no bridge into MediaHub LAN;
- appropriate host-side device authorization/security;
- unauthorized peer detection and quarantine.

## 11. Failure model

Link states:
UNKNOWN -> PROBING -> UP -> DEGRADED -> DOWN -> QUARANTINED.

A high-speed link failure must remove that link from placement without corrupting authoritative state. Scheduler must safely re-place work when the workload permits it.

Physical connectivity alone never makes a peer trusted.

## 12. Distributed workload model

Supported workload contracts:
- NONE;
- MAP;
- MAP_REDUCE;
- SHARDED_STATE.

Only explicitly partitionable workloads may cross nodes.

Results must have deterministic merge semantics and independently verifiable evidence.

## 13. Developer-to-developer compute

Developer Mac minis can form a high-speed compute cluster. The fast interconnect is used for:
- object movement;
- model shards;
- build artifacts;
- distributed task coordination where beneficial;
- intermediate results.

It does not imply shared memory or transparent remote CPU execution.

## 14. MediaHub contribution

Remote MediaHub contributors use the ordinary external network and the Compute Contribution Plane.

Contributor execution is:
- capability-scoped;
- admission-controlled;
- lease-bound;
- isolated;
- network-restricted;
- result-bounded;
- auditable;
- revocable.

The high-speed developer fabric and the contributor plane are different performance domains.

## 15. GitHub mechanisms

- Linux kernel thunderbolt_net / CONFIG_USB4_NET: high-speed IP transport reference.
- exo: distributed execution and optional macOS RDMA reference.
- Ray: distributed execution and resource scheduling.
- NATS/JetStream: asynchronous durable transport.
- gRPC: bounded control RPC.
- containerd/OCI: worker isolation.
- Buf/Protovalidate: schema governance.
- SPIRE: workload identity patterns.
- Cosign/Sigstore: artifact verification.
- OpenTelemetry: telemetry.
- Netmaker/WireGuard: Development Mesh.
- SeaweedFS: optional developer storage.

External components remain replaceable mechanisms. MediaHub contracts remain authoritative.

## 16. Pushback

1. Do not call Thunderbolt a supercomputer bus. It is a high-speed network/interconnect.
2. More bandwidth does not automatically improve distributed workloads; transfer cost must enter placement.
3. Do not expose the high-speed developer network to MediaHub users.
4. Do not make RDMA mandatory.
5. Do not use physical Thunderbolt connectivity as a security boundary.
6. Do not mix developer and user storage.
7. Mac mini hardware generations, OS versions, controllers, firmware, cables and topology must be qualified per node class.

## 17. Qualification sequence

Phase A: two Mac minis, direct Thunderbolt/USB4, dedicated IP subnet, throughput/RTT benchmark.
Phase B: three or more developer nodes, mixed HIGH_SPEED and DEV_MESH, topology-aware scheduling and link failure tests.
Phase C: one MediaHub contributor, bounded workload, zero user data.
Phase D: partitioned workloads and deterministic merge.
Phase E: optional RDMA benchmark against normal IP; IP remains fallback.

## 18. Acceptance gates

- peer identity verified;
- unauthorized peers rejected;
- high-speed link isolated from MediaHub LAN;
- default route unchanged;
- link failure causes safe re-placement;
- authoritative state survives link loss;
- measured bandwidth/RTT affect placement;
- no user data crosses merely because high-speed connectivity exists;
- distributed results remain deterministic and verifiable.

## 19. Reference topology

Developer Mac mini A <== HIGH_SPEED ==> Developer Mac mini B
          |                                  |
          +---------- DEV_MESH --------------+
                         |
                  Developer Control
                         |
                    Scheduler
                         |
              +----------+----------+
              |                     |
       Developer workers     MediaHub contributors
                                  |
                           ordinary network
                                  |
                         bounded worker/evidence

CPRG remains outside the compute path and retains its separate registration-only contract.

## 20. Final principle

The Cloud Development Fabric is a hierarchical heterogeneous compute environment: fast local interconnects between developer servers, governed contribution from MediaHub nodes, separate storage/security domains, and explicit admission/lease/isolation contracts.