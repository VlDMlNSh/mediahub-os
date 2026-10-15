# MediaHub OS — Contour A Contract / Authority Conflict Register, Wave 01

- Date: 2026-10-15
- Status: **SOURCE-ONLY RECONCILIATION REGISTER / NOT NORMATIVE / NOT AN ACCEPTANCE OR IMPLEMENTATION CLAIM**
- Scope: WB-02 of the Contour A Pre-Deployment Readiness Work Breakdown.
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Main HEAD at audit: `608d7463011798ca75e36bfce4b749a9caf4f9a0`
- Documentation branch comparison against main: **DIVERGED**, 1364 ahead / 3 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No merge, rebase, cherry-pick or integration performed.

## 1. Authority and interpretation rules

This register distinguishes: (a) owner-approved decisions, (b) source-level conflicts, (c) unresolved contract gaps, and (d) proposed dispositions. A proposed disposition is not an accepted change. The current owner decision is DEC-DEV-02 Option C, owner-decision record blob `70376a2709e055972ceddc4a280d26992977213c` on the documentation branch:

- Jarvis: corporation-level mission coordination and result tracking through accepted interfaces.
- ASTRA A0: ASTRA-internal engineering workflow state (queue/claim/lease/heartbeat/retry/cancellation/recovery and ASTRA evidence/gate transitions) within its accepted contract.
- MediaHub Product State Authority: sole canonical Contour B product-state mutation authority.

## 2. Source-pinned conflict register

| ID | Conflict / gap | Source evidence (ref + blob SHA) | Controlled disposition | Status / gate |
|---|---|---|---|---|
| CA-AC-01 | A0 authority wording is broader on main than the owner-approved split. | Main unified YAML `adc852009c3a79d0e64265a3af8a4910a1388057` labels `authority.astra.role: single_coordination_authority`; docs-branch YAML `f5040aeb479176508d5b0ca35eb742a6db818867` scopes A0 to ASTRA-internal engineering workflow state. Main reference architecture `7be5fadd3055642e7823c7233f90e978a87e5366` says “single MediaHub coordination and state authority”; docs reference architecture `b354acfa4cff595583a7f1778371143e9868f293` narrows the role. | Reconcile normative prose/model to DEC-DEV-02 using an authorized, coordinated change; do not treat docs-branch content as integrated. | OPEN — owner decision settled; source change control and integration not authorized. |
| CA-AC-02 | Model/test mismatch exists on the documentation branch. | `tests/test_astra_gold_architecture_drift.py` SHA `d6a0e6a6d81dc6e15e343cd80ee950431b1e3b14` on both refs still asserts the old role at line 65; docs model uses the scoped role. | Update model and assertion together only after authorization; then verify with separately authorized tests. | OPEN — static source mismatch only; no test executed. |
| CA-AC-03 | Qualification schema field `state_authority: A0-ASTRA` can be misread as product-state authority unless scope is explicit. | Main schema SHA `aef6229477ed8ec45e45170f98ea87f7ba75ca29`; docs schema SHA `0b86b07dfa916d4485ce1f8f54d19de136d98491`. Docs branch comment limits this field to ASTRA internal queue/claim/gate state; identifiers are stable on both refs. | Preserve historical/stable IDs. Clarify semantics in a coordinated schema/prose update; do not rename the value without compatibility and history evidence. | OPEN — full producer/consumer/history closure incomplete. |
| CA-AC-04 | Executor capability matrix describes A0 authority as “Global coordination/state”, broader than its concrete queue/evidence examples. | Main matrix SHA `da26185254d9954fcee204f81ecca129bf052e7c`; docs branch matrix SHA `9ad83781a8da53d1a8f540ede54eba95281f01c0`. | Scope wording to ASTRA engineering workflow/control state; preserve executor-admission policy and Product State Authority boundary. | OPEN — coordinated wording change required. |
| CA-AC-05 | Security invariants define the authorization path, but the actual Jarvis→A0 ingress and capability lifecycle are not accepted contracts. | MH-12 SHA `cf4ebfd5bf471ca676f075c51d3a24906504e490`: identity → authentication → trust → capability → authorization → policy → consumer boundary → State Authority; unknown authorization fails closed. Owner decision record SHA `70376a2709e055972ceddc4a280d26992977213c` explicitly leaves ingress/API and issuer lifecycle open. | Do not invent endpoint, protocol, token format or issuer. Keep dispatch fail-closed until owner/governance accepts ingress, identity/authentication, replay, capability issue/verify/delegation/revocation and audit semantics. | HARD BLOCKER — WB-03/WB-04. |
| CA-AC-06 | ASTRA qualification model requires claim/lease, duplicate suppression, result publication and recovery, but cross-corporation mission/result governance and A0 authoritative publication/fencing remain unaccepted. | Qualification schema docs SHA `0b86b07dfa916d4485ce1f8f54d19de136d98491` includes G2 control-plane and G6 recovery gates; owner decision record SHA `70376a2709e055972ceddc4a280d26992977213c` requires stable task identity, provenance, validation and conflict detection. | Reuse ASTRA lifecycle only inside ASTRA's boundary. Define accepted corporation task/result contract, fencing/stale-worker rejection, cancellation/idempotency and authoritative publication before dispatch. | HARD BLOCKER — WB-05/WB-06. |
| CA-AC-07 | Target architecture is greenfield, but exact hardware/OS/topology and role-to-node allocation remain owner inputs. | Readiness work breakdown SHA `bce109783aeb577032ab2da767bfc78f2b2d6992` records HW-01…HW-07 OPEN; target architecture is logical, not deployment evidence. | Do not infer asset identity, OS/build, capacity, endpoints or placement from historical server names. Use owner-confirmed inventory before deployment planning. | HARD BLOCKER — WB-01/WB-08. |
| CA-AC-08 | Documentation branch and main have diverged; branch-local corrections are not canonical on main. | Live compare: main HEAD `608d7463011798ca75e36bfce4b749a9caf4f9a0`; docs branch 1364 ahead / 3 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. | Keep source-of-truth status explicit. No branch integration unless separately authorized; preserve source SHAs and re-fetch before any future change. | OPEN — integration prohibited under current authorization. |

## 3. Non-conflicts / invariants preserved

1. DEC-DEV-02 Option C is **OWNER-DECIDED**, not pending.
2. Jarvis does not directly mutate ASTRA-owned queue/claim/lease/gate state; it must use an accepted A0 interface.
3. A0 is not corporation-wide mission authority and is not MediaHub Product State Authority.
4. Product State Authority alone mutates canonical Contour B product state.
5. Unknown identity, capability, authorization, replay, fencing or publication semantics remain fail-closed.
6. Architecture design, implementation, test, verification, qualification, release, deployment and independent acceptance remain separate statuses.
7. Baseline 2.0 remains canonical; Baseline 1.0 remains historical.
8. No candidate selection/admission, hardware choice, runtime execution or deployment is implied by this register.

## 4. Required controlled sequence

1. Complete reliable producer/consumer/history closure for the ASTRA role value and schema fields; search misses are not proof of absence.
2. Resolve WB-03 ingress and WB-04 capability lifecycle contracts without inventing technology or endpoints.
3. Resolve WB-05 mission/task/result schema governance and WB-06 fencing/cancellation/idempotency/publication semantics.
4. Prepare a minimal path-specific normative change set only after explicit authorization; coordinate model, assertion, schema comments and authority prose.
5. Re-fetch changed sources, inspect diff and verify SHAs. Tests remain separately gated.
6. Continue WB-07 admission and WB-08 topology only from source-backed facts; keep target hardware questions HW-01…HW-07 open until owner-confirmed.

## 5. Verification boundary

Read-only GitHub source fetches and branch comparison only. No source contracts, tests, schemas, runtime artifacts or infrastructure were changed. No tests, installs, provider/model calls, credentials, host/runtime inspection, qualification, deployment or branch integration occurred. This register is a source-backed planning/control artifact, not an accepted normative contract.
