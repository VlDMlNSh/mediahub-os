# PASS 1 — Initial Capability Extraction

Status: IN PROGRESS / PARTIAL / NOT MASTER BASELINE

Source evidence is deliberately classified conservatively. Presence in MH-18 does not imply acceptance because MH-18 is explicitly PROPOSED / NOT ACCEPTED / NOT FROZEN.

## Initial capability candidates

| ID | Capability | Evidence | Preliminary status |
|---|---|---|---|
| MH-CAP-0001 | Media/content ingestion pipeline | MH-18 media architecture: discovery, intake, identity, integrity, extraction, normalization, classification, policy, registration, indexing | PROPOSED |
| MH-CAP-0002 | Media validation and quarantine | MH-18: syntax/container/codec/metadata/security/policy/rights validation; reject/quarantine/verification | PROPOSED |
| MH-CAP-0003 | Logical content / asset / object identity model | MH-18 content model and identity semantics | PROPOSED |
| MH-CAP-0004 | Media lifecycle management | MH-18 lifecycle states and owner/authorization/recovery semantics | PROPOSED |
| MH-CAP-0005 | Metadata provenance and conflict handling | MH-18 metadata/provenance model | PROPOSED |
| MH-CAP-0006 | Canonical media storage separation | MH-18 separation of canonical metadata/state, content bytes, derivatives and cache | PROPOSED |
| MH-CAP-0007 | Rebuildable media index | MH-18 Catalog → Index Builder → Search Index | PROPOSED |
| MH-CAP-0008 | Media search | MH-18 search model; search result non-canonical | PROPOSED |
| MH-CAP-0009 | Duplicate detection | MH-18 AI analysis and explicit duplicate-detection artifact on MH-18 branch | PROPOSED |
| MH-CAP-0010 | Thumbnail/preview/waveform derivatives | MH-18 derived systems and dedicated thumbnail artifact | PROPOSED |
| MH-CAP-0011 | Media transcoding | MH-18 bounded, cancellable, observable transcoding | PROPOSED |
| MH-CAP-0012 | Media playback sessions | MH-18 authorized read model → media session → resolver → decoder/player | PROPOSED |
| MH-CAP-0013 | LAN/remote media streaming | MH-18 playback/streaming boundary with auth, quotas and observability | PROPOSED |
| MH-CAP-0014 | Live media / camera capture | MH-18 live-media/device section; explicit camera/microphone/live stream boundary | PROPOSED |
| MH-CAP-0015 | Camera recording into normal media ingestion | MH-18: recording enters normal ingestion | PROPOSED |
| MH-CAP-0016 | RTSP/ONVIF/WebRTC interoperability candidates | MH-18 explicitly names these as candidates; MH-17 protocol selection remains CANDIDATE / NOT SELECTED | PROPOSED / UNSELECTED |
| MH-CAP-0017 | Playlists / queues / collections / smart collections | MH-18 playlist semantics | PROPOSED |
| MH-CAP-0018 | Multiple audio/subtitle tracks | MH-18 subtitles/audio track support | PROPOSED |
| MH-CAP-0019 | External subtitle/artwork untrusted-input handling | MH-18 security model | PROPOSED |
| MH-CAP-0020 | Rights/DRM boundary | MH-18 rights/DRM section | PROPOSED |
| MH-CAP-0021 | Media backup/recovery | MH-18 backup/recovery section | PROPOSED |
| MH-CAP-0022 | Media migration distinct from transcoding | MH-18 migration section | PROPOSED |
| MH-CAP-0023 | Media export | MH-18 export/API section | PROPOSED |
| MH-CAP-0024 | Offline-first media operation | MH-18 offline-first and playback degradation | PROPOSED |
| MH-CAP-0025 | Media privacy and access controls | MH-18 privacy/security boundary; MH-13 dependency | PROPOSED |
| MH-CAP-0026 | Media resource governance | MH-18 bounds for files, storage, streams, processing, CPU/GPU, memory, bandwidth | PROPOSED |
| MH-CAP-0027 | Media processing isolation/sandboxing | MH-18 hostile media and restricted execution boundary | PROPOSED |
| MH-CAP-0028 | Media AI classification/tagging | MH-18 AI: classify, OCR, transcribe, tag | PROPOSED |
| MH-CAP-0029 | Media AI scene/object detection and summarization | MH-18 AI section | PROPOSED |
| MH-CAP-0030 | Media embeddings / probable duplicate identification | MH-18 AI section | PROPOSED |
| MH-CAP-0031 | Automation rules/triggers/actions | MH-20 automation architecture | PROPOSED |
| MH-CAP-0032 | Scheduling/idempotency/retry/rate limiting/debounce/hysteresis | MH-20 automation architecture | PROPOSED |
| MH-CAP-0033 | Manual override and critical-action safety gates | MH-20 safety model | PROPOSED |
| MH-CAP-0034 | Energy measurement/observation/optimization | MH-20 energy domain | PROPOSED |
| MH-CAP-0035 | Controlled self-healing/remediation | MH-20 self-healing domain | PROPOSED |
| MH-CAP-0036 | Offline-first critical control | MH-20 topology/offline rule | PROPOSED |
| MH-CAP-0037 | Device discovery/enrollment/trust/quarantine | MH-17 completion record | ARCHITECTURE-CONTROLLED / ACCEPTANCE NOT CONFIRMED |
| MH-CAP-0038 | Device capability/group model | MH-17 completion record | ARCHITECTURE-CONTROLLED / ACCEPTANCE NOT CONFIRMED |
| MH-CAP-0039 | Device command lifecycle/idempotency/failure semantics | MH-17 completion record | ARCHITECTURE-CONTROLLED / ACCEPTANCE NOT CONFIRMED |
| MH-CAP-0040 | Device telemetry/event normalization | MH-17 completion record | ARCHITECTURE-CONTROLLED / ACCEPTANCE NOT CONFIRMED |

## Important unconfirmed historical claims

The following are NOT yet promoted to accepted capabilities because current accessible evidence is insufficient:

- boxed/native support for specific surveillance vendors such as Dahua and Hikvision;
- concrete ONVIF profile coverage;
- concrete camera models/codecs/firmware qualification;
- guaranteed continuous recording to a particular HDD filesystem/layout;
- NVR-like retention policies beyond the architectural storage/retention boundaries;
- specific commercial/cloud media provider integrations;
- production FFmpeg/GStreamer/VLC selection;
- any production media implementation.

These remain UNRESOLVED / PROPOSED / REQUIRES ACCEPTANCE until stronger historical or implementation evidence is found.

## Critical evidence rule

A filename, branch, PR, or architecture artifact establishes existence of an artifact, not acceptance of every capability implied by it. Capability acceptance requires explicit governance/decision evidence or equivalent strong historical evidence, and implementation confirmation is tracked separately.

## Next extraction targets

1. Recover complete MH-01…MH-23 source bodies from available conversation history / archives.
2. Enumerate every GitHub architecture artifact across historical branches, not just main.
3. Extract capability candidates from MH-01…MH-17 and MH-19…MH-23.
4. Extract development-history capabilities from PRs, commits, tests and abandoned branches.
5. Reconcile the above into the canonical registry with evidence pointers and status transitions.
