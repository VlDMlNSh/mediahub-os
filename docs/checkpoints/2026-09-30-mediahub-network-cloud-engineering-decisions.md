# MediaHub — Engineering Decisions for Network + Cloud Development Fabric

Date: 2026-09-30
Status: consolidated engineering decision record
Scope: decisions ready for subsequent implementation

## 1. Network hierarchy

Use two independent environments:

LOCAL MEDIAHUB
- user-facing;
- Wi-Fi;
- smart-home;
- media;
- local compute/storage;
- user VPN.

CLOUD DEVELOPMENT
- developer control;
- CI/CD;
- Astra;
- developer compute;
- developer storage;
- admitted MediaHub compute contributors.

Never create a flat global LAN.

## 2. Interface hierarchy

Every node publishes:

INTERNET
DEV_MESH
HIGH_SPEED
optional DEV_STORAGE
optional CPRG

Each interface has a declared plane and policy.

Default route is never selected by hardware speed.

## 3. Local MediaHub network

Ethernet/RJ45 is the normal wired backhaul.

MediaHub can provide Wi-Fi AP functionality where hardware supports it.

Multiple MediaHub nodes cooperate with qualified external APs to provide seamless wireless coverage.

Wired backhaul is preferred over wireless mesh.

## 4. Ubiquiti/Keenetic

Treat these as interoperability targets.

Qualification must separately test:
- common SSID;
- authentication;
- roaming;
- fast roaming;
- controller interaction;
- VLAN;
- failure;
- recovery.

Do not claim generic compatibility from vendor name alone.

## 5. User VPN

Implement VPN as an egress policy.

Required modes:
- OFF;
- VPN;
- VPN_KILL_SWITCH;
- VPN_DIRECT_FALLBACK.

The policy must be visible to the user and enforceable at the gateway.

## 6. Developer HIGH_SPEED

Mac mini developer nodes may use direct Thunderbolt/USB4 IP links.

V1:
- IP transport;
- dedicated subnet;
- gRPC/NATS/Ray;
- no RDMA dependency.

Each physical link is a graph edge.

## 7. Shared Internet between Mac minis

Supported technically as an explicit routing feature.

Recommended default:
- each node has its own WAN;
- HIGH_SPEED has no default route.

Optional:
- one node provides developer-only NAT/forwarding to a peer.

Required:
- explicit capability;
- explicit route;
- firewall;
- bandwidth limit;
- audit;
- failure detection.

Never forward user MediaHub traffic through this path.

## 8. Primary Development Node

Primary is a dynamic role.

Selection:
CPU + GPU/NPU + RAM + NVMe + available capacity + HIGH_SPEED + RTT + reliability + control-plane readiness.

Primary loss triggers role migration.

Primary is not the only authority or state store.

## 9. Developer Mesh

Use Netmaker/WireGuard as first candidate.

Keep Headscale/WireGuard as alternative.

Use DEV_MESH for:
- management;
- discovery;
- control;
- fallback communication.

Use HIGH_SPEED for large data transfers when healthy.

## 10. Developer compute

MediaHub scheduler remains authoritative.

Candidate execution:
Ray.

Candidate isolation:
containerd/OCI, with stronger runtime classes for higher-risk jobs.

Candidate event transport:
NATS/JetStream.

Candidate control:
gRPC.

## 11. Security

Identity:
SPIRE optional.

Artifact:
Cosign/Sigstore.

Network enforcement:
Cilium/eBPF or equivalent.

Telemetry:
OpenTelemetry.

None of these becomes the MediaHub authority.

## 12. DNS/DHCP

CoreDNS is the preferred developer DNS candidate.

Kea is the dedicated DHCP candidate where platform-native DHCP is insufficient.

Discovery never grants authorization.

## 13. Routing

Media Mesh and Development Mesh remain separate.

HIGH_SPEED:
- no default route;
- no automatic forwarding;
- no bridge into Media Mesh.

CPRG:
- registration only;
- not compute;
- not transit.

## 14. Storage

User storage and developer storage are different trust domains.

No shared user storage mount on contributor workers.

## 15. Scheduler

Placement must account for:

T = compute + serialization + input_transfer + output_transfer + scheduling + expected_failure_cost

Measured bandwidth and RTT become scheduling inputs.

## 16. Evidence

Every qualification emits:

- node/interface inventory;
- topology;
- routes;
- firewall state;
- link measurements;
- workload placement;
- failure state;
- recovery result;
- policy identifiers;
- evidence digest.

## 17. Required implementation sequence

1. interface inventory schema;
2. network-plane model;
3. route/policy model;
4. interface discovery;
5. HIGH_SPEED qualification harness;
6. iperf3 evidence adapter;
7. developer topology graph;
8. shared-egress policy;
9. firewall enforcement;
10. scheduler network-cost model;
11. primary-role election/migration;
12. DEV_MESH adapter;
13. local Wi-Fi/AP capability adapter;
14. VPN policy engine;
15. compute protocol integration;
16. Ray adapter;
17. NATS/gRPC adapters;
18. isolation adapter;
19. evidence verifier;
20. full network qualification.

## 18. Components that should NOT be integrated yet

- RDMA;
- full OpenWISP control plane;
- full OpenWrt replacement runtime;
- FRR unless dynamic routing complexity requires it;
- SeaweedFS unless storage scale requires it;
- OpenFGA unless authorization complexity requires it.

Start with the smallest stable mechanism.

## 19. Final engineering position

The system should be implemented as a MediaHub-owned network/control architecture with replaceable open-source mechanisms.

The key reusable technology conclusion is:

Thunderbolt/USB4 -> IP -> controlled routing -> authenticated developer transport -> distributed execution.

This is sufficient for V1.

A Mac mini can therefore be both:
- a developer compute node;
- a high-speed peer;
- and, when explicitly authorized, a developer egress router.

Those roles remain separate capabilities.

## 20. Qualification before production

No production deployment should be declared until the following are measured:

- Wi-Fi coverage;
- roaming;
- vendor interoperability;
- HIGH_SPEED throughput;
- RTT/loss;
- MTU;
- sleep/wake;
- shared egress;
- route isolation;
- IPv6;
- firewall;
- node failure;
- primary migration;
- compute re-placement;
- privacy boundary;
- CPRG isolation.

