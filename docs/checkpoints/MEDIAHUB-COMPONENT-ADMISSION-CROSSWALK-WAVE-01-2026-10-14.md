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


## 7.4 OpenHands SDK package-specific source and artifact pin (2026-10-14)

**Disposition: exact source/package/artifact identity now identified; still CANDIDATE / NOT SELECTED / NOT ADMITTED.** This addendum narrows the earlier open identity question in §7.2. It is a paper review only, not a package installation, import, execution, sandbox experiment, security assessment or qualification.

### Upstream identity and immutable-content references

- Canonical upstream repository: [OpenHands/software-agent-sdk](https://github.com/OpenHands/software-agent-sdk), distinct from the umbrella [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) monorepo.
- Release: [v1.54.0](https://github.com/OpenHands/software-agent-sdk/releases/tag/v1.54.0), published 2026-10-09. GitHub release metadata reports `immutable: false`; do not use a mutable tag/release pointer alone as supply-chain pin.
- Release commit: `1d471742ea7be017d013eaaa3080f5d28d5490cb`; GitHub commit API reports a valid verified signature. Pin the full commit SHA for source review, not the tag name alone.
- Distribution: [PyPI openhands-sdk 1.54.0](https://pypi.org/project/openhands-sdk/1.54.0/). The wheel is `openhands_sdk-1.54.0-py3-none-any.whl`, SHA-256 `647bf83c888bc544b0500480aa8a89729f44f6db9f93ea3ba43cfc7fdf070db3`. The source distribution `openhands_sdk-1.54.0.tar.gz` SHA-256 is `431e7bc66ac5caf3a426e25bc67d3a85d5036ace61ff2c20af5a62ea16650485`. These hashes identify specific artifacts; they do not by themselves establish publisher identity, safety or dependency-license closure.
- PyPI release metadata says Trusted Publishing was **not** used for this upload. Record this as a provenance weakness to assess, not as proof of a malicious or invalid artifact.
- The repository-root LICENSE is MIT at the inspected commit. Full transitive license closure has **not** been established. The source tree includes `uv.lock`, but the complete lock was not reviewed in this pass; an official root `SECURITY.md` was not found at the inspected root path. This does not assert that no security processes or other policy documents exist.

### Package footprint and MediaHub fit

- `openhands-sdk` version `1.54.0` declares `requires-python >=3.12`. Contour A's actual target Python versions are UNKNOWN in this documentary pass; no host/runtime inspection was performed. Do not claim target compatibility until an authorized, approved node profile proves it.
- The SDK package directly requires `litellm>=1.93.0`, `fastmcp>=3.2.0,<4`, `fakeredis[lua]>=2.32.1`, `agent-client-protocol>=0.12.1,<0.13.0`, and additional libraries including httpx, jsonschema, joserfc, pydantic, websockets, tree-sitter and lmnr. This creates a material dependency/licensing and routing-policy review obligation because LiteLLM was previously deferred as a standalone gateway candidate. A library dependency is not itself approval to run a second gateway or relax MediaHub route policy.
- The separate `openhands-agent-server` package adds Docker, FastAPI, SQLAlchemy, OpenAI SDK and server/storage/API dependencies. Its deployment would have a larger operational and network surface. Do not include Agent Server by default; a sandboxed workspace/server is a separate design choice that needs an evidenced capability gap and security/egress review.
- Upstream README describes both direct/local workspace use and ephemeral workspaces (for example Docker/Kubernetes) through Agent Server. Local workspace access can touch the workspace and configured tools; upstream features do not replace MediaHub's task-scoped authorization, filesystem/network boundaries, human approval, audit, cancellation or result verification.
- The source repo is active and unarchived, and the root license is MIT, but neither fact substitutes for exact wheel/source provenance, dependency SBOM, vulnerability/license review, node compatibility, network/telemetry audit or independent qualification.

### Admission decision and remaining gates

1. Treat `openhands-sdk==1.54.0` at source commit `1d471742ea7be017d013eaaa3080f5d28d5490cb` and wheel SHA-256 above as a **research pin only**, not as a selected product dependency.
2. Before any admission, review all dependency licenses and hashes from a complete lock/SBOM, publisher/provenance evidence, security advisories, supported OS/runtime versions, actual CPU/RAM envelope, tool default capabilities, telemetry, filesystem/network effects and offline/local-only routing behavior.
3. Obtain the owner decision on whether accepting this SDK's direct LiteLLM dependency is compatible with the existing provider-routing decision. Resolve DEC-DEV-02 (single Jarvis/ASTRA engineering lifecycle owner) and P0-07/P0-05/P0-04 trusted-context/authorization requirements before allocating any privileged worker capability.
4. If subsequently authorized for implementation evaluation, the first design target should be an isolated worker producing a patch/artifact plus source provenance. It must not own queues/leases/retries, Product State Authority, policy, merge/release, or its own qualification promotion. Any install, model/provider call, sandbox run, test/evaluation, qualification, host inspection or deployment needs separate explicit authorization.

**Result:** source/package/artifact identity is sufficiently specific for a further paper review, but the candidate is **NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**. No dependency was admitted, no component manifest or normative contract was changed, and no runtime/test/security execution occurred.


### 7.5 Supply-chain and security-process paper review (2026-10-14)

**Evidence scope:** immutable source commit `1d471742ea7be017d013eaaa3080f5d28d5490cb`, root workspace `pyproject.toml`, `openhands-sdk/pyproject.toml`, GitHub release metadata for `v1.54.0`, root `LICENSE`, and `.github/workflows/security-scan.yml`. No artifact was downloaded; no dependency resolver, scanner, test, or package code was executed.

| Check | Read-only evidence | Finding / status |
|---|---|---|
| Source identity | Official repo `OpenHands/software-agent-sdk`; v1.54.0 points to commit `1d471742ea7be017d013eaaa3080f5d28d5490cb` | Exact source identity known; release metadata says `immutable: false`. |
| Root license | Root `LICENSE` declares MIT | Upstream project license is identifiable. This is not a transitive dependency license conclusion and does not itself authorize admission. |
| Python compatibility | SDK metadata says `requires-python >=3.12` | MediaHub Contour A's approved Python/OS profile remains unknown; compatibility is unproven. |
| Lockfile | Repository tree contains a workspace `uv.lock` | A lockfile exists at the upstream repository root. This pass did not retrieve/parse the full lock or verify all transitive hashes/licenses; do not label the SBOM or license closure complete. |
| Direct dependency conflict | SDK directly requires `litellm>=1.93.0`; upstream workspace constraints pin `litellm==1.93.0` | Material governance gate: MediaHub has not admitted LiteLLM as an independent provider gateway. Decide whether a subordinate SDK dependency is acceptable, and prove that it cannot override MediaHub-owned route/data-class policy. |
| Additional direct dependencies | `fastmcp>=3.2.0,<4`, `fakeredis[lua]>=2.32.1`, `agent-client-protocol>=0.12.1,<0.13.0`, `lmnr>=0.7.60,<0.8.0`, plus HTTP, schema, crypto/JWT, parsing and telemetry-related libraries | Dependency/licensing/network/telemetry review remains open. LMNR is an observability vendor integration candidate; no telemetry or provider call was made. |
| Security workflow | Upstream `.github/workflows/security-scan.yml` describes an OSV/dependency and approval-drift scan; non-release PR scans are opt-in via label or manual dispatch, while release PRs are gated | Evidence of a repository security process, not evidence that this exact release passed a scan. No workflow run or result was inspected in this pass. |
| Security policy | Root `SECURITY.md` was not present at the inspected source path; GitHub Security page was previously observed to report no detected policy | Treat as a disclosure-process evidence gap, not proof of a vulnerability or absence of all security practices. |
| Published artifacts | GitHub release `v1.54.0` exposes platform-specific agent-server binaries and `SHA256SUMS`; release marked mutable | Checksums help identify published files but do not prove local bytes or source-to-artifact provenance. PyPI metadata previously showed Trusted Publishing was not used for this upload. |
| Operational scope | `openhands-sdk` is the core package; `openhands-agent-server` is a separate package with Docker/API/storage dependencies | Keep the server package out of the candidate scope by default. A worker design must explicitly bound filesystem access, subprocesses, network egress, credentials, resource use, cancellation and artifact export. |

**Current conclusion:** the evidence supports a better-scoped research pin, not admission. The upstream repository's security workflow is not equivalent to a verified release attestation; presence of `uv.lock` is not a completed SBOM; MIT at the root does not settle transitive licensing; and a checksum in metadata is not local checksum verification.

**Owner decision needed before further advancement:** choose one of:
- **A — Reject/defer OpenHands SDK** until MediaHub's own controller/lifecycle and local-only routing contracts are closed.
- **B — Continue paper review only** of `openhands-sdk==1.54.0`, with an explicit decision on its LiteLLM/FastMCP/LMNR dependency footprint; no installation or execution.
- **C — Authorize a separately scoped implementation-evaluation plan** only after Contour A authority, target runtime, egress/sandbox and dependency-review gates are resolved. This option is not implied by this document.

No option has been selected by this review. No component manifest, code, lockfile, dependency or normative contract changed.


## 7.6 Exact lock resolution and conditional telemetry boundary (2026-10-14)

**Scope:** supplemental read-only source/metadata trace at SDK source commit 1d471742ea7be017d013eaaa3080f5d28d5490cb. This extends §7.5; it does not close the complete SBOM, licence, provenance, or security review.

### Resolved direct-dependency snapshot

The upstream workspace lock resolves the selected SDK dependencies as follows:

| Package | Version in uv.lock | Evidence observed |
|---|---:|---|
| litellm | 1.93.0 | Lock records source and wheel SHA-256 values; official PyPI metadata identifies MIT. |
| fastmcp | 3.2.0 | Lock records source and wheel SHA-256 values; official PyPI metadata identifies Apache-2.0. |
| fakeredis | 2.34.1 | Lock records source and wheel SHA-256 values. The BSD-3-Clause metadata found during this pass was for 2.32.1, not the locked 2.34.1; exact-version licence remains unverified. |
| agent-client-protocol | 0.12.1 | Lock records source and wheel SHA-256 values; the reviewed PyPI metadata reports Trusted Publishing was not used. Exact-version licence remains unverified in this pass. |
| lmnr | 0.7.60 | Lock records source and wheel SHA-256 values; official PyPI project metadata identifies Apache-2.0. |

This is a small sample of the lockfile, not a complete dependency inventory. A complete locked dependency/SBOM export, per-package licence and notice review, advisory review, and source-to-artifact provenance analysis remain open. No dependency was installed or downloaded and no scanner/resolver was run.

### Telemetry and execution-boundary trace

- At the pinned source commit, the SDK invokes maybe_init_laminar() from the agent module. The initializer skips setup when recognized observability environment variables are absent; LMNR_PROJECT_API_KEY or configured OTEL endpoints can enable instrumentation. The source documents LMNR_BASE_URL with default https://api.lmnr.ai and supports selecting instrumented integrations. This proves a configurable egress path exists in source; it does not prove telemetry was active in MediaHub.
- The same source imports LiteLLM in the core LLM implementation. Therefore LiteLLM is an actual direct provider abstraction dependency, not only a separately deployable optional gateway. Any future use must remain subordinate to MediaHub-owned provider/data-class routing and cannot establish a parallel route authority.
- The SDK's LocalWorkspace executes commands in the host environment. The Agent Server README says it binds to 0.0.0.0 by default and has access to its configured workspace. The AgentSandboxWorkspace documentation places network egress allow-listing in Kubernetes NetworkPolicy and describes optional gVisor/Kata runtime classes. These are upstream configuration features, not evidence of a secure deployment or a qualified MediaHub sandbox.

### Disposition and next gate

OpenHands remains **RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**.

Before any admission proposal:
1. Obtain an owner/governance decision on the direct LiteLLM dependency and document that it cannot override MediaHub routing policy.
2. Complete exact-version licensing/provenance for all direct dependencies and generate/review a complete locked-dependency SBOM plus vulnerability/advisory evidence.
3. Define explicit telemetry policy, allowed egress, disposable worker isolation, least-privilege filesystem mounts, credential isolation, cancellation/resource limits, human approval and artifact-only output.
4. Preserve DEC-DEV-02 and P0-07/P0-05/P0-04 authorization gates. No install, execution, model/provider call, tests, sandbox evaluation, qualification, host inspection, infrastructure change or deployment is authorized by this review.

No component, runtime, manifest, or normative contract was admitted or changed.


## 7.7 Exact-version license, publisher provenance and advisory cross-check (2026-10-14)

**Scope:** read-only review of official PyPI release pages and official upstream repository metadata for the two remaining direct dependencies identified in §7.6. No artifact download, resolver, scanner, test, import, or execution was performed.

| Dependency | Exact-version evidence | Provenance / security-process evidence | Disposition |
|---|---|---|---|
| fakeredis 2.34.1 | Official PyPI page for 2.34.1 explicitly reports SPDX License Expression BSD-3-Clause. The sdist SHA-256 is `4ff55606982972eecce3ab410e03d746c11fe5deda6381d913641fbd8865ea9b`. | PyPI reports Trusted Publishing used; attestation points to `cunla/fakeredis-py@de4e72482402534ac0add5258f3afa9877bf61e5`, tag `v2.34.1`, workflow `publish-pypi.yml`. This is publisher provenance shown by PyPI, not a locally verified artifact hash or a complete dependency security review. | Exact-version license and publication provenance are better evidenced; artifact bytes were not downloaded/verified. |
| agent-client-protocol 0.12.1 | Official PyPI release page exposes exact sdist and wheel hashes: sdist `9963ccb590ed96d7dc542c9c023e90676fc76b1c6562e21a9ee112f4fbcb0095`; wheel `aaf3cc301ed87d9e2c4ccb91adfe1cd58784355f6ce7e513f50e7ca2391862ef`. The official upstream Python SDK repository identifies its license as Apache-2.0, but this review did not establish version-attested license metadata for the exact 0.12.1 distribution. | PyPI reports Trusted Publishing was not used for 0.12.1. The official upstream ACP repository's Security page reports no detected SECURITY.md policy and no published advisories at the time reviewed. This is an evidence gap, not proof of a vulnerability or absence of all security practices. | Exact package hashes known; exact-version artifact license and source-to-artifact provenance remain OPEN. Do not treat the upstream repository license alone as full artifact attestation. |

### Updated gate assessment

- The previous §7.6 statement that fakeredis 2.34.1's exact-version license was unverified is superseded by the official PyPI metadata above: BSD-3-Clause is now evidenced for that release.
- agent-client-protocol 0.12.1 remains less well evidenced: no Trusted Publishing, exact release hashes available, but artifact-specific license/provenance closure is incomplete. The upstream repository's Apache-2.0 license is useful context but is not, by itself, a verified license statement for every published package artifact.
- No claim is made that either dependency is vulnerable. The ACP repository's lack of a detected security policy and lack of published advisories are observations about public evidence only.
- Complete transitive SBOM/license closure, comprehensive advisory assessment, OpenHands release/source-to-artifact provenance, target runtime compatibility, telemetry/egress and sandbox review remain open. The direct LiteLLM dependency still requires an owner/governance decision against MediaHub's single provider-routing authority.
- **Disposition unchanged:** OpenHands SDK remains RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION. No dependency was admitted, downloaded, installed, imported or executed; no tests/scans/model/provider calls/qualification/host inspection/infrastructure/deployment occurred.


## 7.8 OpenHands release provenance and security signal (2026-10-14)

**Scope:** bounded, read-only review of the official PyPI page for `openhands-sdk==1.54.0`, official GitHub release metadata and upstream Security page, plus one publicly reported security-related issue. No artifact was downloaded, and no package code, scanner, test or resolver was executed.

| Evidence | Verified observation | Interpretation / limit |
|---|---|---|
| PyPI distribution identity | The official release page lists `openhands_sdk-1.54.0-py3-none-any.whl` SHA-256 `647bf83c888bc544b0500480aa8a89729f44f6db9f93ea3ba43cfc7fdf070db3` and sdist SHA-256 `431e7bc66ac5caf3a426e25bc67d3a85d5036ace61ff2c20af5a62ea16650485`. | Hashes identify the expected published artifacts; because bytes were not downloaded, this pass did not independently recompute the hashes. |
| Publication provenance | PyPI states Trusted Publishing was **not** used for either file; uploader metadata reports `uv/0.12.24` on Ubuntu 24.04 with CI marked true. | Publisher workflow/source-to-artifact binding is weaker than a verified Trusted Publishing attestation. This is a provenance risk, not proof of tampering. |
| GitHub source/release | Release `v1.54.0` points to commit `1d471742ea7be017d013eaaa3080f5d28d5490cb`; GitHub reports the commit signature as verified/valid. Release metadata says `immutable: false`. | Source commit identity is supported; mutable release metadata and absent PyPI Trusted Publishing mean the published wheel is not cryptographically proven to derive from that commit by the evidence gathered here. |
| Public security process | Official [OpenHands Software Agent SDK Security page](https://github.com/OpenHands/software-agent-sdk/security) says no security policy is detected and no published GitHub advisories are listed at review time. | Public repository configuration only; this is not proof of no vulnerabilities or absence of private/internal security handling. |
| Historical security-related report | Public issue [#4157](https://github.com/OpenHands/software-agent-sdk/issues/4157) described a concern that an LLM security analyzer could trust model self-assessed risk and allow actions classified LOW without human confirmation; it is marked closed as not planned. | Treat as a review lead, not a confirmed vulnerability in v1.54.0. Applicability to the pinned commit and actual configuration has not been verified. MediaHub must not delegate authorization to model-produced risk labels. |
| Optional Agent Server binaries | The v1.54.0 GitHub release exposes platform binaries with release-provided SHA-256 digests, but this review did not download or verify any binary. | Agent Server is not required for the SDK candidate and remains excluded from the candidate scope unless a documented capability gap justifies it. |

### Admission implications

- Require independent artifact digest verification and source-to-artifact provenance evidence before any approved evaluation; do not infer wheel provenance solely from a signed source commit.
- Any future worker integration must have an external, deterministic MediaHub authorization gate. LLM-produced risk labels, prompts, tool descriptions or worker self-assessments cannot grant permission or bypass human approval.
- Preserve task-scoped capabilities, explicit filesystem/network boundaries, egress deny-by-default, credential isolation, cancellation/resource ceilings, audit logs and artifact-only output. These are required design gates, not claims that the SDK enforces them automatically.
- **Disposition unchanged:** RESEARCH PIN ONLY / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION. Complete dependency SBOM/licence/advisory review, target runtime proof, sandbox/egress review and the owner decision on the direct LiteLLM dependency remain open. No runtime action is authorized.


## 7.9 FastMCP 3.2.0 exact-version advisory and provenance check (2026-10-14)

**Scope:** read-only review of the official PyPI release page for `fastmcp==3.2.0` and upstream GitHub security advisories. No artifact was downloaded, unpacked, executed, or independently re-hashed.

| Evidence | Observation | Interpretation / limit |
|---|---|---|
| Exact package/license | Official PyPI release page identifies FastMCP 3.2.0, Apache Software License classifier, wheel SHA-256 `e71aba3df16f86f546a4a9e513261d3233bcc92bef0dfa647bac3fa33623f681`, and sdist SHA-256 `d4830b8ffc3592d3d9c76dc0f398904cf41f04910e41a0de38cc1004e0903bef`. | Release identity and declared license metadata are source-observed; artifact bytes and complete license-notice contents were not independently verified. |
| Publication provenance | PyPI reports Trusted Publishing was used for both wheel and sdist, with upload metadata naming `uv/0.11.2` and CI. | This is stronger publisher evidence than a non-attested upload, but this pass did not independently validate the attestation bundle or rebuild the artifacts. |
| GHSA-vv7q-7jx5-f767 / CVE-2026-32871 | Upstream advisory lists affected FastMCP versions as `<3.2.0` and patched version `3.2.0`; issue concerns SSRF/path traversal in OpenAPIProvider. | The pinned version is the stated patched floor, not within the published affected range. This does not establish safety of other code paths or configuration. |
| GHSA-m8x7-r2rg-vh5g | Upstream advisory lists affected versions as `<3.2.0` and patched version `3.2.0`; issue concerns Windows command injection in subprocess-backed installer commands. | The pinned version is the stated patched floor. MediaHub must not rely on the advisory alone; avoid invoking FastMCP installer commands and preserve the external execution boundary. |
| Advisory coverage | Public upstream advisory listings contain additional findings with distinct affected-version ranges and feature/configuration prerequisites. | A version-specific advisory match is not a complete SBOM scan. The full transitive graph and every advisory's applicability remain unreviewed. |

**Gate disposition:** no confirmed applicable advisory for the two reviewed issues is established against the exact `3.2.0` pin, because upstream lists that version as patched. The candidate still remains **RESEARCH PIN ONLY / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**. Complete transitive SBOM/licence/advisory closure, independently verified artifact provenance, sandbox/egress evidence, target runtime compatibility, and owner disposition on LiteLLM/provider-routing authority remain open. No tests, scans, installation, package execution, provider calls, qualification, host inspection, infrastructure change, or deployment occurred.

## 7.10 agent-client-protocol 0.12.1 exact-tag license/provenance cross-check (2026-10-14)

**Scope:** read-only review of official PyPI release metadata and the exact upstream source commit identified by the official GitHub release page. No package was downloaded, unpacked, installed, imported, executed or independently re-hashed.

| Evidence | Observation | Interpretation / limit |
|---|---|---|
| Exact PyPI artifact identity | PyPI lists sdist SHA-256 `9963ccb590ed96d7dc542c9c023e90676fc76b1c6562e21a9ee112f4fbcb0095` and wheel SHA-256 `aaf3cc301ed87d9e2c4ccb91adfe1cd58784355f6ce7e513f50e7ca2391862ef`. | Published checksums identify expected files; artifact bytes were not downloaded or independently hashed. |
| Publication method | PyPI reports Trusted Publishing was **not** used; upload metadata lists `uv/0.6.14` for both distributions. | There is no PyPI Trusted Publishing attestation tying these artifacts to a source commit in the evidence reviewed. This is a provenance gap, not evidence of tampering. |
| Upstream release identity | Official GitHub release page lists version 0.12.1 at commit `e668ed9` and displays the commit signature as verified. The exact commit's `pyproject.toml` declares version `0.12.1`; the same commit contains an Apache License 2.0 `LICENSE` file. | The source tag/version and repository license are evidenced. The package metadata in that source `pyproject.toml` does not itself declare a license field. Because Trusted Publishing was not used and artifact bytes were not inspected, this does **not** prove the published wheel/sdist were built from that exact commit or that their embedded notices match the source tree. |
| Public security-process signal | The upstream Python SDK Security page reports no detected security policy and no published advisories at review time. | Public repository configuration only; it is not proof that the package has no vulnerabilities or that all relevant advisories were assessed. |
| Source dependency metadata | The exact source commit declares Python `>=3.10,<3.15` and direct runtime dependency `pydantic>=2.7`; optional `logfire` and `http` extras are present. | This helps scope the source package, but does not replace review of the complete locked/transitive graph and the separately resolved OpenHands environment. |

### Updated gate assessment

- The prior open question is narrowed: the exact upstream source revision for 0.12.1 contains an Apache-2.0 license file, and the official release page identifies a signed commit. This is stronger than relying only on the current repository's license badge.
- **Artifact-specific license/provenance is still OPEN**: PyPI did not use Trusted Publishing, artifact bytes and embedded license/notice files were not inspected, and source-to-artifact binding was not independently established.
- No vulnerability conclusion is drawn from the absence of published advisories or a detected security policy.
- **Disposition unchanged:** OpenHands SDK remains **RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**. Complete transitive SBOM/licence/advisory closure, independently verified artifact provenance, target runtime and sandbox/egress evidence, and owner disposition on the direct LiteLLM/provider-routing boundary remain open. No install, package execution, tests/scans, provider calls, qualification, host inspection, infrastructure change or deployment occurred.


## 7.11 LMNR 0.7.60 exact-source, telemetry and provenance review (2026-10-14)

**Scope:** read-only review of the exact upstream tag/commit, its project metadata and license, plus the OpenHands SDK lock rationale. No package or artifact was downloaded, installed, imported, executed or independently hashed; no scanner, resolver, test, telemetry or provider call was run.

| Evidence | Observation | Interpretation / limit |
|---|---|---|
| Locked dependency | The OpenHands SDK lock snapshot resolves `lmnr==0.7.60`; §7.6 records it as a direct dependency. | This is an upstream SDK dependency, not a MediaHub selection or authorization to enable telemetry. |
| Exact source identity | Official `lmnr-ai/lmnr-python` tag `0.7.60` resolves to commit `67dea392f4961bfcf7b5cde3733aaa4a452bb9f9`. The official release page says v0.7.60 was published 2026-08-22 and is not immutable. | Record the full commit as the source-review anchor; a mutable release/tag pointer alone is not a durable supply-chain guarantee. |
| Source license/runtime metadata | At that exact commit, `pyproject.toml` declares package `lmnr` version `0.7.60`, SPDX-style `Apache-2.0`, `LICENSE`, and Python `>=3.10,<4`. The commit contains the Apache-2.0 license text. | Exact source version and repository license are evidenced; this does not by itself prove published artifact bytes, embedded notices or full transitive license closure. |
| Release rationale | The official v0.7.60 release notes describe a fix for LiteLLM streaming usage/reasoning telemetry. | The dependency is materially connected to observability/telemetry behavior; its presence must not be interpreted as permission to transmit prompts, content, secrets or product data. |
| Published artifact provenance | Exact PyPI 0.7.60 wheel/sdist hashes and Trusted Publishing attestation were not independently established in this pass. Other LMNR release pages do not establish provenance for 0.7.60. | Artifact-specific source binding and hashes remain OPEN; do not infer them from neighboring releases or current upstream main. |
| Data-flow boundary | The OpenHands source reviewed in §7.6 calls an LMNR initializer conditionally and documents API-key/OTEL configuration and an LMNR endpoint. | A configurable outbound telemetry path exists in the reviewed source; this is not evidence telemetry was active in MediaHub. |

### Gate disposition

- LMNR 0.7.60 has a source-level Apache-2.0 license and exact source commit anchor, but artifact provenance, transitive SBOM/license/advisory closure and target behavior remain incomplete.
- Any future evaluation must explicitly disable telemetry by default, deny outbound egress unless separately approved, prohibit secrets/private prompts/product data from telemetry, and verify these controls externally. Environment variables or worker configuration are not themselves a MediaHub authorization boundary.
- OpenHands remains **RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**. This review admits no component and does not resolve the separate owner/governance decision on LiteLLM/provider-routing.
- No installation, artifact download, execution, test/scan, provider call, qualification, host inspection, infrastructure change or deployment occurred.


## 7.12 LiteLLM 1.93.0 exact-version advisory gate (2026-10-14)

**Scope:** read-only review of official PyPI metadata and official upstream GitHub security advisories for the exact LiteLLM 1.93.0 version resolved in the OpenHands SDK lock snapshot described in §7.6. No artifact was downloaded, and no package code, scanner, resolver, test or proxy was executed.

| Evidence | Exact observation | Boundary / implication |
|---|---|---|
| Official PyPI release | [LiteLLM 1.93.0](https://pypi.org/project/litellm/1.93.0/) declares MIT, Python >=3.10,<3.15, Trusted Publishing for the listed sdist/wheels. Sdist SHA-256: `140bf215e264c71601bca9c06d2436c5451bb59e1e195ea23fc2d3d87b6929ec`; CPython 3.12 manylinux x86_64 wheel SHA-256: `0784172435de48f66ef7ad89d421604db1ad0db1321ef7f39dbcfe6b20111417`. | Published metadata provides exact artifact identity and publisher provenance signal; artifact bytes were not downloaded/rehashed and this does not prove source-to-artifact equivalence. |
| GHSA-3cv6-jpf6-8222 | [Official upstream advisory](https://github.com/BerriAI/litellm/security/advisories/GHSA-3cv6-jpf6-8222) lists `>=1.93.0, <1.93.2` as affected for authenticated SSRF/provider-credential exfiltration through proxy request-body routing; patched line starts at 1.93.2. | Exact pin 1.93.0 is within the published affected range. Advisory impact is described for the LiteLLM Proxy path; reachability when LiteLLM is used as an SDK-side provider abstraction rather than a deployed proxy is **not established** by this paper review. |
| GHSA-7hp6-4w63-5g45 | [Official upstream advisory](https://github.com/BerriAI/litellm/security/advisories/GHSA-7hp6-4w63-5g45) lists `>=1.91.0, <1.100.4` as affected for privilege escalation to proxy admin; it says versions later than 1.91.0 are exploitable in the default configuration. | 1.93.0 falls in the published affected range. Feature/deployment reachability in the SDK-only consumption model remains unverified. |
| GHSA-g5ff-637f-6q2m | [Official upstream advisory](https://github.com/BerriAI/litellm/security/advisories/GHSA-g5ff-637f-6q2m) lists all versions below 1.95.0 as affected by authenticated proxy local-file read through `vertex_ai_credentials`. | 1.93.0 falls in the published affected range. Do not infer this proxy endpoint is exposed in MediaHub; runtime topology and call-path reachability are not inspected or evidenced. |

**Security disposition:** three official advisory ranges include the exact upstream LiteLLM pin. This is a material dependency-admission blocker, **not** a claim that MediaHub is exploitable or that the advisory-specific proxy endpoints are reachable through the OpenHands SDK's ordinary provider-call path. The exact dependency is used as a direct provider abstraction in the reviewed SDK source; owner/governance must decide whether to reject/defer the candidate, or request a separately scoped, source-only reachability review before any admission. Do not upgrade the pin, edit manifests, install, execute, or select LiteLLM as a provider-routing authority in this pass.

**Candidate status unchanged:** OpenHands remains RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION. Full transitive SBOM/licence/advisory closure, source-to-artifact verification, target runtime, sandbox/egress, P0-07/P0-05/P0-04 gates and owner decision on LiteLLM/provider-routing remain open. No artifact download/install/execution, tests/scans/provider calls, qualification, host inspection, infrastructure change or deployment occurred.


## 7.13 fakeredis 2.34.1 exact-version public advisory signal (2026-10-14)

**Scope:** bounded read-only review of the official PyPI release metadata, the upstream v2.34.1 release/source commit, public upstream security information, and public search results for an exact-version advisory signal. No package/artifact was downloaded, and no scanner, resolver, test, import or execution was performed.

| Evidence | Observation | Interpretation / limit |
|---|---|---|
| Exact release identity | Official PyPI metadata for [fakeredis 2.34.1](https://pypi.org/project/fakeredis/2.34.1/) declares BSD-3-Clause, lists sdist SHA-256 `4ff55606982972eecce3ab410e03d746c11fe5deda6381d913641fbd8865ea9b`, and reports Trusted Publishing. | The published release metadata and publisher signal are evidenced; the artifact bytes were not downloaded or independently re-hashed. |
| Upstream source anchor | Official [v2.34.1 release](https://github.com/cunla/fakeredis-py/releases/tag/v2.34.1) points to commit `de4e72482402534ac0add5258f3afa9877bf61e5`; GitHub reports that commit signature as verified. The release notes list bug fixes for deprecated Redis client arguments and blocking XREAD behavior. | This anchors a signed source release and a narrow change summary; it does not prove every published artifact was independently rebuilt from that source in this review. |
| Public advisory search | A bounded search of official upstream security/release surfaces and public search results did not surface a published advisory specifically matching fakeredis 2.34.1. The upstream repository exposes a Security Policy. | This is a limited negative search result, not proof of no vulnerabilities, no private reports, or a complete advisory-database/SBOM scan. |
| Scope caveat | The OpenHands lock reviewed in §7.6 includes the `fakeredis[lua]` extra. This pass did not independently assess the complete transitive closure or all optional-feature paths, including the Lua runtime dependency. | No whole-package or whole-environment security clearance is implied. |

**Disposition:** no exact-version public advisory match was established in this bounded paper review. This is not a finding that fakeredis 2.34.1 is vulnerability-free and does not close the OpenHands dependency gate. Complete locked transitive SBOM, license/notice and advisory closure, artifact verification, sandbox/egress and target-runtime evidence remain open. OpenHands remains **RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**. No artifact download/install/execution, tests/scans/provider calls, qualification, host inspection, infrastructure change or deployment occurred.


## 7.14 ACP Python SDK 0.12.1 cancellation/lifecycle issue signal (2026-10-14)

**Scope:** bounded read-only review of the exact ACP Python SDK dependency already recorded in §7.6–§7.10, its public GitHub security page, release index, and a public lifecycle issue. No package/artifact was downloaded; no code, tests, scanner, resolver or runtime was executed.

| Evidence | Observation | Interpretation / limit |
|---|---|---|
| Public security page | The official ACP Python SDK repository's Security page currently reports no detected SECURITY.md policy and no published GitHub advisories. | This is repository UI evidence only; it does not establish that the package is vulnerability-free or that private reports/advisories do not exist. |
| Lifecycle issue | Public issue [#108](https://github.com/agentclientprotocol/python-sdk/issues/108) reports that cancelling run_agent during AgentSideConnection.listen() could leave sender/dispatcher tasks running because connection close was not guaranteed in a finally path. The search result marks the issue closed by #113. | This is a concrete asynchronous lifecycle/resource-cleanup signal, not a published security advisory. The issue/result alone does not prove whether the fix is present in exact release 0.12.1 or whether MediaHub exercises this path. |
| Version/source boundary | The reviewed exact upstream release 0.12.1 is anchored in §7.10 to commit e668ed9; the public release index shows subsequent releases exist. | Do not infer the fix's inclusion/exclusion in 0.12.1 without comparing the fixing commit and tag ancestry. No runtime reachability or fix-in-pin claim is made here. |
| Admission relevance | ACP is a direct dependency in the reviewed OpenHands SDK lock snapshot. | Keep lifecycle/cancellation behavior as an unresolved dependency-review item. A separate source-only commit/tag comparison is the next evidence step if permitted; no pin change or runtime test is authorized. |

**Disposition:** no published advisory match was established from the reviewed public Security page, but this is not a security clearance. The cancellation issue is a source-review lead requiring exact fix-to-tag traceability. Exact artifact/source provenance, full transitive SBOM/license/advisory closure, and target runtime/sandbox/egress evidence remain open. OpenHands stays RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION. No download, installation, test, scan, execution, provider call, qualification or infrastructure change occurred.


## 7.15 ACP Python SDK 0.12.1 — cancellation fix traceability (2026-10-14)

**Question reviewed:** Is the cancellation cleanup fix for issue #108 included in the exact upstream release 0.12.1?

- Official issue #108 documents that cancelling `run_agent()` could bypass connection cleanup and leave sender/dispatcher tasks pending. This is the reported issue description, not a finding that MediaHub currently reaches the affected path.
- Official PR #113 is marked merged on 2026-06-29; it closes #108 and identifies merge commit `fe643ab`. The PR page shows the change title `fix: close run_agent connection on cancellation`.
- Official release notes for 0.11.0, dated 2026-07-05, explicitly list fix #113. Official 0.12.1 release notes identify source commit `e668ed9` and follow 0.12.0/0.11.0 in the release line. This is strong release-history evidence that the fix predates 0.12.1 and is included in the published release lineage; this pass did not independently fetch Git objects or run a commit-ancestry comparison.
- **Disposition:** the earlier uncertainty is narrowed: release notes support inclusion in 0.12.1, but exact Git ancestry was not independently verified in this source-only pass. Do not call this a confirmed MediaHub runtime defect or a security clearance. Runtime reachability remains unknown.
- Evidence: https://github.com/agentclientprotocol/python-sdk/issues/108 ; https://github.com/agentclientprotocol/python-sdk/pull/113 ; https://github.com/agentclientprotocol/python-sdk/releases/tag/0.11.0 ; https://github.com/agentclientprotocol/python-sdk/releases.
- No artifact download, install, code execution, tests, pin change, provider call, qualification, host/runtime inspection or infrastructure change occurred.


## 7.16 OpenHands Software Agent SDK — current upstream identity and execution-boundary refresh (2026-10-15)

**Scope:** documentary-only refresh of the canonical upstream repository and its public project/development description. No package/artifact was downloaded, no code was executed, and no tests, scanners, dependency resolution, provider/model calls or host inspection were performed.

| Evidence | Observation | Interpretation / limit |
|---|---|---|
| Canonical upstream identity | Official upstream is [OpenHands/software-agent-sdk](https://github.com/OpenHands/software-agent-sdk). Its README describes Python, TypeScript and REST APIs; the repository owns the Python SDK and Agent Server, while automation scheduling/dispatch belongs elsewhere. | This confirms the candidate identity and clarifies component ownership. It does not admit the SDK or make it a corporation-wide task authority. |
| Execution/workspace model | The official README explicitly says agents may use the local machine as workspace or run in ephemeral workspaces, for example Docker/Kubernetes, through Agent Server. | SDK use does not inherently imply isolation. MediaHub must select and evidence a concrete workspace/executor profile; do not grant direct access to a developer host or product state by default. |
| Development and tests | Official DEVELOPMENT.md documents build/setup and pytest commands. | These are upstream instructions only. They were not run; no compatibility or test result is claimed. |
| Current source pin | The review surfaced the mutable upstream `main` page, but this pass did not establish an immutable current commit SHA or bind a published package artifact to a source commit. | Do not treat mutable `main` as a reproducible admission pin. The previously reviewed lock snapshot remains historical evidence only and must not be silently promoted to a current compatible pin. |
| Security/supply chain | Existing §§7.6–7.15 record dependency-specific observations and unresolved issues, including FastMCP/LiteLLM version-specific advisory review, ACP cancellation history, LMNR telemetry boundary, fakeredis optional Lua path, artifact provenance and transitive closure gaps. | The new upstream identity/workspace facts do not close any dependency or security gate. A lack of a surfaced advisory is not a security clearance. |

**Updated gate assessment:** OpenHands Software Agent SDK remains **RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**. Required before reconsideration: (1) immutable upstream source commit and exact package/artifact pin with source-to-artifact provenance; (2) full locked transitive SBOM, license/notice and advisory closure; (3) target OS/Python/runtime compatibility evidence; (4) an explicit isolated workspace/sandbox profile with filesystem, process, network/egress, credential, resource and cancellation controls; (5) owner disposition on direct LiteLLM/provider-routing boundaries; and (6) separate authorization for any installation or test. MediaHub's deterministic authorization/evidence gate must remain outside the candidate worker; MCP/tool declarations or agent-generated assessments are not authorization.

**Next:** keep this source-only review in the existing crosswalk. Do not create a duplicate candidate record, change dependency pins, install, execute, test, scan or qualify the SDK in this pass.


## 7.17 OpenHands Software Agent SDK — exact release pin and deployment-boundary delta (2026-10-15)

**Status:** SOURCE-REVIEW UPDATE ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NO RUNTIME AUTHORIZATION.

### Immutable source anchors checked

| Upstream artifact | Ref / immutable identity | Evidence and limit |
|---|---|---|
| Official release | `OpenHands/software-agent-sdk@v1.54.0`; release commit `1d471742ea7be017d013eaaa3080f5d28d5490cb` | Official release page identifies v1.54.0 as latest and shows the release commit with GitHub “Verified” signature status. This is a source/release anchor, not a verified package artifact digest or complete source-to-wheel provenance. |
| SDK package metadata | `openhands-sdk/pyproject.toml@v1.54.0`, blob SHA `39c3ce3b1137c59e6a24423a3d11097f446507ee` | Declares package version 1.54.0 and Python `>=3.12`. Dependency constraints include ACP `>=0.12.1,<0.13.0`, FastMCP `>=3.2.0,<4`, LiteLLM `>=1.93.0`, Pydantic `>=2.13.5`, and LMNR `>=0.7.60,<0.8.0`; several dependencies are lower-bounded rather than exactly locked here. Full transitive lock/SBOM and target compatibility are not established by this file. |
| SDK README | `README.md@v1.54.0`, blob SHA `386dc8945133cb51969192b0b29c8396719cbff6` | Describes Python/TypeScript/REST interfaces and both local-machine workspaces and ephemeral workspaces through Agent Server. The SDK does not inherently provide a safe isolation boundary; MediaHub must select and evidence one. |
| Agent Server README | `openhands-agent-server/openhands/agent_server/README.md@v1.54.0`, blob SHA `a64ff0840230ff5ae2d7c167c824048eaf72da9f` | Describes REST/WebSocket endpoints and local filesystem storage. Quick-start documents default bind host `0.0.0.0`; session API-key authentication is described as optional. These defaults are **not acceptable as a MediaHub deployment profile by assumption**. Any later evaluation must explicitly bind to a justified interface and require approved authentication, network/egress controls, workspace isolation and data-retention policy. No server was launched. |
| Upstream license | `LICENSE@v1.54.0`, blob SHA `b0bd86a6335a564bd3766666bebbf014fd6a8013` | Repository-level license text is MIT. This does not establish the licenses/notices of every transitive dependency, optional extra, container image or model/provider. |

### Reconciled assessment

1. The candidate now has a concrete upstream release/source pin: v1.54.0 at commit `1d471742ea7be017d013eaaa3080f5d28d5490cb`. Do not confuse this with a fully pinned installable artifact: wheel/sdist digest, build provenance, complete dependency lock and SBOM remain OPEN.
2. Python `>=3.12` is an explicit compatibility prerequisite. The new target OS/Python profiles are not yet proven, so compatibility remains UNKNOWN.
3. SDK and Agent Server must be treated as separable choices. The SDK is not automatically admitted with its server. If the server is considered later, its documented `0.0.0.0` bind and optional API-key defaults require an explicit hardened deployment profile; no network reachability or session key alone substitutes for MediaHub application authorization.
4. The SDK declares a direct LiteLLM dependency and an LMNR tracing dependency. Provider identity/egress and telemetry privacy must be independently closed; local-only routes must fail closed, and telemetry must not export sensitive prompts, source or secrets.
5. Workspace isolation is a hard gate: no direct developer-host workspace, unrestricted shell/filesystem/network, central credentials, or product-state mutation. Agent output remains untrusted data and cannot authorize, publish, verify its own work, or bypass the MediaHub authorization/evidence gates.

### Gate status after this source pass

- Exact upstream release/source revision: **SOURCE-PINNED** (v1.54.0 / commit above).
- Published package digest and source-to-artifact provenance: **OPEN**.
- Complete locked transitive SBOM, license/notice closure and current advisory review: **OPEN**.
- Python/OS/hardware compatibility: **UNKNOWN / OPEN**.
- Workspace and Agent Server hardening profile: **OPEN**.
- LiteLLM route identity, egress and fail-closed local-only behavior: **OPEN**.
- LMNR/telemetry collection, redaction, retention and egress: **OPEN**.
- Runtime installation, testing, scanning, qualification, selection and admission: **NOT PERFORMED / NOT AUTHORIZED**.

Official upstream evidence: [release v1.54.0](https://github.com/OpenHands/software-agent-sdk/releases/tag/v1.54.0), [SDK metadata](https://github.com/OpenHands/software-agent-sdk/blob/v1.54.0/openhands-sdk/pyproject.toml), [SDK README](https://github.com/OpenHands/software-agent-sdk/blob/v1.54.0/README.md), [Agent Server README](https://github.com/OpenHands/software-agent-sdk/blob/v1.54.0/openhands-agent-server/openhands/agent_server/README.md), [license](https://github.com/OpenHands/software-agent-sdk/blob/v1.54.0/LICENSE).

No package/artifact was downloaded, no code was executed, and no tests, dependency resolution, security scan, provider/model call, credential use, host/runtime inspection, qualification or infrastructure change occurred. The source review is not a security clearance and does not admit the candidate.

## 7.18 Pydantic direct-dependency constraint and release-provenance boundary (2026-10-15)

**Scope:** source-only review of the OpenHands SDK v1.54.0 dependency declaration and official Pydantic release/security surfaces. No artifact was downloaded, dependency resolved, scanner or test run, package imported, or runtime/provider/host accessed.

| Evidence | Observation | Interpretation / limit |
|---|---|---|
| Consumer dependency declaration | OpenHands SDK v1.54.0 `openhands-sdk/pyproject.toml` declares `pydantic>=2.13.5` (source blob already pinned in §7.17: `39c3ce3b1137c59e6a24423a3d11097f446507ee`). | This is a lower bound, not an exact resolved dependency pin. The declaration alone does not identify the actual installed version, transitive `pydantic-core` version, artifact hashes or full lock closure. |
| Release history | Official Pydantic release history lists v2.13.5 (2026-08-28), v2.14.0 (2026-10-08) and v2.14.1 (2026-10-11). v2.13.5 release notes describe several fixes; v2.14.1 release notes describe further fixes. | Multiple releases exist above the declared lower bound. This demonstrates version drift potential, not that any particular version is resolved or preferred for MediaHub. No pin change is proposed. |
| Public security surface | The official `pydantic/pydantic` Security page exposes a security policy and, at review time, no published advisories on the reviewed page. | This bounded public-page observation is not a vulnerability-free conclusion, does not cover every transitive dependency or private report, and is not a substitute for a complete advisory/SBOM review. |
| Artifact provenance | This pass did not independently establish exact PyPI artifact hashes, attestations, source-to-artifact binding or a complete locked dependency graph for the version that OpenHands would resolve. | Artifact-level provenance and reproducibility remain OPEN. Source release metadata is not a lockfile or an SBOM. |

### Disposition

- Pydantic remains an **unresolved transitive/direct dependency-admission gate** for the OpenHands research candidate: declared lower bound is known, exact resolution and complete lock/SBOM are not.
- Do not infer that v2.13.5 or v2.14.1 is the selected dependency; do not edit pins or manifests from this source-only review.
- Before any candidate admission, obtain an immutable complete lock for the chosen target profile; identify exact `pydantic` and `pydantic-core` artifacts, hashes, license notices, source/provenance and advisory coverage; then reconcile compatibility with the approved Python/OS target.
- OpenHands remains **RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**. No install, artifact download, dependency resolution, tests/scans, provider/model call, credentials, host/runtime inspection, qualification or deployment occurred.

Official source references: [OpenHands SDK v1.54.0 dependency metadata](https://github.com/OpenHands/software-agent-sdk/blob/v1.54.0/openhands-sdk/pyproject.toml); [Pydantic release history](https://github.com/pydantic/pydantic/releases); [Pydantic security page](https://github.com/pydantic/pydantic/security).


## 7.19 OpenHands workspace guardrails — target-profile and lock-evidence boundary (2026-10-15)

**Scope:** source-only inspection of the exact OpenHands Software Agent SDK v1.54.0 release commit `1d471742ea7be017d013eaaa3080f5d28d5490cb`, specifically the workspace-root `pyproject.toml` and SDK package metadata. No dependency resolution, package download, installation, test, scan or execution occurred.

| Evidence | Observation | Interpretation / limit |
|---|---|---|
| SDK package requirements | `openhands-sdk/pyproject.toml`, blob SHA `39c3ce3b1137c59e6a24423a3d11097f446507ee`, declares Python `>=3.12` and lower-bounded dependency ranges including `pydantic>=2.13.5`, `litellm>=1.93.0`, `fastmcp>=3.2.0,<4`, and `lmnr>=0.7.60,<0.8.0`. | Package metadata does not alone determine a reproducible resolved environment. Prior §§7.9–7.18 record several dependency-specific unresolved gates; this pass does not close them. |
| Workspace-level guardrails | Root `pyproject.toml`, blob SHA `2da88a5a9f278947e6c6978ff0e0c398f27515d5`, configures Python 3.13 for type checking, `exclude-newer = "7 days"`, and explicit constraints including `litellm==1.93.0`. | These are upstream workspace build/resolution settings, not an accepted MediaHub target profile or proof of the exact package environment. The LiteLLM pin is already within the published advisory ranges recorded in §7.12; do not treat the workspace guardrail as an override of that blocker. |
| Intel macOS conditional | The same root file constrains `cryptography<49` when `sys_platform == 'darwin' and platform_machine == 'x86_64'`, with an upstream comment that v49.0.0 dropped x86_64 macOS wheels. | This proves the upstream workspace accounts for an Intel-macOS packaging boundary. It does not establish that the MediaHub target hardware is Intel, Apple Silicon, or compatible with this candidate. Target hardware/OS/Python facts remain owner-input blockers. |
| Lockfile evidence | The connector returned the `uv.lock` path with blob SHA `5a4afacc446005f7c02c9606390847e73c4c9208` but returned an empty content payload for both UTF-8 and base64 fetches. | This retrieval is insufficient to inspect lock contents or prove lock absence. Do not infer resolved versions or reproducibility from the empty payload; retrieve/verify the exact lock content through a reliable source before using it as evidence. |

### Gate disposition

- Upstream workspace guardrails are now source-observed, but **they are not a MediaHub target lock** and do not establish artifact-level provenance, complete SBOM/license/advisory closure, target compatibility, or runtime isolation.
- The exact resolved `pydantic`/`pydantic-core` versions and complete target-specific lock remain OPEN. The LiteLLM 1.93.0 advisory blocker remains OPEN; no pin or upstream file was changed.
- OpenHands remains **RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**.
- No normative project source, manifest, dependency pin or runtime configuration was changed. No tests, downloads, installs, provider/model calls, credentials, host/runtime inspection, qualification, deployment or branch integration occurred.

**Next:** choose another non-overlapping unresolved admission gate only after checking existing sections, or wait for owner-provided target hardware/OS/Python facts. Do not infer a target profile or start runtime evaluation.


## 7.20 OpenHands SDK live upstream revision and security-policy surface refresh (2026-10-16)

**Scope:** read-only revalidation of upstream package metadata at the already recorded v1.54.0 pin, the current upstream `main` package metadata, repository license, lockfile retrieval, and security-policy surface. No dependency resolution, download, scan, installation, execution, test or runtime evaluation occurred.

| Evidence | Observation | Interpretation / limit |
|---|---|---|
| Pinned SDK metadata | `OpenHands/software-agent-sdk@v1.54.0`, `openhands-sdk/pyproject.toml`, blob SHA `39c3ce3b1137c59e6a24423a3d11097f446507ee`, declares package version `1.54.0`, Python `>=3.12`, and lower-bounded dependency ranges including `pydantic>=2.13.5`, `litellm>=1.93.0`, `fastmcp>=3.2.0,<4`, and `lmnr>=0.7.60,<0.8.0`. | This is source metadata at the pinned tag, not an artifact digest, resolved environment or MediaHub target lock. |
| Moving upstream main | `openhands-sdk/pyproject.toml@main`, blob SHA `160610fcba9b379a10340f16ab77c3bf504f2609`, declares version `1.55.1`, Python `>=3.12`, and `pydantic>=2.13.5`. | Do not substitute moving `main` for the immutable v1.54.0 pin. Any future revision change requires an explicit re-review of source, artifact and dependency evidence. |
| Comparison tag | `openhands-sdk/pyproject.toml@v1.50.1`, blob SHA `ab83f196c70a0732cff40b6d616a730a83db9b2d`, declares version `1.50.1` and `pydantic>=2.12.5`. | The dependency floor varies by version; this is further evidence that the exact revision must be pinned rather than inferred from the repository name or current branch. |
| License | `LICENSE@v1.54.0`, blob SHA `b0bd86a6335a564bd3766666bebbf014fd6a8013`, contains MIT License text. | This confirms the upstream repository license text only. It does not close notices, optional modules, transitive dependency licenses or redistribution obligations for a resolved artifact. |
| Lockfile | `uv.lock@v1.54.0` resolves to blob SHA `5a4afacc446005f7c02c9606390847e73c4c9208`, but the connector again returned an empty content payload. | Lock contents and resolved versions remain UNVERIFIED; empty retrieval is not evidence that the lockfile is absent. |
| Security policy | The pinned ref has no readable root `SECURITY.md` at that path; the upstream GitHub Security overview reports “No security policy detected” and no published advisories at the time it was viewed: https://github.com/OpenHands/software-agent-sdk/security. | Absence of a published policy/advisory is not evidence of absence of vulnerabilities. Require independent dependency/advisory review and a documented MediaHub vulnerability-response path before admission. |

### Gate disposition

- **Candidate status unchanged:** RESEARCH PIN ONLY / CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION.
- Open: immutable package artifact and digest; source-to-artifact provenance; readable exact lock and resolved dependency set; transitive SBOM/license/advisory closure; target OS/Python/hardware fit; isolated workspace profile; provider/egress controls; telemetry privacy; independent security review.
- No component manifest, normative contract, upstream pin, dependency or runtime configuration changed. No test, scan, artifact download, installation, provider/model call, credential use, host/runtime inspection, qualification, deployment or branch integration occurred.

**Next:** do not repeat the same source-pin review. Continue only with a distinct unresolved admission gate or wait for owner-provided target hardware/OS/Python facts. Runtime evaluation remains blocked.


## 7.21 Open Policy Agent (OPA) — source-pin and authority-boundary preflight (2026-10-16)

**Scope:** read-only source inspection of the official `open-policy-agent/opa` repository at upstream commit `fdf6011f57fdc25f01de1982e296bb402cf37625`. Inspected README, LICENSE, go.mod and SECURITY.md by immutable commit ref. No OPA binary, package or source was downloaded, built, installed or executed; no policy was evaluated and no scanner/test/runtime/provider/host action occurred.

| Evidence | Observation | MediaHub interpretation |
|---|---|---|
| Upstream identity and pin | Official repository: https://github.com/open-policy-agent/opa; source commit `fdf6011f57fdc25f01de1982e296bb402cf37625`. README blob SHA `860399b5b7ac265f89508796831990a45eb485c4`. | Immutable source reference for paper evaluation only; not a release selection or a binary/artifact pin. |
| Function and integration | README blob describes OPA as a general-purpose policy engine and its example as a service asking OPA for an allow/deny decision. It points to Go SDK and REST API integration. | Potentially reusable as a policy decision point (PDP). MediaHub's deterministic enforcement point must authenticate the request, validate context and apply the decision. OPA must not become identity issuer, capability issuer, workflow/lifecycle authority or Product State Authority. |
| License | `LICENSE` blob SHA `8f71f43fee3f78649d238238cbde51e6d7055c82` contains Apache License 2.0 text. | Preliminary license signal only; binary distribution, notices and complete dependency licensing remain unreviewed. |
| Build/runtime requirement signal | `go.mod` blob SHA `bb894fcce89f7f52f72d2a174711172a660451e0` declares Go `1.26.0`. | The source branch's Go requirement is not a target compatibility finding. Contour A target OS, toolchain and deployment mode are UNKNOWN; no toolchain installation or build is authorized. |
| Security process | `SECURITY.md` blob SHA `ffc134070059b814cd9061cf50cdc3a866b186d6` directs reporters to the official OPA security policy. | A published reporting route is present in source; this does not replace an advisory review, threat model or MediaHub vulnerability-response process. |
| Policy/evidence controls | The source preflight did not evaluate policy bundle signatures, policy revision pinning, decision-log content/privacy, API authentication, transport protection, outage behavior or policy-update rollback. | All remain open. Unknown, malformed, stale or unavailable policy decisions must not silently authorize privileged actions. Fail-closed behavior must be enforced and tested by MediaHub-owned boundary contracts, not inferred from the existence of OPA. |

### Candidate disposition

- **OPA: RESEARCH-CANDIDATE / SOURCE-PINNED FOR PAPER REVIEW ONLY / NOT SELECTED / NOT ADMITTED / NOT IMPLEMENTED / NOT QUALIFIED.**
- **Potential fit:** policy decision support for task-scoped authorization only if a demonstrated gap exists in the accepted MediaHub authorization contracts.
- **Do not duplicate authority:** existing MediaHub issuer, trusted-context, capability and Product State Authority contracts remain controlling. OPA output is an input to an enforcement decision, not a grant of authority by itself.
- **Open gates:** owner-approved capability gap; exact release/artifact digest and source-to-artifact provenance; full dependency/license/SBOM/advisory review; policy ownership/signing/versioning/rollback; authenticated and bounded input schema; fail-closed behavior; decision-log privacy/retention; API/network/egress design; target OS/toolchain/resource fit; independent security review; separate authorization for any build, install or test.
- No architecture or owner decision was changed. This preflight does not recommend adding OPA alongside an existing accepted policy/enforcement mechanism unless a concrete gap is documented.

**Next:** continue source-only inventory of a distinct shortlisted candidate only if it addresses a separate unresolved capability; otherwise wait for owner disposition on policy authority and target-profile gates. Do not install, build, evaluate policies or run tests without separate authorization.


## 7.22 Temporal Python SDK + Temporal Server — durable-execution fit and authority-boundary preflight (2026-10-16)

**Owner direction:** The owner explicitly confirms the user-authored MediaHub master prompt in this conversation as the project direction. This confirms the architectural direction and workflow priorities; it does **not** select or admit Temporal, approve a second workflow/state authority, or establish target runtime facts.

**Scope:** read-only source inspection of official upstream repositories at immutable commit refs. No source/binary download, build, installation, runtime evaluation, workflow execution, tests, credentials, host/runtime inspection or deployment occurred.

| Evidence | Observation | MediaHub interpretation |
|---|---|---|
| Python SDK source | Official repository: https://github.com/temporalio/sdk-python; inspected commit `346d4dcd0863657c3a33283c952a296762059339`. README blob `81d40696956098ae2ec62695bef46076e41b30ef`; `pyproject.toml` blob `f803404db6d065deec6575daafac6480a12cb0d8` declares package version `1.34.0`, Python `>=3.10`, and MIT license; LICENSE blob `c7f1b9e7e809f4134614fdd5bd1b00c5e3a8df87`. | The inspected commit's package metadata identifies 1.34.0, but this pass did not establish an immutable release tag or a wheel/sdist digest. A request for ref `v1.34.0` returned no matching commit; do not treat the inspected moving-branch commit as an admitted release pin. |
| SDK role | README describes Temporal as a durable, scalable workflow engine and the Python SDK as the framework for authoring workflows and activities. | Plausible substrate for long-running/recoverable activity execution, but not proof that MediaHub needs it. ASTRA A0 already has lifecycle/queue authority contracts under reconciliation. |
| Server dependency | Official server repository: https://github.com/temporalio/temporal; inspected commit `dcd360f177a1238c6f7c59ef5889613b7e243a03`. README blob `d89e30ebb9863ea82c9203e1e696170ea9484af9`; LICENSE blob `3349f76795f4409cba6ae18ea56adf9fbd8346f3` contains MIT license text; `go.mod` blob `1bc4ab1e6cd4eac8a5aee1c07d7b2a8f86b91fad` declares Go `1.27.0`. | The SDK is not a self-contained durable execution service. A server, persistence, operational monitoring, backup/recovery and security profile would need separate evaluation. The source branch's Go requirement is not target compatibility evidence; Contour A OS/toolchain/topology remain UNKNOWN. |
| Security policy source | Root `SECURITY.md` was not found at either inspected repository ref. | This is only a source-path observation, not a conclusion that no security process or vulnerabilities exist. Advisory history, supported release policy, transitive SBOM and vulnerability response require independent review. |
| Architecture boundary | Temporal's workflow execution primitives may overlap with ASTRA queue, retry, cancellation, durable lifecycle and recovery responsibilities. | If considered later, Temporal must be a bounded execution substrate under ASTRA-owned mission/authority contracts, not a second canonical mission registry, Product State Authority, capability issuer or competing owner of accepted task lifecycle. No dual-queue design is implied. |

### Candidate disposition and open gates

- **Temporal Python SDK + Server: FUTURE-GATED / SOURCE-PINNED FOR PAPER REVIEW ONLY / NOT SELECTED / NOT ADMITTED / NOT IMPLEMENTED / NOT QUALIFIED.** This is consistent with the existing component register's `FUTURE-GATED` status.
- **Potential value:** durable execution/recovery for long-running activities, but only if an evidenced lifecycle/recovery requirement cannot be met by the accepted ASTRA A0 design without duplicating its authority.
- **Required before any selection:** owner-approved gap statement; comparison against ASTRA A0 queue/lifecycle/recovery contracts; supported release/tag and exact SDK/server artifact digests; source-to-artifact provenance; dependency/SBOM/license/advisory closure; persistence and backup/recovery design; worker trust/isolation and credential/egress boundaries; server authentication/TLS and data retention; operational footprint and target hardware/OS/toolchain fit; failure, cancellation, retry and idempotency semantics; independent review.
- Do not choose both Temporal and Hatchet by default. Compare only if durable execution is established as a distinct required capability.
- No owner architecture decision was changed; no runtime activity was performed.

**Next:** retain Temporal as a future-gated candidate. Do not proceed to installation or runtime evaluation. First reconcile the accepted ASTRA lifecycle/queue contracts and determine whether a specific durable-execution gap exists; otherwise do not add a second orchestration engine.


## 7.23 ASTRA lifecycle/recovery contract versus Temporal — gap-discrimination pass (2026-10-16)

**Status:** SOURCE-BOUND CONTRACT RECONCILIATION / DOCUMENTARY ONLY. No component selection, implementation, runtime qualification or acceptance.

### Source basis and limits

| Source | Ref/blob evidence | What it establishes | What it does not establish |
|---|---|---|---|
| ASTRA Executor Capability Matrix | `main`, blob `da26185254d9954fcee204f81ecca129bf052e7c`; docs-branch counterpart `9ad83781a8da53d1a8f540ede54eba95281f01c0` | ASTRA-internal dependency-aware dispatch, executor admission/binding, queue/claim/lease/heartbeat/recovery and evidence/gate ownership; source wording differs between refs. | A single branch-integrated contract, runtime conformance, accepted Jarvis-facing ingress, or a corporation-wide durable mission service. |
| ASTRA GOLD Governance Contract | `main`, blob `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Internal policy bounds: heartbeat 120 s, lease 600 s, executor timeout 900 s, result publication timeout 120 s, retry backoff 30 s, maximum 3 concurrent autonomous claims; human creation authority and audit/rotation/revocation requirements. | External request TTL, capability expiry, idempotency retention, proof of an operational queue, or target-hardware compatibility. |
| ASTRA GOLD Reference Architecture | `main`, blob `7be5fadd3055642e7823c7233f90e978a87e5366` | Architecture-level responsibilities include command ingestion, mission decomposition, queue/claim/lease, heartbeat, duplicate-controller rejection, stale-claim detection, result publication and recovery; ambiguous broad authority wording is separately tracked. | Accepted Jarvis→A0 API/issuer lifecycle, complete external state mapping, or runtime evidence that recovery is implemented and works. |
| Jarvis/ASTRA Identity-Lifecycle Contract Trace Wave 05 | docs branch, blob `dc60ccc0af29a74ca3cf88584d66821350b20b9f` | Ingress, capability issuer/delegation/revocation lifecycle, corporation task/result envelope and authority wording remain open/draft-only; ASTRA internal lifecycle requirements are bounded and source-backed. | Admission of Temporal or proof that it closes any of those external contract gaps. |
| WB-14AA / WB-14AC | docs branch, blobs `030273bfe9fd6d44e78b611c011af95d08c88a45` / `d642311d5a487981b6ba79eeb1a49abbb26fd4d3` | Proposal-level ingress semantics include durable admission, idempotency, fencing, cancellation, uncertain-commit reconciliation, result/evidence separation; evidence/qualification boundaries are documented. | Normative acceptance, selected transport/issuer/persistence, or completed implementation/qualification. |
| Temporal source review §7.22 | docs branch crosswalk preceding section | Temporal SDK + server is a potential durable-execution substrate with additional server/persistence/operational requirements. | Evidence that a distinct durability gap remains after the accepted ASTRA lifecycle design is reconciled, or that Temporal would close ingress/security/schema gaps. |

### Gap discrimination

1. **Existing design coverage:** ASTRA sources already describe the internal engineering lifecycle at architecture/policy level, including queue/claim/lease/heartbeat, bounded retry, cancellation/recovery, stale-claim handling, result publication and evidence/gate state. The governance numeric limits are internal controls; they must not be copied as external API/token/idempotency TTLs.
2. **Unproven implementation/runtime:** these documents do not prove the current queue implementation is conformant, reliable, deployed on the new target, or qualified. No runtime claim is made here.
3. **External contract gap:** accepted Jarvis→A0 ingress, trusted caller/issuer/verifier lifecycle, durable external admission/idempotency semantics, corporation task/result/evidence envelope, and owner/approval workflow remain open. Temporal does not itself resolve those authority and interface decisions.
4. **New target boundary:** legacy executor host/node labels and old deployment topology are historical source context only, not targets for the clean new deployment. This pass does not reuse them as target identities.
5. **Decision:** the reviewed evidence does **not** justify adding Temporal now. It also does not prove that all durability requirements are implemented. Keep Temporal **FUTURE-GATED / NOT SELECTED / NOT ADMITTED / NOT IMPLEMENTED / NOT QUALIFIED** until a source-backed, owner-approved residual durability/recovery requirement is isolated after contract reconciliation.
6. **Next evidence:** use existing WB-14 governance and lifecycle traces to complete the cross-route identity/idempotency/lease-fencing/cancellation/retry/restart-recovery/result-provenance matrix. Keep proposed rows distinct from accepted internal ASTRA semantics; do not mint a second queue or mission authority.

### Verification boundary

This pass compared already-pinned repository documents only. No source code was executed, no runtime or host was inspected, no test/schema validator/security scan was run, and no installation, model/provider call, credential use, qualification, deployment or branch integration occurred.


## 7.24 OpenHands Agent Server authentication, workspace isolation and egress admission review (2026-10-17)

**Scope:** source-only review at immutable upstream commit `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`. Detailed findings are recorded in [Wave 40 — OpenHands Agent Server Admission Review](MEDIAHUB-OPENHANDS-AGENT-SERVER-ADMISSION-REVIEW-WAVE-40-2026-10-17.md), blob SHA `e9b1fba5abc1432b86f973becd75fd55be72f246`. This is a separate admission decision for the Agent Server package; it does not automatically follow from SDK source review.

| Evidence | Observation | Admission implication |
|---|---|---|
| Immutable upstream source | Commit `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`, signed/verified by the GitHub commit API; tree `54c039b002905c0c7c4db7c9f8d7a6c7cd5b46c4`. SDK metadata blob `160610fcba9b379a10340f16ab77c3bf504f2609` declares version 1.55.1 and Python `>=3.12`; repository license blob `b0bd86a6335a564bd3766666bebbf014fd6a8013` is MIT. | Source identity is pinned for review. Artifact digest, source-to-artifact provenance, full dependency/SBOM/license/advisory closure and MediaHub target compatibility remain OPEN. |
| Authentication and route exposure | `dependencies.py` blob `d1d2a6aece2056adc15824aed6cdccc4c3c33ead` documents optional session-key enforcement: an empty key list leaves REST routes unsecured. `sockets.py` blob `33d7a4b1666e9cdcf004b157470e9be16cdfe693` accepts WebSockets without a configured key. `__main__.py` blob `226f43dca5a2d1799c84199bbd85bd07bfc98339` defaults to loopback without a key, but allows explicit wildcard binding with a warning. | Any MediaHub target must mandate a non-empty scoped key set, explicit bind/TLS/reverse-proxy/ACL policy and route-by-route auth review. CLI warning is not a policy gate. |
| Documentation/code drift | Agent Server README blob `a64ff0840230ff5ae2d7c167c824048eaf72da9f` describes `0.0.0.0` as the default; pinned executable entrypoint selects loopback without a session key and wildcard bind when authentication is configured, unless overridden. | Record upstream documentation drift. The accepted MediaHub target manifest must declare network settings explicitly rather than rely on prose defaults. |
| Workspace and execution mode | `config.py` blob `a5830083eb110eadc6262287c5242f50e2296b66` defaults `conversation_runtime` to `local`. The README describes local workspace execution and warns that backend subprocesses lack OS isolation. | Local mode is blocked for untrusted autonomous tasks unless a separate accepted task class and boundary prove suitability. SDK/Agent Server presence alone provides no sandbox guarantee. |
| Docker execution boundary | `docker_runtime/registry.py` blob `27803eeab90bf50b900ed7c238b083e855aba3d9` shows non-root UID/GID, dropped capabilities, no-new-privileges, resource limits, per-conversation mounts and loopback-only published ports. The inspected launch command has no explicit network-disable flag or destination allowlist and adds a host-gateway alias. | Useful controls are source-observed; network egress, host reachability, image digest, mounts, cleanup and target qualification remain OPEN. Docker mode is optional and must be explicitly selected in an accepted target profile. |
| Telemetry/privacy | Telemetry policy blob `64e3b567352d4b3fef36327b5d8c5d8b30613403` defaults product-analytics delivery off and gates delivery on consent. Completion logging and Laminar/OpenTelemetry are separate channels; sanitizer blob `3f56a1b00dab0643f2f2bda925eba9386e823854` covers product-analytics event shaping. | R-06 must specify each channel's destination, payload class, consent, retention/deletion, readers, integrity and outage behavior. “Telemetry off” must identify the channel and configuration. |
| Lifecycle/cleanup | Docker registry source includes stale-container cleanup, idle-runtime handling, stop/removal and storage reclamation paths. | Source presence is not crash/restart/cancellation or secret-deletion qualification. A0 must own accepted task admission, lease, cancellation, recovery and evidence reconciliation. |

### Gate disposition

- OpenHands SDK remains **RESEARCH CANDIDATE / NOT SELECTED / NOT ADMITTED**; Agent Server is a distinct **CANDIDATE / NOT ADMITTED**.
- Open gates: exact artifact hashes and provenance; readable complete lock/SBOM/advisory evidence; accepted Python/OS/CPU target; required authentication; isolated workspace/process model; explicit egress and host-gateway policy; telemetry/privacy/audit policy; accepted A0 issuer/lifecycle; cleanup and recovery evidence; owner-approved capability gap.
- The review did not change the canonical component manifest or YAML. No download, install, dependency resolution, test, scan, provider/model call, credential use, host/runtime inspection, qualification, deployment or branch integration occurred.

Official upstream source: https://github.com/OpenHands/software-agent-sdk/commit/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1
