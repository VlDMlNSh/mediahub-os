# Wave 492 — Mature OSS shortlist for MediaHub Contour A and developer fabric

- Date: 2026-10-31
- Status: **RESEARCH SHORTLIST RECORDED / NO COMPONENT ADOPTED**
- Documentation base: canonical docs branch commit `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`
- Runtime source snapshot: `main` commit `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Primary driver: Contour A cloud-agent development fabric; developer tooling is supporting scope.
- Governing baseline: Functional Baseline 2.0; existing OSS integration and component-boundary rules remain authoritative.

## 1. Executive selection

The most useful mature projects to investigate first are:

1. **OpenHands Software Agent SDK** — reusable agent execution primitives and isolated workspaces; evaluate the SDK/Agent Server only, not its automation/dispatch control plane.
2. **Open Policy Agent (OPA)** — policy-as-code decision engine for testable, explicit policy evaluation; MediaHub remains the owner of policy, issuer, capability and authorization authority.
3. **Dagger** — reproducible, containerized build/test tasks that can run from existing GitHub Actions; it must not become a competing CI scheduler or release authority.
4. **Development Containers Specification + CLI** — standardized development environment and a reference implementation; directly relevant to Wave 490/491.
5. **GitHub Artifact Attestations + SLSA provenance** — GitHub-native provenance for build outputs, complementary to the existing Cosign/Syft/Trivy foundation.
6. **OpenTelemetry Collector** — standard telemetry collection/processing/export; extends the already selected non-authoritative OpenTelemetry foundation.

Retain **Temporal** as future-gated only. Do not adopt **Actions Runner Controller (ARC)** for the current Contour A default: it provisions self-hosted runners on a Kubernetes cluster, while the current target is GitHub-hosted ephemeral workers and no owner-operated server/Kubernetes prerequisite.

This is a research order, not an adoption decision. No software was installed, no dependency added, and no runtime was launched.

## 2. Existing MediaHub component decisions checked first

The current `main` source snapshot already contains:
- `oss/README.md` blob `b8f25ad20bf922264971afeb5a3dbf87d004ba3f`: bounded OSS integration tree; adapters isolate upstream APIs; MediaHub contracts remain canonical; versions/provenance are locked before qualification.
- `oss/manifests/components.yaml` blob `7141dd16e9ce9dba3440b1799a56e2ac4da4106d`: OpenTelemetry, Prometheus, Cosign, Syft, Trivy, SOPS, age, Protobuf, gRPC and FFmpeg are `current-foundation`; Temporal/NATS JetStream/etcd/OpenBao/object storage are future-gated; other components are target-gated.
- `architecture/COMPONENT-ARCHITECTURE-DECISIONS.md` blob `42b2701f0d6a1014435e96118e41e33025dbff08`: accepted component decision model and explicit non-authority rules.
- `architecture/COMPONENT-INTEGRATION-BOUNDARY.md` blob `d80f369ed126ac470ab60296559781e45cd203a4`: telemetry is observational; Syft/Cosign/Trivy are release-evidence mechanisms; third-party products do not own MediaHub domain semantics.
- `docs/checkpoints/mediahub-github-component-reconciliation-2.3-infrastructure-pass.md` blob `7fd870134f34a951fe872fe2d79a28554e24c5ca`: Temporal future-gated, Cosign/Syft/Trivy selected, Kubernetes/K3s and Argo CD reference-only, no mandatory orchestration platform.
- `docs/architecture/MH-20-automation-energy-self-healing-architecture.md` blob `4a0b09976e80dac03ce9ab89fd767de3bd783100`: workflow/scheduler candidates remain subject to requirements, compatibility, security, resource, operational, license and evidence review.

No duplicate registry or conflicting component classification is introduced by this report.

## 3. Ranked research shortlist

| Priority | Project | Reuse boundary | Why it fits | Main risk / disqualifier |
|---|---|---|---|---|
| P0 | OpenHands Software Agent SDK | Agent loop, tools, workspaces, event model; optionally sandboxed Agent Server | Directly relevant to coding-agent execution and workspace abstraction | Must not own scheduling, task admission, model routing, provider quota, PR promotion or authority; sandbox and tool permissions need review |
| P0 | OPA | Policy decision evaluation behind MediaHub-owned policy interface | Mature CNCF Graduated policy engine; policies can be tested separately from application code | Rego bundle lifecycle, policy distribution and failure semantics; OPA decision is not an issuer/capability credential |
| P0 | Dagger | Reusable build/test DAGs called from existing GitHub Actions | Same test/build definition can run locally and in CI; content-addressed incremental execution and tracing | Requires container runtime; can duplicate CI logic or expose secrets/network if not constrained |
| P0 | Dev Containers Spec + CLI | Developer environment metadata and CLI validation/build | Standard specification; reference CLI supports config read, build, up, exec, lockfile/frozen-lockfile | Lifecycle scripts, mutable Features, base-image provenance and host mounts |
| P1 | GitHub Artifact Attestations + SLSA | Provenance for specific build artifacts and workflow identities | GitHub-native signed provenance; reusable workflows can strengthen build isolation | Plan/repository visibility constraints; attestations do not prove task correctness or MediaHub acceptance |
| P1 | OpenTelemetry Collector | Receive/process/export traces, metrics and logs | CNCF Graduated telemetry pipeline; vendor-neutral and compatible with existing OTel foundation | Telemetry is non-authoritative; data minimization, exporter allowlist and no secrets/PII |
| P2 / future gate | Temporal | Durable workflow engine only if a demonstrated durability gap remains | Mature durable execution semantics | Introduces a second persistent workflow state subsystem; duplicates MediaHub-owned lifecycle/authority if adopted prematurely |
| Not for current default | Actions Runner Controller (ARC) | Kubernetes-managed self-hosted GitHub Actions runners | Mature GitHub-maintained runner autoscaling option for organizations operating Kubernetes | Wrong deployment target: self-hosted/Kubernetes infrastructure, not GitHub-hosted ephemeral runners |

### P0 — OpenHands Software Agent SDK

Repository: https://github.com/OpenHands/software-agent-sdk  
Documentation: https://docs.openhands.dev/sdk

The SDK provides Python/TypeScript/REST APIs for coding agents, tools, conversations, workspaces and events. Its architecture separates the SDK/Agent Server execution layer from the OpenHands Automation Server that schedules and dispatches work.

**Recommended investigation scope:** SDK + workspace abstraction + Agent Server sandbox boundary. Start with read-only repository inspection and a local deterministic fixture. Compare its workspace/task/event model with MediaHub Task Envelope, Agent Registry, Runner Registry, Evidence Manifest and current controller contracts.

**Explicit exclusions:** do not import OpenHands Automation Server, Agent Canvas or any scheduler/dispatcher as a second control plane. Do not give the agent direct GitHub write, provider-secret, merge, deployment or authority credentials. Agent tools remain least-privilege and task-bound.

The SDK repository advertises MIT licensing; still pin and inspect the exact selected revision and transitive dependencies before any integration. Each OpenHands ecosystem repository has its own license.

### P0 — Open Policy Agent

Repository: https://github.com/open-policy-agent/opa  
Documentation: https://www.openpolicyagent.org/docs  
CNCF maturity: Graduated.

OPA is a general-purpose policy engine using Rego and a query API. It could help make policy decisions deterministic, reviewable and unit-testable across task admission, allowed model/provider routes, data classifications, runner capabilities and artifact acceptance preconditions.

**Recommended investigation scope:** offline policy evaluation in CI against synthetic fixtures; compare Rego input/output contracts to existing MediaHub policy and issuer/capability contracts.

**Explicit exclusions:** OPA must not mint identities, leases, capabilities, signatures or credentials; it must not replace MediaHub Product State Authority, Jarvis or ASTRA A0. MediaHub owns policy source, signed policy release, policy version binding, decision context, fail-closed behavior and audit receipt.

### P0 — Dagger

Repository: https://github.com/dagger/dagger  
Documentation: https://docs.dagger.io/

Dagger offers programmable containerized build/test automation, reusable SDK modules, incremental content-addressed execution and OpenTelemetry traces. It can be called from GitHub Actions and used to reduce drift between local and CI validation.

**Recommended investigation scope:** prototype one non-secret validation task (for example JSON Schema + fixture validation) and compare execution time, reproducibility, cache behavior, auditability and operational cost with the current workflow.

**Explicit exclusions:** Dagger does not replace GitHub Actions, controller admission, task scheduler, provider router, branch protection, release authority or independent review. Do not pass credentials into Dagger during initial qualification. Container runtime, network egress, cache isolation and secret handling require review.

### P0 — Development Containers Specification + CLI

Specification: https://containers.dev/  
Specification repository: https://github.com/devcontainers/spec  
Reference CLI: https://github.com/devcontainers/cli  
CLI documentation: https://code.visualstudio.com/docs/devcontainers/devcontainer-cli

This is the direct follow-up to Waves 490/491. The official CLI supports reading configuration, building and starting environments, running lifecycle commands, and lockfile/frozen-lockfile handling for Features.

**Recommended investigation scope:** validate a candidate `devcontainer.json` without starting it, use lockfiles/frozen lockfiles, pin the image by digest, and map only the Python 3.12 core toolchain first. Keep Python 3.14.7 worker tooling and optional Go/actionlint or transmission-cli tools in separately documented profiles.

**Explicit exclusions:** no secret injection, privileged mode, Docker socket, host networking, broad host mounts, unreviewed lifecycle scripts or unpinned Features. Codespaces remains optional and cost-gated.

### P1 — GitHub Artifact Attestations + SLSA

GitHub documentation: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations  
SLSA framework: https://slsa.dev/  
Attestation action: https://github.com/actions/attest

GitHub artifact attestations bind artifact digests to build provenance, including workflow/repository/environment/commit/event context. GitHub documents SLSA v1.0 Build Level 2 for artifact attestations alone and describes reusable workflows as a route toward Build Level 3.

**Recommended investigation scope:** use a non-production documentation/test artifact in a disposable public-repository fixture; verify attestation identity, source SHA, workflow identity, subject digest and offline verification behavior. Compare this to MediaHub Evidence Manifest and existing Cosign/Syft evidence.

**Plan constraint:** GitHub documents public-repository availability on current plans, while private/internal repositories require GitHub Enterprise Cloud. Reconfirm the exact repository visibility and plan policy at implementation time. No workflow permissions are to be expanded in this research pass.

**Explicit exclusions:** provenance proves where/how an artifact was built, not that it is correct, secure, independently reviewed or accepted.

### P1 — OpenTelemetry Collector

Project: https://github.com/open-telemetry/opentelemetry-collector  
Architecture: https://opentelemetry.io/docs/collector/architecture/  
CNCF maturity: Graduated on 2026-05-11.

The Collector receives telemetry, processes it through pipelines and exports traces, metrics and logs to configured destinations. This is a natural extension of the existing MediaHub OpenTelemetry foundation.

**Recommended investigation scope:** a local-only pipeline with synthetic events, memory limiter, attribute redaction and a single explicitly allowed exporter. Define a MediaHub telemetry schema and correlate controller run/job IDs without logging prompts, tokens, secret values or sensitive user data.

**Explicit exclusions:** telemetry loss must not change command/state behavior; no telemetry backend becomes an authority or mandatory runtime dependency.

### P2 — Temporal (future-gated)

Repository: https://github.com/temporalio/temporal  
Documentation: https://docs.temporal.io/

Temporal provides durable workflow execution. MediaHub already classified it as FUTURE_GATED in component reconciliation 2.3.

**Decision:** do not deploy or integrate now. First demonstrate a specific crash/restart/replay/retry durability gap that cannot be met by existing MediaHub-owned control logic. If such a gap is evidenced, run a bounded comparison against current Task Envelope, Lease, Recovery Record and Evidence Manifest semantics. Do not duplicate canonical state or give Temporal final authorization.

### Not for Contour A default — Actions Runner Controller

Repository: https://github.com/actions/actions-runner-controller  
GitHub docs: https://docs.github.com/en/actions/how-tos/manage-runners/use-actions-runner-controller

ARC is a Kubernetes operator for scaling **self-hosted** GitHub Actions runners. GitHub's docs recommend runner isolation and explain its cluster deployment model.

**Decision:** do not select for the present Cloud Pool. Current Contour A targets GitHub-hosted ephemeral runners and explicitly avoids an owner-operated always-on server/Kubernetes prerequisite. ARC may be reconsidered only for a separately authorized future self-hosted compute contour; it is not a way to manage GitHub-hosted runner capacity.

## 4. Integration order aligned to Contour A

1. **Evidence and policy fixtures:** evaluate OPA offline against synthetic Task Envelope/Capability/ProviderRoute/Quota/Expiry/Revocation fixtures. No runtime authority change.
2. **Provenance:** evaluate GitHub Artifact Attestations/SLSA and compare with current Cosign/Syft release evidence. No production artifact signing changes.
3. **Agent runtime:** inspect OpenHands SDK boundaries and run a harmless read-only sandbox fixture only after exact dependency, tool, workspace and data-policy review. Do not dispatch a live agent.
4. **Build/test repeatability:** compare Dagger against current GitHub Actions for one harmless validation task; do not move controller gates into Dagger.
5. **Developer experience:** use Dev Container CLI to validate candidate configuration after lockfile and base-image provenance decisions are made.
6. **Observability:** evaluate OTel Collector with synthetic data and explicit redaction/export allowlists.
7. **Durable workflow engine:** Temporal only after a measured durability gap.

This order supports the Cloud Pool first priority while preserving the separation between policy, execution, state authority, evidence and acceptance.

## 5. Mandatory qualification template for each candidate

No component is accepted solely because it is popular, CNCF Graduated, used by large organizations or listed in this report. Before implementation, each candidate needs:

- exact upstream repository, immutable commit/tag and release artifact digests;
- license at the selected revision and transitive dependency license review;
- maintainer/security posture, support lifecycle and vulnerability response;
- SBOM and vulnerability scan using the existing approved supply-chain toolchain;
- architecture fit against Baseline 2.0 and existing selected primitives;
- MediaHub adapter/boundary contract and explicit non-authority statement;
- data-flow, secret, identity, capability, network-egress and tenancy threat model;
- resource, concurrency, cost/quota and operational burden estimates;
- positive/negative contract fixtures, failure/degraded-mode and recovery tests;
- rollback/removal plan and independent review;
- exact-head CI evidence and explicit qualification/acceptance status.

Use states: DISCOVERED → RESEARCHED → SHORTLISTED → PINNED → LICENSE_REVIEWED → SECURITY_REVIEWED → INTEGRATED → VERIFIED → QUALIFIED → ACCEPTED. A state must never be skipped by inference.

## 6. Repository and governance status checked

- Repository: `VlDMlNSh/mediahub-os`, public, default branch `main`.
- Main HEAD verified by commit search and compare: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Canonical docs branch `docs/mediahub-chat-tree-map-20261012` verified identical to `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`.
- Issue #301 remains OPEN and prescribes A0/R-06 gates, schema Draft 2020-12 validation, independent review and controlled read-only worker before broader admission.
- PR #605 remains OPEN/DRAFT/UNMERGED. Its exact-head combined statuses and workflow-run query returned empty; reviews were empty. Status is NOT VERIFIED, not PASS.
- PR #604, #603, #601, #600 and #595 remain OPEN/DRAFT/UNMERGED in the checked snapshot. No prior draft was treated as accepted.
- No agent/controller dispatch, provider call, secret access, dependency install, component runtime, workflow dispatch, billing change, merge, deployment, qualification or acceptance occurred in this pass.

## 7. Next bounded research pass

Select the OpenHands SDK and OPA as the two highest-value Contour A candidates for deeper source-level inspection:
- exact pinned upstream commit and release provenance;
- license and dependency manifests;
- workspace/tool isolation and API surface for OpenHands;
- policy bundle, evaluation API, testing and decision-log behavior for OPA;
- map both to existing MediaHub contracts without granting authority;
- produce a candidate-specific threat model and a non-executing integration plan.

Do not install either component or run agent/provider tasks in that pass.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
