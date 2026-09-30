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
Verification status: GitHub API did not resolve the declared SHA at this checkpoint; it is retained as declared historical provenance and must not be rewritten.

## Passport progress

- Section 1 — НАЗНАЧЕНИЕ: substantially reconciled from user answers; one product-boundary item remains for explicit resolution below.
- Sections 2–68: unresolved / not started.

## Section 1 — confirmed requirements

1. MediaHub is one product: a local operating system/platform for buildings.
2. Target scope is not restricted to a single building type; deployment profiles may vary while remaining one product.
3. MediaHub unifies Smart Home, Media, AI, Documents, energy, video surveillance, security, climate, networking, integrations and entertainment.
4. Entertainment includes games launched from gaming PCs and supported mainstream consoles.
5. Digital Twin and advanced Engineering are paid functional extensions.
6. Smart Home is core/mandatory.
7. Media is core on Mac mini/mini-PC deployments; it is not mandatory on iPad-specialized deployments.
8. Documents is core on Mac mini/mini-PC deployments; it is not mandatory on iPad-specialized deployments.
9. Local AI is mandatory, including on iPad/iOS where a qualified small-memory local assistant is available.
10. Engineering as equipment/system integration, equipment configuration and integration is mandatory; advanced Digital Twin/Engineering functionality is a paid extension.
11. Network is core on Mac mini/mini-PC deployments; it is not mandatory on iPad-specialized deployments.
12. A user-facing remote-access mobile application is mandatory.
13. Security is a key core subsystem covering system security, cybersecurity and resistance to attacks and vulnerabilities.
14. Observability, Backup/Recovery and Update/Migration are core.
15. Camera surveillance recording to local storage is a MediaHub capability, subject to node hardware qualification.
16. Media is one peer domain system, not the sole center of the product.
17. AI is intended to provide optional-assistant, core-subsystem, automation-engine, knowledge-interface, engineering-assistant and multimodal capabilities while remaining non-authoritative.
18. Engineering spans developer environment, user/object management, CAD/BIM/Digital Twin, infrastructure diagnostics, AI development workflows, distributed compute, equipment integration and equipment configuration.
19. The Cloud Development Environment is part of the broader MediaHub ecosystem but remains a separate security/control domain from MediaHub OS and its State Authority.
20. Compute Contribution is intended for every MediaHub deployment, subject to capability, opt-in, admission, lease, isolation, revocation, audit and network restrictions already defined by the compute contract.
21. Compute Contribution supports development acceleration, distributed AI, CI/build, inference, training, rendering, simulation, data processing and storage processing, plus approved company development workloads.
22. Cloud capabilities include development, backup, remote access, notifications, optional AI, model registry, software distribution, telemetry, disaster recovery, cloud storage and compute.
23. MediaHub may act as Gateway, Router, Firewall, DHCP, DNS, AP, Controller, Media Server and Smart Home Node, with role separation and deployment qualification still required.
24. Hardware independence is a design objective. Target classes include Mac mini, mini-PC, Raspberry Pi specialized editions and iPad specialized editions. Hardware capability determines feature set.
25. A single-node MediaHub deployment is valid.
26. A multi-node deployment is intended to form a cluster automatically and may provide HA, distributed storage, compute clustering, network mesh and Wi-Fi mesh.
27. If one MediaHub node fails, another qualified node must automatically continue critical functions without manual intervention.
28. Critical functions include security, access control, surveillance, climate and energy.
29. Critical functions must remain operational, to the qualified extent of the deployment, through Internet failure, Cloud failure, failure of one MediaHub node, partial local-network failure, failure of the primary AI subsystem and failure of one storage component.
30. External integrations and OSS components must be provenance-checked and must not use unknown/untrusted software components.
31. MediaHub State Authority is mandatory/core. The term does not mean governmental authority.
32. Mobile remote access and a specialized iPad MediaHub installation are distinct concepts.
33. iPad is not merely a remote client in the specialized deployment model. An iPad may run a hardware-adapted, reduced-capability MediaHub OS/node, analogous to a specialized Raspberry Pi edition.
34. A specialized iPad MediaHub installation provides local MediaHub functionality subject to iPad hardware and OS constraints and may also expose the ordinary remote-access application experience where applicable.
35. iPad may contain local AI and may participate in qualified Compute Contribution; actual capabilities are determined by its hardware/software capability profile.
36. Camera recording on iPad is not mandatory. Recording is available only when the node's hardware, storage and OS profile passes qualification. Raspberry Pi specialized deployments likewise do not provide surveillance recording in the baseline profile.
37. Personal VPN is not yet product-defined; its placement remains open between optional user capability, network profile and gateway function.
38. MediaHub may perform per-client/per-network routing policy, including VPN versus direct paths, subject to later security and network qualification.
39. Cloud Development is explicitly separated from MediaHub State Authority: controlled contracts connect the user/local domain and developer domain; the developer domain does not become canonical user-state authority.
40. Local operation and confidentiality have highest product-level priority.

## Architecture invariants confirmed

- MediaHub State Authority = canonical platform authority.
- Home Assistant Core = Smart Home authority.
- AI != authority.
- Mobile remote-access application != authority.
- Specialized iPad MediaHub node != authority; it is a node implementation of MediaHub OS.
- Cloud != authority over canonical MediaHub state.
- Scheduler != authority.
- OSS component != authority.
- Developer Cluster != authority.
- Local First.
- Unknown device => DENY/QUARANTINE.
- Ambiguous state => FAIL CLOSED.
- Compute Contribution != User Data Access != Developer Personnel Access.
- CPRG remains registration-only.
- Integration follows Contract -> Adapter -> Validation -> Integration -> Qualification.
- Security boundaries must not depend only on physical connectivity.
- User confidentiality takes precedence over convenience.
- HA is a product requirement for qualified multi-node deployments, not yet a specific implementation topology.
- Hardware profile determines capabilities; capability absence on a specialized node does not invalidate the single-product identity.

## Section 1 architecture interpretation

### Product boundary

MediaHub OS is the local building operating system and its node implementations.

The Cloud Development Environment is a separate development domain in the broader MediaHub ecosystem. It may provide compute, storage, development, AI, backup, distribution and other approved services, but it is not part of the canonical local State Authority and cannot override canonical local state.

### Node taxonomy

The current model distinguishes:

- Full MediaHub node: Mac mini / mini-PC class with the full local feature profile.
- Specialized MediaHub node: Raspberry Pi or iPad profile with a reduced hardware-qualified capability set.
- Remote-access application: user-facing mobile application for remote access; this is distinct from the specialized iPad MediaHub OS deployment.

A single physical iPad installation can therefore be a specialized MediaHub node while also exposing user-facing UI capabilities. This does not make it the canonical State Authority.

### HA requirement

The product requirement is automatic continuation of critical functions after failure of one qualified MediaHub node, without manual intervention. The implementation topology (active/passive, active/active, quorum, replicated state, storage strategy and failure-domain design) remains an architecture decision for later reconciliation.

### Surveillance recording

Surveillance recording is a MediaHub capability, not a universal node invariant. The capability matrix will determine whether a given Mac mini, mini-PC, Raspberry Pi or iPad deployment can record locally.

## Open decisions remaining inside Section 1

- exact role and product semantics of personal VPN;
- exact hardware capability matrix;
- exact implementation and qualification model for HA;
- exact criticality/availability targets per subsystem;
- precise boundary of paid Digital Twin/Engineering features;
- final classification of Media/Entertainment capabilities on specialized deployments.

## Rejected / corrected interpretations

- “State Authority” is not governmental authority.
- A specialized iPad installation is not merely the remote-access client; it can be a reduced-capability MediaHub OS/node.
- The remote-access application remains a distinct product surface.
- Media is not the sole product center.
- iOS/iPad is not automatically the canonical state owner.
- Compute Contribution does not grant access to user data or developer personnel privileges.
- Cloud Development is not the canonical local authority.
