# MediaHub OS — OSS Integration Source Tree

This directory is the bounded integration layer for mature open-source components.

Rules:
- upstream projects are not copied wholesale;
- adapters isolate upstream APIs and lifecycle;
- MediaHub contracts remain canonical;
- components marked TARGET_GATED/FUTURE_GATED are not enabled by default;
- no adapter may mutate State Authority except through governed command paths;
- dependency versions and provenance are locked before qualification.

## Layout

- `manifests/` — pinned component manifests and license/provenance metadata.
- `adapters/` — MediaHub-owned integration boundaries.
- `runtime/` — isolated process/runtime wrappers.
- `tools/` — verification, SBOM and qualification helpers.

## Initial mature OSS set

Home Assistant Core, PostgreSQL, pgvector, IfcOpenShell, web-ifc, PaddleOCR, OpenCV, ONNX Runtime, llama.cpp, OpenTelemetry, Prometheus, Cosign, Syft, Trivy, restic, RAUC, SOPS, age, Protobuf, gRPC and FFmpeg.

The source tree is deliberately scaffolding-first: adding an upstream dependency requires a manifest, boundary contract and qualification evidence.
