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
- Sections 2–68: unresolved / not started.

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

Section 1 product requirements are sufficiently reconciled to proceed to Section 2. Implementation and qualification questions deliberately deferred to later passport sections must not be silently assumed here.

## Deferred decisions

- exact HA topology and qualification;
- exact critical SLOs;
- exact hardware capability matrix;
- VPN protocol/provider and detailed routing policy;
- subscription enforcement mechanics;
- detailed capability matrix for Media/Entertainment/Documents on specialized profiles.

## Rejected / corrected interpretations

- State Authority does not mean governmental authority.
- iPad MediaHub OS is not the remote-access application.
- MediaHub iOS OS and MediaHub Remote Access are separate applications.
- Surveillance capability and local recording are separate requirements.
- Media is not the sole product center.
- Cloud Development is not canonical local authority.
