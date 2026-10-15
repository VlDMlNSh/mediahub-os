# MediaHub OS — Unified Component Candidate & Evaluation Register

- Date: 2026-10-15
- Repository: `VlDMlNSh/mediahub-os`
- Documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Status: **UNIFIED RESEARCH REGISTER / CANDIDATES ONLY / NOT AN ADMISSION OR TEST AUTHORIZATION**
- Purpose: one durable, deduplicated index of components already present in the project’s candidate universe, canonical manifest and targeted ecosystem research, with evaluation order and evidence gates.
- Scope statement: this is a broad, repository-bounded reconciliation of identified project artifacts, not proof that every GitHub repository has been scanned or that the historical “40 components” list has been recovered exactly.
- Owner direction: greenfield target for new hardware. Old-server installs, host paths, service names, worker routes and failed deployments are historical context, not target configuration.
- Canonical navigation: [Project map](MEDIAHUB-CHAT-TREE-MAP.md); [Canonical Component Manifest 2.0](../checkpoints/mediahub-github-component-final-manifest-2.0.md); [Admission Crosswalk Wave 01](../checkpoints/MEDIAHUB-COMPONENT-ADMISSION-CROSSWALK-WAVE-01-2026-10-14.md); [Autonomous Agent Ecosystem Survey](../checkpoints/MEDIAHUB-AUTONOMOUS-AGENT-ECOSYSTEM-SURVEY-2026-10-14.md); [Mature Candidate Screen Wave 01](MEDIAHUB-MATURE-COMPONENT-CANDIDATE-SCREEN-WAVE-01-2026-10-15.md); [Chat Consolidation Master Prompt](../checkpoints/MEDIAHUB-CHAT-SESSION-CONSOLIDATION-MASTER-PROMPT-2026-10-15.md).

## 1. Interpretation and authority

This register consolidates candidates; it does **not** replace or silently amend the accepted Functional Baseline 2.0, accepted domain/security contracts, owner decisions or Canonical Component Manifest 2.0.

Statuses have different meanings:
- **FOUNDATION-SELECTED (manifest)** — selected as a development foundation in Manifest 2.0; not proof of installation, compatibility, qualification or production admission on new hardware.
- **TARGET-GATED (manifest)** — candidate in Manifest 2.0, gated on target requirements and qualification.
- **FUTURE-GATED (manifest)** — retained as a future/reference candidate; only reconsider after a concrete capability gap.
- **RESEARCH-CANDIDATE** — surfaced by ecosystem research, not selected/admitted.
- **ALTERNATIVE** — overlaps another candidate in the same role; compare before selecting one.
- **HOLD / EXCLUDED / LEGACY** — not in the active evaluation queue unless the listed condition is met. Historical operational artifacts are not automatically software candidates.

No component is currently promoted by this document to IMPLEMENTED, TESTED, VERIFIED, QUALIFIED, RELEASED, DEPLOYED or ACCEPTED. A README/blob SHA is not an immutable upstream release pin.

## 2. Evaluation backlog — unified candidate set

### A. Contracts, persistence, storage, and recovery

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| PostgreSQL | canonical relational persistence | FOUNDATION-SELECTED (Manifest 2.0) | Confirm target deployment mode, schema ownership, backup/restore and resource profile against hardware/OS; canonical state remains MediaHub-owned. |
| pgvector | vector extension in PostgreSQL | FOUNDATION-SELECTED / TARGET-GATED | Demonstrate a capability gap and benchmark within PostgreSQL; no second vector store by default. |
| Protobuf | versioned typed contracts | FOUNDATION-SELECTED | Pin compiler/runtime versions and compatibility/evolution policy. |
| gRPC | typed RPC transport | FOUNDATION-SELECTED | Verify auth, deadlines, cancellation, retry/idempotency, observability and version compatibility at the contract boundary. |
| S3-compatible object storage | object API/interface | FOUNDATION-SELECTED interface; implementation TBD | Define contract first; compare target-fit implementations only after capacity, durability and failure requirements are known. |
| SeaweedFS | distributed object/file/S3 implementation | TARGET-GATED / conditional sidecar | Only if storage requirements justify a separate service; assess recovery, operational footprint and data migration. |
| restic | backup/restore mechanics | TARGET-GATED | Recovery authority stays MediaHub-owned; verify backup consistency, restore evidence, encryption and rollback. |
| Btrfs / OpenZFS | filesystem/storage mechanisms | FUTURE-GATED / platform-dependent | Requires exact OS/filesystem support, storage topology and recovery requirements. |
| Syncthing | file synchronization | FUTURE-GATED | Non-authoritative sync only; never canonical state replication without explicit contract. |
| NATS JetStream | asynchronous messaging | FUTURE-GATED | Admit only for an evidenced messaging gap; no second broker by default. |
| etcd | coordination/key-value store | FUTURE-GATED | Avoid creating a second coordination/state authority; require explicit consistency and operational need. |
| OpenBao | secrets-management service candidate | FUTURE-GATED | Compare with accepted SOPS+age configuration/secrets approach; avoid duplicate secret authority. |
| Redis | cache/event/state store | EXCLUDED BY DEFAULT | Reopen only with documented gap, decision and requalification. |
| Kafka | event platform | EXCLUDED BY DEFAULT | Reopen only with documented scale/capability gap and architecture decision. |
| MinIO | S3 implementation | EXCLUDED in Manifest 2.0 | Do not re-admit without owner-approved reconsideration of the recorded exclusion and current upstream facts. |

### B. Agent orchestration, corporation control, and durable execution

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| LangGraph | stateful agent graph/orchestration | RESEARCH-CANDIDATE / shortlist | Compare pinned revision against Microsoft Agent Framework; persistence, replay, tool isolation, cancellation and fit to accepted mission/result contracts. |
| Microsoft Agent Framework | agent and multi-agent orchestration | ALTERNATIVE | Compare against LangGraph on identical requirements; do not adopt both by default. |
| Pydantic AI | typed agent/application framework | RESEARCH-CANDIDATE | Check typed I/O, retries, provider boundaries, tool permissions and overlap with selected orchestrator. |
| Google ADK | agent development framework | RESEARCH-CANDIDATE | Check provider/platform coupling, local-first support, license and contract fit. |
| CrewAI | multi-agent orchestration | RESEARCH-CANDIDATE / overlap | Compare only if it offers a measurable capability not covered by the primary candidate. |
| OpenHands Software Agent SDK | coding-agent SDK / Agent Server | RESEARCH PIN ONLY / NOT READY FOR RUNTIME EVALUATION | Pin source and artifact, close transitive SBOM/license/advisory provenance, choose isolated workspace profile, resolve provider routing and authorization boundary. |
| Cline | coding-agent product/reference | RESEARCH-CANDIDATE | Assess as a developer-facing tool, not as corporation authority; check automation/API and sandbox fit. |
| Letta Code | coding-agent / memory-oriented agent | RESEARCH-CANDIDATE | Determine overlap with coding agent and memory services; prove data/control boundaries. |
| OpenClaw | agent runtime/product candidate | RESEARCH-CANDIDATE / security review required | Exact identity, revision, threat model, tool/network/credential boundary and local-only behavior. |
| Hermes Agent | autonomous agent candidate | RESEARCH-CANDIDATE | Exact upstream identity/revision, isolation, persistence, routing and authority separation. |
| Temporal Python SDK | durable workflow execution | FUTURE-GATED / shortlist for separate decision | Demonstrate a durable-lifecycle gap beyond ASTRA A0; no second queue/state authority; assess service and operational overhead. |
| Hatchet | durable workflow/task orchestration | ALTERNATIVE / FUTURE-GATED | Compare with Temporal only if durable execution is required; avoid duplicate orchestration authorities. |
| Jarvis corporation coordinator | project-specific architecture role, not third-party package | OWNER-DIRECTED ARCHITECTURE INPUT | Mission coordination only; must not write ASTRA internal state or Product State Authority state directly. |
| ASTRA A0 | engineering workflow authority | EXISTING PROJECT ARCHITECTURE / CONTRACT GATES OPEN | Do not infer accepted ingress, issuer/delegation, cancellation, fencing or lifecycle semantics where source contracts do not prove them. |
| Product State Authority | canonical product-state mutation authority | ARCHITECTURAL INVARIANT | No agent, framework, sidecar, policy engine or persistence product may take over this authority. |

### C. Tool and agent interoperability protocols

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| MCP Python SDK / Model Context Protocol | tool/resource/context interface | RESEARCH-CANDIDATE / shortlist | Per-tool capability checks, server identity, input validation, audit, sandbox, egress and version pin; protocol support is not authorization. |
| A2A protocol / SDK ecosystem | agent-to-agent federation | HOLD | Capture full official source and immutable revision; define trust, auth, task/result lifecycle and compatibility before comparison. |
| ACP (Agent Communication Protocol) | agent communication/lifecycle protocol | HOLD / targeted source review | Exact version and cancellation/cleanup lifecycle; no external controller gets ASTRA/product authority. |
| Protobuf/gRPC | typed contracts and transport | FOUNDATION-SELECTED | Shared with section A; evaluate as contract substrate, not a grant of authority. |

### D. Policy, security, sandbox, identity, secrets, and supply chain

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| Open Policy Agent (OPA) | policy decision engine | RESEARCH-CANDIDATE / shortlist | Policy inputs/provenance, fail-closed behavior, policy versioning and enforcement points; never state authority. |
| OpenShell | execution/security sandbox candidate | RESEARCH-CANDIDATE | Verify isolation model, OS support, filesystem/process/network/egress/credential/resource controls and audit evidence. |
| Infisical | secrets/configuration service | RESEARCH-CANDIDATE | Compare with SOPS+age and possible OpenBao; avoid multiple secret authorities. |
| SOPS + age | encrypted config/secrets mechanics | FOUNDATION-SELECTED (Manifest 2.0) | Verify key custody and target deployment approach; never record secret values in the register. |
| Cosign | artifact signing/verification | FOUNDATION-SELECTED | Establish signature verification policy and provenance linkage. |
| Syft | SBOM generation | FOUNDATION-SELECTED | Produce locked dependency inventory for an admitted artifact. |
| Trivy | vulnerability/secrets/filesystem scanning | FOUNDATION-SELECTED | Scan only under separately authorized qualification/test plan; scanner output is evidence, not automatic admission. |
| Caddy | edge/reverse-proxy mechanics | TARGET-GATED | Need topology, TLS/auth/egress and OS fit; must not become a second policy or authority layer. |
| Harbor | self-hosted OCI registry | TARGET-GATED | Only if a private artifact registry is required; supply-chain, storage and operations review. |
| WireGuard | network primitive | FUTURE-GATED | Does not replace MediaHub authorization or any accepted network/security contract. |

### E. Observability, evaluation, and verification

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| OpenTelemetry Collector | telemetry pipeline | FOUNDATION-SELECTED / shortlist | Local-first defaults, sensitive-data filtering, retention, destination/egress, credentials and resource costs. |
| Prometheus | metrics | FOUNDATION-SELECTED | Metrics only; not correctness or qualification authority. |
| Arize Phoenix | AI tracing/evaluation observability | RESEARCH-CANDIDATE | Assess local deployment, sensitive-data handling, retention and export behavior. |
| Inspect AI | evaluation harness | RESEARCH-CANDIDATE | Define authorized offline evaluation suite, model/provider boundary and reproducible evidence. |
| Promptfoo | prompt/model evaluation | RESEARCH-CANDIDATE | Pin exact revision; evaluate local-only operation, secret/egress behavior and reproducibility. |
| DeepEval | LLM evaluation | RESEARCH-CANDIDATE | Same gates as other evaluation harnesses; no model/provider call without explicit authorization. |
| OpenTelemetry (SDKs/exporters) | instrumentation | FOUNDATION-SELECTED family | Pin compatible versions; prevent telemetry from becoming authority or leaking sensitive content. |

### F. Local inference and model-serving runtimes

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| Ollama | local model runtime/service | RESEARCH / EXISTING HISTORY, NOT NEW-TARGET PROOF | Determine if target requirements justify it; pin runtime/model digest/license and enforce local-only fail-closed routing. |
| llama.cpp | local LLM inference | TARGET-GATED / Manifest 2.0 | Benchmark only after target hardware and workload are specified; exact build/model provenance and license required. |
| ONNX Runtime | general model inference | TARGET-GATED / Manifest 2.0 | Workload/model-specific hardware acceleration and licensing review. |
| SGLang | high-throughput serving | FUTURE-GATED | Admit only if throughput/serving requirements demonstrate a gap; compare with vLLM. |
| vLLM | high-throughput serving | FUTURE-GATED | GPU/OS/hardware gate and measured need; do not duplicate production runtimes for the same workload. |
| LiteLLM | model/provider routing abstraction | RESEARCH-CANDIDATE / route-boundary review | Exact provider identity, local-only enforcement, fallback behavior, egress, secret custody and model identity consistency. |
| FreeLLMAPI / FCC / OmniRoute / UnoRouter / Alamo | unresolved names/routes/gateway candidates | HOLD — IDENTITY AND ROUTE CONTRACT CONFLICTS OPEN | Resolve exact repository/package, process role, upstream provider, endpoint, model identity and egress; never merge similar names by assumption. |
| Model artifacts (e.g. Qwen tags or hosted model names) | model weights / logical model IDs | NOT COMPONENT ADMISSION | Require exact digest, source, license, quantization and route identity; a mutable tag does not prove identity. |

### G. Memory, retrieval, knowledge graph, and document processing

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| Letta | persistent agent memory | RESEARCH-CANDIDATE | Prove concrete gap; define data retention, deletion, privacy, authority and portability. |
| Mem0 | memory layer | RESEARCH-CANDIDATE / overlap | Compare with Letta/Graphiti and existing project-owned state; no second source of truth. |
| Graphiti | temporal knowledge graph/memory | RESEARCH-CANDIDATE | Determine if graph semantics are required; evidence, provenance, lifecycle and authority boundaries. |
| Haystack | retrieval/document pipeline | RESEARCH-CANDIDATE | Assess ingestion, retrieval, security, local operation and overlap with existing architecture. |
| Qdrant | vector database | RESEARCH-CANDIDATE / default excluded absent gap | Compare against PostgreSQL+pgvector with measured workload; no second vector store by default. |
| Apache Jena | semantic-web / RDF platform | FUTURE-GATED | Admit only for a proven semantic-web capability gap and explicit storage/authority model. |
| RDFLib | RDF interoperability library | TARGET-GATED (Manifest 2.0) | Narrow library-level fit, serialization compatibility, provenance and dependency review. |
| PaddleOCR | OCR | TARGET-GATED (Manifest 2.0) | Language/document requirements, accuracy benchmark, model license and privacy isolation. |
| Unstructured | document ingestion/partitioning | TARGET-GATED | File-type support, parser sandboxing, data egress and sensitive-document boundary. |
| Paperless-ngx | document-management sidecar | CONDITIONAL whole-product candidate | Sensitive-data isolation, ownership, backup/restore, adapter and data export/deletion. |

### H. Media, cameras, audio, photos, and playback

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| FFmpeg | media processing/codecs/transcoding | FOUNDATION-SELECTED | Exact build/license/codec inventory, untrusted-input isolation, resource limits and provenance. |
| OpenCV | computer vision primitive | FOUNDATION-SELECTED / TARGET-GATED in YAML | Workload and target-architecture fit, dependencies and isolation. |
| Jellyfin | media library/server/playback | Manifest whole-product candidate | Adapter boundary, metadata ownership, backup, security and resource profile. |
| Music Assistant | music provider/player orchestration | Manifest whole-product candidate | Provider/data-egress controls and MediaHub-owned domain contract. |
| Snapcast | synchronized multiroom audio | Manifest whole-product candidate | Latency/network topology, device support and recovery. |
| Frigate | camera/NVR/recording/object detection | Manifest whole-product candidate | Camera/network isolation, retention/privacy, hardware acceleration and threat model. |
| Immich | photo/video ingestion and organization | Manifest whole-product candidate | Private-data boundary, backup/restore, mobile ingestion and migration. |
| MediaMTX | live-media transport/router | TARGET-GATED | Target topology, protocol/security, stream lifecycle and workload fit. |
| go2rtc | camera/live-stream adapter | TARGET-GATED / conditional sidecar | Camera-specific fit and avoid duplicating MediaMTX responsibilities without evidence. |
| mpv | playback engine | TARGET-GATED | Compare against libVLC for required platforms, codecs, integration and license. |
| libVLC | alternative playback engine | ALTERNATIVE to mpv | Do not deploy both by default. |
| Home Assistant Core | smart-home integration/control plane | Manifest/YAML target-gated component | Smart-home authority only within its accepted domain; integration boundary and security qualification. |

### I. Digital twin, BIM, CAD, 3D, and creative workflows

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| IfcOpenShell | IFC/BIM processing | TARGET-GATED / Manifest 2.0 | File/version compatibility, dependency/license review and target workload. |
| web-ifc | browser/client IFC engine | TARGET-GATED | Client platform and compatibility with IfcOpenShell artifacts. |
| VTK / vtk.js | scientific/3D visualization | TARGET-GATED | Separate server/client roles, resource footprint and data formats. |
| FreeCAD | CAD/engineering reference | FUTURE-GATED | Use only if target engineering workflow requires it. |
| CloudCompare | point-cloud reference | FUTURE-GATED | Use only for a proven point-cloud workflow. |
| ComfyUI | generative media workflow | FUTURE-GATED | Local-only/egress, model provenance, isolation and workflow reproducibility. |

### J. OS, update, edge, and deployment infrastructure

| Component / family | Role | Current disposition | Evaluation question / gate |
|---|---|---|---|
| RAUC | atomic update mechanics | TARGET-GATED | Only after target OS/update authority is defined; MediaHub remains sole release/update authority. |
| Mender | update platform/reference | FUTURE-GATED | No second OTA authority; compare only if a documented capability gap remains. |
| Kubernetes / K3s | container orchestration | FUTURE-GATED, never prerequisite | Do not add by default; require topology, workload and operations evidence. |
| Argo CD | deployment reference | FUTURE-GATED | No second deployment/update authority; do not use before Contour A gates. |
| S3-compatible storage implementations | object storage | INTERFACE SELECTED / IMPLEMENTATION OPEN | Choose only after hardware, capacity, durability, backup and recovery requirements are known. |

### K. Developer tools, repositories, and non-component references

| Candidate | Role | Current disposition |
|---|---|---|
| OpenHands / Software Agent SDK | autonomous coding-agent substrate | Candidate-only; detailed artifact/security/isolation gates open. |
| Everything Claude Code (ECC) | coding workflow/rules/skills reference | REFERENCE ONLY until exact revision, license, security and overlap review is complete; not automatically a runtime component. |
| browser-use | browser automation library/agent | Research candidate; requires isolated browser, identity, permissions, egress and audit contract. |
| Home Assistant integrations and other sidecars | domain-specific integrations | Individual admission only; parent product presence does not admit every plugin/integration. |

## 3. Consolidated role count and historical “40 components” question

This register deliberately includes both third-party components and project-specific control-plane roles, and therefore is not a claim that the historical list contained exactly 40 items. Earlier records contain multiple overlapping sets and aliases (including alternatives, whole-product sidecars, future-gated references and unresolved provider-route names). The exact original 40-item source has not been independently recovered in the available repository evidence. Do not invent an exact count or silently trim the candidate universe to 40.

The machine-readable `oss/manifests/components.yaml` is explicitly an admission subset, not the exhaustive catalogue. Its omissions do not mean exclusion. Manifest 2.0 remains the canonical component-selection input; this register is the unified evaluation/navigation layer and does not supersede it.

## 4. Evaluation sequence — source-first, no runtime execution

**Wave 0 — prerequisites and contract closure**
1. Confirm target hardware model/specifications, OS/builds, architecture, memory, storage, accelerators and network topology from owner-provided evidence.
2. Derive capability requirements and constraints from Functional Baseline 2.0 and accepted domain/security contracts.
3. Resolve outstanding identity/egress conflicts for FreeLLMAPI/FCC/OmniRoute/UnoRouter/Alamo and model-tag provenance.
4. Resolve accepted Jarvis→ASTRA A0 ingress, capability issuer/delegation/expiry/revocation, cancellation/completion/retry/idempotency, stale-worker fencing, Task Result Envelope/DAG and evidence contract gaps before selecting orchestration frameworks.
5. Pin each upstream candidate to exact tag/commit/artifact and record source-to-artifact provenance, license/notices, SBOM and advisory review.

**Wave 1 — non-overlapping architecture comparisons (documentary only)**
1. LangGraph vs Microsoft Agent Framework vs Pydantic AI; add Google ADK/CrewAI only where they provide a distinct, evidenced alternative.
2. MCP interface/security review; A2A and ACP stay HOLD until source/version/lifecycle evidence is complete.
3. OPA policy-fit review against accepted authorization contracts; OpenShell isolation review; compare Infisical/OpenBao only against the existing SOPS+age direction.
4. OpenTelemetry Collector and local-first evaluation/telemetry candidates; define data redaction, retention and egress.
5. OpenHands SDK exact artifact/SBOM/license/security/workspace review before any runtime request.
6. Temporal vs Hatchet only if ASTRA’s accepted lifecycle contract leaves a demonstrated durable-execution gap.
7. Compare Letta/Mem0/Graphiti/Haystack/Qdrant against project-owned state and PostgreSQL+pgvector; require a capability gap.
8. Compare local inference candidates only after hardware and workload profiles exist; establish exact model identity and fail-closed local-only routes.
9. Evaluate manifest media/document/digital-twin/storage sidecars against explicit product requirements and adapter contracts.

**Wave 2 — separately authorized execution**
No install, test, benchmark, model/provider call, security scan, host/runtime inspection or qualification occurs by virtue of this register. These actions require separate explicit authorization and a scoped plan. When authorized, test only pinned candidates in an isolated environment, record commands/results/artifacts, and keep verification, qualification, release, deployment and acceptance as separate gates.

## 5. Mandatory admission record for each candidate

Every candidate record must include:
1. Stable historical component ID and role; candidate aliases and collision check.
2. Capability gap and Baseline 2.0 requirement trace.
3. Canonical upstream repository, exact immutable commit/tag, package/artifact version and digest.
4. Source-to-artifact provenance; license and notices; full transitive SBOM; vulnerability/advisory findings.
5. Target OS/architecture/hardware compatibility evidence.
6. Data classification, trust boundary, network/egress and provider/model identity.
7. Allowed and forbidden operations; capability issuer and authorization enforcement point.
8. MediaHub-owned adapter and versioned contract; state ownership and idempotency/cancellation/recovery semantics.
9. Functional, negative, degraded-mode, recovery, upgrade/rollback and resource benchmark plan/results (only after authorization).
10. Independent reviewer, evidence links and UTC timestamp.
11. Separate statuses for design, implementation, testing, verification, qualification, release, deployment and acceptance.
12. Removal/replacement plan and dependency/reference closure.

Missing evidence means UNKNOWN / BLOCKED, never PASS. Popularity, an upstream README, a package manifest, a process name or a mutable tag does not prove admission.

## 6. Architecture invariants that the evaluation must preserve

- Functional Baseline 2.0 is canonical; Baseline 1.0 is historical provenance.
- Product State Authority alone mutates canonical product state.
- Jarvis coordinates corporation-level missions; ASTRA A0 owns ASTRA-internal engineering lifecycle state; do not conflate their authorities.
- Agent frameworks, workflow engines, MCP/A2A/ACP, policy engines, memory stores, telemetry systems, sidecars and model runtimes do not become authority by integration.
- Local-only routes fail closed; no silent cloud/provider fallback.
- Do not add two overlapping orchestrators, two vector stores, two message brokers, two recovery authorities, two OTA authorities or duplicate production inference runtimes without an evidenced gap and explicit decision.
- Contour A (autonomous development environment) must be deployed and independently accepted before product Contour B begins.
- Old-server configuration and failed installation attempts are not new-target baseline; preserve their historical evidence but do not reuse them by default.

## 7. Source records reconciled in this pass

- `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` — canonical development selection input; blob SHA at this pass: `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`.
- `oss/manifests/components.yaml` — explicit runtime-deployment admission subset; blob SHA: `e3cf487bcf43ecb92cd110b5af2660c066b58e2a`.
- `docs/checkpoints/MEDIAHUB-AUTONOMOUS-AGENT-ECOSYSTEM-SURVEY-2026-10-14.md` — research snapshot; blob SHA: `5c6cd19e338ed0f59823d18718a484f0129d2ef7`.
- `docs/checkpoints/MEDIAHUB-COMPONENT-ADMISSION-CROSSWALK-WAVE-01-2026-10-14.md` — admission crosswalk; blob SHA before OpenHands source refresh: `82b284ea67f578332e8f57b96a3571d1ecdf827b`; current refreshed blob SHA: `e5be83f63e974c6eb559515c6371a93ae36b1f2b`.
- `docs/architecture/MEDIAHUB-MATURE-COMPONENT-CANDIDATE-SCREEN-WAVE-01-2026-10-15.md` — focused initial screen; blob SHA: `e20570b6f61fed2fb1232cbeb84286ce2e8dca1d`.
- `docs/checkpoints/MEDIAHUB-CHAT-SESSION-CONSOLIDATION-MASTER-PROMPT-2026-10-15.md` — chat reconciliation ledger; blob SHA: `5f5163ca42e900fb3d90b9f8feb0ef7d8b895fa3`.

These SHA values identify the files reviewed during this pass; they are not upstream component version pins.

## 8. Current result and next step

Result: a single deduplicated, role-grouped candidate/evaluation register has been drafted from the repository records above. It intentionally preserves competing candidates and conflicting/unresolved route names instead of selecting them by assumption.

Not done: exhaustive search of all public GitHub repositories, recovery of the exact historic 40-item list, immutable pinning for every candidate, hardware compatibility determination, installs/tests/benchmarks/provider calls, security scans, qualification, deployment or owner acceptance.

Next bounded step: complete Wave 0 prerequisites and source-pin the top non-overlapping agent/tool/policy candidates. The target hardware/OS inventory and open identity/authorization contracts remain blockers. No runtime actions are authorized by this register.


### OpenHands source-pin update (2026-10-15)

- Upstream source revision identified: `OpenHands/software-agent-sdk@v1.54.0`, commit `1d471742ea7be017d013eaaa3080f5d28d5490cb`.
- Python requirement: `>=3.12`; repository license text is MIT. These facts do not close full transitive licensing or artifact provenance.
- Agent Server documentation's default bind `0.0.0.0` and optional session API-key authentication are not acceptable as a default MediaHub deployment profile. SDK and server must be evaluated separately; require explicit isolation, bind/auth, egress, credential, retention and audit design before any runtime consideration.
- Still OPEN: wheel/sdist digest and source-to-artifact provenance; locked transitive SBOM/advisory/license closure; target compatibility; isolated workspace controls; LiteLLM route/egress and LMNR telemetry privacy. Candidate remains NOT SELECTED / NOT ADMITTED / NOT QUALIFIED.
- Source details and exact upstream file blob SHAs are maintained in [Component Admission Crosswalk Wave 01](../checkpoints/MEDIAHUB-COMPONENT-ADMISSION-CROSSWALK-WAVE-01-2026-10-14.md) §7.17. No runtime action occurred.
