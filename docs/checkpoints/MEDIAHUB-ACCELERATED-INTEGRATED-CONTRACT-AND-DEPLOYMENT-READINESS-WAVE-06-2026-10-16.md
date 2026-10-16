# MediaHub OS — Accelerated Integrated Contract, Project-Wide Matrix and Deployment-Readiness Plan, Wave 06

- Date: 2026-10-16
- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Functional authority: `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`
- Status: **PLAN / SOURCE-ANCHORED / NOT ACCEPTED / NOT FROZEN**
- Scope: exact P0 remediation design for the ASTRA GitHub workflow family plus an accelerated, cross-domain convergence program for one project-wide matrix, one verifiable system contract, and deployment-readiness evidence.
- Parent artifacts:
  - [Wave 05 unified security control matrix and verifiable workflow contract](MEDIAHUB-UNIFIED-SECURITY-CONTROL-MATRIX-AND-VERIFIABLE-CONTRACT-WAVE-05-2026-10-16.md)
  - [Unified system traceability matrix v0.1](mediahub-unified-system-traceability-matrix-v0.1.md)
  - [Unified architecture and deployment contract v0.1](mediahub-unified-architecture-and-deployment-contract-v0.1.md)
  - [Canonical source registry and security evidence ledger — Wave 03](MEDIAHUB-CANONICAL-SOURCE-REGISTRY-AND-SECURITY-EVIDENCE-LEDGER-WAVE-03-2026-10-16.md)
  - [ASTRA workflow authority review — Wave 04](MEDIAHUB-ASTRA-WORKFLOW-AUTHORITY-REVIEW-WAVE-04-2026-10-16.md)
  - [Project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Executive decision

Use a **single integrated contract with domain-owned annexes**, not a wholesale rewrite of every legacy document. Preserve accepted Baseline 2.0 and historical IDs; map existing requirements into one canonical register; mark conflicting, duplicate, stale, or weakly evidenced statements as reconciliation items. Keep historical records immutable and distinguish requirement, decision, proposal, implementation, verification, qualification, release, deployment and acceptance.

The accelerated path is a five-day target plan with explicit gates. It is a planning target, not a delivery guarantee: owner decisions, new-hardware facts, authorized test execution, independent review, and actual evidence can extend the schedule. Parallel work is permitted only for source-backed documentation lanes with stable inputs. No lane may claim system readiness from documentation completeness alone.

**Definition of the desired endpoint:** one accepted versioned system contract; one canonical project-wide requirements/control/evidence matrix; a clean-slate target manifest; a reproducible Contour A deployment and qualification record; explicit Contour B admission gates; rollback and recovery evidence; and an independent acceptance decision. “Deployment-ready” requires evidence for the exact target profile and revision, not merely a completed plan.

## 2. Live source baseline and exact P0 patch design

The following current `main` workflow blobs were re-read for this plan:

| Source | Blob SHA | Relevant source locations | Planned disposition |
|---|---|---|---|
| `.github/workflows/astra-autonomous-supervisor.yml` | `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | triggers L5–27; permissions L29–31; node-key forwarding L101–107; provider call L115–119; privileged supervisor job begins L121; persisted checkout credentials L140–144 | P0-1 ref/target preflight; P0-3 explicit secret mapping; P1 token/credential scope |
| `.github/workflows/astra-chat-control.yml` | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | workflow permissions L7–10; association-only issuer gate L23–26; parser L37–48; dispatch L62–72; hard-coded execution target/executor L103–115 | P0-2 actor/capability/replay; P1 canonical target/executor; least privilege |
| `.github/workflows/astra-provider-qualification.yml` | `d3160088fbef4fce152ed7335f0acaa3bb440378` | provider runner and broad environment mapping L27–73; checkout L74–77 | P0-3 caller/callee secret allowlist and provider-specific exposure |
| `.github/workflows/astra-distributed-verification.yml` | `648f56badd2b919b822b4fe4b61f285cca99ed93` | three required HMAC secrets L11–18; per-node exposure L35–45, L71–81, L107–117; aggregate receives all three keys L145–162 | P1 cryptographic boundary review; avoid unsafe removal before verifier semantics are traced |

These SHA values identify reviewed source blobs. Proposed changes below target `main` source, while documentation remains on the docs branch. The refs remain divergent; this plan authorizes no branch integration.

### 2.1 P0-1 — Approved ref and immutable target fence

**Threats:** ASTRA-04-01, ASTRA-04-10; SEC-WF-01 and SEC-WF-10.

**Proposed patch shape:**
1. Add a low-privilege preflight job on a GitHub-hosted runner with no secrets and no self-hosted labels. It validates event type, approved ref, exact 40-character commit SHA, expected repository, and permitted trigger profile.
2. Require every secret-bearing or self-hosted job to depend on preflight and consume its validated outputs. Repeat critical checks inside each privileged job as defense in depth.
3. For `workflow_dispatch`, require the canonical default branch ref. For push-triggered execution, require the approved branch and source SHA. For reusable workflows, validate the caller-supplied target SHA and check out that exact SHA; reject malformed, missing, or conflicting values.
4. Keep the immutable target SHA distinct from the branch name. Branch name alone is not a reproducibility proof.
5. Add explicit concurrency, timeout and cancellation semantics to the preflight-to-privileged path. Preserve the existing stale-run reaper as a separate authority unless a source trace proves otherwise.

**Files:** supervisor workflow first; then chat-control and reusable qualification workflows for consistent caller/callee target binding.

**Verification cases:** approved default-branch dispatch; non-default dispatch denied before secret-bearing jobs; missing/malformed SHA denied; target SHA mismatch denied; workflow definition and checked-out code SHA match; reusable workflow called with conflicting target denied.

**Rollback:** revert the isolated preflight/ref-fence change only after recording the prior blob SHA and the reason for rollback. A rollback that restores an unsafe path must block privileged scheduling until the risk is accepted.

### 2.2 P0-2 — Actor, capability, operation and replay binding

**Threats:** ASTRA-04-02 and ASTRA-04-10; SEC-WF-02 and SEC-WF-10.

**Proposed patch shape:**
1. Treat comment author association as one signal, not complete authorization.
2. Resolve the authenticated GitHub actor/comment author to an explicit allowed actor identity and capability profile. The profile must name allowed operations, targets, risk tier, approval requirements and expiration.
3. Parse the comment into a canonical typed request: request ID, actor ID, operation, task ID, executor ID, node ID, target SHA, issuance time, expiry, nonce, and request digest.
4. Reject unknown fields, aliases, targets and operation combinations. Enforce replay/idempotency through a durable unique request key and a defined retention window. A workflow run ID by itself is not a complete replay policy.
5. Require an independent approval path for high-impact actions such as autonomous GOLD dispatch or distributed worker execution. Approval evidence must bind the exact request digest and target.
6. Split permissions by job: parser/authorization should receive read-only permissions where possible; dispatch requires only the Actions permission it uses; comment reporting receives issue-comment permission; remove workflow-wide `contents: write` unless a traced operation requires it.

**File:** `.github/workflows/astra-chat-control.yml`; inspect `astra_github_agent.py` and the canonical operation/capability registry before choosing where durable idempotency state lives.

**Verification cases:** authorized status request; unauthorized actor; actor allowed for status but denied for run; expired request; duplicate request; modified digest; target mismatch; unknown node/executor; approval bound to a different request; reporting failure does not turn a denied operation into success.

**Rollback:** restore the prior parser/authorization implementation only as an isolated revert; keep privileged run paths disabled until the required policy is re-established.

### 2.3 P0-3 — Explicit provider-secret allowlist

**Threat:** ASTRA-04-04; SEC-WF-04.

**Proposed patch shape:**
1. Remove `secrets: inherit` from the supervisor-to-provider reusable workflow call.
2. Before editing the caller, inspect `ops/qualification/qualify_execution_backends.py`, provider registries, model routing contracts and provider evidence schema to determine which environment variables are consumed for each provider.
3. Produce a source-backed map `provider → credential name → consuming step → egress destination → evidence fields`. Never include secret values.
4. Pass only the exact named secrets required by the approved qualification profile. Prefer separate provider-specific jobs or environment protection so a job for one provider cannot read unrelated provider keys.
5. Keep provider evidence sanitized; prove logs and artifacts contain metadata only, not credential values. The existing long environment list in the callee is not proof every secret is necessary.
6. Ensure ref/target preflight passes before any provider credential enters a job environment.

**Files:** supervisor L115–119 and provider workflow L27–73; related provider registry and qualification code only after a read-only dependency trace.

**Verification cases:** every mapped provider receives its required credential; unrelated credentials are absent; missing credential results in a controlled BLOCKED outcome; no secret value appears in logs/artifacts; provider result binds to target SHA and qualification profile.

**Rollback:** revert only the secret-mapping slice. A broad inherited-secret fallback is not an acceptable automatic rollback; if allowlist mapping fails, provider qualification remains BLOCKED.

### 2.4 P0/P1-4 — Target/executor canonicalization

**Threat:** ASTRA-04-07; SEC-WF-07.

**Proposed patch shape:**
1. Reconcile the parser's accepted values `codex|claude` and `mh-dev-02|Voktors-Mac-mini.local` with the accepted node/executor registry.
2. Remove hard-coded execution values that silently replace validated request values. Dispatch and execution must consume the same canonical target and executor.
3. Validate task contract, node capability, executor capability, target SHA and operation before any side effect.
4. If an executor/target combination is not admitted by the current clean-slate target registry, reject it explicitly. Do not resurrect retired host assumptions by copying old node names into the new target registry.

**File:** `.github/workflows/astra-chat-control.yml` L37–48 and L103–115, plus the authoritative node/capability registry after live source tracing.

**Verification cases:** each admitted combination maps consistently end to end; all unknown/retired combinations are rejected; evidence reports requested and executed target/executor and they match.

### 2.5 P1-5 — HMAC authority and verification design

**Threat:** ASTRA-04-05; SEC-WF-05.

The distributed workflow currently supplies all three node keys to the aggregate job at L160–162. Do not simply delete those mappings before tracing the aggregate verifier: symmetric HMAC verification requires the matching key. Preferred design to evaluate is per-node signature/attestation verification inside the narrowest authorized boundary, then pass a sanitized verified attestation or a public-key-verifiable signature to the aggregate. If HMAC remains, document the unavoidable verifier trust and restrict each key to the minimum step/job. Record rotation and revocation semantics.

**Exit evidence:** key-flow diagram, signer/verifier separation, per-node isolation cases, cross-node impersonation rejection, rotation/revocation record.

### 2.6 P1/P2 — Token scope, credentials, actions and schedule

- Supervisor `persist-credentials: true` at L140–144 must have a traced necessity. Preferred setting is `false`; if later authenticated Git is required, use an explicitly scoped short-lived credential only for that step.
- Replace workflow-wide token grants with per-job minimum permissions. Preserve only capabilities used by named API operations.
- Inventory third-party actions, pin full commit SHAs, record upstream version and update provenance. Pin changes require source/release validation; do not guess SHAs.
- The ten-minute schedule must have an explicit owner, purpose, concurrency/cancellation policy, side-effect ceiling, provider-cost budget and stop condition. A schedule is not evidence of useful autonomous progress.
- Branch protection, rulesets and security-alert status remain UNKNOWN until an authoritative export/API result is captured.

## 3. One project-wide matrix: canonical schema

Create one canonical machine-readable requirements/control/evidence register, then render human-readable views from it. Existing matrices remain linked sources until their rows are reconciled; do not bulk-copy every historic row into a second competing authority.

Required columns:

| Field | Purpose |
|---|---|
| `requirement_id` | Stable historical ID or newly allocated collision-checked ID |
| `domain_id` / `workstream_id` | Canonical domain and owner workstream |
| `source_authority` / `source_path` / `source_sha` | Authority and immutable provenance |
| `baseline_version` | Baseline 2.0, historical 1.0, or proposal |
| `statement` / `rationale` | Testable requirement and traceable reason |
| `requirement_type` | Functional, security, privacy, reliability, performance, lifecycle, governance, deployment |
| `authority_owner` / `decision_status` | Who can decide and whether a decision exists |
| `control_id` / `threat_or_failure_id` | Preventive/detective/recovery control and failure linkage |
| `component_ids` / `interface_ids` | Affected admitted components and contracts |
| `target_profile` / `contour` | Contour A/B and exact hardware/OS profile or UNKNOWN |
| `implementation_status` | NOT STARTED, IN PROGRESS, IMPLEMENTED, BLOCKED |
| `verification_method` / `verification_status` | Test/inspection/review method and result |
| `evidence_uri` / `artifact_digest` / `run_id` | Retrievable, integrity-bound proof |
| `qualification_gate` / `release_gate` | Admission and release relationship |
| `risk` / `open_conflict_id` / `dependency_ids` | Risk and dependency closure |
| `rollback_or_recovery` | Reversal/recovery method |
| `last_verified_at` / `reviewer` | Freshness and independent review |
| `status_reason` / `limitations` | Explicit gap explanation |

### 3.1 Required project domains

The canonical register must cover all of the following, retaining existing MH and requirement IDs:

1. Product definition, Baseline 2.0 authority and functional acceptance.
2. System architecture, State Authority, domain boundaries and ownership.
3. Identity, authentication, authorization, policy and capability issuance.
4. Security threat model, secrets, signing, supply chain and vulnerability evidence.
5. Privacy, data classification, consent, audit and retention.
6. Data/state contracts, migrations, backup, restore and recovery.
7. ASTRA A0 ingress, mission/request schema, idempotency and lifecycle.
8. Jarvis orchestration, agent delegation, queues, scheduling and cancellation.
9. Developer Fabric, worker leases, workspace isolation and artifact provenance.
10. Model/provider registry, local/cloud classification, egress and route evidence.
11. Component manifest, license/security admission, versions, SBOM and provenance.
12. Contour A bootstrap, reproducible build, CI, test and qualification infrastructure.
13. Contour B product deployment, admission, rollout, release and rollback.
14. Clean-slate hardware/OS/topology/storage/network profiles; unknown hardware facts remain UNKNOWN.
15. Observability, logs, metrics, alerts, audit continuity and incident response.
16. Performance, capacity, resource budgets, timeouts and failure recovery.
17. API/interface/schema compatibility and versioning.
18. Mobile and remote-access boundaries; apps remain clients, never authorities.
19. Operations, maintenance, updates, key rotation, decommissioning and recovery drills.
20. Governance, owner decisions, risk acceptance, independent acceptance and evidence custody.

### 3.2 Conflict and duplication handling

- Keep accepted Baseline 2.0 as the functional authority; Baseline 1.0 remains historical provenance.
- Assign stable IDs only after collision search across the map, traceability matrix, master roadmap and existing domain documents.
- Represent each conflict as a record with both source claims, authority level, impact, decision owner, safe interim rule and closure evidence.
- Use statuses: CONFIRMED, PROPOSED, CONFLICT, UNKNOWN, BLOCKED, IMPLEMENTED, VERIFIED, QUALIFIED, ACCEPTED, RETIRED, HISTORY. Never promote one status automatically to another.
- Where FreeLLMAPI/cloud wording and `local_gateway` registry classification disagree, preserve the conflict until service location, upstream provider and egress path have source-backed resolution.
- Preserve legacy host names and failed deployment records as HISTORY or RETIRE candidates only. They are not target inventory evidence for new hardware.
- Every matrix row must have at least one primary source and a clear evidence expectation. Unsupported rows remain EVIDENCE PENDING.

## 4. Integrated system contract structure

The final contract should be one top-level normative document with domain annexes, each carrying an owner, revision and acceptance status:

1. **Authority and scope:** Baseline 2.0, Contour A/B, local-first product boundaries, one logical State Authority.
2. **Trust and identity:** principal model, actor identity, capabilities, policy decision, delegation, expiry and revocation.
3. **Mission/request envelope:** request ID, actor, intent/operation, target profile, immutable source SHA, policy revision, deadline, budget, cancellation, idempotency key and evidence requirements.
4. **Admission:** component identity, source/license/security review, target compatibility, permissions, isolation and owner acceptance.
5. **Execution lifecycle:** queued → admitted → leased → running → result produced → verified → closed, with explicit retry, cancel, timeout, recovery and terminal-state rules.
6. **Routing and egress:** every hop records provider identity, locality, upstream, network/egress policy, data classification, cost and immutable route evidence.
7. **State/data:** authoritative write owner, schema/version, consistency, retention, backup, restore and migration gates.
8. **Security and privacy:** least privilege, secret scope, cryptographic provenance, audit policy, privacy controls and failure behavior.
9. **Evidence:** revision-bound evidence envelope, artifact digest, verifier, timestamp, target profile, limitations and retention.
10. **Qualification/release/deployment:** independent gates, target-specific proof, rollback, disaster recovery and operational acceptance.
11. **Governance:** decision rights, conflict handling, risk acceptance, change control and contract versioning.
12. **Annexes:** component manifest, interface registry, capability matrix, deployment profiles, verification suite catalogue, security matrix, privacy crosswalk, recovery matrix and open-decision ledger.

## 5. Accelerated five-day wave plan

The schedule is a target for converging the documentary and implementation plans, with authorized verification scheduled only after its permission gates. Independent source-backed lanes can run in parallel; integration happens only after each lane publishes exact source refs, stable IDs, dependencies and evidence gaps.

### Day 1 — Authority freeze and canonical inventory

**Goal:** establish the exact input set and eliminate avoidable re-discovery.

- Re-read live refs and SHA for Baseline 2.0, map, master roadmap, unified traceability matrix, deployment contract, component manifest, security ledger, privacy/audit crosswalk, A0 ingress contract, executor capability matrix, lifecycle/recovery contract and provider identity/egress crosswalk.
- Build the source registry with authority ranking and current revision; record branch divergence.
- Define canonical matrix schema, ID allocation rules, status vocabulary and evidence envelope.
- Generate a conflict ledger with duplicates, contradictory claims, stale target references, missing owners, UNKNOWN hardware and missing evidence.
- Deliverables: source authority registry; matrix schema; ID collision report; conflict backlog with P0/P1/P2.

**Exit gate:** every workstream has a primary source, stable scope, owner/decision authority, and an explicit evidence gap list.

### Day 2 — Cross-domain contract convergence

**Goal:** convert the inventory into one testable contract.

- Parallel lanes: identity/policy/security; ASTRA ingress/orchestration; provider/routing/egress; data/privacy/audit; component/supply chain; deployment/lifecycle/recovery; mobile/product boundary.
- Each lane returns requirement IDs, source SHA, interfaces, preconditions, success/failure semantics, evidence format, recovery path and unresolved decisions.
- Merge lane outputs into the single canonical matrix, deduplicate without renumbering existing IDs, and trace every contract clause to matrix rows.
- Resolve technical conflicts by existing authority rules; write decision packets only for product/business/risk decisions that cannot be inferred.
- Deliverables: integrated contract draft, matrix v0.2 candidate, interface/dependency graph and decision packet list.

**Exit gate:** every normative clause maps to requirements; every P0 requirement maps to a control and a verifiable gate.

### Day 3 — P0 security and lifecycle remediation design

**Goal:** remove authority gaps from the critical path before broader implementation.

- Finalize exact workflow patch diffs for P0-1, P0-2 and P0-3; include caller/callee changes, token scope, canonical target mapping, HMAC verifier design and rollback slices.
- Complete ingress request/identity/capability/replay contract and trace through Jarvis → ASTRA A0 → dispatcher → worker → evidence.
- Complete target-independent deployment manifest and lifecycle states, including bootstrap trust, artifact provenance, rollback and recovery.
- Produce negative/positive verification vectors, static checks, required run evidence, and authorization prerequisites.
- Deliverables: patch set proposal, test design, threat-control crosswalk, recovery/rollback plan.

**Exit gate:** each P0 control has a specific source location, proposed change, independent failure test, expected evidence, rollback and reviewer. This exit gate does not itself authorize source edits or test execution.

### Day 4 — Reproducible Contour A and target-profile qualification plan

**Goal:** define what “ready to deploy” means for an exact target.

- Freeze a target manifest schema for hardware identity, OS/image, architecture, storage, network, trust bootstrap, toolchain, component versions, secrets/credentials references, resource budgets and rollback.
- Mark every absent new-hardware fact UNKNOWN; avoid legacy-host inference.
- Define clean-room bootstrap, pinned source/artifacts, reproducible build, CI contract, artifact signing/provenance, SBOM/license/security checks and deterministic evidence capture.
- Define qualification gates for single-node, distributed node, provider routing, local-only mode, interruption/retry/cancellation, recovery, backup/restore, security/privacy, capacity and cost.
- Separate Contour A environment qualification from Contour B product deployment admission.
- Deliverables: target manifest template, reproducibility contract, qualification matrix, evidence retention plan, deployment/rollback runbook draft.

**Exit gate:** each target-specific claim has a defined evidence source and a blocking rule for missing facts.

### Day 5 — Integrated review, acceptance package and execution backlog

**Goal:** produce a coherent package ready for authorized implementation and qualification.

- Run a documentary consistency pass: matrix↔contract↔component manifest↔interfaces↔deployment manifest↔verification gates↔roadmap.
- Validate stable IDs, source SHAs, link integrity, dependency closure, conflict dispositions and no accidental promotion of proposal to acceptance.
- Build a critical-path graph and split implementation into bounded changesets with owners, prerequisites, rollback and acceptance evidence.
- Publish readiness dashboard: accepted / implemented / verified / qualified / blocked / UNKNOWN counts, P0 open risks and target-specific blockers.
- Prepare independent acceptance checklist and the owner decision packet.
- Deliverables: contract candidate v1.0, project matrix candidate v1.0, deployment readiness dossier, critical-path backlog and independent review package.

**Exit gate:** the package is internally consistent and ready for formal review. Production deployment is allowed only after required owner decisions, Contour A deployment and independent acceptance, exact-target qualification, and the separate Contour B admission gate.

## 6. Parallel lanes and integration rules

| Lane | Primary output | Critical dependency | Safe parallel scope |
|---|---|---|---|
| A — Authority/source registry | Source registry, IDs, conflict ledger | Live GitHub refs | Read-only source reconciliation |
| B — Security/identity | Threat-control matrix and authorization contract | Accepted identity/capability sources | Documentation and proposed patches |
| C — ASTRA/Jarvis lifecycle | Ingress-to-worker lifecycle contract | A0 and lifecycle primary docs | Contract trace and negative cases |
| D — Provider/routing/egress | Per-hop route/secret/evidence contract | Provider registry and routing source | Registry crosswalk; no provider calls |
| E — Component/supply chain | Admitted component manifest and provenance | Manifest, license/security evidence | Source/version/license reconciliation |
| F — Data/privacy/audit | Data classification, audit, privacy matrix | Baseline 2.0 and privacy authority | Clause-level crosswalk |
| G — Deployment/recovery | Target manifest and lifecycle gates | Clean-slate target facts; unknowns explicit | Hardware-independent templates |
| H — Verification/evidence | Test catalogue and evidence schema | Stable requirement IDs | Test design; execution separately authorized |
| I — Integration/release | Unified contract, matrix and backlog | Outputs A–H | Integrate only revision-identified outputs |

No lane invents authority. Cross-lane conflicts become named conflict records. Do not create parallel ID sequences for existing requirements. Do not merge divergent Git branches as an integration shortcut.

## 7. Readiness gates for an autonomous hybrid distributed developer fabric

The following are release gates, not current claims of completion:

| Gate | Required evidence | Fail-closed condition |
|---|---|---|
| RD-01 Canonical contract | Accepted revision, owner, scope and clause-to-requirement trace | Any normative clause without authority/trace |
| RD-02 Canonical project matrix | All domains inventoried; ID collisions resolved; source/evidence status explicit | Missing domain or unsupported status promotion |
| RD-03 Identity and policy | Actor, capability, delegation, expiry, revocation, replay/idempotency verified | Any privileged route bypasses policy |
| RD-04 ASTRA/Jarvis lifecycle | End-to-end request/lease/cancel/retry/result/evidence trace | Missing terminal-state or recovery rule |
| RD-05 Component admission | Pinned source, license, security, interface and target compatibility evidence | Unknown critical component provenance |
| RD-06 Routing and egress | Every hop has provider/upstream/locality/egress and route evidence | Local-only claim without end-to-end evidence |
| RD-07 Secrets and permissions | Per-job allowlists, minimum token permissions, key isolation | Unbounded secret or authority exposure |
| RD-08 Contour A bootstrap | Reproducible clean bootstrap/build and independent qualification | Manual undocumented prerequisite or failed gate |
| RD-09 Target profile | Explicit hardware/OS/topology/network/storage manifest | Critical target fact UNKNOWN |
| RD-10 Distributed execution | Node admission, lease fencing, isolation, target-SHA binding and evidence aggregation | Stale or cross-node work accepted |
| RD-11 Recovery | Tested backup/restore, rollback, interrupted-job recovery and key revocation | Recovery path described but unverified |
| RD-12 Observability/audit | Correlated request/run/artifact IDs, integrity, privacy and retention | Required audit evidence absent |
| RD-13 Security/privacy qualification | Revision-bound negative and positive results plus risk disposition | P0 unresolved or test evidence stale |
| RD-14 Performance/cost | Target-specific capacity, queue latency, provider budget and stop controls | Resource/cost ceiling absent |
| RD-15 Independent acceptance | Reviewer decision for exact contract, source and target SHAs | Implementer self-attests as sole acceptance |
| RD-16 Contour B admission | Contour A accepted; product-specific gates passed; rollout/rollback authorized | Contour A acceptance missing |

## 8. What can be completed within several days versus what remains conditional

**Within the documentary workstream:** source inventory, conflict register, matrix schema and consolidation, contract draft, P0 patch proposals, test designs, target manifest template, critical-path backlog, decision packets and acceptance checklist.

**Conditional on separate authorization and evidence:** source/workflow edits, static parser/YAML validation, unit/integration tests, workflow dispatch, provider/model calls, secret-dependent verification, runner inspection, clean-room bootstrap, target hardware qualification, deployment, production rollout and independent acceptance.

The plan must accelerate by parallelizing source-backed analysis and documentation, reusing one ID/evidence schema, and keeping integration gates short. It must not accelerate by skipping provenance, blending divergent branches, using legacy hardware assumptions, or treating unexecuted verification as PASS.

## 9. Immediate next execution sequence

1. Start Wave 07 with Day 1 authority/source inventory, but update existing registers rather than creating another competing inventory.
2. In parallel, prepare a source-backed dependency map for the three P0 workflow changes and trace provider credential consumption before defining the allowlist.
3. Produce a unified domain ownership and interface graph using existing IDs and contract sources.
4. Deliver the first matrix integration increment with every row carrying source SHA, authority status, evidence expectation and blocking reason.
5. Keep P0 workflow implementation as a separate authorization gate; complete proposed diffs and negative-test design before requesting permission to apply or execute them.
6. At the end of each daily wave, read back changed documents, verify blob SHAs, update map/checkpoint/roadmap, publish blockers and identify the next critical-path increment.

## 10. Current limitations and evidence boundary

- This pass is source/documentation planning only. No workflow source was edited, no tests/scanners were run, no workflow was dispatched, no model/provider was invoked, no credentials or secret values were accessed, no runner/host/runtime was inspected, and no infrastructure/deployment/branch integration occurred.
- The docs branch is divergent from `main`; live compare snapshot: DIVERGED, ahead 1,661 / behind 10; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`; main HEAD `b45324009ac3aa65322a702c28069b12190bc4b8`.
- New target hardware, OS, network and topology remain UNKNOWN until authoritative input/acceptance. Historical hosts are provenance, not deployment targets.
- The security contract and this plan remain PROPOSED / NOT ACCEPTED / NOT FROZEN. No deployment-ready or production-acceptance claim is made.

## 11. Conclusion

Wave 06 combines the immediate P0 remediation plan with an accelerated convergence program for the entire project. The intended result is one canonical contract, one source-backed project-wide matrix, one explicit conflict/decision ledger, and a target-specific deployment-readiness dossier whose claims are all tied to evidence and acceptance gates.

**Next wave:** Wave 07 — Project-Wide Canonical Authority Inventory and Matrix Integration, Day 1, with parallel read-only lanes and stable ID/source provenance.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
