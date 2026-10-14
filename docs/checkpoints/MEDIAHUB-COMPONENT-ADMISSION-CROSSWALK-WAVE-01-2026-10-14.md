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
