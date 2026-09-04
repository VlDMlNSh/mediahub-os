# MediaHub — F-010 Personal Media Library / Ingestion / Sync

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED

## Functional requirements

### Personal Media Library
- MediaHub provides one logical Personal Media Library for authorized users.
- The library supports photos, video, audio and other permitted media formats.
- The final exhaustive format list remains deferred.

### Unified library
- Authorized MediaHub, iPhone, iPad, Android and other supported clients can access the same logical library.
- Users should perceive one library rather than unrelated copies.

### Media ingestion
- MediaHub can ingest permitted media from mobile devices, external storage, local network sources, other MediaHub nodes and other supported sources.
- Where possible, MediaHub preserves content identity, metadata, source/provenance, date/time, user association and processing history.

### Automatic organization
- MediaHub can identify media type, extract metadata, index content, detect duplicates, associate related objects and prepare content for search without requiring manual cataloguing.

### Mobile synchronization
- iPhone/iPad/Android clients can synchronize with the Personal Media Library.
- Depending on user settings, synchronization may be device-to-MediaHub, MediaHub-to-device or bidirectional.
- Conflict semantics remain deferred.

### Offline-first
- Mobile and MediaHub components account for temporary connectivity loss.
- Eligible local changes may be retained and synchronized after connectivity returns.

### Search
- Personal Media Library integrates with MediaHub Search.
- Search can use names, metadata and other indexed characteristics.
- Knowledge Graph and Local Assistant may later extend media search capabilities.

### Playback
- Library content integrates with MediaHub Playback and can be rendered through supported MediaHub, HDMI, audio and mobile endpoints.

### MediaHub Cluster
- Multiple MediaHub nodes may jointly provide storage, indexing, processing, transcoding, redundancy and availability for the logical library.
- Internal physical distribution must remain hidden from ordinary users.

### Storage domain separation
- Surveillance Recording Storage and Personal Media Library Storage are separate logical storage domains, even if they use the same physical storage infrastructure.

## Explicitly deferred technical decisions

1. Complete media-format matrix.
2. Exact ingestion sources.
3. Synchronization protocols.
4. Deduplication algorithm.
5. Conflict resolution.
6. Metadata schema.
7. Retention policy.
8. Physical storage layout.
9. Encryption details.
10. Cloud backup.
11. DRM.
12. Transcoding profiles.
13. Offline conflict semantics.

## Main invariant

MediaHub presents one logical Personal Media Library across authorized devices and MediaHub nodes, regardless of where data is physically stored or processed.
