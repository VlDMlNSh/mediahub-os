# MediaHub OS 11.x LTS — Mature OSS Component Baseline

Status: ACCEPTED TARGET / IMPLEMENTATION-GATED

## Rule
MediaHub does not embed complete third-party products as architectural authorities. Mature OSS is adopted only as an isolated implementation primitive, adapter target, protocol implementation, processing engine, or reference for proven lifecycle semantics.

## Core selected primitives
- Home Assistant Core — Smart Home domain authority only.
- PostgreSQL — durable transactional persistence; MediaHub owns schema and invariants.
- pgvector — vector capability inside PostgreSQL; never a second state authority.
- IfcOpenShell — IFC/BIM processing primitive.
- web-ifc — browser/mobile IFC interoperability primitive.
- PaddleOCR — OCR engine, isolated behind Document contract.
- OpenCV — vision/image processing primitive.
- ONNX Runtime — model inference runtime.
- llama.cpp — local LLM inference runtime.
- OpenTelemetry — telemetry instrumentation.
- Prometheus — metrics collection/query.
- Cosign — artifact signing/verification.
- Syft — SBOM generation.
- Trivy — vulnerability scanning.
- restic — backup mechanism; MediaHub owns policy and recovery authority.
- RAUC — OTA/update mechanism; MediaHub owns update authority and lifecycle.
- SOPS + age — encrypted configuration/secrets mechanics.
- Protobuf + gRPC — typed transport contracts/RPC; generated types are not the domain model.
- FFmpeg — isolated media processing primitive.

## Target-gated primitives
- OpenBao — secrets management, subject to trust-boundary qualification.
- S3-compatible object storage — target interface; implementation selected only after license/security/operational qualification.
- NATS JetStream — future distributed messaging candidate; never canonical state.
- etcd — future coordination candidate; never canonical state.

## Reference-only
Temporal, Mender, Kubernetes/K3s, Argo CD, Harbor, Jellyfin, Immich, Paperless-ngx, SeaweedFS, Qdrant, vLLM/SGLang, ComfyUI, OpenDroneMap, VTK/vtk.js, FreeCAD, CloudCompare, n8n.

## Explicit exclusions as foundational authorities
Redis, Kafka, Kubernetes-as-prerequisite, duplicate brokers, duplicate relational stores, duplicate state authorities, duplicate production AI runtimes without benchmark evidence.

## Acceptance gate
A component may become runtime dependency only after: capability gap → license review → provenance → security review → dependency/SBOM lock → adapter/contract boundary → benchmark → negative tests → degraded/recovery tests → rollback/update test → independent qualification.

## Current-runtime constraint
MH-03 remains the reference runnable foundation: single node, in-memory State Authority, deterministic offline-first operation, no implicit persistence/HA activation. Target components do not silently change that status.
