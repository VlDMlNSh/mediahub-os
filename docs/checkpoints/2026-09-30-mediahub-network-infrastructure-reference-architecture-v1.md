# MediaHub Network Infrastructure — Reference Architecture v1

Date: 2026-09-30
Status: normative architecture baseline for subsequent implementation
Scope: Local MediaHub network + developer network interfaces + controlled interconnection to the Cloud Development Fabric
Production deployment: not authorized by this document

## 1. Architecture objective

MediaHub has two materially different network environments:

1. Local MediaHub Network — user-facing network providing wired Internet/backhaul, Wi-Fi coverage extension, local services, smart-home integration, media services and optional user VPN.
2. Cloud Development Network — developer/company environment providing control, development compute, storage, CI/CD, Astra and the distributed development compute fabric.

They must never collapse into one flat network.

The network architecture therefore uses separate logical planes, explicit routing, identity and policy boundaries.

## 2. Canonical planes

### User/local planes

- WAN/Internet
- LAN/Media Mesh
- Wi-Fi Access
- Smart-Home/IoT
- Media Services/Storage
- Guest/Untrusted Client
- User VPN overlay

### Developer planes

- DEV_MESH — private management/control/discovery
- HIGH_SPEED — direct developer-node interconnect
- DEV_STORAGE — optional high-throughput storage path
- DEV_EGRESS — ordinary developer Internet egress
- COMPUTE_CONTRIBUTION — logical security domain for admitted MediaHub compute
- CPRG_REGISTRATION — request-scoped protected registration path

These are logical/security planes. A physical interface may carry more than one plane only when explicit VLAN/VRF/firewall policy makes the separation enforceable.

## 3. MediaHub local topology

Baseline:

                    Internet/WAN
                         |
                    Ethernet/RJ45
                         |
                 +-------+-------+
                 | MediaHub node |
                 +-------+-------+
                    |         |
                 Wi-Fi      local LAN
                    |         |
              clients      smart-home
                    |         |
                    +---- MediaHub ----+
                         media/services

Multiple nodes:

             Ethernet/LAN backhaul
                 /           \
        MediaHub A           MediaHub B
          /    \               /    \
       Wi-Fi  services      Wi-Fi  services

The desired user experience is one seamless local wireless environment. The implementation must distinguish AP operation, controller functions, roaming, channel coordination and actual wireless mesh.

## 4. MediaHub interfaces

A MediaHub node may expose:

- WAN/LAN Ethernet
- Wi-Fi radio(s)
- optional additional Ethernet
- optional management interface
- local storage interfaces
- application/service interfaces

The network daemon must discover actual hardware capabilities rather than assuming that every MediaHub SKU can act as an AP, gateway, switch or wireless mesh node.

No interface is allowed to become a default route merely because it exists.

## 5. Wi-Fi architecture

MediaHub is a first-class Wi-Fi infrastructure participant.

Required capabilities:

- AP mode where hardware permits;
- common SSID/network identity;
- secure client authentication;
- roaming support;
- optional fast-roaming qualification;
- coordinated channel selection where supported;
- wired backhaul preferred;
- actual wireless mesh only when wired backhaul is unavailable or intentionally selected.

External AP interoperability targets:

- Ubiquiti;
- Keenetic;
- future qualified vendors.

Controller logic is separate from radio hardware.

MediaHub may host controller/gateway functions when technically and legally compatible. It does not imply that proprietary vendor firmware/controller software can simply be embedded or replaced.

## 6. Network segmentation

Recommended logical zones:

- MGMT — device/control administration
- HOME — trusted local user devices
- IOT — smart-home devices
- MEDIA — MediaHub media services
- CAMERA — surveillance
- SECURITY — security/fire/fire/intercom/access devices
- GUEST — untrusted clients
- VPN_CLIENT — traffic selected for user VPN
- DEV — never directly bridged to HOME/IOT
- CPRG — registration-only protected path

Inter-zone access is default-deny and opened only by explicit service policy.

Examples:

HOME -> MEDIA: allowed service-specific
IOT -> MEDIA: only required media/service APIs
CAMERA -> MEDIA: only required recording/management paths
GUEST -> HOME: denied
GUEST -> MGMT: denied
IOT -> MGMT: denied
DEV -> HOME/IOT/MEDIA: denied by default
CPRG -> local data plane: denied

## 7. User VPN

The personal paid VPN is an egress policy, not a replacement for local segmentation.

Traffic flow:

Client -> Wi-Fi/LAN -> policy engine -> VPN tunnel -> VPN provider -> Internet

The policy engine selects traffic by:

- client;
- SSID/VLAN;
- destination;
- service class;
- explicit user policy.

The system must define:

- tunnel up/down;
- DNS behavior;
- route installation;
- kill-switch mode;
- fallback-to-direct mode;
- reconnection;
- status reporting.

Default recommendation for implementation: fail closed for traffic explicitly assigned to VPN when the user has enabled kill-switch mode; allow explicit direct fallback only when selected by policy.

No specific VPN provider is selected.

## 8. Remote user application

The user mobile application and iPad wall panel are application clients, not privileged network bridges.

Remote access must use an authenticated application/service channel rather than exposing the entire local LAN.

Required properties:

- mutually authenticated or strongly authenticated client sessions;
- authorization by resource/action;
- reconnect;
- session expiry;
- push/notification channel where needed;
- audit;
- no unrestricted LAN tunneling by default.

Local operation must continue if remote access is unavailable.

## 9. Developer network

Developer servers form a separate Cloud Development Fabric.

Every developer node should be modeled with measured interface capabilities:

| Interface | Function | Default route | Security |
|---|---|---|---|
| INTERNET | ordinary WAN | possible | host firewall |
| DEV_MESH | control/management | no | encrypted/authenticated |
| HIGH_SPEED | node-to-node compute/data | no | dedicated ACL/firewall |
| DEV_STORAGE | storage | no | storage ACL |
| CPRG | registration only where explicitly applicable | no | request-scoped |

HIGH_SPEED is not a default gateway.

## 10. Primary Development Node

The primary development node is a dynamic role.

Selection must consider:

- CPU;
- GPU/NPU;
- RAM;
- NVMe throughput;
- available compute;
- HIGH_SPEED links;
- measured bandwidth/RTT;
- storage;
- reliability;
- uptime;
- control-plane readiness.

The strongest raw CPU is therefore not automatically the primary.

The primary role may migrate without changing node identity.

The primary is not a single point of authority and must not be the only place where developer state exists.

## 11. Mac mini high-speed topology

Baseline for Mac mini developer nodes:

Mac mini A ===== USB4/Thunderbolt ===== Mac mini B
      |                                      |
   DEV_MESH ----------------------------- DEV_MESH
      |                                      |
   INTERNET ----------------------------- INTERNET

The HIGH_SPEED link is treated as an IP network interface.

Linux mainline explicitly provides USB4/Thunderbolt networking via USB4_NET/thunderbolt_net and describes communication between computers over USB4/Thunderbolt, including Apple ThunderboltIP interoperability with macOS and Windows.

The link is therefore a viable V1 high-speed IP transport.

Do not assume arbitrary Thunderbolt cabling creates a multi-node Ethernet switch.

For N developer nodes:

- use a controlled topology;
- model every physical high-speed edge;
- assign a dedicated subnet/address;
- discover link state;
- record measured capacity;
- use topology-aware placement.

## 12. Shared Internet over HIGH_SPEED

A developer node can technically forward IP traffic from another developer node through a Thunderbolt/USB4 IP link.

This enables:

Mac mini A
  INTERNET
     |
  routing/NAT
     |
 HIGH_SPEED
     |
Mac mini B
     |
developer Internet

However this is NOT the normal V1 topology.

Rules:

1. Each developer node should preferably have independent Internet connectivity.
2. HIGH_SPEED must not install a default route automatically.
3. Internet sharing is an explicit developer-network capability.
4. If enabled, routing/NAT/firewall policy is explicit.
5. The egress node must not become an accidental transit router for MediaHub user traffic.
6. Egress policy must be represented in node capability metadata.
7. Loss of the shared egress must not corrupt compute state.
8. Scheduler must account for the shared egress bottleneck.
9. Developer Internet and user VPN are different functions.
10. MediaHub user traffic must never be forwarded through the developer HIGH_SPEED fabric.

### Valid use cases

- temporary bootstrap when one developer node has WAN and another does not;
- controlled common egress for isolated developer workloads;
- bandwidth-limited artifact retrieval;
- lab environments where one node is intentionally the egress router.

### Invalid default

All developer nodes route their normal Internet through the primary merely because it has the strongest hardware.

Network throughput, not CPU strength, determines egress usefulness.

## 13. HIGH_SPEED security

Physical Thunderbolt/USB4 attachment is not trust.

Required:

- node identity;
- authenticated control channel;
- dedicated interface/subnet;
- host firewall;
- default-deny forwarding;
- explicit service ports;
- no bridge to HOME/IOT/MEDIA;
- peer authorization;
- unauthorized-peer quarantine;
- link-state monitoring.

A high-speed link may carry developer compute traffic only after both endpoints satisfy identity and policy requirements.

## 14. Developer compute fabric

Developer workload path:

Scheduler
  |
  +-- local execution
  +-- HIGH_SPEED developer peer
  +-- DEV_MESH peer
  +-- admitted MediaHub contributor
  +-- explicitly authorized external compute

Placement cost includes:

- compute estimate;
- serialization;
- input transfer;
- output transfer;
- bandwidth;
- RTT;
- contention;
- failure/retry penalty.

A workload should remain local when distribution costs more than useful parallelism.

## 15. MediaHub compute contribution

MediaHub nodes can contribute idle CPU/GPU/NPU capacity to the developer fabric only through the Compute Contribution Plane.

Contribution is:

- opt-in;
- capability-scoped;
- lease-bound;
- isolated;
- network-restricted;
- auditable;
- revocable.

Compute contribution does not create a route from developer nodes into the MediaHub LAN.

No shared subnet is required between user Media Mesh and developer compute contributors.

## 16. CPRG

CPRG remains separate.

The only VPN-backed CPRG use is API-key registration.

CPRG is not:

- a general Internet gateway;
- a developer compute node;
- a MediaHub media gateway;
- a permanent VPN transit network;
- a route between HIGH_SPEED and Media Mesh.

The CPRG path is request-scoped, authenticated, leased, audited and closed after registration.

## 17. Routing policy

Default routes:

- MediaHub user network -> user's normal Internet gateway or selected VPN policy.
- Developer node -> its own Internet gateway.
- HIGH_SPEED -> no default route.
- DEV_MESH -> no default route.
- DEV_STORAGE -> no default route.
- CPRG -> registration-only route/policy.

Specific routes are installed only for their owning plane.

No automatic route redistribution between planes.

## 18. Addressing model

The final deployment may choose another private address plan, but the reference architecture reserves separate ranges conceptually:

- Media Mesh: 10.10.0.0/16
- Development Mesh: 10.20.0.0/16
- HIGH_SPEED: 10.30.0.0/24 or per-link /31-/30 style subnets
- Storage: 10.40.0.0/16
- CPRG protected path: dedicated isolated range

These are architecture examples, not production addresses.

IPv6 must be supported in the design. The implementation must avoid assuming IPv4-only semantics.

## 19. DNS/DHCP/service discovery

Recommended division:

- DHCP: Kea or platform-native equivalent;
- authoritative/service DNS: CoreDNS or platform-native equivalent;
- local mDNS/service discovery: Avahi/Bonjour-compatible mechanism where required;
- developer private discovery: DEV_MESH-specific DNS/service registry.

Discovery must never grant authorization.

A discovered service is still unauthorised until identity/policy checks succeed.

## 20. Routing stack candidates

For advanced developer routing, FRRouting is a candidate mechanism.

For encrypted developer mesh:

- Netmaker/WireGuard is the primary candidate for evaluation;
- Headscale is an alternative narrow self-hosted control-plane candidate;
- direct HIGH_SPEED remains preferred for large developer-to-developer transfers.

Neither Netmaker nor Headscale becomes the MediaHub authority.

## 21. Wi-Fi/network-control candidates

Candidate mechanisms:

- OpenWrt — router/AP/network OS building blocks;
- OpenWISP — centralized network-management building blocks;
- vendor-native Ubiquiti/Keenetic mechanisms where interoperability permits.

MediaHub should reuse stable protocol/control ideas and small compatible modules rather than importing an entire external control plane.

OpenWrt is especially relevant as a reference for AP/router/network configuration and package-driven embedded networking. It is not automatically suitable as the MediaHub runtime.

## 22. Developer transport and execution candidates

Use existing stable components as adapters:

- gRPC — bounded control RPC;
- NATS/JetStream — asynchronous events and redelivery;
- Ray — execution backend;
- containerd/OCI — worker isolation;
- Cilium/eBPF or equivalent — execution-boundary network enforcement;
- SPIRE — optional workload identity;
- Cosign/Sigstore — artifact verification;
- OpenTelemetry — telemetry vocabulary.

MediaHub-owned contracts remain authoritative.

## 23. Storage

Separate:

1. user MediaHub storage;
2. developer engineering storage;
3. ephemeral execution workspace.

HIGH_SPEED may carry developer storage traffic but never creates a shared user-data namespace.

## 24. Failure model

### HIGH_SPEED down

- remove link from scheduler placement;
- keep control through DEV_MESH if available;
- continue local jobs;
- re-place partitionable work;
- do not alter default route.

### Developer Internet down

- local developer-to-developer compute can continue;
- jobs not requiring external resources continue;
- artifact/provider operations are deferred or fail according to policy.

### Primary node down

- primary role is re-elected;
- developer state must survive;
- scheduler authority must not depend on one physical machine.

### Wi-Fi MediaHub node down

- affected coverage decreases;
- neighboring qualified APs continue;
- controller/service state remains available according to deployment mode.

### WAN down at MediaHub

- local smart-home/media/control continues;
- remote application access may become unavailable;
- user VPN cannot provide Internet without WAN;
- local LAN must not depend on cloud connectivity.

## 25. Qualification stages

### N1 — Interface inventory
Record every physical/logical interface per node.

### N2 — L2/L3
Verify addresses, MTU, routes, VLAN/VRF and firewall.

### N3 — Wi-Fi
AP, roaming, coverage, backhaul and client isolation.

### N4 — Developer HIGH_SPEED
Two-node Thunderbolt/USB4 link, IP, throughput, RTT, loss, MTU, reconnect.

### N5 — Shared developer egress
Controlled IP forwarding/NAT over HIGH_SPEED; verify no accidental route leakage.

### N6 — Multi-node developer fabric
Topology discovery, scheduler placement, link failure and re-placement.

### N7 — Compute contribution
One MediaHub contributor, no user-data transfer.

### N8 — Security
Unauthorized peer, LAN escape, route escape, CPRG escape, identity failure.

### N9 — Failure/recovery
Primary loss, link loss, WAN loss, node reboot, sleep/wake.

### N10 — Evidence
Machine-readable evidence bundle for every gate.

## 26. Hard acceptance gates

The architecture is not production-qualified until:

- local and developer networks are demonstrably separate;
- no unintended route bridges Media Mesh and Development Mesh;
- HIGH_SPEED has no accidental default route;
- shared Internet requires explicit policy;
- user VPN is isolated from developer VPN/mesh;
- Wi-Fi roaming behavior is measured;
- Ubiquiti/Keenetic interoperability is tested rather than assumed;
- developer node identity is verified;
- unauthorized HIGH_SPEED peers are rejected;
- MediaHub contributors cannot reach user LAN/storage;
- CPRG cannot become transit;
- link failure does not corrupt authoritative state;
- primary-node migration works;
- IPv4/IPv6 behavior is known;
- DNS/DHCP failure modes are understood;
- evidence is reproducible.

## 27. Non-goals

This document does not authorize:

- production network deployment;
- firmware replacement on customer hardware;
- vendor controller redistribution without license review;
- automatic VPN-provider selection;
- general-purpose VPN tunneling;
- flat L2 across MediaHub and developer networks;
- automatic Internet sharing between developer nodes;
- RDMA as a correctness dependency.

## 28. Final architecture principle

MediaHub local networking is a user-facing service fabric.

The Cloud Development Fabric is a separate developer environment.

HIGH_SPEED connects developer nodes for measured, authenticated, topology-aware data and compute movement.

Thunderbolt/USB4 can also carry controlled developer Internet traffic because it is an IP-capable link, but this must remain an explicit routing capability, not an implicit default.

The system should use proven open-source mechanisms where they reduce engineering risk, while keeping MediaHub identity, authorization, privacy, lease, state and evidence contracts under MediaHub control.
