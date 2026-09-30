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

### Q11 — semantic model of MediaHub OS

**Decision: C — hybrid platform model.**

MediaHub OS is one product/platform architecture. On supported hardware where clean system installation is possible, MediaHub may provide its own system installation based on the qualified underlying platform; Linux is the baseline for clean Mac mini/Mini PC installations. Where the platform constrains replacement of the base OS, including Apple platforms, MediaHub operates as a deeply integrated system platform/adaptation over the platform OS while preserving the same canonical MediaHub domains, contracts, security model and authority model.

This does not create separate MediaHub architectures. Platform-specific system implementations are deployment mechanisms for the same architecture.

### Q12 — State Authority across multiple nodes

**Decision: C — one logical distributed State Authority.**

With multiple MediaHub nodes, State Authority remains a single logical canonical authority, physically distributed across qualified nodes. Leadership, replication, quorum, conflict handling, failover and split-brain prevention are implementation mechanisms of that one authority, not separate authorities.

No node may create an independent competing State Authority. Exact topology remains subject to later qualification.

### Q13 — cluster scope

**Decision: 9 — the complete qualified cluster model.**

After automatic discovery, capability qualification and explicit user confirmation, the MediaHub cluster may form all applicable qualified cluster subsystems:

1. compute;
2. storage;
3. Smart Home;
4. network / mesh;
5. Wi-Fi mesh;
6. critical-function redundancy / HA;
7. distributed AI;
8. distributed media;
9. other qualified cluster capabilities defined by the architecture.

The cluster is therefore a unified logical MediaHub cluster with capability-specific distributed subsystems. A subsystem is formed only when its required capabilities, trust, contracts, topology and qualification conditions are satisfied. A missing capability reduces the cluster capability set; it does not create another architecture.

### Section 2 — final reconciliation

Section 2 is closed. The remaining technical details are explicitly carried forward to the passport sections where they belong: OS semantics/platform implementation, State Authority topology, API/contracts, Security/Egress Gateway, Hardware Abstraction and detailed cluster qualification.

### Open questions carried forward

1. Exact platform implementation and qualification model for MediaHub OS across Linux, macOS, iPadOS and Raspberry Pi.
2. Exact State Authority topology: replication, leader/authority semantics, conflict handling, quorum, split-brain prevention and failover.
3. Exact qualification rules for each distributed cluster subsystem and the conditions under which a subsystem may join or leave the cluster.
4. Exact API Gateway topology and trust model.
5. Exact Security/Egress Gateway implementation and separation from network gateway/firewall roles.
6. Exact Hardware Abstraction Layer boundaries and capability-schema format.


## Section 3 — STATE AUTHORITY

### Status
Functionally reconciled for the decisions currently required from the product owner. Implementation-level mechanisms remain deferred to the later architecture/qualification work.

### Confirmed requirements

1. State Authority covers the canonical state required for MediaHub behavior; specialized domain data may remain in domain-owned storage when its canonical identity/reference/versioning is integrated with State Authority.
2. The boundary is hybrid: State Authority owns canonical system state, identity/lifecycle/consistency and authoritative references; domains own specialized domain data within their contracts.
3. All State Authority mutations pass through an authorized State Authority operation path:
   request -> identity -> authorization -> policy -> contract validation -> state change -> version/audit.
4. AI does not have direct write authority over State Authority. AI-generated changes are treated as requests/proposals and must pass the same authorization, policy, contract and validation path as other actors.
5. Conflict handling uses a differentiated deterministic policy: critical state must not use unconditional last-write-wins; unresolved critical conflicts fail closed. Non-critical conflict resolution may use an architecture-defined deterministic strategy.
6. State Authority must retain mandatory change history sufficient for audit, diagnostics, rollback, recovery and provenance.
7. Rollback/recovery is state-aware: configuration and logical state may be restored, but physical actions after restoration must pass current safety, authorization and policy checks.
8. Recovery source of truth is verified durable State Authority state plus verified journal/provenance and validated domain state; AI, UI, cache or cloud copy alone cannot become authoritative.
9. During inter-node communication loss, qualified local operation continues where policy permits; globally coordinated operations may be restricted; reconciliation occurs after connectivity returns; unresolved critical conflicts are not silently auto-resolved.
10. If canonical State Authority service availability is lost, MediaHub enters a constrained local operating mode rather than a total shutdown, preserving qualified critical functions.

### Invariants

- One logical distributed State Authority.
- No competing independent State Authority.
- State Authority != Home Assistant Core: State Authority is canonical platform authority; Home Assistant Core remains Smart Home authority for its domain.
- AI != State Authority authority.
- Cloud != State Authority authority.
- Direct uncontrolled writes to canonical state are prohibited.
- Critical ambiguity/conflict => FAIL CLOSED.
- Recovery never bypasses current security/safety policy.
- Local First remains valid during cloud loss and qualified partial system failures.

### Open questions requiring product-owner decisions

The following are intentionally limited to architectural choices that cannot be safely inferred:

1. **Q3.11 — consistency classes:** Should MediaHub explicitly define multiple consistency classes, for example:
   - strong consistency for security/access-control/critical state;
   - transactional consistency for configuration;
   - eventual consistency for telemetry/derived state;
   - immutable append-only history for audit/provenance?
   Or should all canonical State Authority state use one consistency model?

2. **Q3.12 — offline writes:** During a network partition, may an isolated qualified node **commit changes to canonical state locally** and reconcile them later, or must isolated nodes restrict themselves to operations that do not create canonical state changes?

3. **Q3.13 — physical-state authority:** For equipment whose physical state can change independently of MediaHub (manual switch, vendor controller, sensor, external system), should the architecture treat the observed physical state as authoritative input to State Authority after validation, while distinguishing it from the desired/configured state?

4. **Q3.14 — irreversible operations:** Should safety/security-sensitive operations (door access, alarm/security actions, destructive equipment commands, etc.) require a fresh authorization/policy decision at execution time even when the command was previously scheduled or generated by an automation?

5. **Q3.15 — historical retention:** Should State Authority history be retained indefinitely as an immutable audit/provenance record, or should retention be policy-based by data class and legal/storage constraints?


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
- State Authority is one logical distributed authority across qualified MediaHub nodes.
- Cluster = one logical MediaHub cluster with qualified capability-specific distributed subsystems.
- Missing cluster capability != alternate architecture.

## Final Section 1 status

Section 1 product requirements are sufficiently reconciled to proceed to Section 2. Section 2 is closed. The confirmed model is one MediaHub architecture with heterogeneous qualified hardware profiles, a hybrid platform implementation model, one logical distributed State Authority, and one logical cluster with qualified distributed subsystems. Remaining implementation details are carried forward to their relevant passport sections.

## Deferred decisions

- exact HA topology and qualification;
- exact critical SLOs;
- exact hardware capability matrix;
- VPN protocol/provider and detailed routing policy;
- subscription enforcement mechanics;
- detailed capability matrix for Media/Entertainment/Documents on specialized profiles;
- exact platform implementation and qualification model for MediaHub OS across target platforms;
- State Authority multi-node topology and qualification;
- exact qualification rules for each cluster subsystem;
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
