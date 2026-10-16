# MediaHub OS — Unified Contract and Project Traceability Matrix, Wave 01
Date: 2026-10-16
Repository: https://github.com/VlDMlNSh/mediahub-os
Working ref: docs/mediahub-chat-tree-map-20261012
Status: ANALYSIS / PROPOSED CONTROL ARTIFACT / NOT ACCEPTED AS NORMATIVE
Scope: repository-wide control-plane scan using connected GitHub repository, branch search, recent commit search, file retrieval, and branch comparison. This pass is broad but not exhaustive: the branch API is paginated and only sampled pages and selected primary files were inspected. No claim of complete all-branch or all-file census is made.

## 1. Executive result

The fastest safe route to a single verifiable project contract is a **traceability control matrix**, not a new replacement mega-specification. Preserve accepted sources and branch history; map each requirement/decision/contract to its owner, canonical source/ref/SHA, downstream dependencies, evidence, and acceptance gate. Resolve conflicts through change control rather than silently merging branches or normalizing divergent source documents.

Current canonical functional authority: `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, explicitly ACCEPTED and superseding Baseline 1.0 as current functional reference. Baseline 1.0 remains historical provenance.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 2. Live GitHub evidence collected

- Repository is public, default branch `main`, repository ID `1350132846`; the connected GitHub integration reports admin/maintain/push permissions.
- Recent default-branch commit search returned `b45324009ac3aa65322a702c28069b12190bc4b8` (2026-10-16 15:41:49 UTC), message: “Add safe Gemini API error diagnostics and use Flash-Lite”. Adjacent commits include `c8890ae7f0d7ce1521f65a819d5ad564acb3f590`, `bc7da440a74d0b94df3b4d9ec4b15772df7e44e9`, `66040934216c1e23ac169b4f94bff9ecbbfca8c1`, `ee5e2222e7d28c5a76334000e502c3fac1af9550`, and `506372737aeee145394a16705bf403d7aa975210`. This is commit-search evidence, not a full commit graph.
- Live compare `docs/mediahub-chat-tree-map-20261012...main`: status `diverged`; docs ref ahead by 1,640 commits and behind by 10 commits; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`; documentation-ref HEAD at that comparison: `f75d49b00d6f3cbbcf316e4d97b4e995b118c16f`; main HEAD: `b45324009ac3aa65322a702c28069b12190bc4b8`. Do not integrate branches as part of this pass.
- The compare surfaced main-only changes including `.github/workflows/gemini-readonly-audit-retry.yml`, `.github/workflows/gemini-readonly-audit.yml`, two Contour A source-reconciliation reports, and a modification to `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`. The Baseline 1.0 change must remain separate from canonical Baseline 2.0 unless approved via change control.
- Branch search returned more than 100 names on its first page and a continuation page. Examples span architecture, MH-04 work, ASTRA/GOLD, provider qualification, node-specific historical branches, and P0-07 work. Branch-name presence alone does not establish currency, acceptance, or deployability.
- Open PR search surfaced at least PR #297 (integrated master guide) and PR #291 (queue dispatch separation), as well as PR #295 (executor PATH fix). PR descriptions contain historical/local evidence and explicit qualification caveats; current state and exact head/base SHAs require individual PR retrieval before action.
- Bootstrap instruction blob SHA on the documentation ref: `a4bf8d7eb162a8bfaa103d0889ea706a07390107`.
- Current map header states its latest confirmed incremental update is 2026-10-16 §20.317 and explicitly marks the map as inventory, not full acceptance.
- Continuation checkpoint contains historical HEAD values from prior observations. Those values are not substituted for a fresh live HEAD. The live compare above is the current branch relationship evidence gathered in this pass.

## 3. Authority and boundary contract

| ID | Contract area | Canonical rule/source | Current status | Verification required |
|---|---|---|---|---|
| GOV-01 | Functional baseline | Baseline 2.0 on main, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | ACCEPTED canonical reference | Requirement-level links and change-control lineage |
| GOV-02 | Baseline 1.0 | `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` | Historical provenance | Review main-only edits for provenance and avoid silent import into B2 |
| GOV-03 | Contour separation | Master Roadmap 1.0, §0 | OWNER-DIRECTED plan | Contour A deployment + independent acceptance before Contour B development |
| AUTH-01 | Product mutation | Product State Authority is sole canonical product-state mutation authority | Architectural invariant | Verify every mutation route against P0-03…P0-07 contracts |
| AUTH-02 | Smart Home | Home Assistant Core within approved Smart Home boundary | Architectural invariant | Confirm consumer adapters and domain authority mappings |
| AUTH-03 | Engineering workflow | Jarvis coordinates corporation-level missions; ASTRA A0 owns ASTRA-internal workflow state; Product State Authority owns product mutation | DEC-DEV-02 Option C owner-approved per roadmap | Reconcile main-side broad wording through approved change control |
| SEC-01 | Local-first / egress | Least privilege, fail-closed authorization, explicit provider/egress policy | Required invariant | Evidence-backed route, issuer, destination, fallback, retention and logging matrix |
| LIFE-01 | Lifecycle truth | IDEA → DESIGN → IMPLEMENTED → TESTED → VERIFIED → QUALIFICATION CANDIDATE → QUALIFIED → RELEASED → DEPLOYED → OBSERVED → PRODUCTION ACCEPTED | Required status separation | Each transition needs criteria, actor, immutable evidence and authority |
| EVID-01 | Evidence binding | Claim → source path → ref → commit SHA → blob SHA → status → verification date | Required traceability format | Every matrix row must be source-backed; unknown stays UNKNOWN |
| BR-01 | Branch control | No merge/rebase/cherry-pick without explicit permission | Active restriction | Compare each proposed source and target before any integration |

## 4. Critical cross-project gaps and risks

1. **Branch divergence is material.** The docs ref and main are divergent (10 ahead / 1,640 behind in the live compare orientation). Treat each branch as a separate evidence context. Never use a branch-only document as canonical main truth without explicit adoption.
2. **Baseline provenance risk.** Main contains a large edit to Baseline 1.0 in the compare result. Baseline 2.0 remains the accepted functional reference; inspect that Baseline 1.0 diff independently before any downstream use.
3. **Contract authority is fragmented by domain.** The map is a navigation index, the roadmap sequences work, the baseline defines accepted functionality, domain contracts define authority/interfaces, and evidence records establish state. A single matrix should cross-link these roles rather than replace them.
4. **ASTRA A0 ingress remains a proposed contract family.** Recent docs-branch checkpoint entries WB-14AA through WB-14AE indicate transport-neutral proposals and governance gaps. Issuer/verifier lifecycle, authentication/integrity profile, durable admission/idempotency, freshness/replay, probe response, health vocabulary mapping and A0 lifecycle transitions remain open. Keep proposal-local IDs non-normative until registry collision review and owner acceptance.
5. **P0-07 is a product-mutation hard gate.** Keep the engineering mission route Jarvis → A0 distinct from product mutation via P0-07 → P0-05 → P0-04. Do not apply product-mutation gates indiscriminately to all engineering ingress, and do not bypass them through ASTRA.
6. **Evidence and runtime truth are separate.** Workflow definitions, branch commits, old host identifiers, PR descriptions, and generated reports are not current runtime evidence. Do not infer healthy controllers, current provider routes, or qualification from static artifacts.
7. **Gemini workflow changes are present on main.** Recent commit search shows read-only audit workflows and safer API diagnostics. Static GitHub evidence alone does not prove an API call returned HTTP 200 in the latest run. Runtime/workflow execution is outside this pass's authorization.
8. **Historical node identity contamination remains a map-level risk.** Old node names appear in branch names and prior audit history. Their presence is historical evidence only; target topology must derive from the approved greenfield inventory and current evidence, never from branch names.

## 5. Proposed single project matrix schema

Each row should use these mandatory columns:

`matrix_id | requirement_or_decision_id | domain | statement | authority_type | status | canonical_source_path | ref | commit_sha | blob_sha | source_owner | implementation_owner | upstream_dependencies | downstream_consumers | interface/schema_id | security/data-egress | acceptance_criteria | evidence_uri/digest | verifier | last_verified_utc | conflict_id | next_action | gate`

Rules:
- Preserve existing IDs; run collision checks before assigning stable IDs.
- Distinguish ACCEPTED, OWNER-APPROVED, PROPOSED, OPEN, BLOCKED, UNKNOWN, IMPLEMENTED, TESTED, VERIFIED, QUALIFIED, RELEASED, DEPLOYED, OBSERVED and PRODUCTION ACCEPTED.
- A source row can be authoritative for one scope while implementation authorization remains absent.
- One claim may reference multiple sources; record conflicts explicitly instead of choosing a winner silently.
- All evidence must bind to immutable refs and SHAs. Branch names and mutable URLs alone are insufficient.
- Keep source-of-truth documents unchanged during inventory. Change only through a scoped change request with explicit owner, impact analysis and acceptance evidence.
- Every matrix item must have one accountable decision owner, one source owner, one implementation owner (or explicitly N/A), and a defined acceptance authority. Role mapping may remain UNKNOWN pending governance appointment.
- Matrix completeness is measurable: row count by domain; % with source+SHA; % with acceptance criteria; unresolved conflict count; open decision count; dependency cycles; orphan requirements; duplicate IDs; stale evidence count.

## 6. Recommended execution sequence for the shortest path to one verifiable contract

**Wave 01 — repository control inventory (this artifact):** record live branch divergence, primary authorities, risks and matrix schema. Status: analysis artifact only.

**Wave 02 — canonical source registry:** enumerate every accepted baseline, governance decision, contract/schema registry, security policy, evidence index and acceptance gate on its owning ref. Capture exact commit/blob SHA and owner. Avoid scanning every implementation file before this registry exists.

**Wave 03 — requirement-to-contract crosswalk:** trace Baseline 2.0 requirements and owner decisions into MH-01…MH-25, P0-03…P0-07, ASTRA/Jarvis, provider routing, privacy, mobile and operational qualification. Mark missing edges and conflicts.

**Wave 04 — conflict ledger and decision packets:** one stable conflict ID per disagreement, exact source spans/SHAs, impact, safe compatible interim rule, accountable owner, and required disposition. Do not modify normative sources pending disposition.

**Wave 05 — schema/API ownership matrix:** for every interface, identify producer, consumer, issuer, verifier, authority, persistence/idempotency, freshness/replay, cancellation/fencing, error model, evidence and versioning. Keep candidate schemas non-normative until accepted.

**Wave 06 — acceptance/evidence matrix:** map every release/Contour A readiness gate to criteria, evidence artifacts, independent verifier, freshness, target identity and decision authority. Contour B remains gated on independently accepted Contour A.

**Wave 07 — controlled documentation convergence:** update the map and checkpoint with verified links and status; keep branch integration separate and owner-authorized. Then produce one generated/maintained matrix view from the registry, with source documents remaining authoritative.

## 7. Bounded-pass completion record

Completed: fetched current bootstrap, map, continuation checkpoint, roadmap and Baseline 2.0; enumerated repository metadata; sampled branch pages; inspected recent commit search; inspected open PR search; compared documentation ref against main; recorded the proposed control matrix and the highest-impact gaps.

Not performed: exhaustive all-branch/all-file traversal; fetching every PR head/base or all workflow run logs; model/provider invocation; credentials use; host/runtime inspection; test or qualification execution; installation; infrastructure change; deployment; migration; merge/rebase/cherry-pick; modification of Baseline 2.0 or other normative contracts.

Next safe task: Wave 02 canonical source registry and per-domain source ownership census, starting with Baseline 2.0, P0-03…P0-07, MH-12 security, MH-13 privacy, ASTRA GOLD qualification truth, and the Jarvis→A0 ingress proposal set. Keep branch divergence explicit and do not promote proposal material to accepted contract.
