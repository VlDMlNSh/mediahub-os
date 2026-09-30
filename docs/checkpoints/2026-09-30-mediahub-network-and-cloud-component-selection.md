# MediaHub Network + Cloud Development — Reusable GitHub Components and Engineering Patterns

Date: 2026-09-30
Status: engineering component-selection baseline
Scope: reusable open-source components, code patterns and architectural mechanisms
Production integration: not authorized

## 1. Selection principle

Do not import an entire external control plane merely because it appears to solve a nearby problem.

Use external projects as:
- stable protocol references;
- reusable libraries;
- isolated adapters;
- benchmark/qualification tools;
- small implementation blocks;
- operational mechanisms behind MediaHub-owned contracts.

MediaHub retains authority over identity, admission, privacy, lease, routing policy, state and evidence.

## 2. Network infrastructure candidates

### OpenWrt
Repository: https://github.com/openwrt/openwrt

Use for:
- router/AP architecture reference;
- Linux networking configuration patterns;
- package-driven network functions;
- firewall/routing/Wi-Fi integration patterns.

Potential integration:
- selected packages/configuration patterns;
- hardware qualification reference.

Do not:
- make OpenWrt the MediaHub authority;
- assume every MediaHub hardware platform can run it;
- replace vendor firmware without hardware/license qualification.

### OpenWISP
Repository: https://github.com/openwisp/openwisp-controller

Use for:
- centralized network-management concepts;
- device provisioning/configuration patterns;
- controller/API patterns.

Potential integration:
- selected controller data models and management ideas;
- adapter for qualified AP classes.

Do not:
- automatically adopt OpenWISP as the MediaHub control plane.

### BATMAN-adv
Linux kernel/project family for Layer-2 wireless mesh.

Use only if actual wireless mesh is required after wired-backhaul qualification.

Important distinction:
- seamless roaming != wireless mesh;
- AP controller != mesh routing;
- common SSID != mesh.

V1 should prefer wired Ethernet backhaul.

## 3. Development Mesh candidates

### Netmaker
Repository: https://github.com/gravitl/netmaker

Observed capabilities from its repository:
- WireGuard network automation;
- mesh VPN;
- remote-access gateways;
- site-to-site;
- private DNS;
- ACL;
- Linux/Mac support.

Recommended role:
- Development Mesh adapter/control plane.

Not allowed role:
- Media Mesh authority;
- CPRG replacement;
- user-data gateway;
- default route for all MediaHub traffic.

License review is mandatory before embedding/distributing.

### Headscale
Repository: https://github.com/juanfont/headscale

Observed model:
- self-hosted control server for a Tailscale-compatible WireGuard overlay;
- narrow single-tailnet scope;
- node addressing and route advertisement.

Recommended role:
- alternative Development Mesh control-plane candidate.

Not allowed role:
- local Wi-Fi controller;
- user LAN bridge;
- CPRG replacement.

Headscale's own repository says its scope is a single self-hosted tailnet, which makes it conceptually attractive for a bounded developer mesh rather than a universal MediaHub network.

### WireGuard
Repository: https://github.com/WireGuard/wireguard-go

Use:
- VPN protocol implementation/reference;
- protected developer management links;
- user VPN implementation where protocol support and platform constraints permit.

Do not equate encrypted transport with authorization.

## 4. Routing

### FRRouting
Repository: https://github.com/FRRouting/frr

Use:
- dynamic routing where multiple developer network paths require it;
- route-policy experimentation;
- topology-aware routing in larger developer installations.

V1 may not need FRR if static/policy routing is sufficient.

## 5. DNS and DHCP

### CoreDNS
Repository: https://github.com/coredns/coredns

Use:
- developer/private DNS;
- service discovery support;
- split DNS;
- controlled forwarding.

CoreDNS supports pluggable DNS functions and multiple transports; use only the required subset.

### Kea
Repository: https://github.com/isc-projects/kea

Use:
- DHCP services where a dedicated DHCP service is justified;
- leases/reservations and network provisioning.

Do not introduce a dedicated DHCP service on every MediaHub node unnecessarily. Platform-native DHCP can be preferable for small installations.

## 6. Network qualification

### iperf3
Repository: https://github.com/esnet/iperf

Use:
- HIGH_SPEED throughput;
- ordinary Ethernet throughput;
- TCP/UDP/SCTP measurement;
- JSON evidence;
- regression benchmarks.

The repository explicitly supports Linux/macOS/FreeBSD and measures achievable bandwidth, loss and related parameters.

Use it as a qualification instrument, not as a runtime dependency.

## 7. High-speed Mac mini interconnect

### Linux Thunderbolt/USB4 networking

Linux mainline:
https://github.com/torvalds/linux/blob/master/drivers/net/thunderbolt/Kconfig

The kernel configuration defines USB4_NET for networking between computers over USB4/Thunderbolt and describes Apple ThunderboltIP interoperability with macOS and Windows.

Engineering conclusion:
- USB4/Thunderbolt is suitable as an IP high-speed link candidate;
- use a dedicated interface/subnet;
- do not assume arbitrary multi-node switching;
- measure each link.

### Shared Internet over Thunderbolt/USB4

IP forwarding can be layered over the high-speed interface.

Use cases:
- controlled temporary developer egress;
- bootstrap;
- lab-only shared Internet;
- isolated artifact retrieval.

Do not:
- install a default route through the primary automatically;
- route MediaHub user traffic through developer nodes;
- use shared egress as a substitute for proper developer WAN connectivity.

## 8. Developer compute

### Ray
Repository: https://github.com/ray-project/ray

Use:
- ExecutionBackend adapter;
- distributed tasks/actors;
- resource-aware placement;
- object movement.

MediaHub remains responsible for:
- admission;
- privacy;
- lease;
- fencing;
- execution authorization;
- evidence.

### NATS
Repository: https://github.com/nats-io/nats-server

Use:
- asynchronous control/event transport;
- JetStream for durable delivery where required;
- bounded event streams.

Never treat transport acknowledgement as authoritative state commit.

### gRPC
Repository: https://github.com/grpc/grpc-go

Use:
- bounded synchronous control APIs;
- deadlines;
- cancellation;
- metadata/interceptors.

No unbounded RPC for long-running jobs.

## 9. Isolation

### containerd
Repository: https://github.com/containerd/containerd

Use:
- worker lifecycle;
- image/runtime management.

### OCI Runtime Spec
Repository: https://github.com/opencontainers/runtime-spec

Use:
- portable process/filesystem/resource isolation contract.

For higher-risk workloads, provide a stronger isolation class such as microVM/KVM. OCI is not automatically sufficient for hostile workloads.

## 10. Identity

### SPIRE
Repository: https://github.com/spiffe/spire

Use:
- optional workload identity issuance/attestation mechanism.

MediaHub node identity remains the authoritative application identity.

## 11. Network enforcement

### Cilium
Repository: https://github.com/cilium/cilium

Use:
- identity-aware network policy mechanisms;
- eBPF enforcement concepts;
- execution-boundary policy where supported.

Do not make Cilium the policy authority. The scheduler supplies a policy; the worker enforces it.

## 12. Storage

### SeaweedFS
Repository: https://github.com/seaweedfs/seaweedfs

Use:
- developer engineering storage substrate;
- large-object/data staging where justified.

Never use it as an implicit shared mount for user MediaHub storage.

## 13. Schema and validation

### Buf
Repository: https://github.com/bufbuild/buf

Use:
- Protobuf build;
- lint;
- code generation;
- breaking-change checks.

### Protovalidate
Repository: https://github.com/bufbuild/protovalidate

Use:
- semantic message validation.

Together these provide a strong implementation path for the existing MediaHub compute protocol.

## 14. Artifact trust

### Cosign
Repository: https://github.com/sigstore/cosign

Use:
- artifact signature verification;
- provenance integration.

Artifact digest and policy binding remain MediaHub responsibilities.

## 15. Observability

### OpenTelemetry
Repository: https://github.com/open-telemetry/opentelemetry-specification

Use:
- trace/span context;
- cross-service correlation;
- standard observability vocabulary.

Do not put credentials, personal data or raw user payloads into telemetry.

## 16. Component matrix

| Need | Candidate | Integration form | Authority |
|---|---|---|---|
| AP/router substrate | OpenWrt | selected blocks/reference | MediaHub |
| network management | OpenWISP | adapter/patterns | MediaHub |
| dev mesh | Netmaker | external adapter | MediaHub |
| dev mesh alternative | Headscale | external adapter | MediaHub |
| VPN primitive | WireGuard | protocol/runtime | MediaHub |
| dynamic routing | FRR | optional service | MediaHub |
| DNS | CoreDNS | service | MediaHub |
| DHCP | Kea | service where needed | MediaHub |
| bandwidth qualification | iperf3 | test tool | MediaHub |
| compute | Ray | ExecutionBackend | MediaHub |
| async transport | NATS | EventTransport | MediaHub |
| control RPC | gRPC | transport | MediaHub |
| isolation | containerd/OCI | ExecutionBackend | MediaHub |
| identity | SPIRE | identity adapter | MediaHub |
| network enforcement | Cilium | execution-boundary adapter | MediaHub |
| storage | SeaweedFS | developer storage adapter | MediaHub |
| schemas | Buf | build/CI tool | MediaHub |
| semantic validation | Protovalidate | validator | MediaHub |
| artifacts | Cosign | verifier | MediaHub |
| telemetry | OpenTelemetry | observability | MediaHub |

## 17. Integration strategy

Stage 1:
- MediaHub protocol and state machine;
- Linux/macOS interface inventory;
- iperf3 qualification;
- direct HIGH_SPEED IP.

Stage 2:
- gRPC/NATS adapters;
- deterministic scheduler;
- network policy enforcement.

Stage 3:
- Ray adapter;
- containerd/OCI execution;
- artifact verification.

Stage 4:
- Development Mesh using Netmaker or Headscale;
- CoreDNS/FRR only if complexity requires them.

Stage 5:
- Wi-Fi/AP management adapters;
- OpenWrt/OpenWISP-derived mechanisms after hardware/vendor qualification.

Stage 6:
- optional RDMA;
- advanced storage;
- topology-aware optimization.

## 18. Licensing and distribution gate

Every component must pass:
- license compatibility review;
- dependency/license inventory;
- security review;
- update/maintenance assessment;
- binary/source distribution implications.

No component becomes part of the MediaHub product solely because its GitHub repository is public.

## 19. Final selection principle

Prefer:
1. stable, narrowly scoped components;
2. replaceable adapters;
3. existing standards/protocols;
4. measurable behavior;
5. MediaHub-owned authority.

Avoid:
- monolithic external control planes;
- opaque vendor dependencies;
- physical-network assumptions as security;
- automatic route sharing;
- importing entire platforms when a small mechanism is enough.
