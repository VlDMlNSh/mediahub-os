# MediaHub OS — Contour A Component Selection and Parallel-Agent Operating Record — Wave 142

Date: 2026-10-18
Repository: VlDMlNSh/mediahub-os
Documentation ref: docs/mediahub-chat-tree-map-20261012
Functional review ref: main
Status: BOUNDED DESIGN/SELECTION PASS; PROPOSED QUALIFICATION PLAN; NOT IMPLEMENTED / NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED

## 1. Operating decision: chat engineering remains active

The three Gemini agents are supplemental parallel resources, not substitutes for the primary engineering work in this chat. This chat continues to inspect source-of-truth documents, independently verify their claims, choose the next bounded work item, make architecture/component decisions within existing authority, execute tests or repository changes when gates permit, and reconcile the results. Agent completion is not a prerequisite for continued work unless a specific result is a real dependency.

Current SentinelX observation: only Voktors-Mac-mini.local (host_5f7264034bdf0b51, agent 0.22.0) is operational; plan limit is one active slot. mh-dev-01 and mh-dev-02 are disabled by user state. Therefore all three Gemini cloud workflows can run as separate GitHub-hosted workflow jobs, but this does not mean three SentinelX hosts are simultaneously available.

## 2. Live refs and primary sources checked

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Documentation branch HEAD: `72985f282f528c199e8cda2c9cdcd857c29ce0e0`.
- Branches are not assumed interchangeable; no merge/rebase/cherry-pick performed in this pass.
- Canonical Component Manifest 2.0: `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md`, blob `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`, read from `main`.
- ASTRA GOLD Complete Component Scheme: `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md`, blob `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1`, read from `main`.
- ASTRA GOLD Qualification Launch Schema: `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml`, blob `aef6229477ed8ec45e45170f98ea87f7ba75ca29`, read from `main`.
- Component Registry path `components/COMPONENT-REGISTRY.yaml` was requested from `main`; its content was not captured in the final compact output of this pass, so no registry-specific assertion is made here.
- Canonical component manifest explicitly states selection is closed as a development input, while implementation remains open and production admission remains qualification-gated. This pass therefore selects a Contour A implementation/qualification shortlist; it does not reopen or silently rewrite the canonical whole-product selection.

## 3. Component choices for Contour A — proposed shortlist

| Capability | Preferred existing component/surface | Disposition | Why / boundary |
|---|---|---|---|
| Source control, review, workflow dispatch and evidence transport | GitHub repository + GitHub Actions | SELECT FOR CONTINUED QUALIFICATION | Already the project's control/evidence substrate; exact workflow permissions, immutable source SHA, action pins, artifacts and branch protections must still be verified per workflow. GitHub transport is not Product State Authority. |
| Cloud execution capacity | GitHub-hosted ephemeral runners | PREFERRED TARGET CANDIDATE; TARGET NOT ACCEPTED | Fits the stated cloud-development direction without requiring permanent user-server compute for cloud tasks. Exact runner image, egress, isolation, data class, retention, identity, budget and clean-target manifest remain open. |
| Existing owned-host bridge | SentinelX | AUXILIARY DEVELOPMENT BRIDGE ONLY | Currently one operational host and one active slot; not proof of the final cloud executor topology. Do not treat connected test hosts as the accepted deployment target. |
| Parallel model workers | Three bounded Gemini GitHub Actions workflows, with independent source review | SUPPLEMENTAL WORKERS | Each worker must have a task boundary and source SHA. Workflow success validates that workflow's job, not the claims, output, security contract or Contour A qualification. This chat remains the coordinating engineering thread and independently reviews all outputs. |
| Task/agent/evidence schema validation | Existing schema-validation candidate PR #350 / related PR #338 lineage | KEEP AS CANDIDATE; NOT INTEGRATED/ACCEPTED | Historical exact-head schema CI evidence exists for earlier candidate SHAs, but it cannot be carried forward to a different SHA without rerunning. Independent supply-chain review, exact-head evidence and branch reconciliation remain gates. |
| Executor abstraction | OpenHands Software Agent SDK | RESEARCH/ADAPTER CANDIDATE ONLY | Reuse-first option, not the queue, issuer, policy, or Product State Authority. Existing source notes flag the Agent Server's broad workspace access and default network binding as hardening gates. Do not expose it before accepted ingress/workspace/tool/network contracts. |
| Relational persistence and vector retrieval | PostgreSQL + pgvector | CANONICAL MANIFEST TARGET-GATED | Keep one relational authority; no second DB/vector store absent a measured capability gap. Neither is admitted to the runtime merely by selection. |
| Contract transport | Protobuf + gRPC | SELECTED IN MANIFEST; IMPLEMENTATION/QUALIFICATION BY USE CASE | Versioned typed contracts; no authority transfer through transport. Do not introduce a second transport without evidence. |
| Observability | OpenTelemetry Collector + Prometheus | SELECTED IN MANIFEST | Telemetry/metrics only; neither is correctness or product-state authority. |
| Supply-chain evidence | Syft + Cosign + Trivy | SELECTED IN MANIFEST | SBOM, signing/verification and scanning primitives; must be pinned and qualified in the concrete pipeline. |
| Secret/config mechanics | SOPS + age | SELECTED IN MANIFEST | Encryption/config mechanics only; do not place secrets in repository, logs or evidence. Actual runtime secret custody remains a separate gate. |
| Durable queue/workflow engine | Temporal; brokers Redis/Kafka; Kubernetes/K3s | DO NOT ADD BY DEFAULT | Manifest excludes or future-gates them. Add only after a reproducible capability-gap test shows GitHub Actions plus the minimal existing queue cannot meet a required invariant. Kubernetes is not a prerequisite. |
| Local inference runtime | llama.cpp / ONNX Runtime | TARGET-GATED CANDIDATES | Select per model/workload only after exact model provenance, supported hardware, license, resource benchmark, isolation, privacy and recovery evidence. Do not equate these with cloud provider routing. |
| Artifact/object storage | S3-compatible interface | SELECTED INTERFACE; BACKEND OPEN/TARGET-GATED | Preserve replaceable storage implementation and MediaHub-owned recovery/provenance authority; do not select a backend without target and restore tests. |

## 4. Decision rules for the next selection increments

1. Select components by a documented capability gap and source-to-contract crosswalk, not popularity or agent preference.
2. Pin exact repository, version/tag/commit, license, provenance and release artifact before runtime admission.
3. Record each candidate as one of: CANONICAL / SELECTED / TARGET-GATED / FUTURE-GATED / NOT_PROVEN / REJECTED, preserving the manifest's vocabulary.
4. A selected component must not own MediaHub canonical state, authorization, policy, production admission, update/release or recovery authority.
5. No duplicate database, vector store, broker, OTA authority, recovery authority or AI runtime without a measured gap and requalification.
6. Keep Contour B gated until Contour A is deployed and independently accepted.

## 5. Gemini follow-up evidence observed

- Agent 2 follow-up workflow [39113645568](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39113645568): completed/success; produced PR #355 at head `9862df3ade9d7888e9e134fe3f25b08d981e7d3f`. PR is open, no status checks reported by GitHub API in this observation.
- Agent 3 follow-up workflow [39113671012](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39113671012): still in progress at last observation; PR #357 is open at head `6acbc14a8dcce7e2f822861e86dbc7e8fbf0ec1f`, but its workflow-generated checkpoint explicitly says no tests were executed. Treat as static source review only.
- Autonomous Engineering follow-up [39113687269](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39113687269): completed/success; produced PR #356 at head `4fe3b41c763b0e8c929f5ef4a8233939b72fe06e`. PR is open, no status checks reported by GitHub API in this observation.
- The three workflow job successes do not establish PR CI, independent acceptance, live queue behavior, qualification, deployment or production acceptance. The three follow-up PRs remain unmerged. Earlier PRs #352–#354 remain separate candidates and are not treated as accepted facts.
- The agent-3 report correctly labels its work static-only and leaves provider self-promotion NOT_VERIFIED. The agent schema report says no external JSON Schema dialect validator was invoked in its pass. Its claims about queue tests must be re-run at the exact current candidate SHA before being called executed evidence.

## 6. Immediate next actions

1. Independently inspect PR #355 diff and source-to-classification crosswalk against the exact canonical manifest and registry; ensure it does not promote a candidate beyond its declared status.
2. Inspect PR #356 schema pointers, validator invocation and fixture claims against the actual workflow and exact head SHA; do not rely on narrative labels.
3. Inspect PR #357 source line references independently and separate static observations from executed tests.
4. Continue component selection with the smallest Contour A critical path: issuer/ingress + task/agent/evidence contracts + isolated ephemeral runner/workspace + provenance + bounded queue/cancel/recovery. Record concrete upstream choices and unresolved gates per component.
5. Reconcile documentation branch and main only after live diff, exact-head CI, required review/branch-protection and lossless-conflict checks. No integration or deployment is implied by this report.

## 7. Disposition

This is a component shortlist and operating decision record, not implementation or runtime qualification. Contour A remains NOT READY FOR DEPLOYMENT / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. No secrets were accessed; no provider invocation, installation, merge or deployment occurred in this pass.

Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
