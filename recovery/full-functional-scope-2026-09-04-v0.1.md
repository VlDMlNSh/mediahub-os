# MediaHub — Full Functional Scope / User Baseline

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED BASELINE

## Governing principle

This document captures the product-owner-defined functional scope before clean implementation. It is authoritative as a functional input, but does not silently override already accepted architectural invariants. Any conflict with MH-01…MH-23 must be explicitly reconciled and recorded.

The functional baseline is reconstructed first; implementation must not begin until the complete capability inventory, reconciliation and master baseline are accepted.

## Smart Home Hub

- MediaHub is primarily a smart-home hub.
- Home Assistant is an internal underlying smart-home integration/automation technology inside MediaHub Core.
- Home Assistant has no external user-facing interface in the product.
- The user must not need to know that Home Assistant exists or that it is used internally.
- The user manages the smart home entirely through the native MediaHub UI and product model.
- MediaHub must support out-of-box integration with the most widespread/common smart-home manufacturers, brands, protocols and ecosystems rather than being limited to a small fixed vendor list.
- When a new device appears on the network or through an available discovery channel, MediaHub automatically detects it, identifies the manufacturer/device type/capabilities where possible, and offers the user integration.
- The onboarding flow offers room assignment, device-type classification and configuration.
- Throughout discovery, installation and configuration, MediaHub provides contextual pop-up hints, installation instructions and actionable configuration guidance.
- Guidance may include concrete network/configuration actions, including which IP address/page to open and what settings to change when required.

### Smart Home Device Discovery & Onboarding — CONFIRMED_ACCEPTED

- MediaHub continuously monitors available device-discovery channels.
- When new equipment appears, MediaHub detects it, identifies manufacturer/model/device class/capabilities where possible, determines available integration methods, and offers integration.
- The user interacts with the device through the MediaHub product model rather than through an underlying integration technology.
- Onboarding provides room assignment, classification, naming/grouping and configuration.
- If manual configuration is required, MediaHub provides actionable step-by-step guidance, potentially including an IP address, page to open, setting to change and verification action.
- After integration, MediaHub should handle ordinary device operation without exposing integration internals.
- If a device disappears, changes network identity, restarts, is replaced or changes capabilities, MediaHub should attempt rediscovery and recovery without requiring a full re-onboarding where technically possible.
- Unknown devices are surfaced safely with options to identify, investigate, integrate if possible, or keep isolated until understood.
- Core UX invariant: the user works with a device through MediaHub; the underlying integration mechanism is hidden.

### Vendor & Protocol Coverage — CONFIRMED_ACCEPTED

- MediaHub is not limited to a small fixed vendor list.
- The out-of-box requirement applies to the most widespread/common smart-home manufacturers, brands, protocols and ecosystems.
- Coverage is considered across manufacturer, protocol and ecosystem levels.
- Target device classes include switches, relays, dimmers, outlets, lighting, LED controllers, sensors, thermostats, heating, HVAC, ventilation, blinds/shutters/curtains, gates/doors/locks, intercom/security equipment, multimedia equipment, energy equipment, controllers and DIY/IoT devices, as applicable.
- MediaHub should automatically determine the appropriate integration mechanism where possible rather than requiring the user to choose protocols or integrations.
- Vendor-specific adapters may exist internally, but the user-facing model remains MediaHub.
- A dedicated Vendor / Protocol Coverage Registry will track vendor/model/family, device class, protocol, discovery, pairing, configuration, control, telemetry, events, firmware, local/cloud behavior and MediaHub status.
- Coverage status values may include CONFIRMED_SUPPORTED, REQUIRED, PLANNED, CANDIDATE, UNRESOLVED, NOT_SUPPORTED and DEPRECATED.

### Smart Home Device Model & Capabilities — CONFIRMED_ACCEPTED

- MediaHub uses a unified device model regardless of vendor, manufacturer, protocol or underlying integration mechanism.
- A device entity includes, as applicable: Identity, Manufacturer, Model, Device Type, Room/Area, Groups, Capabilities, State, Controls, Sensors, Events, Configuration, Connectivity and Lifecycle.
- The abstraction is capability-first: a device may expose multiple capabilities such as on/off, dimming, color, temperature, power measurement, motion detection and events.
- Target device types include lights, switches, relays, outlets, sensors, climate devices, heating, ventilation, blinds/shutters/curtains, doors, locks, cameras, energy devices, multimedia devices, controllers and other supported equipment.
- One physical device may expose multiple functional entities/capabilities within the MediaHub model.
- MediaHub assigns devices to rooms/areas, suggesting assignment automatically where possible while allowing user correction.
- Users can create/use groups by room, type, function, scene, zone or custom criteria.
- Device state includes availability, operational state, sensor values, connectivity state, command execution state and relevant functional state.
- Controls are presented through the unified MediaHub UI according to available capabilities.
- Device events are available to automation, notifications, the Local Assistant, history and diagnostics as appropriate.
- Connectivity is presented simply to ordinary users; detailed protocol/network information is reserved for advanced/engineer settings.
- Device lifecycle is represented conceptually as: Discovered → Identified → Proposed → Integrated → Configured → Operational → Unavailable/Recovering → Replaced/Retired, with transitions determined by actual system state.
- Manufacturer and protocol are properties of the integration layer; capability and device semantics belong to the MediaHub product model.
- Core UX invariant: the user works with the device, not with the integration technology.

### Automation / Scenes / Rules / Scheduling — CONFIRMED_ACCEPTED

- MediaHub provides a unified Smart Home automation engine over the unified device model.
- Automation may connect devices, device states, sensors, events, rooms/zones, groups, schedules, presence, energy, security, video surveillance, multimedia, networking and MediaHub state.
- Triggers may include device state changes, sensor values, events, time/schedules, presence, room state, security events, surveillance events, network state, MediaHub state, energy conditions, multimedia events, user commands and Local Assistant commands.
- Conditions may inspect device state, sensor values, time/date, presence, room/zone, energy state, network state, other automations and device availability.
- Actions may control supported devices and subsystems, including lighting, climate, heating/HVAC, blinds, doors/locks, energy systems, multimedia, surveillance, networking, notifications and permitted external integrations.
- Scenes provide a user-facing way to combine multiple actions into one MediaHub function.
- Scheduling supports one-time, daily, weekly, recurring, time-based, event-relative and delayed actions.
- Automation execution accounts for device unavailability, retry, timeout, cancellation, prevention of unwanted duplicate execution and recovery from transient failure; exact retry/idempotency semantics remain a later technical decision.
- Critical local automations should be able to execute without Internet access when required local components are available.
- Automation must not bypass system security, authorization or safety constraints; exact safety classes and confirmation rules remain subject to later contracts.
- Local Assistant may create, explain, modify, diagnose and improve automations, scenes and schedules in natural language. Created automations become ordinary MediaHub automations and do not require the Assistant to remain available for execution.
- Execution history and user-visible explanation of automation behavior are required, with exact data model defined later.

### Notifications / Events / History — CONFIRMED_ACCEPTED

- MediaHub provides a unified event model for events originating from devices, sensors, automations, surveillance, energy systems, networking, MediaHub Cluster, external integrations, Local Assistant and MediaHub itself.
- Events may feed Automation, Notifications, History, Diagnostics and Local Assistant.
- MediaHub notifies users about significant events including new-device discovery, integration/onboarding status, device failures or loss of connectivity, recovery, automation results, security/surveillance events, power/energy issues, network issues, MediaHub issues, cluster events and situations requiring user action.
- Notifications should be contextual and actionable where possible rather than merely descriptive.
- Notification priority includes informational, warning, important and critical levels; exact semantics remain to be defined.
- MediaHub retains significant event history for user review, automation analysis, diagnostics, Local Assistant, energy analysis, security investigation and state recovery as appropriate.
- Event history should support a causal chain such as Event → Trigger → Automation → Action → Result so users and engineers can understand why an action occurred.
- Users should be able to ask why an action occurred and receive a comprehensible explanation based on the relevant event/automation chain.
- Ordinary UI presents human-oriented information; Advanced/Engineer Settings may expose technical events, sources, integration details, network parameters, errors, correlation/request identifiers and extended execution history.
- Local events and critical local notifications should not depend on Internet access when required local components are available.
- Exact event schema, retention, aggregation, deduplication, privacy, cluster synchronization, cloud history, export and notification delivery channels remain later technical decisions.

### KINCONY

- KINCONY is a first-class supported vendor/integration.
- KINCONY boards are added to MediaHub via MQTT and use KCS vendor firmware.
- The KCS primary web interface is proxied/embedded into the MediaHub UI and exposed in settings for detailed board configuration.
- When a blank/unflashed KINCONY board is connected to MediaHub by USB, MediaHub detects it.
- MediaHub locates the latest firmware for the detected board on the KINCONY forum/source and flashes the board.
- The KINCONY onboarding flow then continues into normal MediaHub integration.

### Smart-home external ecosystem export

- The integrated smart-home system is exportable/bridgeable to external user applications/ecosystems including Loxone, Yandex Alice and Apple HomeKit.
- Apple HomeKit integration may require an additional server in the local network.
- Yandex Alice integration is intended through Yandex Cloud.
- MediaHub Local Assistant is a general MediaHub assistant that can be used for Loxone onboarding and automation construction; it is not a Loxone-specific assistant.

## Video surveillance

- Out-of-box vendor support is required for Dahua, Hikvision and Ajax.
- Devices from these vendors are automatically detected when they appear on the network.
- MediaHub provides complete integration instructions and distribution/assignment guidance during onboarding.
- Product principle: eliminate unnecessary physical intermediary equipment where possible, such as a separate NVR.
- Recording, archival storage and surveillance playback are performed directly by MediaHub.
- During MediaHub installation, the installer offers disk-space allocation into at least two logical areas: surveillance recording storage and media library storage.

## Networking, seamless coverage and MediaHub scaling modes

- Out-of-box support is required for Ubiquiti and Keenetic networking equipment.
- Product principle: eliminate unnecessary physical intermediary infrastructure where possible.
- MediaHub is intended to replace a Ubiquiti server/controller layer where applicable.
- MediaHub can participate directly in building/extending a seamless wireless home network alongside Keenetic and Ubiquiti equipment.
- Example target deployment: one Ubiquiti access point plus one MediaHub can provide/extend home wireless coverage.
- Multiple MediaHub units in one local network can form a local MediaHub cluster.
- The local cluster redistributes computing tasks/workloads among MediaHub nodes and supports additional coordinated functions.
- The local cluster can also participate in seamless wireless networking.
- MediaHub settings must expose these capabilities through simple user-facing actions rather than requiring users to manage complex network or cluster infrastructure.
- A user should be able to select a simple action such as extending the seamless home network or joining/creating a local MediaHub cluster, after which MediaHub handles the underlying configuration as far as technically possible.
- When another MediaHub is discovered on the local network, the system should identify its capabilities and offer the user a simple option to join or coordinate the nodes.
- MediaHub settings allow selection of the relevant Internet uplink/path for the wireless network, including ordinary Internet or Internet routed through VPN, subject to the available network topology.

### Local MediaHub Cluster

- Several MediaHub nodes in the local network operate as a coordinated local cluster.
- The cluster may distribute compute, AI, media processing, transcoding, automation and other authorized workloads.
- The system should support degraded operation and failover where technically possible.
- Exact topology, coordination, scheduling, failover and security semantics require later technical acceptance.

### Cloud Cluster

- MediaHub can participate in a distributed cloud compute/development cluster in addition to a local cluster.
- The cloud cluster aggregates participating MediaHub compute capacity for authorized workloads.
- MediaHub can use the cloud cluster when local capabilities are insufficient.
- The user-facing configuration must remain simple; underlying distributed-compute mechanics are hidden from ordinary users.
- Resource contribution, consent, metering, limits, data boundaries and security require later technical acceptance.

## Distributed cloud development / compute environment

- MediaHub nodes may contribute otherwise-unused compute capacity to a shared cloud development/supercomputing environment.
- The shared environment hosts a cloud assistant.
- MediaHub consults the cloud assistant when local tools/capabilities are insufficient.
- The more Internet-connected MediaHub nodes participate, the more aggregate compute capacity is available to this environment.
- Core development tools/environment controls are restricted to the developer/operator, not ordinary end users.
- A content-generation engine in this environment can study designated sources and generate daily video content.
- Target generated content includes short stories, educational videos, equipment reviews, setup/integration/mounting lectures, electrical lectures and similar technical educational material.
- The environment also supports automatic generation of the MediaHub company website from specified parameters; this will be expanded in a later scope pass.

## Visual/user interface

- Default visual interface is a light-gray waiting/loading screen inspired by the visual simplicity and centered composition of Apple installation/loading screens.
- A centered MediaHub logo is displayed at the corresponding central position.
- This is an intentional product visual direction; implementation must not assume copying proprietary Apple assets.
- MediaHub exposes normal settings and a separate advanced settings area intended for engineers.
- Navigation should be highly intuitive and visually coherent across the product.
- Ordinary users must not be exposed to internal infrastructure complexity such as Home Assistant administration, cluster orchestration or distributed-compute mechanics.

## Phone as media/IO endpoint

- When an iPhone is detected within the relevant connectivity range, MediaHub can connect it.
- MediaHub can route audio/video from the phone to its HDMI output and audio system.
- Target video quality includes 4K where source/network/hardware support permits.
- Because mini PCs/Mac mini-class devices may lack a built-in microphone, a connected iPhone or Android device can serve as an audio input/output endpoint; the exact audio routing semantics require clarification.
- Android is also a supported phone endpoint.

## Game controllers and gaming

- MediaHub supports common console controllers, including Xbox and PlayStation controllers.
- Controllers can be used for MediaHub navigation and gaming.
- Games can be played from consoles and from a gaming PC.
- Video from a console or phone can be routed directly to MediaHub HDMI output.
- Exact console/PC transport protocol and capture/input topology remain to be specified.

## Personal media library

- MediaHub contains a media library for users.
- Users can synchronize the media library with iPhone and Android devices.
- Goal: create a shared/common media library across MediaHub and user mobile devices.

## Cross-cutting product principles recovered from this scope

- Hidden implementation layers should be replaced by a unified MediaHub experience where technically feasible.
- Home Assistant is an internal implementation component, not a user-facing product or user-facing mental model.
- Automatic discovery and guided onboarding are first-class product behavior.
- Contextual instructions should be actionable, not merely descriptive.
- Local-first operation is strongly implied for core smart-home, surveillance, networking and assistant functions; exact cloud fallback rules require formalization.
- Engineer/advanced configuration exists separately from ordinary user settings.
- Network extension, local clustering and cloud clustering should be exposed as simple MediaHub configuration choices while implementation complexity remains internal.
- MediaHub is intended to unify smart home, surveillance, networking, media, mobile-device integration and distributed compute under one product surface.

## Items explicitly requiring clarification / acceptance

1. Exact initial vendor/protocol coverage matrix for “most widespread/common manufacturers”.
2. Home Assistant version/fork and exact boundary between HA runtime and MediaHub Core.
3. Whether Home Assistant add-ons/integrations may execute unchanged or require MediaHub adapters.
4. KINCONY firmware discovery source, authenticity/signature verification, supported board models and safe USB flashing/recovery behavior.
5. Whether automatic firmware flashing requires user confirmation.
6. Exact Loxone integration mechanism.
7. Exact Yandex Cloud architecture and data/privacy boundary.
8. Apple HomeKit bridge architecture and required additional server.
9. Exact Dahua/Hikvision/Ajax product families, protocols, discovery mechanisms and supported camera/NVR/device classes.
10. Recording modes, retention policy, storage quotas, disk failure/recovery and playback/export semantics.
11. Exact disk partition/filesystem model: physical partitions vs logical storage pools/volumes.
12. Whether surveillance storage and media library storage can be resized/rebalanced after installation.
13. Exact meaning of replacing a Ubiquiti server/controller and which controller functions MediaHub assumes.
14. Exact Wi-Fi hardware/radio capabilities required for MediaHub to participate as an AP/mesh node.
15. Exact local-cluster topology, coordination model, workload scheduling, failover and security boundaries.
16. Exact cloud-cluster architecture, resource contribution/consent, metering/limits and data boundary.
17. Ownership/security model for the developer-only cloud development environment.
18. Exact source-ingestion, copyright/licensing and moderation rules for generated educational video.
19. Exact website generation architecture and publishing/deployment flow.
20. Exact iPhone/Android discovery and transport protocols for audio/video.
21. Exact audio direction: phone microphone -> MediaHub, MediaHub -> phone speaker, phone audio -> MediaHub speakers, etc.
22. Exact gaming input/video topology for Xbox/PlayStation and gaming PC.
23. Supported mobile media types, sync direction, conflict resolution, offline behavior and privacy controls.
24. Exact visual UI design system; Apple-inspired visual direction must remain an original MediaHub implementation.
25. Exact event schema, retention, aggregation, deduplication, privacy, cluster synchronization, cloud history, export and notification delivery semantics.

## Recovery classification

All functional blocks explicitly approved by the product owner to date are CONFIRMED_ACCEPTED. Technical details explicitly listed as requiring later clarification remain unresolved and are not silently converted into implementation decisions.
