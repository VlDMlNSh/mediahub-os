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


---

## Wave 02 — Contour A clause-level acceptance matrix (2026-10-17)

- Working ref for this update: `docs/mediahub-broad-contour-a-wave105-20261017`
- Status: **SOURCE-BOUND CONTROL MATRIX / PROPOSED / NOT ACCEPTED AS NORMATIVE**
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- This section extends the existing cross-domain traceability register; it does not create a second integration register or amend Functional Baseline 2.0.
- Source baseline: Baseline 2.0 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.

### Status vocabulary

- **PASS-SCOPED** — evidence demonstrates only the exact source/test scope stated; not runtime acceptance.
- **OPEN** — a normative interface, decision, or required evidence is still missing.
- **BLOCKED** — downstream implementation/qualification must not proceed until named upstream gates close.
- **UNKNOWN** — reviewed sources do not establish the value; do not infer or silently default it.
- **PROPOSED** — engineering recommendation awaiting the appropriate authority's approval.

### Acceptance rows

| Matrix ID | Required invariant / acceptance condition | Source-of-truth and inspected revision | Evidence currently available | State | Close-out evidence / accountable gate |
|---|---|---|---|---|---|
| CA-AUTH-01 | Jarvis coordinates missions; ASTRA A0 owns only ASTRA-internal engineering workflow state; MediaHub Product State Authority alone mutates canonical product state. No adapter, worker, model, queue or verifier inherits product authority. | Baseline 2.0 `main` blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; architecture contract `docs/checkpoints/MEDIAHUB-OS-VERIFIABLE-ARCHITECTURE-CONTRACT-01.md@docs/mediahub-chat-tree-map-20261012`, blob `c248956417cc61d66c968a4c58a56e799f653354`; Issue #301. | Role separation is recorded in the readiness and source-reconciliation documents. | OPEN | Independent clause-level review across authority consumers and negative tests proving denied product-state mutation from A0/worker paths. Authority owner remains the decision gate. |
| CA-SCHEMA-01 | All three proposed v0.2 schemas meta-validate against JSON Schema Draft 2020-12; format assertions enabled; positive and malformed/nested-negative cases have deterministic outcomes. | Candidate `contour-a-schema-validation-consolidation-wave98-20261017`, head `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`; validator blob `02c326da8cf90d2e5253dff3c1a5b90d72f6e18d`. | Run [39058425661](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39058425661), job `117471084337`: 3/3 schema meta-validations, 3/3 positive fixtures, 179/179 negative cases rejected, zero reported failures; artifact `12110676230`, SHA-256 `7957517179ce91c469e851996d2141410640c008da90c6f0c35f879ac185bb3c`. | PASS-SCOPED | Independent reviewer confirms schema source pins, fixture quality, validator implementation and artifact provenance; refresh CI if source or base changes. No live admission claim follows from this row. |
| CA-SEM-01 | Task envelope, agent registry and evidence manifest agree on task/agent/provider/model identity, source commit, schema references/digests and policy provenance; inconsistent combinations are rejected. | Candidate head as above; semantic validator blob `7c69f478301360930e9e2ff341692cf2676b16cd`. | Same run recorded 26/26 synthetic semantic negative fixtures rejected. The validator explicitly characterizes itself as an engineering test profile and does not resolve live authority. | PASS-SCOPED / OPEN FOR LIVE REFERENCES | Preserve negative fixtures; add independent review and an authorized integration test against registered issuer/grant/policy references without using production secrets. |
| CA-A0-01 | Ingress has a named caller identity, accepted endpoint/protocol/version, authenticated transport, message integrity and an issuer whose trust root, signing/verification profile, audience, key rotation, expiry and revocation are explicit. | A0/MH-12 source trace `docs/checkpoints/MEDIAHUB-A0-LIFECYCLE-MH12-CAPABILITY-ISSUER-SOURCE-TRACE-WAVE-07-2026-10-15.md@docs/mediahub-chat-tree-map-20261012`, blob `49ca0b69737bf8d44fe3a42daa47fd9157c9097d`; MH-12 source SHA cited in trace `cf4ebfd5bf471ca676f075c51d3a24906504e490`. | Source trace explicitly reports ingress identity, issuer profile and external caller/wire contract as unestablished. | BLOCKED / UNKNOWN | Approve the protocol and trust-root decision through governance; provide source paths/SHAs, wire schema, issuer-verifier compatibility tests, invalid-signature/wrong-audience/expired/revoked-token rejection, key-rotation evidence and audit linkage. Do not invent token format. |
| CA-A0-02 | Lease and claim handling fences stale workers; renewals, expiry, cancellation, retries, idempotency and recovery are deterministic and auditable. A lease timeout alone is not fencing; never claim global exactly-once execution without evidence. | A0/MH-12 source trace blob `49ca0b69737bf8d44fe3a42daa47fd9157c9097d`; governance YAML on `main`, blob cited by trace `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`; ASTRA reference architecture `main`, SHA `7be5fadd3055642e7823c7233f90e978a87e5366`. | Governance documents lease TTL 600 seconds and max three concurrent autonomous claims; source trace says fencing generation, idempotency-key scope, replay response and cancellation races are not established at Jarvis↔A0 boundary. Values are documentary, not runtime evidence. | BLOCKED / OPEN | Accept state machine and persistence contract; test stale-generation commit rejection, duplicate delivery, lease expiry/reclaim, cancellation races, bounded retry and recovery-to-BLOCKED; publish run/job/artifact digests. |
| CA-CAP-01 | Authorization binds principal, issuer, operation, resource/target, scope, constraints, provenance, lifetime and revocation; missing, malformed, stale, ambiguous or unavailable authorization resolves to deny/quarantine. | MH-12 Security Architecture `main`, blob cited by A0 trace `cf4ebfd5bf471ca676f075c51d3a24906504e490`; A0 trace blob `49ca0b69737bf8d44fe3a42daa47fd9157c9097d`. | Required semantics are source-traced; the concrete capability representation and A0 verification procedure are not selected/accepted. | OPEN | Independent security review of a selected source-pinned implementation and positive/negative policy vectors; record revocation propagation, failure mode and no-fallback evidence. |
| CA-R06-01 | Security audit is distinct from ordinary logging and from state authority. Capture bounded intent/decision/outcome metadata with actor, time, operation, capability context, policy decision, result and security context; integrity, reader access and export are controlled. | R-06/MH-12/MH-13 crosswalk `docs/checkpoints/MEDIAHUB-P0-07-D2-R06-MH12-MH13-AUDIT-PRIVACY-CROSSWALK-WAVE-05-2026-10-16.md@docs/mediahub-chat-tree-map-20261012`, blob `099ad9f6a85bd4764dd16ccbfa9695c2abd6d5bd`. | Technical direction is documented; no accepted runtime sink, registered event schema or durable emission guarantee is evidenced. | BLOCKED | Governance accepts event taxonomy and sink contract; tests verify bounded fields, integrity, access policy, failure semantics, durable evidence and no raw payload by default. Audit is not Product State Authority. |
| CA-R06-02 | Audit/privacy controls explicitly determine data classification, minimization, purpose, retention/deletion, residency, clock source/skew, durability and operation-specific behavior during audit unavailability. | Same R-06 crosswalk blob `099ad9f6a85bd4764dd16ccbfa9695c2abd6d5bd`; MH-13 governance/reconstruction SHAs `e732ff9cacbc9c1189bd83306cdff30906326cf0` and `8c66fb49bbe011d8ef5dd78287c72efdad77a8fe` cited in source. | Exact retention periods, legal/residency mapping, approved clock and sink availability policy remain unknown. | UNKNOWN / BLOCKED | Named governance decision resolves each field; acceptance tests verify redaction, retention/deletion, access, export, timestamp ordering/skew and fail-closed/containment behavior per operation. |
| CA-TARGET-01 | Exact clean target profile has an accountable owner/approval, hardware/OS/runtime, network, workspace/isolation, storage, resource limits, allowed destinations, support lifecycle and qualification evidence. | Target authority reconciliation `docs/checkpoints/MEDIAHUB-CLEAN-TARGET-MANIFEST-AUTHORITY-RECONCILIATION-WAVE-10-2026-10-16.md@docs/mediahub-chat-tree-map-20261012`, blob `1f748bf80e08067fd85a7e1b0821cc4d12bda676`; MH-15 acceptance criteria SHA cited there `082642e67dc66cb359a5566773c143854cafaa00`. | Reviewed source states no owner-accepted exact clean target manifest; target identity/profile UNKNOWN and MH-15 not accepted/frozen. | BLOCKED / UNKNOWN | Identify and accept the exact target manifest with provenance and approval; demonstrate workspace isolation, resource constraints, supported toolchain, network allowlist/egress and rollback. Component catalogue alone does not close this row. |
| CA-WORKER-01 | First cloud worker is read-only and least privilege, checks out immutable source SHA, disables credential persistence, injects secrets only at runtime where explicitly needed, isolates workspace, limits egress and emits immutable provenance. | Issue #301; existing hardened read-only workflow candidate PR #334, current observed head `517b76d7f52f05fa145ae7fb44b3bba541f72267`; workflow contract tests are recorded in PR history at prior heads. | The prior tested head is not the exact current-head verification in this wave; PR #334 is OPEN/DRAFT and GitHub reports it non-mergeable. No dispatch was performed in this wave. | OPEN / BLOCKED | Reconcile workflow branch/base, rerun actionlint and the security-contract suite on exact head, independent review; authorized controlled dispatch must prove no writes/secrets beyond policy, no model fallback and complete evidence manifest. |
| CA-EVID-01 | Every claim binds task ID, source ref/commit, schema and policy digests, actor/agent identity, route/model, times, result and artifact digest; provenance is tamper-evident and does not leak credentials or raw context. | Candidate evidence-manifest schema and validator `02c326da8cf90d2e5253dff3c1a5b90d72f6e18d`; semantic validator `7c69f478301360930e9e2ff341692cf2676b16cd`; Issue #301. | Synthetic fixtures validate field/digest consistency only. No live issuer/policy resolution, secret-flow audit or qualified worker provenance is proven. | PASS-SCOPED / OPEN | Independent schema review plus controlled read-only worker execution; read artifact bytes back; verify run/job/artifact IDs and digests match exact workflow/source SHA. |
| CA-QUEUE-01 | The queue/dispatcher admits only tasks with a valid issuer/capability, accepted target/route/policy/budget, immutable source SHA, bounded expiry and complete evidence contract; retries/concurrency/recovery are bounded and fail-closed. | Issue #301 and A0 trace blob `49ca0b69737bf8d44fe3a42daa47fd9157c9097d`; existing activation queue is explicitly documentary per Issue #301. | CAF-Q entries are documented; no qualified live scheduler or accepted external Jarvis↔A0 ingress contract is evidenced. | BLOCKED | Keep dispatch disabled until CA-A0-01/02, CA-CAP-01, CA-R06-01/02, CA-TARGET-01, CA-WORKER-01 pass; then test duplicate, malformed, expired, revoked, budget-exhausted and unknown-route tasks. |
| CA-SUPPLY-01 | Lock regeneration is repeatable from a hash-locked bootstrap; package bytes, publisher provenance, actions and runner/runtime are independently reviewable. | Candidate head `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`; lock-generation bootstrap blob `2cb89e822dabbe54a11e6b718ec8443b8891c926`; workflow blob `22ed52a9252630bfa62b5fbb7d37ea79c84f8b82`. | Lock run [39058422263](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39058422263) passed hash-locked install and byte-for-byte lock regeneration; artifact `12110905625`, SHA-256 `c94ead52345eba9d652a0107c611eb67dca46e39f0ce0b49b40d1938e54ad224`. PyPI metadata cited in PR #338 says Trusted Publishing was not used for `setuptools==84.0.0`. | PASS-SCOPED / OPEN | Independent supply-chain reviewer resolves the publisher-provenance residual; verify all action pins, package digests, sources and permissions; refresh on exact head. |
| CA-PROMO-01 | Design, implementation, testing, verification, qualification, release, deployment and production acceptance remain separate explicit states with authoritative transition evidence. | Baseline 2.0 blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; Unified Architecture Contract blob `c248956417cc61d66c968a4c58a56e799f653354`; Issue #301. | Reports distinguish CI success from qualification, deployment and acceptance; all Contour A acceptance gates remain open. | OPEN | Each transition has named authority, preconditions, immutable evidence, independent verifier where required, and rollback/exception status. Current disposition stays NOT QUALIFIED / NOT DEPLOYED / NOT PRODUCTION-ACCEPTED. |

### Dependency order and promotion rule

1. `CA-AUTH-01` authority role confirmation remains invariant throughout; this matrix grants no authority.
2. `CA-A0-01`, `CA-A0-02`, `CA-CAP-01`, `CA-R06-01`, `CA-R06-02` and `CA-TARGET-01` are blocking contract/governance dependencies.
3. `CA-SCHEMA-01`, `CA-SEM-01` and `CA-SUPPLY-01` can be independently reviewed in parallel; their PASS-SCOPED state does not satisfy the blocking runtime dependencies.
4. `CA-WORKER-01` must not be qualified before accepted target/isolation and authorization contracts. `CA-QUEUE-01` remains non-operational until all required gates pass.
5. Promotion requires a fresh exact-source SHA, passing required CI, independent review, auditable evidence and explicit authority for each transition. Missing or ambiguous data stays UNKNOWN and blocks admission.

### Wave 02 completeness check

- Rows in this Contour A slice: 14.
- PASS-SCOPED rows: `CA-SCHEMA-01`, portions of `CA-SEM-01`, `CA-EVID-01`, `CA-SUPPLY-01`; each explicitly limited to existing fixture/lock evidence.
- Blocking or unknown domains remain: A0 ingress/issuer; lease/fencing/recovery; runtime capability verification; R-06 audit/privacy governance; accepted clean target; isolated worker; live queue/dispatch; promotion/acceptance.
- This table is an evidence and work-ordering aid. It does not amend Baseline 2.0, approve protocol choices, select an issuer technology, establish target hardware, authorize provider calls or prove Contour A readiness.
