# MediaHub OS 11.x LTS / MediaHub iOS
# Hybrid AI + Cluster Architecture v1.0

Date: 2026-09-08
Status: ENGINEERING BASELINE / NOT PRODUCTION QUALIFIED
Immutable MH-05 R4: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`

## 1. Purpose

Define the unified execution architecture for the MediaHub Mobile Access Layer, three AI compute tiers and two cluster planes:
- Local AI on a MediaHub node;
- Local MediaHub Cluster AI across trusted local nodes;
- Cloud Development AI in a separate privileged company trust plane;
- MediaHub Core iPad and Remote Mobile Application as distinct mobile clients;
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

The cloud development environment is the privileged computational environment serving the needs of the MediaHub company. It includes website generation/storage/maintenance infrastructure, the Trusted Sources Intelligence Engine, the AI Human Clone Platform for authorized real-person digital clones participating in generated media content, engineering and Digital Twin compute, commercial infrastructure, burst GPU capacity, large-model inference, training/evaluation, simulation, CI and research workloads.

It must enforce privileged identity, workload authorization, data minimization, residency,
egress controls, audit, metering, isolation and explicit transfer policy. It never receives direct
State Authority access and cannot become a fallback authority for home/runtime state.

## 7. Mobile Access Layer

MediaHub Mobile Access Layer consists of two distinct products/modes:
1. **MediaHub Core for iPad** — the first minimal MediaHub Core client installed on iPad, providing
   governed access to MediaHub and SmartHome through the MediaHub API. It never talks directly to devices.
2. **Remote Mobile Application** — a remote iPhone/iPad client for accessing MediaHub services through
   the MediaHub API. It is a client, not an alternate authority.

Both clients use secure identity/session, governed MediaHub connectivity, media access/control,
smart-home operation, notifications, offline cache where permitted, and policy-controlled AI Gateway access.
Mobile is an access layer, not a mandatory AI execution tier.

## 8. iPad Dashboard Builder

Users can create panels from MediaHub capabilities rather than direct device APIs:
Select capability -> select room/device/media -> configure presentation/permissions -> preview
-> deterministic validation -> publish dashboard.

Published dashboards call governed MediaHub APIs. A dashboard cannot bypass authentication,
authorization, State Authority or device trust boundaries.

## 9. AI Human Clone Platform

The AI Human Clone Platform creates and operates authorized digital representations of real people
for participation in generated MediaHub media content. It is not an AI developer or autonomous software
engineer. Each clone requires explicit identity provenance, authorization/consent records, permitted
content/use scope, asset/model provenance, revocation, auditability and clear separation between
synthetic output and the real person. Clone generation remains subject to applicable safety, rights,
privacy and content policies. The platform cannot mutate canonical MediaHub state.

## 10. Reference execution flow

User -> MediaHub Core iPad / Remote Mobile Application -> MediaHub API -> AI Gateway -> Local / Local Cluster / Cloud Development
-> result/proposal -> policy validation -> governed command path -> State Authority -> event/observation.

For non-mutating tasks, the flow may terminate at an authorized read/search/media result.
For mutation requests, no AI or mobile component may skip validation and authorization.

## 11. Recovery and self-healing

Cluster self-healing follows: Observe -> Classify -> Decide -> Authorize -> Act -> Verify -> Record
-> Recover -> Escalate. Telemetry is observational. Recovery actions require deterministic policy
and authorization. Repeated failure moves the system into bounded degraded mode and escalation.

## 12. Component policy

Build as MediaHub IP: AI Gateway, AI Router, cluster semantics/control plane, resource governance,
mobile API contracts, Mobile Core/Remote Mobile client contracts, dashboard model/builder, Trusted Sources
Intelligence Engine orchestration/provenance semantics, AI Human Clone identity/authorization/provenance
semantics, Cloud Development Platform control boundaries, authority and policy boundaries, recovery semantics.

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
