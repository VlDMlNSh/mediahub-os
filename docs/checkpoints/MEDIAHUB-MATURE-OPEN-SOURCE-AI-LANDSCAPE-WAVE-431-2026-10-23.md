# MediaHub OS — Mature Open-Source AI Engineering Landscape (Wave 431)

- Date: 2026-10-23
- Status: **RESEARCH SNAPSHOT / CANDIDATE REGISTER / NOT A QUALIFICATION OR ADOPTION DECISION**
- Immutable MediaHub base target SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Canonical continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Governing Contour A issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Scope and evidence standard

This is the first consolidated landscape pass, not a claim that every GitHub repository has been exhaustively enumerated. GitHub repository search was sampled across agent frameworks, durable workflow engines, model gateways, observability, evaluation, guardrails, and coding-agent workbenches. For representative projects, repository metadata and README content were fetched directly through GitHub at the observed default branch. A README/metadata read is evidence of project scope and repository presence, not proof of production suitability, security, maintenance quality, benchmark performance, or license compatibility.

The next qualification pass must pin immutable commit SHAs and inspect release history, license files, dependency manifests/lockfiles, security advisories, CI/test configuration, maintainers, open critical issues, data flow, permission model, and the exact component proposed for reuse. Scores are intentionally not fabricated where those checks have not been completed.

### Selection criteria

1. **Control-plane compatibility:** can the component be used behind MediaHub's existing issuer/capability checks and MediaHub Product State Authority?
2. **Durable execution:** idempotency, retry policy, cancellation, timeouts, recovery, leases/fencing, reconciliation and observable terminal states.
3. **GitHub-native engineering fit:** immutable source SHA, branch/PR workflows, artifact provenance, test gates and clean failure semantics.
4. **Provider neutrality and cost policy:** explicit provider/model routing, quota awareness, no implicit paid fallback, and auditable route selection.
5. **Security boundary:** least privilege, secret isolation, sandboxing, prompt/tool-injection controls and data minimization.
6. **Operational maturity:** active maintained codebase, CI and tests, usable docs, release discipline, ecosystem and migration cost.
7. **Adoption economics:** reuse a narrow component/algorithm where possible; avoid importing an entire runtime unless a prototype proves it superior.

## 2. Candidate register

| Layer | Project | Observed source | Strongest candidate contribution | Adoption posture |
|---|---|---|---|---|
| Stateful agent orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) | Default branch `main`; README blob `97c31e9cb4d8fe56be8d768ce3eb5e22400e897e` | Stateful graph execution for long-running agent flows; inspect checkpointing, interrupts and recovery semantics | **High-priority architecture reference**; prototype only behind MediaHub contracts |
| Multi-language agent framework | [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | `main`; README blob `bc9a8b080aeca9b3c5a25f216f8f96f61ffc012c` | Production-oriented Python/.NET agent workflows and hosting patterns | **High-priority comparison**; note that it is the successor direction for AutoGen |
| Agent collaboration / task delegation | [CrewAI](https://github.com/crewAIInc/crewAI) | `main`; README blob `4a5360ad587a35625684747157881558c6acae1d` | Role/task-oriented delegation patterns and workflow ergonomics | **Pattern donor**; test deterministic execution and authority boundaries |
| Typed agent runtime | [Pydantic AI](https://github.com/pydantic/pydantic-ai) | `main`; README blob `0d6afafd97a197da2d78b26e3b7aaf1c41d784b0` | Typed tool/model contracts, validation and structured outputs | **High-priority pattern donor** for schema-bound task envelopes and outputs |
| Agent handoffs and guardrails | [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | `main`; README blob `40f490c110cd584f7034bd221c6da37379fc41ff` | Handoffs, tools, guardrails, tracing; provider compatibility claimed by upstream | **Pattern donor**; verify route control and no-paid-fallback policy before use |
| Agent development kit | [Google ADK Python](https://github.com/google/adk-python) | `main`; README blob `24f2b1f494b8298178ef73fd909c175508f4606a` | Agent composition and deployment patterns; README declares Apache-2.0 | **Comparison candidate**; evaluate portability and runtime coupling |
| Broad agent harness | [Ruflo](https://github.com/ruvnet/ruflo) | Prior observed HEAD `88349655ebc2de8f9bf702aaf31d6be768e1ea11`; prior package version `3.59.17`; prior MIT license blob `5c4718198a4156beacc780980077043a98b0dd6a` | Broad multi-agent harness, tool/MCP integration and tested GitHub mutation failure semantics | **Do not dismiss as a whole-runtime option**; compare against MediaHub using a bounded adapter prototype and explicit authority mapping |
| Coding-agent workbench | [OpenHands / Agent Canvas](https://github.com/OpenHands/OpenHands) | `main`; README blob `54f41832322ab4701c202a102cd4db23e3e4dc3a` | Unified interface for coding agents and local/remote/cloud execution backends | **High-priority executor/workbench reference**, not a replacement for MediaHub governance |
| Research-agent application | [DeerFlow](https://github.com/bytedance/deer-flow) | `main`; README blob `93b78f53e627660da5c83a4b1d778b7c098b5490`; README declares MIT | Research workflow composition, scoped sub-agents and artifact-oriented output | **Workflow pattern donor**; not presumed to be a general corporate control plane |
| RAG and agent pipelines | [Haystack](https://github.com/deepset-ai/haystack) | `main`; README blob `afa079b2a7e90e815fdaf9b09edcd7ad010e3e91` | Composable pipelines, retrieval and tool/agent building blocks | **Domain-specific donor** for knowledge/RAG, not core scheduler |
| Durable workflow execution | [Temporal](https://github.com/temporalio/temporal) | `main`; README blob `d89e30ebb9863ea82c9203e1e696170ea9484af9` | Durable workflows, retry/recovery across process failures | **Highest-priority reliability reference**; compare operational cost and persistence needs before adoption |
| Durable async services | [Restate](https://github.com/restatedev/restate) | `main`; README blob `6ef156693eb3452f01e17d4e4e69d9b4fcfa22bb` | Durable execution and resilient event-driven services | **Temporal alternative**; benchmark replay/idempotency/cancellation fit |
| Transactional workflow patterns | [DBOS Transact](https://github.com/dbos-inc/dbos-transact-ts) | `main`; repository metadata only in this pass | Durable functions/workflow patterns close to application/database transactions | **Secondary comparison**; inspect activity, ecosystem and production evidence before prioritizing |
| Model gateway / provider adapter | [LiteLLM](https://github.com/BerriAI/litellm) | `main`; README blob `5fd84b529dc66aa71c36fb7e5188303e7432613d` | Broad provider API normalization, gateway, spend and routing features | **Capability reference, security review required**; do not add dependency or deploy until release/advisory/dependency audit and exact no-paid-fallback tests pass |
| Model gateway | [Bifrost](https://github.com/maximhq/bifrost) | Observed default branch `dev`; README blob `eb28462fd74d6d76d3681b4ac3947ae91bb34495` | Gateway architecture and high-throughput provider interface | **High-priority LiteLLM alternative**; inspect license, provider policy, telemetry and routing failure semantics |
| Model/compute decision layer | [vLLM Semantic Router](https://github.com/vllm-project/semantic-router) | `main`; README blob `768312ccf41c5ac38239328a9d283c9dee7fab71` | Policy-driven model/compute selection | **Routing-policy donor**; must preserve explicit allowed-provider and budget allowlists |
| LLM tracing and prompt analytics | [Langfuse](https://github.com/langfuse/langfuse) | `main`; README blob `3c4ad5773b846b6b1c16355640ebd87ff031f92e` | Tracing, prompt/version observability and evaluation workflow | **High-priority observability candidate**; assess data residency, redaction and self-hosting |
| LLM tracing/evaluation | [Arize Phoenix](https://github.com/Arize-ai/phoenix) | `main`; README blob `57e2f3ff4099ee6d45f21160dd2d2f504809e2b6` | OpenTelemetry-oriented traces and evaluation workflows | **Observability alternative**; compare data handling and deployment footprint |
| Agent/LLM observability | [Comet Opik](https://github.com/comet-ml/opik) | `main`; README blob `f0379f032b170fa4e9a328abcc235617b3e163e1` | Agent traces, evaluations and operational visibility | **Observability alternative**; compare with Langfuse/Phoenix using same test traces |
| Runtime guardrails | [NVIDIA NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | `develop`; README blob `0e89130b921f58db81c27ff2d8fc990b58fbcff1`; README declares Apache-2.0 | Programmable conversation/tool guardrails | **Security-pattern donor**, never substitute for issuer/capability enforcement |
| LLM evaluation and red-team tests | [Promptfoo](https://github.com/promptfoo/promptfoo) | `main`; README blob `a6713365c28b9e7949b2b4c2ba87845dd50e0ce3`; README declares MIT | Regression evaluations, red-team and policy testing | **High-priority test harness candidate** for prompt/tool/data-route regression suites |
| Visual AI application platform | [Dify](https://github.com/langgenius/dify) | `main`; repository metadata only in this pass | Full product surface for workflow/RAG/app building | **Compare as product subsystem only**; avoid introducing a parallel authority/state plane |
| Visual flow builder | [Langflow](https://github.com/langflow-ai/langflow) | `main`; repository metadata only in this pass | Visual composition/prototyping | **UX/prototyping reference**, not a production governance replacement |
| MCP server ecosystem | [MCP Servers](https://github.com/modelcontextprotocol/servers) | `main`; repository metadata only in this pass | Reference integrations and protocol examples | **Select per server**, pin and sandbox individually; do not trust the catalog as an allowlist |
| Workflow/agent application framework | [Microsoft AutoGen](https://github.com/microsoft/autogen) | `main`; README blob `042b9df197a220ec7072a116d694cd497ec332ad` | Historical multi-agent patterns | **Do not select as a new runtime**: upstream README marks repository archived and points to Microsoft Agent Framework |

## 3. Cross-project synthesis: strongest properties to borrow

| Capability | Best sources to study first | What MediaHub should extract | Non-negotiable adaptation |
|---|---|---|---|
| Durable execution/recovery | Temporal, Restate, LangGraph | Explicit state transitions, retry budgets, cancellation, replay/reconciliation, durable execution journals | GitHub run/job/artifact IDs remain evidence; no hidden second state authority |
| Multi-agent orchestration | Microsoft Agent Framework, LangGraph, Ruflo, CrewAI | Bounded delegation, dependency graphs, role-specific contracts, explicit handoffs | One controller/issuer; no agent can self-grant capability or promote its own output |
| Typed contracts and output validation | Pydantic AI, OpenAI Agents SDK | Strict typed envelopes, structured outputs, schema-first validation, typed tool results | Draft 2020-12 validation and negative fixtures remain mandatory for MediaHub envelopes |
| Coding executor abstraction | OpenHands, Ruflo | Adapter boundary for different executors, sandboxed workspaces, structured task/result lifecycle | Provider and executor identity, capabilities, source SHA and route policy must be checked before execution |
| Model/provider routing | Bifrost, LiteLLM, vLLM Semantic Router | Provider adapters, normalized errors, model selection policy, health/quota signals | Explicit provider/model allowlists, budget ceiling, quota-aware resume, no paid fallback unless separately authorized |
| Evaluation and security regression | Promptfoo, NeMo Guardrails | Repeatable red-team, prompt-injection, tool policy and model-output regression suites | Guardrails complement, never replace, issuer/capability and GitHub permission checks |
| Observability | Langfuse, Phoenix, Opik | Correlated traces, latency/cost attribution, evaluation lineage | Minimize payloads; redact secrets and personal content; preserve local-first/data-classification constraints |
| Retrieval/knowledge pipelines | Haystack, DeerFlow | Modular retrieval and evidence-producing research tasks | Knowledge/data access stays scoped to approved workload and source allowlists |
| GitHub mutation reliability | Ruflo commit `88349655ebc2de8f9bf702aaf31d6be768e1ea11` | Test failures as first-class; never claim PR/issue mutation succeeded without exact operation and read-back evidence | Use MediaHub's existing GitHub transport and provenance contract; no alternate credential or mutation plane |

## 4. Candidate scoring policy

Do not rank projects by stars, repository size or README claims alone. The next pass should score each shortlisted project 0–5 on:
- functional fit;
- durable recovery/idempotency;
- least-privilege/security;
- provider neutrality and budget enforcement;
- test/CI quality;
- maintenance/release health;
- license and dependency compatibility;
- integration/migration cost.

Each score must link to concrete code/tests/releases/advisories, not reputation. Security, authority compatibility, and no-paid-fallback compliance are **gates**, not dimensions that can be averaged away by popularity. Any candidate failing a gate remains reference-only.

## 5. Preliminary architecture decision

**Do not choose a single replacement framework yet.** Use a modular comparative strategy:
1. Keep MediaHub issuer/capability, Product State Authority, Baseline 2.0 and GitHub controller contracts as the acceptance boundary.
2. Compare Temporal and Restate against the existing GitHub Actions controller for durable recovery needs; first identify which failures GitHub Actions already handles adequately.
3. Prototype the orchestration adapter against LangGraph, Microsoft Agent Framework and Ruflo using the same bounded task envelope, same target SHA, same test suite and same failure injection.
4. Compare Bifrost and LiteLLM against the existing provider routing implementation with tests proving denied-provider rejection, quota exhaustion, resume, cost ceiling and no paid fallback. Do not install or deploy either based on README alone.
5. Run identical sanitized trace/evaluation fixtures through Langfuse, Phoenix and Opik; select at most one observability platform after residency/redaction review.
6. Add Promptfoo and/or equivalent open tests to the qualification pipeline only after dependency and workflow-permission review.
7. Choose components independently by layer. Replacing the entire orchestration runtime is an allowed option if the same immutable workload passes the acceptance suite and the migration preserves historical IDs, Baseline 2.0 semantics, authority boundaries and rollback.

## 6. Current MediaHub state and blockers discovered during this pass

- Repository main target observed through GitHub commit search: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Issue #301 remains open. It explicitly states that the schema queue is documentary, JSON Schema Draft 2020-12 meta-validation/negative fixtures remain open, and issuer/ingress/lease/cancel/recovery plus audit/privacy authority gates precede agent admission.
- Canonical map file path and blob SHA were found on `docs/mediahub-chat-tree-map-20261012`, but the GitHub file connector returned empty content for the 1.17 MB / 7,900-line map. A blob read using the returned SHA unexpectedly returned checkpoint-wave text rather than a readable map. Treat the map body as **NOT VERIFIED in this pass**; do not write a guessed map update. The canonical map URL remains the source link, not proof of successful read-back.
- PR #583 is still open, draft and unmerged. Observed head SHA: `9de1526e6daa121c62aa85fc707d9a8c6f9e0d4d`; formal reviews: none recorded; combined status endpoint returned no statuses. The workflow query returned six runs, four successful and two failed:
  - Astra Verify run [39973058604](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058604), job `120480482676`: **FAILED** at “Cloud admission unit tests”.
  - Workflow contract validation run [39973058901](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058901), job `120480483315`: **FAILED** at “Run controller transport contracts”.
  - The other observed runs [39973058613](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058613), [39973058680](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058680), [39973058385](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058385), [39973058548](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058548) completed successfully.
- Therefore PR #583 exact-head CI is **FAILED / NOT ACCEPTABLE** until the two failing steps are investigated and rerun on a new exact head. This is a separate active blocker; do not launch the Gemini batch while the required governance gates remain unverified.
- No Gemini dispatch, provider inference, local installation, deployment, merge, qualification or Contour A acceptance was performed in this landscape pass.

## 7. Next bounded package

**Target:** next immutable MediaHub SHA after the research PR is created, then pin immutable upstream SHAs for the first 8 candidates.

**Work:**
1. Diagnose the two PR #583 failed steps from exact logs and source; repair only proven causes.
2. Pin source commit SHA, release, license file SHA, dependency manifest/lockfile SHA, CI test evidence and security advisory status for LangGraph, Microsoft Agent Framework, Ruflo, Temporal, Restate, Bifrost, LiteLLM and Promptfoo.
3. Build a side-by-side matrix using one synthetic GitHub task envelope with success, timeout, duplicate dispatch, cancellation, quota exhaustion, invalid artifact, failed PR creation and recovery cases.
4. Do not run real provider inference or dispatch agents until Issue #301's gates pass.
5. Re-read report and PR file, record blob SHA, exact-head CI and independent review; update canonical checkpoint/map only after their true source content is readable and verified.

**Disposition:** landscape initialized; candidate-level source read-back partially verified; full candidate qualification NOT RUN; no component adopted; Contour A NOT ACCEPTED.
