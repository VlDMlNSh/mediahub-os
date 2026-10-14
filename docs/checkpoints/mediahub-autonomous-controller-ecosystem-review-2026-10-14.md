# Autonomous Controller Ecosystem Review — 2026-10-14

- Status: **READ-ONLY RESEARCH / CANDIDATES ONLY / NOT ADMITTED**
- Scope: external GitHub discovery relevant to Jarvis, ASTRA/Astra Gold, local-first and hybrid developer fabric.
- Repository: `VlDMlNSh/mediahub-os`
- Review branch: `docs/mediahub-chat-tree-map-20261012`
- Main HEAD observed during review: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`
- Documentation branch HEAD observed during review: `bc91c941c904aa80ee61cb75acae44bfad37e71f`
- Authority: roadmap and canonical component manifest govern admission. This note does not select, install, integrate, qualify, or authorize any dependency.

## 1. Executive result

A bounded GitHub search was performed across agent orchestration, local LLM tooling, durable workflows, and Home Assistant/MCP integration. This was **not an exhaustive scan of all GitHub repositories**; search relevance and indexing are incomplete. The search returned many recent, low-evidence repositories, so popularity/recency alone is not a sufficient admission criterion.

The immediate improvement is not to bolt on multiple agent frameworks. It is to preserve one task-state authority, one queue/lease lifecycle owner, typed capability boundaries, explicit data-egress policy, durable recovery semantics, and reproducible component provenance. Any external project must fill a documented gap without introducing a competing state authority or bypassing Product State Authority.

## 2. Candidate portfolio for source-level review

These are well-known upstream projects to evaluate against the existing Canonical Component Manifest 2.0 and repository contracts. Their inclusion is **a review recommendation, not a selection or compatibility claim**.

| Candidate | Official repository | Potential fit | Required admission checks |
|---|---|---|---|
| LangGraph | https://github.com/langchain-ai/langgraph | Stateful graph-based agent workflows; checkpointing and human-in-the-loop patterns | Compare its persistence/state semantics with ASTRA's single lifecycle authority; licensing, dependency/resource footprint, local-only behavior, recovery semantics |
| Temporal | https://github.com/temporalio/temporal | Durable workflow execution, retries, timers, long-running orchestration | Operational footprint on constrained Mac mini; database/service dependencies; determine whether it solves a proven gap without duplicating queue authority |
| OpenHands | https://github.com/All-Hands-AI/OpenHands | Autonomous software-engineering agent patterns and sandboxed task execution | Treat as a candidate worker/product, not controller authority; inspect sandboxing, tool permissions, network egress, model/provider assumptions, supported hardware |
| Microsoft AutoGen | https://github.com/microsoft/autogen | Multi-agent coordination and agent conversation patterns | Compare with existing Jarvis/ASTRA orchestration; avoid parallel orchestration stacks and ambiguous ownership |
| CrewAI | https://github.com/crewAIInc/crewAI | Role/task-based multi-agent patterns | Verify current APIs, licensing, security boundaries and need; avoid adding a second task lifecycle |
| Ollama | https://github.com/ollama/ollama | Local model serving interface | Validate target OS/CPU/GPU, model licensing, memory envelope, API behavior, auth/network exposure and explicit no-cloud-fallback policy |
| llama.cpp | https://github.com/ggml-org/llama.cpp | Low-level local inference, quantized model execution, broad hardware coverage | Validate supported build target and performance only with authorized hardware evidence; packaging, model provenance and update/rollback |
| LiteLLM | https://github.com/BerriAI/litellm | Multi-provider routing and unified API interface | Must not weaken data-class routing, secret custody, local-only policy, audit, budget or provider allowlists |
| Model Context Protocol | https://github.com/modelcontextprotocol | Typed tool/resource integration protocol ecosystem | Protocol compatibility is not authorization; every tool needs least privilege, consent/confirmation where required, audit and egress controls |
| Home Assistant Core | https://github.com/home-assistant/core | Smart-home integration/control domain | Existing project boundary says Home Assistant Core remains smart-home authority; AI/controller must not bypass its authorization or become canonical product-state authority |

## 3. Architecture patterns worth reusing (not copying wholesale)

1. **Single-writer state authority:** Jarvis/ASTRA may coordinate engineering work, but neither gains canonical MediaHub product-state mutation rights. Preserve the existing Policy → Authorization → Consumer Boundary → State Authority path.
2. **Durable task envelope:** stable task ID, idempotency key, declared inputs/data class, capability set, deadline, cancellation token, retry budget, lease/heartbeat, output schema, provenance and evidence references.
3. **Typed tool boundary:** schema-validated requests, explicit capability allowlist, scoped identity, policy decision, human approval for sensitive actions, bounded execution, structured result and audit event.
4. **Local-first inference policy:** local-only routes fail closed. A cloud provider is used only where the task's data class and explicit route policy permit it; no silent fallback.
5. **Worker isolation:** workers receive task-scoped capabilities, not ambient shell/admin credentials. Treat contributed or customer-site compute as a separate untrusted trust domain.
6. **Evidence-driven promotion:** a worker's output is a candidate artifact until independently checked; it cannot self-promote implementation, verification, qualification, release, deployment or acceptance status.
7. **Operational recovery:** explicit cancellation/retry semantics, crash-safe leases, bounded concurrency/quotas, observable readiness, backup/restore, rollback and provenance.
8. **Supply-chain admission:** pin immutable release/commit, record license, source provenance, dependency lock/SBOM, supported platforms, network flows, secrets, resource envelope and rollback plan.

## 4. Search evidence and limitations

The connected GitHub search returned current search-index results for broad queries:
- autonomous agent orchestration;
- local LLM agent runtime;
- durable workflow execution;
- Home Assistant + MCP integration.

Some returned repositories were newly created or weakly described. They were not treated as top-tier merely because they appeared in search results. The external candidates in §2 are well-known upstream projects identified for a second, source-level review; this pass did not inspect every candidate's current release, license file, advisories, dependency graph, benchmarks or compatibility matrix.

This review does not claim a complete GitHub scan, an objective global ranking, or proof that any candidate is the “best” current option.

## 5. Admission matrix — current disposition

| Candidate group | Disposition | Reason |
|---|---|---|
| Agent frameworks (LangGraph, AutoGen, CrewAI) | CANDIDATE / NOT ADMITTED | Potential orchestration overlap; no documented gap-to-component mapping yet |
| Durable workflow engine (Temporal) | CANDIDATE / NOT ADMITTED | Could address durable workflow gaps, but may add operational weight and duplicate queue ownership |
| Coding agent (OpenHands) | CANDIDATE / NOT ADMITTED | Potential isolated worker only; sandbox/security/provider/data egress require review |
| Local inference (Ollama, llama.cpp) | CANDIDATE / NOT ADMITTED | Hardware and OS profiles remain unevidenced; compare with current manifest choices |
| Provider router (LiteLLM) | CANDIDATE / NOT ADMITTED | Must be subordinate to project policy and must not create uncontrolled fallback |
| MCP ecosystem | PROTOCOL CANDIDATE / NOT AUTHORIZATION | Integration format only; not a trust model or permission grant |
| Home Assistant Core | EXISTING DOMAIN AUTHORITY TO PRESERVE | Do not duplicate or bypass its smart-home authority |

## 6. Admission process and remaining gates

The first two documentary steps have now been completed against the live canonical input:

1. Read the current Canonical Component Manifest 2.0 on `main`, blob SHA `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`.
2. Crosswalk candidate projects against its explicit selected, target-gated, future-gated and excluded categories in §8 below. The manifest does not assign stable per-component IDs; this review does not invent any.

Remaining gates:
3. For a candidate the owner elects to advance, recheck exact release/tag/commit, licence and path-level redistribution terms, security advisories, supported hardware/OS, dependency footprint, network flows, resource envelope and rollback/removal procedure.
4. Record a concrete capability gap and approved route into the manifest/admission queue; no gap means defer or reject unnecessary duplication.
5. Only after owner design review and separate implementation authorization may a candidate-specific compatibility/evidence plan be prepared. Installation, provider/model invocation, tests, qualification, host inspection, infrastructure changes and deployment remain gated and were not performed here.

## 7. Safety and project constraints respected

- No software was installed.
- No models or external inference providers were invoked.
- No credentials or hosts/runtime were inspected.
- No tests or qualification were run.
- No infrastructure or deployment was changed.
- No code or runtime component was integrated.
- No branch was merged, rebased or cherry-picked.


## 8. Crosswalk against Canonical Component Manifest 2.0

**Authority source:** `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` on `main`, blob `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`. The manifest states that component selection is closed, implementation remains open and production admission is qualification-gated. It also says existing code or popularity does not imply selection, and no component may add a second State Authority, task-lifecycle owner, policy authority, update authority or recovery authority.

| Candidate / family | Exact manifest alignment | Disposition for Jarvis + ASTRA | Reason / required next evidence |
|---|---|---|---|
| OpenHands Software Agent SDK | Not listed in Manifest 2.0; covered by the separate broad survey as a coding-worker candidate | **First worker candidate to evaluate; NOT ADMITTED** | It may supplement the controller with bounded isolated coding jobs. It must produce a patch/artifact and source identity only; no merge, release, canonical-state mutation, evidence self-promotion or ambient credentials. Requires an owner-approved gap, workspace/egress controls, pinned release, licence/SBOM and platform evidence. |
| LangGraph; Microsoft Agent Framework; CrewAI; AutoGen | Not listed as selected components; these are alternative orchestration frameworks | **Do not stack or replace Jarvis/ASTRA by default** | They overlap with existing task planning, workflow and state/lifecycle responsibilities. Select at most one alternative only if a measured gap remains after the existing ASTRA lifecycle is examined. AutoGen and Microsoft Agent Framework are not two extra components to add together. |
| Temporal | Manifest §5: **future/reference-gated**, durable workflows only after a demonstrated gap | **Keep future-gated** | Potential recovery/durability option, but could add a separate workflow service and duplicate lease/retry lifecycle. No adoption until the gap, operational footprint, state ownership and recovery semantics are established. |
| Ollama | Existing adapter/route is present in code, but Ollama is **not named in Manifest 2.0's AI candidate rows** | **Existing code candidate only; not manifest-admitted as canonical runtime** | Do not infer approval from the existing class. DEC-DEV-01 composition remains open, and MH-ARCH-045/046 document separate route-policy and model-provenance risks. Owner disposition and manifest source control are required before selecting it as the local runtime. |
| llama.cpp; ONNX Runtime | Manifest §4: **target-gated implementation candidates** | **Retain current gate; do not add duplicate inference stacks** | Compare against an approved node/hardware profile only when a measurable performance or capability gap is documented and benchmarking is separately authorized. |
| LiteLLM or another provider gateway | Not selected in Manifest 2.0; the repository already has `CloudFirstOrchestrator` | **Defer/reject by default** | Adds overlapping routing, failure/fallback and logging controls without solving the MediaHub-owned data-class/egress decision. Licence-path and deployment/security review also remain outstanding. Keep LOCAL_ONLY fail-closed policy outside any third-party gateway. |
| MCP | Protocol, not a selected runtime component in Manifest 2.0 | **Protocol candidate only; NOT an authorization mechanism** | Consider for interoperable tool/resource adapters when there is a concrete integration need. Every tool still needs MediaHub-owned authorization, least privilege, explicit allowlist, timeouts, egress restriction, audit minimization and revocation. |
| A2A | Not listed in Manifest 2.0 | **Defer until remote agent-to-agent interoperability is required** | It addresses agent-to-agent communication rather than trusted authorization or canonical task state. Adding it now would expand attack and compatibility surface without a demonstrated use case. |
| NVIDIA OpenShell or another agent sandbox | Not listed in Manifest 2.0 | **Candidate for later sandbox evaluation; NOT ADMITTED** | Useful security concepts, but the surveyed upstream support/maturity pages show conflicting release/security status language and platform limits. Pin the exact release with matching security docs and validate the intended Linux worker or Apple-Silicon profile before an admission decision. It is not a blanket solution for an Intel macOS host. |
| OpenTelemetry Python | Manifest §2 already selects OpenTelemetry Collector and Prometheus; the Python SDK itself is not separately listed | **Potential additive instrumentation candidate** | It can complement existing telemetry if a source-backed instrumentation gap is confirmed. Keep telemetry observational, bounded and sanitized. It cannot substitute for a durable, access-controlled security-audit contract or become a state authority. |
| Inspect AI | Not listed in Manifest 2.0; evaluation tooling only | **Defer until a separate evaluation authorization** | Could support a future model/agent evaluation harness, but no evaluations were run or authorized in this pass. It cannot replace ASTRA G0–G11, independent A3 or human acceptance. |
| Open Policy Agent (OPA) | Not listed in Manifest 2.0; policy-engine ownership remains a governance boundary | **Defer** | Introducing a second policy engine before the project settles P0-07 identity/context and policy ownership risks parallel authorization truth. Revisit only as an explicitly subordinate adapter with owner-approved policy-source precedence. |
| OpenClaw, Letta Code and other all-in-one personal-agent systems | Not selected in Manifest 2.0 | **Do not install as Jarvis/ASTRA replacements** | They bring their own control plane, memory/session semantics and tool permissions. That is broader than the bounded worker gap and risks a competing lifecycle/controller. Study narrowly scoped patterns only; preserve MediaHub ownership and provenance. |
| Home Assistant Core | The distributed/product architecture names it as the Smart Home operational authority; it is not a Jarvis/ASTRA controller component | **Preserve its domain authority** | Integrations may use its approved interfaces but Jarvis/ASTRA and third-party agents must not bypass or replace its smart-home authorization boundary. |

### Minimal recommendation

For the first evidence-gated evaluation, prefer **one isolated OpenHands SDK worker** over introducing a second top-level orchestrator; evaluate MCP only where tool interoperability is needed; consider OpenTelemetry Python as a telemetry adapter; keep Temporal, OpenShell, OPA, A2A, Inspect AI and other orchestration stacks deferred until a specific capability gap justifies them. Keep local inference behind an explicitly admitted route policy. The existing Ollama code is not by itself evidence that Ollama has been selected under Manifest 2.0.

This is a recommendation for owner review, **not an adopted selection**. No manifest row, component ID, normative contract, code, dependency, deployment or qualification status is changed by this crosswalk.
