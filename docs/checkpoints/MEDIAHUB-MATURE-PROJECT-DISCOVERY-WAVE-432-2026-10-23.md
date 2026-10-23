# MediaHub OS — Mature Project Discovery Register (Wave 432)

- Date: 2026-10-23
- Status: DISCOVERY CONTINUES / CANDIDATE CORPUS EXPANDED / COMPARISON AND ADOPTION NOT STARTED
- Immutable MediaHub base target SHA: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7
- Working branch: research/mature-ai-project-landscape-wave431-20261023
- Previous register: [Wave 431](MEDIAHUB-MATURE-OPEN-SOURCE-AI-LANDSCAPE-WAVE-431-2026-10-23.md)
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Canonical continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Governing Contour A issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Purpose and phase boundary

This pass expands discovery beyond Ruflo and the first set of agent frameworks. The landscape covers agent runtimes, coding executors, durable workflows, provider gateways, local model serving, telemetry/evaluation, policy testing, memory/RAG, browser automation, sandboxing, protocols and visual workflow products.

**This report does not rank or select the final implementation stack.** Wave 431 capability notes are research hypotheses, not scored comparison or an adoption decision. Per owner direction, formal side-by-side comparison and component assembly start only after the candidate inventory is screened and frozen.

“Search all GitHub” cannot honestly mean proving that every repository was enumerated. The operational definition is a repeatable discovery sweep across capability categories, cross-checked against independent landscape indexes, followed by source-level maturity screening. Discovery indexes consulted include the [Aglio Labs catalog of agent frameworks and orchestration tools](https://github.com/aglio-lab/ai-agent-frameworks), the [Langfuse framework survey](https://langfuse.com/blog/2025-03-19-ai-agent-comparison), and fresh repository-level searches. Catalogs and roundups are discovery aids only, not correctness, security, maintenance, license or benchmark evidence.

## 2. Screening states

- **CANDIDATE** — GitHub metadata observed this pass says the repository is active/not archived and it is relevant to a defined MediaHub subsystem; not yet qualified.
- **CONDITIONAL** — useful source candidate, but license, README, provider coupling, pre-release state or split OSS/enterprise boundary needs special review.
- **REFERENCE_ONLY** — useful for historical migration/provenance, but not recommended as the next active runtime.
- **EXCLUDED_FROM_ACTIVE_SHORTLIST** — repository was observed archived or maintainers explicitly point to an active successor.
- **NOT AUDITED** — exact immutable repo HEAD, release, license/blob SHA, manifests and lockfiles, CI/tests, advisories and runtime behavior are not all verified. README blob SHA is not a repository HEAD pin.

No candidate receives maturity PASS because of stars, size, a well-known sponsor or a polished README. Final admission needs exact source pinning, active-maintenance evidence, license/dependency/security review, CI/tests review, architecture fit and reproducible tests for the intended MediaHub use.

## 3. Candidate inventory

### A. Agent frameworks, orchestration and typed task contracts

| Candidate | Repository | Reason / evidence | Status |
|---|---|---|---|
| LangGraph | https://github.com/langchain-ai/langgraph | Stateful graph-shaped agent workflow; README blob 97c31e9cb4d8fe56be8d768ce3eb5e22400e897e | CANDIDATE |
| Microsoft Agent Framework | https://github.com/microsoft/agent-framework | Multi-agent workflows across Python/.NET; README blob bc9a8b080aeca9b3c5a25f216f8f96f61ffc012c | CANDIDATE |
| CrewAI | https://github.com/crewAIInc/crewAI | Role/task delegation; README blob 4a5360ad587a35625684747157881558c6acae1d | CANDIDATE |
| Ruflo | https://github.com/ruvnet/ruflo | Broad coding-agent harness; previous observed HEAD 88349655ebc2de8f9bf702aaf31d6be768e1ea11; re-pin current HEAD | CANDIDATE |
| Pydantic AI | https://github.com/pydantic/pydantic-ai | Typed outputs, validation, dependency injection; README blob 0d6afafd97a197da2d78b26e3b7aaf1c41d784b0 | CANDIDATE |
| OpenAI Agents SDK | https://github.com/openai/openai-agents-python | Handoffs, tools, guardrails and tracing; README blob 40f490c110cd584f7034bd221c6da37379fc41ff | CANDIDATE |
| Google ADK | https://github.com/google/adk-python | Agent composition and deployment; README blob 24f2b1f494b8298178ef73fd909c175508f4606a | CANDIDATE |
| Agno | https://github.com/agno-agi/agno | Self-hostable agent runtime, storage and memory; README blob 2813f35fa7620ff7d95465d853d7b0a6ee2c00b4 | CANDIDATE |
| Hugging Face smolagents | https://github.com/huggingface/smolagents | Small model-agnostic tool/code loop and local-model integrations; README blob 7c8af38d981a563add56db76b10cde810e010690 | CANDIDATE |
| Mastra | https://github.com/mastra-ai/mastra | TypeScript agents/workflows, routing, suspend/resume; README blob f6465bcaf53f737e3754c28660e142ca44e07c97 | CANDIDATE; audit OSS/enterprise boundary |
| Strands Agents | https://github.com/strands-agents/harness-sdk | Model-driven agent loop and harness; README blob 8deea9e1814068770e52cd91e729422eaa319a7e | CANDIDATE |
| LlamaIndex | https://github.com/run-llama/llama_index | Parsing, indexing, retrieval and agent workflows; README blob 572527a8f5293bcf001366da01e51549280ff2e0 | CONDITIONAL: README says OSS remains, primary company focus shifted to document products |
| LangChain | https://github.com/langchain-ai/langchain | Model/tool ecosystem around agents | CANDIDATE; measure overlap with LangGraph rather than counting as separate engine |
| Deep Agents | https://github.com/langchain-ai/deepagents | Higher-level long-horizon harness with planning/subagents | CANDIDATE; overlaps with LangGraph |
| Vercel AI SDK | https://github.com/vercel/ai | TypeScript model/tool primitives, streaming and application APIs | CANDIDATE; pin exact packages/subpaths |
| BeeAI Framework | https://github.com/i-am-bee/beeai-framework | Python/TypeScript agent workflows and interoperability | CANDIDATE; inspect current governance |
| Claude Agent SDK (Python) | https://github.com/anthropics/claude-agent-sdk-python | Official Claude Code harness integration for the Claude executor line | CONDITIONAL: vendor terms and provider-only behavior must be reviewed |
| Semantic Kernel | https://github.com/microsoft/semantic-kernel | Historical patterns/migration context; README blob 02cab29b8f983d06039752b7326c95ecca7a2891 | REFERENCE_ONLY for new runtime selection: README points to Microsoft Agent Framework as successor |

### B. Coding-agent executors and developer workbenches

| Candidate | Repository | Reason / evidence | Status |
|---|---|---|---|
| OpenHands / Agent Canvas | https://github.com/OpenHands/OpenHands | Developer-agent control center across local, remote and cloud backends; README blob 54f41832322ab4701c202a102cd4db23e3e4dc3a | CANDIDATE |
| Goose | https://github.com/aaif-goose/goose | Local/desktop/CLI agent, multiple providers and MCP; README blob 44c960f0193de1ccd3a13721cfe2daf5e7707ac5 | CANDIDATE |
| OpenCode | https://github.com/anomalyco/opencode | Terminal coding agent with build/plan modes; default branch observed as dev; README blob a8551f97c57f9140c4c2ce9f7c004dc4bc21954b | CANDIDATE |
| Cline | https://github.com/cline/cline | IDE/CLI/desktop agent and SDK with checkpoints; README blob 1b870599c7e12943b5a71b69c975744d61cbc25a | CANDIDATE |
| Aider | https://github.com/Aider-AI/aider | Git-oriented code editing, commits, lint/test loop; README blob 816c876cb67021fa9f8d37267c8e57923eabdb07 | CANDIDATE; audit maintenance cadence |
| mini-SWE-agent | https://github.com/SWE-agent/mini-swe-agent | Minimal coding executor and benchmark history; README blob 7db1d82dfa92eaa00adeb10c8681677a9e6ec639 | CANDIDATE; maintainers recommend it over older SWE-agent |
| OpenAI Codex CLI | https://github.com/openai/codex | Coding executor and sandbox/permission patterns | CANDIDATE; verify model and permission scope |
| Gemini CLI | https://github.com/google-gemini/gemini-cli | Coding executor and tool-use patterns | CANDIDATE; must not replace approved MediaHub Gemini GitHub Actions transport |
| Qwen Code | https://github.com/QwenLM/qwen-code | Coding executor and local/provider integration | CANDIDATE; route allowlists and security review required |
| Hermes Agent | https://github.com/NousResearch/hermes-agent | General-purpose agent, tools and memory | CANDIDATE; distinguish personal-agent assumptions from corporate multi-tenant needs |
| Open Interpreter | https://github.com/OpenInterpreter/open-interpreter | Agent/tool execution and local computer interaction | CONDITIONAL: inspect sandbox defaults and host permissions |
| Docker Agent | https://github.com/docker/docker-agent | Declarative YAML agent and toolsets; README blob d3daeb8ead7e59d1acc0b453d034429d5e0449a7 | CANDIDATE; test embedding without adding a second authority plane |

### C. Durable workflows and background execution

| Candidate | Repository | Reason / evidence | Status |
|---|---|---|---|
| Temporal | https://github.com/temporalio/temporal | Durable workflow state/retries/recovery; README blob d89e30ebb9863ea82c9203e1e696170ea9484af9 | CANDIDATE |
| Restate | https://github.com/restatedev/restate | Durable services and workflow recovery; README blob 6ef156693eb3452f01e17d4e4e69d9b4fcfa22bb | CANDIDATE |
| DBOS Transact TypeScript | https://github.com/dbos-inc/dbos-transact-ts | Durable application functions/workflows | CANDIDATE |
| Inngest | https://github.com/inngest/inngest | Event-driven durable functions/background jobs | CANDIDATE |
| Prefect | https://github.com/PrefectHQ/prefect | Workflow/task orchestration | CANDIDATE |
| Dagster | https://github.com/dagster-io/dagster | Data/asset orchestration patterns | CANDIDATE; likely specialized |
| Trigger.dev | https://github.com/triggerdotdev/trigger.dev | Background task execution | CANDIDATE; audit license/self-host limits |
| Argo Workflows | https://github.com/argoproj/argo-workflows | Kubernetes-native workflow/DAG execution | CANDIDATE; heavier infrastructure |
| Kestra | https://github.com/kestra-io/kestra | Declarative workflows and plugin execution | CANDIDATE; inspect deployment/license details |

### D. Provider routing and model serving

| Candidate | Repository | Reason / evidence | Status |
|---|---|---|---|
| LiteLLM | https://github.com/BerriAI/litellm | Normalized provider API and routing | CANDIDATE; version-specific security/advisory and no-paid-fallback test required |
| Bifrost | https://github.com/maximhq/bifrost | Multi-provider AI gateway; README blob eb28462fd74d6d76d3681b4ac3947ae91bb34495 | CANDIDATE; default branch observed as dev |
| vLLM Semantic Router | https://github.com/vllm-project/semantic-router | Policy-driven model/compute selection; README blob 768312ccf41c5ac38239328a9d283c9dee7fab71 | CANDIDATE |
| Portkey AI Gateway | https://github.com/Portkey-AI/gateway | Provider normalization/routing; README blob 199b744cab2e0a3cf48f98a44782aeda482fc0f1, MIT license blob 2c0759f826129145c2b8d792ad1160a0b6342448 | CONDITIONAL: README says 2.0 is pre-release/transition |
| Helicone | https://github.com/Helicone/helicone | Gateway plus LLM observability; README blob 0bfc46167e1a9056c564bf67173641f3dd96d498, license blob 4a1ada09a20596ca4619e4f2001104cf743a10fa | CONDITIONAL: default fallback capability must never bypass explicit provider/budget allowlists |
| vLLM | https://github.com/vllm-project/vllm | High-throughput model serving | CANDIDATE; serving, not controller |
| SGLang | https://github.com/sgl-project/sglang | Model serving/runtime | CANDIDATE |
| Ollama | https://github.com/ollama/ollama | Local model management and inference API | CANDIDATE; require qualified loopback/auth boundary |
| llama.cpp | https://github.com/ggml-org/llama.cpp | Local quantized inference engine | CANDIDATE; serving layer only |

### E. Tracing, evaluation and regression testing

| Candidate | Repository | Reason / evidence | Status |
|---|---|---|---|
| Langfuse | https://github.com/langfuse/langfuse | LLM traces, prompt/version management and evaluation; README blob 3c4ad5773b846b6b1c16355640ebd87ff031f92e | CANDIDATE |
| Arize Phoenix | https://github.com/Arize-ai/phoenix | LLM tracing/evaluation; README blob 57e2f3ff4099ee6d45f21160dd2d2f504809e2b6 | CANDIDATE |
| Opik | https://github.com/comet-ml/opik | Agent tracing/evaluation; README blob f0379f032b170fa4e9a328abcc235617b3e163e1 | CANDIDATE |
| OpenLIT | https://github.com/openlit/openlit | OpenTelemetry-aligned LLM observability | CANDIDATE |
| OpenLLMetry | https://github.com/traceloop/openllmetry | OpenTelemetry instrumentation for LLM applications | CANDIDATE; avoid duplicate tracing layers without proven need |
| Promptfoo | https://github.com/promptfoo/promptfoo | Prompt regression, LLM evaluation and red-team tests; README blob a6713365c28b9e7949b2b4c2ba87845dd50e0ce3 | CANDIDATE |
| Inspect AI | https://github.com/UKGovernmentBEIS/inspect_ai | Model/security evaluation tasks; README blob d4081077fc07881e696a7005a8ea0b0b6464e001 | CANDIDATE |
| DeepEval | https://github.com/confident-ai/deepeval | Unit-test-style LLM and agent trajectory evaluation; README blob 3a0898fcf91d70f1b2643c1fc8851ffaee054700 | CANDIDATE |
| Ragas | https://github.com/vibrantlabsai/ragas | RAG/application evaluation; README blob 07b1f00fde50ee8506f3087326285041c1a1a05c | CANDIDATE |
| lm-evaluation-harness | https://github.com/EleutherAI/lm-evaluation-harness | Reproducible model benchmarks | CANDIDATE; benchmark layer |
| Giskard OSS | https://github.com/Giskard-AI/giskard-oss | AI testing and evaluation | CANDIDATE; inspect current OSS/enterprise boundary |

### F. Guardrails, memory, retrieval and knowledge

| Candidate | Repository | Reason / evidence | Status |
|---|---|---|---|
| NVIDIA NeMo Guardrails | https://github.com/NVIDIA-NeMo/Guardrails | Conversation/tool guardrail patterns; README blob 0e89130b921f58db81c27ff2d8fc990b58fbcff1 | CANDIDATE; never replaces issuer/capability |
| Guardrails AI | https://github.com/guardrails-ai/guardrails | Output validation and structured guardrails; README blob ad2b492d82205b633d8298bc58ab22d120b56b0e | CANDIDATE |
| Mem0 | https://github.com/mem0ai/mem0 | Agent memory and retrieval; README blob c9ed6dbfbe14a2fe60b8f3761a083786157a6987 | CANDIDATE; separate OSS and managed-platform claims |
| Graphiti | https://github.com/getzep/graphiti | Temporal context graph and agent memory; README blob dc1d339d13d77b6cccb9d00af54b5f15665760bd | CANDIDATE |
| Haystack | https://github.com/deepset-ai/haystack | Composable retrieval/agent pipelines; README blob afa079b2a7e90e815fdaf9b09edcd7ad010e3e91 | CANDIDATE |
| Qdrant | https://github.com/qdrant/qdrant | Vector retrieval/storage substrate | CANDIDATE; data subsystem |
| Weaviate | https://github.com/weaviate/weaviate | Vector retrieval/database substrate | CANDIDATE; data subsystem |
| Chroma | https://github.com/chroma-core/chroma | Vector store | CANDIDATE; data subsystem |
| Milvus | https://github.com/milvus-io/milvus | Scalable vector database | CANDIDATE; data subsystem |

### G. Sandboxing, browser automation, protocols and integrations

| Candidate | Repository | Reason / evidence | Status |
|---|---|---|---|
| OpenSandbox | https://github.com/opensandbox-group/OpenSandbox | Isolated code/command/file/browser/desktop environments; README blob f5c62efcbcdd8582785229c731df4ead54ccbf98 | CANDIDATE; E2E/Kubernetes workflow badges observed |
| E2B | https://github.com/e2b-dev/E2B | Sandboxed code execution | CANDIDATE; inspect hosted vs self-host boundary |
| Browser Use | https://github.com/browser-use/browser-use | Browser automation agent; README blob fe0d153c091192af376573013bf27974de9169ff | CANDIDATE; audit cloud/local modes |
| Stagehand | https://github.com/browserbase/stagehand | Browser-agent SDK; README blob b474ec5e4861b4e1dc10ca1f81ebf3cfe77966f0 | CANDIDATE |
| Playwright | https://github.com/microsoft/playwright | Deterministic browser automation/testing primitive | CANDIDATE; baseline comparator, not autonomous agent |
| A2A | https://github.com/a2aproject/A2A | Agent interoperability protocol | CANDIDATE; protocol alone grants no authority |
| MCP TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk | Tool/server protocol implementation | CANDIDATE; select each server individually |
| MCP Go SDK | https://github.com/modelcontextprotocol/go-sdk | Go protocol implementation | CANDIDATE; protocol only |
| Composio | https://github.com/ComposioHQ/composio | Tool integrations and execution adapters | CONDITIONAL; inspect external-service assumptions, scopes and licensing |

### H. Workflow product surfaces and automation

| Candidate | Repository | Reason / evidence | Status |
|---|---|---|---|
| Dify | https://github.com/langgenius/dify | AI application/workflow platform | CONDITIONAL; license and parallel control-plane/state ownership review |
| Langflow | https://github.com/langflow-ai/langflow | Visual workflow composition | CANDIDATE; UX/prototyping, not presumed production authority |
| Activepieces | https://github.com/activepieces/activepieces | Workflow automation/integrations | CONDITIONAL; audit OSS/enterprise split and license |
| n8n | https://github.com/n8n-io/n8n | Broad automation workflow ecosystem | CONDITIONAL; do not presume OSI-open or production-compatible licensing |

## 4. Excluded or demoted after read-back

| Repository | Observed status | Decision |
|---|---|---|
| https://github.com/microsoft/autogen | README states archived/no longer maintained and redirects to Microsoft Agent Framework | EXCLUDED_FROM_ACTIVE_SHORTLIST; historical reference only |
| https://github.com/FlowiseAI/Flowise | GitHub metadata returned archived=true | EXCLUDED_FROM_ACTIVE_SHORTLIST |
| https://github.com/RooCodeInc/Roo-Code | GitHub metadata returned archived=true | EXCLUDED_FROM_ACTIVE_SHORTLIST |
| https://github.com/daytonaio/daytona | GitHub metadata returned archived=true | EXCLUDED_FROM_ACTIVE_SHORTLIST |
| https://github.com/protectai/llm-guard | GitHub metadata returned archived=true | EXCLUDED_FROM_ACTIVE_SHORTLIST; investigate maintained successors if needed |
| https://github.com/SWE-agent/SWE-agent | README says active effort moved to mini-swe-agent and recommends the successor | REFERENCE_ONLY; test mini-swe-agent instead |
| https://github.com/microsoft/semantic-kernel | README points to Microsoft Agent Framework as successor | REFERENCE_ONLY for a new runtime decision |

Archive status is a point-in-time observation from GitHub repository metadata on 2026-10-23; recheck before final selection.

## 5. Discovery coverage and inventory-freeze gate

The inventory is **not frozen yet**. The next discovery phase must record exact search queries, candidate repositories inspected and exclusion reasons.

- [x] Agent frameworks and multi-agent orchestration — repository searches, external survey, metadata and selected READMEs.
- [x] Coding-agent runners and workbenches — repository metadata, selected READMEs and an independent October 2026 landscape.
- [x] Durable workflows — representative engines discovered; reliability comparison not started.
- [x] Provider gateways, model routers and local model servers — several independent candidates discovered; none deployed.
- [x] Observability, evaluation, red-teaming and guardrails — several candidates discovered.
- [x] Memory/RAG, vector storage, sandboxing, browser automation and agent protocols — initial cross-category set discovered.
- [ ] Finish searches for additional first-party/foundation-backed projects in each subsystem and log exact queries/results.
- [ ] For every shortlisted repository pin immutable HEAD SHA, latest release/tag, license file/blob SHA, root manifest and lockfile, CI/test evidence, security advisories and maintainer/commit activity.
- [ ] Resolve overlaps, provider coupling and license conditions; remove candidates that fail maintenance/license/security gates or mark them reference-only.
- [ ] Publish a frozen candidate list and evidence manifest. Only then begin the formal comparison matrix.
- [ ] After comparison, build narrow adapters/fixtures from selected components in an isolated branch; preserve one MediaHub control plane and one Product State Authority.

## 6. MediaHub state and governance evidence

- Main target from repository-scoped GitHub commit search: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open. It requires issuer/ingress/lease/cancel/recovery and R-06 audit/privacy gates, an authoritative runner/workspace/network manifest, Draft 2020-12 schema meta-validation/negative fixtures and source-bound workflow hardening before agent admission.
- Canonical map path returned blob SHA 78fa7dfa02357fe9e95645843e583f8802867d78, but GitHub file content was empty (also with base64 requested) and blob fallback content did not match the map. Map body remains NOT VERIFIED; no guessed edit was made.
- Bootstrap blob SHA 75f30750183efe8c6877368e9f0ada48f8e81ea7 was read back; it confirms Baseline 2.0 is the accepted current functional baseline and that map recovery is required before map updates.
- Checkpoint blob SHA b33b6be5702e30bda001745c6d71e11c4e843250 (436,052 characters); Master Roadmap blob SHA 21c4bf2702dbf636fa902f4f5716c6f39bb5dd1c (805,397 characters). Relevant recent sections were read, including the Wave 429 local FCC blocker.
- PR #585 remains open, Draft, unmerged and based on main SHA f0448f28c7cfa61e4450c38529f09afbfdbbc7c7. Previous head af793954d4ff4dc4ab4bb731e610bf651d87d222 passed Astra Verify run [39974471617](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39974471617), job 120485369174, and Astra Cloud Runtime Validation run [39974471379](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39974471379), job 120485367072. Formal review list was empty. This commit will trigger new exact-head verification.
- PR #583 remains open, Draft, unmerged. Its observed head 9de1526e6daa121c62aa85fc707d9a8c6f9e0d4d failed Astra Verify [39973058604](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058604) and workflow contract validation [39973058901](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058901). Both logs identify the same brittle test, test_pr_probe_concurrency_isolated_from_long_running_agent_batch: it asserts a literal “group: mediahub-gemini-controller-batch”, while the workflow uses a GitHub expression whose fallback is “mediahub-gemini-controller-batch”. This is the evidenced failure cause; a narrow fix must retain semantic checks that PR probe concurrency is isolated from the serialized dispatch group. No fix or rerun was performed in this discovery pass.
- No Gemini controller/child dispatch, provider inference, secret read, local installation, deployment, merge, runtime qualification, inventory freeze, component assembly or Contour A acceptance occurred in this pass.

## 7. Next bounded package

1. Complete final subsystem searches and source screening; remove archived/superseded candidates and flag source-available/license boundaries.
2. Pin every remaining candidate at a commit SHA and collect release, license, manifest/lockfile, CI/test and advisory evidence.
3. Fix PR #583's brittle assertion in a separate bounded branch, rerun contract tests/exact-head CI and obtain independent review.
4. Refresh PR #585 exact-head CI after adding this report and obtain independent review. Do not update the canonical map until its body can be read and verified.
5. Freeze the candidate inventory only when completeness is evidenced; then start side-by-side comparison and component assembly.

**Disposition:** discovery expanded; archive/successor exclusions evidenced; inventory remains open; formal comparison and implementation NOT STARTED; Contour A NOT ACCEPTED.
