# MediaHub OS — GitHub Component Reconciliation 2.1 / Media Deep Pass

Date: 2026-10-01
Parent baseline: docs/checkpoints/mediahub-github-component-reconciliation-2.0.md
Status: QUALIFIED MEDIA DEEP-PASS

## Result

A second GitHub pass was performed against the MediaHub capability matrix, contract map and repository candidates. The pass specifically tested whether media transport, live streaming, camera/NVR, playback, music, multiroom audio and photo/video management were already available as mature blocks.

## Decisions

### 1. MediaMTX — ADD / TARGET-GATED
Repository: https://github.com/bluenviron/mediamtx

Role:
- generic live-media router/proxy;
- RTSP, RTMP, WebRTC, HLS, SRT, Media-over-QUIC and related protocol handling;
- protocol conversion;
- stream forwarding/proxying;
- recording/playback of live streams;
- Prometheus-compatible metrics.

Reason:
MediaMTX fills the generic live media transport layer more completely than implementing protocol routing inside MediaHub.

Boundary:
MediaHub owns source identity, stream identity, authorization, policy, lifecycle and canonical metadata. MediaMTX owns media transport mechanics only.

### 2. go2rtc — RETAIN / SPECIALIZED CAMERA STREAM ADAPTER
Repository: https://github.com/AlexxIT/go2rtc

Role:
- camera-centric low-latency streaming;
- codec negotiation;
- WebRTC/RTSP and many camera protocols;
- two-way camera audio;
- integration adapter.

Decision:
Do not use MediaMTX and go2rtc as uncontrolled duplicate general-purpose routers.

Use:
- MediaMTX = general media transport plane where required.
- go2rtc = camera-specific adapter where its camera compatibility/latency capability materially exceeds the generic transport path.

Activation of both requires explicit boundary mapping and measured non-overlap.

### 3. Jellyfin — RETAIN / WHOLE MEDIA SERVICE CANDIDATE
Repository: https://github.com/jellyfin/jellyfin

Role:
- media library;
- metadata;
- playback service;
- transcoding orchestration;
- client/server media delivery.

Decision:
Do not reproduce a second media-library/server stack inside MediaHub.

MediaHub integrates Jellyfin through an adapter and normalizes its capabilities into MediaHub_Media_Contract.

### 4. Music Assistant — RETAIN / WHOLE MUSIC SERVICE CANDIDATE
Repository: https://github.com/music-assistant/server

Role:
- provider aggregation;
- music library;
- player control;
- multi-provider playback orchestration.

Decision:
Whole-product deployment is preferable to reimplementing provider/player integration breadth.

### 5. Snapcast — RETAIN / WHOLE SYNCHRONIZED AUDIO SERVICE CANDIDATE
Repository: https://github.com/snapcast/snapcast

Role:
- synchronized multiroom audio transport.

Decision:
MediaHub owns zones, identities, policy and desired playback state; Snapcast owns synchronization mechanics.

### 6. Frigate — RETAIN / WHOLE CAMERA/NVR SERVICE CANDIDATE
Repository: https://github.com/blakeblackshear/frigate

Role:
- local NVR;
- recording;
- camera processing;
- object detection;
- camera live view.

Decision:
Do not implement NVR internals in MediaHub.

### 7. Immich — RETAIN / WHOLE PHOTO/VIDEO SERVICE CANDIDATE
Repository: https://github.com/immich-app/immich

Role:
- photo/video ingestion;
- organization;
- search;
- mobile backup workflows.

Decision:
Do not reproduce a mature photo/video management system inside MediaHub.

## Non-adoption after this pass

- nginx-rtmp-module: no need while a modern general media router exists.
- Ant Media Server: capability overlap and unnecessary complexity for the current MediaHub media boundary.
- OvenMediaEngine: reference/alternative only; no demonstrated gap versus MediaMTX.
- UniversalMediaServer/Gerbera: legacy/protocol-specific alternatives; no current capability gap.
- additional NVR projects: no demonstrated advantage over Frigate.
- additional multiroom projects: no demonstrated advantage over Snapcast.
- additional media-library products: no demonstrated advantage over Jellyfin.
- duplicate photo/video platform: no demonstrated advantage over Immich.

## Media plane after reconciliation

MediaHub Media Domain
  -> MediaHub Media Contract
  -> source/endpoint adapters
  -> [Jellyfin] media library/playback service
  -> [Music Assistant] music orchestration
  -> [Snapcast] synchronized audio
  -> [Frigate] camera/NVR
  -> [Immich] photo/video
  -> [MediaMTX] generic live-media transport
  -> [go2rtc] camera-specific streaming adapter where required
  -> [FFmpeg] codec/transcode primitive
  -> [OpenCV] vision primitive where required

None of these components becomes MediaHub State Authority.

## Remaining gates before activation

1. Version/tag pinning.
2. License/redistribution review.
3. SBOM/provenance.
4. Security review.
5. API/adapter contracts.
6. Identity mapping.
7. Storage boundary.
8. Resource limits.
9. Failure/degraded semantics.
10. Recovery/restore.
11. Upgrade/rollback.
12. Performance qualification.
13. Privacy/egress qualification.
14. Independent qualification.

## Loop result

No additional mature media product was found that justifies another production dependency after this pass.

The media component graph is now considered CLOSED FOR SELECTION, pending implementation-time qualification of the explicitly gated components.

Architecture was not changed.
