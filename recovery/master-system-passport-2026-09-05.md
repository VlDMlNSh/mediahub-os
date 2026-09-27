# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS

# MASTER SYSTEM PASSPORT — FULL FUNCTIONAL / PRODUCT DESCRIPTION

**Status:** CONFIRMED_ACCEPTED — LONG-TERM BASELINE
**Date:** 2026-09-05
**Purpose:** canonical product and functional passport before final architecture reconstruction.

## 1. Product identity
MediaHub is a comprehensive engineering system and software/hardware product for design, equipment selection, supply, installation, integration, automation, commissioning, operation, diagnostics, modernization, and support of smart-home and building engineering systems.

MediaHub is not merely a media server, NAS, Smart Home Hub, or surveillance recorder. It unifies Smart Home, lighting, automation, climate, ventilation, heating, energy, security, video surveillance, networking, media, personal media, AI, distributed compute, engineering, lifecycle management, and external ecosystems behind one user-facing system model.

## 2. Core principle
The user works with devices, rooms, functions, scenes, automation, media, cameras, energy, network, projects, and results—not protocols, adapters, containers, internal services, or compute locations. Internal gateways, vendor adapters, Home Assistant, storage nodes, cluster nodes, transcoding, AI and cloud services are implementation layers hidden behind MediaHub.

## 3. Home Assistant
Home Assistant is the internal source of truth for Smart Home integration and automation. Its user interface is absent from the MediaHub user experience. MediaHub is the sole user-facing Smart Home model. Integration should be maximally automated: discovery → identification → integration selection → connection → configuration → entity creation → capability detection → room assignment → automation preparation.

## 4. Smart Home and equipment
Broad out-of-box support is required for common manufacturers, protocols and ecosystems. First-class directions include KINCONY, Dahua, Hikvision, Ajax, Ubiquiti, Keenetic, KNX, DALI, RS-485, Centrsvet, Arlight, Maytoni, Loxone, Apple HomeKit, Yandex Alice and other common systems. Coverage is extensible and tracked in a vendor/protocol registry.

Supported device classes include switches, relays, dimmers, outlets, lighting, LED controllers, sensors, thermostats, heating, HVAC, ventilation, blinds, shutters, curtains, gates, doors, locks, intercom/security, multimedia, energy equipment, controllers, DIY/IoT and other supported classes.

KINCONY USB onboarding is a preserved capability: detect board → install latest KCS firmware → network onboarding → expose supported KCS capabilities through MediaHub.

## 5. Automation, scenes and scheduling
Unified automation operates across devices, sensors, events, rooms, zones, groups, schedules, presence, energy, security, surveillance, multimedia, networking, MediaHub state and Local Assistant. It supports triggers, conditions, actions, scenes, one-time and recurring schedules, delays, retries/timeouts/cancellation semantics where supported, and execution history/explanation. Local critical automation should work without Internet where technically possible and cannot bypass security, authorization or safety.

## 6. Lighting, climate and engineering systems
MediaHub integrates lighting, KNX/DALI/RS-485 and wireless automation systems; heating, ventilation, HVAC, climate controls and related sensors; and associated engineering equipment.

## 7. Energy
Energy is one integrated system covering grid, UPS, solar, wind where supported, generators, inverters, batteries/storage and consumers. MediaHub observes availability, power, consumption, generation, charge/discharge, energy, states and alarms and incorporates energy into automation, scheduling, notification, diagnostics, Assistant and cluster workload decisions. Safe generator/source switching may be supported where technically and safely possible.

## 8. Video surveillance
MediaHub is a full surveillance node: discovery, identification, onboarding, live view, recording, archive, playback, search, events, notifications, diagnostics and authorized export. Dahua, Hikvision and Ajax are first-class requirements. MediaHub can record supported camera streams directly to its own storage; a separate NVR is not mandatory. Canonical flow: Camera → MediaHub → Surveillance Recording Storage.

Surveillance Recording Storage is a separate logical domain from Personal Media Library Storage.

## 9. Personal Media Library
One logical Personal Media Library spans authorized MediaHub nodes and clients. It supports photos, video, audio and other permitted media; ingestion from phones, external storage, LAN, other MediaHub and supported sources; metadata/provenance preservation where possible; organization, indexing, duplicate detection, search, processing, playback and bidirectional mobile synchronization subject to settings. It is offline-first where possible.

## 10. Playback, live media and streaming
Unified playback covers video, audio, photos, live media, streaming, personal media and permitted external content. Endpoints include MediaHub, HDMI displays, TVs, audio systems, phones, tablets, network devices and other supported endpoints. Live streams may originate from cameras, phones, other MediaHub and external sources. Transcoding/processing may be local or distributed; routing is hidden from the user. 4K is supported where source, network, decoder, GPU and display permit.

## 11. Audio
MediaHub provides a unified audio system spanning local/attached audio, HDMI, network audio, AV receivers, speakers, mobile devices, other MediaHub and supported endpoints. Multi-room audio is supported as a unified system. Phone can be an audio source or receiver.

Where hardware provides a physical 3.5 mm analog audio output, that output is a first-class preserved requirement. Mac mini uses its standard/original Apple audio capability as part of the MediaHub audio concept. Mac mini MediaHub supports MediaHub Hi-End Audio: minimum configuration includes a soundbar and can expand with two floor-standing speakers. Exact hardware/electrical implementation remains an implementation detail.

## 12. HDMI/display
HDMI is the primary local visual output. It supports MediaHub UI, media, photos, surveillance, live view, gaming, Smart Home, Assistant and permitted processing results. Displays are first-class endpoints. Multiple displays and distributed output are supported where hardware permits. Physical connection does not grant authorization.

## 13. Phone as Media/IO endpoint
iPhone, iPad and Android can be UI, media source/receiver, audio/video endpoint, camera, microphone, Personal Media Library client, surveillance client and remote MediaHub endpoint. Phone ↔ MediaHub media transfer and synchronization are supported subject to authorization and platform constraints. Phone microphone/camera can be used as MediaHub IO where supported.

## 14. Gaming
MediaHub integrates Xbox, PlayStation, gaming PCs, MediaHub Gaming and other supported gaming endpoints, including HDMI output and common media routing.

## 15. External ecosystem export/projection
Integrated and configured Smart Home equipment can be projected/exposed into supported external ecosystems such as Apple HomeKit, Yandex Alice and Loxone where applicable. MediaHub remains the primary system model. An internal Loxone mini-server capability is planned so a separate physical server is not inherently required when MediaHub can provide the function.

## 16. Export system
Export is a distinct MediaHub capability covering permitted device/entity representations, automation/scenes, events, media, surveillance archives, engineering project data, schemes, cable schedules, as-built documentation and external ecosystem representations, subject to permissions, privacy, security and destination compatibility. Exact formats remain implementation-defined.

## 17. Local Assistant and AI
Local Assistant runs locally inside MediaHub and assists with equipment integration/configuration, automation creation/modification/explanation, media/audio control, Smart Home control, diagnostics and contextual understanding. Local execution is preferred. If a task cannot be solved locally or local generation is too slow, MediaHub may invoke an internal cloud compute/assistant path. The user never receives direct Cloud Development access.

## 18. Cloud Development
Cloud Development is a separate internal company/development contour for MediaHub operational and engineering needs, website generation, internal development services, distributed compute and AI/content generation. It may include engines that study trusted sources and generate media/content and engineering-support services. It is not a user-facing workspace.

## 19. Local MediaHub Cluster and distributed compute
Multiple MediaHub nodes can form a Local MediaHub Cluster. Nodes can redistribute compute, AI, media processing, transcoding, storage, streaming, automation and redundancy/failover where technically possible. The user sees one MediaHub system and does not select individual compute nodes.

MediaHub can also participate in building/extending seamless wireless home networks alongside Keenetic/Ubiquiti, including supported router/access-point/network-extension roles. User-facing actions include simple network extension and cluster join/create operations; internal topology is hidden.

## 20. Professional/commercial engineering edition
A separate professional/commercial MediaHub edition serves designers, engineers, integrators, installers, commissioning and operating organizations. Every project begins as a Designer Project. MediaHub accepts PDF, images and drawings, analyzes source materials and creates a virtual twin/digital representation of the object.

The engineering contour supports equipment selection, topology, engineering-system schemes, wiring, cable schedules, installation guidance, configuration, automation, commissioning, diagnostics, modernization and as-built/executive documentation. Lifecycle: design → selection → topology → installation → connection → configuration → automation → commissioning → operation → diagnostics → modernization.

## 21. Contextual guidance
Across installation, integration, configuration, automation, commissioning and external ecosystem export, MediaHub provides small contextual hints. Activating a hint opens complete actionable step-by-step instructions. This is a cross-cutting capability, not installer-only behavior.

## 22. UI/UX
MediaHub uses a minimalist, intuitive visual language broadly inspired by the clarity and navigation principles of iOS/macOS without implying reuse of proprietary Apple assets. Home/standby provides shortcuts for Games, Media, Smart Home, surveillance/live/archive and other frequent functions. Settings exposes Smart Home, automation, network, required settings, Engineering Mode and expanded Installer Mode. Technical complexity is hidden unless needed.

## 23. Users, identity and access
MediaHub supports multiple users with profiles, devices, preferences, presence, permissions, notifications and scoped access. Conceptual roles include ordinary user, owner/admin, engineer/integrator and system/operator. Authorization applies to devices, automation, scenes, schedules, network, integrations, cluster, storage, surveillance, updates, diagnostics and engineering functions. Presence is not authentication; authentication is not authorization.

## 24. Cybersecurity, protection and safety — ACCEPTED SYSTEM REQUIREMENT
MediaHub itself is a maximally protected system. Cybersecurity is a built-in, cross-cutting property of the product, not an optional add-on. MediaHub shall include the security mechanisms and protected communication protocols necessary to defend the system, users, devices, network, remote access, data, automations, clusters, integrations and privileged development infrastructure against the broad range of relevant cyberattacks and unauthorized access.

Security architecture must preserve defense-in-depth, authenticated and authorized operations, protected communications, trusted-device/node handling, isolation of unknown/untrusted equipment, secure remote access, auditability, safe update/recovery paths and protection of sensitive data. Discovery does not equal trust; physical connection does not grant authorization; remote access does not increase rights; Developer access remains separately privileged.

The exact cryptographic algorithms, protocols, key/certificate lifecycle, MFA/passkeys, VPN/remote transport, trust enrollment, threat model, security levels and recovery mechanisms remain implementation/contract details to be formally defined later. The high-level security requirement itself is accepted and must not be lost.

## 25. Events, notifications and history
Unified events originate from devices, sensors, automation, surveillance, energy, network, cluster, MediaHub, Local Assistant and external integrations. Notifications are contextual/actionable and have informational, warning, important and critical priorities. Significant event history preserves causal explanation: Event → Trigger → Automation → Action → Result.

## 26. Presence and context
Presence may represent at-home, absent, returning, departing, room and zone context based on supported sources including phones, network, Smart Home and motion. It feeds automation, notifications, energy, security, media and Assistant while remaining governed by privacy/security.

## 27. Diagnostics, health and readiness
MediaHub provides diagnostics across devices, network, automation, energy, surveillance, storage, cluster, media and integrations. Health is observation-only; Readiness is operation-scoped. Health, Readiness, Liveness, Trust and Authorization are distinct semantics.

## 28. Offline-first
Local functions should remain operational without Internet whenever technically possible, including local Smart Home, critical automation, surveillance, local media, HDMI, audio, Local Assistant and local cluster functions. Cloud is an additional resource, not the foundation of local operation.

## 29. Updates, recovery, backup and migration
Updates should provide an experience maximally close to iOS/macOS: a visible Updates section, version description and user-initiated update. MediaHub is resilient/self-recovering, creates recovery checkpoints and can directly manage filesystem state as needed for integrity/recovery. Backup, restore and migration cover system configuration, Smart Home, automation, users, media, surveillance and projects as applicable.

## 30. Installer
Multiboot USB installer supports target hardware testing/detection, driver/component selection, required Linux image download, Linux installation and MediaHub component installation for compatible Mac mini, mini PC and Raspberry Pi targets. Installation allocates separate logical domains for surveillance recording, Personal Media Library and system/recovery/backup. Installer UI is minimalist and macOS-like in general interaction language without proprietary Apple asset reuse.

## 31. Product variants
### Full Mac mini
Full-featured MediaHub. Uses Mac mini standard/original Apple audio capability. Supports Hi-End Audio.

### Full mini PC
Full-featured MediaHub on compatible mini PC hardware.

### Simplified Raspberry Pi
Reduced MediaHub variant for supported lightweight roles. It does not provide local hard-disk surveillance-stream recording and does not provide local Personal Media Library storage.

### iOS/iPadOS MediaHub
A distinct product variant for iPhone/iPad located on the object. It enables minimal MediaHub deployment and specialized wall/home control panels. It provides Smart Home, automation, surveillance, media control, notifications, diagnostics and other platform-supported MediaHub functions. It does not provide local hard-disk surveillance recording or local Personal Media Library storage.

The iOS/iPadOS object-installed variant can also act as a local MediaHub node/server within the capabilities and restrictions of the platform and can provide the intended local infrastructure for a remote HomeKit-control scenario. Exact Apple/HomeKit APIs, background execution, network and remote-access mechanisms remain subject to technical validation.

### Commercial/Engineering
Separate professional product direction for engineering design, Digital Twin, installation, commissioning, diagnostics, modernization and as-built documentation.

## 32. Data, Search and Knowledge Graph
MediaHub unifies device, user, room, event, automation, media, surveillance, energy, network, engineering and project relationships. Unified Search and Knowledge Graph provide contextual retrieval and support Local Assistant reasoning. Privacy and access controls govern data visibility and processing.

## 33. Product-level invariants
- MediaHub is one unified user-facing system.
- Home Assistant is internal; its UI is not user-facing.
- User works with device/function, not protocol/integration.
- Surveillance Recording Storage and Personal Media Library Storage are separate logical domains.
- MediaHub can directly record supported cameras; separate NVR is not mandatory.
- Local-first operation is preferred.
- Cloud Development is never directly exposed to ordinary users.
- Remote access never increases authorization.
- Discovery is not trust; presence is not authentication; authentication is not authorization.
- Physical connection does not grant rights.
- Security is a built-in product property.
- 3.5 mm analog audio remains a first-class requirement where the hardware connector exists.
- Functional differences between product variants must be preserved.
- Internal distribution of storage, processing and networking is hidden behind the unified MediaHub model.

## 34. Long-term governance
This passport is the accepted master functional/product description. It is the authoritative high-level source for subsequent Function Master Inventory, loss audit, duplicate audit, conflict reconciliation, capability registry, contract registry, architecture reconstruction and development baseline. Deferred technical details must remain visible as open items and may not be silently removed or weakened during later decomposition.
