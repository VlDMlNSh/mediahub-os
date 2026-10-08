# ASTRA GOLD — Unified Autonomous Development System

Status: CANONICAL / QUALIFICATION-READY DESIGN
Version: 1.0
Date: 2026-10-02
Scope: MediaHub OS / MediaHub iOS

## 1. Definition

**ASTRA GOLD is the complete distributed autonomous development system.**

It is not a name for Astra coordinator alone. ASTRA GOLD is the integrated control, execution, verification, transport, provider, evidence, recovery, queue, security and observability fabric used to develop MediaHub autonomously.

Qualification is therefore performed against the **whole system**, not against isolated components.

## 2. System topology
## 2.1 Candidate desktop execution surface: OpenFlux

OpenFlux is admitted to the architecture only as a **qualification-gated candidate desktop agent**. The identified candidate is the EDEAI/OpenFlux Tauri desktop agent, which documents multi-agent task splitting, multi-LLM connectivity, MCP/tool integration, browser automation, desktop control, memory, sandboxing and local execution. These capabilities are architectural candidates, not MediaHub qualification evidence. [External source: EDEAI/OpenFlux README]

Boundary:
- OpenFlux is **not** A0, A1, A2 or A3.
- OpenFlux has no coordination authority, provider authority, credential-creation authority or MediaHub State Authority.
- OpenFlux cannot promote itself or a provider to ASTRA GOLD eligibility.
- OpenFlux remains NOT_PROVEN until identity, provenance, sandbox boundary, non-mutating probe, bounded execution, result validation, recovery and independent A3 verification are demonstrated on an approved node.
- The canonical source identity currently recorded is EDEAI/OpenFlux; other projects named OpenFlux remain separate candidates until positively identified.

Placement: candidate_desktop_agents -> executor admission gate -> isolated workspace -> A3 verification.


```
                                  HUMAN AUTHORITY
                                        │
                         architecture / security / release
                                        │
                                  ┌─────▼─────┐
                                  │ ASTRA GOLD │
                                  └─────┬─────┘
                                        │
                             ┌──────────▼──────────┐
                             │ A0 ASTRA CONTROLLER │
                             │ coordination/state  │
                             └──────────┬──────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
        A1 ARCHITECT               A2 BUILDERS               A3 VERIFIER
        contracts/ADR              bounded changes           independent
              │                         │                      evidence
              └──────────────┬──────────┴──────────┬───────────┘
                             │                     │
                    DYNAMIC TASK-SCOPED WORKERS    │
                             │                     │
                             ▼                     ▼
                  ┌────────────────────────────────────────┐
                  │       AUTONOMOUS CONTROL PLANE          │
                  │ command → queue → claim → lease →      │
                  │ dispatch → heartbeat → result → replay │
                  │ recovery → integration → reconciliation │
                  └───────────────────┬────────────────────┘
                                      │
                         ┌────────────▼────────────┐
                         │     EXECUTION FABRIC    │
                         └────────────┬────────────┘
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       │                              │                              │
 LOCAL EXECUTORS                CLOUD PROVIDERS                 GATEWAYS
       │                              │                              │
 ┌─────┼──────────────┐       ┌───────┼───────────────┐       ┌──────┼──────────┐
 │     │      │       │       │       │       │       │       │      │          │
Codex Claude  Cursor  DeepSeek Gemini  Kimi  DeepSeek Perplexity ChatGPT  GigaChat
CLI   Code    Stagewise Harness  │      │      │        │        │          │
 │     │       │       │         └──────┴──────┴────────┴────────┴──────────┘
 │     │       │       │
 │     └── Claude Code is a LOCAL EXECUTOR ────────────────┐
 │                                                         │
 ├── Ollama / Kimi K3 In-C  (local model fabric)          │
 └── FreeLLMAPI              (local gateway)               │
                                                           │
                    ┌──────────────────────────────────────┘
                    │
                    ▼
        ┌──────────────────────────────────────────────────────┐
        │ CLOUD / ROUTING FABRIC                                │
        │ OpenRouter · UnoRouter · ZeroRouter · NaraRouter      │
        │ OrcaRouter · Claude gateway · FCC · OmniRoute          │
        │ SiliconFlow · Novita · Z.ai · LLM7 · SambaNova        │
        │ Aion Labs · Cloudflare · Groq · Mistral · HuggingFace │
        └───────────────────────┬───────────────────────────────┘
                                │
                       provider adapters / APIs
                                │
                                ▼
                 isolated workspace + build/test/runtime
                                │
                                ▼
                       A3 independent verification
                                │
                                ▼
                    integration / reconciliation
                                │
                                ▼
                      GitHub canonical evidence
                                │
                                ▼
                     heartbeat / recovery / soak
                                │
                                └──────► ASTRA GOLD loop
```

**Critical distinction:** Claude appears in two different architectural positions by design:
- **Claude Code** = local execution client / executor.
- **Claude** = provider/gateway identity for Anthropic-compatible cloud execution.
- **FCC** and **OmniRoute** = transport/gateway mechanisms, not agents.
- **ECC** = auxiliary support, not an executor authority.
- **OpenRouter/UnoRouter/ZeroRouter/etc.** = routing/provider gateways, not independent A0/A1/A2/A3 authorities.

## 3. Authority model

1. Human remains final authority for global architecture, production deployment, destructive changes, security-sensitive decisions and permanent governance changes.
2. A0 Astra is the single coordination authority.
3. A1 Architect owns architecture proposals, contracts and decision records within assigned scope.
4. A2 Builder performs bounded implementation.
5. A3 Verifier independently verifies integrated results.
6. Executor clients (Codex, Claude Code) have executor authority only.
7. FCC and OmniRoute are transport/routing mechanisms, not architecture or state authorities.
8. ECC is auxiliary support only; it has no provider-selection, credential-creation or state authority.
9. GitHub is the transport/evidence substrate, not MediaHub domain State Authority.
10. AI providers and cloud services never become MediaHub State Authority.

## 4. Component classes

### 4.1 Coordination
- A0 Astra
- mission decomposition
- scheduling
- claims
- conflict detection
- integration
- architecture reconciliation
- retry/recovery policy

### 4.2 Persistent role fabric
- A1 Architect
- A2 Builder
- A3 Verifier
- dynamic task-scoped instances
- bounded adaptive parallelism

### 4.3 Autonomous controller
- command ingestion
- command identity
- target SHA binding
- worker liveness
- claim leases
- queue advancement
- result publication
- restart/re-execution
- duplicate suppression
- failure classification
- recovery
- heartbeat

### 4.4 Complete execution and provider fabric

#### Local execution clients
- **Codex CLI** — local coding/repository/testing executor.
- **Claude Code CLI** — local coding/architecture/review executor. This is the Claude executor that has been under qualification.
- **Cursor** — local development tooling.
- **DeepSeek Harness** — local harness/subagent execution.
- **Stagewise** — local frontend/development tooling.

#### Local model/gateway layer
- **Ollama** — local model runtime.
- **Kimi K3 In-C** — local reasoning/coding model runtime.
- **FreeLLMAPI** — local gateway/provider adapter.

#### Direct cloud providers / agent identities
- Gemini
- Perplexity
- Kimi
- DeepSeek
- ChatGPT / OpenAI
- GigaChat
- SiliconFlow
- Novita
- Z.ai
- LLM7
- SambaNova
- Aion Labs
- Cloudflare Workers AI
- Groq
- Mistral
- Hugging Face

#### Cloud routing/gateway providers
- OpenRouter
- UnoRouter
- ZeroRouter
- NaraRouter
- OrcaRouter
- Claude/Anthropic gateway

#### Transport/adapters
- FCC
- OmniRoute
- GitHub transport
- provider-specific adapters

#### Auxiliary components
- ECC local assistant
- Delx Memory MCP / session handoff component

The repository's provider-model registry currently contains 23 candidate provider entries:
`siliconflow-1`, `siliconflow-2`, `novita-1`, `novita-2`, `zai-1`, `zai-2`, `kimi-1`, `llm7-1`, `sambanova-1`, `aionlabs-1`, `cloudflare-1`, `cloudflare-2`, `nararouter-1`, `orcarouter-1`, `unorouter-1`, `zerouter-1`, `deepseek-1`, `gemini-1`, `groq-1`, `mistral-1`, `mistral-2`, `openrouter-1`, `huggingface-1`.

These are **candidate provider/model entries**, not automatic qualification results.

#### Mandatory executor paths
The minimum whole-system executor matrix is:

1. Codex + FCC
2. Claude Code + FCC
3. Codex + OmniRoute
4. Claude Code + OmniRoute

The native Claude Code path is now explicitly represented as an additional qualification path:
5. Claude Code direct/native

Direct Codex/native and other provider-specific paths may be added after independent runtime proof.

### 4.5 Auxiliary intelligence
ECC is an explicit ASTRA GOLD auxiliary support component. It participates in the distributed scheme only as an advisory/diagnostic/context-support lane. It is not an A0/A1/A2/A3 role, not a provider, not a transport authority, and not a state authority.

ECC can assist with analysis where explicitly allowed, but it cannot:
- select providers;
- create credentials;
- mutate State Authority;
- bypass A3 verification;
- bypass qualification;
- redefine architecture.

### 4.6 Transport and persistence
- GitHub repository and branches
- command contracts
- claim/evidence records
- result records
- workflow execution
- artifact storage
- canonical branch reconciliation

### 4.7 Verification
- focused tests
- regression suite
- contract tests
- architecture conformance
- security boundary checks
- concurrency checks
- timeout/failure checks
- recovery checks
- independent A3 verification
- exact-SHA evidence

### 4.8 Observability and recovery
- structured logs
- health/heartbeat
- worker identity
- duplicate detection
- queue state
- evidence freshness
- timeout/retry state
- restart/recovery
- 24h soak
- failure injection

## 5. Hybrid admission model

Every provider/executor follows the same fail-closed ladder:

`REGISTERED → CREDENTIAL_PRESENT → AUTH_SUCCESS → MODEL_DISCOVERY_PASS → PROBE_PASS → EXECUTION_PASS → A3_VERIFIED → ASTRA_GOLD_ELIGIBLE`.

Missing or historical evidence never promotes a provider. A gateway response never proves native-provider qualification. Claude Code execution through FCC/OmniRoute proves an executor+transport path, not Anthropic-native API qualification.

## 6. Core lifecycle

Every autonomous mission follows:

```
DISCOVER
  -> DECOMPOSE
  -> CLAIM
  -> EXECUTE
  -> VERIFY
  -> CONFLICT ANALYSIS
  -> INTEGRATE
  -> SYSTEM VERIFY
  -> ARCHITECTURE RECONCILIATION
  -> EVIDENCE COMMIT
  -> CLOSE
```

A mission is not complete because an executor reports success. Completion requires fresh observable evidence.

## 7. Unified ASTRA GOLD state machine

```
DESIGNED
  -> PREFLIGHT
  -> ADMITTED
  -> QUALIFICATION
  -> EXECUTION
  -> VERIFICATION
  -> INTEGRATION
  -> RECONCILIATION
  -> SOAK
  -> GOLD_ACTIVE

Any failed mandatory gate
  -> BLOCKED
  -> DIAGNOSE
  -> REPAIR
  -> PREFLIGHT
```

No state may transition to GOLD_ACTIVE using historical evidence.

## 8. Qualification model

Qualification is a system qualification. The canonical gate ids, names and
numeric thresholds live in the single machine-readable source
`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`; this section summarizes it.

### G0_IDENTITY — Identity
- canonical node identity
- runner identity
- executor identity
- provider/model identity
- repository identity
- exact source SHA
- clean worktree

### G1_BOUNDARY — Boundary
- authority boundary
- transport boundary
- state-authority boundary
- credential boundary
- isolated workspace

### G2_CONTROL_PLANE — Control Plane
- Astra coordinator
- command contract
- claim lease
- queue progress
- duplicate suppression
- result publication
- heartbeat

### G3_EXECUTION_PATH — Execution Path
For each Codex/Claude path:
- executable/runtime identity
- provider identity
- exact source SHA
- isolated workspace
- marker probe
- timeout enforcement
- malformed-result rejection
- nonzero exit handling
- result schema validation

### G4_23_WAVE_QUALIFICATION — 23-Wave Qualification
Minimum 23 fresh rounds for every mandatory execution path:
1. CODEX_FCC
2. CLAUDE_FCC
3. CODEX_OMNIROUTE
4. CLAUDE_OMNIROUTE
5. CLAUDE_CODE_DIRECT

A missing launcher is BLOCKED, not PASS.

### G5_CONCURRENCY — Concurrency
- maximum three concurrent autonomous claims by default (G-5), one per permanent executor lane
- disjoint write boundaries required
- shared surfaces serialized
- collision detection
- duplicate-controller rejection
- independent evidence

### G6_RECOVERY — Recovery
- executor timeout
- executor failure
- transport interruption
- stale claim
- worker restart
- duplicate controller
- replay/idempotency
- result publication recovery

### G7_INTEGRATED_A3 — Integrated A3
A3 verifies the complete integrated result independently of A0/A2 assertions.

### G8_PRE_SOAK — Pre-Soak
All required evidence bundles must be fresh and PASS.

### G9_24H_SOAK — 24H SOAK
- canonical controller remains alive
- queue remains serviceable
- heartbeat remains fresh
- executor admission remains fail-closed
- recovery path remains functional
- no unauthorized authority transfer
- evidence remains publishable

### G10_LAUNCH_READY — Launch Ready
Only after fresh PASS of G0–G9 and a complete launch-input bundle.

### G11_LAUNCH — Human Launch
HUMAN_ONLY. Requires release SHA, evidence bundle, A3 record, soak record and
rollback target.

## 9. Evidence contract

Every qualification result must contain:
- schema version
- mission/command ID
- node ID
- controller identity
- executor identity
- provider identity
- exact source SHA
- start/end timestamps
- round number
- exit status
- timeout status
- marker status
- workspace identity
- mutation result
- verification result
- failure classification
- evidence references
- credential status = SUPPRESSED

Historical evidence cannot satisfy a fresh gate.

## 10. Fail-closed rules

The system MUST block when:
- launcher is missing;
- executable identity is ambiguous;
- provider identity is ambiguous;
- source SHA cannot be proven;
- workspace isolation cannot be proven;
- marker probe is absent;
- timeout cannot be enforced;
- malformed result is accepted;
- A3 evidence is missing;
- evidence is stale;
- transport state is uncertain;
- claim ownership is ambiguous;
- duplicate controller ownership exists.

## 11. Controller 24/7 contract

The autonomous controller is a continuously supervised state machine, not a single shell process.

Required properties:
- one canonical coordination owner;
- bounded worker concurrency;
- durable command identity;
- idempotent claim handling;
- heartbeat;
- liveness detection;
- restart/re-exec;
- stale-claim recovery;
- duplicate-worker prevention;
- queue advancement;
- evidence publication;
- fail-closed degradation;
- periodic integrated verification.

A scheduled GitHub workflow alone is not sufficient proof of a 24/7 controller. The controller itself must remain alive and produce fresh heartbeat/evidence records throughout the soak.

## 12. Security boundaries

- credentials never committed;
- credentials never emitted in evidence;
- executor cannot become architecture authority;
- transport cannot become state authority;
- cloud provider cannot bypass admission;
- ECC cannot create credentials;
- A2 cannot self-verify;
- A0 cannot self-certify a disputed implementation;
- A3 must remain independently verifiable;
- destructive/production actions require explicit human authorization.

## 13. Qualification result semantics

Only these top-level states are valid:

- PASS — every mandatory gate has fresh evidence.
- BLOCKED — required capability/evidence is unavailable.
- FAILED — a required test executed and failed.
- RECONCILIATION_REQUIRED — system state is uncertain.
- NOT_APPLICABLE — explicitly excluded by architecture contract.

There is no implicit PASS.

## 14. Canonical implementation boundary

ASTRA GOLD owns the autonomous development fabric.

MediaHub product domains remain separate:
- Media domain
- Document domain
- Digital Twin domain
- Smart Home domain
- Engineering domain
- Asset metadata
- UI/API
- persistence
- recovery
- update/release

ASTRA GOLD may develop and verify these domains but must never silently become their domain State Authority.

## 15. Target repository layout

```
.github/agent-system/       governance
.github/agents/             role profiles
.github/workflows/          controller and qualification automation
architecture/               canonical architecture
control/commands/           command contracts
control/claims/             claims
control/results/            execution results
control/qualification/      qualification contracts/evidence
ops/agent-fabric/           executor routing
ops/qualification/         qualification executors
runtime/                    autonomous runtime
evidence/                   fresh qualification evidence
tests/                      verification
```

## 16. Definition of ready

ASTRA GOLD is **qualification-ready** when:
1. the unified contract is committed;
2. all mandatory components have one canonical owner;
3. all executor paths are explicitly classified;
4. qualification gates are machine-readable;
5. the controller can ingest and publish commands/results;
6. 23-wave evidence can be generated fresh;
7. recovery tests are defined;
8. 24h soak is explicitly gated;
9. no component can silently acquire authority outside its role.

ASTRA GOLD is **GOLD_ACTIVE** only after actual execution proves those properties.

## 17. Current truth

As of 2026-10-02 the architecture is being normalized to this unified ASTRA GOLD definition.

The repository already contains substantial pieces: Astra coordination, A1/A2/A3 role contracts, autonomous queue, provider routing, qualification workflows, pre-soak/GOLD workflows, evidence contracts and recovery mechanisms.

The current runtime qualification is not yet PASS because the canonical GitHub Actions execution has been observed pending with no executing job, and fresh 23-wave executor evidence has not been produced.

This document therefore defines the target qualification surface; it does not convert unverified runtime behavior into PASS.
