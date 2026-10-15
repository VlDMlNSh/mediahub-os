# MediaHub OS — Agent / Task / Provider Schema Inventory and Draft Corporation Contracts, Wave 01

- Date: 2026-10-15
- Status: **SOURCE-BOUND INVENTORY + NON-NORMATIVE DESIGN DRAFT / NOT ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED**
- Repository: `VlDMlNSh/mediahub-os`
- Target documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Purpose: record the current source-backed coverage of agent, provider, mission/task, executor, result and evidence fields; identify genuine gaps; provide a bounded versioned-contract outline without promoting a proposal to a normative contract.
- Safety boundary: documentation-only. No tests, installation, model/provider calls, credential access, host/runtime inspection, qualification, infrastructure change, deployment, migration or branch integration.

## 1. Ref and source integrity

Live comparison at the start of this pass:
- `main` HEAD: `608d7463011798ca75e36bfce4b749a9caf4f9a0`
- `docs/mediahub-chat-tree-map-20261012` HEAD: `76439fec9f35df9c8d1834aecc67af908b398575`
- compare status: `DIVERGED`; docs branch 1191 ahead / 3 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No merge/rebase/cherry-pick or ref synchronization was attempted.

Source files reviewed (blob SHA at time of review):

| Source | Ref | Blob SHA | Confirmed scope |
|---|---|---|---|
| `profiles/agent-registry.json` | `main` | `993cbbe1b2b2a88da7d8884a897b404f055981a8` | Existing agent registry, schema ID `mediahub.ai.agent-registry`, version `1.2.0`, agent entries and declared capabilities |
| `profiles/providers/astra-gold-hybrid-agent-fabric.yaml` | `main` | `acf3ad43e68bf49ffa5a1d2c89f64bd363c0e181` | Provider/agent-fabric declaration with qualification-gated status and provider entries; declaration is not runtime proof |
| `schemas/ai/ai-inference-request.schema.json` | `main` | `e59c72b4a2a62b2372da57c6699ab12ebe25122f` | Versioned single inference request |
| `schemas/mediahub-component-evidence-record.schema.json` | docs ref | `2e62a9d0174e2c72e23ac88edc3094d13b4e336a` | Draft v0.1 revision-bound component/gate/deployment evidence; not qualification by itself |
| `control/qualification/g4-115.json` | `main` | `d4ae8e7cc341706c2a1dd5265726ef1e045f93d1` | ASTRA GOLD qualification contract, including a result-schema reference and verification status; not a corporation-wide task-result envelope |
| `evidence/provider-model.json` | `main` | `3112dc235c5f2e8aefcc2d9ee68ae331a6079944` | Historical provider/model evidence schema `mediahub.provider-model.v1`; point-in-time evidence, not current qualification |
| `oss/manifests/components.yaml` | `main` | `7141dd16e9ce9dba3440b1799a56e2ac4da4106d` | Qualification-gated component manifest, schema version 1; not an agent/task protocol |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | `main` | `da26185254d9954fcee204f81ecca129bf052e7c` | ASTRA-internal executor lifecycle/readiness/claim/lease/recovery and verifier policy |
| `docs/architecture/MH-12-security-architecture.md` | `main` | `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Identity, trust, capability, authorization, policy and boundary invariants |
| `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md` | docs ref | `e112cc73178eef5f71b8a814296e4902c2e80390` | Proposed mission and adapter fields; explicitly draft and does not establish an accepted A0 endpoint |
| `docs/checkpoints/MEDIAHUB-CORPORATION-TASK-RESULT-TECHNICAL-BASELINE-WAVE-09-2026-10-15.md` | docs ref | `6ab5f244cb0d4e74ac2b26013c02502832170365` | Technical recommendation for mission/task/result semantics; not normative |
| `docs/checkpoints/MEDIAHUB-DISTRIBUTED-TASK-DAG-AND-RESULT-CONTRACT-CROSSWALK-WAVE-01-2026-10-15.md` | docs ref | `9cf876b094278b4b2de9851cc488a5b3dabc147b` | Previous source-bound crosswalk and gaps |
| `docs/checkpoints/MEDIAHUB-JARVIS-CORPORATION-RESPONSIBILITY-INTERFACE-MATRIX-WAVE-01-2026-10-15.md` | docs ref | `d5934af98552ddee99ac5658dfffc8a3049f5cad` | Corporation role boundaries and interface gaps |
| `docs/checkpoints/MEDIAHUB-CHAT-TO-GITHUB-OWNER-DECISIONS-AND-CORPORATION-DIRECTION-WAVE-01-2026-10-15.md` | docs ref | `70376a2709e055972ceddc4a280d26992977213c` | Owner-approved responsibility split and direction; not proof of implementation |

**Search limitation:** this is a source-grounded inventory of the identified registry/schema/contract paths, not a claim that every repository path, branch, runtime or offline node was exhaustively scanned. Candidate conventional paths `schemas/engineering/task.schema.json`, `schemas/mission.schema.json` and `schemas/task-result.schema.json` were not found at the tested `main` paths (404). No accepted corporation-wide mission/DAG/executor-profile/task-result schema was identified in the checked sources.

## 2. Existing schema and contract coverage

| Entity / concern | Existing source coverage | Reusable fields/semantics | Missing or unsafe inference | Disposition |
|---|---|---|---|---|
| Agent registry entry | `profiles/agent-registry.json` v1.2.0 | Stable declared agent identity, role/capabilities and registry metadata where present | Registry declaration does not establish live availability, executor identity, trust, authorization or qualification | Reuse registry; do not create a duplicate agent catalogue |
| Provider / gateway / model | Provider fabric v1 plus `evidence/provider-model.json` | Declared provider IDs, capability/status declarations and historical provider/model evidence | Agent, client, executor, gateway, upstream provider and model are different identities; registry status is not live route proof | Reuse identity references; add per-task immutable route provenance only in a proposed task/result contract |
| Single AI inference request | `mediahub.ai.ai-inference-request` v1.0.0 | `request_id`, provider/model fields, operation, input, parameters, metadata, schema ID/version/owner | No mission ID, DAG, task dependency, worker lease, cancellation, artifact acceptance or corporation result lifecycle | Keep strictly as one inference operation |
| Component/gate evidence | Component evidence record v0.1 draft | `record_id`, `component_id`, `source_sha`, authority scope, forbidden operations, classification, egress, provider/model identity, evidence references, qualification/gate references | Does not define a per-task result envelope and does not itself qualify a component | Reference evidence records by URI/digest/revision; do not overload this schema |
| ASTRA engineering task lifecycle | ASTRA executor capability matrix | Dependency readiness, executor binding, claim conflicts, capacity gate, leases/heartbeats/recovery, target-SHA isolation, independent A3 verification | Not a corporation-wide wire format; exact Jarvis-facing A0 ingress and issuer lifecycle are not established by this matrix | Reuse within ASTRA only |
| G4 qualification | `control/qualification/g4-115.json` | ASTRA GOLD qualification/result-schema and verification contract | Not a generic result schema for arbitrary corporate tasks | Preserve as a separate ASTRA qualification domain |
| Component inventory/admission | `oss/manifests/components.yaml` v1 and admission crosswalk | Component IDs and target/current-foundation/qualification-gated statuses | Not proof of deployment, availability or permission to use a component | Preserve status and admission gates |
| Corporation mission | Adapter draft + owner direction | Proposed mission ID, idempotency, target SHA, data class/egress, budget/deadline, acceptance criteria, evidence revision | No accepted corporation-wide wire schema or authoritative admission API identified | Draft only |
| Corporation task DAG | Technical baseline + crosswalk | Proposed stable task IDs, immutable DAG revision, explicit dependency edges, bounded attempts, declared outputs | No accepted corporation-wide DAG schema identified | Draft only |
| Executor profile | Agent registry + ASTRA capability matrix + MH-12 | Declared role/capability, scoped authority, locality/egress and verification constraints across sources | No single accepted profile schema joining identity, admission, trust, resource and provenance | Draft only |
| Task result envelope | Technical baseline + component evidence substrate | Proposed task/attempt IDs, target/input digest, status, artifact digests, route provenance, checks, limitations, cancellation/partial status and verifier disposition | No accepted corporation-wide result envelope identified | Draft only; results remain untrusted until independently validated |

## 3. Authority split — invariant for every proposed schema

- **Jarvis:** corporation-level mission coordinator; decomposes work, chooses permitted routes/executors, tracks progress and collects results through accepted interfaces. It does not write ASTRA queue/lease/gate internals and does not mutate canonical product state.
- **ASTRA A0:** sole writer for ASTRA-internal engineering queue, claim, lease, heartbeat, retry/cancellation and ASTRA-specific evidence/gate transitions under its accepted contract. Its “state” is not canonical MediaHub product state.
- **Product State Authority:** sole authority for canonical product-state mutation. No agent, model, provider, gateway, GitHub adapter or worker receives this authority by implication.
- **Security/capability issuer:** must be an explicitly sourced and governed authority. Jarvis and workers cannot self-issue authority. Missing issuer/delegation/revocation semantics fail closed.
- **Executor / external agent controller:** executes bounded work and returns untrusted results; it does not certify its own output or gain control over MediaHub/A0 state.

## 4. Proposed versioned contract family (NON-NORMATIVE)

Use separate schema IDs and semantic versions; these are **suggested identifiers, not registered or accepted identifiers**:
- `mediahub.corporation.mission-envelope` — proposed major version 1
- `mediahub.corporation.task-dag` — proposed major version 1
- `mediahub.corporation.executor-profile` — proposed major version 1
- `mediahub.corporation.task-result-envelope` — proposed major version 1
- `mediahub.corporation.evidence-reference` — consider a shared definition only if it does not conflict with the existing component-evidence `evidenceReference` definition

### 4.1 Mission Envelope — proposed field groups

Required candidate groups:
- schema identity: `schema_id`, `schema_version`, `mission_id`;
- request provenance: `request_id`, authenticated principal reference, correlation ID;
- objective: bounded goal, in-scope resources, explicit exclusions and expected artifacts;
- revision binding: target repository/ref/SHA, contract revision and policy revision;
- admission: idempotency key plus canonical payload digest (never claim exactly-once side effects);
- constraints: data classification, allowed egress, eligible executor classes, resource/cost budget, deadline;
- lifecycle request: cancellation request reference and retry/attempt policy reference;
- acceptance: criteria revision, required verifier class, evidence schema revision;
- result: accepted/rejected/pending disposition and evidence reference, as supplied by the authoritative ingress.

**Not defined here:** concrete A0 endpoint, token/signature format, issuer identity, persistence guarantees, exact state enum or endpoint authentication. These must come from accepted primary contracts.

### 4.2 Task DAG — proposed field groups

- schema identity and immutable `dag_id` / `dag_revision`;
- parent `mission_id` and target/input revision;
- task nodes with stable `task_id`, bounded objective, task class, declared inputs/outputs and acceptance-criteria reference;
- explicit dependency edges and dependency revisions;
- eligibility constraints: capability profile reference, data class/egress, resource budget, deadline and verifier requirement;
- bounded attempt/retry policy reference, cancellation propagation policy and side-effect/idempotency declaration;
- integration outputs and conflict-resolution/verification gates.

Validation recommendations: reject duplicate task IDs, missing edge endpoints, cycles, ambiguous target revisions and undeclared outputs before dispatch. These are recommendations pending contract approval, not implemented guarantees.

### 4.3 Executor Profile — proposed field groups

- stable profile ID/revision and owner;
- separate identities for agent role, executor service, client, gateway, upstream provider and model;
- declared capabilities and supported task classes, with source/provenance and freshness;
- trust/admission status, authorization/capability reference, allowed operations and forbidden operations;
- workspace/isolation class, filesystem/network/tool scope, secret-access prohibition or explicit bounded reference;
- locality/egress/data-class constraints and fallback policy;
- platform/runtime/model version and immutable digest where available;
- resource envelope, concurrency limit, timeout and output limits;
- health/availability evidence timestamp, qualification reference and independent-verifier requirement.

A profile declaration is not proof of runtime presence, permission, connectivity or qualification.

### 4.4 Task Result Envelope — proposed field groups

- schema identity, mission/task/attempt IDs, idempotency/admission reference and correlation ID;
- target SHA, input digest, DAG/task-contract revision and policy revision;
- executor/client/gateway/upstream-provider/model identities and route-decision evidence;
- outcome enum that preserves at least success, partial, blocked, failed, cancelled, timed-out and unverified as distinct meanings;
- output artifact references with immutable digests, declared output names and media types;
- checks performed, check evidence, limitations, warnings and unresolved dependencies;
- timestamps, duration/resource usage, retryable classification and cancellation/late-result context;
- independent verifier identity/disposition and revision-bound evidence references;
- explicit separation of result verification, qualification, release, deployment and product acceptance.

Executors cannot set authoritative A0 terminal state or canonical product state by publishing this envelope. The receiving authority validates it and determines its own lifecycle transition.

### 4.5 Evidence Reference — proposed reuse boundary

Prefer referencing the existing component evidence record by stable record ID, URI and digest rather than copying its full schema. A task-level evidence reference may need `kind`, `uri`, `digest`, `captured_at`, source revision and redaction metadata, but this must be reconciled with existing evidence definitions before creating a new shared schema.

## 5. Field disposition matrix

| Field | Existing coverage | Proposed destination | Status |
|---|---|---|---|
| `schema_id` / `schema_version` | Present in agent registry, inference schema, provider fabric and component manifest with differing naming conventions | Every new contract, with a registered ID/version convention | Existing pattern; cross-contract convention unresolved |
| Stable agent identity / capabilities | Agent registry | Executor profile references registry identity | Existing partial coverage |
| Provider/gateway/model identity | Provider fabric and provider-model evidence | Per-task route provenance in mission/result | Partial; runtime route proof unresolved |
| `request_id` | Inference request | Mission links original request without redefining inference request | Existing for inference; mission linkage proposed |
| `mission_id` / idempotency key | Adapter draft / technical baseline | Mission envelope and admission record | Proposal only |
| `dag_id`, DAG revision, task IDs, dependency edges | ASTRA matrix has dependency semantics; not a corporation wire schema | Task DAG | Proposal only |
| Executor identity and permission scope | Partial across registry, ASTRA matrix and MH-12 | Executor profile + per-task result provenance | Cross-contract gap |
| Lease/claim/fencing generation | ASTRA lifecycle semantics; exact storage-enforced corporation-wide contract not found | ASTRA-owned lifecycle reference, not Jarvis-owned queue fields | Requires accepted A0 contract |
| Target SHA / input digest | ASTRA target-SHA isolation and evidence schema | Mission, task and result | Existing fragments; end-to-end binding proposed |
| Data classification / egress | Evidence schema, adapter draft, MH-12 | Mission and executor admission/result route record | Partial; runtime enforcement unverified |
| Budget / deadline / timeout | Technical baseline and adapter draft recommendations | Mission/task/profile | Proposal; shared policy source unresolved |
| Artifact URI/digest | Component evidence schema and technical baseline | Result envelope | Partial; task output envelope not accepted |
| Cancellation / retry / late completion | ASTRA lifecycle policy; technical baseline recommendations | Task DAG references policy; result records attempt/cancellation context | Corporation-wide semantics unresolved |
| Verification disposition | ASTRA A3 and G4 contracts; evidence schema qualification fields | Result envelope references verifier evidence; independent gate owns final disposition | Separate domains; no self-approval |
| Product state mutation | MH-12 and owner decision record | Not an executor/result field; separate Product State Authority operation | Invariant, never delegated by implication |

## 6. Blockers and fail-closed technical defaults

1. **A0 ingress:** no accepted Jarvis-facing submission/status API was identified in the reviewed sources. Do not invent endpoint, method, payload acceptance or response semantics.
2. **Capability issuer:** issuer identity, delegation, attenuation, expiry and revocation lifecycle are not fully sourced as an accepted operational contract. Deny A0-managed ingress until sourced.
3. **Fencing:** lease timeout alone is not proof that stale workers cannot publish. Require the accepted A0 storage contract to specify fencing/generation checks before claiming the race is closed.
4. **Provider topology:** gateway labels do not prove upstream provider or locality. Unknown identity remains UNKNOWN; local-only must not silently fall back to cloud.
5. **Schema registration:** suggested schema IDs are not registered. Check repository-wide ID collisions and owner/governance gates before creating JSON Schema files.
6. **Normative conflicts:** the ASTRA capability matrix on `main` has broader A0 “Global coordination/state” wording than the documentation-branch scope clarification. Branches remain diverged; no silent integration or normative overwrite.
7. **Evidence and status:** inventory/schema declarations do not prove runtime, testing, qualification, release, deployment or acceptance.

## 7. Next step

Read the live schema and ID conventions across all relevant refs, including the existing registry and G4 result references; trace producers/consumers; search for any less-obvious task/agent/provider-fabric/result schema and historical ID collisions. Then, if no existing contract covers the gap, create JSON Schema drafts in a dedicated proposal-only namespace and add a field-to-source traceability table. Do not promote them to normative, change runtime code, install components, call providers, or integrate diverged branches in this pass.


## 8. Follow-up source clarification — ASTRA result-schema field and authority wording

A follow-up inspection of exact source contents narrows two points:

1. `control/qualification/g4-115.json@main` (blob SHA `d4ae8e7cc341706c2a1dd5265726ef1e045f93d1`) declares schema identifier `mediahub.astra-gold.g4-115-contract.v1` and lists the string `result_schema` in `required_round_fields`. It does **not** name a JSON Schema URI, define the corporation-wide result-envelope structure, or establish a shared task-result contract. Therefore G4 coverage is only a required qualification-evidence field, not an existing reusable task-result schema. This supersedes any broader interpretation of “G4 result-schema reference” in earlier notes.
2. `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md@main` (SHA `7be5fadd3055642e7823c7233f90e978a87e5366`, §1) says “A0-ASTRA is the single MediaHub coordination and state authority”; `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md@main` (SHA `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1`, §1) says “A0-ASTRA = single coordination and MediaHub State Authority”; and `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml@main` (SHA `adc852009c3a79d0e64265a3af8a4910a1388057`, lines 11–14) assigns separate final architecture/security and single coordination authority roles. These statements remain in conflict with owner-approved DEC-DEV-02 Option C and the documented Product State Authority invariant. No normative source was changed. Treat as an open controlled-reconciliation blocker.
3. `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml@main` (SHA `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`) defines numeric lifecycle bounds (heartbeat 120s, lease 600s, retry backoff 30s, max three concurrent autonomous claims) and lists revocation support in the qualification/governance model. Those declarations do not identify the concrete Jarvis-facing A0 ingress, issuer service, credential/capability representation, revocation propagation procedure or storage-enforced fencing semantics.
4. The GitHub file-search connector returned zero matches for multiple ordinary terms (`agent-registry`, `result_schema`, `task_id`, `mediahub-component-evidence-record`, `provider-model`) despite known existing files. This search result is non-diagnostic and **cannot** be used as evidence that no additional schemas or ID collisions exist. The repository-wide collision scan remains open; this pass only records direct reads of the listed files and known-path probes.

### Corrected disposition

- G4 is not a corporation-wide task-result schema.
- No accepted Jarvis→A0 ingress/issuer/fencing/cancellation/replay wire contract was found in the reviewed primary sources.
- The A0/product-state authority contradiction remains unresolved and must be handled by controlled source reconciliation; no merge or normative edit is authorized.
- Next independent step: trace the P0-07 → P0-05 identity/context/authorization bridge using its canonical-read trace and source clauses, then record exact producer/consumer edges where discoverable. Continue schema-ID inventory only through verifiable repository-tree/source evidence; do not represent the failed search connector as an exhaustive scan.
## 9. Bounded schema-ID census and cross-ref comparison (2026-10-15)

**Scope and method:** read-only GitHub tree census for main and docs/mediahub-chat-tree-map-20261012; fetched and inspected the 26 JSON Schema files present under schemas/ on the documentation ref and the related registry/provider/G4 artifacts already indexed above. The recursive tree response for the documentation ref was complete (truncated=false, tree SHA e1c9d45d941072641cd61ef3e8fcb13e474896fc, 930 tracked tree entries). No runtime scan, test, schema validator, or provider was run.

### Confirmed results

- main contains 25 files under schemas/**/*.json; the documentation ref contains those same 25 paths with identical blob SHAs plus the documentation-ref-only schemas/mediahub-component-evidence-record.schema.json (blob 2e62a9d0174e2c72e23ac88edc3094d13b4e336a). This is a real cross-ref artifact difference, not an ID collision.
- The 26 inspected schema files have 26 distinct literal top-level $id values; no duplicate exact $id was found within this bounded schema-directory census.
- ID namespace conventions are not uniform: observed forms include mediahub://contracts/ai/..., mediahub.ai...., mediahub://schemas/..., https://mediahub.local/..., and https://mediahub-os.invalid/.... Domain IDs are also not always a literal path mirror (for example, the desired_state filename uses a hyphenated ID segment). This is a consistency/registration risk, not proof that any one identifier is invalid.
- Version metadata is likewise not represented by one proven repository-wide convention: the agent registry declares schema_id=mediahub.ai.agent-registry and schema_version=1.2.0; inference/provider schemas carry their own schema metadata; G4 lists the field name result_schema in required_round_fields but does not thereby define a reusable corporation-wide result schema.
- The docs-only component-evidence schema remains a draft substrate for component/gate evidence. It is not a corporation-wide task-result envelope and must not be treated as accepted on main.

### Limits and disposition

- This is not a complete repository-wide collision proof for every schema-like identifier embedded in code, YAML, Markdown, generated artifacts, historical refs, or external systems. GitHub code-search results previously returned zero matches despite known files, so those negative results are non-diagnostic. Producer/consumer edges and historical ID reuse remain open outside the inspected files.
- Do not register proposed mission/DAG/executor/result/evidence IDs or create production JSON Schemas until the naming/version convention, complete producer/consumer census, accepted Jarvis→A0 ingress, capability issuer lifecycle, and governance gates are resolved.
- No normative schema, registry, runtime code, configuration, or contract was changed. No tests, installation, provider/model calls, credentials, host/runtime inspection, qualification, deployment, or branch integration occurred.

**Next bounded step:** trace non-secret producer/consumer references for the existing agent registry, provider fabric and inference request/response contracts across the relevant source files; record only source-backed edges and leave a complete repository-wide collision claim open until the search coverage is demonstrably complete.


## 10. Source-backed producer/consumer crosswalk — agent registry, provider fabric and inference (2026-10-15)

**Scope:** read-only source inspection of the exact documentation-ref files listed below. This is a bounded producer/consumer trace, not an exhaustive repository-wide call-graph or runtime validation. No tests were run.

| Artifact / source | Confirmed producer/consumer evidence | Contract boundary and unresolved edge |
|---|---|---|
| profiles/agent-registry.json, blob 993cbbe1b2b2a88da7d8884a897b404f055981a8 | Registry declares schema_id=mediahub.ai.agent-registry, schema_version=1.2.0, agent IDs/capabilities/tier/activation, and a separate hybrid_fabric section with duplicated lists and qualification-state entries. | No explicit $schema reference or validated consumer was established in this pass. The top-level agents list and hybrid_fabric lists contain overlapping identity data; consistency is a risk, not a proven runtime defect. Several entries declare enabled=true while qualification remains pending/not proven; the registry itself also states registration does not imply authorization/success. |
| schemas/ai/ai-inference-request.schema.json, blob e59c72b4a2a62b2372da57c6699ab12ebe25122f; ai-inference-response.schema.json, blob cbd7774600aa6380d40c9a676e54583a01dfcdca | tests/ai/test_ai_inference.py, blob e54eec7fed2a14a714bd0f39c49b1ce495f7c999, reads these exact files and asserts schema IDs, version, owner, request/response fields and status/operation enums. | This establishes a source-level test consumer, not that tests passed or that production runtime validates messages. Request ID is the correlation field; provider/model are optional. The contract covers a single inference operation, not a mission, DAG, worker lease, cancellation race or corporation task-result envelope. |
| schemas/ai/ai-provider-registry.schema.json, blob 9537a64bc948b1bea3e2a640670f48e107760a50 | tests/ai/test_ai_provider_registry.py, blob 5b064c47e54c541f70cc9c314cbec14f64141015, reads the schema and asserts metadata, provider-reference shape, selection-policy values and required fields. | Evidence establishes a test consumer only. No checked production source binds the runtime provider catalog to this schema in the bounded pass. The registry schema's provider entries are IDs/enabled/priority, not full provider/adapter definitions. |
| schemas/ai/ai-provider.schema.json, blob 364a1aed7a8ff14b382aad0eab4ec0b5d5a55347; ai-provider-adapter.schema.json, blob e0dab7002222451579e649a7d1d29985393d9a42 | These define provider identity/model/capabilities/authentication/availability and adapter transport/operations/state/capabilities/endpoints. | No producer/consumer validation edge for either schema was established from the inspected runtime files. Keep provider definition, adapter instance, provider registry and inference request/response as distinct concepts. |
| runtime/mediahub_runtime/local_providers.py, blob 8361b7d6782adaa9dcd4e47b5d9e9940d41bb1a3 | Direct source shows FreeLLMAPIExecutor uses provider_id=freellmapi, local gateway URL/config, a key-file reference and OpenAI-compatible /models and /chat/completions paths. It parses choices[0].message.content. | This is a concrete provider adapter path, but the inspected code does not import/validate the canonical inference request/response or provider/adapter schemas. Source code alone does not establish the configured upstream provider or prove local-only/egress behavior. Do not infer deployment state or call the endpoint. |
| runtime/mediahub_runtime/worker_router.py, blob 00ce4d3e96d327baa38de9644e7bff20a79040ed | Implements a separate opt-in claude-code worker decision and labels ollama as fallback; failure currently raises worker_fallback_requires_model_adapter rather than executing a model adapter. | This is an agent-worker path, not a provider schema consumer. It must not be conflated with the inference provider fabric; fallback is not demonstrated as a completed route. |
| profiles/providers/astra-gold-hybrid-agent-fabric.yaml, blob acf3ad43e68bf49ffa5a1d2c89f64bd363c0e181 | Declares a separate mediahub.astra-gold.hybrid-agent-fabric.v1 catalog, admission gates, agent/gateway IDs and qualification states. | This is qualification-gated profile data, not evidence that those agents are available or authorized. Its IDs/statuses overlap with the agent registry and provider-model registry but have different shapes/purposes; no canonical synchronization/validation edge was proven. |
| ops/qualification/provider_model_registry.json, blob 62328126fd2cd8879a73bb6812adcacd3e2abe84 | Defines a separate provider/model qualification catalog with its own schema, selection order, provider IDs, model lists, endpoint, credential-environment names and classification fields. | This is not the same identifier space as agent IDs, provider IDs, adapter IDs or the canonical provider-registry schema. The file contains credential references/names, not secret values; no credential was read. Exact consumer linkage to runtime routing was not established here. |
| architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md, blob e549692f207fbc91d9b9b9b92b8e665404f07290; docs/architecture/MH-21-provider-contract.md, blob d2bf7e29eee9ff2e07f4e25bf58229df11ff3cda; MH-21-ai-routing.md, blob 2c1eef7c06d3f24965c4e9e5479ac2c52e161da5 | Architecture says the target is not yet runtime-qualified; provider-neutral operations and routing are explicitly PROPOSED in MH-21. | These are design sources, not evidence of implementation. Architecture-level FreeLLMAPI cloud-path wording remains in tension with the runtime class local_gateway and local loopback default; this is a source/config identity question, not resolved by this crosswalk. |

### Findings and disposition

1. **Confirmed separation:** inference request/response, provider definition, adapter definition, provider registry, agent registry, ASTRA-GOLD qualification fabric and provider/model qualification catalog have different purposes. None should be overloaded into a corporation-wide mission/DAG/result schema.
2. **Confirmed source consumers:** current checked tests read the inference and provider-registry schema files. This is not evidence that tests ran or that runtime requests are validated.
3. **Validation gap in inspected source:** no production consumer was established that validates the agent registry, provider registry, provider or adapter data against their corresponding JSON Schemas. This is limited to the inspected paths and is not a repository-wide absence claim.
4. **Identity drift risk:** agent IDs, gateway IDs, provider/model registry IDs, adapter IDs and qualification IDs are distinct namespaces; overlapping names must not be treated as interchangeable identities. Registry duplicates/qualification states need a future source-backed reconciliation, not a speculative bulk rewrite.
5. **Route identity remains unresolved:** the architecture describes FreeLLMAPI as a cloud-model path while the runtime adapter labels it local_gateway and defaults to loopback. A local gateway may proxy upstream, but that is only a hypothesis until source/config evidence establishes the actual upstream and egress semantics.
6. **No new normative schema or IDs proposed/registered.** The Jarvis→A0 ingress, capability issuer lifecycle, fencing, cancellation/replay semantics and D6 governance status remain blockers. Do not infer runtime enforcement, test results or provider availability.

**Next bounded step:** continue read-only source tracing of where profiles/agent-registry.json, profiles/providers/astra-gold-hybrid-agent-fabric.yaml and ops/qualification/provider_model_registry.json are loaded and reconciled, using exact repository paths/source evidence. In parallel, trace FreeLLMAPI/FCC/OmniRoute/UnoRouter/Alamo identity from non-secret source/config references. Do not call providers, inspect hosts, run tests or change routing/configuration.


## 11. Registry loader/consumer and route-identity trace — bounded source pass (2026-10-15)

**Scope:** source read only on the documentation ref. No code executed, no tests/qualification launched, no provider endpoints called, no credential values read.

| Data/source | Exact evidenced load/use path | What remains unproven |
|---|---|---|
| `ops/qualification/provider_model_registry.json` blob `62328126fd2cd8879a73bb6812adcacd3e2abe84` | `ops/qualification/qualify_execution_backends.py` blob `acf092d5dd9d67ab187f1b67ab691ca730028306` sets `REGISTRY = ROOT / "ops" / "qualification" / "provider_model_registry.json"`, reads JSON in `main()`, and maps `qualify` over `registry["providers"]`. The script includes outbound catalog/model request code and reads credential *environment variable names* from registry entries. | This is an actual source-level loader and potential live-provider call path, not evidence it was executed. No current run/evidence was requested or inspected. Runtime validation against a JSON Schema is not shown; the file's own `schema` label is not by itself validation. |
| `.github/workflows/astra-provider-qualification.yml` blob `d3160088fbef4fce152ed7335f0acaa3bb440378` | Declares a `workflow_call` with command ID/target SHA, a self-hosted `mediahub-provider` runner, maps many repository secrets to environment variables, checks the exact node/user, calls `qualify_execution_backends.py --target-sha`, and uploads sanitized evidence. | Workflow configuration is not proof a workflow ran, credentials exist, the runner is online, or any provider qualified. It is an explicit gated path that can make external requests; do not invoke it without separate authorization. |
| `profiles/agent-registry.json` blob `993cbbe1b2b2a88da7d8884a897b404f055981a8` | `tests/test_astra_gold_registry.py` blob `9a6727c74b675412e60e8e944f4a9f777bfc4192` directly loads JSON and asserts non-authoritative ECC boundaries and the distinction between `claude-code` execution client and `claude` provider/gateway identity. | The inspected runtime modules do not establish this file as a runtime-loaded canonical registry. Test reads are not runtime consumers and tests were not run. |
| `profiles/providers/astra-gold-hybrid-agent-fabric.yaml` blob `acf3ad43e68bf49ffa5a1d2c89f64bd363c0e181` | Declares qualification gates and per-agent status; explicitly says registration/credential reference is not authorization and requires runtime auth, model discovery, non-mutating probe, fresh evidence and A3 verification. | No exact production loader for this YAML was established in the checked paths. Its entries remain declarative, not evidence of active/authorized routes. |
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml` blob `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` and `ops/agent-fabric/providers/node-role-map.yaml` blob `6fab2a8513ad32ed5bb15be819ad74cc2365214b` | Routing data explicitly distinguishes FCC and OmniRoute as transports/gateways and gives them executor-only authority; node-role-map declares GitHub-transport command/result paths and required fencing fields. | These files are qualification-gated declarations. No runtime loader/consumer for these exact YAML files was established here; do not treat them as active routing. |
| `runtime/mediahub_runtime/local_providers.py` blob `8361b7d6782adaa9dcd4e47b5d9e9940d41bb1a3`; `profiles/agent-registry.json`; hybrid fabric YAML | Runtime adapter uses provider ID `freellmapi`, classifies itself `local_gateway`, defaults to `http://127.0.0.1:3001/v1`, and reads a key file only when adapter methods execute. The profile marks the fabric entry `PENDING`; agent registry lists `freellmapi` as `local_gateway` and separately records it as `NOT_PROVEN` in qualification states. | Local loopback establishes the configured first hop only. It does not identify the upstream behind the gateway or prove local-only egress. The different registration/qualification fields have distinct meanings; do not collapse them into one status. |
| `ops/qualification/hybrid_agent_auth_probe.py` blob `1fb0cb41d219eaf26dc830c8585a790c89a5cb50`; `tests/test_hybrid_agent_auth_probe.py` blob `238e2b9881bafb59e9bab63217e84d89b92e904c` | Probe code defines provider IDs/endpoints and would issue outbound requests when `probe()`/main are invoked; the test source asserts provider set and fail-closed behavior when credential variables are absent. | Neither probe nor tests were run. Their existence does not establish authentication, endpoint reachability, credential presence or qualification. |

### Reconciliation findings

1. **One concrete loader established:** the provider/model qualification script reads the qualification catalog and contains live HTTP request paths. This is separate from the canonical AI provider schemas and from the agent registry.
2. **Other registries remain unlinked at runtime in the inspected evidence:** agent registry has test readers; the hybrid fabric and executor/node YAMLs are declarative in the checked sources. This is a bounded finding, not a repository-wide proof of no other loader.
3. **Route identity has three layers:** (a) agent/provider identity (`freellmapi`), (b) local gateway first hop (`127.0.0.1:3001/v1`), and (c) unknown upstream/egress behind that gateway. Only the first two are source-declared; layer (c) remains UNKNOWN.
4. **FCC and OmniRoute are explicitly transports/gateways, not agents**, in the agent registry; executor-routing YAML assigns executor-only authority. No evidence here establishes their actual launchers, endpoint, credentials or active state.
5. **Qualification status is intentionally non-equivalent to registration/enabled:** registry entries can be enabled/registered while qualification is NOT_PROVEN/PENDING. No bulk status edits are justified.
6. No provider/model calls, credential reads, test runs, qualification, runtime/host inspection, config edits or schema changes were performed.

**Next bounded step:** reconcile identity fields across the three registries and the routing declarations into a source-anchored, non-mutating comparison table (agent ID, provider ID, transport/gateway ID, model ID, credential reference name, declared status, loader evidence, qualification evidence). Keep actual upstream/egress UNKNOWN until source evidence proves it. Do not launch the qualification workflow or probes.


## 12. Cross-registry identity/status reconciliation matrix (2026-10-15)

**Source scope:** documentation branch only. This table compares declarations; it does not claim runtime loading, credentials present, endpoint reachability, or qualification success. Credential names only are recorded, never values.

Source blobs: profiles/agent-registry.json 993cbbe1b2b2a88da7d8884a897b404f055981a8; profiles/providers/astra-gold-hybrid-agent-fabric.yaml acf3ad43e68bf49ffa5a1d2c89f64bd363c0e181; ops/qualification/provider_model_registry.json 62328126fd2cd8879a73bb6812adcacd3e2abe84; ops/agent-fabric/providers/local-executor-routing-v2.yaml af3d96fe91055af6ba79eded9c800d28d8c0c5c9; ops/agent-fabric/providers/node-role-map.yaml 6fab2a8513ad32ed5bb15be819ad74cc2365214b.

| Comparison key (not a canonical shared ID) | Agent registry declaration | Hybrid fabric declaration | Provider/model catalog declaration |
|---|---|---|---|
| ollama | local; enabled=true; activation=unspecified | local_fabric/ local_model; status=unspecified | — |
| freellmapi | local_gateway; enabled=true; activation=unspecified | gateways/ local_gateway; status= PENDING; ref= local_key_file | — |
| gemini | external; enabled=true; activation=credentialed_only | cloud_agents/ direct_cloud; status= NOT_PROVEN; ref= GEMINI_API_KEY | gemini-1: models=gemini-3.8-flash, gemini-3.5-flash-lite; credential_env=GEMINI_API_KEY; cost=free_tier; persistence=free_tier |
| perplexity | external; enabled=true; activation=credentialed_only | cloud_agents/ direct_cloud; status= NOT_PROVEN; ref= PERPLEXITY_API_KEY | — |
| kimi | external; enabled=true; activation=credentialed_only | cloud_agents/ direct_cloud; status= NOT_PROVEN; ref= KIMI_API_KEY | kimi-1: models=kimi-k2.5; credential_env=KIMI_API_KEY, MOONSHOT_API_KEY; cost=free; persistence=free_tier |
| deepseek | external; enabled=true; activation=credentialed_only | cloud_agents/ direct_cloud; status= NOT_PROVEN; ref= DEEPSEEK_API_KEY | deepseek-1: models=deepseek-chat, deepseek-reasoner; credential_env=DEEPSEEK_API_KEY; cost=trial; persistence=trial |
| chatgpt | external; enabled=true; activation=credentialed_only | cloud_agents/ direct_cloud; status= NOT_PROVEN; ref= OPENAI_API_KEY | — |
| openai | — | gateways/ direct_cloud; status= NOT_PROVEN; ref= OPENAI_API_KEY | — |
| openrouter | external; enabled=true; activation=credentialed_only | gateways/ cloud_gateway; status= NOT_PROVEN; ref= OPENROUTER_API_KEY | openrouter-1: models=openai/gpt-oss-120b:free, google/gemini-2.5-flash:free; credential_env=OPENROUTER_API_KEY; cost=router; persistence=router |
| unorouter | external_gateway; enabled=true; activation=credentialed_only; credential=UNOROUTER_API_KEY | gateways/ cloud_gateway; status= NOT_PROVEN; ref= UNOROUTER_API_KEY | unorouter-1: models=gpt-oss-120b:free; credential_env=UNOROUTER_API_KEY; cost=router; persistence=router |
| claude | external_gateway; enabled=true; activation=credentialed_only; credential=OMNIROUTE_API_KEY | gateways/ cloud_gateway; status= NOT_PROVEN; ref= OMNIROUTE_API_KEY | — |
| cloudflare | — | gateways/ direct_cloud; status= CANDIDATE; ref= CLOUDFLARE_API_TOKEN | cloudflare-1: models=@cf/meta/llama-3.1-8b-instruct; credential_env=CLOUDFLARE_API_TOKEN_1, CLOUDFLARE_API_TOKEN; cost=free; persistence=workers_ai<br>cloudflare-2: models=@cf/meta/llama-3.1-8b-instruct; credential_env=CLOUDFLARE_API_TOKEN_2; cost=free; persistence=workers_ai |
| siliconflow | — | gateways/ direct_cloud; status= CANDIDATE; ref= SILICONFLOW_API_KEY | siliconflow-1: models=THUDM/glm-4-9b-chat; credential_env=SILICONFLOW_API_KEY_1, SILICONFLOW_API_KEY; cost=free; persistence=permanent_free<br>siliconflow-2: models=deepseek-ai/DeepSeek-R1-Distill-Qwen-7B, Qwen/Qwen2.5-7B-Instruct, THUDM/glm-4-9b-chat; credential_env=SILICONFLOW_API_KEY_2; cost=free; persistence=permanent_free |
| novita | — | gateways/ direct_cloud; status= CANDIDATE; ref= NOVITA_API_KEY | novita-1: models=meta-llama/Llama-3.2-1B-Instruct, Qwen/Qwen2.5-7B-Instruct, THUDM/glm-4-9b-chat; credential_env=NOVITA_API_KEY_1, NOVITA_API_KEY; cost=free; persistence=permanent_free<br>novita-2: models=meta-llama/Llama-3.2-1B-Instruct, Qwen/Qwen2.5-7B-Instruct, THUDM/glm-4-9b-chat; credential_env=NOVITA_API_KEY_2; cost=free; persistence=permanent_free |
| zai | — | gateways/ direct_cloud; status= CANDIDATE; ref= ZAI_API_KEY | zai-1: models=glm-4.7-flash, glm-4.5-flash; credential_env=ZAI_API_KEY_1, ZAI_API_KEY; cost=free; persistence=permanent_free<br>zai-2: models=glm-4.7-flash, glm-4.5-flash; credential_env=ZAI_API_KEY_2; cost=free; persistence=permanent_free |
| llm7 | — | gateways/ direct_cloud; status= CANDIDATE; ref= LLM7_API_KEY | llm7-1: models=default; credential_env=LLM7_API_KEY; cost=free; persistence=free_tier |
| sambanova | — | gateways/ direct_cloud; status= CANDIDATE; ref= SAMBANOVA_API_KEY | sambanova-1: models=DeepSeek-V3.1, Meta-Llama-3.3-70B-Instruct; credential_env=SAMBANOVA_API_KEY; cost=free; persistence=free_tier |
| aionlabs | — | gateways/ direct_cloud; status= CANDIDATE; ref= AIONLABS_API_KEY | aionlabs-1: models=aion-labs/aion-3.5-mini, aion-labs/aion-3.5; credential_env=AIONLABS_API_KEY; cost=free; persistence=free_tier |
| groq | — | gateways/ direct_cloud; status= CANDIDATE; ref= GROQ_API_KEY | groq-1: models=openai/gpt-oss-20b, openai/gpt-oss-120b; credential_env=GROQ_API_KEY; cost=free_tier; persistence=free_tier |
| mistral | — | gateways/ direct_cloud; status= CANDIDATE; ref= MISTRAL_API_KEY | mistral-1: models=mistral-small-latest, mistral-large-latest; credential_env=MISTRAL_API_KEY_1; cost=free_tier; persistence=free_tier<br>mistral-2: models=mistral-small-latest, mistral-large-latest; credential_env=MISTRAL_API_KEY_2; cost=free_tier; persistence=free_tier |
| huggingface | — | gateways/ direct_cloud; status= CANDIDATE; ref= HF_TOKEN | huggingface-1: models=openai/gpt-oss-120b:fastest, Qwen/Qwen3-Coder-480B-A35B-Instruct:fastest; credential_env=HF_TOKEN; cost=free_tier; persistence=free_tier |
| nararouter | — | gateways/ cloud_gateway; status= CANDIDATE; ref= NARAROUTER_API_KEY | nararouter-1: models=default; credential_env=NARAROUTER_API_KEY_1, NARAROUTER_API_KEY; cost=router; persistence=router |
| orcarouter | — | gateways/ cloud_gateway; status= CANDIDATE; ref= ORCAROUTER_API_KEY | orcarouter-1: models=default; credential_env=ORCAROUTER_API_KEY; cost=router; persistence=router |
| zerouter | — | gateways/ cloud_gateway; status= NOT_PROVEN; ref= ZEROUTER_API_KEY | zerouter-1: models=gpt-5.4; credential_env=ZEROUTER_API_KEY; cost=router; persistence=router |
| gigachat | — | cloud_agents/ direct_cloud; status= REGISTERED_NOT_QUALIFIED; ref= GIGACHAT_API_PERS | — |
| kimi-k3-in-c | local; enabled=true; activation=checkpoint_required | local_fabric/ local_model; status=unspecified | — |
| claude-code | local_tooling; enabled=true; activation=local_install_required; qualification=pending | local_fabric/ local_executor; status= NOT_PROVEN | — |
| codex | local_tooling; enabled=true; activation=local_install_required; qualification=pending | local_fabric/ local_executor; status= NOT_PROVEN | — |
| cursor | local_tooling; enabled=true; activation=local_install_required; qualification=pending | local_fabric/ local_tooling; status=unspecified | — |

### Cross-registry discrepancies and safe interpretation

1. **Identifier domains are not normalized.** The agent registry uses agent/gateway IDs (for example ollama, freellmapi, claude); the qualification registry uses provider-instance IDs (for example ollama-local-1, gemini-1, siliconflow-1) plus separate provider/family and model fields. Matching names/families are evidence of a naming relationship only, not a foreign-key contract.
2. **Qualification status is not one field.** Agent-registry enabled/activation, hybrid-fabric status, and provider-catalog presence/selection order represent different lifecycle dimensions. Listing or enabling an entry does not establish credentials, successful authentication, model discovery, or A3 verification.
3. **Credential reference names differ across catalogs.** Hybrid fabric uses one credential reference per declared agent/gateway, while provider-model entries can list multiple environment-variable fallbacks. No secrets were read and no credential availability is claimed.
4. **Transport/executor IDs are a separate domain.** Routing uses CODEX_FCC, CLAUDE_FCC, CODEX_OMNIROUTE, CLAUDE_OMNIROUTE, and CLAUDE_CODE_DIRECT; node-role-map adds labels such as CLAUDE_LOCAL_FCC/CODEX_LOCAL_FCC, node IDs, executor and model fields. They are not provider-catalog IDs. Exact runtime loading and cross-file referential validation were not established.
5. **Model disagreements must not be auto-corrected.** Node-role-map declares qwen2.5-coder:1.5b for local Claude executor pools and qwen2.5-coder:3b for a Codex pool; provider-model registry declares qwen2.5-coder:3b under ollama-local-1. These are declarations in separate artifacts, not proof that routes are connected or a confirmed defect.
6. **FreeLLMAPI remains a three-layer unknown:** provider identity freellmapi; loopback first hop 127.0.0.1:3001/v1; upstream/egress UNKNOWN. Do not mark it local-only or cloud-backed without source/config evidence of the gateway upstream.
7. **No normalization or ID changes made.** A future canonical crosswalk requires owner-approved namespace/authority rules and loader evidence. No runtime/config/schema code changed in this pass.

**Next bounded step:** trace the declared executor IDs and provider/model IDs to exact launcher/loader call sites (source-only), prioritizing whether local-executor-routing-v2.yaml and node-role-map.yaml are read by any executable path. Do not invoke launchers, probes, providers or workflows.


## 13. Executable loader trace: executor routing and node-role declarations (2026-10-15)

### Evidence scope

Source-only inspection on the documentation branch. No workflow, launcher, probe, provider, test, qualification or host operation was invoked. The files below were fetched at the listed blob SHAs; no runtime/config code was changed.

| Artifact | Blob SHA | What the source establishes |
|---|---|---|
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml` | `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` | Declarative executor IDs include `CODEX_FCC`, `CLAUDE_FCC`, `CODEX_OMNIROUTE`, `CLAUDE_OMNIROUTE`, `CLAUDE_CODE_DIRECT`; all are executor-only. |
| `ops/agent-fabric/providers/node-role-map.yaml` | `6fab2a8513ad32ed5bb15be819ad74cc2365214b` | Declares `mh-dev-02` as a `primary-local-executor-pool` with `CODEX_LOCAL_FCC`, model `qwen2.5-coder:3b`, executor `codex`; declares `Voktors-Mac-mini.local` as a fast local pool. |
| `ops/qualification/run_distributed_local_worker.py` | `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | **Executable worker does not load either YAML.** It hardcodes a separate `NODE_CONFIG`: `mh-dev-02` has model `qwen2.5-coder:3b` and pool `primary_local`; it separately accepts `Voktors-Mini.Dlink` and `Voktors-Mac-mini.local`. Runtime executor input permits both `codex` and `claude`. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Workflow dispatch input restricts `executor` to `claude`; its `mh-dev-02` job sets `ASTRA_EXECUTOR=claude` and checks for the 3B model. This differs from node-role-map's Codex executor declaration for that pool. Workflow was not invoked. |
| `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml` | `0b86b07dfa916d4485ce1f8f54d19de136d98491` | Declarative qualification contract lists five mandatory paths including both FCC and OmniRoute Codex/Claude routes plus direct Claude Code; this is a gate declaration, not evidence that these paths are loaded from the executor-routing YAML. |
| `runtime/mediahub_runtime/agent_fabric.py` | `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` | Implements file-backed task claim/lease coordination; the inspected module does not reference either routing YAML. |
| `astra_github_agent.py` | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Qualification path constructs isolated Codex configuration and local OmniRoute base URL in code; no reference to either routing YAML was found in the inspected file. |

### Reconciliation findings

1. **Loader gap confirmed within inspected executable paths:** the worker uses hardcoded `NODE_CONFIG`; the executor-routing and node-role YAML are not read by that worker. The exact authoritative runtime source for the YAML declarations is therefore **NOT ESTABLISHED** by this trace.
2. **Executor declaration mismatch:** node-role-map assigns `mh-dev-02` to Codex (`CODEX_LOCAL_FCC`), while the distributed-local-worker workflow's `mh-dev-02` job is Claude-only. The worker code accepts either executor, so the workflow gate is the narrower policy. This is a source-level cross-artifact inconsistency; actual workflow execution/routing was not observed.
3. **Node identity alias risk:** node-role-map names `Voktors-Mac-mini.local`, while the worker supports both that ID and `Voktors-Mini.Dlink`. No canonical alias contract or identity-equivalence proof was found in these inspected files.
4. **Duplicated configuration drift risk:** node/model/pool values exist in both YAML and Python literals. Existing equality for the 3B model on `mh-dev-02` does not establish a shared source of truth. Do not patch one side by inference.
5. **No runtime loader should be claimed for provider/model registry based on this trace.** The qualification script separately reads `ops/qualification/provider_model_registry.json`, but that is a different catalog and a distinct execution path.

### Owner decision required before implementation

Choose one explicit authority model: (A) YAML becomes the normative source and executable code consumes validated YAML; (B) Python/runtime config is normative and YAML is generated/verified derivative; or (C) retain separate artifacts with an owner-approved cross-file conformance gate. Recommendation: **A or B with one canonical source and a fail-closed conformance check**; do not choose automatically. Decide also whether `mh-dev-02` is Codex or Claude for this workflow and whether the two Voktors node IDs are aliases or distinct nodes.

**Next bounded step:** inspect the source-only control plane and task/launcher contract for who selects `ASTRA_EXECUTOR` and supplies node IDs, then document the authority decision as OPEN unless an existing accepted contract resolves it. Do not invoke the workflow or worker.


## 14. Control-plane input versus worker-dispatch contract (2026-10-15)

### Source evidence

| Artifact | Blob SHA | Evidence |
|---|---|---|
| `.github/workflows/astra-chat-control.yml` | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | Parser accepts executor `codex|claude` and node `mh-dev-02|Voktors-Mac-mini.local`; task validation checks task executor/node against those selected inputs. The execution step then hardcodes `ASTRA_NODE_ID=mh-dev-02`, `ASTRA_EXECUTOR=codex`, and asserts parsed node/executor are exactly `mh-dev-02`/`codex`. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Separate workflow offers `claude` as its only executor option; its `mh-dev-02` job sets `ASTRA_EXECUTOR=claude`. |
| `control/qualification/distributed-runner-contract.json` | `993f51f07c7937165ffb3bfbe59cd0801ea71ec0` | Canonical node ID `Voktors-Mac-mini.local` explicitly allows hostnames `Voktors-Mac-mini.local` and `Voktors-Mini.Dlink`; this supports a hostname allowlist relationship but does not make these two strings interchangeable node IDs in every contract. |
| `ops/qualification/run_distributed_local_worker.py` | `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | Hardcoded `NODE_CONFIG` includes both Voktors strings and node `mh-dev-02`; it does not load either executor-routing YAML. |
| `ops/control/sign_command.py` | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Node-key name mapping supports `mh-dev-02` and `Voktors-Mac-mini.local`; signing requires credentials by environment-variable name when invoked. No key values were read and signer was not invoked. |

### Confirmed source-level inconsistencies

1. **Input/execution mismatch:** the chat-control workflow accepts a selected Claude or Voktors node at validation, but the worker step is pinned to Codex on `mh-dev-02`. A Voktors/Claude or `mh-dev-02`/Claude request is therefore inconsistent with the later hard-coded checks; source inspection predicts rejection at those checks, but no workflow was run.
2. **Two dispatch contracts disagree:** `astra-chat-control.yml` hardcodes Codex for `mh-dev-02`, while `astra-distributed-local-worker.yml` only exposes Claude for `mh-dev-02`. This is a real cross-workflow policy contradiction in source, not evidence of which route has been used operationally.
3. **Node ID versus hostname:** the distributed runner contract has one canonical Voktors node ID and a two-entry hostname allowlist. Worker `NODE_CONFIG` also contains both strings as keys. The hostname alias is documented, but the duplicate worker keys remain a drift surface.
4. **Task selection is not a single validated route object end-to-end:** input task/node/executor are checked, then execution values are hardcoded separately. The inspected path has no single normalized route object consumed through dispatch and worker.

### Required disposition

- Do not patch one workflow to guess the intended executor. Owner must select the supported executor policy for `mh-dev-02` and whether the chat-control route is intentionally Codex-only.
- Normalize the accepted request into one route tuple `(task_id, node_id, executor, target_sha)`; ensure the exact same validated tuple controls admission and execution, and ensure task contract and runner policy agree. This is a design recommendation, not an accepted implementation contract.
- Keep Voktors node ID canonical as `Voktors-Mac-mini.local` unless an owner-approved contract says otherwise; treat `Voktors-Mini.Dlink` as a hostname alias only where the runner contract explicitly allows it.
- No code, workflow, schema or runtime files changed. No workflow, tests, qualification, signer, provider, credentials or host/runtime was invoked/read.

### Planning estimate for reconciliation (non-binding)

Static source-backed map, component inventory, cross-file conflict ledger and contract draft: **10–20 focused working days** (roughly 2–4 weeks), assuming one bounded pass per issue cluster and no new large subsystem discovery. Implementation of approved fixes, test/qualification evidence and independent Contour A acceptance are separate, currently unestimated phases because owner decisions, branch integration and local runner availability are unresolved. Zero unknown defects cannot be guaranteed; the target should be zero *known untriaged* contradictions, each dispositioned as fixed, accepted exception, blocked or owner decision.


## 15. Owner direction — clean-slate target for new hardware (2026-10-15)

### Decision recorded

The owner has explicitly directed that the next target be a **new system for new hardware**. Previously attempted, unsuccessful installations on old servers are **not part of the target runtime, deployment plan, component allowlist, node inventory, or qualification baseline**. Do not spend further work making those old-server installation attempts operational or reconciling their runtime assumptions as if they were target requirements.

### Required handling of legacy material

1. Classify every old-server-specific reference as one of: (a) active runtime/config/deployment artifact; (b) historical evidence/provenance; (c) reusable generic design/code candidate; or (d) unknown pending path-level review.
2. Exclude (a) from the new target. In subsequent bounded passes, identify exact paths and dependencies; remove obsolete active artifacts only when the path is demonstrably exclusive to the retired server target and removal does not erase shared contracts or working generic components.
3. Preserve (b) as clearly marked historical audit evidence; do not silently rewrite history or confuse historical attempts with current deployment state.
4. Admit (c) only through the component-admission gate: source/version pin, license/security review, compatibility with the new hardware, architecture ownership, and explicit status. Prior unsuccessful installation is not evidence that a component is required or useful.
5. Do not infer the new hardware topology, OS, node identities, model inventory, storage, network, or provider policy: these remain UNKNOWN until backed by owner-supplied hardware facts or accepted target design.

### Clean-slate target artifacts

Build one target-only package with: (i) target system map; (ii) authoritative component inventory with role, source/pin, license, dependencies, target compatibility, status and evidence; (iii) one accepted contract set with owners and versioning; (iv) one traceability/coverage matrix from requirements to components, interfaces, controls and acceptance evidence; (v) conflict ledger whose every item is fixed, accepted exception, historical/retired, blocked, or owner decision; and (vi) a deployment/qualification plan kept separate from actual qualification evidence.

### Scope and safety

This entry records the owner's target direction; it does **not** claim that legacy files have already been deleted or that a new system has been implemented. No files outside documentation were deleted or changed in this pass. Broad repository deletion is deferred until an inventory identifies exact old-server-exclusive paths and their dependency/reference impact. No tests, installs, qualification, provider calls, credentials, host/runtime inspection, infrastructure changes or deployment were performed.

### Estimate after scope change

Planning estimate remains **10–20 focused working days** for target-only source reconciliation, legacy/target classification, component inventory, conflict ledger, one coherent draft contract set and traceability matrix, assuming bounded passes and no major new subsystem discovery. This is not elapsed calendar time: at 2–4 focused hours/day it is approximately 3–6 calendar weeks. Implementation, hardware-specific integration, tests/qualification and independent Contour A acceptance are separate phases and cannot be responsibly estimated until the target hardware facts and owner decisions are recorded. The measurable objective is zero known untriaged conflicts, not an absolute guarantee of zero defects.


## 16. Old-server artifact triage — source evidence and dispositions (2026-10-15)

This section implements the owner direction to build a new system for new hardware. “Old-server install attempts” and their observed runtime state are not valid target requirements or evidence. Dispositions are preliminary and do not assert the new hardware inventory.

| Path | Source-backed observation | Disposition | Guardrail / next action |
|---|---|---|---|
| .github/workflows/mediahub-one-time-storage-migration.yml (blob b0f71f515419067c6b1508dc073b2dbce4f2ca7b) | Workflow checks host mh-dev-01, targets /srv/mediahub, and contains git rm/commit self-removal logic. | RETIRE CANDIDATE — high risk if accidentally dispatched. | Never invoke. Verify references and remove from target branch only after confirming it is not required by a current approved process; Git history preserves provenance. |
| .github/workflows/mediahub-runner-migration-smoke.yml (blob 1f6682584d51b8155e66959734d1f335802dde67) | Targets mh-dev-01, runner user mediahub-runner, and checkout ref implementation/p0-06-core-runtime-services; runs lifecycle tests. | RETIRE CANDIDATE / HISTORY. | Do not run against old runners. Close references and retain enough historical evidence before retiring active workflow. |
| ops/systemd/mediahub-astra-github-bootstrap.service (blob bb88eb20bd2127c9c70a223bc07025ee9c150916) | Hardcodes ASTRA_NODE_ID=mh-dev-02, /home/mediahub/astra-work, and clones repository main. | RETIRE CANDIDATE — old-host binding. | Do not install/start. Check service references and old-host ownership before removal. |
| ops/qualification/run_distributed_local_worker.py (blob 42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d) and .github/workflows/astra-distributed-local-worker.yml (blob f650f2416c19dc75b4a0eeec037661c0c6169910) | Hardcoded node aliases, users, model tags and runner labels; current workflow's mh-dev-02 path permits Claude while another control workflow pins Codex. | TARGET-EXCLUDED pending fresh admission; generic logic may be reusable. | Do not treat any listed node/model as a new-hardware fact. Resolve route contract only after target topology is specified. |
| ops/astra-github-bootstrap.sh (blob 5f36f35ea85f55e5f49af6d3dabb5e876fffa09b), deploy/mediahub-astra-github.service (blob e1962e4afe5db7ac1fcb901344d9f88205de0689), deploy/com.mediahub.astra.github-agent.plist (blob 2cca029b502fd911ec38272871c823a8717ed8fd) | Generic-looking bootstrap/service templates; service has fixed /opt/mediahub/astra paths. | REUSE CANDIDATE, NOT APPROVED. | Re-admit only after new OS/path/security/identity design; do not assume portability. |
| docs/checkpoints/MEDIAHUB-PARTIAL-PASS-EVIDENCE-AND-PORTABLE-DEPLOYMENT-PROFILES-WAVE-01-2026-10-14.md (blob 529eed85da2828c9b062c8ef86de07b01ba9746e) | Contains prior observations of mh-dev-02 and Voktors Mac mini and clearly labels hardware profiles as proposals. | HISTORY. | Preserve provenance; do not use old runtime observations as target qualification evidence. |
| docs/checkpoints/mediahub-unified-architecture-and-deployment-contract-v0.1.md (blob 71ae0e68cc6ad494f85f33f64cde09ef5c4273d7) | Cross-domain proposal; explicitly not accepted/frozen, components/hardware are target-gated. | RECONCILE, NOT DELETE. | Keep as draft input; do not promote proposed components or hardware to accepted baseline. |

### Deletion boundary

No files were deleted in this pass. The source tree establishes several strong retirement candidates, but code-search did not provide a reliable cross-reference closure and the new hardware inventory has not yet identified which physical/logical identities are definitively retired. Removing shared source or normative contracts by inference would risk losing reusable code or accepted requirements. Next pass: close references for the first three candidates and retire only exact old-target-exclusive active artifacts; keep history and reusable generic components separate.

### Estimate

Remaining static reconciliation estimate: **10–20 focused working days** for a target-only map, component allowlist, coherent draft contract set, traceability matrix and conflict ledger, assuming no major new subsystem is discovered. At 2–4 focused hours/day: about **3–6 calendar weeks**. This is not a promise of zero defects: the defensible criterion is zero known untriaged conflicts. New-hardware implementation, qualification and independent Contour A acceptance are additional phases, currently not estimable without hardware specifications and owner decisions.


## 17. Owner clarification — clean-slate system for new hardware (2026-10-15)

**Owner direction recorded:** the system discussed since the Mac Pro, Mac mini server and remote video server entered the project—including Jarvis, the multi-agent system and the agent corporation—is one new system being designed from the ground up for new hardware. It is not a migration or continuation of the failed old-server installation attempts.

### Target-state rules

1. Old-server identities, observed paths, package/install attempts, runtime state, runner labels, model availability and deployment outcomes are **LEGACY / NOT TARGET EVIDENCE**. They must not determine the new topology or be reported as working components.
2. Preserve product requirements, architecture ideas and source provenance separately from old deployment details. Mature GitHub projects/components may be considered as candidates, but each requires fresh source pinning, license/security review, interface fit, isolation, owner approval and target qualification before admission.
3. Every artifact receives an explicit disposition: RETIRE (confirmed old-target-only active artifact), HISTORY (preserve audit provenance), REQUIREMENT-CANDIDATE (validate against Baseline 2.0 and owner decisions), REUSE-CANDIDATE (fresh admission required), or UNKNOWN (evidence insufficient). No bulk deletion by filename or age.
4. The three confirmed old-target-bound active artifacts removed from this documentation branch in this pass are:
   - .github/workflows/mediahub-one-time-storage-migration.yml — old mh-dev-01 /srv/mediahub migration workflow; prior blob b0f71f515419067c6b1508dc073b2dbce4f2ca7b.
   - .github/workflows/mediahub-runner-migration-smoke.yml — fixed mh-dev-01 runner and implementation/p0-06-core-runtime-services target; prior blob 1f6682584d51b8155e66959734d1f335802dde67.
   - ops/systemd/mediahub-astra-github-bootstrap.service — fixed mh-dev-02, /home/mediahub/astra-work and main checkout; prior blob bb88eb20bd2127c9c70a223bc07025ee9c150916.
   These deletions affect only docs/mediahub-chat-tree-map-20261012; no merge/integration into main was performed. Git history preserves the removed blobs.
5. Related worker/workflow code with mixed reusable logic and old node/model bindings remains TARGET-EXCLUDED / RECONCILE; it is not automatically deleted or admitted. Shared code, security invariants, Baseline 2.0 requirements and historical evidence are not legacy merely because they predate the new hardware.
6. New hardware identity/specifications, OS, topology, network, storage, compute, model/runtime selection and deployment boundaries remain UNKNOWN until supplied by the owner or explicitly accepted through architecture governance. Do not invent a hardware bill of materials.

### Reconciliation target and estimate

The target deliverables remain one navigable map; one component allowlist with lifecycle/disposition and evidence; a coherent versioned contract register; a requirement → component → interface → security control → verification evidence matrix; and a conflict ledger with no known untriaged entries. Current planning estimate: **10–20 focused working days** for static source reconciliation and these architecture artifacts, approximately **3–6 calendar weeks at 2–4 focused hours/day**. This is a planning range, not a guarantee of zero defects. Implementation, qualification, deployment and independent Contour A acceptance are separate, currently unestimated phases pending hardware specifications and owner decisions.

No tests, workflows, installers, models/providers, credentials, host/runtime, qualification or deployment were invoked in this pass.


## 18. Clean-slate disposition of legacy executor control paths (2026-10-15)

### Bounded source evidence

| Artifact | Source-backed finding | New-system disposition |
|---|---|---|
| `.github/workflows/astra-chat-control.yml` (blob `51b17ec2410032772f9baa1de4afedb6b000f3c4`) | Its parser accepts `codex` or `claude` and accepts `mh-dev-02` or `Voktors-Mac-mini.local`; the later execution step hardcodes `ASTRA_NODE_ID=mh-dev-02`, `ASTRA_EXECUTOR=codex`, and asserts the same node/executor. The accepted input domain is broader than the actual dispatch step. | LEGACY / TARGET-EXCLUDED. Do not repair this route for the retired target; do not use it as the new system's routing contract. |
| `.github/workflows/astra-distributed-local-worker.yml` (blob `f650f2416c19dc75b4a0eeec037661c0c6169910`) | Dispatch offers Claude only and binds execution to `mh-dev-01`, `mh-dev-02`, or `Voktors-Mac-mini.local`, with old runner labels, hostnames, users, FCC paths and Ollama model tags. | LEGACY / TARGET-EXCLUDED. No target admission. |
| `ops/qualification/run_distributed_local_worker.py` (blob `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`) | Hardcodes the same old node identities, users, model tags, pools and filesystem paths in `NODE_CONFIG`; it does not load the routing/node-role YAMLs in the inspected path. | LEGACY IMPLEMENTATION; do not carry forward by default. Any reusable algorithm must be extracted and re-reviewed independently against the new contracts. |
| `control/qualification/distributed-runner-contract.json` (blob `993f51f07c7937165ffb3bfbe59cd0801ea71ec0`) | Names `mh-dev-01` as canonical and the other named nodes as non-authoritative; its hostname allowlist explicitly aliases two Voktors names. | LEGACY TOPOLOGY CONTRACT; not a new-hardware contract. |
| `tests/test_distributed_local_worker.py` (blob `5fd79a665ef49e4e594a8fbccb8d77ec1f0659ae`) | Test source is coupled to the old worker implementation. | HISTORY / LEGACY TEST; not evidence of target compatibility or acceptance. Not run. |

### Disposition decision for this pass

- These artifacts are now classified as **LEGACY / TARGET-EXCLUDED**, not as active target components and not as a backlog to fix for old servers. This closes the question of which executor value the retired workflow should use: no value is selected for the new system from these artifacts.
- Do not infer that the generic worker implementation is worth reusing. The new system's agent corporation, Jarvis control plane, ASTRA responsibilities, task/result contracts and component choices must be designed from accepted requirements and freshly admitted mature components.
- The source trace establishes an internal legacy route inconsistency, but no workflow or worker was invoked and no runtime behavior was tested. This finding must not be presented as a new-system defect.
- No source code, workflows, tests or runtime artifacts were deleted in this pass. Before deleting additional files, close repository references and dependencies, then delete only exact old-target-exclusive active artifacts in a separate bounded pass. Preserve provenance and accepted Baseline 2.0/security/authority requirements.
- New hardware, OS, topology, node identities, model/runtime, network and storage remain UNKNOWN until owner-supplied or explicitly accepted. No component is admitted to the target by this classification alone.

**Next bounded step:** inventory remaining active old-node-bound workflow/service/config artifacts and their references; retire only those proven old-target-exclusive. In parallel, start the target-only component allowlist from requirement-to-capability needs—not from the existing worker inventory.


## 19. Additional legacy-bound workflow and service references (2026-10-15)

Status: **SOURCE-ONLY CLASSIFICATION / TARGET EXCLUSION; no runtime or deployment claim**.

The greenfield direction is now explicit: the MediaHub/Jarvis/ASTRA multi-agent corporation discussed around the prior Mac Pro, Mac mini and remote video-server setup is a newly designed target for new hardware. Old-server installation attempts and their node-specific execution topology are not the target baseline. Existing repository artifacts are not automatically valid simply because they are present.

| Artifact | Source evidence | Greenfield disposition |
|---|---|---|
| `.github/workflows/astra-autonomous-supervisor.yml` (blob `a0209a2d01122354d19e95d2f362a6ecfa3d6186`) | Hardcodes `mh-dev-01`, `mediahub-runner`, `/home/mediahub/astra-work`, old command/result paths and old-node HMAC secret mapping. | **LEGACY-BOUND / TARGET-EXCLUDED** as an execution route. Do not repair for old hardware. Reuse generic patterns only after contract/security review. |
| `ops/launchd/com.mediahub.astra.github-agent.plist` (blob `d1d8aea99c2303c26e542a3d1c5e54b4596521d0`) | Hardcodes `/Users/voktor/astra-work`, `/Users/voktor/astra-state`, and `Voktors-Mini.Dlink`. | **LEGACY-BOUND / TARGET-EXCLUDED** deployment definition. |
| `ops/systemd/mediahub-mesh.service` (blob `bfa8b075229385ac14b8ba34dccad84275d1c474`) | Hardcodes `/home/mediahub/astra-work`. | **LEGACY-BOUND / TARGET-EXCLUDED** deployment definition. |
| `deploy/mediahub-astra-github.service` (blob `e1962e4afe5db7ac1fcb901344d9f88205de0689`) and `deploy/com.mediahub.astra.github-agent.plist` (blob `2cca029b502fd911ec38272871c823a8717ed8fd`) | Service/launch-agent artifacts exist; the first has a systemd unit shape, while the fetched plist did not expose old-node strings in the bounded search. | **UNADMITTED / HOLD** pending full path/dependency closure; do not label both definitively old-node-exclusive based on filename alone. |
| `ops/node/mh-dev-02-mesh-check.sh` (blob `e588f8d07922ebfe1ad1322d2702c08b2b7eb702`) | Hardcodes Linux user paths under `/home/mediahub` and old FCC/llama.cpp executable locations. | **LEGACY-BOUND / TARGET-EXCLUDED** diagnostic script. |
| `.github/workflows/astra-chat-control.yml` and `.github/workflows/astra-distributed-local-worker.yml` | Prior §18/§97 trace established fixed old node IDs, runner labels, executor restrictions, hostnames, model tags and hardcoded dispatch/worker values. | **LEGACY-BOUND / TARGET-EXCLUDED** execution routes. Do not fix by reconciling old hardware configurations. |
| `.github/workflows/mediahub-claude-worker.yml` (blob `e1260cfef88ac02bcc9d0cce67bb497820f5f63c`) | Contains a dependency installation step and bounded Claude invocation; no old host identity was found in the inspected lines. | **UNADMITTED REUSE CANDIDATE**, not a selected target component. Requires independent review of external model/provider use, permissions, supply chain, isolation and the new execution contract. |
| `.github/workflows/mediahub-agent-fabric-verify.yml` (blob `2cec0ba1f02018f7037417363c707a13bc673117`) | Verification workflow installs pytest; no target hardware identity was established in the inspected lines. | **UNADMITTED VERIFICATION CANDIDATE** only. It is not proof of passing checks and was not invoked. |

### Deletion and evidence rule

This pass does **not** delete repository artifacts. Presence in the repository, a legacy-looking filename, or old deployment evidence alone is insufficient to prove that a file is safe to delete: first close tracked and textual references, imports, workflow calls, service references, docs links and tests; then delete only exact old-target-exclusive active artifacts in a separate bounded change. Preserve historical records and provenance, but clearly label them **HISTORICAL / NOT TARGET** so they cannot be mistaken for the new system. Do not remove Baseline 2.0 or accepted security/authority invariants merely because old deployment assumptions are retired.

### Target baseline consequences

- No old node, server hostname, old user path, old model tag, old runner label, previously attempted installation or old deployment result is carried into the new target by default.
- The Mac Pro / Mac mini / remote video server discussion is retained as requirements and design context, not as evidence of current hardware state or a deployment baseline.
- Target component admission must start from capability requirements, independently reviewed mature upstream components, immutable source/version pins, license/security/supply-chain review, explicit interfaces, owner decisions and evidence gates.
- Hardware/OS/topology, node identities, storage/network boundaries, model runtime and provider policy remain **UNKNOWN** until supplied or explicitly accepted. No component is admitted by this classification.
- Next: close remaining old-node references with a source-only dependency map, then produce a target-only component allowlist and a single requirements → component → interface → control → evidence matrix.


## 14. Owner decision — greenfield system reset (2026-10-15)

- **Decision status:** EXPLICIT OWNER DIRECTION RECORDED; detailed target architecture and component admission remain OPEN.
- **Scope:** the intended MediaHub OS system is a new greenfield design for new hardware. The Mac Pro, Mac mini/server, remote video server, Jarvis, multi-agent corporation and Astra concepts discussed in the project belong to the new target system being designed from scratch; they are not proof that the old deployments worked or that any component is currently installed, usable, qualified or accepted.
- **Legacy boundary:** prior attempts to install or operate components on old servers are not the target runtime baseline. Do not treat old host-specific configuration, deployment assumptions, runtime observations, credentials/paths, failed installation instructions, or stale qualification claims as requirements for the new system. Re-evaluate every candidate component against current upstream source, maintenance, license, security, isolation, hardware/OS compatibility, interface contracts and explicit admission evidence.
- **Repository hygiene:** identify legacy operational artifacts and remove or quarantine them only after a path/ID/dependency impact review. Preserve historical IDs and audit evidence where required; archival records must be explicitly marked HISTORICAL / NOT TARGET CONFIGURATION, not silently reused as active contracts. This instruction does not authorize deleting unrelated history or changing accepted normative contracts by inference.
- **New source of truth:** the greenfield target needs one readable architecture map, one versioned system contract, one component inventory/admission ledger, one traceability matrix (requirement → component/interface → contract → verification evidence → status), and a decision log. Each item must distinguish PROPOSED, ACCEPTED, IMPLEMENTED, VERIFIED, QUALIFIED, DEPLOYED and ACCEPTED-INDEPENDENTLY.
- **Admission rule:** GitHub projects are candidates only until reviewed and pinned to immutable upstream revisions with license/provenance, maintenance/security, dependency/SBOM, runtime compatibility, isolation/permission, egress and contract-fit evidence. No component is considered selected merely because it appeared in earlier discussion or old repository configuration.
- **Non-goals for this pass:** no old host/runtime access, install, provider/model invocation, tests/qualification, deployment, migration, branch integration or bulk deletion. No new hardware inventory was supplied in this decision, so hardware-specific compatibility remains OPEN.
- **Replaces the previous next-step priority:** do not continue tracing old-server executor routing as though it were the target design. First build a greenfield/legacy separation ledger and map the desired system's domains and contracts; then shortlist mature components and admit them one by one.

### Planning estimate (not a promise)

For a repository-wide, source-backed first pass, budget roughly **2–4 focused working days** for inventory, conflict/duplicate classification, target architecture map, contract skeleton and component shortlist. Expect another **3–7+ focused working days** for owner decisions, upstream component due diligence, contract closure and remediation proposals. This excludes implementation, tests/qualification, deployment and independent acceptance; hardware/OS details, unresolved authority decisions and branch reconciliation can extend the schedule. “No conflicts/errors” can only be claimed against a defined scope and completed verification evidence, not guaranteed globally in advance.


### 20.278 Greenfield / legacy artifact ledger pass (2026-10-15)

- New ledger: [Greenfield / Legacy Artifact Ledger, Wave 01](../architecture/MEDIAHUB-GREENFIELD-LEGACY-ARTIFACT-LEDGER-WAVE-01-2026-10-15.md).
- This pass adopts the owner's clean-slate clarification: Mac Pro, Mac mini/server, remote video server, Jarvis, Astra, multi-agent system and corporation are the new target design; prior old-server attempts are not target runtime baseline.
- The ledger classifies known old-node routing and service artifacts as LEGACY-OPERATIONAL or SHARED-OR-UNKNOWN, while holding registries, schemas, runtime modules and normative security/baseline artifacts until their references and semantics are reviewed.
- No repository files were deleted. A source-backed classification does not establish that a file is safe to delete; exact paths, blob SHAs, reverse references, IDs and reusable invariants must be closed first.
- New hardware/OS/topology inventory is still absent from reviewed evidence. No hardware compatibility claim is made.
