# ASTRA GOLD — COMPLETE COMPONENT SCHEME

Status: CANONICAL ARCHITECTURAL RECONCILIATION / QUALIFICATION INVENTORY
Date: 2026-10-02
System: MediaHub OS / MediaHub iOS

## 1. Authority hierarchy

Human = final architecture, production, security and launch authority.
A0-ASTRA = single coordination and MediaHub State Authority.
A1 = architecture/contracts.
A2 = bounded implementation.
A3 = independent verification.
Executors = execution only.
Providers, models, gateways, transports and candidate tools never gain MediaHub authority by registration or use.

## 2. Lifecycle

DISCOVER → PREFLIGHT → ADMIT → QUALIFY → EXECUTE → VERIFY → INTEGRATE → RECONCILE → PRE_SOAK → SOAK_24H → LAUNCH_READY → HUMAN LAUNCH.

Failure: BLOCKED → DIAGNOSE → REPAIR → PREFLIGHT.

## 3. Core components

| Component | Class | Authority | Status / role |
|---|---|---|---|
| Human | final authority | final | architecture/security/production/launch |
| A0-ASTRA | coordinator | A0 | decomposition, claims, scheduling, integration, reconciliation, state |
| A1 | architect | A1 | contracts and architecture |
| A2 | builder | A2 | bounded implementation |
| A3 | verifier | A3 | independent verification |
| Codex | executor | none | bounded implementation/testing |
| Claude Code | executor | none | bounded implementation/testing |
| Cursor | local tooling | none | execution surface |
| DeepSeek Harness | local harness | none | execution surface; qualification required |
| Stagewise | local tooling | none | execution surface; qualification required |
| ECC | auxiliary | none | analysis/context/diagnostics |
| Delx Memory Bun | auxiliary | none | auxiliary memory/context |

## 4. Transport and routing

Transport is never MediaHub State Authority.

- GitHub Transport — repository/evidence transport.
- FCC — execution transport/gateway.
- OmniRoute — execution transport/gateway.
- OpenRouter — provider gateway.
- UniRouter — provider gateway.
- ZeroRouter — provider gateway.
- NaraRouter — provider gateway.
- OrcaRouter — provider gateway.
- FreeLLMAPI — local gateway candidate; routing only until qualified.

## 5. Cloud/provider fabric

Registered provider identities:
Gemini, Perplexity, Kimi, DeepSeek, ChatGPT/OpenAI, Claude/Anthropic, GigaChat.

Provider catalog candidates:
SiliconFlow, Novita, ZAI, LLM7, SambaNova, AionLabs, Cloudflare, Groq, Mistral, Hugging Face.

Provider rule:
REGISTERED ≠ CREDENTIAL_PRESENT ≠ AUTH_SUCCESS ≠ MODEL_DISCOVERY_PASS ≠ PROBE_PASS ≠ EXECUTION_PASS ≠ A3_VERIFIED.

## 6. Local inference/model fabric

| Component | Type | Qualification |
|---|---|---|
| Ollama | local inference runtime | NOT_PROVEN |
| Kimi K3 In-C | local model/runtime | NOT_PROVEN |
| Gemma 4 | local model family | NOT_PROVEN |
| MiniCPM-V 4.5 8B 1MK | candidate local multimodal model | NOT_PROVEN |

Model admission is variant-specific:
exact identity → checkpoint/weight provenance → runtime identity → resources → non-mutating probe → reasoning/code probe → tool probe → multimodal probe where applicable → latency/memory → recovery → isolated execution → result validation → A3.

## 7. Candidate autonomous/execution systems

| Candidate | Type | Status | Boundary |
|---|---|---|---|
| OpenOPC | autonomous development system | NOT_PROVEN | execution surface only |
| OpenFlux | desktop agent | NOT_PROVEN | execution surface only |
| SoL-Pi | autonomous research/agent harness | NOT_PROVEN | execution surface only |
| Colibri | coding/agent candidate | NOT_PROVEN | no authority |
| unlazy | developer-tool candidate | NOT_PROVEN | no authority |

None may coordinate ASTRA, select providers, create credentials, own state, self-qualify or self-promote.

## 8. Browser/web candidates

| Candidate | Type | Status |
|---|---|---|
| WebTool-DeepSeek | browser extension/web-agent tooling | NOT_PROVEN |
| codex-chatgpt-web | browser bridge/coding harness | NOT_PROVEN |

Required security qualification:
browser-session isolation, cookie/token isolation, tool permission boundary, prompt-injection resistance, account/session recovery, auditability.

## 9. Coding harness / IDE candidates

DeepSeek Harness, Stagewise, SoL-Pi and OpenOPC require:
workspace isolation, subprocess boundary, tool allowlist, plugin boundary, bounded execution, review/rework integrity, cancellation, timeout, worker recovery and replay idempotency.

## 10. Discovery/routing candidates

| Candidate | Type | Status |
|---|---|---|
| free-coding-models | model discovery/router | NOT_PROVEN |
| FreeLLMAPI | LLM gateway/router | NOT_PROVEN |

These components may discover or route providers/models. They cannot become MediaHub State Authority or credential authority.

## 11. Security-tool candidate

| Candidate | Type | Status |
|---|---|---|
| naabu | bounded security/networking tool | NOT_PROVEN |

Qualification requires explicit target scope, safe/dry-run operation, network permission boundary, rate limits, audit trail and destructive-action prohibition.

## 12. Complete review inventory

1. OpenOPC
2. OpenFlux
3. Gemma 4
4. MiniCPM-V 4.5 8B 1MK
5. SoL-Pi
6. Colibri
7. WebTool-DeepSeek
8. DeepSeek Harness
9. Stagewise
10. free-coding-models
11. FreeLLMAPI
12. unlazy
13. naabu
14. codex-chatgpt-web

All are REVIEW/QUALIFICATION candidates unless independently qualified.

## 13. Mandatory executor matrix

1. Codex + FCC
2. Claude Code + FCC
3. Codex + OmniRoute
4. Claude Code + OmniRoute
5. Claude Code direct/native

23 fresh successful isolated rounds per path = 115 mandatory rounds. These five combinations are qualification-test paths and do not replace the three permanent Claude production scheduler lanes.

Per round:
fresh command ID, exact source SHA, executor identity, provider/transport identity, isolated workspace, exit status, timeout, marker and schema-valid result.

## 14. Control plane

**Lane mapping note (2026-10-12):** the current repository queue binds `mh-dev-01`, `mh-dev-02`, and `Voktors-Mac-mini.local` as three temporary qualification-harness lanes. That is not the final hardware plan. The intended developer fleet is the purchased Mac Pro plus a Linux Mac mini Mid-2011 (planned 16 GB RAM); the Mac mini M2 is the first MediaHub product prototype and must be removed from the permanent ASTRA developer pool at commissioning. Until the queue, machine-readable G5 thresholds, task IDs, workflow routing and topology tests are reconciled, the target deployment remains BLOCKED. Start the target with two physical-host claims; extra logical lanes require explicit isolation/capacity evidence.

Required:
command contract, claim/lease, queue progress, duplicate suppression, heartbeat, result publication, stale-claim handling, worker restart, duplicate-controller rejection and replay idempotency.

Concurrency:
maximum 3 autonomous claims, matching the canonical governance contract, qualification schema, reference architecture and topology tests; claims disjoint; shared surfaces serialized.

## 15. Recovery

Mandatory:
timeout, executor failure, transport interruption, stale claim, worker restart, duplicate controller, replay idempotency, result-publication recovery.

Every required scenario must pass.

## 16. A3

A3 independently verifies:
focused tests, regression, contracts, architecture conformance, security, concurrency, failure, recovery and exact-SHA evidence.

A2 cannot certify itself as A3.

## 17. Pre-soak / 24h soak

PRE_SOAK:
all mandatory paths + recovery + A3 + clean worktree + fresh evidence.

SOAK_24H:
continuous heartbeat, no unexplained restart, no duplicate-claim corruption, no unresolved execution failure, evidence integrity and no authority-boundary violation.

Historical evidence cannot substitute for current evidence.

## 18. Promotion ladder

REGISTERED
→ CREDENTIAL_PRESENT
→ AUTH_SUCCESS
→ MODEL_DISCOVERY_PASS
→ PROBE_PASS
→ EXECUTION_PASS
→ RESULT_VALIDATION_PASS
→ A3_VERIFIED
→ ASTRA_GOLD_ELIGIBLE
→ LAUNCH_READY
→ LAUNCHED

No implicit transition.

## 19. Identity blockers

Colibri and LeonxInx/unlazy currently require exact upstream identity resolution before runtime admission.

A bare github.com reference is not a component identity and cannot enter runtime qualification.

## 20. Launch

G0 Identity
G1 Boundary
G2 Control Plane
G3 Execution Path
G4 23-Wave
G5 Concurrency
G6 Recovery
G7 Integrated A3
G8 Pre-Soak
G9 24h Soak
G10 Launch Ready
G11 Human Launch

G11 is HUMAN_ONLY.

## 21. Absolute invariants

- No credentials in Git.
- No secrets in evidence.
- No provider State Authority.
- No transport State Authority.
- No model executor authority by implication.
- No candidate self-qualification.
- No candidate self-promotion.
- No A2 self-verification.
- No launch without independent A3.
- No launch without recovery.
- No launch without 24h soak.
- Missing/contradictory evidence => BLOCKED.
