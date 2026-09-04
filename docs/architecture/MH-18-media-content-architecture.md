# MH-18 — MEDIA / CONTENT ARCHITECTURE
Status: PROPOSED / NOT ACCEPTED / NOT FROZEN
Date: 2026-09-04

## 1. Canonical invariant
MediaHub manages media/content as a domain, but content bytes, metadata, catalog, storage, index, cache and derivatives are never State Authority.

Source → Ingestion → Validation → Normalization → Content Model → Authorized Command → P0-05 → State Authority → Catalog/Metadata → Storage/Index/Playback.

No media file, indexer, transcoder, AI component, plugin, device or provider may bypass authorization.

## 2. Model and identity
Content is logical work; Asset is acquired representation; Object/File is byte object; Storage Locator is mutable physical location; External ID is provider-scoped; Digest/fingerprint are evidence; Version is schema/representation version. Filename/path/URL/digest are not domain identity.

## 3. Lifecycle
DISCOVERED → INGESTING → VALIDATING → REGISTERED → INDEXED → AVAILABLE → PROCESSING → PUBLISHED → ARCHIVED → DELETED/QUARANTINED. Every transition has owner, authorization, observable failure and recovery semantics. Device lifecycle schema is not reused for media lifecycle.

## 4. Ingestion and validation
Sources are untrusted by default. Pipeline: discovery, intake, identity, integrity, malware/safety analysis, extraction, normalization, classification, policy, registration, indexing, availability. Limits, timeout, cancellation, retry budget and idempotency are mandatory. Validation covers syntax, container/format, codec/stream, metadata, security, policy and rights. Malformed/hostile media is rejected, quarantined or requires verification.

## 5. Metadata/provenance
Metadata sources: user, provider, device, extracted, computed, AI. Facts carry provenance, timestamp, version and confidence where applicable. Conflicts are explicit and resolved by contract/policy/user; no hidden priority. AI output is candidate data until authorized.

## 6. Storage
Separate canonical metadata/state, content bytes, derivatives and cache. Storage is not authority. Candidate backends remain unselected pending evidence/ADR. Deletion distinguishes catalog removal, byte deletion, derivative/cache purge, external-copy revocation, secure deletion and retention hold.

## 7. Derived systems
Index, search, thumbnails, previews, waveforms and transcodes are derived/rebuildable. Canonical Catalog → Index Builder → Search Index. Search result is never canonical state. Transcoding is isolated, bounded, cancellable, observable and cannot mutate canonical state directly.

## 8. Playback/streaming
Playback uses authorized read model → media session → resolver → storage → decoder/player → output device. Session state is separate from global runtime state. LAN/remote streaming requires authentication, authorization, quotas and observability. Local operation must degrade gracefully without cloud.

## 9. Playlists/subtitles
Playlist is ordered references; queue is session ordering; collection is grouping; smart collection is derived query unless explicitly modeled; favorite/bookmark are references. Multiple audio/subtitle tracks are supported architecturally. External subtitle/artwork data is untrusted.

## 10. Rights/DRM
Rights metadata is descriptive and does not grant authorization. Provider/DRM authority remains external. No bypass, forged entitlement or circumvention. DRM integration requires platform, licensing, security and governance evidence.

## 11. Devices/live media
MH-17 owns device/protocol boundary. Devices are not authority. Camera/microphone/live streams require explicit privacy/security authorization, bounded capture, retention and storage. RTSP/ONVIF/WebRTC are candidates only until verified. Recording enters normal ingestion.

## 12. AI
Media AI may classify, OCR, transcribe, tag, summarize, detect scenes/objects, recommend, embed and identify probable duplicates. Flow: Media → AI → Candidate Metadata → Validation → Policy → Authorization → State Authority. AI cannot silently delete, publish, change rights or expose private media.

## 13. Security/isolation
Threats include malicious media, parser exploits, traversal, archive bombs, malformed codecs/subtitles/artwork, poisoned AI input and exfiltration. Processing requires least privilege, restricted filesystem/network, quotas and suitable isolation. Exact sandbox/codec technology is not canonical without ADR/evidence.

## 14. Privacy
Apply MH-13 minimization, purpose limitation, access control, retention, redaction, explicit external transfer and audit. Do not log media payloads by default. Private content must not cross provider/AI/export boundaries without explicit authorization.

## 15. Backup/recovery/migration
Back up media, canonical metadata and configuration according to separate contracts. Rebuild indexes/derivatives where possible. Restore gate: Integrity → Compatibility → Authorization → Restore → Validation → Health Gate. Data migration is distinct from transcoding.

## 16. Resource governance
Bound file/upload size, metadata, thumbnail/temp storage, index size, streams, processing concurrency, CPU/GPU, memory and bandwidth. Priority must preserve Core Runtime and active user playback over background indexing/AI/cache rebuild.

## 17. APIs/export/plugins
APIs distinguish browse/search/read/playback/import/upload/transcode/export/delete/metadata mutation. Every operation is capability-scoped. Export is explicit, bounded, auditable and privacy-aware. Plugins can extend adapters/providers/analyzers but never become Content or State Authority.

## 18. Technology neutrality
FFmpeg, GStreamer, VLC, databases, search engines, object storage/NAS, CDN and DRM providers are CANDIDATE. Selection requires requirements → compatibility → security/resource/licensing analysis → ADR → evidence.

## 19. Testing/governance
Testing covers contracts, corpus/fuzzing, security, privacy, performance, compatibility, recovery and authorization negatives. Evidence records exact version/platform/configuration/timestamp/scope. No VERIFIED/PASS/ACCEPTED/FROZEN claim is made for untested media implementation.

## 20. Current decision
Repository audit found foundation contracts but no observed media implementation. Therefore MH-18 establishes architecture and gates, not production authorization. Production ingestion, bulk import/export/deletion, storage migration, codec installation, provider/DRM integration and camera/live capture remain unauthorized until separate gates pass.

## 21. Acceptance
Required acceptance includes all 50 requested domains, evidence register, contradiction/unknown resolution, traceability to MH-01…MH-18 and P0-03…P0-07, security/privacy review, tests and governance decision. Current status remains NOT ACCEPTED / NOT FROZEN.
