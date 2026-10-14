# MediaHub OS — Autonomous Agent Ecosystem Survey

- Date: 2026-10-14
- Repository: VlDMlNSh/mediahub-os
- Ref: docs/mediahub-chat-tree-map-20261012
- Status: RESEARCH SNAPSHOT / CANDIDATE-ONLY / NOT ACCEPTED / NOT IMPLEMENTED
- Scope: targeted public GitHub review across autonomous coding agents, agent SDKs, workflow engines, local inference, tool protocols, sandboxing, policy, telemetry, memory and evaluation.
- Important limitation: this is a broad targeted survey, **not an exhaustive scan of every repository on GitHub**. Popularity, recent commits or upstream README claims do not establish suitability, safety, compatibility, qualification or adoption.
- Change boundary: no product code or normative contract was changed; no software installed; no tests, evaluations, provider/model calls, host/runtime inspection, deployment or qualification performed.

## 1. Executive recommendation

Do not replace Jarvis or ASTRA with a third-party all-in-one autonomous agent. Preserve Jarvis as the intended engineering coordinator and ASTRA as a bounded engineering-control subsystem, while the cross-system lifecycle owner remains unresolved under DEC-DEV-02. Keep MediaHub Product State Authority exclusive over canonical product mutations.

The strongest direction is a **composed, policy-gated engineering fabric**:

1. Jarvis and ASTRA remain MediaHub-owned coordination/evidence components.
2. Coding and research agents run as replaceable, least-privilege workers behind a narrow adapter; the first candidate to evaluate for coding workers is the OpenHands Software Agent SDK.
3. MCP is a candidate tool-interface protocol, not an authorization mechanism.
4. The existing Ollama/local-provider path remains the initial local-inference candidate. Specify and repair route-policy semantics before adding another inference server or a new gateway.
5. Explicit execution modes and data-class policy must prevent a local-only request from entering the cloud route set. This concrete source-level gap is recorded separately as MH-ARCH-045.
6. Keep task/evidence ownership, identity, authorization, audit, provenance and release gates inside MediaHub contracts. Third-party agent memory, workflow history, model output and plugin metadata never become canonical product state.
7. Add observability/evaluation adapters only behind existing contracts; durable workflow or separate policy engines are conditional choices after a demonstrated gap, not default additions.

The objective is not to accumulate the most frameworks. It is to increase capability while minimizing overlapping control planes, authority ambiguity, data egress and unqualified dependencies.

## 2. Survey method and evidence quality

The survey used live GitHub repository metadata and official repository READMEs/security or support documentation on 2026-10-14. The search covered six themes: autonomous coding agents; agent orchestration frameworks; durable workflows; local inference; agent memory; and sandbox/policy enforcement. Repository stars are approximate counters at retrieval time and are included only as context, not as a ranking. “Pushed” is a GitHub metadata snapshot. Licences require review at the exact pinned revision and dependency/subdirectory level before adoption.

The review prioritized source role, architectural overlap, security boundary, local/hybrid fit, licensing, project activity and fit with the existing MediaHub Component Manifest 2.0. It did not clone repositories, run upstream code, inspect their full source trees or validate their claims experimentally.

## 3. Relevant public repositories

| Project | GitHub snapshot | Licence metadata | Potential value | Recommended disposition for MediaHub |
|---|---:|---|---|---|
| [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk) | ~1.3k stars; active 2026-10-14 | MIT | Modular coding-agent SDK, local workspaces or ephemeral workspaces through its Agent Server | **First coding-worker candidate to evaluate.** Use behind a bounded executor adapter; isolated workspace; no independent merge, release or State Authority permission. |
| [OpenHands](https://github.com/OpenHands/OpenHands) | ~90.9k; active 2026-10-14 | MIT | Full AI-driven development environment | Reference implementation and alternative platform, but too broad to install wholesale into Jarvis/ASTRA without a documented gap. Prefer evaluating the smaller SDK first. |
| [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) | ~16.2k; active 2026-10-14 | Apache-2.0 | Sandboxed agent runtime with filesystem/process/network policy | **Security architecture candidate; not admitted by MediaHub.** Upstream status sources conflict: the current support matrix labels Latest v0.1.4 and recommends stable releases for production, while Security Best Practices and a shared support-page banner still say alpha / do not use in production; the v0.1.0 release milestone says the alpha designation was removed. Treat this as upstream documentation/version-lineage drift and pin the exact release plus matching security docs before any production decision. Platform: x86_64 Linux is supported; macOS is supported only on Apple Silicon; Windows WSL 2 is experimental. It therefore does not fit an Intel Mac Pro as a macOS runtime; Linux-worker evaluation is conditional on the approved target profile and runtime prerequisites. |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | ~20.6k; active 2026-10-14 | MIT | Typed Python agent/tool interfaces and model adapters | Candidate for a small typed worker or adapter prototype if the existing gateway demonstrably lacks these contracts. Do not introduce it as a second top-level controller by default. |
| [LangGraph](https://github.com/langchain-ai/langgraph) | ~43.3k; active 2026-10-14 | MIT | Stateful graph orchestration, checkpoints, interrupt/human review and durable execution patterns | Alternative orchestration candidate. Evaluate against the existing Astra bounded lifecycle; do not add in parallel with Pydantic AI/Temporal for the same responsibility without a measured need. |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | ~14.1k; active 2026-10-14 | MIT | Python/.NET agent and workflow framework with checkpointing and human-in-the-loop patterns | Valid alternative if a standard framework is required. The older Microsoft AutoGen project is in maintenance mode and directs new projects toward this framework. |
| [Temporal](https://github.com/temporalio/temporal) / [Python SDK](https://github.com/temporalio/sdk-python) | ~23.7k; active 2026-10-14 | MIT | Durable, restart-resilient task/workflow execution | Already future-gated by the Component Manifest. Evaluate only if authorized evidence shows the current lifecycle fails required durability/recovery criteria. It must not become a competing task-lifecycle owner. |
| [Ollama](https://github.com/ollama/ollama) | ~183k; active 2026-10-14 | MIT | Local model serving and REST API | Already referenced by code and component plan. Keep as the initial local provider candidate; validate the hardware/model profile and route-policy contract before another runtime is added. Repository presence does not prove installation. |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | ~131k; active 2026-10-14 | MIT | Portable local inference and an OpenAI-compatible server | Already target-gated in the Component Manifest. Keep as an alternative to benchmark on an authorized hardware profile; do not deploy a duplicate local inference stack by default. |
| [LiteLLM](https://github.com/BerriAI/litellm) | ~61.2k; active 2026-10-14 | GitHub API reports NOASSERTION; licence treatment differs for enterprise paths | Multi-provider gateway, route/cost controls and logging | **Defer.** It overlaps with the current CloudFirstOrchestrator and does not replace MediaHub data-class, egress or authorization policy. A path-by-path licence review is mandatory before selection. |
| [Model Context Protocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | ~9.45k; active 2026-10-13 | Repository README says MIT; verify pinned files | Standard interface for tools and context providers | **Adopt as a protocol candidate, not an authority.** Require server allowlists, narrow tool schemas, provenance, explicit identity/authorization, egress restrictions and audit around every server. |
| [Agent2Agent (A2A)](https://github.com/a2aproject/A2A) | ~26.1k; active 2026-10-13 | Apache-2.0 | Cross-framework remote agent communication | Future-gated. Use only when remote inter-agent interoperability is a proven requirement; internal Jarvis↔ASTRA integration should first use a typed internal contract. |
| [Open Policy Agent](https://github.com/open-policy-agent/opa) | ~12.4k; active 2026-10-14 | Apache-2.0 | Declarative policy-as-code engine | Conditional future candidate. Do not introduce a second decision authority while P0-07/P0-05 authorization contracts and policy ownership are unresolved. |
| [OpenTelemetry Python](https://github.com/open-telemetry/opentelemetry-python) | ~2.67k; active 2026-10-14 | Apache-2.0 | Traces and metrics SDK for Python; logs maturity differs by signal | Good instrumentation candidate complementary to the selected OTel Collector and Prometheus. Trace IDs, task transitions, route/provider/model identity, timing and sanitized failures; avoid prompts, secrets and user payloads. |
| [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) | ~3.0k; active 2026-10-14 | MIT | LLM/agent evaluation framework and reusable evaluations | Future candidate for a gated evaluation harness. No evaluations were run in this survey; introduce only after explicit test/qualification authorization and an evidence plan. |
| [Cline](https://github.com/cline/cline) | ~70.3k; active 2026-10-14 | Apache-2.0 | Autonomous coding agent delivered as SDK, IDE extension or CLI | Useful comparative reference or optional executor, not a replacement for Jarvis/ASTRA control and governance. |
| [browser-use](https://github.com/browser-use/browser-use) | ~118k; last push 2026-10-09 | MIT | Browser-driven agent tasks | Optional bounded research worker. Browser/network access must be explicitly scoped and isolated; never grant unbounded host or account authority. |
| [Letta Code](https://github.com/letta-ai/letta-code) | ~3.6k; active 2026-10-14 | Apache-2.0 | Stateful agent memory, identity and long-running agent experience | Reference for user-facing memory patterns only. Self-modifying prompts/skills/memory need versioning, provenance and review; agent memory is not canonical project truth. |
| [OpenClaw](https://github.com/openclaw/openclaw) | ~392k; active 2026-10-14 | MIT | Full personal agent/gateway with broad tool integrations | **Do not adopt wholesale as privileged Jarvis/ASTRA controller.** Its documented trust model assumes one operator or mutually trusting team per gateway; it is not a shared boundary for mutually untrusted users. Reuse only patterns that pass MediaHub threat review. |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | ~254k; active 2026-10-14 | MIT | Personal/self-improving agent with long-lived experience | Comparative reference; do not inherit self-modification or tool privileges as a default architecture. |
| [Google Agent Development Kit](https://github.com/google/adk-python) | ~21.8k; active 2026-10-14 | Apache-2.0 | Code-first agent framework | Alternative to Pydantic AI, LangGraph or Microsoft Agent Framework, not a component to stack with all of them. |
| [CrewAI](https://github.com/crewAIInc/crewAI) | ~59.7k; active 2026-10-14 | MIT | Role-oriented multi-agent coordination | Pattern reference only unless a verified role/workflow gap exists. It must not create a parallel multi-agent scheduler or lifecycle owner. |

### Interpretation

- Stars are a weak signal: they reflect visibility, not correctness, secure defaults, lifecycle semantics, resource requirements or fit with this system.
- A README saying “production-grade” or “secure” is not independent evidence that a component satisfies MediaHub requirements.
- The current canonical Component Manifest 2.0 already selects or gates several of these roles. This report does not amend that manifest and does not supersede its authority.
- Licences and support matrices must be rechecked at the exact version/SHA eventually proposed for admission. No source code was copied from upstream repositories.

## 4. Confirmed integration gap in the inspected source path — MH-ARCH-045

Primary-source read-through on main found the following mismatch:

| Evidence source | Revision | Observation |
|---|---|---|
| runtime/mediahub_runtime/astra_gateway.py | blob SHA 10985e4ad8f682313d08e7492ecc1856a8bce20f | AstraTaskRequest has no explicit route-mode field in the inspected DTO. The gateway labels new work cloud_first/cloud_first_local_extension and calls the orchestrator without a route-policy argument. |
| runtime/mediahub_runtime/cloud_orchestrator.py | blob SHA 24c28197df7baca49abd81956752a7a5092506d9 | Cloud routes are considered before local routes; local extension is enabled by default and cloud execution errors can advance candidate selection. Setting allow_local_extension=false would still not, by itself, express LOCAL_ONLY because the route list begins with cloud candidates. |
| architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md | blob SHA e549692f207fbc91d9b9b9b92b8e665404f07290 | The accepted target architecture requires an explicit local-only mode that fails closed when the local endpoint is unavailable and prohibits silent cloud fallback in that mode. |

**Finding:** confirmed static route-contract mismatch in the inspected source path; potential privacy/data-egress consequence. Deployment and real-world use of this source path are UNKNOWN, so this is not evidence of an observed production data leak.

**Required disposition:** preserve as MH-ARCH-045 / P1 until a controlled design defines route mode, data-class admission and permitted providers end-to-end. A local-only request must never add cloud candidates; unavailable local service must return a bounded failure, not route to cloud. Cloud-allowed mode must use only policy-admitted providers and expose actual provider/model identity in evidence. Failover is permitted only within the same explicitly admitted policy set. Do not patch implementation or elevate status in this research pass.

## 5. Recommended target composition for Jarvis and ASTRA

~~~text
Human / repository owner
        |
        v
Jarvis — engineering coordination / plan / review routing
        |
        | typed task contract; lifecycle ownership still needs DEC-DEV-02
        v
ASTRA — bounded engineering queue/claims/evidence/gate subsystem
        |
        v
Admission boundary — identity + authorization + task policy + data class
        |
        +-------------------------------+
        |                               |
        v                               v
Isolated worker adapter             Model route-policy boundary
(e.g. OpenHands SDK candidate)      LOCAL_ONLY / CLOUD_ALLOWED (design needed)
        |                               |
        v                               +------> admitted local endpoint (Ollama candidate)
Ephemeral workspace                  |
narrow capabilities                  +------> explicitly admitted cloud providers
no direct authority                  (never in LOCAL_ONLY)
        |
        v
Artifact/change proposal + source SHA + sanitized evidence
        |
        v
Independent verification / human approval / controlled GitHub flow

MCP: tool-interface protocol behind admission and per-server policy.
OpenTelemetry SDK/Collector: operational telemetry, not an authority.
Inspect AI: future evaluation harness only after explicit authorization.
MediaHub Product State Authority: separate and exclusive; never delegated to the above.
~~~

The diagram is a recommendation, not an adopted architecture. The unresolved Jarvis/ASTRA lifecycle-owner decision, trusted-context issuer path, and provider/data-egress policy remain hard gates. Third-party frameworks never gain product-state authority.

## 6. Phased evaluation/admission plan

### Stage 0 — resolve contract blockers (documentary)

1. Resolve the existing DEC-DEV-02 single lifecycle-owner question; do not let Jarvis and ASTRA both own the same leases/retry/cancel/promotion transitions.
2. Complete the P0-07/P0-05/P0-04 trusted-context and authorization chain and actual independent D2 review.
3. Define task-level route policy and data-class/provider matrix consistent with Distributed AI Infrastructure. Distinguish local-only from cloud-allowed explicitly.
4. Determine worker trust profiles and permitted GitHub/workspace capabilities. Keep privileged credentials out of agents and returned logs.

### Stage 1 — choose one coding-worker candidate

Evaluate OpenHands Software Agent SDK against one bounded coding task and a reference adapter; compare it with the existing runner and at most one typed-agent alternative. The worker should operate only in an isolated workspace, produce a patch/artifact and exact source identity, and never merge, release, alter canonical state or self-promote its evidence.

### Stage 2 — standardize tool access

Evaluate MCP for replaceable tool adapters. Each server gets a pinned version, licence/SBOM, explicit tool allowlist, narrowly scoped identity/capabilities, egress policy, timeouts, sanitized audit and revocation path. MCP transport or server registration is not authorization.

### Stage 3 — route local and hybrid inference safely

Keep Ollama as the existing initial local-serving candidate. Specify route policy before adding runtimes. Benchmark llama.cpp or ONNX Runtime only when an authorized hardware profile and measurable capability gap exist. No implicit local-to-cloud fallback in local-only mode; no cloud route without explicit data/provider admission.

### Stage 4 — sandbox and observe

Review OpenShell maturity and target compatibility; it is not a production candidate while its official docs describe alpha/not-for-production status, and macOS support is limited to Apple Silicon. Assess Linux-worker applicability separately. Consider OpenTelemetry Python instrumentation to complement the already-selected Collector/Prometheus, with telemetry strictly observational and payload/secret-minimized.

### Stage 5 — durability and evaluation, conditionally

Only after explicitly authorized verification identifies a real gap, compare Temporal with the existing bounded task lifecycle. Only after tests/qualification are authorized should Inspect AI or an equivalent evaluation harness be integrated. A2A is unnecessary until cross-platform/remote agent-to-agent interoperability is an actual requirement. OPA is conditional on governance confirming policy ownership and avoiding a competing authorization authority.

## 7. Admission checklist for any upstream component

Before any eventual code contribution or installation:

- Pin exact repository, release/tag/commit SHA and transitive dependencies.
- Verify licence and notices for the exact included paths, then generate an SBOM and vulnerability/licence scan.
- Compare platform/hardware/OS requirements with an approved target profile.
- Document task/data boundary, identity, permissions, egress, secret handling, sandboxing, failure behavior and revocation.
- Trace every component into accepted MediaHub contracts and ownership boundaries.
- Establish reproducible focused tests, negative security tests, evidence retention and independent review once the user separately authorizes that stage.
- Prove that the dependency does not introduce an alternate State Authority, task-lifecycle owner, policy authority, update authority or recovery authority.
- Record selection as SELECTED / NOT DEPLOYED; promotion to IMPLEMENTED, VERIFIED, QUALIFIED, RELEASED, DEPLOYED or ACCEPTED requires separate evidence.

## 8. Explicit non-claims and next step

- This is a targeted survey of relevant repositories, not an exhaustive scan of GitHub.
- No component was installed, invoked or copied into MediaHub.
- No code, tests, qualification, host/runtime, credentials, infrastructure, release or deployment activity occurred.
- The survey itself is not an owner decision and does not change the Component Manifest, Baseline 2.0 or any domain contract.
- ASTRA Current Truth remains G0–G11 BLOCKED / overall NOT_PROVEN / BLOCKED on main at the inspected snapshot.
- Contour B remains gated on deployment and independent acceptance of Contour A.
- Next authorized documentary step: owner review of this candidate assessment and the route-policy gap; then write a formal design spec only after design approval. Implementation planning and execution require the subsequent review/authorization gates.


## 9. Follow-up source-identity and routing trace (2026-10-14)

This addendum revalidates selected survey claims against live main sources and reconciles the external-research findings with the single MediaHub remediation register. It does not change the canonical Component Manifest or authorize installation.

### 9.1 Upstream OpenShell status drift

The upstream pages inspected during follow-up do not support a single unqualified maturity statement:
- Current Support Matrix documentation identifies Latest as v0.1.4 and says stable releases should be used for production deployments: https://docs.nvidia.com/openshell/latest/reference/support-matrix
- Security Best Practices still carries a banner saying OpenShell is alpha and should not be used in production: https://docs.nvidia.com/openshell/latest/security/best-practices.html
- The v0.1.0 release milestone says the alpha designation was removed and describes a stable release cadence: https://github.com/NVIDIA/OpenShell/milestone/10

Therefore the project must pin the exact candidate release and review version-matched policy/security documentation before drawing a production-maturity conclusion. MediaHub admission is still NOT APPROVED. Platform scope remains material: official support documents list Linux amd64/arm64, macOS Apple Silicon, and Windows WSL 2 experimental; host-specific compatibility remains a separate gate.

### 9.2 MH-ARCH-046 — Ollama selected-model identity vs executor evidence

Main source blobs freshly re-read:
- `runtime/mediahub_runtime/astra_gateway.py`: `10985e4ad8f682313d08e7492ecc1856a8bce20f`
- `runtime/mediahub_runtime/cloud_orchestrator.py`: `24c28197df7baca49abd81956752a7a5092506d9`
- `tests/ai/test_cloud_orchestrator_failover.py`: `c66b63b158c545ae627c596791381b83ef902c59`

Static trace: `OllamaExecutor` sends its class-level model string `qwen2.5-coder:3b`. The orchestrator's default Ollama route separately reads `MEDIAHUB_OLLAMA_MODEL` / `MEDIAHUB_OLLAMA_MODELS` for the decision/evidence model field, while the default gateway injects a preconstructed `OllamaExecutor()` and the orchestrator's executor lookup returns that instance without binding the route-selected model to it. Consequently, a configured route model may differ from the model sent in the Ollama request; with no route model configured, route evidence may say `unspecified` while the executor still sends its class default. This is a **confirmed static model-identity/provenance mismatch in the inspected construction path**, not proof that a live request has used the mismatched configuration.

Required disposition: resolve one actual model identity at admission, pass it to the executor and record that same identity in the selected route, events, provider qualification and result evidence. A future implementation must add focused configured/default model tests and a mismatch-negative test under explicit test authorization. No test was run in this pass.

### 9.3 Crosswalk to the unified finding register

- MH-ARCH-045 — explicit LOCAL_ONLY route contract is absent from the inspected AstraGateway/CloudFirstOrchestrator call path; the accepted distributed-infrastructure target requires local-only operation to fail closed without silent cloud fallback on the specified development route. The precise relationship between this gateway and the Claude Code/FCC path still requires an explicit call-path/scope crosswalk. Do not assert an observed production egress incident.
- MH-ARCH-046 — actual Ollama executor model and selected/evidenced model can diverge as described above.

Both are source-review findings only. No code changed, no tests or qualification ran, and no runtime/provider/model invocation occurred.
