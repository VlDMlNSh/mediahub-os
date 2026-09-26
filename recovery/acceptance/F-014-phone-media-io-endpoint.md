# F-014 — Phone as Media / IO Endpoint

**Status:** CONFIRMED_ACCEPTED

**Acceptance:** User explicitly approved Block 14.

## 14.1 Role of phone

iPhone/iPad/Android may act as:
- MediaHub user UI;
- media source;
- media receiver;
- audio endpoint;
- video endpoint;
- camera/microphone IO endpoint;
- Personal Media Library device;
- remote MediaHub endpoint.

## 14.2 Phone → MediaHub

The phone may transmit photos, video, audio and other supported media, and live camera/audio input in allowed scenarios. Content may enter the Personal Media Library or be used directly.

## 14.3 MediaHub → Phone

The phone may receive video, photos, audio, live media, surveillance live view, Personal Media Library content and other permitted data.

## 14.4 Phone as camera

The phone may provide an additional video/IO source where the scenario and permissions allow it.

Canonical example: Phone Camera → MediaHub → Display / Recording / Processing.

Exact scenarios remain deferred.

## 14.5 Phone as microphone/audio input

The phone may provide audio/voice input in allowed scenarios.

## 14.6 Phone as remote endpoint

The MediaHub User App operates locally and remotely. Remote access must not automatically increase rights.

## 14.7 Phone ↔ Personal Media Library

The phone is a primary client of the unified Personal Media Library. Supported flows include Phone → MediaHub, MediaHub → Phone and bidirectional synchronization. Offline-first behavior is required; detailed conflict semantics remain deferred.

## 14.8 Phone ↔ Playback

The phone may send media to MediaHub, receive media from MediaHub, select playback endpoints, control playback and act as a playback endpoint.

## 14.9 Phone ↔ Surveillance

An authorized phone may live-view surveillance, access authorized archive material and receive surveillance notifications and related events.

## 14.10 Phone ↔ Local Assistant

The User App is a mobile interaction point for the MediaHub Local Assistant. The user interacts with MediaHub; the Assistant uses local resources first and may use additional compute when permitted. The user has no direct Cloud Development access.

## 14.11 Multiple phones/users

Multiple mobile devices and users are supported, with potentially different rights, settings, library access, notification preferences, room/zone access and available functions.

## 14.12 Security

A phone is not trusted merely because it is discovered or present on the network.

Invariants:
- Discovery ≠ Trust
- Presence ≠ Authentication
- Authentication ≠ Authorization

## 14.13 Deferred

Remote protocol, NAT traversal, VPN/direct/relay mechanisms, mobile API, camera streaming, audio transport, synchronization/conflict resolution, encryption and iOS/Android background execution limits remain deferred.

## Main invariant

**The phone is a fully capable authorized Media/IO endpoint of MediaHub, not merely a remote control.**

## Traceability

- Functional domain: 14 — Phone as Media / IO Endpoint
- Related accepted blocks: F-007 Users / Identity / Access / Authorization; F-009 Remote Access / Mobile / Cloud Escalation; F-010 Personal Media Library / Ingestion / Sync; F-011 Video Surveillance; F-012 Media Playback / Live Media / Streaming; F-013 Audio System.
- Technical implementation details not explicitly accepted here remain deferred.
