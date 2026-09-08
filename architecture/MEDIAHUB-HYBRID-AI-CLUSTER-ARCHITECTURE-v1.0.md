# MediaHub OS 11.x LTS / MediaHub iOS
# Hybrid AI + Cluster Architecture v1.0

Date: 2026-09-08
Status: ENGINEERING BASELINE / NOT PRODUCTION QUALIFIED
Immutable MH-05 R4: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`

## 1. Purpose

Define the unified execution architecture for four AI tiers and two cluster planes:
- Local AI on a MediaHub node;
- Local MediaHub Cluster AI across trusted local nodes;
- Cloud Development Cluster AI in a separate privileged trust plane;
- Mobile AI client capabilities for MediaHub iPhone/iPad;
- Local MediaHub Cluster as the building/runtime compute plane;
- Cloud Development Cluster as privileged development/compute infrastructure.

This document materializes architecture only. It does not authorize MH-06, durable persistence,
HA production rollout, release, or production authorization while MH-05 qualification is open.

## 2. Non-negotiable authority model

State Authority remains the sole canonical mutation authority.
AI systems produce intents, proposals, hypotheses, plans, classifications or diagnostics.
AI, mobile UI, cluster orchestration, cloud compute, telemetry and external components cannot
write canonical state directly. All mutations pass through the governed command/authorization path.

The Local MediaHub Cluster is one coordinated user-facing system, not multiple competing authorities.
The Cloud Development Cluster is separate in identity, authorization, governance, data and egress.

## 3. AI Fabric

MediaHub AI Gateway is the common entry point for local, cluster and cloud AI execution.
The gateway classifies requests and selects an execution tier using deterministic policy:
latency, privacy, data classification, capability, resource availability, network state, cost,
model qualification and user authorization.

Execution tiers:
1. LOCAL — lowest-latency, privacy-first node execution.
2. LOCAL_CLUSTER — distributed AI/media workloads across trusted MediaHub nodes.
3. CLOUD_DEVELOPMENT — privileged burst GPU, CI, research and large-model workloads.
4. MOBILE_CLIENT — iPhone/iPad client execution and controlled calls into the AI Gateway.

Cloud escalation is explicit, auditable and fail-closed. Cloud availability never becomes a
precondition for ordinary local smart-home operation.

## 4. Local AI / Alamo

Alamo is the MediaHub local operational assistant. It is not the development agent harness.
Local inference may use llama.cpp or another qualified local runtime through an adapter.
Local AI can perform voice/text interaction, RAG, document/image interpretation, diagnostics,
planning and automation proposals. Deterministic validators and State Authority govern execution.

ECC remains outside the runtime as a developer-agent harness for autonomous engineering.

## 5. Local MediaHub Cluster

The local cluster provides coordinated compute, GPU/AI, media processing, transcoding, storage,
streaming, automation and bounded failover where the selected deployment profile supports them.

MediaHub-owned cluster semantics include node identity, membership, workload admission, scheduling,
resource quotas, health/fault classification, failover, split-brain protection, recovery, evidence,
and policy. K3s/Kubernetes and Argo CD are replaceable implementation substrates, not authorities.

Before multi-node production rollout, the cluster profile requires a qualified OCI registry,
artifact provenance/signing, resource governance, node trust, recovery evidence and failure testing.

## 6. Cloud Development Cluster

The cloud cluster is a privileged development/compute plane. It may provide burst GPU capacity,
large-model inference, training/evaluation, simulation, CI and research workloads.

It must enforce privileged identity, workload authorization, data minimization, residency,
egress controls, audit, metering, isolation and explicit transfer policy. It never receives direct
State Authority access and cannot become a fallback authority for home/runtime state.

## 7. Mobile product contour

MediaHub iOS is split conceptually into a minimal deployable Core and richer experiences.
The minimal iPhone/iPad application must support secure identity/session, MediaHub connectivity,
media access/control, smart-home operation, notifications, offline cache and the dashboard engine.

The iPhone is primarily a mobile user/control endpoint. The iPad additionally serves as a
persistent smart-home control surface with multi-room, media, climate, security, energy and
custom dashboard experiences.

## 8. iPad Dashboard Builder

Users can create panels from MediaHub capabilities rather than direct device APIs:
Select capability -> select room/device/media -> configure presentation/permissions -> preview
-> deterministic validation -> publish dashboard.

Published dashboards call governed MediaHub APIs. A dashboard cannot bypass authentication,
authorization, State Authority or device trust boundaries.

## 9. Mobile AI

The mobile client may use on-device capabilities for low-latency interactions and call the
MediaHub AI Gateway for local or cluster inference. Cloud AI is available only when policy permits.
Mobile AI receives the same advisory-vs-authoritative boundary as every other AI surface.

## 10. Reference execution flow

User -> iPhone/iPad -> Mobile Gateway -> AI Gateway -> Local / Local Cluster / Cloud Development
-> result/proposal -> policy validation -> governed command path -> State Authority -> event/observation.

For non-mutating tasks, the flow may terminate at an authorized read/search/media result.
For mutation requests, no AI or mobile component may skip validation and authorization.

## 11. Recovery and self-healing

Cluster self-healing follows: Observe -> Classify -> Decide -> Authorize -> Act -> Verify -> Record
-> Recover -> Escalate. Telemetry is observational. Recovery actions require deterministic policy
and authorization. Repeated failure moves the system into bounded degraded mode and escalation.

## 12. Component policy

Build as MediaHub IP: AI Gateway, AI Router, cluster semantics/control plane, resource governance,
mobile API contracts, dashboard model/builder, authority and policy boundaries, recovery semantics.

Adopt through isolated adapters: llama.cpp, PaddleOCR, OpenCV, ONNX Runtime, PostgreSQL/pgvector,
OpenTelemetry, Prometheus, Temporal, restic, Cosign, Syft, Trivy, OpenBao, K3s/Kubernetes, Argo CD,
OCI registry and other qualified infrastructure components.

Reference/integration only: Jellyfin, Immich, FreeCAD, n8n and other systems that must not become
MediaHub canonical authorities.

## 13. Qualification gates

Architecture materialization does not equal qualification. Every production cluster/AI/mobile
implementation requires exact version/provenance, license review, threat-model review, integration
and negative tests, reproducible evidence and rollback/recovery evidence.

MH-05 T5 independent security review and independent system-wide negative verification/F-03 remain
blocking for the immutable R4 qualification object. This architecture wave must not be represented
as independent qualification or production authorization.
