# MH-10 REVERSE MASTER PROMPT

Date: 2026-09-05
Repository: `VlDMlNSh/mediahub-os`
Branch: `recovery/full-functional-spec`
Status: RECONCILED PROJECTION / NOT ACCEPTED / NOT FROZEN

## 1. MH identifier
MH-10 — AI / INTELLIGENCE ARCHITECTURE.

## 2. Historical scope
AI/intelligence, Local Assistant, controlled cloud escalation, AI content/website generation, knowledge and RAG, agents/orchestration, tools, AI memory, model lifecycle/qualification, AI resource governance, safety, privacy, prompt-injection resistance, observability/audit, AI failure domains, media/knowledge interaction, and AI authority boundaries.

## 3. Source evidence and provenance
Primary canonical control point:
- `recovery/forensic-control-point-2026-09-05.md`
- `recovery/mh01-23-redistribution-projection-matrix-2026-09-05.yaml`
- `specification/capability-registry.yaml`
- `specification/contract-registry.yaml`
- `specification/invariant-registry.yaml`
- `specification/decision-registry.yaml`
- `specification/dependency-graph.yaml`
- `architecture/master-mediahub-architecture-reconstruction-2026-09-05.md`
- `development/implementation-map.yaml`

Historical/current-chat evidence:
- MH-10 Architecture Master Prompt supplied in the MH-10 architecture chat.
- Existing MH-10 architectural baseline established before redistribution, including AI authority boundary, canonical AI flow, agent/RAG/model/security/resource principles.

Provenance rule: historical chat material is evidence; canonical registries and the master control point have higher authority. No chat evidence is silently promoted to canonical registry truth.

## 4. CAP mapping
Primary MH-10 capabilities:
- CAP-020 — `local_ai_assistant` → `assistant_core`
- CAP-025 — `distributed_compute_and_ai_processing` → `cluster_core`
- CAP-026 — `privileged_cloud_development_compute_assistant` → `cloud_development`
- CAP-027 — `trusted_source_content_generation` → `cloud_development`
- CAP-028 — `parameterized_company_website_generation` → `cloud_development`
- CAP-038 — `cross_domain_knowledge_graph` → `knowledge_core`
- CAP-050 — `simulation_verification_acceptance` → `verification`
- CAP-054 — `actionable_contextual_installation_configuration_guidance` → `guidance_core`

Cross-cutting AI dependencies/relationships:
- CAP-031 telemetry
- CAP-032 health/readiness
- CAP-033 diagnostics
- CAP-036 metadata/provenance
- CAP-039 privacy/data governance
- CAP-040 security/trust/authentication/authorization
- CAP-048 resource governance
- CAP-058 security/safety invariant

Anti-loss result: all CAP-001…CAP-058 remain preserved in the canonical registry; MH-10 does not claim ownership of capabilities owned by other domains.

## 5. Requirement mapping
Mapped requirements include:
- intelligence is advisory/bounded and never canonical authority;
- Local Assistant is preferred first path;
- cloud escalation is controlled and privileged;
- AI-generated output is not evidence or canonical state by default;
- agents operate through explicit bounded tools/capabilities;
- RAG context is untrusted content, not instruction authority;
- model lifecycle requires provenance, qualification and rollback/quarantine semantics;
- AI resource use is governed by runtime/resource policy;
- critical operations cannot depend solely on AI;
- AI failures degrade safely to deterministic/manual/runtime mechanisms;
- AI interactions with configuration, policy, plugins, UI and devices preserve existing authority boundaries.

## 6. Contract mapping
Primary contracts:
- CTR-001 state-authority
- CTR-002 consumer-boundary
- CTR-003 identity-authentication-authorization
- CTR-006 device-command
- CTR-018 cloud-development-boundary
- CTR-019 assistant-escalation
- CTR-020 health
- CTR-021 readiness
- CTR-022 diagnostics
- CTR-026 privacy
- CTR-031 guidance
- CTR-033 telemetry
- CTR-034 search-knowledge
- CTR-035 resource-governance
- CTR-036 verification-acceptance

No new canonical contract is created by this projection.

## 7. Invariant mapping
Directly affected/protected invariants:
- INV-001 function preservation
- INV-002 security by design
- INV-005 authentication != authorization
- INV-006 remote access does not increase authorization
- INV-007 ordinary user does not receive Cloud Development access
- INV-008 local-first
- INV-009 offline-first where technically possible
- INV-019 deferred != rejected
- INV-021 security is system-level
- INV-022 health observation-only
- INV-023 readiness operation-scoped
- INV-024 health/readiness/liveness/trust/authorization remain distinct
- INV-025 internal topology hidden from ordinary users
- INV-026 historical evidence preserved
- INV-027 unique canonical function
- INV-029 cloud development cluster distinct from local cluster
- INV-030 surveillance recording does not require separate NVR where MediaHub provides it

AI-specific architectural constraints also preserve the stronger MH-10 rules: AI != authority, confidence != authorization, model output != command, RAG != instruction authority, agent != admin, tool output != trust, and AI cannot bypass Consumer Boundary or State Authority.

## 8. Decision mapping
Accepted decisions materially constraining MH-10:
- DEC-001 functional baseline is primary product truth
- DEC-005 local/offline first
- DEC-006 privileged Cloud Development
- DEC-007 local cluster as one coordinated system
- DEC-008 health/readiness semantics
- DEC-009 security system invariant
- DEC-011 P0-P8 historical decomposition
- DEC-012 deferred detail is preserved

Draft architecture decisions relevant to MH-10:
- DEC-A-001 capability-centric master architecture
- DEC-A-002 explicit authority/security boundaries
- DEC-A-003 separate local/cloud trust/control planes

No draft decision is promoted to accepted by MH-10.

## 9. Architecture/boundary mapping
Canonical projection: `assistant_core`, `knowledge_core`, `cloud_development`, `cluster_core`, `security_core`, `privacy_security`, `resource_governance`, `verification`, with cross-domain relationships to runtime, command, observability, diagnostics, UI and integration layers.

Canonical mutation path:
`AI -> Proposal -> Policy -> Authorization -> Command -> Consumer Boundary -> State Authority -> Canonical State`

Read path:
`Authorized Read Model -> AI -> Analysis/Recommendation`

AI has no direct State Authority mutation path.

## 10. Classification
- RETAIN: AI authority boundary, local-first assistant, controlled cloud escalation, knowledge/RAG separation, bounded agent/tool model, model lifecycle and qualification requirements, safety/privacy/security rules.
- REMAP: historical AI implementation concepts map to `assistant_core`, `knowledge_core`, `cloud_development`, `cluster_core`, `resource_governance`, `verification` and cross-cutting security/privacy/observability ownership.
- RECONCILE: MH-10 versus existing MH-21 distributed AI/security/cloud corpus; exact ownership and non-duplication must be centrally reconciled.
- REPLACE: any historical statement that gives AI direct canonical-state mutation, self-authorization, policy override, unrestricted tool/filesystem/shell access, or ordinary-user Cloud Development access is superseded by the canonical authority hierarchy.
- RETIRE: none authorized by MH-10.
- UNKNOWN: exact production model/provider/hardware/routing/gateway/RAG persistence/tool sandbox/agent isolation and provider-specific controls.

## 11. Contradictions
1. MH-10 and MH-21 overlap in distributed AI/security/cloud scope. This is an ownership/projection reconciliation issue, not a capability-loss event.
2. P0-07 remains implementation/governance incomplete. AI policy/configuration publication cannot be treated as production-authorized.
3. Existing repository AI contracts/schemas do not by themselves prove production qualification of the full MH-10 architecture.

## 12. Missing evidence
- exact target AI hardware and accelerator inventory;
- benchmark and safety qualification evidence for production models;
- exact AI Gateway implementation and security controls;
- provider retention/residency/egress evidence;
- model artifact provenance/signing/digest policy in production;
- tool sandbox and agent isolation implementation evidence;
- RAG ingestion/index/retrieval security evidence;
- AI memory persistence and deletion semantics;
- production incident-response and red-team results;
- complete historical MH-10 corpus beyond the accessible current chat evidence.

## 13. Dangling references
Potentially dangling until central reconciliation:
- MH-10 ↔ MH-21 AI/cloud responsibility boundary;
- AI interactions with MH-11 observability;
- AI persistence versus MH-14 persistence boundary;
- AI security/model supply chain versus MH-12;
- privacy/data processing versus MH-13;
- production qualification versus MH-22.

These are cross-MH references, not missing capabilities.

## 14. Stale references
Any historical implementation-specific provider/model/version claim without current evidence is stale/non-canonical. P0-era decomposition must not be treated as current ownership. No stale claim is promoted.

## 15. Proposed technical decisions
PD-10-001: establish a formal AI/Intelligence Boundary contract under `assistant_core`.
PD-10-002: establish explicit model qualification and provenance gates before production activation.
PD-10-003: establish bounded tool/agent capability contracts with authorization before mutation execution.
PD-10-004: establish controlled local-to-cloud escalation with privacy/data-classification gates.
PD-10-005: establish AI failure-domain/resource isolation from critical runtime.

All five remain PROPOSED / EVIDENCE-BLOCKED and require central governance before canonicalization.

## 16. Contract impacts
Potential updates to CTR-019, CTR-018, CTR-034, CTR-035, CTR-036, and possibly CTR-026/CTR-003/CTR-006. No silent registry changes are authorized.

## 17. Invariant impacts
No existing invariant is proposed for removal. Proposed AI constraints strengthen INV-002, INV-005, INV-007, INV-008, INV-009, INV-021, INV-024, INV-026 and INV-029.

## 18. Dependency impacts
Primary graph dependencies:
`assistant_core -> smart_home_core/media_core/diagnostics/search_core/knowledge_core/cloud_development` and `cluster_core -> resource_governance`, plus security/privacy/observability/verification cross-cutting dependencies. The dependency graph remains authoritative; MH-10 cannot independently rewrite it.

## 19. Verification requirements
Required before production qualification:
- AI authority-boundary contract tests;
- authorization-before-mutation tests;
- prompt-injection and poisoned-RAG tests;
- malicious-tool-output tests;
- data-exfiltration/privacy tests;
- model provenance/integrity/update/rollback tests;
- agent/tool capability escalation tests;
- cloud outage and local fallback tests;
- resource exhaustion/isolation tests;
- critical-operation AI dependency tests;
- hallucination/uncertainty and false-success tests;
- regression and compatibility tests;
- full traceability to CAP/CTR/INV/DEC;
- MH-22 acceptance evidence.

## 20. Acceptance evidence
Current evidence establishes architectural constraints and canonical baseline relationships only. It does NOT establish full production qualification, acceptance or freeze of MH-10.

Acceptance authority: central reconciliation/governance plus explicit human acceptance; MH-10 has no unilateral acceptance authority.

## 21. Remaining OPEN items
All production-specific unknowns above remain OPEN/EVIDENCE-BLOCKED. In particular, exact model/provider choice, AI Gateway, RAG persistence, memory persistence, tool sandbox, agent isolation, hardware qualification and production cloud topology remain unresolved.

## 22. Anti-loss confirmation
CONFIRMED: no CAP is removed, retired or replaced by inference. UNKNOWN/EVIDENCE_GAP is preserved as such. DEFERRED is not rejected. MH-10 projection does not claim ownership over capabilities assigned to other canonical domains.

## 23. Suggested canonical registry changes
1. Consider adding explicit AI authority-boundary semantics to CTR-019.
2. Consider adding model provenance/qualification requirements to CTR-019/CTR-036.
3. Consider adding AI workload isolation semantics to CTR-035.
4. Consider explicit AI/security/privacy cross-references in the canonical dependency graph.
5. Consider a dedicated AI architecture contract only if central reconciliation proves existing contracts insufficient.

Each proposal requires reason, evidence, affected CAP/CTR/INV/DEC, dependency impact, verification impact and acceptance authority. No proposal is applied by this MH chat.

## 24. Explicit authority statement
MH-10 has NO unilateral authority to modify CAP/CTR/INV/DEC registries, canonical ownership, master architecture acceptance state, production authorization, or implementation status.

## 25. Final projection state
MH-10 = ACCOUNTED FOR as a canonical projection with explicit evidence gaps and one material cross-MH reconciliation issue (MH-21 overlap).

Master Architecture remains DRAFT / NOT ACCEPTED.
Production implementation remains BLOCKED.
