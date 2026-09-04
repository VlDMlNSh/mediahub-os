# MediaHub — Full Functional Scope / User Baseline

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED BASELINE + USER-REVIEW CORRECTIONS

## 1. Governing principle

This document captures the product-owner-defined functional scope before clean implementation. It is authoritative as a functional input, but does not silently override already accepted architectural invariants. Any conflict with MH-01…MH-23 must be explicitly reconciled and recorded.

The functional baseline is reconstructed first; implementation must not begin until the complete capability inventory, reconciliation and master baseline are accepted.

## 2. Smart Home Hub

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
- The exact initial vendor/protocol coverage matrix is a separate registry to be established; the requirement itself is broad out-of-box coverage of the most widespread smart-home equipment.

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

## 3. Video surveillance

- Out-of-box vendor support is required for Dahua, Hikvision and Ajax.
- Devices from these vendors are automatically detected when they appear on the network.
- MediaHub provides complete integration instructions and distribution/assignment guidance during onboarding.
- Product principle: eliminate unnecessary physical intermediary equipment where possible, such as a separate NVR.
- Recording, archival storage and surveillance playback are performed directly by MediaHub.
- During MediaHub installation, the installer offers disk-space allocation into at least two logical areas:
  1. surveillance recording storage;
  2. media library storage.

## 4. Networking, seamless coverage and MediaHub scaling modes

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

## 5. Distributed cloud development / compute environment

- MediaHub nodes may contribute otherwise-unused compute capacity to a shared cloud development/supercomputing environment.
- The shared environment hosts a cloud assistant.
- MediaHub consults the cloud assistant when local tools/capabilities are insufficient.
- The more Internet-connected MediaHub nodes participate, the more aggregate compute capacity is available to this environment.
- Core development tools/environment controls are restricted to the developer/operator, not ordinary end users.
- A content-generation engine in this environment can study designated sources and generate daily video content.
- Target generated content includes short stories, educational videos, equipment reviews, setup/integration/mounting lectures, electrical lectures and similar technical educational material.
- The environment also supports automatic generation of the MediaHub company website from specified parameters; this will be expanded in a later scope pass.

## 6. Visual/user interface

- Default visual interface is a light-gray waiting/loading screen inspired by the visual simplicity and centered composition of Apple installation/loading screens.
- A centered MediaHub logo is displayed at the corresponding central position.
- This is an intentional product visual direction; implementation must not assume copying proprietary Apple assets.
- MediaHub exposes normal settings and a separate advanced settings area intended for engineers.
- Navigation should be highly intuitive and visually coherent across the product.
- Ordinary users must not be exposed to internal infrastructure complexity such as Home Assistant administration, cluster orchestration or distributed-compute mechanics.

## 7. Phone as media/IO endpoint

- When an iPhone is detected within the relevant connectivity range, MediaHub can connect it.
- MediaHub can route audio/video from the phone to its HDMI output and audio system.
- Target video quality includes 4K where source/network/hardware support permits.
- Because mini PCs/Mac mini-class devices may lack a built-in microphone, a connected iPhone or Android device can serve as an audio input/output endpoint; the exact audio routing semantics require clarification.
- Android is also a supported phone endpoint.

## 8. Game controllers and gaming

- MediaHub supports common console controllers, including Xbox and PlayStation controllers.
- Controllers can be used for MediaHub navigation and gaming.
- Games can be played from consoles and from a gaming PC.
- Video from a console or phone can be routed directly to MediaHub HDMI output.
- Exact console/PC transport protocol and capture/input topology remain to be specified.

## 9. Personal media library

- MediaHub contains a media library for users.
- Users can synchronize the media library with iPhone and Android devices.
- Goal: create a shared/common media library across MediaHub and user mobile devices.

## 10. Cross-cutting product principles recovered from this scope

- Hidden implementation layers should be replaced by a unified MediaHub experience where technically feasible.
- Home Assistant is an internal implementation component, not a user-facing product or user-facing mental model.
- Automatic discovery and guided onboarding are first-class product behavior.
- Contextual instructions should be actionable, not merely descriptive.
- Local-first operation is strongly implied for core smart-home, surveillance, networking and assistant functions; exact cloud fallback rules require formalization.
- Engineer/advanced configuration exists separately from ordinary user settings.
- Network extension, local clustering and cloud clustering should be exposed as simple MediaHub configuration choices while implementation complexity remains internal.
- MediaHub is intended to unify smart home, surveillance, networking, media, mobile-device integration and distributed compute under one product surface.

## 11. Items explicitly requiring clarification / acceptance

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

## 12. Recovery classification

The core functional scope previously explicitly approved by the product owner remains CONFIRMED_ACCEPTED. The smart-home abstraction correction and MediaHub scaling/network modes are recorded here as the current user-review correction and must receive explicit user acceptance before being promoted to the immutable master baseline.
