# MH-18 — Media / Content Architecture

**Status:** PROPOSED — AUDIT IN PROGRESS
**Branch:** `mh-18-media-content-architecture`
**Date:** 2026-09-04

## 1. Scope

Media/content subsystem for MediaHub OS 11.x LTS / MediaHub iOS: ingestion, content identity, metadata, catalog, storage, derived artifacts, indexing/search, playback/streaming, processing, AI enrichment, rights/DRM boundary, device/live-media interaction, privacy, security, backup/recovery, observability and governance.

## 2. Governing invariant

Media content, metadata, catalog, storage, indexes, caches and derived artifacts are NOT State Authority. Canonical runtime/domain mutation remains behind the existing State Authority / consumer boundary.

Canonical conceptual flow:

`Source → Ingestion → Validation → Normalization → Content Model → Authorized Command → State Authority → Catalog/Metadata → Storage/Index/Playback`

No media file, indexer, transcoder, AI component or plugin may bypass the authorized mutation path.

## 3. Current repository evidence

Repository: `VlDMlNSh/mediahub-os`, default branch `main`.

Observed repository structure contains:
- `contracts/ai` with AI inference/model/provider contracts;
- `contracts/core` and `contracts/identity`;
- `schemas/domain` with generic domain schemas including identity, lifecycle, device, endpoint, relationship and state;
- `schemas/ai` with AI request/response/model/provider schemas;
- `docs/architecture` currently containing P0-06 Core Runtime Services artifacts;
- `tests/ai`, `tests/contracts`, `tests/domain`, `tests/schemas`, `tests/static`;
- CI workflows for P0-06/P0-07/P0-08 and bridge verification.

README currently describes the repository only as the foundation repository for MediaHub OS.

## 4. Audit classification

### VERIFIED

- The repository is private and its default branch is `main`.
- Current HEAD observed during audit is `6eb2ef9efc3ebe6cb89594a0d7180ed7a4c4cb18`.
- P0-06 explicitly preserves a single canonical State Authority and requires service access through P0-05.
- P0-06 explicitly excludes durable persistence, network transport/mutation, subprocess/shell execution, arbitrary filesystem mutation, cloud/hardware persistence, plugin subsystem implementation and autonomous AI mutation.
- An identity-boundary schema exists and defines device, binding, adapter, capability, event, command, execution, request, correlation, causation and recovery identities.
- A domain lifecycle schema exists, but it describes MediaHub Device lifecycle, not media-content lifecycle.
- AI inference request schema exists with operations including generate, classify, embed, transcribe and transform.
- No repository evidence was found for FFmpeg, GStreamer or VLC integration.
- No repository evidence was found for media-specific ingestion, playback, streaming, transcoding, subtitles, playlists, camera/live media, media storage or media index implementation.

### OBSERVED

- The repository is currently foundation/contract oriented rather than a media implementation repository.
- Generic domain schemas and identity contracts provide useful integration primitives for MH-18 but do not constitute a media content model.
- Existing AI contracts are a candidate integration boundary for media analysis; they do not establish media AI authorization semantics by themselves.
- Current CI emphasizes contract/runtime governance and security boundaries rather than media processing.

### HISTORICAL

- Recent Git history is dominated by P0-06/P0-07/P0-08 governance and verification work, including exact-head verification and isolated runner changes.
- Historical PR descriptions explicitly state that P0-06/P0-04 work did not authorize persistence, external execution or production integration.

### PROPOSED

- MH-18 content model, identity model, lifecycle, ingestion pipeline, storage abstraction, derived-artifact model, playback/session model, processing isolation, rights boundary and media API are to be designed in subsequent passes.
- Technology choices such as FFmpeg/GStreamer/VLC, databases, search engines, object storage, NAS, CDN or DRM providers remain CANDIDATE until requirements/evidence/ADR.

### UNKNOWN / REQUIRES VERIFICATION

- Actual implementation outside the visible repository artifacts or in unlisted branches/worktrees.
- Full MH-01…MH-17 artifact set and exact traceability from those chats into repository files.
- Concrete State Authority implementation status beyond the inspected P0-06 documentation.
- Existing iOS-specific media implementation, if any exists outside this repository.
- Runtime dependency manifests beyond the currently inspected tree.
- Real device/provider capabilities and protocol behavior.
- Media performance/resource requirements.
- Legal/licensing/DRM requirements.
- Backup/restore behavior for media content.

### BLOCKED

- No evidence currently authorizes production media ingestion, bulk export/deletion, storage migration, codec installation, external provider integration, DRM integration, camera access or live capture.

### CONTRADICTIONS

No confirmed contradiction was established from the inspected repository artifacts.

Potential future contradiction to resolve: generic domain `lifecycle` is device-oriented and must not be reused as the media-content lifecycle without an explicit contract decision.

## 5. Immediate architecture conclusion

MH-18 must be built as a domain/content subsystem adjacent to, not inside, State Authority. The first implementation gate should define content identity and ingestion/validation contracts before any real media parser, codec, storage backend or network provider is integrated.

## 6. Next gate

Proceed to **MH-18.2 — Content Identity / Ingestion / Validation Contract** only after the repository audit evidence is recorded and unresolved implementation/dependency scope is explicitly tracked.

## 7. Acceptance state

`NOT ACCEPTED / NOT FROZEN`

This artifact does not authorize production media integration.
