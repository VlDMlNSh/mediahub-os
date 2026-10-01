# MediaHub OS — Canonical Component Manifest 2.0

Date: 2026-10-01
Repository: VlDMlNSh/mediahub-os
Status: CANONICAL DEVELOPMENT INPUT
Scope: component selection reconciliation after MH-25; architecture MH-1…MH-24 remains authoritative.

## 1. Operating rule

This manifest is the single component-selection input for autonomous development.

Selection is not production qualification. No TARGET-GATED or FUTURE-GATED component may enter a production runtime without the qualification gate in §8.

MediaHub retains authority over:
- domain models and public contracts;
- State Authority;
- identity, authorization and policy;
- Smart Home operational authority;
- privacy/user-data boundary;
- recovery authority;
- update/release authority;
- production admission;
- provenance and audit.

Third-party internal state never becomes MediaHub canonical state.

## 2. Canonical foundation

| Component | Mode | Boundary |
|---|---|---|
| PostgreSQL | EMBED_BLOCK / TARGET-GATED | canonical relational persistence under MediaHub schema/invariants |
| pgvector | EMBED_BLOCK / TARGET-GATED | vector retrieval inside PostgreSQL |
| Protobuf | EMBED_BLOCK / SELECTED | typed versioned contracts |
| gRPC | EMBED_BLOCK / SELECTED | typed RPC transport |
| OpenTelemetry Collector | EMBED_BLOCK / SELECTED | telemetry pipeline only |
| Prometheus | EMBED_BLOCK / SELECTED | metrics only; never correctness authority |
| SOPS + age | EMBED_BLOCK / SELECTED | encrypted configuration/secrets mechanics |
| Cosign | EMBED_BLOCK / SELECTED | artifact signing/verification |
| Syft | EMBED_BLOCK / SELECTED | SBOM generation |
| Trivy | EMBED_BLOCK / SELECTED | vulnerability/secrets/filesystem scanning |
| S3-compatible object storage | INTERFACE / SELECTED | object contract; implementation replaceable |
| FFmpeg | EMBED_BLOCK / SELECTED | media codec/container/transcode primitive |
| OpenCV | EMBED_BLOCK / SELECTED | vision primitive |

## 3. Whole-product sidecars

Use only behind MediaHub-owned adapters/contracts.

- Jellyfin — media library/server/playback.
- Music Assistant — music provider/player orchestration.
- Snapcast — synchronized multiroom audio.
- Frigate — camera/NVR/recording/object detection.
- Immich — photo/video ingestion/organization/search/mobile backup.

Conditional whole-product candidates:
- Paperless-ngx — sensitive-document boundary qualification required.
- SeaweedFS — storage qualification required.
- go2rtc — camera-specific stream adapter qualification required.

## 4. Target-gated implementation candidates

### Media
- MediaMTX — generic live-media transport/router.
- go2rtc — specialized camera/live-stream adapter.
- mpv — playback engine candidate.
- libVLC — alternative playback engine; do not deploy both by default.

### Storage / recovery / update
- SeaweedFS — distributed object/file/S3 implementation.
- restic — backup/restore mechanics.
- RAUC — atomic update mechanics.

### Documents / knowledge
- PaddleOCR — OCR.
- Unstructured — bounded document ingestion/partitioning.
- RDFLib — RDF interoperability.

### Digital Twin / engineering
- IfcOpenShell — primary IFC/BIM engine.
- web-ifc — client-side IFC engine.
- VTK/vtk.js — 2D/3D/scientific visualization.

### AI
- ONNX Runtime — general inference.
- llama.cpp — local LLM inference.

### Network / edge / supply chain
- Caddy — edge/reverse-proxy mechanics.
- Harbor — self-hosted OCI registry if required.

## 5. Reference / future-gated

- Syncthing — non-authoritative file synchronization only.
- Btrfs/OpenZFS — platform storage mechanisms.
- WireGuard — network primitive; does not replace CPRG.
- FreeCAD — engineering/CAD reference.
- CloudCompare — point-cloud reference.
- vLLM/SGLang — high-throughput inference only after benchmark gap.
- ComfyUI — generation workflow reference.
- OpenSearch — search only after measured PostgreSQL capability gap.
- Apache Jena — semantic-web reference/future.
- Temporal — durable workflows only after demonstrated gap.
- NATS JetStream — async transport only after demonstrated gap.
- etcd — coordination only after demonstrated gap.
- Kubernetes/K3s — orchestration reference, never prerequisite.
- Argo CD — deployment reference, no second update authority.
- Mender — update reference, no second OTA authority.

## 6. Explicit exclusions

- MinIO — excluded from new selection because the referenced GitHub repository is archived/read-only.
- Redis — no default cache/event/state authority.
- Kafka — no default event platform.
- second relational database — prohibited without explicit capability gap and requalification.
- second vector database — prohibited without benchmark evidence.
- second message broker — prohibited without capability gap.
- second OTA authority — prohibited.
- second recovery authority — prohibited.
- mandatory Kubernetes — prohibited.
- duplicate production AI runtimes for the same workload — prohibited without benchmark evidence.
- any sidecar whose internal model becomes a public MediaHub contract — prohibited.

## 7. Domain map

Developer Fabric → corporate development domain; heterogeneous Linux/macOS; at least one macOS node; dynamic Primary Development Node; capability/lease scheduling; HIGH_SPEED where qualified; no raw user data.

Media → MediaHub Media Contract → adapters/sidecars → MediaMTX/go2rtc/FFmpeg/Jellyfin/Music Assistant/Snapcast/Frigate/Immich as qualified.

Documents/Knowledge → PostgreSQL + pgvector + MediaHub contracts; OCR/ingestion/semantic interoperability are derived capabilities.

Digital Twin/Engineering → MediaHub project/provenance authority + object storage + IfcOpenShell/web-ifc/VTK where qualified.

AI → Model Registry → Qualification → Policy Admission → Runtime → Tool/Domain Contract → Result → Provenance/Audit. AI never gains domain authority.

Storage/Recovery → MediaHub recovery authority + object contract + restic/SeaweedFS/filesystem mechanisms where qualified.

Update → MediaHub update/release authority + RAUC mechanics where qualified.

## 8. Mandatory qualification gate

Every new runtime dependency must pass:

1. capability gap;
2. exact source/repository;
3. license/redistribution;
4. provenance/release;
5. version/tag or immutable commit pin;
6. SBOM;
7. signature/provenance verification;
8. security review;
9. MediaHub adapter/contract boundary;
10. functional tests;
11. negative/failure tests;
12. degraded-mode tests;
13. recovery/restore tests where applicable;
14. upgrade/rollback;
15. performance/resource benchmark;
16. independent qualification;
17. removal/replacement procedure.

Failure of a gate blocks production admission.

## 9. Autonomous selection rule

Astra may select an existing component only when:
- the capability gap is evidenced;
- the component exists in this manifest or passes the same admission process;
- no authority boundary is transferred;
- immutable provenance/version is recorded;
- qualification evidence is attached;
- the component can be removed/replaced without breaking canonical contracts.

Astra must prefer reuse over reimplementation, but must not add a dependency merely because it is popular or mature.

## 10. Development order

1. Developer Fabric + iOS Developer Mobile foundation.
2. Canonical contracts, build/test/release scaffolding and artifact provenance.
3. State/persistence/security/privacy/observability foundations.
4. MediaHub adapters and core media primitives.
5. Documents/knowledge/digital-twin/AI capabilities.
6. Target-gated sidecars and infrastructure implementations.
7. Qualification, recovery, upgrade/rollback and production admission.
8. Continuous autonomous queue until the defined product backlog is exhausted.

## 11. Closure

Component selection reconciliation 2.0–2.3 is superseded by this manifest.

Status: selection CLOSED.
Implementation: OPEN.
Production admission: QUALIFICATION-GATED.
Architecture: unchanged.
