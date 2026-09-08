# MediaHub OS 11.x LTS / MediaHub iOS
# COMPONENT ECOSYSTEM & REUSE MATRIX v2.0

Date: 2026-09-08
Status: ENGINEERING EXECUTION BASELINE / NOT RELEASE AUTHORIZATION
Immutable R4: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`

## 1. Executive decision

The previous component list is narrowed to the smallest set that materially improves MediaHub.

MediaHub owns the canonical model and all authoritative mutations. External projects are adapters,
engines, runtimes, observability or recovery mechanisms. No external project may become the system
of record for MediaHub state, engineering truth, authorization or provenance.

## 2. Selected runtime set

| Priority | Component | MediaHub role | Decision |
|---|---|---|---|
| P0 | PostgreSQL + pgvector | canonical transactional persistence + initial retrieval | INSTALL/INTEGRATE |
| P0 | S3-compatible object storage | documents/media/artefacts | INSTALL/INTEGRATE |
| P0 | IfcOpenShell | IFC engineering foundation | INTEGRATE |
| P0 | PaddleOCR | document/OCR intelligence | INTEGRATE |
| P0 | OpenCV + ONNX Runtime | deterministic vision/inference primitives | INTEGRATE |
| P0 | llama.cpp | local LLM/VLM runtime | INTEGRATE |
| P0 | Temporal | durable retries/recovery workflows | INTEGRATE after contract tests |
| P0 | OpenTelemetry Collector | telemetry transport | INTEGRATE |
| P0 | Prometheus | metrics/health evidence | INTEGRATE |
| P0 | restic | encrypted backup/restore substrate | INTEGRATE |
| P0 | RAUC | appliance A/B update + rollback | INTEGRATE on appliance track |
| P0 | Cosign/Sigstore | artifact signing/verification | INTEGRATE |
| P0 | Syft | SBOM | INTEGRATE |
| P0 | Trivy | vulnerability/misconfiguration/secrets scan | INTEGRATE |
| P0 | OpenBao | secret lifecycle where central secrets are required | INTEGRATE only when deployment needs it |
| P1 | web-ifc | browser IFC read/write | INTEGRATE when web BIM surface lands |
| P1 | three.js + vtk.js | digital-twin visualization | INTEGRATE in UI vertical |
| P1 | OpenDroneMap | scan/photogrammetry ingestion | OPTIONAL adapter |
| P1 | vLLM OR SGLang | high-throughput GPU inference | BENCHMARK, then select one |
| P0/P1 | Local MediaHub Cluster | primary multi-node building runtime; scheduling, HA/failover, distributed media/AI/storage | REQUIRED architectural track; implementation gated by cluster contract/evidence |
| P0/P1 | Cloud Development Cluster | privileged external compute/development plane; burst GPU/CI/research | REQUIRED separate plane; never canonical authority |
| P1/P2 | K3s + Argo CD | candidate orchestration/GitOps substrate for local/edge and cloud cluster profiles | evaluate per deployment profile; not deferred as an architecture capability |
| P1 | OCI registry | signed/container artifact distribution for cluster plane | REQUIRED before multi-node production rollout |
| P2 | Harbor | full registry governance/UI/scanning integration | add only if registry scale/tenancy requires it |

## 3. Rejected or reference-only dependencies

- Jellyfin: reference/integration candidate; never canonical media authority.
- Immich: reference/integration candidate; never canonical personal-media authority.
- Mender: reference alternative; do not deploy with RAUC as a second OTA authority.
- Massing: competitor/reference, not a MediaHub dependency.
- FreeCAD: engineering reference, not canonical BIM authority.
- CloudCompare: external tool boundary because of licensing/packaging constraints.
- ComfyUI/InvokeAI: optional creative workflow, not engineering geometry authority.
- Qdrant/OpenSearch: no second retrieval/search store until benchmark proves PostgreSQL+pgvector insufficient.
- MinIO: do not select as the new baseline solely on name recognition; its GitHub repository is archived.

## 4. Integration gates

Every dependency must pass: exact pin -> license review -> SBOM -> security scan -> API contract ->
data model mapping -> isolation boundary -> provenance mapping -> failure/degraded mode -> rollback ->
integration test. Installation alone never counts as integration.

## 5. Self-regulation principle

The self-regulating loop is MediaHub-owned:

observe -> classify -> decide -> authorize -> act -> verify -> record evidence -> recover/retry -> learn

AI may recommend; deterministic policy and State Authority decide. Recovery may retry/restart/restore,
but must not silently alter authoritative state.

## 6. Target outcome

The selected stack closes six high-value gaps: durable execution, document/engineering intelligence,
local AI, observable operation, cryptographic supply-chain control, and backup/update recovery.
The system remains modular and can boot without P1/P2 components.
