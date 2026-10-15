# MediaHub OS — Contour A Authority-Wording Reconciliation Proposal, Wave 01

- Date: 2026-10-15
- Status: **SOURCE-ANCHORED PROPOSAL / OWNER DECISION ALREADY RECORDED / NOT NORMATIVE / NOT APPLIED TO MAIN**
- Scope: statement-level reconciliation of ASTRA authority wording against owner-approved DEC-DEV-02 Option C.
- Boundary: this is a documentation proposal only. It does not amend main-branch contracts, accept an API, change runtime authority, authorize integration, or claim implementation/qualification.

## 1. Owner decision and governing interpretation

The owner-approved decision is **DEC-DEV-02 Option C** as recorded in `docs/checkpoints/MEDIAHUB-CHAT-TO-GITHUB-OWNER-DECISIONS-AND-CORPORATION-DIRECTION-WAVE-01-2026-10-15.md`, documentation-branch blob SHA `70376a2709e055972ceddc4a280d26992977213c`.

The approved responsibility split is:

1. **Jarvis** — corporation-level mission coordination: receive goals, plan/decompose missions, select only permitted routes and eligible executors, and track mission status/results through defined interfaces.
2. **ASTRA A0 / Astra Gold** — sole writer for ASTRA-internal engineering workflow state within its accepted contract: queue, claims, leases, heartbeat, retry/cancellation/recovery, and ASTRA-specific evidence/gate transitions.
3. **MediaHub Product State Authority** — sole canonical product-state mutation authority for Contour B. Jarvis, ASTRA, models, providers, workers and GitHub adapters gain no such authority by implication.

This decision is already owner-decided; this proposal does not reopen Option C. Exact Jarvis→A0 ingress, authentication/replay, capability issuer/verifier lifecycle, fencing and result publication remain separate open contract gates.

## 2. Statement-level source crosswalk

| ID | Source statement / source pin | Conflict or interpretation risk | Proposed wording for controlled change | Status |
|---|---|---|---|---|
| AUTH-01 | `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md`, `main`, blob SHA `7be5fadd3055642e7823c7233f90e978a87e5366`, §1: “A0-ASTRA is the single MediaHub coordination and state authority.” | “MediaHub coordination and state” can be read as corporation-wide mission ownership or canonical product-state authority, contradicting DEC-DEV-02 Option C. | “ASTRA A0 is the sole authority for ASTRA-internal engineering workflow state and execution admission within the accepted ASTRA contract. Jarvis coordinates corporation-level missions and submits ASTRA-governed engineering work through an accepted A0 interface. MediaHub Product State Authority remains the sole canonical Contour B product-state mutation authority.” | PROPOSED; main unchanged |
| AUTH-02 | `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md`, `main`, blob SHA `da26185254d9954fcee204f81ecca129bf052e7c`, Authority mapping row: “Global coordination/state” → A0 Astra; runtime “autonomous queue + claim/evidence state”. | Label is broader than the row’s concrete queue/evidence examples and can imply authority outside ASTRA workflow state. | Rename capability to “ASTRA engineering workflow/control state”; retain A0 as owner of ASTRA queue, claim, lease, heartbeat/retry/cancellation, evidence and gate transitions only. Explicitly exclude corporation-level mission ownership and canonical Contour B product-state mutation. | PROPOSED; main unchanged |
| AUTH-03 | `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml`, `main`, blob SHA recorded in Wave 04 as `adc852009c3a79d0e64265a3af8a4910a1388057`; A0 is described as `single_coordination_authority`. | Machine-readable authority label can preserve the same overbroad interpretation even if prose is clarified. | Replace only after schema/consumer impact is established with a scope-explicit enum/value such as `astra_engineering_workflow_authority`; define Jarvis mission coordination and Product State Authority as separate authority domains. Do not rename the value before searching all producers/consumers and compatibility constraints. | PROPOSED; exact field/path and consumers need revalidation before edit |
| AUTH-04 | `docs/checkpoints/MEDIAHUB-CHAT-TO-GITHUB-OWNER-DECISIONS-AND-CORPORATION-DIRECTION-WAVE-01-2026-10-15.md`, docs branch blob SHA `70376a2709e055972ceddc4a280d26992977213c`, §1: Option C is explicitly approved and says primary ASTRA wording must be reconciled through controlled documentation change. | No ambiguity remains about the owner’s selected option; the unresolved issue is source wording and change control. | Preserve the decision as OWNER-DECIDED. Link each amended primary statement to this decision and record affected source SHAs, consumer impact, review and post-change SHA. Do not describe the decision itself as pending. | OWNER DECISION RECORDED; change not applied |
| AUTH-05 | `docs/architecture/MH-12-security-architecture.md`, `main`, blob SHA `cf4ebfd5bf471ca676f075c51d3a24906504e490`: identity → authentication → trust → capability → authorization → policy → consumer boundary → State Authority; capability cannot self-grant; ambiguity fails closed. | Scope clarification must not weaken security checks or be misread as a capability grant or a concrete issuer/API decision. | Add an explicit cross-reference, not a new bypass: every Jarvis→A0 operation requires an accepted authenticated ingress and capability/authorization path; Product State Authority remains a distinct boundary. Unknown issuer, replay rules or authorization remains BLOCKED/deny. | INVARIANT; ingress/issuer contract still OPEN |

## 3. Required wording invariants

Any approved revision must preserve all of the following:

- Jarvis does not directly mutate ASTRA A0 queue/claim/lease/gate state; it uses an accepted A0 interface.
- A0 does not become corporation-level mission authority or Product State Authority by owning ASTRA’s internal workflow state.
- Product State Authority alone mutates canonical Contour B product state.
- External executors, models, providers, gateways and GitHub adapters are not authority sources.
- Missing/ambiguous identity, capability, authorization, replay, fencing or publisher evidence fails closed.
- Existing ASTRA lifecycle thresholds remain sourced from the canonical ASTRA governance contract; this proposal does not copy or redefine them.
- Source wording reconciliation is distinct from implementation, verification, qualification, release, deployment and acceptance.
- Baseline 2.0 remains canonical; no Baseline 1.0 merge or reinterpretation is introduced.

## 4. Change-control sequence

1. Re-fetch every cited source at the time of any proposed edit; confirm branch, path and blob SHA.
2. Resolve the machine-readable field/path and complete producer/consumer/reference closure for AUTH-03. A proposed enum string is not permission to change a public or persisted identifier.
3. Prepare a minimal path-specific diff against the authoritative source branch and record compatibility implications. Do not change the normative `main` files as part of this proposal.
4. Obtain the required owner/governance authorization for the exact source edits and integration route.
5. After authorized changes, re-read changed files, inspect exact diff, verify all cited blob SHAs and update the map/checkpoint. Branch merge/rebase/cherry-pick remains a separate explicitly authorized action.
6. Independently review the resulting authority wording against DEC-DEV-02, MH-12, ASTRA governance, and all discovered consumers.

## 5. Open blockers deliberately not solved here

- Accepted Jarvis→A0 endpoint/protocol, principal, authentication, request/ack/error schemas and replay protection.
- Capability issuer/attester authority; audience/scope/expiry/attenuation/delegation/revocation/rotation/audit and verifier contract.
- A0 claim fencing, stale lease rejection, authoritative result publication and duplicate/conflicting publisher semantics.
- Corporation mission/task/result/evidence schema governance, namespace/version policy and producer/consumer closure.
- Owner-supplied target hardware/OS/topology inventory.
- Explicit authorization for implementation/runtime work.

## 6. Evidence and disposition

This proposal is based on the source pins above and the existing Wave 04 authority/security reconciliation. It records a controlled proposed interpretation, not an accepted contract revision. No source in `main` was changed by this proposal. No code was executed; no tests, installs, provider/model calls, credentials, host/runtime inspection, qualification, deployment, infrastructure change or branch integration occurred.

**Next bounded step:** independently re-fetch and close the exact field/path plus producer/consumer references for AUTH-03, then prepare a minimal owner/governance review packet. Do not edit normative sources until explicit change authorization is given.
