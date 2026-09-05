# MediaHub — F-013 Audio System

Date: 2026-09-05
Status: CONFIRMED_ACCEPTED

## Functional requirements

### Unified audio system
- MediaHub provides one audio subsystem for music, video audio, Personal Media Library, streaming audio, live audio, system sounds, Local Assistant voice interaction and other authorized MediaHub audio output.

### Audio sources
- Sources may include Personal Media Library, iPhone/iPad, Android, MediaHub, other MediaHub nodes, network sources, Smart Home/external multimedia devices and other supported external sources.

### Audio endpoints
- Output may target built-in or attached audio devices, HDMI, network audio devices, supported AV receivers, speakers, mobile devices, other MediaHub nodes and other supported endpoints.

### Multi-room Audio
- Multiple MediaHub and supported audio devices may form one multi-room audio system.
- Users can select a room or group of rooms, play one source across multiple zones where supported, synchronize playback where supported and independently control zones.

### Phone as audio endpoint
- A phone may act as an audio source to MediaHub or receive MediaHub audio, subject to authorization and supported capabilities.

### Audio routing
- MediaHub routes audio between available sources and endpoints.
- The ordinary user model is Source → Room/Zone → Audio System; internal routing protocols are hidden.

### Control
- Where supported, unified controls include play/pause, stop, seek, volume, mute, source selection, zone selection, zone grouping/separation, track selection and other endpoint-specific controls.

### Smart Home integration
- Audio participates in automations, scenes, schedules, presence, notifications, events and Local Assistant scenarios.

### Local Assistant
- Local Assistant can perform authorized audio actions such as playback, stop, volume changes, source/zone selection and state explanation through the unified MediaHub model.

### Cluster
- MediaHub Cluster may distribute audio storage, processing, streaming, transcoding, delivery and zone coordination.
- Users experience one MediaHub audio system.

## Explicitly deferred technical decisions

1. Specific audio protocols.
2. AirPlay/Chromecast and analogous technologies.
3. Specific AV receiver models.
4. Specific speaker models.
5. Bluetooth profiles.
6. Hi-Res/DSD and other specialized formats.
7. Multi-room synchronization protocol.
8. DSP.
9. Room correction.
10. Exact hardware audio-output configuration.

## Main invariant

MediaHub represents audio as one integrated system of sources, zones and endpoints while hiding internal protocols, routing and distributed processing from ordinary users.
