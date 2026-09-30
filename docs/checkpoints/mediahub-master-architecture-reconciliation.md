# MediaHub Master Architecture Reconciliation

Date: 2026-09-30
Status: active master checkpoint
Passport: MEDIAHUB OS 11.x LTS / MEDIAHUB iOS — FUNCTIONAL BASELINE 1.0

## Provenance

Repository: VlDMlNSh/mediahub-os
Branch: main

Immutable R4 baseline declared by project history:
- SHA: 471f709f5633feab7aeb62dd3ea52effad6d2bc584
- Tree: 2279612908135418b2b5448d598274ea6741deaa
Verification: the declared R4 SHA was not resolved by the available GitHub API at this checkpoint; it is retained as declared historical provenance and is not rewritten.

## Passport progress

- Section 1 — НАЗНАЧЕНИЕ: functionally reconciled and closed.
- Section 2 — ОСНОВНАЯ АРХИТЕКТУРНАЯ МОДЕЛЬ: functionally reconciled and closed.
- Sections 3–68: unresolved / not started.

## Section 1 — confirmed requirements

### Product

1. MediaHub is one product: a local operating system for buildings.
2. It combines Smart Home, Media, AI, Documents, energy, surveillance, security, climate, networking, integrations and entertainment.
3. Entertainment includes games launched from gaming PCs and supported mainstream consoles.
4. Deployment profiles may differ by building and hardware while remaining one product.
5. Local operation and confidentiality have highest product priority.

### Core capabilities

6. Smart Home is mandatory.
7. Media is a full-node core capability; specialized profiles may provide a reduced/qualified Media capability.
8. Documents is a full-node core capability; specialized profiles may omit it.
9. Local AI is a mandatory product capability, subject to qualified hardware/runtime availability.
10. Core Engineering is mandatory and covers equipment integration, equipment setup, diagnostics and configuration of object systems.
11. Network is core on full Mac mini/mini-PC profiles; specialized profiles may have reduced network-management capabilities.
12. Security, Observability, Backup/Recovery and Update/Migration are core.
13. Surveillance is a core domain. Local recording is a separate hardware-dependent capability.

### Applications / OS surfaces

14. MediaHub iOS OS and MediaHub Remote Access are two completely different applications.
15. MediaHub iOS OS is a hardware-adapted, reduced-capability local MediaHub OS for supported Apple hardware, analogous in product role to a specialized Raspberry Pi MediaHub edition.
16. MediaHub Remote Access is a separate remote-access application family with iOS and Android applications.
17. MediaHub Remote Access is not the MediaHub iOS OS and must not be conflated in identity, contracts, deployment or release architecture.
18. A specialized iPad installation is a MediaHub OS/node, not merely a remote client.
19. iPad may run Local AI and qualified Compute Contribution subject to its hardware/software capability profile.

### Specialized hardware

20. Raspberry Pi and iPad profiles are specialized MediaHub OS deployments.
21. Specialized profiles have hardware-qualified capability sets.
22. Raspberry Pi baseline includes Smart Home, full surveillance/integration/control of available equipment, but local surveillance recording to hard disk is not mandatory.
23. iPad baseline follows the same principle: Smart Home and surveillance/integration/control are required capabilities to the extent supported by hardware/OS; local recording is not mandatory.
24. Hardware independence is a design objective. Capability is determined by qualification, not device name alone.
25. Single-node MediaHub is valid.

### HA / cluster

26. Multiple MediaHub nodes automatically form a cluster.
27. The cluster may provide HA, distributed storage, compute clustering, network mesh and Wi-Fi mesh.
28. If one qualified MediaHub node fails, another qualified node must automatically continue critical functions without manual intervention.
29. Critical availability is tiered: security, access control and surveillance are higher-criticality; climate and energy are also critical. Media/AI/entertainment are lower tiers unless later requirements elevate them.
30. Critical functions must remain operational, to the qualified extent of the deployment, through Internet failure, Cloud failure, one-node failure, partial LAN failure, primary-AI failure and one-storage-component failure.
31. HA implementation topology (active/passive, active/active, quorum, replication, storage and failure domains) remains a later architecture decision.
32. Multiple MediaHub nodes may require multiple Home Assistant Core instances. The architecture must define clustered Smart Home authority, replication, split-brain prevention and failover rather than assuming a single HA instance remains the only runtime.

### Network / VPN

33. MediaHub may act as Gateway, Router, Firewall, DHCP, DNS, AP, Controller, Media Server and Smart Home Node, subject to role separation and qualification.
34. Personal VPN is a MediaHub Gateway function.
35. MediaHub may apply per-client/per-network routing policy selecting VPN or direct paths. Protocol, provider and detailed policy remain later decisions.

### Engineering / Digital Twin

36. Digital Twin and advanced Engineering are paid functional extensions.
37. Paid scope includes full object model, CAD/BIM, spatial model, simulation, engineering workflows, advanced AI engineering, engineering-network diagrams, cable schedules, as-built documentation and generation of project packages for electrical supply, automation, ventilation, HVAC, heating, water supply, low-voltage systems, energy and backup power.
38. Exact subscription entitlements and enforcement remain later implementation decisions.

### Cloud Development

39. Cloud Development Environment is part of the broader MediaHub ecosystem but is a separate security/control domain from MediaHub OS and its State Authority.
40. Cloud capabilities include development, backup, remote access, notifications, optional AI, model registry, software distribution, telemetry, disaster recovery, cloud storage and compute.
41. Cloud Development cannot override canonical local MediaHub state.

### Compute Contribution

42. Compute Contribution is intended for every MediaHub deployment, subject to capability, opt-in, admission, lease, isolation, revocation, audit and network restrictions.
43. It supports development acceleration, distributed AI, CI/build, inference, training, rendering, simulation, data processing, storage processing and approved company development workloads.
44. Compute Contribution != User Data Access != Developer Personnel Access.

## Section 2 — ОСНОВНАЯ АРХИТЕКТУРНАЯ МОДЕЛЬ

### Confirmed requirements

1. MediaHub has one unified software core and one unified contract model across hardware profiles.
2. MediaHub does not require identical hardware capabilities across installations.
3. Every installation must undergo hardware detection and hardware-profile qualification.
4. Available functions are determined by the qualified hardware profile, not by product name alone.
5. Missing hardware capability does not create a different MediaHub architecture; the corresponding capability is unavailable in that profile.
6. The architecture is one product architecture over heterogeneous qualified hardware profiles.
7. Domain boundaries and deployment boundaries are distinct: a domain is a logical responsibility/contract boundary; a deployment is a concrete runtime/hardware placement.
8. Security / Identity / Trust uses a centralized control-plane model with enforcement points inside each domain.
9. MediaHub API direction is a unified API gateway plus versioned domain contracts; this remains preliminary until contract and API sections are reconciled.
10. Mobile canonical model is fixed: MediaHub Core iOS/iPadOS is a local full-minimal MediaHub OS edition; MediaHub iOS Remote / Android Remote is a separate remote-access application.
11. Cloud interaction follows the controlled boundary: MediaHub -> Security / Egress Gateway -> AI Gateway -> Cloud Development AI.
12. Cluster formation starts with automatic discovery, then proposal, then explicit user confirmation before cluster formation.
13. For clean installations on Mac mini and Mini PC, Linux is the baseline platform under consideration.
14. In parallel, MediaHub is developed as an adaptable system for macOS, iPadOS and Raspberry Pi.

### Decisions

- Unified architecture, unified contracts, heterogeneous hardware capability profiles.
- Hardware qualification is a prerequisite for declaring a capability available on an installation.
- Hardware Abstraction Layer is an architectural mechanism for keeping domain contracts independent from physical hardware differences.
- A hardware profile is a qualified capability description, not a separate product architecture.
- macOS/iPadOS/Raspberry Pi adaptations remain implementations of the same MediaHub architecture; clean Mac mini/Mini PC installations use Linux as the baseline platform under consideration.
- Security/Identity/Trust is a control plane, but enforcement is distributed to the domains that execute protected operations.
- Cloud Development is never reached by an uncontrolled direct path from local domains; egress and AI policy gates mediate the path.
- Automatic discovery alone does not authorize cluster formation; explicit user confirmation is required.

### Rationale

The architecture must support Mac mini, Mini PC, Raspberry Pi and iPad without creating incompatible architectural branches. Hardware differences are therefore represented as qualified capabilities behind a common abstraction and contract surface. This preserves one product architecture while allowing capability reduction or extension by hardware.

### Constraints

- No architectural fork merely because a device lacks a capability.
- No capability may be advertised as available without hardware/runtime qualification.
- Linux for clean Mac mini/Mini PC installations is a baseline platform direction, not yet a final OS semantic definition for the MediaHub OS product.
- macOS, iPadOS and Raspberry Pi support must preserve the same canonical domain and contract model where platform constraints permit.
- Physical hardware must not become an implicit authority or bypass domain contracts.
- Security control-plane centralization must not become a single enforcement point or single point of failure.
- The cloud boundary must preserve Local First and confidentiality-first requirements.

### Invariants

- MediaHub Architecture = one architecture + one contract model + qualified hardware profiles.
- Capability availability = hardware/software qualification result.
- Missing capability != alternate architecture.
- Domain != deployment.
- Security / Identity / Trust = centralized control plane + distributed enforcement.
- Remote Access != local Core.
- MediaHub Core iOS/iPadOS != remote client.
- Cluster formation = discovery -> proposal -> user confirmation -> formation.
- Cloud access = Security/Egress Gateway -> AI Gateway -> Cloud Development AI.
- Cloud != local State Authority.
- Local First.
- Unknown/ambiguous protected state follows existing DENY/QUARANTINE / FAIL CLOSED rules.

### Affected components

Hardware / Platform, MediaHub OS Core, State Authority, Security / Identity / Trust, MediaHub API, Local AI, Local Cluster AI, Cloud Development AI, Mobile/Core iPadOS, Remote Access, Network System, Cluster formation and qualification.

### Open questions carried forward

1. Exact semantic definition of MediaHub OS across Linux, macOS, iPadOS and Raspberry Pi: operating-system image, distribution/system layer, or unified platform with platform-specific system implementations.
2. Exact State Authority topology across multiple MediaHub nodes: replication, leader/authority semantics, conflict handling, quorum, split-brain prevention and failover.
3. Exact scope of automatic cluster formation: compute, storage, Smart Home, network/mesh, redundancy, or a qualified subset of these capabilities.
4. Exact API Gateway topology and trust model.
5. Exact Security/Egress Gateway implementation and separation from network gateway/firewall roles.
6. Exact Hardware Abstraction Layer boundaries and capability-schema format.

## Architecture invariants

- MediaHub State Authority = canonical platform authority; it is not governmental authority.
- Home Assistant Core = Smart Home authority.
- AI != authority.
- MediaHub Remote Access != authority.
- MediaHub iOS OS node != authority.
- Cloud != authority over canonical MediaHub state.
- Scheduler != authority.
- OSS component != authority.
- Developer Cluster != authority.
- Local First.
- Unknown device => DENY/QUARANTINE.
- Ambiguous state => FAIL CLOSED.
- CPRG remains registration-only.
- Integration = Contract -> Adapter -> Validation -> Integration -> Qualification.
- Security boundaries cannot depend only on physical connectivity.
- User confidentiality takes precedence over convenience.
- Hardware profile determines capabilities.
- MediaHub iOS OS and MediaHub Remote Access are separate applications.

## Final Section 1 status

Section 1 product requirements are sufficiently reconciled to proceed to Section 2. Section 2 is now functionally reconciled for the confirmed hardware-profile and unified-architecture principle. Remaining OS semantic, State Authority topology, cluster scope, API and security-gateway details are explicitly carried forward and must be resolved in their relevant passport sections.

## Deferred decisions

- exact HA topology and qualification;
- exact critical SLOs;
- exact hardware capability matrix;
- VPN protocol/provider and detailed routing policy;
- subscription enforcement mechanics;
- detailed capability matrix for Media/Entertainment/Documents on specialized profiles;
- exact semantic definition of MediaHub OS across target platforms;
- State Authority multi-node topology;
- exact cluster formation scope;
- final API Gateway topology;
- final Security/Egress Gateway topology;
- Hardware Abstraction Layer and capability-schema specification.

## Rejected / corrected interpretations

- State Authority does not mean governmental authority.
- iPad MediaHub OS is not the remote-access application.
- MediaHub iOS OS and MediaHub Remote Access are separate applications.
- Surveillance capability and local recording are separate requirements.
- Media is not the sole product center.
- Cloud Development is not canonical local authority.
- Hardware-specific capability differences do not justify separate MediaHub architectures.
