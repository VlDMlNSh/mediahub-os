# MediaHub OS — Mature Component Candidate Screen, Wave 01

- Date: 2026-10-15
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **SOURCE-BOUNDED CANDIDATE SCREEN / NOT ADMITTED / NOT IMPLEMENTED / NOT QUALIFIED**
- Scope: initial upstream source review for the new greenfield Jarvis + ASTRA + multi-agent corporation target.
- Owner direction: the new system is designed for new hardware from scratch. Prior server configurations and failed installation attempts are not target facts.
- Safety boundary: repository/document review only. No install, test, model/provider call, credentials, host/runtime inspection, workflow dispatch, deployment, migration, infrastructure change or branch integration.

## 1. Admission rule

A public repository is a candidate, not a selected component. This pass establishes only that the upstream project and its declared purpose are relevant enough for deeper due diligence. It does not establish production maturity for MediaHub, compatibility with target hardware/OS, license approval, secure configuration, correct interfaces, or permission to install.

Before any candidate is admitted, record:
1. immutable upstream commit/tag and release provenance;
2. license and notices for the exact pinned revision;
3. maintenance/release and security-advisory review;
4. dependency/SBOM and supply-chain review;
5. target OS, CPU/architecture, memory, storage and network compatibility;
6. identity, authentication, authorization, isolation and least-privilege model;
7. data-egress/provider behavior, telemetry defaults and secret custody;
8. exact MediaHub interface and contract mapping;
9. failure/retry/cancellation/recovery semantics and observability;
10. owner/governance approval where a decision changes an accepted boundary;
11. independent verification and qualification evidence before release/deployment.

## 2. Candidate screen

| Candidate | Upstream source reviewed | Potential fit | Boundary / risk to resolve | Current disposition |
|---|---|---|---|---|
| LangGraph | https://github.com/langchain-ai/langgraph — README blob `97c31e9cb4d8fe56be8d768ce3eb5e22400e897e` on `main` at review time | Stateful agent graph/orchestration; a possible implementation layer for bounded specialist workflows | Does not itself define MediaHub corporation authority, accepted mission/result schemas, security policy or the ASTRA A0 ingress contract. Pin release and assess persistence/checkpointer, model integrations, tool isolation and recovery. | **SHORTLIST FOR DEEPER REVIEW**; not selected/admitted |
| Temporal Python SDK | https://github.com/temporalio/sdk-python — README blob `81d40696956098ae2ec62695bef46076e41b30ef` on `main` at review time | Durable execution of long-running workflows and activities | Adds a distinct workflow runtime/service and operational footprint; assess whether needed alongside ASTRA lifecycle and avoid duplicate queue/state authority. Evaluate self-hosting/resource costs and deterministic workflow constraints. | **SHORTLIST FOR DEEPER REVIEW**; not selected/admitted |
| Microsoft Agent Framework | https://github.com/microsoft/agent-framework — README blob `c5b3b07d9b5ff8ac327db0d65ba8c1373614a1ac` on `main` at review time | Alternative agent and multi-agent workflow framework, Python/.NET | Overlaps with LangGraph and other orchestration candidates; choose one only after comparative contract, dependency, ecosystem and operational assessment. Do not adopt multiple overlapping frameworks by default. | **ALTERNATIVE CANDIDATE**; not selected/admitted |
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk — README blob `50ea0ed227b72de82917d67d678d1d24783ab2e9` on `main` at review time | Standardized tool/resource/context interfaces between approved clients and bounded tool servers | Protocol conformance is not authorization. Need explicit per-tool capabilities, server identity, input validation, audit, data-egress rules, process isolation and version compatibility. | **SHORTLIST FOR INTERFACE REVIEW**; not selected/admitted |
| Open Policy Agent (OPA) | https://github.com/open-policy-agent/opa — README blob `860399b5b7ac265f89508796831990a45eb485c4` on `main` at review time | Policy decision engine for explicit authorization/admission decisions | Policy engine must not become product state authority; policy input provenance, fail-closed behavior, policy distribution/versioning and enforcement points must be defined. Existing accepted security contracts remain authoritative. | **SHORTLIST FOR POLICY-FIT REVIEW**; not selected/admitted |
| OpenTelemetry Collector | https://github.com/open-telemetry/opentelemetry-collector — README blob `95bb0001d74b1415b0111e72f07ec2e806b80c0b` on `main` at review time | Telemetry pipeline and observability integration | Must review sensitive-data filtering, local retention, export destinations, credentials, resource overhead and disabled-by-default external egress. Telemetry is not qualification evidence unless linked to revision-bound acceptance criteria. | **SHORTLIST FOR OBSERVABILITY REVIEW**; not selected/admitted |
| A2A protocol / SDK ecosystem | Initial official-repository discovery only; full readable upstream source and immutable revision not captured in this pass | Possible bounded federation between MediaHub and an external controller/executor | Protocol selection, version, trust establishment, authentication, task/result lifecycle and compatibility are not established. Do not give an external controller access to ASTRA internal state or canonical product state. | **HOLD — SOURCE PIN AND CONTRACT REVIEW REQUIRED** |

## 3. Preliminary architecture recommendation (proposal only)

Use a **layered, non-duplicative** design rather than selecting an all-in-one framework:
- Jarvis remains the corporation-level mission coordinator under owner-approved DEC-DEV-02.
- ASTRA A0 retains ASTRA-internal engineering lifecycle state under its accepted contract.
- MediaHub Product State Authority remains the only canonical product-state mutation authority.
- Agent orchestration, durable workflow execution, tool interoperability, policy decisions and telemetry are separate capability categories; one product must not silently inherit another category's authority.
- Prefer a small candidate set: one primary agent orchestration runtime, a durable workflow engine only if a documented use case justifies the added service, a bounded tool protocol, a policy enforcement design, and local-first observability.
- This recommendation is not an accepted component decision. Existing source contracts, Baseline 2.0 and owner decisions take precedence.

## 4. Important gaps

- No candidate has been pinned to an immutable upstream commit/tag in this pass; README blob SHAs are evidence of the reviewed README contents, **not** upstream commit SHAs.
- The exact new hardware identifiers, CPU/architecture, memory, storage, GPU/accelerator, operating-system builds and network topology are not present in the reviewed target source set.
- No comparative benchmark, install, test, security audit, compatibility run, qualification or deployment was performed.
- No repository was added as a dependency or vendored into MediaHub.
- A2A requires a fresh source read and versioned contract review before it can be compared fairly with the other candidates.
- Candidate maturity in the upstream ecosystem does not imply suitability or qualification for this target system.

## 5. Next bounded step

Create a source-pinned comparative admission matrix for the top non-overlapping candidates, beginning with LangGraph vs Microsoft Agent Framework for agent orchestration, and MCP for tool boundaries. Add Temporal only as a separate durability decision, not as a default second controller. In parallel, capture the owner-provided target hardware/OS inventory when available. Do not install anything or change runtime state until the admission gates and required authorization are satisfied.

## 6. Evidence references

Reviewed GitHub README blob SHAs:
- LangGraph: `97c31e9cb4d8fe56be8d768ce3eb5e22400e897e`
- Temporal Python SDK: `81d40696956098ae2ec62695bef46076e41b30ef`
- Microsoft Agent Framework: `c5b3b07d9b5ff8ac327db0d65ba8c1373614a1ac`
- MCP Python SDK: `50ea0ed227b72de82917d67d678d1d24783ab2e9`
- OPA: `860399b5b7ac265f89508796831990a45eb485c4`
- OpenTelemetry Collector: `95bb0001d74b1415b0111e72f07ec2e806b80c0b`

These are Git blob SHAs for README files at the review time, not immutable release pins and not qualification evidence.
