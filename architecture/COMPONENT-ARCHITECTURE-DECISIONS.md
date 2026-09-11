# MediaHub OS — Component Architecture Decisions

Date: 2026-09-11
Status: ACCEPTED BASELINE
Registry: `components/COMPONENT-REGISTRY.yaml`

## Governing decision

MediaHub does not adopt complete third-party products by default. Third-party projects are evaluated as sources of stable implementation blocks, protocols, schemas, algorithms, lifecycle semantics and interoperability patterns.

MediaHub retains ownership of domain model, State Authority, event semantics, authorization policy, device model, update authority, recovery authority, release gates and production authorization.

## Status model

- CURRENT_FOUNDATION — compatible with the frozen runnable foundation.
- TARGET_GATED — required by Functional Baseline 1.0 but activation requires explicit governance/qualification.
- FUTURE_GATED — not activated until a demonstrated capability gap and acceptance gate.
- REFERENCE — engineering source only; not an implicit runtime dependency.
- EXCLUDED — not foundational.

## CURRENT_FOUNDATION / selected primitives

- Protobuf + gRPC — typed contracts/RPC; generated types never become the domain model.
- OpenTelemetry + Prometheus — non-authoritative observability.
- SOPS + age — encrypted configuration/secrets mechanics.
- Syft + Cosign + Trivy — SBOM, signing and vulnerability evidence.
- FFmpeg — isolated media-processing primitive.

## TARGET_GATED

- PostgreSQL — transactional persistence; MediaHub owns schema/invariants.
- pgvector — vector capability within PostgreSQL; no second state authority.
- Home Assistant Core — Smart Home domain authority only; MediaHub Smart Home Layer remains the platform boundary.
- IfcOpenShell + web-ifc — IFC/BIM interoperability primitives.
- PaddleOCR — OCR engine behind the Document contract.
- OpenCV — vision/image processing primitive.
- ONNX Runtime + llama.cpp — inference runtimes behind the MediaHub AI Gateway.
- restic — backup mechanics; MediaHub owns backup policy and recovery authority.
- RAUC — OTA mechanics; MediaHub owns update policy, authorization and lifecycle.

## FUTURE_GATED

- NATS/JetStream — distributed asynchronous transport/durable streams only after measured need.
- etcd — coordination/membership/leases only after measured need.
- OpenBao — secrets service only after trust-boundary qualification.
- S3-compatible object storage — interface target, implementation selected after license/security/operational review.

## REFERENCE

Temporal, Caddy, Jellyfin, SeaweedFS, Paperless-ngx, Immich, Mender, Kubernetes/K3s, Argo CD, Harbor, Qdrant, vLLM/SGLang, ComfyUI, OpenDroneMap, VTK/vtk.js, FreeCAD, CloudCompare, n8n.

## EXCLUDED as foundational authorities

Redis, Kafka, Kubernetes-as-runtime-prerequisite, duplicate brokers, duplicate relational databases, duplicate metrics stacks, duplicate production AI runtimes without benchmark evidence.

## Acceptance gate

Every TARGET_GATED/FUTURE_GATED dependency requires: capability gap → license review → provenance → security review → dependency/SBOM lock → explicit contract/adapter boundary → benchmark where applicable → negative tests → degraded/recovery tests → rollback/update test → independent qualification.

## Current-runtime constraint

MH-03 remains the reference runnable foundation: single node, in-memory State Authority, deterministic offline-first operation, with persistence/HA integrations future-governed. No component classification in this document silently activates a target dependency.
