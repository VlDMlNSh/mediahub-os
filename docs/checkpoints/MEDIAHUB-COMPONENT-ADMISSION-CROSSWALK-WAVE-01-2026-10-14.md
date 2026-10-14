# MediaHub OS — Component Admission Crosswalk, Wave 01

- Date: 2026-10-14
- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **DOCUMENTARY CROSSWALK / CANDIDATES ONLY / NOT OWNER-APPROVED / NO COMPONENT ADMITTED**
- Roadmap phase: Phase 06 — Component admission and reproducible software bill of materials; prerequisites in Phases 03–04 remain open.
- Purpose: cross-reference the autonomous-agent ecosystem survey with the current canonical component manifest and machine-readable manifest, then define an evidence-backed admission sequence.
- Scope boundary: this report does not modify the canonical manifest, source code, runtime configuration, Baseline 2.0 or any domain contract.

## 1. Live source/ref ledger

| Source | Ref | Blob SHA | Use / status |
|---|---|---|---|
| `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` | `main` | `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | Canonical component-selection input; selection is closed, implementation is open, production admission is qualification-gated. |
| `docs/checkpoints/mediahub-github-component-reconciliation-2.0.md` | `main` | `dd69a8c1c002bbde45944ebdc3d16096d2c9cf07` | Detailed candidate provenance, role and gate rationale. |
| `oss/manifests/components.yaml` | `main` | `7141dd16e9ce9dba3440b1799a56e2ac4da4106d` | Machine-readable, qualification-gated component set. Its precise scope relative to the full selection record requires explicit reconciliation; do not presume omission is either an error or approval. |
| `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` | `main` | `e549692f207fbc91d9b9b9b92b8e665404f07290` | Alamo is the target local inference endpoint/service label; concrete runtime/API/model are not established deployment facts. |
| `runtime/mediahub_runtime/astra_gateway.py` | `main` | `10985e4ad8f682313d08e7492ecc1856a8bce20f` | Survey-reported explicit route-mode field missing from inspected DTO. |
| `runtime/mediahub_runtime/cloud_orchestrator.py` | `main` | `24c28197df7baca49abd81956752a7a5092506d9` | Survey-reported cloud-first ordering and local-extension behavior; static source finding only. |
| `docs/checkpoints/MEDIAHUB-AUTONOMOUS-AGENT-ECOSYSTEM-SURVEY-2026-10-14.md` | `docs/mediahub-chat-tree-map-20261012` | `5c6cd19e338ed0f59823d18718a484f0129d2ef7` | Broader upstream survey and findings MH-ARCH-045 / MH-ARCH-046; candidate-only, not accepted. |
| `docs/checkpoints/MEDIAHUB-OWNER-DECISION-PACKET-01.md` | `docs/mediahub-chat-tree-map-20261012` | `a9f7929f9ac910c3fff1f1fb59f4ee68abf67e42` | DEC-DEV-01…08 remain proposed; DEC-DEV-01 and DEC-DEV-02 directly constrain inference composition and the engineering lifecycle owner. |
| `docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md` | `docs/mediahub-chat-tree-map-20261012` | `84579cf3ca5619721289a03e84797b811781f107` | Work sequencing authority; Phase 06 requires pinned provenance, license/SBOM/security/resource gates and owner-approved justification for new infrastructure. |

### Refs and divergence

- Live `main` HEAD observed: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`.
- Documentation branch HEAD observed before this report: `190e083267b4a9495fbdca484b2b09187bc5b622`.
- Compare result: **DIVERGED**, documentation branch 945 commits ahead and 2 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Do not merge/rebase/cherry-pick to reconcile this difference. This crosswalk is committed only to the documentation branch.

## 2. Findings from comparison

### 2.1 Local inference: runtime references versus component admission

The canonical manifest lists **ONNX Runtime** and **llama.cpp** as target-gated AI candidates. It does not list **Ollama** as a component. The accepted-target architecture names **Alamo** as the local inference endpoint/service label and says runtime/API/model are to be established from deployment evidence. The source survey, meanwhile, identifies an existing Ollama-related executor/route path and records MH-ARCH-045 and MH-ARCH-046.

Disposition: **open representation/traceability gap; Ollama is not admitted by inference**. Keep Alamo (endpoint label), the chosen runtime, API adapter and model identity as distinct fields. Resolve DEC-DEV-01 and route-policy/MH-ARCH-045/MH-ARCH-046 before any local inference runtime is selected or declared ready. Do not install or invoke a runtime under this crosswalk.

### 2.2 Canonical manifest versus machine-readable YAML

The YAML file carries `status: qualification-gated` and a smaller operationally styled component set, including Home Assistant Core as target-gated, inference runtimes as target-gated, and selected foundation mechanics such as Protobuf, gRPC, telemetry, signing, SBOM and vulnerability scanning. The text manifest also describes media whole-product candidates and other future/target-gated components.

The two files may intentionally serve different scopes. This pass does **not** establish that their difference is a defect. Record a bounded documentation task: explicitly declare the YAML’s scope (runtime deployment/admission subset versus complete selection catalogue) and define how its IDs/statuses trace to the text manifest. Do not automatically copy every row into YAML or promote its status.

### 2.3 One worker candidate, not a new controller

The existing survey recommends evaluating the **OpenHands Software Agent SDK** as the first coding-worker candidate, behind an isolated adapter. It is not listed in the canonical component manifest. It must remain CANDIDATE / NOT ADMITTED until a specific capability gap, licence and pinned revision, resource/platform profile, sandbox/tool policy, dependency/SBOM, evidence format, isolation and rollback/removal procedure are reviewed.

Any future worker produces a patch/artifact and provenance; it must not independently merge, release, mutate canonical product state or promote its own qualification. DEC-DEV-02's unresolved Jarvis/ASTRA lifecycle-owner decision and the P0-07/P0-05/P0-04 authorization chain remain upstream gates. No worker evaluation or code was run in this pass.

## 3. Candidate disposition crosswalk

| Candidate / family | Current evidence in project | Crosswalk disposition | Reason / next gate |
|---|---|---|---|
| ONNX Runtime | Canonical manifest §4 and machine-readable YAML | TARGET-GATED (existing) | Must be tied to an approved hardware/model profile, model registry, adapter contract, policy and qualification evidence. No promotion. |
| llama.cpp | Canonical manifest §4 and machine-readable YAML | TARGET-GATED (existing) | Alternative local inference runtime. Benchmark only after a specific workload/hardware gap and separate authorization; do not run beside a duplicate runtime by default. |
| Ollama | Present in survey/runtime-source trace; absent from both current manifest component lists inspected | CANDIDATE / REPRESENTATION GAP | Resolve DEC-DEV-01; explicitly reconcile Alamo endpoint with runtime/API/model and address MH-ARCH-045 and MH-ARCH-046. Absence from manifest means not manifest-admitted. |
| OpenHands Software Agent SDK | Ecosystem survey; absent from manifest | FIRST WORKER CANDIDATE TO REVIEW / NOT ADMITTED | Review exact release/license/transitive deps and sandbox, permissions, data access, task artifact and removal plan. DEC-DEV-02 and trusted-context authorization gates first. |
| OpenHands full platform | Ecosystem survey; broader application surface | REFERENCE / DEFER | Too broad to replace Jarvis/ASTRA absent a demonstrated capability gap; prefer evaluating the smaller SDK if worker reuse is justified. |
| NVIDIA OpenShell | Survey documents upstream maturity-document drift and platform limits; absent from manifest | SECURITY PATTERN / NOT PRODUCTION-ADMITTED | Pin exact release and matching official security/support docs. Survey reports macOS support only on Apple Silicon, which does not establish compatibility for the Intel Mac Pro. Linux worker suitability is a separate hardware/runtime gate. |
| MCP | Survey proposes protocol only; absent from manifest's runtime list | PROTOCOL CANDIDATE / NOT AUTHORIZATION | A tool protocol does not grant trust. Requires per-server allowlists, typed schemas, scoped identity/capability, egress policy, audit, timeout and revocation contracts. |
| LangGraph; Pydantic AI; Microsoft Agent Framework | Survey candidates; absent from manifest | ALTERNATIVES / DEFER | Do not add multiple parallel orchestration/agent frameworks. Consider at most one only if an evidenced adapter/workflow capability gap survives DEC-DEV-02 and owner review. Do not select AutoGen as a new foundation merely because an earlier broad report named it. |
| Temporal | Explicitly future-gated/reference in canonical manifest §5 | FUTURE-GATED | Admit only if authorized evidence demonstrates a material durability/retry/recovery gap that the existing single lifecycle owner cannot meet. Never becomes a second task-state authority. |
| LiteLLM | Survey identifies orchestration/gateway overlap and unclear licence treatment for some paths; absent from manifest | DEFER / NOT ADMITTED | Existing provider routing and data-class policy must be reconciled first. Exact license/path review and owner-approved capability gap are required. |
| Open Policy Agent | Survey: conditional policy-as-code candidate; absent from manifest | DEFER / GOVERNANCE GATED | Do not introduce another policy decision authority while P0-07/P0-05 authorization ownership and contracts remain unresolved. |
| A2A | Survey treats remote agent-to-agent interoperability as future-gated; absent from manifest | FUTURE / NOT REQUIRED NOW | Only reconsider if remote, cross-framework agent interoperability becomes an actual requirement; use typed internal contracts first. |
| Inspect AI / evaluation harness | Survey: evaluation-only candidate | NOT AUTHORIZED IN THIS PASS | Evaluation and tests require separate explicit authorization. Do not install or invoke it here. |
| OpenTelemetry Collector / Prometheus | Selected/current-foundation entries in canonical manifest and YAML | EXISTING FOUNDATION; NON-AUTHORITATIVE | Observability must not become correctness or state authority. Any additional instrumentation package needs a scoped dependency review; do not add another telemetry backend by default. |
| Home Assistant Core | Explicit smart-home authority boundary; YAML marks component target-gated | AUTHORITY BOUNDARY PRESERVED; RUNTIME GATE REMAINS | The architectural authority boundary does not prove any local installation or qualify a runtime. Keep MediaHub/Jarvis/ASTRA from bypassing Home Assistant's domain authority. |

## 4. Admission rule to apply uniformly

No outside-manifest component is READY / SELECTED merely because it is popular, active, locally runnable, or named in a survey. Before admission, record:

1. evidenced capability gap and owner/contract authority;
2. official repository and exact release/tag or immutable commit;
3. exact license and notices for included code and transitive dependencies;
4. upstream provenance, reproducible dependency lock, SBOM and signature/checksum evidence;
5. supported OS/CPU/hardware and measured resource envelope for the actual target;
6. data class, identity, scoped capabilities, tool/server allowlist, network flows and fail-closed behavior;
7. MediaHub-owned adapter/contract and prohibition of competing state/policy/queue/recovery/update authority;
8. negative/degraded/recovery tests and performance benchmarks **after separate authorization**;
9. independent qualification, rollback/removal procedure and explicit owner decision.

Existing selected or target-gated components must retain their exact source-defined status. This crosswalk itself grants no installation, implementation, test, qualification, provider-call, host-inspection, infrastructure-change, deployment or merge permission.

## 5. Bounded next actions

1. Resolve/document the ownership and scope relationship between `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` and `oss/manifests/components.yaml` without silently normalizing either source.
2. Reconcile the Alamo/Ollama/ONNX Runtime/llama.cpp runtime registry with DEC-DEV-01 and existing MH-ARCH-045/MH-ARCH-046 evidence; leave the route-policy and selected-model-identity gaps open until their separately authorized design/review gates are satisfied.
3. Keep OpenHands SDK as the first **paper-evaluation candidate**, not a selected dependency. Map its exact pinned release, license, platform/resources, sandbox and authority boundary only after lifecycle owner and trusted-context prerequisites are addressed.
4. Preserve Temporal, OpenShell, alternative agent frameworks, LiteLLM, OPA, A2A and evaluation harnesses as gated/deferred according to the table above.

## 6. Verification and non-claims

- This report is a documentary crosswalk against live GitHub sources; it is not an exhaustive scan of GitHub or a complete upstream security audit.
- No canonical manifest or runtime code was changed.
- No component was installed, integrated, executed or invoked.
- No tests/evaluations/qualification, model/provider calls, credentials, host/runtime inspection, infrastructure changes, deployment or branch integration occurred.
- No owner decision, architecture acceptance or qualification status was inferred.


## 7.1 Scope reconciliation — text manifest versus YAML admission subset (2026-10-14)

**Status: confirmed scope/traceability ambiguity; not yet proven to be a defect.**

Live source comparison:
- Canonical text selection input on `main`: `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md`, blob `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`. It describes foundation, whole-product sidecars, target-gated candidates, future/reference-gated entries and exclusions; it explicitly calls itself the single component-selection input.
- Machine-readable YAML on `main`: `oss/manifests/components.yaml`, blob `7141dd16e9ce9dba3440b1799a56e2ac4da4106d`. It declares `schema_version: 1` and `status: qualification-gated`, but does not state whether its component list is exhaustive, deployment-scoped, or a subset of the text selection catalogue.
- Reconciliation narrative on `main`: `docs/checkpoints/mediahub-github-component-reconciliation-2.0.md`, blob `dd69a8c1c002bbde45944ebdc3d16096d2c9cf07`, describes selection modes and a broader final implementation set, but the retrieved evidence does not establish a normative YAML-to-text-manifest mapping rule.

Observed differences include absent text-manifest entries in YAML (for example Jellyfin, Music Assistant, Snapcast and several whole-product candidates), differing status vocabulary (`SELECTED` / `TARGET-GATED` / `FUTURE-GATED` versus `current-foundation` / `target-gated`), and Home Assistant Core appearing in YAML despite not being a row in the text manifest's component tables. Some differences may be intentional scope differences; they must not be normalized by inference.

**Required disposition:** owner/governance should choose and document one of:
A. YAML is the exhaustive machine-readable projection of the text manifest, with stable IDs, mapping rules and parity checks; or
B. YAML is a narrower runtime/deployment-admission subset, with an explicit scope declaration, source-of-truth relationship, and traceability rules for omitted entries/status translation.

Recommendation: B is less disruptive if YAML is intended only for runtime/deployment admission, but this remains a proposal, not an accepted decision. Until decided, neither file is automatically rewritten; no status is promoted, no component is admitted, and no test/CI/qualification run is implied. Next safe documentary step is to prepare a concise owner decision record and map the exact parity/status semantics; do not implement the YAML schema change before approval.


## 7.2 OpenHands SDK source-pin preflight (2026-10-14)

**Disposition: NOT READY for a package-level paper-evaluation; candidate remains NOT ADMITTED.** This pass verified upstream repository identity and current release metadata, but did not establish the exact SDK distribution/version or its complete dependency licence boundary.

- The official repository formerly addressed as `All-Hands-AI/OpenHands` redirects to `OpenHands/OpenHands`. Official repository page: https://github.com/OpenHands/OpenHands.
- GitHub's latest release endpoint currently identifies monorepo tag `v1.27.1`, targeting commit `f07aebdf5cdd71f4a05ebcf30f8bef5e4e3b70b9`, published 2026-10-12. The release metadata reports `immutable: false`; therefore this tag alone is not an immutable supply-chain pin.
- The repository-root `LICENSE` is MIT. This establishes the root repository's displayed license only; it does **not** establish the license of every SDK subdirectory, optional package, transitive dependency, container image or separately distributed artifact.
- The official Model Context Protocol Python SDK repository is `modelcontextprotocol/python-sdk`; the latest-release endpoint returned `v2.3.0` (published 2026-10-02), and its root LICENSE is MIT. This is protocol SDK metadata, not evidence that MCP provides authorization or that this exact version is compatible with MediaHub.
- Upstream metadata and licence pages were inspected read-only. No package was installed, imported, executed or copied; no tests, sandbox experiment, security assessment or compatibility evaluation was performed.

**Required before advancing:** identify the exact OpenHands SDK package name and official package/repository path; pin a release and immutable commit or artifact digest; inspect package-specific license/notices and transitive dependency metadata; establish supported OS/CPU and sandbox model; map every tool/network/filesystem capability to Contour A's task-scoped authorization, human approval, egress, audit, cancellation and artifact-only return contracts. The worker must not own queue/lease lifecycle, canonical product state, policy, merge/release or qualification promotion. MCP must remain an interface protocol behind MediaHub-owned authorization.

**Recommendation:** do not choose the OpenHands monorepo tag as an SDK pin. Continue as research only until exact SDK identity and the owner-approved capability gap are established. No component manifest or owner decision is changed by this note.


## 7.3 Owner decision — YAML is a scoped admission subset (2026-10-14)

**Decision status: OWNER-CONFIRMED in conversation on 2026-10-14.**

The owner selected option B: `oss/manifests/components.yaml` is a **runtime/deployment admission subset**, not an exhaustive projection of the canonical text component-selection manifest.

Applied to the documentation branch:
- Declared `scope: runtime-deployment-admission-subset`.
- Linked the source of truth to `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` at `main`.
- Declared `status_semantics: admission-readiness-only`.
- Declared `omission_semantics: omission-does-not-imply-exclusion`.

The source text manifest remains the component-selection catalogue. YAML statuses must not be treated as a lossless translation of text-manifest modes, and YAML omission must not be interpreted as EXCLUDED. This change clarifies scope; it does not admit or qualify any component and does not establish runtime readiness.

**Branch boundary:** YAML edit was committed only to `docs/mediahub-chat-tree-map-20261012`. The same path on `main` remains unchanged because the branches are diverged; no merge/cherry-pick or main-branch deployment was performed. The branch change is therefore documented and read-back verified, but is not yet present on `main`.

**Verification:** read-back of `oss/manifests/components.yaml` on the documentation branch returned blob SHA `e3cf487bcf43ecb92cd110b5af2660c066b58e2a`. No tests, CI, qualification or runtime execution were run.
