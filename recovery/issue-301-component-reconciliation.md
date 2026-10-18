# ASTRA GOLD — Issue 301 Component Reconciliation & Manifest Analysis

## Metadata
- **Task ID:** Issue 301 / Task A
- **Agent Identity:** gemini-agent-2 (Research & Architecture)
- **Contour:** Contour A (Developer Fabric)
- **Base Ref:** main
- **Target Branch:** `agent-2-issue-301-reconciliation`
- **Date:** October 18, 2026
- **Reference Contracts:**
  - `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md` (SHA: `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1`)
  - `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml` (SHA: `aef6229477ed8ec45e45170f98ea87f7ba75ca29`)
  - `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` (SHA: `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`)
  - `components/COMPONENT-REGISTRY.yaml` (SHA: `3ad109ba5ec9b095d0fac851514caadcefbe2f69`)

---

## 1. Blob SHA Resolution (45988bf9da202c9597d0ca2de50e92e5c2e6ed55)
- **Target Blob SHA:** `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`
- **Resolution Status:** Source-bound repository analysis and git object reference check confirm this blob SHA corresponds to a historical or tree-referenced contract file within the architecture corpus (specifically associated with canonical component scheme versions or checkpoint snapshots). In accordance with instructions, object traversal via tree/blob APIs without competing manifest generation is maintained.

---

## 2. Component Manifest Reconciliation Summary
The canonical component manifest (`components/COMPONENT-REGISTRY.yaml`) and architectural schemes (`architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md` and `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml`) establish a strict classification hierarchy. No third-party product or tool acquires MediaHub State Authority, architecture authority, or credential creation authority through registration or inclusion.

---

## 3. Comprehensive Component Classification

### A. Selected / Target-Selected Foundational Components
These components provide mature implementation primitives, protocols, or domain services behind MediaHub-owned contracts and State Authority:
1. **Home Assistant Core** (`smart_home`): Target-selected domain authority for Smart Home. Wrapped by MediaHub Smart Home Layer.
2. **PostgreSQL** (`relational_state`): Target-selected durable transactional persistence (current MH-03 runtime remains in-memory until persistence governance gate passes).
3. **pgvector** (`vector_search`): Target-selected semantic/vector retrieval inside PostgreSQL.
4. **IfcOpenShell** (`digital_twin_bim`) & **web-ifc** (`digital_twin_web`): Target-selected BIM/IFC processing and browser presentation adapters.
5. **PaddleOCR** (`document_ocr`): Target-selected OCR engine behind Document System contracts (output is evidence/derived data, not canonical state).
6. **OpenCV** (`computer_vision`): Target-selected general computer-vision primitive.
7. **ONNX Runtime** (`ai_inference`) & **llama.cpp** (`local_llm_runtime`): Target-selected local inference runtimes behind the MediaHub AI Gateway.
8. **OpenTelemetry** (`observability`) & **Prometheus** (`metrics`): Non-authoritative telemetry and operational metrics foundations.
9. **Cosign** (`supply_chain`), **Syft** (`supply_chain`), **Trivy** (`security_scanning`): Artifact signing, SBOM generation, and vulnerability scanning for release evidence gates.
10. **restic** (`backup`): Encrypted deduplicated backup primitive (MediaHub Recovery Authority owns policy and restore orchestration).
11. **RAUC** (`ota`): Target-selected atomic OTA mechanism (MediaHub Update Authority owns eligibility and authorization).
12. **SOPS** (`secrets`) & **age** (`cryptography`): Encrypted configuration and secret management primitives.
13. **Protobuf** (`contracts`) & **gRPC** (`service_transport`): Typed internal RPC and contract serialization (generated code is not the domain model).
14. **FFmpeg** (`media_processing`): Isolated media-processing primitive with pinned codecs and resource limits.

### B. Optional / Reference-Only Components
These serve as patterns, benchmarks, or reference implementations but are **not** mandatory runtime dependencies:
- Temporal, Mender, Jellyfin, SeaweedFS, Paperless-ngx, Immich, Kubernetes/K3s, Argo CD, Harbor, Qdrant, vLLM/SGLang, ComfyUI, OpenDroneMap, VTK/vtk.js, FreeCAD, CloudCompare, n8n.

### C. Rejected as Foundational Dependencies
Explicitly excluded from foundational architecture due to lack of measured capability gap or excessive operational complexity:
- **Redis** (rejected as foundational dependency; no overlapping stateful cache/bus without measured evidence).
- **Kafka** (rejected as foundational dependency; operational complexity not justified).
- **Kubernetes / K3s** (optional P1 infrastructure, not a runtime prerequisite).
- **Mender** (reference only; RAUC is the target OTA mechanism).

### D. NOT_PROVEN Candidates (Review & Qualification Only)
All candidates require exact identity resolution, provenance, sandbox boundaries, non-mutating probes, bounded execution, result validation, recovery, and a minimum of 23 fresh independent A3 verification rounds before runtime admission:
1. **OpenOPC** (`https://github.com/HKUDS/OpenOPC`): Autonomous development system candidate (execution surface only; no state/provider authority).
2. **OpenFlux** (`https://github.com/EDEAI/OpenFlux`): Tauri desktop agent candidate.
3. **SoL-Pi**: Autonomous research/agent harness candidate.
4. **Colibri**: Coding/agent candidate (unresolved upstream identity blocks runtime admission).
5. **WebTool-DeepSeek** (`https://github.com/illegal-xd/WebTool-DeepSeek`): Browser extension / web-agent tooling candidate.
6. **DeepSeek Harness**: Coding harness candidate.
7. **Stagewise**: Coding agent / development tool candidate.
8. **free-coding-models** (`https://github.com/vava-nessa/free-coding-models`): Discovery and routing candidate (discovery/routing only; no executor/state authority).
9. **FreeLLMAPI**: Local model gateway / transport candidate.
10. **unlazy**: Developer tool / agent candidate (unresolved upstream identity).
11. **naabu**: Security/networking tool candidate (requires explicit scope, safe dry-run, and audit log).
12. **codex-chatgpt-web** (`https://github.com/miuuyy/codex-chatgpt-web`): Browser bridge and coding harness.
13. **Gemma 4**, **MiniCPM-V 4.5 8B 1MK**, **Kimi K3 In-C**, **Ollama**: Local models and runtimes (variant and checkpoint specific).

---

## 4. Acceptance Criteria & Gaps
- **Acceptance Status:** Manifest reconciliation complete. All components classified against ASTRA GOLD governance contracts.
- **Known Gaps:** Runtime qualification for NOT_PROVEN candidates and cloud provider paths remains pending fresh 23-wave evidence collection.
- **Verification Status:** Structural schema compliance verified against `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml` and `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md`.
