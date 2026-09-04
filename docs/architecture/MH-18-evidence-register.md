# MH-18 — Evidence Register

**Status:** PROPOSED / AUDIT BASELINE
**Audit timestamp:** 2026-09-04

| ID | Source | Artifact | Observation | Classification | Confidence |
|---|---|---|---|---|---|
| E-18-001 | GitHub repository metadata | `VlDMlNSh/mediahub-os` | Private repository, default branch `main` | VERIFIED | High |
| E-18-002 | Git tree | `main` @ `6eb2ef9efc3ebe6cb89594a0d7180ed7a4c4cb18` | Current tree contains contracts, schemas, docs, tests, tools and CI workflows; no visible media implementation paths | VERIFIED | High |
| E-18-003 | `README.md` | repository root | README describes repository as foundation repository for MediaHub OS | VERIFIED | High |
| E-18-004 | `docs/architecture/P0-06-core-runtime-services-boundary.md` | P0-06 boundary | State Authority remains sole canonical mutation authority; P0-05 is consumer boundary | VERIFIED | High |
| E-18-005 | P0-06 boundary/contract | P0-06 docs | Durable persistence, network mutation, subprocess/shell, arbitrary filesystem mutation and autonomous AI mutation are explicitly excluded | VERIFIED | High |
| E-18-006 | `schemas/identity/identity-boundary.schema.json` | identity boundary | Canonical identity separation exists for device/binding/adapter/capability/event/command/execution/request/correlation/causation/recovery | VERIFIED | High |
| E-18-007 | `schemas/domain/lifecycle.schema.json` | domain lifecycle | Lifecycle enum is for MediaHub Device (`DISCOVERED`…`RETIRED`), not media assets | VERIFIED | High |
| E-18-008 | `schemas/ai/ai-inference-request.schema.json` | AI contract | AI request supports generate/classify/embed/transcribe/transform | VERIFIED | High |
| E-18-009 | GitHub code search | repository | No FFmpeg evidence found | OBSERVED | Medium |
| E-18-010 | GitHub code search | repository | No GStreamer/VLC evidence found | OBSERVED | Medium |
| E-18-011 | GitHub code search | repository | No media ingestion/playback/streaming/transcoding/subtitle/playlist/camera/live-media evidence found | OBSERVED | Medium |
| E-18-012 | Git history | recent commits | Recent work is concentrated on P0-06/P0-07/P0-08 governance, CI and isolated runner verification | HISTORICAL | High |

## Evidence discipline

Absence from the visible repository is evidence only about the inspected repository state; it is not proof that no implementation exists elsewhere. External devices/providers/codecs require separate observed test evidence and must not inherit behavior from category assumptions.
