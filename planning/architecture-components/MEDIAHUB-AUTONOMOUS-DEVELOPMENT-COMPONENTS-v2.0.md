# MediaHub Autonomous Development Component Profile v2.1

Date: 2026-09-08
Status: ENGINEERING BASELINE

## 1. ECC decision

ECC is adopted as an **engineering-harness accelerator**, not as a MediaHub runtime dependency and not as an authority. The official `affaan-m/ECC` repository is MIT licensed and provides skills, agents, hooks, rules, memory/context controls and security tooling for Codex/Claude Code and other harnesses.

ECC 2.2.1 was installed into an isolated Codex home for MediaHub validation. It must remain isolated from MediaHub runtime state.

## 2. Local Assistant distinction

Alamo/Local Assistant is a MediaHub product/runtime capability. ECC is a developer-agent operating layer. They solve different problems:
- Alamo: user-facing/local operational assistant; governed by MediaHub AI Gateway and State Authority boundaries.
- ECC: engineering workflow orchestration; plan/test/implement/review/verify and developer security/context assistance.
ECC cannot become part of canonical building state.

## 3. Cluster decision

Cluster is NOT deferred as an architectural capability. MediaHub explicitly requires two separate cluster planes:
1. Local MediaHub Cluster — building/runtime plane for coordinated compute, media, AI, storage, automation and failover.
2. Cloud Development Cluster — privileged development/compute plane for burst GPU, CI, research and controlled cloud escalation.

The implementation technology is what remains evidence-gated. K3s/Kubernetes, Argo CD, OCI registry and storage/network substrates are implementation choices, not reasons to postpone the cluster capability.

## 4. Mandatory cluster contracts

Identity, membership, coordination, workload placement, failover, split-brain protection, recovery, resource governance, data residency, egress, audit and metering must be implemented before production HA claims.

## 5. Autonomous development stack

P0: ECC + existing autonomous controller/watchdog/security gate + GitHub CI + deterministic test/security pipeline.
P0 runtime: State Authority, security/identity, storage domains, recovery/lifecycle, observability, evidence/provenance.
P0/P1 infrastructure: PostgreSQL/pgvector, object storage, Temporal, OTel, Prometheus, restic, RAUC, Cosign, Syft, Trivy, OpenBao.
P1 engineering/AI: IfcOpenShell, PaddleOCR, OpenCV, ONNX Runtime, llama.cpp, web-ifc, three.js/vtk.js.
P1 cluster: local cluster + cloud development cluster, with K3s/Kubernetes and Argo CD selected by qualification per profile.

## 6. Cloud Development Platform / AI Human Clone boundary

Cloud Development AI is the company-internal computational environment serving MediaHub company needs, not merely an engineering assistant. Its governed scope includes website infrastructure, Trusted Sources Intelligence Engine, AI Human Clone Platform, engineering/Digital Twin compute and broader commercial infrastructure.

**AI Human Clone Platform** means authorized digital clones of real people participating in generated media content. It is not an AI developer clone. The implementation must carry identity provenance, explicit authorization/consent, use/content scope, model/asset provenance, revocation and audit records, and must distinguish synthetic media from the real person. No clone service may mutate canonical MediaHub state.

Mobile architecture is the **MediaHub Mobile Access Layer** with two distinct clients: **MediaHub Core for iPad** and **Remote Mobile Application**. Both consume MediaHub APIs and never become alternate authorities or direct device-control paths.

Cloud is never ordinary-user direct access. Local/cluster AI may request controlled cloud compute only through the MediaHub AI Gateway when deterministic policy permits and data controls are satisfied.

## 7. Governance

No component may mutate canonical state directly. External tools are replaceable implementation dependencies. Exact versions, license, SBOM, security scan, provenance, integration tests and rollback path are mandatory.
