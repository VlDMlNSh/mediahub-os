# F-015 — HDMI / Display / Visual Output

**Status:** CONFIRMED_ACCEPTED

**Acceptance:** User explicitly approved Block 15, with an additional requirement that the 3.5 mm audio output be preserved in the MediaHub functional baseline.

## 15.1 HDMI as standard MediaHub output

HDMI is a primary local output path for video, photos, MediaHub UI, Live Media, surveillance, movies and other media, gaming content, processing results and other permitted visual data.

## 15.2 TV / monitor / display

A connected HDMI display is a full visual endpoint of MediaHub. MediaHub should discover available displays, determine capabilities where technically possible, offer them as outputs and allow content/output selection.

## 15.3 Unified Display Endpoint model

Display endpoints belong to the common MediaHub Endpoint model and may expose identity, type, connection, availability, resolution, supported modes, current source/content, output state and capabilities such as HDR/color/refresh where available. Exact capability model remains deferred.

## 15.4 MediaHub UI on HDMI

MediaHub may present its UI on an external display, including media library, cameras, Smart Home, home state, notifications, Local Assistant and authorized diagnostics/engineering views.

## 15.5 Playback → HDMI

The Playback subsystem supports HDMI as an output, including Personal Media Library, Live Media and surveillance content.

## 15.6 Phone → MediaHub → HDMI

Phone media and permitted live camera/video content may be routed through MediaHub to an HDMI display.

## 15.7 Surveillance → HDMI

Authorized surveillance live view and archive content may be displayed over HDMI. Multi-camera layout and technical constraints remain deferred.

## 15.8 Gaming → HDMI

Gaming sources including Xbox, PlayStation, gaming PC, MediaHub Gaming and other supported endpoints may use HDMI as a primary local visual output when hardware/topology permit. Protocols, latency, capture/pass-through and topology remain deferred.

## 15.9 Multiple displays

MediaHub should support multiple displays where hardware/topology permit, including independent sources, one source to multiple displays and distributed output through MediaHub Cluster. Exact synchronization and limitations remain deferred.

## 15.10 MediaHub Cluster → Display

A MediaHub Cluster may distribute source, storage, processing/transcoding and HDMI output responsibilities across nodes. Internal routing remains hidden from ordinary users.

## 15.11 4K and other modes

4K and other modern display modes should be supported when source, network, decoder/GPU and display capabilities allow. HDR, refresh rates, color spaces, VRR and similar technical details remain deferred.

## 15.12 Display + Smart Home

HDMI displays may provide visual Smart Home interfaces for rooms, devices, cameras, scenes, automations, energy, notifications and Local Assistant.

## 15.13 Security / Authorization

Protected content and display control remain subject to identity, authorization, security and privacy rules. Physical HDMI connection does not grant additional rights.

## 15.14 Offline-first

Local HDMI output and local MediaHub functions should continue without Internet when required local resources remain available.

## 15.15 3.5 mm analog audio output — preserved requirement

MediaHub must preserve support for a **3.5 mm analog audio output** where the selected MediaHub hardware provides the corresponding physical connector.

The 3.5 mm output is a first-class local audio output path and must integrate with the unified Audio System / Endpoint model from F-013.

It may be used for permitted audio playback and other authorized audio output scenarios, including connection to powered speakers, headphones or other compatible analog audio equipment.

The exact electrical implementation, codec/DAC characteristics, independent-versus-shared output routing, volume semantics and hardware-specific capabilities remain deferred.

This requirement must not be lost during hardware/platform selection or implementation decomposition.

## 15.16 Deferred

HDMI version, HDMI-CEC, HDCP, EDID, GPU/decoder stack, HDR standards, refresh-rate matrix, VRR, ARC/eARC, capture/pass-through, multi-display synchronization, DRM implementation and exact compositor architecture remain deferred.

For 3.5 mm audio: exact hardware implementation, DAC characteristics, routing topology and hardware-specific capabilities remain deferred.

## Main invariants

- HDMI is a standard MediaHub visual output.
- A TV/monitor/display is a first-class Display Endpoint.
- The user interacts with MediaHub's unified output model, not internal transport details.
- Physical HDMI connection does not grant authorization.
- **The 3.5 mm analog audio output is a preserved first-class MediaHub audio output requirement where the hardware provides the connector.**

## Traceability

- Functional domain: 15 — HDMI / Display / Visual Output
- Related accepted blocks: F-007 Users / Identity / Access / Authorization; F-009 Remote Access / Mobile / Cloud Escalation; F-010 Personal Media Library / Ingestion / Sync; F-011 Video Surveillance; F-012 Media Playback / Live Media / Streaming; F-013 Audio System; F-014 Phone as Media / IO Endpoint.
- Technical implementation details not explicitly accepted here remain deferred.
