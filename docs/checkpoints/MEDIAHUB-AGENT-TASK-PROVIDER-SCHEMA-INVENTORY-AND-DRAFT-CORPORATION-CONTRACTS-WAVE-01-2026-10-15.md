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
