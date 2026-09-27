# MediaHub OS 11.x LTS / MediaHub iOS
# Component Adoption & Architecture Alignment Report v1.0

Date: 2026-09-08
Status: ENGINEERING_BASELINE / NOT RELEASE AUTHORIZATION

## 1. Decision

The component report is accepted as an **engineering selection baseline**, with one important qualification: it does not replace the Master System Passport, Master Architecture, capability/contract/invariant registries, or governance gates. It adds implementation choices underneath those authoritative layers.

The report is aligned with the accepted passport and current architecture where each adopted technology is treated as an implementation dependency rather than a new product authority.

## 2. Non-negotiable architecture alignment

- MediaHub remains the single user-facing system model.
- Home Assistant remains internal for Smart Home integration/automation; it is not a user-facing UI.
- State Authority remains the sole canonical mutation authority.
- AI, UI, plugins, integrations, cloud, telemetry, health/readiness and recovery remain non-authoritative consumers/services.
- Discovery != trust; presence != authentication; authentication != authorization; physical connection != authorization.
- Surveillance Recording Storage and Personal Media Library Storage remain separate logical domains.
- Local-first remains the preferred operating model; cloud is an additional resource.
- Engineering/Digital Twin data remains under MediaHub's own domain model and provenance graph.
- LLM/VLM output is advisory/hypothesis-producing; authoritative BIM/engineering artifacts require deterministic validation/compilation.
- MH-05 qualification, MH-06, production and release remain locked.
- Immutable R4 `471f709f5633feab7aeb62dd3ea52effad6d2bc4` is never modified.

## 3. P0 — implement as MediaHub-owned capabilities

1. State Authority / canonical state and event path.
2. Product/variant model and capability matrix.
3. Device/function model and onboarding orchestration.
4. Automation/scenes/scheduling/energy semantics.
5. Security/identity/authentication/authorization/trust policy.
6. Storage domain model and retention/recovery semantics.
7. Media/personal-media/surveillance domain semantics.
8. Local Assistant and AI Gateway (routing, privacy, policy, audit).
9. Unified Search and Knowledge Graph.
10. Engineering Project model.
11. Digital Twin Graph with stable IDs, provenance, confidence and validation state.
12. Drawing Intermediate Representation (Drawing IR).
13. Engineering Graph and Cable Graph.
14. Deterministic Document Generator for drawings, schedules, cable journals, equipment lists, revisions and exports.
15. Engineering validation/rules engine.
16. Mobile API/auth/session/authorization contracts.
17. Cluster/resource governance and workload admission.
18. Installer/update/migration/recovery orchestration.
19. Evidence/provenance/checkpoint model.

## 4. P0/P1 open-source foundations

| Domain | Preferred component | Role | Policy |
|---|---|---|---|
| IFC core | IfcOpenShell | IFC parsing/generation/validation foundation | P0, pin exact release/commit |
| Web IFC | web-ifc | browser-side IFC read/write | P0/P1, isolate license boundary |
| OCR/document AI | PaddleOCR | PDF/image extraction and structured document understanding | P0 |
| Vision runtime | OpenCV + ONNX Runtime | deterministic CV/inference primitives | P0 |
| Local LLM | llama.cpp | edge/local inference and OpenAI-compatible local serving | P0 |
| GPU LLM | vLLM or SGLang | high-throughput GPU serving | P1 benchmark; choose one production path |
| Database | PostgreSQL + pgvector | canonical transactional data + initial vector retrieval | P0 |
| Durable workflows | Temporal | long-running/retryable workflow orchestration | P0/P1 after contract fit |
| Object storage | S3-compatible storage | media/documents/artefacts | P0 |
| Observability | OpenTelemetry Collector | telemetry pipeline | P0 |
| Metrics | Prometheus | metrics/time-series | P0 |
| Signing | Cosign/Sigstore | artifact signing/provenance | P0 |
| SBOM | Syft | SBOM generation | P0 |
| Security scan | Trivy | image/filesystem/dependency scanning | P0 |
| Backup | restic | backup/recovery | P0 |
| OTA | RAUC | appliance/embedded update and rollback | P0 for appliance track; Mender is reference alternative |
| 3D/web rendering | three.js + vtk.js/VTK as required | 3D/digital-twin visualization | P1 |
| Photogrammetry | OpenDroneMap | optional image-to-3D pipeline | P1 |
| Point cloud | CloudCompare | external engineering/reference tool | P1, separate process/license boundary |
| Visual workflow | ComfyUI or InvokeAI | optional generative visual workflows | P1, never authoritative geometry |
| Scale | K3s/Kubernetes + Argo CD | clustered deployment | P1/P2, only after local baseline |
| Registry | OCI registry/Harbor | artifact distribution | P1/P2 |
| Secrets | OpenBao or equivalent | secret lifecycle | P0 where deployment requires central secret service |

## 5. Reference-only projects

Jellyfin, Immich, Mender, Massing, FreeCAD and similar mature projects are architectural/UX/implementation references unless a separate dependency decision explicitly authorizes code integration. They must not become hidden authorities or replace MediaHub domain semantics.

## 6. Explicit exclusions from baseline

- Do not deploy both RAUC and Mender as production OTA authorities.
- Do not introduce PostgreSQL + pgvector + Qdrant + OpenSearch simultaneously without benchmark evidence.
- Do not make both vLLM and SGLang production serving authorities; benchmark and select one per deployment profile.
- Do not make Jellyfin or Immich the MediaHub canonical media model.
- Do not make FreeCAD the canonical BIM/engineering model.
- Do not make an LLM the authoritative geometry compiler.
- Do not introduce Kubernetes before the local/systemd/Compose development baseline is reproducible.

## 7. Passport traceability

| Passport capability | Component boundary | Primary foundation | Authority |
|---|---|---|---|
| Smart Home | smart_home_core/device_management/automation_core | Home Assistant internal + MediaHub model | State Authority |
| Surveillance | surveillance_core/storage_core | media/video stack + object/block storage | State Authority |
| Personal Media | personal_media_core/media_core | media processing + object storage | State Authority |
| Local Assistant | assistant_core/knowledge_core/search_core | llama.cpp + OCR/CV + retrieval | MediaHub AI Gateway; advisory output |
| Engineering | engineering_core | IfcOpenShell/web-ifc + Drawing IR | MediaHub engineering model |
| Digital Twin | engineering_core/knowledge_core | IFC + graph/DB + 3D renderer | MediaHub Digital Twin Graph |
| Mobile | mobile_media/ui_core + API boundary | iOS/iPadOS platform APIs | State Authority/API contracts |
| Cluster | cluster_core/resource_governance | local runtime + later K3s | MediaHub scheduler/governance |
| Updates | lifecycle_core/recovery_core | RAUC + signed artifacts | MediaHub lifecycle authority |
| Security | security_core/privacy_security | OS/platform crypto + scanners/signing/secrets | Security policy + authorization boundary |
| Observability | observability/diagnostics | OTel + Prometheus | observation only |

## 8. Implementation order

### Pass A — architecture/materialization
Create component registry, dependency constraints, license/provenance fields, and passport traceability. No production release implication.

### Pass B — foundation
Materialize State Authority contracts, runtime, persistence boundary, object storage boundary, security/identity contracts, evidence model.

### Pass C — product verticals
Implement Smart Home/device/automation, surveillance, personal media, media/audio, mobile, network/cluster, and engineering vertical slices through the canonical command/state/event path.

### Pass D — engineering moat
Implement Drawing IR, Digital Twin Graph, Engineering Graph, Cable Graph, deterministic document generator and validation/rules engine.

### Pass E — AI
Implement AI Gateway, local model runtime, OCR/CV, retrieval and Knowledge Graph. Enforce advisory-vs-authoritative boundary.

### Pass F — production engineering
Observability, SBOM, scanning, signing, backup, OTA, migration/recovery, installer and hardware qualification.

### Pass G — scale
Only after reproducible local baseline: GPU serving, registry, K3s/Kubernetes, GitOps, distributed storage/compute.

## 9. Evidence gates for every component

Before an external component becomes a runtime dependency, record:

- exact version or immutable commit;
- upstream source and license;
- transitive dependencies;
- maintenance/release posture;
- known security advisories;
- compatibility with target Linux/iOS/build toolchains;
- reproducible acquisition/build procedure;
- SBOM entry;
- security scan result;
- test coverage and integration contract;
- rollback/removal path;
- owner and authority boundary.

## 10. Current engineering conclusion

The selected component set improves MediaHub substantially because it closes the major implementation gaps identified by the passport: engineering/Digital Twin, document intelligence, local AI, durable workflows, storage, observability, supply-chain security, recovery/OTA and scalable compute.

The components are deliberately subordinate to MediaHub's architecture. The strategic moat remains MediaHub-owned: canonical domain model, state authority, provenance, Drawing IR, Digital Twin Graph, Engineering/Cable Graph, deterministic document generation, validation, AI policy/routing and unified UX.

**Status: READY FOR AUTONOMOUS ENGINEERING MATERIALIZATION.**

This report does not authorize MH-05 qualification, MH-06, production release, or release freeze.
