# MH-18 — Architecture Chat Synchronization Record

Date: 2026-09-04
Branch: `mh-18-media-content-architecture`
Repository: `VlDMlNSh/mediahub-os`
Status: PROPOSED / NOT ACCEPTED / NOT FROZEN

## Purpose

Durable synchronization record for the MH-18 architecture chat. The repository is the long-term source of record for the architecture baseline; the ChatGPT conversation is not required to reconstruct the current state.

## Reference artifacts

- `MH-18-media-content-architecture.md`
- `MH-18-content-model.md`
- `MH-18-content-identity.md`
- `MH-18-content-lifecycle.md`
- `MH-18-ingestion.md`
- `MH-18-ingestion-pipeline.md`
- `MH-18-integrity.md`
- `MH-18-validation.md`
- `MH-18-metadata.md`
- `MH-18-metadata-provenance.md`
- `MH-18-ai-analysis.md`
- `MH-18-privacy.md`
- `MH-18-storage.md`
- `MH-18-indexing.md`
- `MH-18-search.md`
- `MH-18-transcoding.md`
- `MH-18-playback.md`
- `MH-18-streaming.md`
- `MH-18-playlists.md`
- `MH-18-subtitles.md`
- `MH-18-rights.md`
- `MH-18-drm-boundary.md`
- `MH-18-content-security.md`
- `MH-18-sandboxing.md`
- `MH-18-backup-recovery.md`
- `MH-18-migration.md`
- `MH-18-observability.md`
- `MH-18-resource-governance.md`
- `MH-18-api.md`
- `MH-18-export.md`
- `MH-18-plugin-interaction.md`
- `MH-18-supply-chain.md`
- `MH-18-testing-model.md`
- `MH-18-security-testing.md`
- `MH-18-privacy-testing.md`
- `MH-18-performance-testing.md`
- `MH-18-compatibility-testing.md`
- `MH-18-technology-evaluation.md`
- `MH-18-evidence-register.md`
- `MH-18-decision-log.md`
- `MH-18-contradiction-register.md`
- `MH-18-unknowns.md`
- `MH-18-acceptance-criteria.md`

## Canonical architectural position

Media/content is a domain, not the canonical state authority. Content, asset, object/file, storage locator, external identity, digest/fingerprint and version are distinct concepts. Ingestion, validation, metadata extraction, indexing, AI analysis, transcoding, playback, storage and plugins cannot bypass the authorization path or become State Authority.

Derived artifacts remain derived and rebuildable. Search/index/cache/thumbnails/previews/transcodes are not canonical truth. AI output is candidate metadata until validated and authorized.

External media, providers, codecs/parsers and imported metadata are untrusted by default. Processing is bounded, isolated, observable and privacy-aware.

## Repository audit outcome

The MH-18 pass established architecture contracts and governance gates. The audit did not establish a production media implementation. Therefore no production ingestion, bulk import/export/deletion, storage migration, codec installation, provider/DRM integration or camera/live capture is authorized by MH-18.

Technology choices such as FFmpeg/GStreamer/VLC, storage/search engines and DRM providers remain candidates pending requirements, compatibility, security/resource/licensing analysis, evidence and ADR.

## Developer handoff rule

Implementation belongs in a separate development chat. The development chat consumes a Master Prompt generated from this baseline. On completion or when architectural deviations are found, it returns a Reverse Master Prompt containing implementation changes, tests, evidence, deviations, contradictions, unknowns and proposed architectural changes.

No development chat output becomes architectural truth automatically. Architecture changes are reviewed in the appropriate MH architecture chat and synchronized back to GitHub.

## Next architectural handoff

The next domain chat is MH-19 — Knowledge Graph / Digital Twin Architecture. Its baseline constraints include: Knowledge ≠ State Authority; Digital Twin ≠ Physical Device; Inference ≠ Fact; AI-generated relationship ≠ Verified. Any canonical mutation must follow Policy → Authorization → Consumer Boundary → State Authority.
