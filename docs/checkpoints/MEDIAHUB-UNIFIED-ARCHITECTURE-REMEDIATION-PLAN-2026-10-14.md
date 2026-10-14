# MediaHub OS — Unified Architecture Remediation Plan

- **Date:** 2026-10-14
- **Repository:** `VlDMlNSh/mediahub-os`
- **Status:** `WORKING REMEDIATION REGISTER / NOT ACCEPTED / NOT FROZEN`
- **Purpose:** consolidate currently evidenced duplicates, source conflicts, navigation defects, governance gaps and verification blockers into one prioritized continuation plan.
- **Authority boundary:** this plan is a tracking artifact, not a normative contract, owner decision, implementation authorization, test/qualification result, release, deployment or acceptance.
- **Canonical functional baseline:** [Functional Baseline 2.0](mediahub-functional-baseline-2.0.md) on `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. Baseline 1.0 remains historical provenance; neither baseline is rewritten by this plan.

## 1. Audit boundary and live source identity

### 1.1 Refs observed

- `main` HEAD: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`.
- `docs/mediahub-chat-tree-map-20261012` HEAD at audit start: `0f4be9c11c9f09e1283bd03fd997ad7c0110e706`.
- Comparison: **DIVERGED**, docs branch ahead by 808 commits and behind by 2; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Complete recursive `main` tree at the inspected HEAD: tree SHA `cbb1862fcb4aa22ba24fea4ff12b580ffb305593`, 798 entries, `truncated=false`.
- The scan is a complete path inventory plus targeted source reading and consistency checks. It is **not** a semantic line-by-line audit of all 798 files; runtime behavior, CI outcome and actual service health remain unverified.

### 1.2 Evidence classes

- **CONFIRMED STATIC CONFLICT/DEFECT:** incompatible source text or IDs were directly observed.
- **CONFIRMED DUPLICATE FAMILY / SEMANTIC DIVERGENCE:** multiple paths with the same case-insensitive basename exist and sampled counterparts differ.
- **OPEN GOVERNANCE DECISION:** sources leave authority or acceptance to the owner; no technical guess may close it.
- **UNVERIFIED RISK:** needs a separately authorized test, runtime inspection, qualified review or broader source pass.
- **REPAIRED IN DOCS BRANCH ONLY:** a documentation correction exists on the docs branch but has not been integrated into `main`.

## 2. Consolidated finding register

| ID | Priority | Finding | Evidence / affected sources | Required disposition | State |
|---|---|---|---|---|---|
| MH-ARCH-001 | P0 | **Jarvis/ASTRA lifecycle authority conflict.** ASTRA component scheme on `main` says A0-ASTRA is “single coordination and MediaHub State Authority”; Jarvis ARC-003/018 limits ASTRA to its engineering lifecycle and requires one cross-system lifecycle owner. This wording can be read as granting product-state authority that conflicts with the P0-04 sole canonical mutation boundary. | `main` component scheme SHA `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1`; docs component scheme SHA `d321565a6e0fac1eef329adec67a35ba795b63aa`; [DEC-DEV crosswalk](MEDIAHUB-DEC-DEV-01-08-CROSSWALK-VALIDATION-WAVE-01-2026-10-14.md); owner packet §6.5. | Owner/governance must choose the existing DEC-DEV-02 model A/B/C and approve a typed lifecycle/delegation contract. Do not grant product-state authority to A0. | OPEN_CONFLICT |
| MH-ARCH-002 | P0 | **Concurrency limit 2 vs 3 on `main`.** Component scheme §14 says maximum 2 autonomous claims; launch schema and governance registry say 3, as do prose sources. Existing topology test asserts 3 in selected prose files but does not assert the component-scheme value, so it would not detect this specific conflict. | `main` component scheme SHA `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1`; launch schema `aef6229477ed8ec45e45170f98ea87f7ba75ca29`; governance `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`; topology test `cc5410f631a161b3e3bfb4bae198340f905da6e4`. | Canonical schema is currently named as numeric authority; align `main` through a separately authorized, narrowly scoped change and strengthen drift assertions. The docs branch already removes the duplicated numeric value from the component scheme; do not infer that this resolves `main`. | OPEN / MAIN DRIFT |
| MH-ARCH-003 | P1 | **Authority wording inside governance contract is broader than its field-level authority map.** The purpose says one machine-readable source for gate identity and thresholds, while `authority_source` and `gate_registry.source_of_truth` designate the launch schema and governance holds mirrored threshold values. | Governance SHA `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`; launch schema SHA `aef6229477ed8ec45e45170f98ea87f7ba75ca29`; owner packet §7.1. | Owner/governance selects and documents field-level ownership. Current recommendation recorded in the owner packet is schema-authoritative numeric values with governance registry/mirror and fail-closed drift checks; it is not an accepted decision yet. | OWNER/GOVERNANCE |
| MH-ARCH-004 | P1 | **Design readiness can be mistaken for live qualification.** Unified YAML says `status: QUALIFICATION_READY_HYBRID_FABRIC` while generated Current Truth says all G0–G11 BLOCKED and overall `NOT_PROVEN / BLOCKED`. Model version 1.1 and paired Markdown version 1.0 also need explicit lineage semantics. | Unified YAML `adc852009c3a79d0e64265a3af8a4910a1388057`; Current Truth `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`; [wave 06 audit](MEDIAHUB-PROJECT-WIDE-ARCHITECTURE-INTEGRITY-WAVE-06-2026-10-14.md). | Approve a governed interpretation or versioned status-schema change that separates design maturity from runtime qualification. Until then, Current Truth is the live gate source; no design label promotes a gate. | OPEN |
| MH-ARCH-005 | P1 | **MH-03 document-family duplication with divergent contents.** Eighteen same-basename pairs exist between `architecture/MH-03-*.md` and `docs/architecture/mh-03/MH-03-*.md`; all 18 root/nested blob-SHA pairs differ. Four pairs have already been compared as text, and the contradiction-register pair has a direct status conflict: root `C03-08` requires governance review for the proposed HA path, while the nested copy says no current explicit contradictions are identified. `architecture/MH-03-index.md` (blob `b2d2eeb1b89117d10605c231e79378eebc437c5f`) lists the root-level artifacts as required, but remains PROPOSED; the nested directory has no `MH-03-index.md`. | Full 18-pair source/SHA table in Wave 09 below; examples: root contradiction register `5879ad2ab19110ae7418f881cbd7603a10ff996e` vs nested `7986b072983f1d6f828b7214f4896b91c91392f2`; root runtime foundation `325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2` vs nested `2457451017daa0f91e9e978e44c91e1e49d0d7a3`; lifecycle `300363a06fe678d3511c2a4b843678bf200df5f0` vs `41baa81406dcd25b8b1537adf9c8b1289c38edcd`; acceptance `e96adaac2eb52e2f8058cc889485ec982bf606e5` vs `eefb645d89c7c3046636d8344515aa02b7ccebe3`. | Preserve both trees and provenance. Confirm the active MH-03 source location and intended role of nested files; then reconcile each of the 18 pairs through a narrow reviewed change or explicitly label the copies as historical/derived. Root index is evidence of intended layout, not an accepted/frozen decision. Do not delete files before checking inbound references and ID lineage. | CONFIRMED DIVERGENT FAMILY; OWNER/GOVERNANCE ROUTE OPEN |
| MH-ARCH-006 | P0 | **P0-07 trusted-context and mutation/publication path remains unproven.** Existing evidence does not demonstrate an accepted trusted issuer/provisioner lifecycle or end-to-end P0-07 → P0-05 → P0-04 request/context/resource/revision binding. D1 is NOT DEMONSTRATED; D2 NOT EVIDENCED; D3/D4/D5 remain evidence-gated; D6 is open; D7 change-control ownership remains open. | [D2 proposal](P0-07-D2-TRUSTED-CONTEXT-AUTHORITY-LIFECYCLE-PROPOSAL-2026-10-13.md), SHA `39400abce88da7ea54be7d9d7505f215eba43408`; [traceability matrix](mediahub-unified-system-traceability-matrix-v0.1.md), SHA `43e495aae6b4dc55a0d2e07fa4723d364898a5c1`; owner register. | Continue source tracing only where it can prove an existing path. Otherwise route the proposal to governance. Keep P0-07 mutation/publication blocked and P0-05 v1.1 NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN. | BLOCKED |
| MH-ARCH-007 | P0 | **Qualified independent P0-07 D2 review is absent.** R-01…R-06 worksheet in the D2 proposal is blank; an internal desk review and source routing are not an independent review. | D2 proposal §13, SHA `39400abce88da7ea54be7d9d7505f215eba43408`; [crosswalk wave 01](MEDIAHUB-DEC-DEV-01-08-CROSSWALK-VALIDATION-WAVE-01-2026-10-14.md). | Owner/governance appoints a qualified independent reviewer or defers. Record competence, independence/conflicts, exact proposal/source SHAs, itemized R-01…R-06 dispositions and attributable sign-off. | WAITING OWNER / REVIEWER |
| MH-ARCH-008 | P0 | **Contour A → Contour B acceptance gate is not closed.** Contour B product work remains prohibited until Contour A is deployed, independently qualified and explicitly accepted with traceable evidence. | Master roadmap §5 and DEC-DEV-08; owner packet; current qualification truth. | Preserve the hard gate. No product implementation in Contour B until required Contour A deployment and independent acceptance evidence exist. | BLOCKING |
| MH-ARCH-009 | P1 | **Traceability and placement artifacts remain proposals.** Unified traceability matrix and node/service placement register are marked PROPOSED / NOT ACCEPTED / NOT FROZEN; they cannot be used as accepted implementation contracts. | Traceability matrix SHA `43e495aae6b4dc55a0d2e07fa4723d364898a5c1`; placement register SHA `59107fd6d7b8a73d671098adcf2824c310642907`. | Resolve prerequisite owner decisions and primary-source conflicts; submit bounded documents for domain-owner/governance acceptance and freeze before using them as implementation authority. | OPEN |
| MH-ARCH-010 | P1 | **Cross-branch drift is material.** Docs branch is 808 commits ahead and 2 behind `main`; there are source wording differences and branch-only corrections. A broad merge/rebase/cherry-pick would combine a large, diverged history and is not justified by this audit. | Live compare: `main` `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; docs branch `0f4be9c11c9f09e1283bd03fd997ad7c0110e706`; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. | Do not integrate branches as a shortcut. Use a file-level change-control queue with exact base SHA, owner/source approval, narrow diff, review and post-write readback for each authorized main change. | DIVERGED / NO INTEGRATION |
| MH-ARCH-011 | P1 | **Project map and continuation artifacts are large and append-heavy.** Map ≈686 KB, checkpoint ≈274 KB and traceability matrix ≈303 KB. They provide extensive provenance but increase retrieval cost and make duplicated/obsolete conclusions harder to notice. | Live docs-branch files; map SHA `128747b623e9ca34f36796b1aa2923ab0a533895`; checkpoint SHA `b41c1019df4c106c1000865f6d0c00eec559a0d7`; traceability SHA `43e495aae6b4dc55a0d2e07fa4723d364898a5c1`. | Preserve historical entries; do not truncate history. Add a short current-state index and a single prioritized remediation register (this document), then link old wave reports rather than repeating full conclusions. Consider archival/indexing only under approved documentation policy. | MAINTAINABILITY RISK |
| MH-ARCH-012 | P2 | **Repeated basenames require classification, not blanket deletion.** The refreshed docs-branch inventory contains 24 distinct case-insensitive basename-collision groups, representing 44 path occurrences beyond the first path for each basename. These groups include 18 MH-03 pairs; expected conventions (`README.md`, `SKILL.md`, `__init__.py`); and three non-MH-03 pairs requiring classification. The exact count supersedes the earlier estimate of 37; this count does not mean 24 semantic defects. No case-only collision of complete repository paths was found. | Current tree: docs ref `6326b659d62177585e8a58f49e52f8546fdd242e`, 904 entries / 827 blobs, `truncated=false`; main tree `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`, 798 entries / 721 blobs. Same-basename examples: mesh capability schema `d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c` vs domain capability schema `fe80659b570ac58829f10410feb5c700388f87c0`; launch-agent plist `2cca029b502fd911ec38272871c823a8717ed8fd` vs `d1d8aea99c2303c26e542a3d1c5e54b4596521d0`; mesh state model `d02780894cfb5d3c0fc7878d57a08fac2e428efc` vs runtime StateAuthority interface `a2115b81f52a63feb357e484bd982a6a32641d81`. | Maintain a per-group classification: expected package/document convention, intentionally distinct schema, distinct Python responsibility, potentially co-installable deployment manifests, or divergent copy. Do not rename/delete by basename alone. The `capability.schema.json` pair has distinct `$id` and object semantics; the `state.py` pair serves different purposes. | INVENTORY CONFIRMED; CLASSIFICATION PARTIAL |
| MH-ARCH-013 | P1 | **Qualification status remains blocked; required rounds are criteria, not evidence.** Current Truth has G0–G11 BLOCKED and overall NOT_PROVEN / BLOCKED. The 23-round-per-path, 115-round aggregate and 24-hour soak requirements do not prove those activities occurred or passed. | [Current Truth](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/qualification/CURRENT-TRUTH.generated.md), SHA `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`; launch schema; qualification blueprint. | Preserve fail-closed status. Only authorized, fresh, immutable evidence and the required independent A3/human gates can change qualification status. | NOT_PROVEN / BLOCKED |
| MH-ARCH-014 | P2 | **Broad static integrity does not prove CI/test health or runtime behavior.** Existing governance invariant enforcement references were path-checked; tests, workflows, credentials, services and host state were not exercised in this pass. | Wave 06 audit and live repository tree. | After explicit authorization, plan a separate read-only/test qualification wave with scope, commands, target SHA, expected outputs, evidence storage and rollback boundaries. Until then, do not claim tests pass or the runtime is healthy. | UNVERIFIED |
| MH-ARCH-024 | P1 | **MH-03 lifecycle/acceptance mirror coverage diverges.** Root and nested lifecycle documents have different transition/failure detail; root acceptance criteria list explicit acceptance conditions, while nested criteria add a fuller gate set and evidence/decision-register review. Both copies remain PROPOSED/NOT ACCEPTED. This confirms coverage asymmetry, not by itself an incompatible invariant. | Root lifecycle `architecture/MH-03-lifecycle.md` SHA `300363a06fe678d3511c2a4b843678bf200df5f0`; nested lifecycle `docs/architecture/mh-03/MH-03-lifecycle.md` SHA `41baa81406dcd25b8b1537adf9c8b1289c38edcd`; root acceptance `architecture/MH-03-acceptance-criteria.md` SHA `e96adaac2eb52e2f8058cc889485ec982bf606e5`; nested acceptance `docs/architecture/mh-03/MH-03-acceptance-criteria.md` SHA `eefb645d89c7c3046636d8344515aa02b7ccebe3`; root index `architecture/MH-03-index.md` SHA `b2d2eeb1b89117d10605c231e79378eebc437c5f` is PROPOSED and no nested index exists. | Preserve both trees. Compare remaining clause-level behavior and dependencies; after owner/governance selects root, nested, or governed synchronized views, reconcile with source anchors and inbound-reference/ID checks. Do not promote acceptance status from either copy. | CONFIRMED ASYMMETRIC COVERAGE; AUTHORITY OPEN |
| MH-ARCH-025 | P1 | **MH-03 command-execution root/nested pair has asymmetric mutation-path coverage.** Both copies preserve commands-as-requests, deny missing authorization, reject malformed/stale commands, forbid direct UI/AI/plugin/device/cloud mutation, and retain sole State Authority. The root flow says `Command → Validation → Authorization/Policy → Consumer Contract → State Authority → Canonical Mutation → Event → Observers`; the nested flow explicitly adds `Input → Integration/Capability Boundary`, calls the P0-05 Consumer Boundary by name, and requires explicit context/bounded inputs. Root explicitly forbids private authoritative state; nested explicitly forbids event/telemetry as implicit command. No direct semantic contradiction was established, but the missing/implicit steps in the root flow matter for authority-boundary readability. | Root `architecture/MH-03-command-execution.md` SHA `b9197759e70107f1be5968e8669288d991360003`; nested `docs/architecture/mh-03/MH-03-command-execution.md` SHA `8a9e1066f00cf9a7a3128c00eada857b18cef32f`; root index `architecture/MH-03-index.md` SHA `b2d2eeb1b89117d10605c231e79378eebc437c5f`. All are PROPOSED context; the root index is not accepted canonical authority. | Preserve both versions. After owner/governance chooses root canonical, nested canonical or synchronized views, create a clause-level crosswalk. Ensure the canonical contract explicitly locates input/capability boundaries and P0-05 without weakening existing fail-closed, stale-transaction or single-State-Authority invariants. No source file changed in this pass. | CONFIRMED ASYMMETRIC COVERAGE; DIRECT CONTRADICTION NOT PROVEN |
| MH-ARCH-026 | P1 | **MH-03 evidence-register pair contains an acceptance/provenance status conflict.** The root register marks E03-01…E03-04 FROZEN / INHERITED within a PROPOSED register; nested register marks E03-01 ACCEPTED / IMPLEMENTATION AUTHORIZED and E03-02…E03-04 ACCEPTED / FROZEN. The evidence IDs do not carry equivalent source/status descriptions across the two files. | Root evidence register `architecture/MH-03-evidence-register.md` SHA `07dd464fe23ba91943053f658c8d804ec67b5fb6`; nested `docs/architecture/mh-03/MH-03-evidence-register.md` SHA `865a1bda46984cd8b3384aaea99ec9f9c86746d4`; root index remains PROPOSED. | Preserve both files until the owner/governance authority selects root canonical, nested canonical or governed synchronized views; reconcile each evidence ID, provenance and acceptance status before citing either register as an accepted authority. Do not infer real-world implementation authorization from the nested label. | CONFIRMED EVIDENCE/STATUS/PROVENANCE CONFLICT; OWNER DISPOSITION REQUIRED |
| MH-ARCH-027 | P2 | **MH-03 degraded-mode mirror pair has asymmetric transition/definition coverage.** Both copies preserve fail-safe local/deterministic operation where capability permits, isolation of optional failures, no mutation fallback on State Authority failure, and no weakening of authorization/trust. The nested copy explicitly defines DEGRADED as a known subset of unavailable/impaired capabilities and enumerates READY→DEGRADED, DEGRADED→RECOVERING, RECOVERING→READY/DEGRADED; the root copy specifies that recovery returns to READY only after health/dependency checks pass but does not enumerate the failed-recovery transition. This is coverage asymmetry, not a demonstrated logical contradiction. | Root `architecture/MH-03-degraded-mode.md` SHA `f724cedc52f7421c520c1183fa8e8e078fe93082`; nested `docs/architecture/mh-03/MH-03-degraded-mode.md` SHA `7b70229049b80a230b201806aab59f394e0d33bd`; root index `architecture/MH-03-index.md` SHA `b2d2eeb1b89117d10605c231e79378eebc437c5f` is PROPOSED. | Keep both sources unchanged while the canonical-tree choice is unresolved. After selection, make the transition/failure model complete and bidirectionally traceable without changing fail-closed or sole-State-Authority invariants. | CONFIRMED ASYMMETRIC COVERAGE; DIRECT CONTRADICTION NOT PROVEN |
| MH-ARCH-028 | P2 | **MH-03 error-handling mirror pair has complementary but asymmetric failure/sanitization requirements.** The root copy classifies supervised restart/isolation and states that errors must be observable without making telemetry authoritative and that recovery stays inside the authority model. The nested copy requires stable/bounded/sanitized errors, prohibits exposing credentials/secrets/private material/unnecessary internal paths, and forbids partial lifecycle transitions/canonical-state corruption. Both preserve reject/deny/fail-closed behavior and no fallback authority; no direct contradiction was found. | Root `architecture/MH-03-error-handling.md` SHA `bd2157deb94c2823c6b6fac2988945b7bc412ef3`; nested `docs/architecture/mh-03/MH-03-error-handling.md` SHA `a33051aabb24447cf993755e84569917fe37f037`; root index SHA `b2d2eeb1b89117d10605c231e79378eebc437c5f`. | Preserve both sources; after owner/governance selects canonical source or synchronized-view policy, crosswalk error classes, sanitization, observable diagnostics, restart/isolation, partial-transition and recovery behavior. Do not infer acceptance from either copy. | CONFIRMED ASYMMETRIC COVERAGE; DIRECT CONTRADICTION NOT PROVEN |
| MH-ARCH-030 | P2 | **MH-03 health-model mirror pair has asymmetric state and privacy/readiness detail.** Both sources treat health as observational rather than canonical authority and distinguish liveness/readiness/dependency health. The nested source defines STARTING/READY/DEGRADED/RECOVERING/STOPPING/STOPPED, fail-closed readiness for missing critical foundation, optional-dependency degradation, and prohibition on exposing mutable internal objects or sensitive data; the root source adds authority/lifecycle health dimensions but does not enumerate those states or privacy constraints. No direct contradiction established. | Root `architecture/MH-03-health-model.md` SHA `a4b9e8838d6b88ea629b9ee3642b6bcc791cba47`; nested `docs/architecture/mh-03/MH-03-health-model.md` SHA `2f5840218dfdc0103e16721ebf467150d19cb216`; root index `architecture/MH-03-index.md` SHA `b2d2eeb1b89117d10605c231e79378eebc437c5f` is PROPOSED. | Preserve both sources pending owner/governance choice of root canonical, nested canonical or governed synchronized views. Then crosswalk health dimensions/states, critical-vs-optional dependency behavior, readiness semantics, sensitive-data exposure and authority non-mutation constraints. Do not infer acceptance from either copy. | CONFIRMED ASYMMETRIC COVERAGE; DIRECT CONTRADICTION NOT PROVEN |
| MH-ARCH-029 | P2 — repaired in docs branch | **Master roadmap contained duplicate top-level numeric section IDs.** The historical `## 8. Current blockers and explicit non-claims` collided with the P0-07 addendum; two `## 28. Execution update` sections separately covered command-execution and evidence-register reviews. | Pre-repair blob `31cfe03f94f8f61c0c3e144e3e78c28ee0d2a08`; repaired roadmap blob `a84e04b2ecebb5b66c2ca7b3843bcdd08113672b`. | Preserve all historical content; P0-07 addendum is now nested as `### 10.5`, evidence-register update is `## 29`, plan-navigation repair is `## 30`, and health-model update is `## 31`. Post-write numeric-heading scan and read-back required. | PATCH APPLIED / HEADING SCAN PENDING |
| MH-ARCH-016 | P1 | **Functional Baseline 1.0 authority/version conflict across branches.** The same path has materially different documents: `main` blob `9df4892ed0734050ac79732603d15bb414717310` is a 68-section historical edition 1.0 passport; the docs branch blob `1a2f06f50dd69990be58b12a98376b92f12fd14f` is a much shorter document declaring itself `NORMATIVE / SINGLE SOURCE OF TRUTH`. Accepted Functional Baseline 2.0 explicitly supersedes Baseline 1.0 as current functional reference. | `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` on both refs; `docs/checkpoints/mediahub-functional-baseline-2.0.md` on `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. | Do not rewrite or delete either branch's baseline in this pass. Preserve Baseline 2.0 as canonical; obtain provenance/owner disposition for the docs-branch rewrite, then label the branch copy as historical/superseded or restore a traceable historical artifact through a separately authorized narrow change. Check inbound links and historical IDs before any consolidation. | CONFIRMED CROSS-BRANCH AUTHORITY CONFLICT |
| MH-ARCH-044 | P2 | **MH-03 service-boundary mirror pair has asymmetric explicitness around lifecycle state, capability grants, P0-05/P0-04 and recovery policy.** Both copies deny runtime canonical mutation and preserve the governed command path; nested text explicitly names P0-05/P0-04, forbids self-granted capabilities and scopes recovery to policy-approved actions, while root uses a tabular role/authority matrix and explicitly says logical boundaries do not imply separate processes/containers/technologies. | Root `architecture/MH-03-service-boundaries.md` SHA `02672aa1c377d04a3a7e0a7cff5b767a89ee0fcb`; nested `docs/architecture/mh-03/MH-03-service-boundaries.md` SHA `cb9e5800d20ab3ee463bc30446419c95d556a87c`; root index SHA `b2d2eeb1b89117d10605c231e79378eebc437c5f` is PROPOSED. | Preserve both. Once owner/governance selects root canonical, nested canonical or governed synchronized views, crosswalk each service role against explicit authority restrictions, lifecycle/capability semantics, P0-05/P0-04 path, recovery policy and deployment-topology neutrality. Do not infer acceptance or require separate processes from logical boundaries alone. | CONFIRMED ASYMMETRIC EXPLICITNESS; DIRECT CONTRADICTION NOT PROVEN |
| MH-ARCH-045 | P1 | **Explicit LOCAL_ONLY route policy is absent from the inspected AstraGateway request path; applicability to the specific accepted client route remains unresolved.** `AstraTaskRequest` has no route-mode field; `AstraGatewayRuntime.run` calls the orchestrator without a route-policy argument; candidate construction starts with cloud routes and optionally appends local routes. `allow_local_extension=false` is not LOCAL_ONLY because it removes local candidates rather than cloud candidates. The accepted distributed-infrastructure target requires LOCAL_ONLY to fail closed with no silent cloud fallback on the specified development path. This is a potential privacy/egress design risk, not evidence of production leakage; actual use is unknown. | `runtime/mediahub_runtime/astra_gateway.py` SHA `10985e4ad8f682313d08e7492ecc1856a8bce20f`; `runtime/mediahub_runtime/cloud_orchestrator.py` SHA `24c28197df7baca49abd81956752a7a5092506d9`; `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` SHA `e549692f207fbc91d9b9b9b92b8e665404f07290`. | Trace the exact client/gateway scope and govern a trusted, auditable route-mode/data-class/provider policy. If this path serves LOCAL_ONLY work, the candidate set must contain no cloud providers and local unavailability must fail closed; CLOUD_ALLOWED failover must stay within that task's admitted provider set. Do not patch runtime or claim production impact until design/change authorization and later verification. | ROUTE MODE ABSENT IN INSPECTED PATH; TARGET-SCOPE / RUNTIME UNKNOWN |
| MH-ARCH-046 | P1 | **Ollama selected model can diverge from the actual executor model and reported provenance.** `OllamaExecutor` sends its hard-coded class model `qwen2.5-coder:3b`; the orchestrator's Ollama route reports the `MEDIAHUB_OLLAMA_MODEL(S)` selection but returns a preconstructed executor without binding that model. With no route model configured, evidence can report `unspecified` while the executor sends the hard-coded model. | `runtime/mediahub_runtime/astra_gateway.py` SHA `10985e4ad8f682313d08e7492ecc1856a8bce20f`; `runtime/mediahub_runtime/cloud_orchestrator.py` SHA `24c28197df7baca49abd81956752a7a5092506d9`; targeted test file `tests/ai/test_cloud_orchestrator_failover.py` SHA `c66b63b158c545ae627c596791381b83ef902c59` covers other route/failover cases but was not run and contains no explicit Ollama selected-vs-actual identity assertion in the inspected content. | Bind one resolved model identity to route decision, actual executor request, qualification evidence and emitted result/event metadata. Add focused default/configured/mismatch-negative tests only after separate test authorization. Do not claim live impact until execution evidence exists. | CONFIRMED STATIC IDENTITY/PROVENANCE MISMATCH; RUNTIME IMPACT NOT VERIFIED |


## 3. Previously repaired documentation defects

These are recorded as repaired only on the documentation branch; they are not global closure:

1. **Map navigation collisions:** seven duplicate numbered section IDs were repaired by preserving first occurrences, assigning unique IDs to later headings and fixing a self-reference. Verified map SHA: `128747b623e9ca34f36796b1aa2923ab0a533895`; the wave-06 report records the collision table and post-write checks.
2. **ASTRA component-scheme duplicated numeric threshold:** docs branch now refers to `runtime_thresholds.max_parallel_autonomous_claims` and its schema authority instead of duplicating the numeric value. Current docs component scheme SHA: `d321565a6e0fac1eef329adec67a35ba795b63aa`. `main` still contains the old value 2.
3. **Administrative questions:** the existing owner decision packet contains ADMIN-01…ADMIN-04 with options and recommendations. They are proposals, not owner decisions.

## 4. Prioritized development sequence

### Wave 0 — Establish the controlled decision queue (P0, documentary)

- Use this plan as the single prioritized cross-cutting register; retain prior reports as evidence sources, not competing master plans.
- Refresh source refs/SHA immediately before every subsequent change.
- Preserve the canonical Baseline 2.0, the Contour A/B boundary, historical IDs and fail-closed status.
- Do not integrate branches; no merge/rebase/cherry-pick is part of this wave.

**Exit:** every P0/P1 issue has one owner/authority, exact source anchors, an explicit state and a next evidence/decision action.

### Wave 1 — Owner/governance decisions (P0)

1. **ADMIN-01 / MH-ARCH-001:** select DEC-DEV-02 A/B/C lifecycle ownership model. Recommendation in existing owner packet: C as safe interim boundary unless a single delegated lifecycle can be proven and accepted.
2. **ADMIN-02 / MH-ARCH-007:** appoint a qualified independent P0-07 D2 reviewer or explicitly defer; no review is fabricated.
3. **ADMIN-03 / MH-ARCH-004:** choose a governed meaning/versioning model for design readiness vs runtime truth.
4. **ADMIN-04 / MH-ARCH-010:** choose a controlled source-change route for main/docs wording, without authorizing broad branch integration.
5. **ADMIN-05 / MH-ARCH-003:** confirm field-level source-of-truth ownership for numeric thresholds; current recommendation is launch schema as numeric authority, governance as registry/mirror with fail-closed drift checking.

**Exit:** attributable owner/governance decisions exist for the questions that are actually ripe; no recommendation is silently promoted.

### Wave 2 — P0-07 / P0-05 / P0-04 trust and change-control chain (P0)

- Trace existing caller → authenticated principal → trusted context issuer/lifecycle → operation/scope → P0-04 canonical mutation → revision/evidence path.
- Separate D1, D2, D3, D4, D5, D6 and D7 closure criteria; do not collapse them into one generic “security passed”.
- Obtain the independent D2 R-01…R-06 review and separate owner/governance disposition.
- Resolve the D6 normative-text status only with exact acceptance evidence; do not edit a DRAFT header by inference.
- Preserve P0-07 mutation/publication BLOCKED until accepted contract/API and evidence close the gap.

**Exit:** exact end-to-end source/evidence binding and governed contracts; otherwise explicit BLOCKED with remaining unknowns.

### Wave 3 — Canonical ASTRA contract and cross-branch repair (P1)

- Reconcile concurrency wording in `main` against the current launch-schema authority and add assertions that include the component scheme.
- Resolve the governance contract purpose/authority-source wording and equality checks.
- Separate design maturity and live qualification status; document model version lineage.
- Reconcile A0 scope only after DEC-DEV-02 governance disposition.
- Submit narrow, source-reviewed changes through the authorized route; reread all changed files and record resulting blob/commit SHAs.

**Exit:** one machine-readable authority per field, no contradictory normative prose, and no false runtime-ready label.

### Wave 4 — Duplicate document families and link/ID integrity (P1/P2)

- Compare all 18 MH-03 basename pairs; document per-file authority, provenance, status, consumers and required synchronization.
- Classify the 24 basename-collision groups / 44 extra path occurrences recorded in Wave 09 as expected package layout, separate artifacts, historical copies or defects; do not equate same basename with duplicate content.
- Continue Markdown relative-link/path and section-ID scans across the map-selected architecture/checkpoint sources.
- Preserve old IDs and use redirects/provenance notes where consolidation is approved.

**Exit:** duplicate-family inventory with an explicit disposition for every pair and no unresolved ambiguous canonical references in the scoped set.

### Wave 5 — Evidence-backed qualification and acceptance (P0; authorization required)

- Only after explicit permission, define a bounded test/qualification plan; do not run it merely because this plan lists it.
- Verify governance invariant tests, schema/drift checks, relevant workflow contracts and evidence freshness on an exact target SHA.
- Preserve separate statuses for design, implementation, tests, verification, qualification, release, deployment and acceptance.
- Contour B remains blocked until Contour A deployment, independent qualification and explicit acceptance are evidenced.

**Exit:** all required gates have fresh, attributable PASS evidence and human authorization; otherwise remain NOT_PROVEN / BLOCKED.

## 5. Administrative decision block

Reply with the existing ID and option letter. The recommendation is not adopted unless the owner explicitly selects it. These questions consolidate the existing owner packet; they do not create new normative decision IDs.

### ADMIN-01 — DEC-DEV-02 lifecycle authority
- **A:** Jarvis owns the cross-system engineering task lifecycle; ASTRA is a bounded execution/qualification adapter.
- **B:** ASTRA owns a bounded lifecycle explicitly delegated by Jarvis through an accepted typed contract, scope, revocation and fencing semantics.
- **C (safe interim recommendation):** strictly disjoint Jarvis/ASTRA lifecycle domains until a reviewed delegation contract exists.
- **No response:** keep OPEN_CONFLICT; no authority expansion or implementation.

### ADMIN-02 — P0-07 D2 independent review
- **A (recommended):** appoint a qualified independent reviewer and record competence, independence/conflicts, exact proposal/source SHAs, R-01…R-06 dispositions and attributable sign-off.
- **B:** defer; D2 stays NOT EVIDENCED and mutation/publication stays BLOCKED.
- **No response:** same fail-closed state.

### ADMIN-03 — ASTRA design-status semantics
- **A (recommended):** retain the current enum only as design/model readiness; Current Truth alone reports live runtime gate state.
- **B:** approve a versioned schema/model change to explicitly separate design maturity and runtime qualification, including consumer updates.
- **C:** defer changes; treat runtime qualification as NOT_PROVEN / BLOCKED.
- **No response:** no status promotion.

### ADMIN-04 — main/docs source correction route
- **A (recommended):** authorize a minimal file-level change request for specifically approved wording only, with before/after SHA and review; no broad branch integration.
- **B:** require architecture review/rewording before proposing a source change.
- **C:** defer and preserve the drift as open.
- **No response:** no main changes, merge, rebase or cherry-pick.

### ADMIN-05 — numeric threshold authority
- **A (recommended):** launch schema is the numeric authority; governance contract is the registry/mirror, with equality checks and fail-closed drift handling.
- **B:** governance contract becomes the sole numeric authority; revise schema authority fields and consumers under controlled governance.
- **C:** keep both files but define field-level ownership and require mismatch to block qualification.
- **No response:** current explicit schema authority remains the working interpretation, but no disputed value is silently changed.

### Decisions deliberately not re-asked
- P0-05 D6 remains defer/request evidence; do not infer normative acceptance from implementation-tree acceptance.
- Existing P0-05 D1–D7 owner directions remain in force.
- DEC-DEV-01 and DEC-DEV-03/04/05/06/07 retain their recorded evidence prerequisites.
- DEC-DEV-08 is a binding Contour A → Contour B gate, not a discretionary bypass.
- Baseline 2.0 remains accepted/canonical/immutable; Baseline 1.0 remains historical.

## 6. Linked evidence register

- [Project-wide architecture integrity sweep wave 06](MEDIAHUB-PROJECT-WIDE-ARCHITECTURE-INTEGRITY-WAVE-06-2026-10-14.md) — map IDs, tree coverage, ASTRA contracts, admin questions.
- [ASTRA source-of-truth reconciliation wave 05](MEDIAHUB-ASTRA-SOURCE-OF-TRUTH-RECONCILIATION-WAVE-05-2026-10-14.md) — threshold authority wording and prior correction.
- [ASTRA cross-branch source-drift wave 04](MEDIAHUB-ASTRA-CROSS-BRANCH-SOURCE-DRIFT-WAVE-04-2026-10-14.md) — main/docs A0 and concurrency drift.
- [DEC-DEV-01…08 crosswalk validation wave 01](MEDIAHUB-DEC-DEV-01-08-CROSSWALK-VALIDATION-WAVE-01-2026-10-14.md) — placement/lifecycle authority findings.
- [P0-07 D2 trusted-context authority/lifecycle proposal](P0-07-D2-TRUSTED-CONTEXT-AUTHORITY-LIFECYCLE-PROPOSAL-2026-10-13.md) — review proposal and blank independent-review worksheet.
- [Owner decision packet 01](MEDIAHUB-OWNER-DECISION-PACKET-01.md) — existing decision options and recommendations.
- [Unified system traceability matrix](mediahub-unified-system-traceability-matrix-v0.1.md) — cross-contract evidence links; proposed/not accepted/not frozen.
- [Node/service placement and decision register](MEDIAHUB-NODE-SERVICE-PLACEMENT-AND-DECISION-REGISTER-01.md) — placement and DEC-DEV prerequisites.

## 7. Guardrails and closure semantics

- A finding is closed only by exact source evidence, authorized change or attributable owner/governance decision appropriate to that finding, followed by readback verification.
- Documentation cleanup is not implementation. Static source inspection is not a test. A blank worksheet is not an independent review. A workflow definition is not a successful workflow run.
- No tests, qualification, host/runtime inspection, credentials, model/provider calls, installation, infrastructure change, deployment, migration, merge, rebase or cherry-pick were performed as part of this plan.
- No main-branch normative file was changed.
- **Current overall status remains: architecture globally NOT ACCEPTED / qualification NOT_PROVEN / BLOCKED.**

## 8. Wave 07 addendum — test-contract alignment (2026-10-14)

This pass read back the current docs-branch topology/drift tests and paired ASTRA model. It was static inspection only; no test runner was invoked.

### Additional confirmed finding

| ID | Priority | Finding | Evidence | Required disposition | State |
|---|---|---|---|---|---|
| MH-ARCH-015 | P0 | **A drift test hard-codes the disputed A0 state-authority claim.** `tests/test_astra_gold_architecture_drift.py` asserts `qualification.authority.state_authority == "A0-ASTRA"` and `unified.authority.astra.role == "single_coordination_authority"` (test blob `d6a0e6a6d81dc6e15e343cd80ee950431b1e3b14`). Those assertions encode the same disputed interpretation identified in MH-ARCH-001 rather than checking a settled, owner-approved boundary. A green result from this test could not establish that the lifecycle/product-state authority conflict is resolved. | Paired model YAML blob `193f81eb3cf463ebc38c6b2c3fca8c19e502f176`; component-scheme conflict and owner packet refs listed in MH-ARCH-001. | After owner disposition of DEC-DEV-02, update the contract and test assertions together. Before that decision, do not change the normative value by inference; make the unresolved authority boundary explicit and keep the associated acceptance gate blocked. | CONFIRMED TEST-CONTRACT RISK / OWNER-BLOCKED |

### Additional consistency observations

- The topology test on the docs branch now checks the schema/governance/model numeric mirror for concurrency and asserts that selected prose no longer repeats the number (test blob `1362ff8723a63e3594a3559c97dc9e3091d0c674`). This is source-code inspection only; the test was not run, so no pass claim is made.
- The paired Markdown architecture remains version 1.0 (`architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md`, blob `610a611f42d19a55ab7a172e00068c40c5ce5da5`) while its paired YAML model is version 1.1 (blob `193f81eb3cf463ebc38c6b2c3fca8c19e502f176`). This may be intentional semantic-versioning/format lineage, but the source set does not establish that relationship clearly enough; it remains within MH-ARCH-004 and requires explicit lineage metadata or a documented compatibility rule.
- The YAML top-level status `QUALIFICATION_READY_HYBRID_FABRIC` is now accompanied by a comment distinguishing design/model readiness from live qualification. This improves wording but does not reconcile status enums or change `CURRENT-TRUTH.generated.md`, which remains `NOT_PROVEN / BLOCKED`.
- The source test explicitly asserts version 1.1 for YAML and the source links for reference/schema. That validates the YAML model's own expected version, not the relationship between the paired Markdown and YAML documents.
- No normative contract was changed in this addendum. The remediation plan remains `WORKING / NOT ACCEPTED / NOT FROZEN`; no test, qualification, runtime inspection or branch integration was performed.


### Wave 08 addendum — Baseline 1.0 cross-branch authority drift (2026-10-14)

- Compared the exact same path on both live refs. `main` blob `9df4892ed0734050ac79732603d15bb414717310` is 33,711 characters and identifies itself as the historical 68-section Functional Baseline 1.0 passport. The docs-branch blob `1a2f06f50dd69990be58b12a98376b92f12fd14f` is 14,527 characters and calls itself `NORMATIVE / SINGLE SOURCE OF TRUTH`.
- The accepted Functional Baseline 2.0 on `main` explicitly supersedes Baseline 1.0 as the current functional reference while retaining Baseline 1.0 as historical provenance. This makes the docs-branch Baseline 1.0 authority label materially misleading and a cross-branch source/provenance conflict.
- Added MH-ARCH-016 (P1). No baseline file was modified: provenance and owner disposition are required before any relabeling, restoration or consolidation. Baseline 2.0 remains canonical.
- Static/documentary finding only; no tests, qualification, runtime inspection or branch integration. Main and docs refs remain diverged.

## 9. Wave 09 — full repository path/duplicate and qualification-contract consistency sweep (2026-10-14)

### 9.1 Live repository inventory and branch coverage

- `main` HEAD: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`.
- `docs/mediahub-chat-tree-map-20261012` HEAD at this pass: `6326b659d62177585e8a58f49e52f8546fdd242e`.
- Compare: DIVERGED; docs branch ahead 820 / behind 2; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Main tree: 798 entries / 721 blob files, tree SHA `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`, not truncated.
- Documentation tree: 904 entries / 827 blob files, tree SHA `6326b659d62177585e8a58f49e52f8546fdd242e`, not truncated.
- Every path in the main tree also exists in the documentation tree; 106 blob paths exist only on the documentation branch. This is path coverage only: it does **not** mean same-path contents are equal. The two commits unique to `main` modify `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`, whose main/docs blobs differ materially (see MH-ARCH-016).
- This was a full recursive path inventory with targeted content reads, not semantic line-by-line review of every file. No tests, CI workflows, runtime or host state were executed/inspected.

### 9.2 Complete basename-collision inventory and classification

- The tree scan found **24 distinct basename-collision groups** and **44 path occurrences beyond the first entry** for those repeated basenames. A prior working estimate of 37 is superseded. There are zero full-path case-insensitive/case-only collisions.
- Exact duplicate blob scan found one repeated-content group: ten zero-byte `__init__.py` package markers sharing blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`. No other repeated blob-SHA groups were found. Same basename therefore must not be equated with duplicate content or a defect.
- The 24 groups are: 18 mirrored MH-03 pairs; 8 `README.md` files; 16 `__init__.py` package markers; 2 `SKILL.md` files; 2 `capability.schema.json` files; 2 `com.mediahub.astra.github-agent.plist` deployment manifests; and 2 `state.py` files. The group totals count unique basenames, while the repeated path counts above are the excess entries beyond one representative per group.
- `architecture/mesh/capability.schema.json` (`d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c`) and `schemas/domain/capability.schema.json` (`fe80659b570ac58829f10410feb5c700388f87c0`) are different contracts with different `$id`, required fields and semantics; do not merge them solely because the basename matches.
- `ops/mesh/state.py` (`d02780894cfb5d3c0fc7878d57a08fac2e428efc`) implements mesh node/replica lifecycle transitions; `runtime/mediahub_runtime/state.py` (`a2115b81f52a63feb357e484bd982a6a32641d81`) defines the canonical StateAuthority interface. These are distinct responsibilities, not duplicate implementations.

### 9.3 MH-03 divergent mirror pairs — all paths and blob SHAs

Each left path is under `architecture/`; its same-basename right path is under `docs/architecture/mh-03/`. All 18 blob-SHA pairs differ. This establishes divergent content bytes; it does not assert that every pair has been semantically reviewed.

| Basename | `architecture/` blob SHA | `docs/architecture/mh-03/` blob SHA |
|---|---|---|
| `MH-03-acceptance-criteria.md` | `e96adaac2eb52e2f8058cc889485ec982bf606e5` | `eefb645d89c7c3046636d8344515aa02b7ccebe3` |
| `MH-03-command-execution.md` | `b9197759e70107f1be5968e8669288d991360003` | `8a9e1066f00cf9a7a3128c00eada857b18cef32f` |
| `MH-03-contradiction-register.md` | `5879ad2ab19110ae7418f881cbd7603a10ff996e` | `7986b072983f1d6f828b7214f4896b91c91392f2` |
| `MH-03-decision-log.md` | `e202a60c48726a78b0e5b7d1c191f62cfd2caaa1` | `4089e4573a083adcde921acd8ac0bd09c98d6a2f` |
| `MH-03-degraded-mode.md` | `f724cedc52f7421c520c1183fa8e8e078fe93082` | `7b70229049b80a230b201806aab59f394e0d33bd` |
| `MH-03-error-handling.md` | `bd2157deb94c2823c6b6fac2988945b7bc412ef3` | `a33051aabb24447cf993755e84569917fe37f037` |
| `MH-03-event-model.md` | `bd7c50063c518f428217ca2e906c615017f02ae6` | `330b98cba91125ac6e57e662d4eebeb37b6df00a` |
| `MH-03-evidence-register.md` | `07dd464fe23ba91943053f658c8d804ec67b5fb6` | `865a1bda46984cd8b3384aaea99ec9f9c86746d4` |
| `MH-03-health-model.md` | `a4b9e8838d6b88ea629b9ee3642b6bcc791cba47` | `2f5840218dfdc0103e16721ebf467150d19cb216` |
| `MH-03-lifecycle.md` | `300363a06fe678d3511c2a4b843678bf200df5f0` | `41baa81406dcd25b8b1537adf9c8b1289c38edcd` |
| `MH-03-recovery-boundary.md` | `dd3746ab986a736af559d400f66f578d91aa4188` | `24f957fdc7070cd39ed4a116c5e1e0c40e912253` |
| `MH-03-runtime-dependencies.md` | `7bf2c9db634cfe149f8f6199d2eeae1813499be5` | `115dfbbf8d00b01865c4db4590f44a7f7a5eced7` |
| `MH-03-runtime-foundation.md` | `325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2` | `2457451017daa0f91e9e978e44c91e1e49d0d7a3` |
| `MH-03-runtime-model.md` | `03a3ce4837591827e5eb3e20e36214e394ffca82` | `d43d456f745f4503c6dc0ad3f76dbaf051940747` |
| `MH-03-runtime-observability.md` | `aa33cd18290bf486b19fad08f3a377aa5ed7a298` | `f7fba8708bc57eb8baa2d8ecc866fb58d18c9d6b` |
| `MH-03-service-boundaries.md` | `02672aa1c377d04a3a7e0a7cff5b767a89ee0fcb` | `cb9e5800d20ab3ee463bc30446419c95d556a87c` |
| `MH-03-shutdown-sequence.md` | `37d2dad130cb611799191bdbde5b4803adea37bb` | `cef347ea1e6ce02a38283aba4a47ae4353082f30` |
| `MH-03-startup-sequence.md` | `87ecefe90cb0f8c306682d31a8c6f613a2fcfcf9` | `a2fa93260f13f909c345319252a5b63440265ecc` |

The root index identifies the root-level filenames as its required artifacts, but its own status is PROPOSED. The nested directory has no `MH-03-index.md`. One direct semantic conflict is already confirmed: the root contradiction register records C03-08 as governance review required for a proposed PostgreSQL/etcd/NATS HA path conflicting with the frozen single-node/in-memory foundation; the nested copy states that no current explicit contradictions were identified. Keep this family P1 and ask for controlled source disposition rather than silently choosing one version.

### 9.4 Additional confirmed findings

| ID | Priority | Finding | Evidence | Required action | State |
|---|---|---|---|---|---|
| MH-ARCH-017 | P1 | **ASTRA G4 mandatory-path matrix differs between machine schema and prose.** The canonical launch schema defines five mandatory paths: `CODEX_FCC`, `CLAUDE_FCC`, `CODEX_OMNIROUTE`, `CLAUDE_OMNIROUTE`, `CLAUDE_CODE_DIRECT`. The unified Markdown G4 section says “every mandatory execution path” but enumerates only the three Claude paths. This is distinct from the three permanent Claude production lanes: qualification path inventory and permanent runtime pool are different concepts. | Main schema blob `aef6229477ed8ec45e45170f98ea87f7ba75ca29`; docs schema `0b86b07dfa916d4485ce1f8f54d19de136d98491`; main unified Markdown `e2067dc41b52983fc4e0b2549fb6af3c099cbc60`; docs Markdown `610a611f42d19a55ab7a172e00068c40c5ce5da5`; schema test `090ce2ecb02e58a3c48a7a729279dea9a387f339`. | Make prose reference the canonical mandatory-path list (or enumerate the full five-path contract), and add an exact test assertion that prevents the prose/schema sets from drifting. Preserve the separate three-lane production topology. | CONFIRMED CONTRACT/PROSE MISMATCH |
| MH-ARCH-018 | P1 | **Two launch-agent manifests share one LaunchAgent label but invoke different programs and environments.** If both are installed in the same macOS launchd domain, label collision/overwrite or ambiguous service ownership is possible. Installation state was not inspected, so co-installation is not asserted. | `deploy/com.mediahub.astra.github-agent.plist` blob `2cca029b502fd911ec38272871c823a8717ed8fd` launches `/usr/bin/python3 /opt/mediahub/astra/astra_github_agent.py`; `ops/launchd/com.mediahub.astra.github-agent.plist` blob `d1d8aea99c2303c26e542a3d1c5e54b4596521d0` launches `/bin/bash /Users/voktor/astra-work/ops/astra-github-bootstrap.sh`; both use `com.mediahub.astra.github-agent`. | Classify manifests as mutually exclusive deployment profiles or assign distinct labels if they represent separate services; document canonical owner and prevent accidental co-installation. Requires target/operations owner confirmation; no host was inspected. | CONFIRMED MANIFEST COLLISION / DEPLOYMENT UNKNOWN |
| MH-ARCH-019 | P1 — repaired in docs branch | **Project-map navigation IDs had collisions at both the original three nested headings and a later appended MH-03 wave.** Wave 06's first broad check missed mixed heading levels; a later appended section reused `20.185`, creating a new duplicate after the earlier fix. | Original pre-fix map `19e775bc581229dad48e7d603a74202eb9f12fab`; second pre-fix map `e3eadac3f1f36cae870d694bb25ae2150775a726`. Original IDs: `20.97`, `20.98`, `20.183`; reintroduced ID: `20.185`. | Original headings rekeyed to `20.98.1`, `20.98.2`, `20.184.1`; later MH-03 drift heading rekeyed `20.185` → `20.204`; complete wave 09 entry is `20.205`. All heading levels were rescanned after the final write. Navigation-only; no source-contract meaning changed. | PATCH APPLIED; FINAL READ-BACK VERIFIED (2026-10-14) |
| MH-ARCH-020 | P2 | **File-basename collisions that are not duplicate contracts need explicit classification.** The two capability schemas have distinct IDs/semantics; the two `state.py` files serve mesh lifecycle versus product StateAuthority interface. | Schema SHAs and state module SHAs listed in §9.2. | Keep them separate; where discoverability is ambiguous, clarify path/namespace in the index and verify consumer references before any rename. | DISTINCT RESPONSIBILITIES / NAMING RISK |
| MH-ARCH-021 | P1 | **MH-03 mirror-family governance/status drift exceeds the known contradiction-register conflict.** The proposed root index lists root-level artifacts as required, but is itself PROPOSED; root/nested decision logs differ (root adds MH3-D10/D11 on future-governed persistence/HA), evidence registers differ in acceptance/implementation-authorization wording and E03-06 provenance, and the contradiction registers disagree on whether C03-08 is an active governance review. These are material status/lineage differences, not mere duplicate files. | Root index blob `b2d2eeb1b89117d10605c231e79378eebc437c5f`; root decision log `e202a60c48726a78b0e5b7d1c191f62cfd2caaa1`; nested decision log `4089e4573a083adcde921acd8ac0bd09c98d6a2f`; root evidence register `07dd464fe23ba91943053f658c8d804ec67b5fb6`; nested evidence register `865a1bda46984cd8b3384aaea99ec9f9c86746d4`; root contradiction register `5879ad2ab19110ae7418f881cbd7603a10ff996e`; nested contradiction register `7986b072983f1d6f828b7214f4896b91c91392f2`. | Keep both trees unchanged. Governance owner must explicitly designate canonical source or synchronized-view model, resolve status/decision/evidence deltas, and then reconcile all 18 pairs with provenance and reference checks. Root index supports root as intended location but is PROPOSED, so this is not sufficient authority to promote it. | CONFIRMED SOURCE/STATUS DRIFT; OWNER DISPOSITION REQUIRED |
| MH-ARCH-022 | P1 | **MH-03 runtime-foundation mirror pair has asymmetric contract coverage, but no direct semantic contradiction established in this pass.** Both files remain PROPOSED and agree on sole State Authority, in-memory state, mandatory P0-05 boundary, single-node/no-HA and no unauthorized physical persistence. The root copy adds an explicit offline-first chain, full command/event mutation path and enumerated acceptance gates; the nested copy adds shutdown ordering and technology-choice candidate wording. Root index lists root artifacts as required but is itself PROPOSED; it does not resolve canonical authority. | `architecture/MH-03-runtime-foundation.md` blob `325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2`; `docs/architecture/mh-03/MH-03-runtime-foundation.md` blob `2457451017daa0f91e9e978e44c91e1e49d0d7a3`; root index `architecture/MH-03-index.md` blob `b2d2eeb1b89117d10605c231e79378eebc437c5f`. | Preserve both files. Record this as scope/coverage drift, not a proven contradiction. Add a bidirectional clause crosswalk only after owner selects root canonical, nested canonical, or governed synchronized views. Check inbound references and acceptance-criteria paths before any sync/delete. | CONFIRMED ASYMMETRIC COVERAGE; CANONICAL AUTHORITY OPEN |
| MH-ARCH-023 | P2 — repaired in docs branch | **Project map contained a legacy duplicate top-level numeric heading ID `16`.** The earlier Baseline 1.0 passport heading and its subsections used ID 16; a later `## 16. Owner decision register` reused that ID. | Pre-repair map blob `430a32472afa5df6511c6458be09b931d7b8bbba`; initial repair read-back `7dea16102dbc1908906d89b4637f90f196a15f4d`; latest map at this scan `4a8cf6d3ad4d8febde4c1a5a5a21b4392a725881`. | Preserved historical `16`; rekeyed the later heading to `20.208`; recorded repair at `20.209`. The latest anchored all-level scan found 266 numeric headings, all 266 unique, zero duplicates. Map-local scan found no inbound `#16-owner-decision-register` reference; repository-wide fragment audit remains open. | PATCH APPLIED; LATEST READ-BACK VERIFIED / REPOSITORY-WIDE FRAGMENT AUDIT OPEN |

### 9.5 Updated prioritized sequence

1. **P0 security/authority:** ADMIN-01 lifecycle authority and P0-07 D1/D2/D3/D5/D6/D7 gaps; commission qualified independent D2 R-01…R-06 review; keep mutation/publication blocked until contract and evidence close the chain.
2. **P1 source-control/ASTRA:** ADMIN-03/04/05; reconcile the main-only concurrency text 2 vs canonical schema 3; resolve A0 scope only after DEC-DEV-02; fix the G4 five-vs-three mandatory-path prose discrepancy under controlled source review; clarify paired YAML/Markdown model version/status lineage.
3. **P1 MH-03 source family:** resolve the intended root vs nested documentation location; inspect references/IDs; then issue an explicit source-of-truth/redirect or controlled content reconciliation for all 18 pairs. Do not delete historical content.
4. **P1 deployment manifest:** ask the target/operations owner to classify whether the two same-label LaunchAgent files are alternative profiles or distinct services. No runtime/host inspection or installation was performed.
5. **P1/P2 documentation integrity:** retain the map's hierarchical heading-ID repair and perform a fresh full-level scan; classify all 24 repeated-basename groups without treating conventional README/skill/package markers as defects.
6. **P0 qualification/acceptance:** after explicit authorization, define a separate test/qualification wave against exact SHA. Current Truth stays G0–G11 BLOCKED / NOT_PROVEN; Contour B remains gated.

### 9.6 Additional administrative questions for owner/governance

These questions do not create new normative DEC IDs. Existing ADMIN-01…ADMIN-05 remain in §5.

**MH-03 source family — what is the authoritative disposition?**
- **A (recommended):** Treat root `architecture/MH-03-*.md` as the intended canonical location because `architecture/MH-03-index.md` lists those filenames; after provenance/link review, label nested counterparts as historical/derived redirects and reconcile material deltas.
- **B:** Declare `docs/architecture/mh-03/` canonical and update the root index/pointers only through a governed change.
- **C:** Keep both as explicit separate views with a named owning source and required synchronization/evidence; no path may be cited as accepted until that rule is recorded.
- **Recommendation:** A is the strongest existing-source interpretation but remains a proposal because the root index itself is PROPOSED and content conflict exists.

**LaunchAgent manifests — how should the same-label profiles be governed?**
- **A:** Declare one manifest canonical and mark the other obsolete/non-coinstallable, preserving history.
- **B:** They represent distinct deployment profiles/services; give each its own label and explicit target/owner in a separately authorized change.
- **C (safe interim):** Treat them as mutually exclusive examples until the operations owner confirms intended target; do not install both or infer active service state.
- **Recommendation:** C until the target/operations owner resolves intended use; then A or B based on evidence.

### 9.7 Scope and non-claims

- The tree scan is complete and untruncated at the listed refs; semantic review remains risk-based and targeted.
- Selected navigation-critical files were link-checked and had no missing relative paths at the earlier checked revisions; the project-wide Markdown link graph has not been exhaustively validated.
- No tests, qualifications, CI runs, runtime/host inspection, credential/provider/model calls, installation, infrastructure change, deployment, migration, merge, rebase or cherry-pick were performed.
- Current main qualification truth remains G0–G11 BLOCKED / overall NOT_PROVEN. Baseline 2.0 remains canonical, Baseline 1.0 remains historical provenance, and Contour B remains blocked.



### 9.8 Map heading-ID repair — independent read-back (2026-10-14)

- Re-fetched the current documentation-branch map at blob `05980cf0dcd96dffcc59aa981cd1a8e2c311ea9c` and scanned all Markdown headings whose section number begins the heading title.
- Counted 257 numbered section headings; found **zero duplicate section IDs**. Confirmed the intended nested IDs `20.98.1`, `20.98.2`, and `20.184.1` are present.
- An exploratory broad regex initially flagged `20.68` twice because a later heading's prose title references “§20.68”; this is not a duplicate section ID. The anchored section-number scan removes that false positive.
- The first three nested-heading collisions were fixed and verified at map blob `05980cf0dcd96dffcc59aa981cd1a8e2c311ea9c`. Wave 09 later appended an MH-03 drift heading reusing existing ID `20.185`; this created a second collision, now fixed by rekeying that appended heading to `20.204` and adding project-wide wave 09 at `20.205`. Final map blob after recheck is `020969a87b3a1701e5d484fe76c93f2db9e240b9`. This read-back does not claim a full Markdown-link-graph audit or semantic review of every file.


### 9.9 MH-03 contradiction-register pair — source-anchored classification (2026-10-14)

- Read the root index, root and nested contradiction registers, decision logs, and evidence registers from the live documentation branch. No source files in either MH-03 tree were modified.
- The root index lists root-level filenames as required artifacts, but the index status is PROPOSED / NOT ACCEPTED. This is evidence of intended placement, not an accepted canonical-source decision.
- Root contradiction register records C03-08 as GOVERNANCE REVIEW REQUIRED for the proposed PostgreSQL/etcd/NATS HA path conflicting with the inherited single-node/in-memory foundation; the nested register says no current explicit contradictions were identified.
- Root decision log adds MH3-D10/D11 (future governance-gated persistence/HA and non-authoritative technology integration) absent from the nested decision log. Root/nested evidence registers also differ materially in status language, including “ACCEPTED / IMPLEMENTATION AUTHORIZED” in nested E03-01 versus PROPOSED in the root register.
- Added MH-ARCH-021. Classification: confirmed source/status drift; no conclusion that one copy is authoritative. Preserve both copies pending owner disposition. Next decision required: canonical root source, canonical nested source, or explicitly governed synchronized views.

### 9.10 Final map heading-ID verification after wave 09 (2026-10-14)

- Before-fix map blob: `e3eadac3f1f36cae870d694bb25ae2150775a726`. An anchored scan found a duplicate level-2 ID `20.185`: the original P0-07 canonical-read join trace and a newly appended MH-03 source/status drift entry. The appended section had reused a historical ID.
- Corrected only the project map: preserved the original `20.185` heading, changed the appended MH-03 drift entry to `20.204`, updated map incremental-update metadata to `§20.205`, and added a summary of the Wave 09 unified audit at `§20.205`.
- Read-back map blob: `020969a87b3a1701e5d484fe76c93f2db9e240b9`; update commit `1bbceb26656bb3da7fa23468ff8a2e32fd245174`.
- The initial post-wave-09 scan exposed a second appended heading reusing `20.204` (the separate unified-passport consolidation entry added after the scan input was read). This was corrected by rekeying the passport heading to `20.206`, preserving `20.204` for the MH-03 source/status finding and `20.205` for wave 09. The final anchored read-back on map blob `261910c6a2827036dc3ecd23ed4a8aa25216768b` counted 260 numeric headings, 260 unique IDs and zero duplicates. Any broader Markdown link-graph defect remains outside this check.
- The unified plan remains the single current remediation register. No normative MH-03 file, baseline, ASTRA gate source or `main` file was changed; this map repair does not decide which MH-03 tree is canonical.

### 9.11 Final collision count after concurrent map addition (2026-10-14)

- A subsequent live read found the unified-passport consolidation heading had been appended with ID `20.204`, duplicating the MH-03 mirror-family heading. The map now has monotonic terminal IDs `20.203` (Baseline 1.0 drift), `20.204` (MH-03 source/status drift), `20.205` (Wave 09 project-wide audit), and `20.206` (unified passport consolidation).
- The duplicated passport heading was changed only to `20.206`; map metadata now identifies the latest verified incremental entry as §20.206.
- Final map read-back blob `261910c6a2827036dc3ecd23ed4a8aa25216768b`; 260 numbered section headings across levels 2–4, all 260 IDs unique, zero collisions.
- This resolves only the map heading-ID collision. It does not declare the complete Markdown link graph clean or any architecture accepted/frozen.



### 9.12 MH-03 runtime-foundation pair — bounded scope/provenance comparison (2026-10-14)

**Sources re-fetched from** `docs/mediahub-chat-tree-map-20261012`:
- Root index `architecture/MH-03-index.md`, blob `b2d2eeb1b89117d10605c231e79378eebc437c5f`, status PROPOSED; lists root-level artifacts as required.
- Root runtime foundation `architecture/MH-03-runtime-foundation.md`, blob `325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2`, status PROPOSED.
- Nested runtime foundation `docs/architecture/mh-03/MH-03-runtime-foundation.md`, blob `2457451017daa0f91e9e978e44c91e1e49d0d7a3`, status PROPOSED.

**Observed alignment:** both files state that State Authority is the sole canonical mutation authority, current state is in-memory, P0-05 is the mandatory boundary, the foundation is single-node/no-HA, physical persistence is not authorized, commands are requests and events are facts, and State Authority failure does not create fallback authority.

**Observed scope asymmetry:** the root file explicitly enumerates the offline-first deterministic chain, a full command → validation → authorization/policy → consumer contract → State Authority → event → observers path, and several acceptance prerequisites. The nested file adds a shutdown ordering and an explicit statement that technology choices remain CANDIDATE until evidence/compatibility/security/architecture decision. These differences are not by themselves proof of contradiction, but they mean neither file is a byte-identical mirror or complete substitute for the other.

**Disposition:** MH-ARCH-022 records confirmed asymmetric coverage, not a semantic conflict. The root index's required-artifact list is evidence of intended placement only; its PROPOSED status does not confer canonical authority. Both files remain unchanged. This was not an exhaustive inbound-reference search and does not decide the canonical tree. Next: extend the provenance/reference inventory to one additional pair, while owner/governance disposition remains required before reconciliation.

### 9.13 Core-document relative-link path check (2026-10-14)

- Refreshed the complete, non-truncated documentation-branch tree at `010546262e58c5a1b5b0fe2569b443ef6b7559a9` (904 tree entries / 827 blobs).
- Re-fetched the current exact blobs for the single remediation plan (`e2419c2d0dd7be7df09dcebe6e95bf1c7eb7d1b9`), map (`261910c6a2827036dc3ecd23ed4a8aa25216768b`), roadmap (`bed279bb26f6cea99a9217198ac18f0731998dba`) and checkpoint (`ac63eec13e8ce034d8e77750438159f7503d51c0`).
- Parsed Markdown inline link targets and resolved repository-relative paths against the correct documentation-branch tree. Counts: plan 14 relative links, map 98, roadmap 10, checkpoint 29. All **151 inspected relative links resolve to existing repository paths**; no missing-path target was found in these four core documents.
- Scope limitation: this verifies resolved path existence, not fragment/heading anchors, generated links, raw HTML links, or the complete link graph across all repository files. It is not a semantic or runtime check.
- The single remediation plan remains the current issue register. This check created no new defect ID and does not change any acceptance/qualification status.



### 9.14 Project-map duplicate numeric heading ID — follow-up repair (2026-10-14)

- The map scan on pre-repair blob `430a32472afa5df6511c6458be09b931d7b8bbba` confirmed that `## 16. Owner decision register — 2026-10-12` reused the earlier Baseline 1.0 passport section ID `16`. The later heading has now been rekeyed to `20.208`.
- MH-ARCH-023 is a documentation/navigation defect, not an architecture-contract conflict. The map-only scan found no explicit inbound fragment reference, but other repository documents were not exhaustively searched.
- Initial read-back after the repair on map blob `7dea16102dbc1908906d89b4637f90f196a15f4d` found 263/263 unique numeric heading IDs; the current map later added §20.210–§20.212. The latest full anchored scan on map blob `4a8cf6d3ad4d8febde4c1a5a5a21b4392a725881` found 266 numbered headings, 266 unique IDs, zero collisions. The earlier broad count of 282/281 remains unreproduced and is not treated as current.


### 9.15 MH-03 lifecycle and acceptance-criteria mirror review (2026-10-14)

- Refreshed the exact root/nested lifecycle and acceptance-criteria blobs on `docs/mediahub-chat-tree-map-20261012`; compared headings, status labels, lifecycle/failure semantics, acceptance prerequisites and the root index. This is a bounded source comparison, not a complete audit of every clause in all 18 pairs.
- Root lifecycle (`architecture/MH-03-lifecycle.md`, `300363a06fe678d3511c2a4b843678bf200df5f0`) explicitly lists READY dependency readiness, optional-dependency DEGRADED behavior, recovery inside existing authority boundaries, and no shadow state/fallback mutation on State Authority failure. Nested lifecycle (`docs/architecture/mh-03/MH-03-lifecycle.md`, `41baa81406dcd25b8b1537adf9c8b1289c38edcd`) summarizes READY/DEGRADED/recovery and adds a repeated-failure no-authority-escalation constraint, but omits some explicit root statements.
- Root acceptance criteria (`architecture/MH-03-acceptance-criteria.md`, `e96adaac2eb52e2f8058cc889485ec982bf606e5`) enumerate acceptance conditions and contradiction review. Nested criteria (`docs/architecture/mh-03/MH-03-acceptance-criteria.md`, `eefb645d89c7c3046636d8344515aa02b7ccebe3`) explicitly enumerate gates and evidence/decision-register review and articulate the required runtime/State Authority outcome.
- Both sets remain PROPOSED / NOT ACCEPTED; root `architecture/MH-03-index.md` (`b2d2eeb1b89117d10605c231e79378eebc437c5f`) is also PROPOSED and lists root artifacts, while no nested index exists. This does not establish accepted canonical authority.
- Added MH-ARCH-024 as **asymmetric coverage confirmed; direct contradiction not established by this pass**. No MH-03 source was modified, deleted or promoted. Remaining 18-pair reconciliation requires owner/governance choice and reviewed inbound-reference/ID checks.
- Live refs at start of this pass: `main` HEAD `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; docs branch HEAD `547f8558f5f56d7eab15433974d9cc28909eef37`; branch comparison remains DIVERGED, ahead 854 / behind 2, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. These counts are snapshot-specific and must be refreshed before future writes.
- No tests, CI, qualification, runtime/host inspection, credentials/provider/model calls, installations, infrastructure changes, deployment, migration, merge, rebase or cherry-pick were performed.

### 9.16 MH-03 command-execution mirror review (2026-10-14)

- Re-fetched current documentation-branch versions of the root and nested command-execution contracts and the root index. Live refs before write: `main` HEAD `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; docs branch HEAD `c128c006a4d73ec42e423a35ae3caf7a51d57415`; DIVERGED, ahead 860 / behind 2; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Root command execution blob `b9197759e70107f1be5968e8669288d991360003` and nested blob `8a9e1066f00cf9a7a3128c00eada857b18cef32f` share the core fail-closed/no-direct-mutation/single-State-Authority rules. Root explicitly says stale transactions are rejected and command execution cannot use a private authoritative state store.
- Root flow uses the generic term “Consumer Contract”; nested flow names the P0-05 consumer boundary and includes the integration/capability boundary before validation. Nested contract additionally requires explicit context/bounded inputs and explicitly forbids treating events/telemetry as implicit commands. Root and nested therefore have materially asymmetric coverage, but a direct logical contradiction was not established.
- Added `MH-ARCH-025` to the prioritized register. Both files remain PROPOSED and unmodified; no canonical root/nested decision was inferred. Root index `b2d2eeb1b89117d10605c231e79378eebc437c5f` is also PROPOSED, and no nested index exists.
- Next: continue the remaining MH-03 pair-by-pair source/reference review, keeping coverage asymmetry distinct from proven contradiction. No tests, qualification, runtime/host inspection, deployment, migration or branch integration occurred.

### 9.17 MH-03 evidence-register pair — acceptance/provenance status conflict (2026-10-14)

- Re-fetched the root and nested evidence registers and their paired decision logs from the live documentation branch. This is a bounded comparison of four documents, not a review of all clauses in the 18-pair MH-03 family.
- Root evidence register `architecture/MH-03-evidence-register.md`, blob `07dd464fe23ba91943053f658c8d804ec67b5fb6`, is marked `PROPOSED`. It classifies E03-01…E03-04 as `FROZEN / INHERITED`, E03-05 as inherited/proposed according to the upstream MH-2 status, and E03-06 as a repository/topology observation with limited provenance.
- Nested evidence register `docs/architecture/mh-03/MH-03-evidence-register.md`, blob `865a1bda46984cd8b3384aaea99ec9f9c86746d4`, marks E03-01 as `ACCEPTED / IMPLEMENTATION AUTHORIZED`, E03-02…E03-04 as `ACCEPTED / FROZEN`, and introduces E03-07 production topology verification and E03-08 production security qualification as not yet verified/established.
- The pair is not a harmless formatting duplicate: the same E03 identifiers map to different evidence and acceptance states (notably E03-01), and the nested register's “implementation authorized” label is not supported by the root register's proposed/inherited classification. This confirms **status/provenance conflict**; it does not establish which register is authoritative, nor does it prove any real-world implementation authorization.
- The paired decision logs also differ: root `architecture/MH-03-decision-log.md` (`e202a60c48726a78b0e5b7d1c191f62cfd2caaa1`) adds MH3-D10/D11 future governance-gated persistence/HA constraints, while nested `docs/architecture/mh-03/MH-03-decision-log.md` (`4089e4573a083adcde921acd8ac0bd09c98d6a2f`) records MH3-D09 as FROZEN CONSTRAINT but does not include D10/D11. Both are proposed artifacts; absence in the nested file is coverage/lineage drift, not automatic rejection of the extra decisions.
- Root recovery boundary (`dd3746ab986a736af559d400f66f578d91aa4188`) and nested recovery boundary (`24f957fdc7070cd39ed4a116c5e1e0c40e912253`) share fail-closed authority constraints but have different recovery loop/stop-policy specificity. Root runtime model (`03a3ce4837591827e5eb3e20e36214e394ffca82`) and nested runtime model (`d43d456f745f4503c6dc0ad3f76dbaf051940747`) likewise express compatible core planes/authority boundaries with asymmetric coverage. These additional pairs remain review candidates; no direct contradiction is claimed from this pass.
- Added **MH-ARCH-026 (P1)**: MH-03 evidence-register pair contains a material evidence-ID/status/provenance conflict, including a nested implementation-authorization label that is not substantiated by the paired root register. Required action: preserve both sources; owner/governance must select root canonical, nested canonical, or governed synchronized views; reconcile ID meanings, evidence provenance and acceptance labels before either register is cited as accepted authority.
- No MH-03 source was changed, deleted, synchronized or promoted. No tests/qualification, runtime/host inspection, credentials/provider/model calls, installation, infrastructure change, deployment, migration, merge, rebase or cherry-pick occurred.

### 9.18 Final live core-document link-path and map-ID rescan (2026-10-14)

- Refreshed the live docs-branch tree at `beaa981fd4e159a6ada5d55c2035332599d7f0f5`: 904 entries / 827 blobs, not truncated. At scan time, `main` was `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; docs branch was DIVERGED, ahead 863 / behind 2; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Live core documents re-fetched: plan `f5db88583d46aafe4fe6a46b6060b5b3840c62d6`, map `4a8cf6d3ad4d8febde4c1a5a5a21b4392a725881`, roadmap `8a189fdb4ad8d7bf33a6d4318ec3cc34e186ab83`, checkpoint `bc85e35edf3638c2152f597768e0174d63352374`, bootstrap `49b4760b4adf4f1565fac0aa4697da000f1cf37b`.
- Anchored map-heading scan across levels 1–6: 266 numeric headings, 266 unique IDs, zero duplicates (194 level-2 and 72 level-3). Latest map sections include `20.210` core link path check, `20.211` MH-03 lifecycle/acceptance comparison and `20.212` MH-03 command-execution comparison.
- Relative inline Markdown paths were rechecked against that docs-branch tree: plan 14, map 103, roadmap 12, checkpoint 29, bootstrap 1. All **159/159 targets resolve to existing repository paths**. This does not validate fragment anchors, raw HTML/generated links, or the entire repository link graph.
- No status is promoted: Baseline 2.0 remains canonical, Baseline 1.0 remains historical provenance, G0–G11 remain BLOCKED / NOT_PROVEN, Contour B remains gated. No tests/CI, qualification, runtime/host inspection, provider/model calls, credentials, installation, infrastructure, deployment, migration or branch integration occurred.

### 9.19 MH-03 degraded-mode mirror review (2026-10-14)

- Re-fetched both current root/nested degraded-mode documents and the root index from the documentation branch. Root `architecture/MH-03-degraded-mode.md` SHA `f724cedc52f7421c520c1183fa8e8e078fe93082`; nested `docs/architecture/mh-03/MH-03-degraded-mode.md` SHA `7b70229049b80a230b201806aab59f394e0d33bd`; index SHA `b2d2eeb1b89117d10605c231e79378eebc437c5f` is PROPOSED.
- Shared invariants: deterministic/local operation where allowed, isolate optional failures, no mutation fallback if State Authority is unavailable, and no degradation that relaxes authorization/trust. Nested file explicitly defines the known impaired-capability subset and all four recovery transitions, including failed recovery back to DEGRADED. Root says READY is restored only after health/dependency checks but does not enumerate RECOVERING → DEGRADED.
- Added MH-ARCH-027: asymmetric coverage confirmed; direct contradiction not proven. Both source files remain unmodified and PROPOSED.
- No tests or runtime operations were performed.

### 9.20 MH-03 error-handling mirror review (2026-10-14)

- Root `architecture/MH-03-error-handling.md` SHA `bd2157deb94c2823c6b6fac2988945b7bc412ef3`; nested `docs/architecture/mh-03/MH-03-error-handling.md` SHA `a33051aabb24447cf993755e84569917fe37f037`; root index remains PROPOSED.
- Shared core classes: malformed/ambiguous input, missing authorization, stale transaction, unknown identity/dependency, critical/optional dependency failures, and no fallback authority. Root adds supervised restart/isolation and observability without telemetry authority; nested adds stable/bounded/sanitized errors, no secret/private-path disclosure, no partial lifecycle transition and no canonical-state corruption.
- Added MH-ARCH-028: complementary asymmetric coverage, not a proven contradiction. Preserve both files pending source model selection.

### 9.21 Master-roadmap numeric heading-ID collision (2026-10-14)

- Live docs-branch roadmap blob before repair `31cfe03f94f8f61c0c3e144e3e78c28ee0d2a08d` has duplicate H2 numeric IDs `8` and `28`: `## 8. Current blockers and explicit non-claims` versus the appended P0-07 execution record also labelled `8`; and command-execution versus evidence-register records both labelled `28`. The following unified-plan navigation entry uses `29`.
- Added MH-ARCH-029. Repair only navigational labels; preserve every historical finding and paragraph. The P0-07 D1/D2 update will become `### 10.5`, evidence-register update `## 29`, plan subsection-ID repair `## 30`; new records follow as `## 31` and `## 32`.
- This is a documentation defect, not a product/runtime defect. After the roadmap repair, re-read it and scan numeric H2/H3 headings and repository-local references. Do not change decision/acceptance status.

### 9.22 MH-03 health-model mirror review (2026-10-14)

- Re-fetched root `architecture/MH-03-health-model.md` (blob `a4b9e8838d6b88ea629b9ee3642b6bcc791cba47`) and nested `docs/architecture/mh-03/MH-03-health-model.md` (blob `2f5840218dfdc0103e16721ebf467150d19cb216`), plus root index `architecture/MH-03-index.md` (blob `b2d2eeb1b89117d10605c231e79378eebc437c5f`, PROPOSED).
- Shared invariant: health is observational/control metadata, not canonical domain state; health signals cannot mutate canonical state. Both mention liveness, readiness and dependency health.
- Nested adds explicit lifecycle states STARTING/READY/DEGRADED/RECOVERING/STOPPING/STOPPED, fail-closed readiness when critical foundation is missing, optional-dependency degradation without false full readiness, and no exposure of mutable internal objects or sensitive data. Root adds authority-health and lifecycle-health dimensions but does not enumerate the same state/privacy/readiness details.
- Classification: **asymmetric coverage confirmed; direct contradiction not established**. Added MH-ARCH-030 (P2) to the single consolidated register. Both source files remain unchanged and PROPOSED; root index does not establish accepted canonical authority.
- No tests, qualification, runtime/host inspection, implementation, deployment, migration or branch integration. Qualification remains NOT_PROVEN / BLOCKED; Contour B remains gated.
- Next: review the next unreviewed MH-03 root/nested pair using exact live refs/SHAs, and continue preserving both copies pending explicit source-model disposition.


### 9.23 MH-03 runtime-model / recovery / event / dependency / lifecycle sequence mirror comparison (2026-10-14)

**Scope:** read-only semantic comparison of six root/nested pairs in the current documentation branch. The root files generally declare `Status: PROPOSED`; the nested mirrors frequently provide additional detail but do not consistently carry the same status metadata. No source contract was changed and no normative authority was inferred.

**Live refs:** documentation branch `8871054b96395498c99daeb9db15430e4980cc53`; tree SHA `8871054b96395498c99daeb9db15430e4980cc53`. Main remains `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; comparison is diverged, ahead 874 / behind 2, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No integration performed.

| Finding | Priority | Root source (blob SHA) | Nested source (blob SHA) | Confirmed difference | Classification / next action |
|---|---|---|---|---|---|
| MH-ARCH-031 | P2 | `architecture/MH-03-runtime-model.md` — `03a3ce4837591827e5eb3e20e36214e394ffca82` | `docs/architecture/mh-03/MH-03-runtime-model.md` — `d43d456f745f4503c6dc0ad3f76dbaf051940747` | Root has explicit PROPOSED status and a five-plane ASCII topology; nested adds authority flow, forbids shadow canonical stores and describes logical components, but omits status. | Asymmetric coverage confirmed; not yet a direct contradiction. Decide canonical source and align status/required invariants after owner disposition. |
| MH-ARCH-032 | P2 | `architecture/MH-03-recovery-boundary.md` — `dd3746ab986a736af559d400f66f578d91aa4188` | `docs/architecture/mh-03/MH-03-recovery-boundary.md` — `24f957fdc7070cd39ed4a116c5e1e0c40e912253` | Root enumerates recovery responsibilities and explicit forbidden authority changes; nested adds allowed recovery classes and bounded/observable loop requirements but omits root status and several root prohibitions verbatim. | Coverage asymmetry confirmed; preserve both pending canonical-path decision; then create a single acceptance checklist covering both sets. |
| MH-ARCH-033 | P2 | `architecture/MH-03-event-model.md` — `bd7c50063c518f428217ca2e906c615017f02ae6` | `docs/architecture/mh-03/MH-03-event-model.md` — `330b98cba91125ac6e57e662d4eebeb37b6df00a` | Root defines Command/Event distinction and explicitly forbids Event→Command, Telemetry→Mutation and Recommendation→Mutation; nested defines immutable facts, observer-only consumers and required event identity/type/time/source/correlation/payload fields. | Complementary but unaligned coverage. Merge concepts only after owner confirms canonical document; no event schema/runtime validity asserted. |
| MH-ARCH-034 | P2 | `architecture/MH-03-runtime-dependencies.md` — `7bf2c9db634cfe149f8f6199d2eeae1813499be5` | `docs/architecture/mh-03/MH-03-runtime-dependencies.md` — `115dfbbf8d00b01865c4db4590f44a7f7a5eced7` | Root calls out critical State Authority dependency, initialization order and optional cloud/AI/RAG isolation; nested classifies mandatory/feature/optional dependencies and adds deterministic ordering/cycle blocking/no silent authority promotion. | Asymmetric coverage; combine into traceable dependency invariants after canonical-path decision. |
| MH-ARCH-035 | P2 | `architecture/MH-03-shutdown-sequence.md` — `37d2dad130cb611799191bdbde5b4803adea37bb` | `docs/architecture/mh-03/MH-03-shutdown-sequence.md` — `cef347ea1e6ce02a38283aba4a47ae4353082f30` | Root has explicit PROPOSED status, supervision/event-dispatch stop and resource closure; nested adds readiness false, explicit canonical-state preservation and controlled continuation on service failure, but uses a shorter sequence. | Sequence mismatch in coverage, not proof of an executable defect. Align step ordering and failure semantics before implementation/qualification. |
| MH-ARCH-036 | P2 | `architecture/MH-03-startup-sequence.md` — `87ecefe90f8c0f8c306682d31a8c6f613a2fcfcf9` | `docs/architecture/mh-03/MH-03-startup-sequence.md` — `a2fa93260f13f909c345319252a5b63440265ecc` | Root specifies explicit trust/security initialization and command/event boundaries; nested expands bootstrap/config validation, State Authority under P0-04 and Core Runtime Services under P0-06, but omits explicit status metadata. | Coverage/status asymmetry. Create one ordered startup contract only after canonical authority and decision references are verified. |

**Repository-wide duplicate inventory (static tree snapshot, not a deletion recommendation):** 827 tracked blobs; 24 repeated-basename groups; one identical-blob group consisting of ten intentionally empty `__init__.py` files; no case-insensitive path collisions. Repeated names include 18 root/nested MH-03 pairs, `architecture/mesh/capability.schema.json` vs `schemas/domain/capability.schema.json`, `deploy/com.mediahub.astra.github-agent.plist` vs `ops/launchd/com.mediahub.astra.github-agent.plist`, and `ops/mesh/state.py` vs `runtime/mediahub_runtime/state.py`. Same basename is a candidate classification, not proof of duplication. The empty package initializer group is identical by blob SHA `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` and should not be deleted without import/package semantics review.

**Branch state:** `main` and documentation branch remain diverged (874 ahead / 2 behind at this snapshot). Do not merge/rebase/cherry-pick under the current permission boundary. An integration ledger and owner-approved promotion policy are required before branch convergence.

**Next bounded pass:** review remaining unreviewed MH-03 mirror pairs, then classify the two non-MH-03 schema/state pairs and launchd plist pair by references, ownership and generated/manual status. Do not delete, rename or rewrite normative sources on inference. Qualification remains NOT_PROVEN/BLOCKED; this was static document review only.

### 9.24 Documentation navigation collision repairs (2026-10-14)

- Post-write heading scan found duplicate numeric ID `20.213` in the project map (the health-model entry collided with the earlier evidence-register entry). Rekeyed only the health-model heading to `20.214`; map blob `31b285f02b9490bf1d57ebaaae442c559932cb46`.
- The roadmap still had duplicate numeric H2 IDs `8` and `28`. Preserved the historical P0-07 addendum content and nested it as `### 10.5`; changed the evidence-register review heading `28`→`29`, plan-navigation repair `29`→`30`, and health-model review `30`→`31`. Roadmap blob `a84e04b2ecebb5b66c2ca7b3843bcdd08113672b`.
- These are navigation-only repairs; no technical contract, finding disposition, owner decision or qualification status changed. Final heading scan/read-back is required.


### 9.25 Non-MH-03 repeated-basename classification (2026-10-14)

**Scope:** read-only content inspection of the three remaining non-MH-03 same-basename pairs. This does not claim exhaustive consumer-reference tracing, schema validation, test execution, host inspection, or runtime verification.

| Finding | Priority | Source evidence | Classification and required disposition |
|---|---|---|---|
| **MH-ARCH-037** | **P1; deployment collision risk, actual runtime impact unknown** | `deploy/com.mediahub.astra.github-agent.plist` blob `2cca029b502fd911ec38272871c823a8717ed8fd`; `ops/launchd/com.mediahub.astra.github-agent.plist` blob `d1d8aea99c2303c26e542a3d1c5e54b4596521d0`. | Both declare launchd Label `com.mediahub.astra.github-agent`, but their ProgramArguments and environments differ: one launches a Python agent from a deployment path; the other launches a bootstrap script and sets worktree/state/node variables. If both are installed in one launchd domain, label collision/replacement is possible. Whether either is installed is UNKNOWN. Preserve both; trace package/workflow references and target ownership. Owner/governance must decide whether these are mutually exclusive target-specific manifests or whether labels/targets need governed separation. No host inspection or install occurred. |
| **MH-ARCH-038** | **P2; not established as duplicate** | `architecture/mesh/capability.schema.json` blob `d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c`; `schemas/domain/capability.schema.json` blob `fe80659b570ac58829f10410feb5c700388f87c0`. | Mesh schema ID `mediahub.mesh.capability.v1` describes provider/executable/identity hash/authority/qualification state. Domain schema describes product capability ID/type/status/properties/commands/events/constraints/dependencies/conflicts/safety/discovery state. Same basename, different apparent domain contracts. Keep both; trace references/producers/consumers and document their distinct owners/versioning. Do not merge or rename based on basename alone. |
| **MH-ARCH-039** | **P2; not established as duplicate** | `ops/mesh/state.py` blob `d02780894cfb5d3c0fc7878d57a08fac2e428efc`; `runtime/mediahub_runtime/state.py` blob `a2115b81f52a63feb357e484bd982a6a32641d81`. | Ops module defines node/replica lifecycle transition tables; runtime module defines an abstract `StateAuthority` interface for read/begin/commit/abort/snapshot/restore. Same basename, distinct responsibilities. Keep both; trace imports and confirm the lifecycle helper does not create a parallel product-state authority. Runtime behavior remains unverified. |

**Repeated-basename inventory:** the inspected tree contains 24 groups: 18 root/nested MH-03 families, the three pairs above, and `__init__.py`, `README.md`, and `SKILL.md` groups. Ten files in the `__init__.py` group are identical empty files (blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`); other package initializers are non-empty. Same-name README/SKILL files are context-specific; basename alone does not prove duplication. No case-insensitive path collision appeared in this tree snapshot.

**Updated sequence:** (1) owner/governance decisions for ADMIN-01…05 and MH-03 source model; independent P0-07 D2 review appointment/defer decision; (2) trace MH-ARCH-037 through declared package/workflow references; (3) keep ASTRA G0–G11 BLOCKED / overall NOT_PROVEN while resolving authority, concurrency and trusted-context evidence via approved change control; (4) trace MH-ARCH-038/039 schema and import references; (5) finish remaining MH-03 pairs and inbound references; (6) refresh refs/tree and run any static checks, CI, tests or qualification only after explicit authorization.

**Non-claims:** no actual host-level LaunchAgent collision, schema-consumer validity, import correctness, CI/test health, implementation, qualification or acceptance is asserted. No candidate file was deleted, renamed or promoted.


### 9.26 MH-ARCH-040 — LaunchAgent target/ownership reference pass (2026-10-14)

**Status:** confirmed static manifest divergence; deployment intent and actual host state UNKNOWN. Existing MH-ARCH-037 is refined, not closed.

- Re-read both manifests on `docs/mediahub-chat-tree-map-20261012`: `deploy/com.mediahub.astra.github-agent.plist` blob `2cca029b502fd911ec38272871c823a8717ed8fd`; `ops/launchd/com.mediahub.astra.github-agent.plist` blob `d1d8aea99c2303c26e542a3d1c5e54b4596521d0`. Both use Label `com.mediahub.astra.github-agent`, KeepAlive and RunAtLoad, but they target different execution models.
- Deployment manifest directly runs `/usr/bin/python3 /opt/mediahub/astra/astra_github_agent.py` and sets only `ASTRA_GITHUB_REPO`. The ops LaunchAgent runs `/bin/bash /Users/voktor/astra-work/ops/astra-github-bootstrap.sh`, adds user-specific worktree/state/node values, and points to a bootstrap that fetches `main`, checks out `origin/main`, executes `git reset --hard origin/$BRANCH`, then execs the agent. This is a destructive worktree-reset behavior if that bootstrap is actually run against a worktree containing local changes; no such runtime execution was performed here.
- `deploy/mediahub-astra-github.service` is a separate Linux systemd service (blob `e1962e4afe5db7ac1fcb901344d9f88205de0689`), not a launchd package/install reference. Its existence reinforces that repository contains target-specific deployment assets but does not prove the two plists are intentionally mutually exclusive.
- GitHub code-search API queries for the plist basename/path returned zero results with `incomplete_results=true`; therefore they do **not** establish absence of package/workflow consumers. Workflow directory inventory contains CI/qualification workflows, but this pass did not prove a manifest installer/package consumer. Consumer/reference tracing remains INCOMPLETE.
- Classification: same-label collision is a conditional launchd-domain conflict; actual co-installation, active service state and target ownership are UNKNOWN. Do not rename labels, delete a manifest, or run the bootstrap. Owner/governance must state whether the plists are mutually exclusive per-host deployment profiles or authorize a governed separation of labels/targets. Independently, any use of the bootstrap requires explicit review/authorization of its `reset --hard` semantics.
- No host inspection, installation, workflow run, test, qualification, credentials, runtime execution, or infrastructure/deployment operation occurred. No manifest/source code changed.


### 9.27 MH-ARCH-038 / MH-ARCH-039 — targeted schema and state-import trace (2026-10-14)

**Status:** partial static trace; no duplicate is established. This pass reads declared consumers/producers found in the current docs-branch tree and tests; it does not claim exhaustive textual reference coverage because GitHub code search returned empty results and cannot establish absence.

**MH-ARCH-038 — capability schemas**
- Mesh schema `architecture/mesh/capability.schema.json` blob `d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c` declares `$id=mediahub.mesh.capability.v1`, requiring `schema_version`, `capability_id`, `provider`, `version`, `executable`, `identity_sha256`, `authority`, `qualification_state`; `sandbox` is a property but not required.
- Direct mesh producer/consumer evidence: `ops/mesh/inventory.py` blob `b07e84cb6a5144d90e0a01c79e51239d401b8d57` emits that mesh schema version; `ops/mesh/validators.py` blob `416a7ecaf4add9d0b81f0467cf426d9c7deb3ec7` validates the same field family; `ops/mesh/admission.py` blob `46e92d3c4f9b9865356443403e9ebd34587996cd` consumes the mesh capability record; `ops/mesh/registry.py` imports node transition helper; `tests/test_mesh_capability_inventory_contract.py` blob `cf0d03367e48f360ef6c6981e1bf7b4d798bf322` covers the inventory producer; `tests/test_mesh_p2p_contracts.py` blob `794d4b36ee72428ccdbfb75d7f9df96e0545b8a1` checks the mesh schema ID and required fields.
- Domain schema `schemas/domain/capability.schema.json` blob `fe80659b570ac58829f10410feb5c700388f87c0` has `$id=mediahub://schemas/domain/capability.schema.json` and models product capability status/commands/events/dependencies/safety/discovery. Direct reference evidence found: `tests/domain/test_capability_schema.py` blob `3a062d04f55c1efd8da506db1ca50dbeb599fa67` loads and asserts its identity/enums. No shared producer or consumer between these two schemas was established in the inspected sources. Classification remains separate domain contracts pending broader reference tracing; do not merge/rename.
- Static observation for future contract review, not a qualification result: the mesh schema sets `additionalProperties:false` and declares `sandbox` as an optional property; the hand-written validator’s required set matches the schema’s required fields but does not itself enforce the JSON Schema’s full additional-property/type constraints. This is not yet classified as a defect because no authorized validation/test pass or full consumer-contract analysis was performed.

**MH-ARCH-039 — state modules**
- `ops/mesh/registry.py` blob `7d87ae0faf93f55ebbee1c3140b0a1b9cc20a01a` imports `transition_node_state` from `.state` and calls it from `activate_from_heartbeat`; the helper in `ops/mesh/state.py` blob `d02780894cfb5d3c0fc7878d57a08fac2e428efc` contains only mesh node/replica transition tables and a transition lookup that raises `ValueError` on invalid pairs.
- `runtime/mediahub_runtime/in_memory_state.py` blob `0fbc71369d19e09944ba67a60ccb9df802f30a4b` imports `StateAuthority` from `.state` and implements `InMemoryStateAuthority`; `runtime/mediahub_runtime/state.py` blob `a2115b81f52a63feb357e484bd982a6a32641d81` declares the abstract read/begin/commit/abort/snapshot/restore boundary. Targeted evidence shows different import domains and responsibilities; no direct cross-import from the mesh lifecycle helper into product runtime authority was found in the inspected files.
- Related evidence: `tests/test_mesh_p2p_contracts.py` references mesh transitions; `tests/test_mesh_runtime_contract.py` checks mesh service boundary/default fail-closed text; no tests were executed.

**Limitations / disposition:** current docs branch recursive tree at commit `73fa626723e4cff7b1c888cc1f2e8da461a94055` contains 904 entries (`truncated=false`). This gives complete path inventory for that snapshot, not exhaustive content search. GitHub code search returned zero results for exact schema IDs and `StateAuthority`, so this is not evidence of no other references. No source/schema/test changed; no tests, CI, runtime, installation, host inspection or qualification was performed. MH-ARCH-038 and MH-ARCH-039 remain OPEN / PARTIAL TRACE.


### 9.28 MH-ARCH-041 — MH-03 command-execution mirror comparison (2026-10-14)

**Status:** confirmed content/coverage divergence between two PROPOSED documents; no accepted canonical path is inferred.

- Root source `architecture/MH-03-command-execution.md`, blob `b9197759e70107f1be5968e8669288d991360003`, states `Command → Validation → Authorization/Policy → Consumer Contract → State Authority → Canonical Mutation → Event → Observers`. It explicitly rejects direct mutations, missing/invalid authorization, malformed/ambiguous commands, stale transactions and private authoritative stores.
- Nested source `docs/architecture/mh-03/MH-03-command-execution.md`, blob `8a9e1066f00cf9a7a3128c00eada857b18cef32f`, states `Input → Integration/Capability Boundary → Validation → Policy/Authorization → P0-05 Consumer Boundary → State Authority → Canonical Mutation → Event → Observers`. It additionally names UI/API, AI, plugin, device, cloud and event/telemetry bypasses and requires explicit context/bounded inputs.
- The core sole-State-Authority/fail-closed intent aligns, but the root sequence omits the nested document's explicit Integration/Capability Boundary and P0-05 Consumer Boundary, while the nested sequence adds steps and scope. This is a material contract-coverage asymmetry because the consumer boundary is an architecture invariant; it is not evidence that runtime execution currently bypasses it.
- `architecture/MH-03-index.md` blob `b2d2eeb1b89117d10605c231e79378eebc437c5f` lists the root command-execution file as required, but the index itself is PROPOSED and says governance/compatibility reviews remain required. That listing is not acceptance evidence and does not resolve whether the nested file is a mirror, elaboration, or historical copy.
- **Disposition:** preserve both files. Owner/governance must confirm the canonical source/path and whether both boundary steps are mandatory in the accepted sequence before any reconciliation. No implementation change, deletion, rename or status promotion.
- **Verification boundary:** current docs branch tree at `ba8c6016101a7a0b9a6d69107567b58ada25a164` contains 827 blobs, `truncated=false`; this is a complete path inventory for that snapshot, not exhaustive textual inbound-reference coverage. No tests, CI, qualification, runtime/host inspection, installation, deployment or branch integration occurred.


### 9.29 MH-ARCH-042 — MH-03 acceptance-criteria mirror divergence (2026-10-14)

**Status:** confirmed criteria/coverage divergence between two PROPOSED documents; no acceptance or canonical-source authority inferred.

- Root `architecture/MH-03-acceptance-criteria.md`, blob `e96adaac2eb52e2f8058cc889485ec982bf606e5`, declares `PROPOSED / NOT ACCEPTED`. Its acceptance checklist includes MH-1/MH-2, P0-03/P0-04, lifecycle, authority path, services/dependencies, command/event, failure/recovery, health/observability, security/trust, historical reconciliation and contradiction review. Its acceptance condition explicitly requires no unauthorized mutation path, no shadow State Authority, coherent deterministic offline-first core, and explicit classification of open governance issues.
- Nested `docs/architecture/mh-03/MH-03-acceptance-criteria.md`, blob `eefb645d89c7c3046636d8344515aa02b7ccebe3`, requires P0-03/P0-04/**P0-05/P0-06**, adds evidence/decision register review, and states that Runtime must start/live/coordinate/degrade/stop unambiguously while State Authority remains the sole canonical mutation authority. It separately requires governance approval for PROPOSED → ACCEPTED and a separate freeze decision.
- The criteria overlap substantially, but the root checklist omits explicit P0-05/P0-06 reviews and evidence/decision-register review that the nested checklist includes. These are material gate-coverage differences. Conversely, the root states several explicit acceptance outcomes more directly. Neither text proves that any gate has actually passed.
- Both files remain PROPOSED/unaccepted. The root index is also PROPOSED; path listing alone cannot determine whether the nested file is an elaboration, mirror, or superseded artifact.
- **Disposition:** preserve both. Owner/governance must determine the canonical source and resolve the acceptance-gate set before either file is reconciled or any acceptance status changes. Do not infer acceptance from document presence.
- **Verification boundary:** docs branch tree at `2f3724adcf8b3e6ea10d83ef2ca7c2f04cdf1610` had 827 blobs, `truncated=false`; this proves path inventory for that snapshot, not exhaustive textual references. No tests, CI, qualification, runtime/host inspection, installation, deployment or branch integration occurred.


### 9.30 MH-ARCH-043 — MH-03 runtime-observability mirror divergence (2026-10-14)

**Status:** confirmed complementary coverage asymmetry between two PROPOSED documents; direct contradiction and runtime behavior are not proven.

- Root `architecture/MH-03-runtime-observability.md`, blob `aa33cd18290bf486b19fad08f3a377aa5ed7a298`, defines logs/metrics/health/diagnostics/traces, explicitly says diagnostics may produce observation/alert/recommendation, and requires any mutation request to re-enter the governed command → policy/authorization → Consumer Contract → State Authority path. It calls out lifecycle transitions, dependency failures, degraded state, recovery attempts and authority-path failures as diagnostic targets, without unrestricted credential exposure or trust-boundary bypass.
- Nested `docs/architecture/mh-03/MH-03-runtime-observability.md`, blob `f7fba8708bc57eb8baa2d8ecc866fb58d18c9d6b`, explicitly characterizes an observer plane as non-mutating, requires collection/output to be bounded and sanitized, enumerates observation/alert/recommendation outputs, and explicitly names P0-05 in the operational response path. It expressly prohibits disclosure of credentials, secrets, private material and unnecessary personal data.
- The core invariant aligns: observability is not a mutation authority, and operational response must re-enter governed authorization/state handling. The root version is more explicit about which runtime failures/transitions must be diagnosable; the nested version is more explicit about bounded/sanitized collection and privacy categories and names P0-05 directly. These are material coverage differences, not evidence of an actual telemetry-to-state bypass.
- Both documents remain PROPOSED. The root MH-03 index is also PROPOSED and does not independently authorize canonicalization.
- **Disposition:** preserve both files. Owner/governance must select a canonical source or synchronized-view policy before crosswalking diagnostic coverage, sanitization/privacy requirements and the exact mandatory command path. Do not promote status or infer implementation/qualification.
- **Verification boundary:** refreshed recursive tree at docs branch HEAD `8f499d2c3785ec22cfea61e03a2087c7ce69b33e` contains 904 entries with `truncated=false`. This is complete path inventory for that commit, not exhaustive content/reference proof. No tests, CI, runtime/host inspection, installation, deployment, qualification or branch integration occurred.


### 9.31 MH-ARCH-044 — MH-03 service-boundary mirror review (2026-10-14)

**Status:** confirmed asymmetric explicitness between two PROPOSED documents; no direct contradiction, accepted canonical source, or runtime defect is established.

- Root `architecture/MH-03-service-boundaries.md`, blob `02672aa1c377d04a3a7e0a7cff5b767a89ee0fcb`, uses a responsibility/authority-restriction table for Runtime Coordinator, Lifecycle Manager, Dependency Manager, Service Supervisor, Command Executor, Event Dispatcher, Health Manager, Configuration Manager, Recovery Manager and Observability Adapter. It explicitly says logical boundaries do not require separate processes, containers or specific technologies.
- Nested `docs/architecture/mh-03/MH-03-service-boundaries.md`, blob `cb9e5800d20ab3ee463bc30446419c95d556a87c`, covers similar roles but explicitly states all canonical-state access remains through P0-05/P0-04, service supervisors cannot self-grant capabilities, configuration remains within P0-07 scope, and recovery actions must be policy-approved. Its role descriptions also combine liveness/readiness/failure/restart in the supervisor and call out event-to-command prohibition.
- The shared invariant aligns: runtime coordinates and does not become canonical mutation authority. The differences are explicitness/coverage, not proof of a runtime bypass. Both sources are PROPOSED; `architecture/MH-03-index.md` is also PROPOSED and cannot settle canonical-path authority.
- **Disposition:** preserve both documents unchanged. Owner/governance must select a canonical source or synchronized-view policy. After that, produce a clause-level crosswalk covering each service role, capability/lifecycle authority, P0-05/P0-04 access path, policy-bounded recovery and the principle that logical boundaries do not prescribe process topology. No renames, deletion, acceptance promotion or implementation change.
- **Verification boundary:** static reading of the two files and the root index only. Current repository branch state was rechecked immediately before this pass; `docs/mediahub-chat-tree-map-20261012` is diverged from `main` by 917 commits ahead / 2 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No tests, CI, runtime/host inspection, installation, deployment, qualification or branch integration occurred.


### 9.32 MH-ARCH-045 — explicit route mode / local-only contract gap (2026-10-14)

**Status:** route mode is absent from the inspected gateway path; mapping to the specifically named LOCAL_ONLY client route and any live runtime use remain OPEN / NOT VERIFIED.

- Main source runtime/mediahub_runtime/astra_gateway.py, blob 10985e4ad8f682313d08e7492ecc1856a8bce20f: the inspected AstraTaskRequest does not expose an explicit route-mode field; run() labels tasks cloud_first / cloud_first_local_extension and calls the orchestrator without a route-mode argument.
- Main source runtime/mediahub_runtime/cloud_orchestrator.py, blob 24c28197df7baca49abd81956752a7a5092506d9: default candidate construction lists configured/admitted cloud routes first and appends local routes when local extension is allowed. Execution may continue to later candidates after a provider error. This path does not implement a clear LOCAL_ONLY request policy; merely disabling local extension would still permit cloud routes.
- Accepted target architecture architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md, blob e549692f207fbc91d9b9b9b92b8e665404f07290, requires a distinct local-only mode, fail-closed when the local endpoint is unavailable and no silent cloud fallback in that mode.
- **Assessment/disposition:** the inspected gateway/orchestrator path lacks explicit LOCAL_ONLY semantics, but the precise call-path relationship to the Claude Code/FCC local-only target clause is not yet established. This is a source-level design gap and potential privacy/egress risk, not proof of a production leak or a claim that all routes ignore a separate upstream policy. Owner/architecture review must specify task route mode, data classification, permitted route set, provider/model evidence and same-policy failover. If this path serves LOCAL_ONLY work, exclude all cloud candidates and fail closed on local unavailability; CLOUD_ALLOWED may use only explicitly admitted providers. Do not patch runtime or change a normative contract in this documentary pass.
- Related candidate assessment: [MEDIAHUB-AUTONOMOUS-AGENT-ECOSYSTEM-SURVEY-2026-10-14.md](MEDIAHUB-AUTONOMOUS-AGENT-ECOSYSTEM-SURVEY-2026-10-14.md). No code was installed/copied; no tests, provider/model calls, host/runtime inspection, infrastructure changes, deployment or qualification occurred.

### 9.33 Autonomous agent ecosystem survey — candidate-only (2026-10-14)

- Added [MEDIAHUB-AUTONOMOUS-AGENT-ECOSYSTEM-SURVEY-2026-10-14.md](MEDIAHUB-AUTONOMOUS-AGENT-ECOSYSTEM-SURVEY-2026-10-14.md) based on targeted GitHub repository metadata and official upstream documentation available on 2026-10-14. This is not an exhaustive scan of all GitHub repositories and does not claim an upstream candidate has passed qualification.
- Primary recommendations: evaluate OpenHands Software Agent SDK as a bounded coding worker; evaluate MCP as a tool-interface protocol behind MediaHub-owned authorization; retain current Ollama and target-gated llama.cpp/ONNX choices pending route/hardware evidence; consider OpenTelemetry Python and Inspect AI only in authorized instrumentation/evaluation stages.
- Defer/condition other candidates: OpenShell's upstream maturity sources are inconsistent—latest support matrix identifies v0.1.4 and recommends stable-release production use, while Security Best Practices/support-page banners retain alpha/no-production wording and the v0.1.0 milestone says the alpha designation was removed. Treat it as candidate-only until an exact release and matching security documents are pinned and reviewed; macOS support is limited to Apple Silicon. Temporal only after a proven durability gap; A2A only for an actual remote interoperability requirement; OPA only after policy-ownership governance; LiteLLM due overlap with the existing orchestrator and licence-path review. Do not adopt whole-agent projects as the Jarvis/ASTRA authority plane.
- All recommendations remain RESEARCH / CANDIDATE ONLY / NOT ACCEPTED / NOT IMPLEMENTED. Existing Component Manifest 2.0, Baseline 2.0, authority contracts and Contour A/B gate remain unchanged.



### 9.34 MH-ARCH-046 — Ollama model identity / result-provenance source trace (2026-10-14)

**Status:** confirmed static mismatch in the inspected construction path; actual deployed behavior/use is not known.

- `runtime/mediahub_runtime/astra_gateway.py`, blob `10985e4ad8f682313d08e7492ecc1856a8bce20f`: `OllamaExecutor.model` is class-level `qwen2.5-coder:3b`, and its request payload uses `self.model`.
- `runtime/mediahub_runtime/cloud_orchestrator.py`, blob `24c28197df7baca49abd81956752a7a5092506d9`: the default Ollama `ProviderRoute` declares `model_env="MEDIAHUB_OLLAMA_MODEL"`; plural configured models are also expanded. But `_executor_for` falls through to the preconstructed executor held in `self._executors` rather than binding the route's selected model into the Ollama instance. The default `AstraGatewayRuntime` constructs the orchestrator with `executors={"ollama": OllamaExecutor()}`.
- `AstraGatewayRuntime.run` records `decision.model or "unspecified"` in its selected-provider/result path, which can therefore differ from the executor's hard-coded payload model. The inspected `tests/ai/test_cloud_orchestrator_failover.py`, blob `c66b63b158c545ae627c596791381b83ef902c59`, has route/failover assertions but no explicit Ollama selected-vs-actual model identity assertion; it was read only and not run.

**Disposition:** future design/implementation must resolve a single effective model identifier at route admission and carry it through executor construction, qualification, event and result evidence. Add default-model, configured-model and mismatch-negative checks only after explicit test authorization. Do not claim the defect affects an active deployment absent runtime evidence.


### 9.35 MH-ARCH-047 — P0-07 to P0-05 trusted-context binding gap (2026-10-14)

**Classification:** confirmed targeted static contract gap in the inspected authorization seam; system-wide absence and deployed impact are not established.

- architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md (main blob 8d831c2a8fa333977dd86524099568bae2a8db0e) defines a richer trust chain: boot/runtime trust context → authenticated principal → device/workload identity → capability/policy evaluation → authorized command → Consumer Contract → State Authority. It requires auditable identity, policy/version and correlation metadata where applicable.
- runtime/mediahub_runtime/authorization.py (main blob 4d8df5d3c1c26f7f133a8093cd270635b085f4d5) exposes AuthorizationContext(principal, capability) and an explicit grant check on (principal, capability, operation). The targeted module itself does not carry a verified issuer, device/workload binding, request/correlation identity, policy revision, expiry or revocation proof. This observation is limited to the inspected seam; it does not establish that every caller/path lacks separate upstream checks.
- runtime/mediahub_runtime/consumer_boundary.py (main blob 98bf2da9cea85da2c82145b4baef417c20b9ae73) accepts this AuthorizationContext as the request context. schemas/identity/identity-boundary.schema.json (main blob 1d085bb1f2c458faaeff23bd92d83aa5d1bd3879) defines identity/correlation identifiers as a separate schema, but the inspected authorization dataclass does not itself bind or validate them. The connection between a trusted issuer, schema validation, authorization evaluation and consumer request remains unproven in this targeted trace.
- Cross-branch refinement (read-only): `integration/p0-07-runtime-reconciled` HEAD `b54f5c389513998dfb6e6e362b62ff5d07430995` contains the same `AuthorizationContext(principal, capability)` seam (blob `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`) and P0-05 boundary (blob `23b95f1b37cb35e311b61e3babcca4bd1aea9596`). Its `docs/architecture/P0-07-p0-05-mutation-adapter-contract.md` (blob `22b8e1897e124578e66c8d619b3e8eaf41f69a88`) explicitly labels implementation BLOCKED — GOVERNANCE/API GAP and says no approved mapping may replace independent P0-04 authorization. `docs/architecture/P0-07-authorization-reconciliation.md` (blob `04381ce6e223b8632ec15d17e475b56fe1ab8772`) preserves P0-07 domain authorization and P0-04 transaction authorization as distinct requirements. This corroborates the governance block and does not prove a deployed bypass or justify changing frozen contracts. Branches inspected: `implementation/p0-05-consumer-boundary` HEAD `c872899a969fb9b947d638f507cd8794e9f86cab`; `implementation/p0-04-in-memory-state-authority` HEAD `1d5c34081d1caf16118ab8efef21ce19686e03a9`.
- architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml (main blob 1d3ac25e7817f365807ad85d0d7c9007bd48bebf) requires independent evidence/qualification stages; generated docs/qualification/CURRENT-TRUTH.generated.md (main blob 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731) still marks G0–G11 BLOCKED / overall NOT_PROVEN. The manual-only .github/workflows/mediahub-p0-07-verification.yml (blob 7fb80f402b4792b6a77cf8a4aad83d1ee5209789) targets a self-hosted runner and was not dispatched; it is not evidence that P0-07 passed.

**Required disposition:** keep P0-07/P0-05 blocked. The owner/governance review must identify the trusted context issuer and canonical binding mechanism, define the exact claims and freshness/revocation checks, trace the validated context through policy evaluation and Consumer Boundary, and assign an independent D2 reviewer. Preserve existing DEC-DEV-02 lifecycle ownership and DEC-DEV-05 egress-policy decisions; do not create a second policy or State Authority. Only after design approval and explicit authorization may implementation/tests/qualification be planned. No code, tests, workflow, credentials, host/runtime, installation or deployment were changed or exercised in this pass.


#### Crosswalk clarification (2026-10-14)

This MH-ARCH-047 source trace corroborates, rather than duplicates as a new defect, the already-existing map-selected proposal `docs/checkpoints/P0-07-D2-TRUSTED-CONTEXT-AUTHORITY-LIFECYCLE-PROPOSAL-2026-10-13.md` (documentation-branch blob `39400abce88da7ea54be7d9d7505f215eba43408`). That proposal already records the bounded trusted-context/lifecycle gap and the owner-selected option B: prepare a proposal for governance review only. MH-ARCH-047 is retained as a traceability identifier for this pass; it does not create a second issue, decision, authority, or implementation authorization.
