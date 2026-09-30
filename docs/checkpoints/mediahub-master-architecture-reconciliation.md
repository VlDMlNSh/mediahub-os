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

- Section 1 — НАЗНАЧЕНИЕ: reconciled from user answers; final product-boundary clarifications remain below.
- Sections 2–68: unresolved / not started.

## Section 1 — confirmed requirements

1. MediaHub is one product: a local operating system/platform for buildings.
2. Target scope is not restricted to a single building type; deployment profiles may vary while remaining one product.
3. MediaHub unifies Smart Home, Media, AI, Documents, energy, video surveillance, security, climate, networking, integrations and entertainment.
4. Entertainment includes games launched from gaming PCs and supported mainstream consoles.
5. Digital Twin and Engineering are paid functional extensions.
6. Smart Home is core/mandatory.
7. Media is core on Mac mini/mini-PC deployments; it is not mandatory on iPad-specialized deployments.
8. Documents is core on Mac mini/mini-PC deployments; it is not mandatory on iPad-specialized deployments.
9. Local AI is mandatory, including on iPad/iOS where a qualified small-memory local assistant is available.
10. Engineering as equipment/system integration is mandatory; advanced Digital Twin/Engineering functionality is a paid extension.
11. Network is core on Mac mini/mini-PC deployments; it is not mandatory on iPad-specialized deployments.
12. User mobile remote-access application is mandatory.
13. Security is a key core subsystem covering system security, cybersecurity and attack/vulnerability resistance.
14. Observability, Backup/Recovery and Update/Migration are core.
15. Camera surveillance recording to local disk is part of the intended system capability, subject to hardware qualification.
16. Media is one peer domain system, not the sole center of the product.
17. AI is intended to provide assistant, automation, knowledge, engineering-assistant and multimodal capabilities while remaining non-authoritative.
18. Engineering spans developer environment, user/object management, CAD/BIM/Digital Twin, infrastructure diagnostics, AI development workflows, distributed compute, equipment integration and equipment configuration.
19. Developer/Cloud Development Environment is conceptually part of the broader MediaHub ecosystem, while remaining a separate security/control domain.
20. Compute Contribution is intended for every MediaHub deployment, subject to capability, opt-in and qualification constraints already defined by the compute contract.
21. Compute Contribution supports development acceleration, distributed AI, CI/build, inference, training, rendering, simulation, data processing and storage processing, plus approved company development workloads.
22. Cloud capabilities include development, backup, remote access, notifications, optional AI, model registry, software distribution, telemetry, disaster recovery, cloud storage and compute.
23. MediaHub may act as Gateway, Router, Firewall, DHCP, DNS, AP, Controller, Media Server and Smart Home Node, with role separation and deployment qualification still required.
24. Hardware independence is a design objective. Target classes include Mac mini, mini-PC, Raspberry Pi specialized editions and iPad specialized editions. Hardware capability determines available feature set.
25. A single-node MediaHub deployment is valid.
26. A multi-node deployment is intended to form a cluster automatically and may provide HA, distributed storage, compute clustering, network mesh and Wi-Fi mesh; exact HA semantics remain an architecture decision.
27. Critical functions include security, access control, surveillance, climate and energy.
28. Local operation and confidentiality have highest product-level priority.
29. External integrations and OSS components must be provenance-checked and must not use unknown/untrusted software components.
30. Mobile is a client authority boundary, not the State Authority.
31. Cloud, scheduler, OSS components and developer infrastructure are not authoritative over canonical MediaHub state.

## Terminology correction

“MediaHub State Authority” does NOT mean governmental authority.

It means the canonical software authority that owns the authoritative MediaHub system state and its valid state transitions.

Therefore:
MediaHub State Authority = canonical platform authority.

It remains mandatory/core even though the term was initially misunderstood in the questionnaire.

## Architecture invariants confirmed

- MediaHub State Authority = canonical platform authority.
- Home Assistant Core = Smart Home authority.
- AI != authority.
- Mobile != authority.
- Cloud != authority.
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

## Open decisions remaining inside Section 1

These must be resolved before Section 2:
- exact definition of the product boundary between MediaHub OS and the separate Cloud Development Environment;
- exact iPad role: client, specialized MediaHub node, or both under distinct operating modes;
- exact semantics and qualification threshold for automatic HA;
- whether surveillance recording on iPad is a product capability or merely a hardware-dependent optional deployment capability;
- exact role of personal VPN;
- exact hardware capability matrix;
- exact criticality/availability class for each critical subsystem;
- precise boundary of paid Digital Twin/Engineering features;
- final classification of Media/Entertainment capabilities on specialized deployments.

## Rejected / corrected interpretation

- “State Authority” is not governmental authority.
- Media is not the sole product center.
- iOS is not automatically the canonical state owner.
- Compute Contribution does not grant access to user data or developer personnel privileges.
- Cloud is not the canonical authority.
