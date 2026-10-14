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

## 6. Required next steps

1. Locate and read the exact current Canonical Component Manifest 2.0 path and source SHA on its authoritative ref.
2. Crosswalk each candidate to an existing manifest ID and a concrete capability gap. If no gap exists, reject as unnecessary duplication.
3. Inspect official upstream README, license, release tags, supported platforms, security policy/advisories and dependency footprint; pin exact revisions only after admission review.
4. Record owner decisions for any new runtime, broker, database, agent framework or state store. Do not add them by inference.
5. After approval, produce a compatibility/evidence plan for each selected candidate. Installation, model/provider invocation, tests, qualification, host inspection, infrastructure changes and deployment remain separately gated and were not performed here.

## 7. Safety and project constraints respected

- No software was installed.
- No models or external inference providers were invoked.
- No credentials or hosts/runtime were inspected.
- No tests or qualification were run.
- No infrastructure or deployment was changed.
- No code or runtime component was integrated.
- No branch was merged, rebased or cherry-picked.
