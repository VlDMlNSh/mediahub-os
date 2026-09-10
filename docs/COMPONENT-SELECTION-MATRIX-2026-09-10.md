# MediaHub Component Selection Matrix — 2026-09-10

## 1. Governing rule

No significant MediaHub component is started from zero before GitHub prior-art inspection.
For every component: contract -> candidates -> maturity -> maintenance -> license -> security -> tests -> source inspection -> minimal stable block selection.

Selection modes:
USE-AS-IS, BORROW, VENDOR, REIMPLEMENT-MINIMAL, REFERENCE, REJECT.

External projects never become MediaHub authority. MediaHub-native contracts remain authoritative.

## 2. Native MediaHub components already selected

| Native block | Current implementation | Decision | Next boundary |
|---|---|---|---|
| Canonical Protocol | mediahub_canonical_protocol.py | KEEP/NATIVE | capability matrix |
| Capability Matrix | protocol/capability contracts | KEEP/NATIVE | provider adapter |
| Provider Registry | mediahub_provider_registry.py | KEEP/NATIVE | routing authority |
| Resilience | mediahub_resilience.py | KEEP/NATIVE | execution |
| Credential Broker | mediahub_credential_broker.py | KEEP/NATIVE | provider execution |
| Policy Engine | mediahub_policy_engine.py | KEEP/NATIVE | egress |
| Egress Controller | mediahub_egress_controller.py | KEEP/NATIVE | network execution |
| Security Boundary | mediahub_development_security_boundary.py | KEEP/NATIVE | agent/sandbox |
| Provider Adapters | mediahub_provider_adapters.py | KEEP/NATIVE | native execution |
| Native Execution | mediahub_native_execution.py | KEEP/NATIVE | agent launcher |
| Model Registry | mediahub_model_registry.py | KEEP/NATIVE | model qualification |
| Streaming Boundary | mediahub_streaming_boundary.py | KEEP/NATIVE | provider response |
| Native Agent Launcher | mediahub_native_agent_launcher.py | KEEP/NATIVE | Codex/Claude |
| Sandbox lifecycle | cloud_development_sandbox.py | KEEP/NATIVE | hardened runtime |
| Provider Gateway | mediahub_provider_gateway*.py | KEEP/NATIVE | controlled cutover |
| Autonomous control plane | local_autonomous_agent.py + loops | KEEP/NATIVE | orchestration |
| Runtime authority | state_authority.py | KEEP/NATIVE | product state |
| Evidence/provenance | evidence.py + checkpoint docs | KEEP/NATIVE | qualification |

## 3. Provider/gateway prior art

| GitHub project | Decision | Stable block to use | Not to import |
|---|---|---|---|
| OmniRoute | BORROW/REFERENCE | provider-node/registry and fallback ideas | gateway authority |
| Bifrost | BORROW/REFERENCE | provider adapters, cooldown/circuit ideas, routing tests | gateway authority |
| LiteLLM | BORROW/REFERENCE | router strategies, retry semantics, provider matrix tests | enterprise-only code / proxy authority |
| OpenAI Codex | USE-AS-IS via adapter | official CLI execution surface, model selection, sandbox flags | direct Core authority |
| Claude Code | USE-AS-IS via adapter | official CLI print/structured output and model selection | direct Core authority |

Provider implementations remain behind MediaHub canonical protocol, policy, credential and egress boundaries.

## 4. Sandbox and execution prior art

| Project | Decision | Stable block | Status |
|---|---|---|---|
| Daytona | REFERENCE -> candidate backend | lifecycle, resource limits, egress controls, isolated sandbox model | not installed |
| E2B | REFERENCE -> alternative backend | SDK/sandbox lifecycle and execution API concepts | not installed |
| Anthropic sandbox-runtime | REFERENCE/BORROW candidate | local OS-level sandbox boundary patterns | not installed |
| Firecracker | USE-AS-IS/REFERENCE | microVM isolation and lifecycle model | future hardened runtime candidate |
| OpenHands | REFERENCE | agent/backend/sandbox separation | not installed |

Current native sandbox is intentionally filesystem-only. It does not claim kernel/network isolation.

## 5. Policy, identity and tool boundary

| Project | Decision | Stable block | MediaHub use |
|---|---|---|---|
| Open Policy Agent | USE-AS-IS/REFERENCE | declarative policy evaluation | future policy execution backend; native contract remains authority |
| MCP Python SDK | VENDOR/REFERENCE | protocol/client/server/transport lifecycle | Wave 06 tool boundary |
| MCP Swift SDK | VENDOR/REFERENCE | Swift client/server, transports, cancellation | iOS/iPad MCP boundary |
| PydanticAI | REFERENCE/VENDOR | typed model/tool contracts | typed orchestration patterns |

MCP is a transport/tool protocol, not an authority. Every call remains authenticated, authorized, bounded and audited by MediaHub.

## 6. Durable orchestration and recovery

| Project | Decision | Stable block | MediaHub implementation |
|---|---|---|---|
| LangGraph | REFERENCE | durable state graph, checkpoints, retry/interrupt semantics | native durable orchestration in Wave 05 |
| PydanticAI | REFERENCE | typed task/tool/model interfaces | selective patterns only |
| Renovate | USE-AS-IS | dependency discovery and update PR workflow | supply-chain maintenance |

MediaHub will not inherit unrestricted agent permissions from an external orchestrator.

## 7. Observability and evidence

| Project | Decision | Stable block | MediaHub use |
|---|---|---|---|
| OpenTelemetry | USE-AS-IS | vendor-neutral traces/metrics/log pipeline | observability infrastructure |
| Sigstore Cosign | USE-AS-IS | artifact/signature verification | supply-chain gate |
| Gitleaks | USE-AS-IS | secret scanning | security gate |
| Semgrep | USE-AS-IS | structural SAST rules | security gate |
| OSS-Fuzz | REFERENCE/USE-AS-IS where applicable | continuous fuzzing methodology | failure/fuzz qualification |

Security tools supplement MediaHub authority; they do not replace policy or release gates.

## 8. Explicitly rejected architectural shortcuts

- OpenRouter as MediaHub authority: REJECT.
- OmniRoute/Bifrost/LiteLLM as product authority: REJECT.
- Full agent frameworks embedded into Core: REJECT unless separately qualified.
- Full sandbox platform embedded wholesale: REJECT; use backend contract and minimal stable integration.
- Credentials stored in provider registry: REJECT.
- Provider-specific logic in canonical protocol: REJECT.
- Cloud as mandatory product dependency: REJECT.

## 9. Canonical implementation stack

MediaHub Core / State Authority
-> Governance / Policy / Capability
-> Cloud Development Adapter
-> Provider Registry + Model Registry
-> Native Provider Adapter
-> Credential Broker + Egress Controller
-> Native Agent Launcher
-> Sandbox Contract
-> selected sandbox backend
-> bounded execution + streaming
-> audit/provenance/evidence

The selected sandbox backend remains replaceable. Daytona is the leading candidate, but adoption requires a separate license/security/self-hosting qualification gate.

## 10. Wave ordering after component selection

04C: native agent launcher -> Adapter integration -> bounded streaming -> failure injection -> qualification.
05: durable native orchestration using LangGraph as prior-art reference, not authority.
06: MCP + hardened sandbox/provenance boundary; evaluate Daytona/E2B/Firecracker/Anthropic sandbox-runtime.
07: Local Cluster controller and scheduling.
08: real provider E2E only with authorized credentials.
09: supply chain: SBOM, signatures, provenance, dependency/license gates.
10+: iOS/iPad, HIL, upgrade/migration/rollback, final qualification.

## 11. Evidence rule

A selection in this document means selected for architectural use, not installed or production-qualified.
INSTALL/USE/QUALIFIED states must be proven separately with exact commit, test and security evidence.

R4 remains immutable: 471f709f5633feab7aeb62dd3ea52effad6d2bc4 / tree 2279612908135418b2b5448d598274ea6741deaa.
