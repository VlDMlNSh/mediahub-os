# MediaHub OS — GitHub Component Reconciliation 2.0

Date: 2026-10-01
Repository: VlDMlNSh/mediahub-os
Repository HEAD at analysis: 73c5f6f76d8b157d0a2a5ed8d4da21c760b1bc25
Status: QUALIFIED COMPONENT BASELINE / DEVELOPMENT INPUT
Purpose: final candidate inventory for implementation selection; architecture remains MediaHub-owned.

## 1. Governing rule

Do not reimplement a mature capability that is already available as a stable GitHub project when it can be integrated without transferring MediaHub authority.

Selection modes:
- EMBED_BLOCK — use a mature library/runtime as an implementation primitive.
- SIDECAR_WHOLE — deploy the complete product when the product capability is materially better than rebuilding it; integrate through a MediaHub adapter/API boundary.
- REFERENCE — use architecture, algorithms, schemas, lifecycle semantics and implementation patterns only.
- TARGET_GATED — candidate for implementation after explicit qualification gates.
- EXCLUDED — not admitted to the MediaHub foundation.

MediaHub retains:
- domain model;
- State Authority;
- authorization and policy;
- recovery authority;
- update authority;
- release/production authority;
- public contracts;
- user-data boundary.

A third-party component is never authoritative merely because it stores state internally.

## 2. Final implementation set

### A. Core platform / contracts

1. PostgreSQL — EMBED_BLOCK / TARGET_GATED
   Source: https://github.com/postgres/postgres
   Use: durable relational persistence.
   Boundary: MediaHub owns schema, invariants, migrations, retention and transaction semantics.
   Gate: backup/restore, migration rollback, concurrency, failure recovery.

2. pgvector — EMBED_BLOCK / TARGET_GATED
   Source: https://github.com/pgvector/pgvector
   Use: vector retrieval inside PostgreSQL.
   Rule: no second vector/state authority.

3. Protobuf — EMBED_BLOCK / SELECTED
   Source: https://github.com/protocolbuffers/protobuf
   Use: versioned typed contracts.
   Rule: generated code is not the domain model.

4. gRPC — EMBED_BLOCK / SELECTED
   Source: https://github.com/grpc/grpc
   Use: typed service RPC.
   Gate: authn/authz, timeout/cancellation, compatibility and failure semantics.

5. OpenTelemetry Collector — EMBED_BLOCK / SELECTED
   Source: https://github.com/open-telemetry/opentelemetry-collector
   Use: telemetry pipeline.
   Rule: non-authoritative and non-mutating.

6. Prometheus — EMBED_BLOCK / SELECTED
   Source: https://github.com/prometheus/prometheus
   Use: metrics.
   Rule: metrics never become correctness prerequisites.

7. SOPS + age — EMBED_BLOCK / SELECTED
   Sources: https://github.com/getsops/sops ; https://github.com/FiloSottile/age
   Use: encrypted configuration/secrets mechanics.
   Rule: do not introduce a duplicate production secret authority.

8. Cosign — EMBED_BLOCK / SELECTED
   Source: https://github.com/sigstore/cosign
   Use: artifact signing and verification.

9. Syft — EMBED_BLOCK / SELECTED
   Source: https://github.com/anchore/syft
   Use: SBOM generation.

10. Trivy — EMBED_BLOCK / SELECTED
    Source: https://github.com/aquasecurity/trivy
    Use: vulnerability/secrets/filesystem scanning.

11. restic — EMBED_BLOCK / TARGET_GATED
    Source: https://github.com/restic/restic
    Use: backup/restore mechanics.
    Rule: MediaHub remains recovery authority; backup success alone is not recovery evidence.

12. RAUC — EMBED_BLOCK / TARGET_GATED
    Source: https://github.com/rauc/rauc
    Use: atomic OTA/update mechanics.
    Rule: MediaHub remains update authority.

## 3. Media subsystem — direct adoption

13. FFmpeg — EMBED_BLOCK / SELECTED MEDIA PRIMITIVE
    Source: https://github.com/FFmpeg/FFmpeg
    Use: codec/container/transcode/demux/mux/media-processing engine.
    Boundary: isolated worker, explicit codec/build matrix, resource/time limits and sandboxing.
    Decision: mandatory media primitive.

14. go2rtc — SIDECAR_WHOLE or EMBED_BLOCK / TARGET-GATED
    Source: https://github.com/AlexxIT/go2rtc
    Use: RTSP/WebRTC/stream negotiation, restreaming, low-latency camera/media transport.
    Evidence: current GitHub release v1.9.14 (2026-01-19) is published with Linux/macOS binaries.
    Decision: strong candidate for camera/live-stream transport; do not duplicate its protocol handling in MediaHub.
    Gate: security, API boundary, resource isolation and current-version requalification.

15. Jellyfin Server — SIDECAR_WHOLE / MEDIA CANDIDATE
    Source: https://github.com/jellyfin/jellyfin
    Use: mature media-library/server/playback backend, metadata and client-facing media services.
    Evidence: GitHub shows Jellyfin 12.0 as latest release and packaging for 12.1 in September 2026.
    Integration: MediaHub remains unified authority/UI; Jellyfin may operate as an isolated media engine/service.
    Gate: API contract, metadata ownership, identity mapping, storage boundary, upgrade/rollback and license review.
    Decision: promote from historical REFERENCE to explicit WHOLE-PRODUCT CANDIDATE because the media domain benefits from existing implementation breadth.

16. Music Assistant Server — SIDECAR_WHOLE / MEDIA CANDIDATE
    Source: https://github.com/music-assistant/server
    Use: music library/provider/player orchestration and multi-speaker control.
    Evidence: GitHub shows stable 2.10.4 and ongoing 2.11.x beta/nightly releases.
    Integration: sidecar behind MediaHub media/audio contract; do not expose its internal model as MediaHub domain model.
    Decision: whole-product candidate for music subsystem; stable channel only for production qualification.

17. Snapcast — SIDECAR_WHOLE / MEDIA CANDIDATE
    Source: https://github.com/snapcast/snapcast
    Use: synchronized multiroom audio transport/player.
    Integration: audio distribution layer only; MediaHub owns zones, identity, policy and desired state.
    Gate: platform support, latency, recovery, clock synchronization and licensing.
    Decision: retain as whole-product candidate where synchronized multiroom audio is required.

18. mpv — EMBED_BLOCK / REFERENCE-TO-IMPLEMENTATION
    Source: https://github.com/mpv-player/mpv
    Use: high-quality playback engine and reference for playback lifecycle/hardware decoding.
    Decision: candidate playback engine for MediaHub-owned clients/nodes, not a server authority.
    Gate: license/build configuration, embedding API, hardware acceleration matrix.

19. libVLC — EMBED_BLOCK / REFERENCE-TO-IMPLEMENTATION
    Source: https://github.com/VideoLanVLC/vlc
    Use: embeddable playback/streaming/conversion engine.
    Decision: alternative to mpv; do not deploy both by default.
    Gate: benchmark against actual MediaHub playback targets and platform constraints.

## 4. Camera / NVR / visual media

20. Frigate — SIDECAR_WHOLE / MEDIA CANDIDATE
    Source: https://github.com/blakeblackshear/frigate
    Use: local NVR, camera recording, object detection, RTSP restreaming and WebRTC/MSE live view.
    Evidence: GitHub release 0.18.0 exists; project is MIT licensed.
    Integration: Frigate may own its internal recording/indexing implementation, but MediaHub owns platform policy, device identity and public integration.
    Decision: strong candidate for camera/NVR capability; avoid rebuilding NVR internals.
    Gate: retention, storage, accelerator support, privacy/egress, HA boundary and recovery.

21. OpenCV — EMBED_BLOCK / SELECTED
    Source: https://github.com/opencv/opencv
    Use: vision/image-processing primitive.
    Rule: behind MediaHub-owned contracts.

## 5. Photos / home video

22. Immich — SIDECAR_WHOLE / MEDIA CANDIDATE
    Source: https://github.com/immich-app/immich
    Use: photo/video ingestion, search, organization, sharing and mobile backup workflows.
    Evidence: GitHub shows active 3.x development; RC releases are explicitly marked pre-release.
    Production rule: use stable releases only; never deploy RC as production baseline.
    Integration: sidecar media service; MediaHub owns identity boundary, storage policy and unified navigation.
    Gate: API stability, storage/backup, metadata ownership, license/upgrade/recovery review.
    Decision: candidate for complete photo/video subsystem rather than reimplementing a large mature application.

## 6. Documents / knowledge

23. PaddleOCR — EMBED_BLOCK / TARGET-GATED
    Source: https://github.com/PaddlePaddle/PaddleOCR
    Use: OCR engine.
    Rule: OCR output is derived, provenance-bearing data.

24. Paperless-ngx — SIDECAR_WHOLE / REFERENCE-CANDIDATE
    Source: https://github.com/paperless-ngx/paperless-ngx
    Use: mature document ingestion/indexing/archive implementation.
    Evidence: active project with 3.2.1 release in September 2026.
    Critical boundary: project stores sensitive documents in clear text by default and explicitly warns about trusted-host operation.
    Decision: useful implementation/reference source; whole-product deployment requires a privacy/security boundary review and must not become MediaHub document authority.
    Prefer component extraction/pattern reuse before full sidecar deployment.

25. PostgreSQL + pgvector + MediaHub document contracts
    Decision: preferred foundational document persistence/search substrate before adding another database or vector authority.

## 7. Digital Twin / engineering

26. IfcOpenShell — EMBED_BLOCK / TARGET-GATED
    Source: https://github.com/IfcOpenShell/IfcOpenShell
    Use: IFC/BIM parsing, validation and geometry processing.

27. web-ifc — EMBED_BLOCK / TARGET-GATED
    Source: https://github.com/ThatOpen/engine_web-ifc
    Use: browser/mobile IFC interoperability.

28. FreeCAD — REFERENCE
    Source: https://github.com/FreeCAD/FreeCAD
    Use: engineering/CAD algorithms and interoperability patterns.
    Rule: do not make FreeCAD the MediaHub engineering domain authority without a measured capability gap.

29. CloudCompare — REFERENCE
    Source: https://github.com/CloudCompare/CloudCompare
    Use: point-cloud processing and 3D engineering workflows.
    Rule: integrate only where measured point-cloud capability is required.

30. VTK / vtk.js — REFERENCE / TARGET-CANDIDATE
    Source: https://github.com/Kitware/VTK
    Use: scientific/engineering visualization and 3D rendering patterns.
    Gate: benchmark against MediaHub UI/3D requirements before activation.

## 8. AI

31. ONNX Runtime — EMBED_BLOCK / TARGET-GATED
    Source: https://github.com/microsoft/onnxruntime
    Use: portable model inference.
    Rule: MediaHub controls model registry, provenance, policy and execution admission.

32. llama.cpp — EMBED_BLOCK / TARGET-GATED
    Source: https://github.com/ggml-org/llama.cpp
    Use: local LLM inference.
    Rule: no direct physical/authority path from model to devices.

33. vLLM / SGLang — REFERENCE / FUTURE-GATED
    Sources: https://github.com/vllm-project/vllm ; https://github.com/sgl-project/sglang
    Use: high-throughput server inference patterns.
    Decision: do not introduce as duplicate production inference runtimes until benchmark evidence shows a real gap versus ONNX Runtime/llama.cpp and actual model workloads.

34. ComfyUI — REFERENCE
    Source: https://github.com/comfyanonymous/ComfyUI
    Use: image-generation workflow patterns only.
    Decision: no foundational dependency; activate only for a concrete MediaHub media-generation workflow.

## 9. Storage

35. S3-compatible object storage — TARGET INTERFACE
    Rule: protocol is required; implementation is not predetermined.

36. SeaweedFS — TARGET-GATED IMPLEMENTATION CANDIDATE
    Source: https://github.com/seaweedfs/seaweedfs
    Use: distributed object/file storage and S3 gateway.
    Evidence: active project with S3, replication/erasure-coding and distributed storage architecture.
    Decision: stronger current candidate than the old MinIO reference.
    Gate: operational qualification, security, backup/restore, performance, licensing and authority boundary.

37. MinIO — EXCLUDED FROM NEW SELECTION
    Source: https://github.com/minio/minio
    Evidence: GitHub repository was archived by owner on 2026-04-25 and is read-only.
    Decision: remove as a preferred new implementation candidate; retain historical provenance only.
    Reason: maintenance/lifecycle status no longer meets the intended stable-block criterion.

38. Syncthing — REFERENCE / TARGET-CANDIDATE
    Source: https://github.com/syncthing/syncthing
    Use: peer-to-peer file synchronization semantics.
    Rule: not canonical state replication and not a replacement for MediaHub persistence/backup authority.
    Gate: only for explicitly defined file-sync capability.

39. Btrfs-progs / Btrfs — REFERENCE / PLATFORM OPTION
    Source: https://github.com/kdave/btrfs-progs
    Use: CoW filesystem, snapshots and recovery tooling on Linux.
    Rule: filesystem mechanism, not MediaHub state authority.
    Gate: hardware/storage topology and recovery qualification.

40. OpenZFS — REFERENCE / PLATFORM OPTION
    Source: https://github.com/openzfs/zfs
    Use: storage integrity, snapshots and dataset management where platform permits.
    Rule: infrastructure storage primitive, not domain state authority.

## 10. Networking / transport

41. WireGuard — REFERENCE / PLATFORM NETWORK PRIMITIVE
    Source: https://github.com/WireGuard/wireguard-go
    Use: secure transport where explicitly required by platform/network design.
    Rule: does not replace the defined CPRG role; CPRG remains a narrowly scoped API-key registration channel.

42. Caddy — REFERENCE / TARGET-CANDIDATE
    Source: https://github.com/caddyserver/caddy
    Use: reverse proxy/TLS/HTTP edge mechanics.
    Rule: only an edge implementation; it does not own identity or authorization policy.

## 11. Workflow / orchestration

43. Temporal — REFERENCE / FUTURE-GATED
    Source: https://github.com/temporalio/temporal
    Use: durable workflow semantics.
    Gate: introduce only if Astra/MediaHub workload demonstrates a material workflow persistence/retry gap.

44. NATS JetStream — FUTURE-GATED
    Source: https://github.com/nats-io/nats-server
    Use: asynchronous transport/durable streams.
    Rule: never canonical state.

45. etcd — FUTURE-GATED
    Source: https://github.com/etcd-io/etcd
    Use: leases/membership/coordination.
    Rule: never domain state authority.

## 12. Supply chain / artifact infrastructure

46. Harbor — TARGET-INTERFACE / REFERENCE
    Source: https://github.com/goharbor/harbor
    Use: OCI registry pattern and implementation candidate.
    Gate: only if a self-hosted OCI registry capability is required; integrate with Cosign/Syft/Trivy.

47. Kubernetes/K3s — REFERENCE ONLY
    Sources: https://github.com/kubernetes/kubernetes ; https://github.com/k3s-io/k3s
    Rule: never a prerequisite for MediaHub. Consider only when measured cluster-operational complexity is justified.

48. Argo CD — REFERENCE ONLY
    Source: https://github.com/argoproj/argo-cd
    Rule: not required while MediaHub owns update/release authority.

49. Mender — REFERENCE ONLY
    Source: https://github.com/mendersoftware/mender
    Rule: cannot create a second production OTA authority alongside RAUC.

## 13. Whole-product decisions

Approved as explicit candidates for whole deployment behind MediaHub boundaries:
- Jellyfin — general media library/server.
- Music Assistant — music provider/player orchestration.
- Snapcast — synchronized multiroom audio.
- Frigate — NVR/camera recording/object detection.
- Immich — photo/video management and ingestion.

Conditional:
- Paperless-ngx — only after privacy/storage/security boundary qualification.
- SeaweedFS — only after storage qualification.
- go2rtc — likely sidecar for live camera/stream transport after security qualification.

Not whole-product dependencies:
- Home Assistant Core is a domain authority for Smart Home, not a generic MediaHub platform.
- PostgreSQL/pgvector are persistence primitives.
- FFmpeg/OpenCV/ONNX Runtime/llama.cpp/etc. are implementation primitives.
- Reference products remain reference until a capability gap is proven.

## 14. Duplicate-authority prohibitions

Do not introduce:
- Redis as default cache/event/state layer;
- Kafka as default event platform;
- a second relational database;
- a second vector database without benchmark evidence;
- a second production message broker without capability gap;
- a second OTA authority;
- a second recovery authority;
- Kubernetes as a runtime prerequisite;
- multiple production AI runtimes for the same workload without benchmark evidence;
- whole products whose internal data model becomes a public MediaHub contract.

## 15. Mandatory qualification gate for every new runtime dependency

1. Capability gap.
2. Exact GitHub source/repository.
3. License and redistribution review.
4. Provenance and release verification.
5. Version/tag or immutable commit pin.
6. SBOM.
7. Signature/provenance verification where available.
8. Vulnerability/security review.
9. Adapter/contract boundary.
10. Functional tests.
11. Negative/failure tests.
12. Degraded-mode tests.
13. Recovery/restore tests where applicable.
14. Upgrade/rollback test.
15. Performance/resource benchmark.
16. Independent qualification.
17. Removal/replacement procedure.

## 16. Result

The prior OSS baseline is superseded as the component-selection input by this 2.0 reconciliation.

Net decisions:
- retain mature primitives already selected;
- add explicit whole-product media candidates where rebuilding would waste effort;
- add go2rtc as a camera/live-stream candidate;
- elevate SeaweedFS as a current object-storage implementation candidate;
- remove MinIO from new selection because its GitHub repository is archived;
- keep Paperless-ngx, FreeCAD, CloudCompare, VTK, Syncthing and similar systems bounded as conditional/reference components;
- preserve MediaHub ownership of all canonical state, policy, identity, recovery, update and production authority.

This document is a development-selection baseline, not an automatic activation manifest.
