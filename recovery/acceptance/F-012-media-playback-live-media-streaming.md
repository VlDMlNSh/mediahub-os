# MediaHub — F-012 Media Playback / Live Media / Streaming

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED

## Functional requirements

### Unified Media Playback
- MediaHub provides a unified playback system for video, audio, photos, live media, streaming content, Personal Media Library content and permitted external content.
- The user receives one coherent playback model rather than separate subsystem-specific players.

### Media endpoints
- Playback may target MediaHub, HDMI displays, televisions, audio systems, supported network devices, iPhone/iPad and other supported endpoints.

### HDMI
- HDMI is a primary local media-output path.
- It may carry movies, video, photos, the MediaHub interface, live video, surveillance camera views, gaming content and other permitted media.

### Live Media
- MediaHub supports live media as a distinct media-stream type.
- Sources may include cameras, network sources, mobile devices, other MediaHub nodes and other supported external sources.

### Streaming
- MediaHub supports streaming playback where supported by the source, network and hardware.
- Internal transport technology is not part of the ordinary user-facing model.

### Phone as media source
- iPhone/Android may act as media sources for MediaHub and supported endpoints.
- Supported content includes video, photos and audio.

### MediaHub to phone
- MediaHub may deliver permitted media to mobile devices for viewing, listening, remote access, Personal Media Library access and offline copies.

### 4K
- MediaHub should support 4K playback where source content, network, decoding hardware and output device permit it.
- 4K capability does not override hardware or source limitations.

### Transcoding
- If direct playback is not possible, MediaHub may transcode content.
- Transcoding may be performed locally, on another MediaHub Cluster node or in an authorized compute context.
- Users do not manually select internal compute nodes.

### Playback control
- Where supported, the unified control model includes play, pause, stop, seek, volume, mute, source selection, output selection, track selection, subtitle selection and other applicable controls.

### Local-first
- Local media and local sources should be playable without mandatory dependence on external cloud services when local infrastructure is sufficient.

### Cluster
- MediaHub Cluster may distribute streaming, transcoding, storage access, media processing and delivery.
- The user-facing model remains a unified MediaHub media system.

## Explicitly deferred technical decisions

1. Specific streaming protocols.
2. Codecs.
3. Containers.
4. DRM.
5. AirPlay/Chromecast and other concrete technologies.
6. Exact HDMI stack.
7. HDR profiles.
8. Audio formats.
9. Adaptive bitrate implementation.
10. Exact transcoding profiles.
11. Cloud streaming architecture.

## Main invariant

MediaHub provides a unified user-facing playback model in which the source, processing, storage and endpoint may reside on different nodes while the user controls one coherent Media Playback system.
