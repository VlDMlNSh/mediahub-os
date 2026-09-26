# F-006 — Presence / People / Context

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED

## Functional acceptance

- MediaHub determines whether a person is present at home, absent, returning or departing.
- MediaHub may determine presence in a specific room/zone where technically possible.
- Presence sources may include iPhone, Android, Smart Home devices, network signals, motion sensors and other permitted sources.
- MediaHub supports multiple users and distinguishes people when technically possible.
- A user context may include an identifier, associated devices, presence zones, preferences, permissions and personal settings.
- Exact person-identification mechanisms are not fixed by this functional block.
- Presence is part of overall MediaHub context and may feed Automation Engine, Scenes, Notifications, Energy Management, Security, Media, Local Assistant, HVAC, lighting and other authorized subsystems.
- Presence-driven behavior must remain subject to authorization and safety constraints.
- Presence and people data are governed by MediaHub Privacy/Data Governance and Security requirements.
- Presence should not require constant external cloud transfer when local processing is possible and appropriate.
- Different users may have different control rights, settings, preferences, devices, notifications and access to rooms/functions.
- Advanced/Engineer Settings may expose technical presence/context sources and state; ordinary users should not be forced to manage those internals.

## Explicitly unresolved technical decisions

1. Exact person-identification mechanisms.
2. BLE/Wi-Fi/geolocation and other presence-source selection.
3. Zone accuracy and confidence semantics.
4. Privacy consent model.
5. Cloud/local processing and transmission semantics.
6. Conflict resolution and precedence among presence sources.
7. Presence history and retention.
8. Spoofing resistance and security protection.
9. External ecosystem interaction semantics.

## Acceptance meaning

This file records the product-owner acceptance of the functional scope above. It does not authorize implementation of unresolved technical details and does not silently modify MH-01…MH-23 architectural decisions. Reconciliation remains required during the recovery passes.
