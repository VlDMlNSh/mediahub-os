# MediaHub — Full Functional Scope / User Baseline v0.1

Date: 2026-09-04
Status: RECOVERED FROM PRODUCT OWNER DESCRIPTION / REQUIRES ARCHITECTURAL RECONCILIATION

## 1. Governing principle

This document captures the product-owner-defined functional scope before clean implementation. It is authoritative as a functional input, but does not silently override already accepted architectural invariants. Any conflict with MH-01…MH-23 must be explicitly reconciled and recorded.

## 2. Smart Home Hub

- MediaHub is primarily a smart-home hub.
- Home Assistant is the underlying smart-home integration and automation engine.
- Home Assistant has no external user-facing interface in the product; it is embedded/hidden inside the MediaHub core.
- MediaHub provides a unified native user interface over the underlying Home Assistant functionality.
- Out-of-box support is required for automatic discovery/addition of devices from common smart-home manufacturers.
- When a new device appears on the network, MediaHub automatically detects/indicates it and starts the onboarding flow.
- Onboarding offers room assignment and device-type classification.
- Throughout discovery, installation and configuration, MediaHub provides contextual pop-up hints, installation instructions and configuration guidance.
- Guidance may include concrete network/configuration actions, including which IP address/page to open and what settings to change when required.

### KINCONY

- KINCONY is a first-class supported vendor/integration.
- KINCONY boards are added to MediaHub via MQTT and use KCS vendor firmware.
- The KCS primary web interface is proxied/embedded into the MediaHub UI and exposed in settings for detailed board configuration.
- When a blank/unflashed KINCONY board is connected to MediaHub by USB, MediaHub detects it.
- MediaHub locates the latest firmware for the detected board on the KINCONY forum/source and flashes the board.
- The KINCONY onboarding flow then continues into normal MediaHub integration.

### Smart-home external ecosystem export

- The integrated smart-home system is exportable/bridgeable to remote user applications/ecosystems including Loxone, Yandex Alice and Apple HomeKit.
- Apple HomeKit integration may require an additional server in the local network.
- Yandex Alice integration is intended through Yandex Cloud.
- A proprietary MediaHub assistant is intended for Loxone onboarding and automation construction.
- The Loxone assistant runs locally on MediaHub.

## 3. Video surveillance

- Out-of-box vendor support is required for Dahua, Hikvision and Ajax.
- Devices from these vendors are automatically detected when they appear on the network.
- MediaHub provides complete integration instructions and distribution/assignment guidance during onboarding.
- Product principle: eliminate unnecessary physical intermediary equipment where possible, such as a separate NVR.
- Recording, archival storage and surveillance playback are performed directly by MediaHub.
- During MediaHub installation, the installer offers disk-space allocation into at least two logical areas:
  1. surveillance recording storage;
  2. media library storage.

## 4. Networking

- Out-of-box support is required for Ubiquiti and Keenetic networking equipment.
- Product principle: eliminate unnecessary physical intermediary infrastructure where possible.
- MediaHub is intended to replace a Ubiquiti server/controller layer where applicable.
- MediaHub can participate directly in building/extending a seamless wireless home network alongside Keenetic and Ubiquiti equipment.
- Example target deployment: one Ubiquiti access point plus one MediaHub can provide/extend home wireless coverage.
- Multiple MediaHub units in one local network form a local cluster.
- The cluster redistributes computing tasks/workloads among MediaHub nodes and supports additional coordinated functions.
- The cluster also participates in seamless wireless networking.
- MediaHub settings allow selection of which connection/path it rebroadcasts as the wireless network uplink: ordinary Internet or Internet routed through VPN.

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
- Automatic discovery and guided onboarding are first-class product behavior.
- Contextual instructions should be actionable, not merely descriptive.
- Local-first operation is strongly implied for core smart-home, surveillance, networking and assistant functions; exact cloud fallback rules require formalization.
- Engineer/advanced configuration exists separately from ordinary user settings.
- MediaHub is intended to unify smart home, surveillance, networking, media, mobile-device integration and distributed compute under one product surface.

## 11. Items explicitly requiring clarification / acceptance

1. Exact definition of “all common manufacturers” and the initial supported vendor/protocol matrix.
2. Home Assistant version/fork and exact boundary between HA runtime and MediaHub core.
3. Whether Home Assistant add-ons/integrations may execute unchanged or require MediaHub adapters.
4. KINCONY firmware discovery source, authenticity/signature verification, supported board models and safe USB flashing/recovery behavior.
5. Whether automatic firmware flashing requires user confirmation.
6. Exact Loxone integration mechanism and meaning of “MPV”/proprietary assistant terminology.
7. Exact Yandex Cloud architecture and data/privacy boundary.
8. Apple HomeKit bridge architecture and required additional server.
9. Exact Dahua/Hikvision/Ajax product families, protocols, discovery mechanisms and supported camera/NVR/device classes.
10. Recording modes, retention policy, storage quotas, disk failure/recovery and playback/export semantics.
11. Exact disk partition/filesystem model: physical partitions vs logical storage pools/volumes.
12. Whether surveillance storage and media library storage can be resized/rebalanced after installation.
13. Exact meaning of replacing a Ubiquiti server/controller and which controller functions MediaHub assumes.
14. Exact Wi-Fi hardware/radio capabilities required for MediaHub to participate as an AP/mesh node.
15. Exact cluster topology, consensus/coordination model, workload scheduling, failover and security boundaries.
16. Whether compute contribution to the shared cloud environment is opt-in, how resources are metered/limited, and what data/code may cross the local boundary.
17. Ownership/security model for the developer-only cloud development environment.
18. Exact source-ingestion, copyright/licensing and moderation rules for generated educational video.
19. Exact website generation architecture and publishing/deployment flow.
20. Exact iPhone/Android discovery and transport protocols for audio/video; whether this means AirPlay, Miracast, WebRTC, USB, proprietary transport, or multiple paths.
21. Exact audio direction: phone microphone -> MediaHub, MediaHub -> phone speaker, phone audio -> MediaHub speakers, etc.
22. Exact gaming input/video topology for Xbox/PlayStation and gaming PC.
23. Supported mobile media types, sync direction, conflict resolution, offline behavior and privacy controls.
24. Exact visual UI design system; Apple-inspired visual direction must remain an original MediaHub implementation.

## 12. Recovery classification

All capabilities in this document are classified as PRODUCT-OWNER-DECLARED / RECOVERED INPUT for the new master specification. They must be mapped against MH-01…MH-23 and development history before implementation authorization.
