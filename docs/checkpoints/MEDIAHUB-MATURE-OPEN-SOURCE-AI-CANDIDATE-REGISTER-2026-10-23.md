# MediaHub OS — Mature Open-Source AI Candidate Register

- Date: 2026-10-23
- Status: DISCOVERY REGISTER / NOT FROZEN / NOT SCORED / NOTHING ADOPTED
- Immutable MediaHub target: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7
- Research branch: research/mature-ai-project-landscape-wave431-20261023
- Initial landscape: [Wave 431 report](MEDIAHUB-MATURE-OPEN-SOURCE-AI-LANDSCAPE-WAVE-431-2026-10-23.md)
- Expanded discovery: [Wave 432 report](MEDIAHUB-MATURE-PROJECT-DISCOVERY-WAVE-432-2026-10-23.md)
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Canonical checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Register rules and discovery sources

This is a candidate register, not a quality ranking, recommendation to install, or declaration that every entry is mature. A mature-candidate decision requires independent checks of activity, releases, license, dependencies, security posture, CI, tests, documentation and architecture fit. GitHub archived=false alone does not establish maturity.

It is not possible to prove that every GitHub repository has been enumerated. Coverage is made systematic by seeding discovery from multiple source-linked catalogs and checking upstream repositories. The catalogs observed in this pass:

- [Awesome Agent Runtime](https://github.com/sandbaseai/awesome-agent-runtime), README blob f3966aee2dd2657dd0a2b8e097f2fbf29ab6b1ad; describes 500 projects across ten production-agent infrastructure categories.
- [AI Agent Frameworks & Orchestration Tools](https://github.com/aglio-lab/ai-agent-frameworks), README blob 6bf6d81ed66adf04277e262a8a8b5b33160def5b; describes 166 active and 8 historical entries across 14 categories, stated review date 2026-07-16.
- [Awesome AI Agent Orchestration](https://github.com/Awesome-llms-labs/awesome-AI-agent-orchestration), README blob 67f8fd0fa7465e99f39e92e505dd093f5151e783; states a September 2026 snapshot with 98 entries and explicit verification flags.
- [Awesome Agent Infrastructure, Backblaze](https://github.com/backblaze-labs/awesome-agent-infrastructure), README blob f20b4187e7df4cb8b41d0572eb3d201e48184f2d.
- [Coding-Agent Harness Study](https://github.com/SteveVitali/coding-agent-harness-study), README blob b1861cf58db9266bbbc087ec4fb6f629cd39ebc4; six coding-agent harnesses, pinned-commit evidence ledger, snapshot 2026-08-04. Recheck any fast-moving findings against current source.

Catalog inclusion is not an endorsement. Commercial, open-core, source-available, and pre-release projects are comparison references only until license and terms allow the proposed reuse.

Screening states:
- CANDIDATE — relevant upstream repository found; maturity/security/license screening remains.
- CONDITIONAL — pre-release, open-core, provider coupling, or licensing/runtime boundary requires special review.
- REFERENCE ONLY — useful for historical migration or patterns, but not the default new runtime.
- EXCLUDED — repository was observed archived or upstream recommends a successor.
- NOT AUDITED — current commit SHA, latest stable release, license blob, dependency locks, CI/advisories and behavior are not all pinned and verified.

No comparative scoring or component selection begins until this register is screened and frozen.

## 2. Agent SDKs, orchestration and task contracts

| Candidate | Status | Capability to inspect |
|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | CANDIDATE | Stateful graph orchestration, checkpointing, interrupt/resume, recovery |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | CANDIDATE | Multi-agent workflows, Python/.NET, HITL and hosting |
| [CrewAI](https://github.com/crewAIInc/crewAI) | CANDIDATE | Role/task delegation |
| [Ruflo](https://github.com/ruvnet/ruflo) | CANDIDATE | Coding-agent harness, coordination, plugins/MCP and GitHub mutation failure handling |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | CANDIDATE | Typed tasks, structured outputs, validated tool contracts |
| [OpenAI Agents SDK, Python](https://github.com/openai/openai-agents-python) | CANDIDATE | Handoffs, tools, guardrails, tracing, sandbox integration |
| [OpenAI Agents SDK, TypeScript](https://github.com/openai/openai-agents-js) | CANDIDATE | TypeScript agent loops, handoffs and guardrails |
| [Google ADK](https://github.com/google/adk-python) | CANDIDATE | Agent composition, workflows and evaluation |
| [Agno](https://github.com/agno-agi/agno) | CANDIDATE | Agent teams, storage, memory and API runtime |
| [Hugging Face smolagents](https://github.com/huggingface/smolagents) | CANDIDATE | Small, inspectable agent loop and tool/code execution |
| [Mastra](https://github.com/mastra-ai/mastra) | CANDIDATE | TypeScript agents, graph workflows and suspend/resume |
| [Strands Agents](https://github.com/strands-agents/harness-sdk) | CANDIDATE | Model-driven loop, hooks, MCP and multi-agent patterns |
| [LlamaIndex](https://github.com/run-llama/llama_index) | CONDITIONAL | Document parsing, retrieval and data-oriented workflows; upstream says its primary company focus shifted |
| [LangChain](https://github.com/langchain-ai/langchain) | CANDIDATE | Provider/tool/retrieval ecosystem; measure overlap with LangGraph |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | CANDIDATE | Higher-level planning and subagent harness |
| [Vercel AI SDK](https://github.com/vercel/ai) | CANDIDATE | TypeScript model abstraction, streaming and tool loops |
| [BeeAI Framework](https://github.com/i-am-bee/beeai-framework) | CANDIDATE | Python/TypeScript, governance patterns, A2A/MCP |
| [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) | CONDITIONAL | Official Claude Code loop; provider terms and executor boundary review required |
| [AG2](https://github.com/ag2ai/ag2) | CANDIDATE | Community-maintained multi-agent patterns after AutoGen |
| [AgentScope](https://github.com/agentscope-ai/agentscope) | CANDIDATE | Event-driven runtime, tool sandboxing and human approval |
| [Dapr Agents](https://github.com/dapr/dapr-agents) | CANDIDATE | Durable workflows, virtual actors, pub/sub and recovery |
| [Agent Squad](https://github.com/2FastLabs/agent-squad) | CANDIDATE | Intent routing and specialized-agent coordination |
| [DSPy](https://github.com/stanfordnlp/dspy) | CANDIDATE | Declarative and optimizable LM programs |
| [Genkit](https://github.com/firebase/genkit) | CANDIDATE | Typed flows, tools, retrieval and evaluation |
| [Mirascope](https://github.com/Mirascope/mirascope) | CANDIDATE | Code-first typed model calls and tool loops |
| [Atomic Agents](https://github.com/Eigenwise/atomic-agents) | CANDIDATE | Schema-driven components and explicit I/O |
| [VoltAgent](https://github.com/VoltAgent/voltagent) | CANDIDATE | TypeScript agents, supervisors, workflows and telemetry |
| [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit) | CANDIDATE | Framework-agnostic profiling and evaluation |
| [Rig](https://github.com/0xPlaygrounds/rig) | CANDIDATE | Rust LLM applications, tools, providers and RAG |
| [Langroid](https://github.com/langroid/langroid) | CANDIDATE | Message-passing agents and delegation |
| [MetaGPT](https://github.com/FoundationAgents/MetaGPT) | CANDIDATE | Specialized software roles and spec/code/test generation |
| [OGX](https://github.com/ogx-ai/ogx) | CANDIDATE | Agentic API, tools/MCP and RAG; verify project ownership and boundaries |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | REFERENCE ONLY | README points new work to Microsoft Agent Framework |
| [Microsoft AutoGen](https://github.com/microsoft/autogen) | EXCLUDED | README says archived/no longer maintained and directs to Agent Framework |

## 3. Coding agents and executor harnesses

| Candidate | Status | Capability to inspect |
|---|---|---|
| [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk) | CANDIDATE | Hosted coding runtime, container-backed execution and REST/WebSocket control |
| [OpenHands / Agent Canvas](https://github.com/OpenHands/OpenHands) | CANDIDATE | Frontend/control center; distinct from its engine SDK |
| [Goose](https://github.com/aaif-goose/goose) | CANDIDATE | Local/desktop/CLI agent, providers, MCP and ACP |
| [OpenCode](https://github.com/anomalyco/opencode) | CANDIDATE | Coding engine/API, model handling, build/plan modes |
| [Cline](https://github.com/cline/cline) | CANDIDATE | Agent SDK/core, IDE/CLI, checkpoints and human review |
| [Aider](https://github.com/Aider-AI/aider) | CANDIDATE | Git-aware coding, repo map and edit/test/commit loop |
| [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) | CANDIDATE | Minimal issue-to-code executor and benchmark baseline |
| [OpenAI Codex CLI](https://github.com/openai/codex) | CANDIDATE | Terminal coding agent and sandbox patterns |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | CANDIDATE | Terminal coding agent; never replace/bypass MediaHub's approved Gemini Actions transport |
| [Qwen Code](https://github.com/QwenLM/qwen-code) | CANDIDATE | Coding harness and model flexibility |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | CANDIDATE | General agent loop, tools and memory; assess personal-agent assumptions |
| [Open Interpreter](https://github.com/OpenInterpreter/open-interpreter) | CONDITIONAL | Local computer/code execution; sandbox is a gate |
| [Docker Agent](https://github.com/docker/docker-agent) | CANDIDATE | Declarative agent specs, toolsets and multi-agent flows |
| [Kilo Code](https://github.com/Kilo-Org/kilocode) | CANDIDATE | Coding frontends and OpenCode-derived parts; license blob c5762eb3ad5a0e1788ef155772fe3c240ab23e42 |
| [Pi agent](https://github.com/earendil-works/pi) | CANDIDATE | Small/injectable loop useful as a custom-harness baseline |
| [Continue](https://github.com/continuedev/continue) | CANDIDATE | IDE/CLI/code-assistant SDK patterns |
| [OpenClaw](https://github.com/openclaw/openclaw) | CANDIDATE | Broad personal-assistant runtime; assess corporate threat/data model |
| [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) | CONDITIONAL | Claude executor candidate; separate from routing and authorization |

Demoted/excluded: [SWE-agent v1](https://github.com/SWE-agent/SWE-agent), whose upstream recommends mini-SWE-agent; [Roo Code](https://github.com/RooCodeInc/Roo-Code), whose GitHub metadata returned archived=true on 2026-10-23. The [Coding-Agent Harness Study](https://github.com/SteveVitali/coding-agent-harness-study) is a pinned August 2026 starting point only; recheck fast-moving sources.

## 4. Durable workflows and schedulers

| Candidate | Status | Capability to inspect |
|---|---|---|
| [Temporal](https://github.com/temporalio/temporal) | CANDIDATE | Durable execution, retries, recovery, signals and versioning |
| [Restate](https://github.com/restatedev/restate) | CANDIDATE | Durable services and resumable execution |
| [DBOS Transact](https://github.com/dbos-inc/dbos-transact-ts) | CANDIDATE | Durable application functions and database-aligned workflows |
| [Inngest](https://github.com/inngest/inngest) | CANDIDATE | Event-driven durable jobs |
| [Prefect](https://github.com/PrefectHQ/prefect) | CANDIDATE | Observable tasks, retries and schedules |
| [Dagster](https://github.com/dagster-io/dagster) | CANDIDATE | Data/asset lineage and event-driven execution |
| [Trigger.dev](https://github.com/triggerdotdev/trigger.dev) | CANDIDATE | Background jobs and long-running tasks |
| [Argo Workflows](https://github.com/argoproj/argo-workflows) | CANDIDATE | Kubernetes-native DAGs and isolated steps |
| [Argo Events](https://github.com/argoproj/argo-events) | CANDIDATE | Event sources and workflow triggers |
| [Kestra](https://github.com/kestra-io/kestra) | CANDIDATE | Declarative workflows, scheduler and plugin tasks |
| [Flyte](https://github.com/flyteorg/flyte) | CANDIDATE | Typed/reproducible workflow and compute orchestration |

## 5. Gateways, model routers and local serving

| Candidate | Status | Capability to inspect |
|---|---|---|
| [LiteLLM](https://github.com/BerriAI/litellm) | CANDIDATE | Provider normalization, routing and quota/spend controls |
| [Bifrost](https://github.com/maximhq/bifrost) | CANDIDATE | Multi-provider gateway; queried default branch was dev |
| [vLLM Semantic Router](https://github.com/vllm-project/semantic-router) | CANDIDATE | Policy-driven model/compute selection |
| [Portkey Gateway](https://github.com/Portkey-AI/gateway) | CONDITIONAL | README describes 2.0 as pre-release/transition |
| [Helicone](https://github.com/Helicone/helicone) | CONDITIONAL | Gateway/observability; automatic fallback must not bypass MediaHub route policy |
| [vLLM](https://github.com/vllm-project/vllm) | CANDIDATE | High-throughput model serving |
| [SGLang](https://github.com/sgl-project/sglang) | CANDIDATE | Optimized model serving |
| [Ollama](https://github.com/ollama/ollama) | CANDIDATE | Local runtime only through qualified loopback/auth boundary |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | CANDIDATE | Quantized local inference engine |

## 6. Observability, evaluation, benchmarks and red team

| Candidate | Status | Capability to inspect |
|---|---|---|
| [Langfuse](https://github.com/langfuse/langfuse) | CANDIDATE | Traces, prompt versions, analytics and evaluations |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | CANDIDATE | LLM traces and evaluations |
| [Opik](https://github.com/comet-ml/opik) | CANDIDATE | Agent tracing, datasets and evaluations |
| [OpenLIT](https://github.com/openlit/openlit) | CANDIDATE | OpenTelemetry AI observability |
| [OpenLLMetry](https://github.com/traceloop/openllmetry) | CANDIDATE | OpenTelemetry instrumentation |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | CANDIDATE | Regression tests and red-team |
| [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) | CANDIDATE | Model/security evaluations and task suites |
| [DeepEval](https://github.com/confident-ai/deepeval) | CANDIDATE | Agent trajectory and LLM application evaluation |
| [Ragas](https://github.com/vibrantlabsai/ragas) | CANDIDATE | RAG/application evaluation |
| [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | CANDIDATE | Reproducible model benchmarks |
| [Giskard OSS](https://github.com/Giskard-AI/giskard-oss) | CANDIDATE | AI test and vulnerability evaluation |
| [garak](https://github.com/NVIDIA/garak) | CANDIDATE | LLM vulnerability probes |

## 7. Security policy, provenance and supply chain

| Candidate | Status | Capability to inspect |
|---|---|---|
| [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | CANDIDATE | Conversation/tool guardrails; never replace issuer/capability |
| [Guardrails AI](https://github.com/guardrails-ai/guardrails) | CANDIDATE | Output validation and structured guardrails |
| [Open Policy Agent](https://github.com/open-policy-agent/opa) | CANDIDATE | Policy-as-code evaluator |
| [Cedar](https://github.com/cedar-policy/cedar) | CANDIDATE | Authorization policy language/evaluator |
| [Sigstore Cosign](https://github.com/sigstore/cosign) | CANDIDATE | Artifact/container signing and verification |
| [in-toto](https://github.com/in-toto/in-toto) | CANDIDATE | Supply-chain steps and provenance |
| [SLSA GitHub generator](https://github.com/slsa-framework/slsa-github-generator) | CANDIDATE | GitHub Actions build provenance |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | CANDIDATE | Repository/security hygiene signals |
| [Syft](https://github.com/anchore/syft) | CANDIDATE | SBOM generation |
| [Trivy](https://github.com/aquasecurity/trivy) | CANDIDATE | Dependency, container and config scanning |
| [SPIRE](https://github.com/spiffe/spire) | CANDIDATE | Workload identity and attestation |
| [Smallstep Certificates](https://github.com/smallstep/certificates) | CANDIDATE | Certificate authority and workload TLS |
| [Backstage](https://github.com/backstage/backstage) | CANDIDATE | Developer portal/component catalog if a concrete need exists |

Archived: [LLM Guard](https://github.com/protectai/llm-guard), GitHub metadata returned archived=true on 2026-10-23. Exclude unless a maintained successor is identified.

## 8. Memory, retrieval, RAG and vector infrastructure

| Candidate | Status | Capability to inspect |
|---|---|---|
| [Mem0](https://github.com/mem0ai/mem0) | CANDIDATE | Memory extraction, scope and retrieval; separate OSS from hosted claims |
| [Graphiti](https://github.com/getzep/graphiti) | CANDIDATE | Temporal context graphs |
| [Letta](https://github.com/letta-ai/letta) | CANDIDATE | Stateful agents and editable/archival memory |
| [LangMem](https://github.com/langchain-ai/langmem) | CANDIDATE | Semantic, episodic and procedural memory |
| [Cognee](https://github.com/topoteretes/cognee) | CANDIDATE | Graph/vector knowledge engineering |
| [Hindsight](https://github.com/vectorize-io/hindsight) | CANDIDATE | Temporal memory and belief/observation networks |
| [Supermemory](https://github.com/supermemoryai/supermemory) | CANDIDATE | Memory API and context retrieval |
| [Memvid](https://github.com/memvid/memvid) | CANDIDATE | Portable/local indexed memory artifacts |
| [Haystack](https://github.com/deepset-ai/haystack) | CANDIDATE | Retrieval pipelines and agent blocks |
| [RAGFlow](https://github.com/infiniflow/ragflow) | CANDIDATE | Document parsing, hybrid retrieval and RAG flows |
| [txtai](https://github.com/neuml/txtai) | CANDIDATE | Embeddings, semantic search and local knowledge pipelines |
| [R2R](https://github.com/SciPhi-AI/R2R) | CANDIDATE | Ingestion, hybrid search, graph retrieval and APIs |
| [Onyx](https://github.com/onyx-dot-app/onyx) | CONDITIONAL | Enterprise search and permission-aware retrieval; review open-core |
| [Pathway / Serviette](https://github.com/pathwaycom/serviette) | CANDIDATE | Real-time retrieval templates; validate rename and exact source |
| [Khoj](https://github.com/khoj-ai/khoj) | CANDIDATE | Self-hosted knowledge agent and document search |
| [MindsDB Mindshub](https://github.com/mindsdb/mindshub) | CANDIDATE | Agents over federated data/connectors |
| [DocsGPT](https://github.com/arc53/DocsGPT) | CANDIDATE | Self-hostable documentation/search agent |
| [Qdrant](https://github.com/qdrant/qdrant) | CANDIDATE | Vector database |
| [Weaviate](https://github.com/weaviate/weaviate) | CANDIDATE | Vector/database retrieval layer |
| [Chroma](https://github.com/chroma-core/chroma) | CANDIDATE | Vector storage/retrieval API |
| [Milvus](https://github.com/milvus-io/milvus) | CANDIDATE | Scalable vector database |

## 9. Sandboxing, browser automation and protocols

| Candidate | Status | Capability to inspect |
|---|---|---|
| [OpenSandbox](https://github.com/opensandbox-group/OpenSandbox) | CANDIDATE | Isolated command/code/browser/desktop execution |
| [E2B](https://github.com/e2b-dev/E2B) | CONDITIONAL | Code sandboxes; compare self-hosted versus hosted-service dependence |
| [Browser Use](https://github.com/browser-use/browser-use) | CANDIDATE | Browser-agent loop |
| [Stagehand](https://github.com/browserbase/stagehand) | CANDIDATE | Browser-agent SDK |
| [Playwright](https://github.com/microsoft/playwright) | CANDIDATE | Deterministic browser automation/test primitive |
| [A2A](https://github.com/a2aproject/A2A) | CANDIDATE | Agent discovery/task interoperability; protocol does not grant authority |
| [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) | CANDIDATE | MCP client/server primitives |
| [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | CANDIDATE | MCP primitives |
| [MCP Go SDK](https://github.com/modelcontextprotocol/go-sdk) | CANDIDATE | MCP primitives |
| [Open Agent Schema Framework](https://github.com/agntcy/oasf) | CANDIDATE | Agent capability/skill metadata schema |
| [Agent Network Protocol](https://github.com/agent-network-protocol/AgentNetworkProtocol) | CANDIDATE | Alternate agent discovery/identity/messaging |
| [Composio](https://github.com/ComposioHQ/composio) | CONDITIONAL | SaaS/tool integrations; review scopes, secrets, licensing |

## 10. Visual product frameworks and optional voice

| Candidate | Status | Capability to inspect |
|---|---|---|
| [Dify](https://github.com/langgenius/dify) | CONDITIONAL | Self-hostable app/workflow product; licensing and parallel authority plane |
| [Langflow](https://github.com/langflow-ai/langflow) | CANDIDATE | Visual graph composition/API/MCP |
| [Rivet](https://github.com/Ironclad/rivet) | CANDIDATE | Visual graph editor/library |
| [Activepieces](https://github.com/activepieces/activepieces) | CONDITIONAL | Workflow automation; audit OSS/enterprise split |
| [n8n](https://github.com/n8n-io/n8n) | CONDITIONAL | Fair-code/source-available workflow product, not presumed OSI-open |
| [Pipecat](https://github.com/pipecat-ai/pipecat) | OPTIONAL DOMAIN | Real-time voice/multimodal pipeline |
| [LiveKit Agents](https://github.com/livekit/agents) | OPTIONAL DOMAIN | Real-time voice workers/transports |
| [Rasa](https://github.com/RasaHQ/rasa) | CONDITIONAL / OPTIONAL DOMAIN | Conversational workflow; queried default branch was 3.6.x, verify successor/release |

Archived visual reference: [Flowise](https://github.com/FlowiseAI/Flowise), GitHub metadata returned archived=true on 2026-10-23.

## 11. Inventory freeze gates — comparison intentionally deferred

1. Coverage: record date, query strings, screened results and exclusions from at least the four catalogs above plus direct GitHub searches across orchestration, coding executors, durable jobs, gateways/routing/serving, evaluation, security, memory/RAG, sandbox/browser, protocols/integrations, and telemetry/provenance.
2. Canonical identity: resolve renamed repositories and redirects; remove archived forks; treat a UI and its SDK/engine as one family where appropriate.
3. Source/version evidence: pin current upstream commit SHA, latest stable release/tag, license file/blob SHA, package manifest/lockfile SHA, CI/tests, advisories and maintenance window for every survivor.
4. License filter: separate OSI-approved OSS, open-core, source-available/fair-code, commercial-only and pre-release components.
5. Maturity filter: require activity, release discipline, tests and docs; flag abandoned/superseded and single-maintainer risk.
6. Security filter: reject/demote projects requiring uncontrolled secrets, implicit paid fallback, excessive permissions, unsandboxed host execution, unredacted telemetry or a competing authority/state plane.
7. Freeze: publish a dated immutable list with explicit included/excluded candidates and reasons. Only then start scored comparison.

## 12. Comparison and assembly phase after freeze

After the inventory-freeze gates pass, test the shortlisted options against the same workload and acceptance suite. Score documented evidence for functional fit, recovery/retries, least privilege, provider neutrality/budget, CI/test quality, observability, license/dependency health and integration cost. Popularity is not a substitute for measurements.

Build selected components by layer on an isolated prototype branch. A complete orchestrator replacement is allowed if demonstrably better and if the prototype preserves Baseline 2.0, historical IDs, a single MediaHub control plane/issuer/capability model, one Product State Authority, immutable provenance, no unauthorized paid fallback, fail-closed evidence, rollback, and separate execution/verification/qualification/deployment/acceptance states.

## 13. MediaHub state and active blockers

- Main SHA observed from repository-scoped GitHub commit search: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open. Agent admission remains behind issuer/ingress/lease/cancel/recovery, R-06 audit/privacy, accepted runner/workspace/network manifest, JSON Schema Draft 2020-12 meta-validation/negative fixtures and source-bound workflow hardening.
- Canonical map API returns an empty body even when base64 is requested; blob fallback content does not match the expected map. Map body NOT VERIFIED; no guessed edit.
- Bootstrap SHA 75f30750183efe8c6877368e9f0ada48f8e81ea7; checkpoint SHA b33b6be5702e30bda001745c6d71e11c4e843250; Master Roadmap SHA 21c4bf2702dbf636fa902f4f5716c6f39bb5dd1c.
- PR #585 is open/Draft/unmerged at previous head af793954d4ff4dc4ab4bb731e610bf651d87d222. Astra Verify run 39974471617/job 120485369174 and Cloud Runtime Validation run 39974471379/job 120485367072 passed at that head; formal review was empty. This register commit requires fresh exact-head checks/review.
- PR #583 is open/Draft/unmerged at 9de1526e6daa121c62aa85fc707d9a8c6f9e0d4d; Astra Verify 39973058604 and workflow contract validation 39973058901 failed. Logs show the same brittle test expects the literal line group: mediahub-gemini-controller-batch while the workflow uses an expression whose fallback is that value. The fix remains unapplied/unverified.
- No provider inference, Gemini dispatch, local installation, deployment, merge, comparison benchmark, inventory freeze or component adoption occurred in this discovery pass.

## 14. Next bounded action

Complete remaining category searches and exact maturity/license/source pins. Fix the proven brittle assertion in PR #583 on its own narrow branch and rerun exact-head CI; do not mix controller fixes into this research PR. Only after inventory-freeze gates close begin comparative testing and assembling components.
