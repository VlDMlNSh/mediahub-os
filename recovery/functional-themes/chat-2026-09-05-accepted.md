# MediaHub Functional Recovery — Accepted Additions from 2026-09-05 Concept Discussion

**Status:** CONFIRMED_ACCEPTED
**Recovery stream:** full-functional-spec
**Date:** 2026-09-05

This artifact preserves the functions explicitly accepted by the user in the 2026-09-05 recovery discussion. It is a functional record, not an implementation authorization.

## 1. Product concept

MediaHub is an engineering system and product of a construction/installation organization engaged in smart-home and building engineering design, installation, integration, automation, commissioning, operation, diagnostics, modernization and lifecycle support.

MediaHub unifies home equipment, Smart Home, lighting, automation, climate, ventilation, heating, energy systems, security, video surveillance, networking and media.

## 2. Canonical integration and automation core

Home Assistant is the single source of truth for equipment integration and automation inside MediaHub.

The Home Assistant user interface is absent. Home Assistant is an internal, maximally automated technology layer; MediaHub is the sole user-facing product model for the integrated home.

The system should hide protocol/integration complexity from the user while exposing device/function semantics through MediaHub.

## 3. Lighting and automation

MediaHub provides broad out-of-box support for major automation and lighting manufacturers and common wired/wireless automation systems.

Wired systems include KNX, DALI, RS-485 and other wired systems, integrated through manufacturer or existing compatible hubs where appropriate. Wireless automation systems are also supported.

KINCONY boards running KCS are primary automation elements. When an empty compatible KINCONY board is connected to MediaHub by USB, MediaHub detects it, installs the latest KCS firmware, brings it onto the network, and exposes relevant KCS interface components through the unified MediaHub settings/UI.

Lighting includes relay controllers, dimmers and extensions for KNX, DALI and other wired systems. Boxed support includes Centrsvet, Arlight, Maytoni and other common manufacturers.

## 4. Surveillance, security and intermediate-layer reduction

Boxed support includes Dahua, Hikvision, Ajax and similar common systems.

Where technically possible, MediaHub reduces intermediate physical equipment by implementing functions directly or through software/virtualized services; a separate NVR or security panel is not inherently mandatory where MediaHub can provide the required function.

## 5. Climate, ventilation, heating and energy

MediaHub integrates climate, ventilation and heating systems.

Energy infrastructure includes supported solar panels, wind generators, generators, UPS systems, batteries/storage and other energy sources/equipment, as one integrated engineering system.

## 6. Network infrastructure

MediaHub devices connect to the network through UTP/Ethernet using RJ-45.

MediaHub can participate directly in wireless-network construction with other MediaHub nodes and network equipment such as Keenetic and Ubiquiti, including router and access-point roles and contribution to wireless coverage.

Network configuration can select ordinary direct Internet networking or a specialized VPN network, subject to later technical definition.

MediaHub can reduce intermediate physical infrastructure where possible by deploying virtual/software services instead of dedicated hardware.

Multiple MediaHub devices on the local network can form a local MediaHub Cluster and redistribute compute resources.

Internet-connected MediaHub devices can participate in a separate Cloud Development Cluster/cloud development environment. Ordinary users never receive direct access to Cloud Development.

## 7. UI/UX and contextual guidance

The MediaHub UI is minimalist, intuitive and visually inspired by the navigation and simplicity of iOS/macOS.

The standby screen uses a light-gray visual treatment and an Apple-like centered startup visual concept as specified by the user; exact implementation remains subject to platform/legal/technical constraints.

A settings entry is available in the upper-left area and includes Smart Home, automation, network and required system settings, plus an Engineering mode and expanded Installer mode with a broad range of settings.

The standby/home screen provides compact entry points for games, media, Smart Home, surveillance/live view/archive and other core functions.

Across installation, integration, configuration, automation and external ecosystem export, MediaHub provides small contextual pop-up hints. Selecting a hint opens a full actionable step-by-step instruction to simplify user coordination.

## 8. Mobile endpoints and media routing

When a phone is nearby, its microphone can be used as an input device for MediaHub where supported/authorized.

MediaHub supports routing audio and video from a phone to HDMI and 3.5 mm audio output, including 4K video where source, network and hardware permit.

MediaHub has a remote Smart Home/mobile application with remote access to the Personal Media Library subject to authorization.

User and Developer mobile applications are distinct products with different permission/capability surfaces.

## 9. External ecosystem projection

Integrated and configured Smart Home equipment can be automatically exposed/projected to supported external ecosystems such as Apple HomeKit, Yandex Alice and Loxone when the required iPhone/iPad and/or local-network conditions are present.

MediaHub includes a planned internal Loxone mini-server capability so that Loxone-related integration can be hosted within MediaHub rather than requiring an unnecessary separate physical server, subject to technical definition.

The user interacts with MediaHub as the primary system model; external ecosystem projection is an integration function.

## 10. Local Assistant and cloud assistance

A local AI/home assistant runs locally inside MediaHub.

It helps with equipment integration, equipment configuration, automation creation/modification, media and audio stream control, explanation and diagnostics.

The Local Assistant may call a cloud assistant when the task cannot be solved within the local network or when local response generation would take too long. Cloud assistance remains an internal service path rather than direct user access to Cloud Development.

## 11. Cloud Development environment

The Cloud Development environment is intended for MediaHub company's own operational/development needs.

It includes site generation and company-internal development services, including an engine that studies trusted sources and generates media/content.

A separate engineering-system contour generates engineering instructions, diagrams, cable schedules and related engineering artifacts.

## 12. Commercial/professional engineering edition

MediaHub is developed as a commercial/professional version for developers, engineers and integrators.

Every project starts from a designer project. MediaHub accepts designer source material including PDF documents, images and drawings.

MediaHub processes these materials, creates a virtual twin/digital representation of the object, and, together with installer instructions, develops engineering-system schemes, assists with equipment selection and manages the object through completion.

MediaHub prepares as-built/executive documentation.

## 13. Updates

MediaHub system updates should provide an iOS-like update experience.

A new update appears in the Updates section with a user-facing description of new functions/features.

The user explicitly performs/initiates the update rather than having silent uncontrolled updates.

## 14. Self-recovery and filesystem control

MediaHub is self-recovering/resilient by design.

It creates recovery checkpoints and directly manages the filesystem as required to support system recovery and integrity.

Exact checkpoint, filesystem, rollback, backup and recovery implementation semantics remain subject to later technical specification unless separately accepted.

## 15. Product variants and media/storage capabilities

MediaHub has distinct variants: full Mac mini, mini PC, simplified Raspberry Pi, and iOS for iPhone/iPad deployed on the object.

The Raspberry Pi and iOS variants do not include local hard-disk surveillance-stream recording or local Personal Media Library storage.

The full Mac mini concept includes use of the Mac mini's standard/original audio capability and supports construction of a MediaHub Hi-End audio system. The minimum Hi-End configuration includes a soundbar and can expand with two floor-standing speakers.

## Acceptance statement

All functions in this artifact were explicitly accepted by the user in the 2026-09-05 discussion. They must be preserved in the functional master inventory and must be traceable into later architecture, implementation and testing. Acceptance here does not by itself authorize implementation of deferred technical details.
