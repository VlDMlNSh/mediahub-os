# MediaHub — F-011 Video Surveillance / Recording / Archive

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED

## Functional requirements

### Integrated surveillance
- MediaHub provides an integrated video-surveillance subsystem covering camera discovery, onboarding, control, live view, recording, archive, playback, search, events, notifications and diagnostics.

### First-class vendor requirements
- Dahua, Hikvision and Ajax are first-class out-of-box surveillance integration requirements.
- Coverage is extensible through the Vendor / Protocol Coverage Registry and is not limited to these vendors.

### Automatic discovery and onboarding
- MediaHub discovers available supported cameras, identifies vendor/model/type/capabilities where possible, determines an integration path and offers onboarding.
- User-facing interaction is with the MediaHub camera/device model rather than an integration protocol.

### Direct recording to MediaHub
- MediaHub can record supported camera streams directly to its own storage.
- A separate NVR is not a mandatory architectural component when MediaHub has sufficient capabilities.
- Canonical flow where supported: Camera → MediaHub → Surveillance Storage.

### Surveillance storage
- Surveillance recordings use a distinct logical storage domain: Surveillance Recording Storage.
- Surveillance Recording Storage remains separate from Personal Media Library Storage even when the same physical storage infrastructure is used.

### Archive
- Supported recording modes include continuous recording, event-triggered recording and other supported modes.
- MediaHub provides archive storage, playback, seeking, search and authorized export.

### Live view
- Authorized users can view supported cameras in real time through MediaHub, iPhone/iPad and other supported clients.

### Events and automation
- Surveillance events participate in the common Event Model and can feed Automation, Notifications, History, Diagnostics, Security and Local Assistant.
- Smart Home state and automation may interact with surveillance modes subject to authorization and safety constraints.

### Storage management
- MediaHub accounts for surveillance storage capacity, disk state, occupancy, retention, recording failures, degradation and recovery.

### Cluster
- Multiple MediaHub nodes may jointly provide surveillance recording, processing, transcoding, redundancy, failover and archive availability where technically supported.
- The user-facing model remains one surveillance system rather than a collection of internal storage/compute nodes.

## Explicitly deferred technical decisions

1. Exact supported camera models.
2. Complete vendor matrix.
3. ONVIF profiles.
4. RTSP.
5. WebRTC.
6. Discovery mechanisms.
7. Codecs.
8. Resolution profiles.
9. Bitrate.
10. FPS.
11. Retention policy.
12. Storage quotas.
13. Overwrite policy.
14. Failover semantics.
15. Physical disk architecture.
16. RAID/ZFS/other storage technology.
17. AI video analytics.
18. Person/object detection.
19. Privacy masking.
20. Exact remote-access mechanism.

## Main invariant

MediaHub is a full surveillance node capable, where supported, of discovering, integrating, recording, storing and playing back camera video directly; a separate NVR is not mandatory.
