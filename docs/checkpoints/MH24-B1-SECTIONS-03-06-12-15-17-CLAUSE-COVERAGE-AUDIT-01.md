# MH-24 — Literal Clause-Coverage Audit for Baseline 1.0 §§3–6, 12, 15–17

**Date:** 2026-10-12  
**Status:** DOCUMENTARY AUDIT / OPEN — no baseline amendment, governance decision, implementation, qualification or release authorization.  
**Purpose:** Map each independently meaningful sentence, list item, sequence, prohibition and condition in eight B1 sections to Batch 04 record(s), and distinguish literal source requirements from derived acceptance controls.

## 1. Sources and authority

| Source | Ref | Blob SHA | Role |
|---|---|---|---|
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Normative source clauses |
| `docs/checkpoints/mediahub-functional-baseline-2.0.md` | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Candidate successor mapping only |
| `docs/checkpoints/MH24-ATOMIC-TRACEABILITY-BACKLOG-04.md` | `docs/mediahub-chat-tree-map-20261012` | `26163e6f60b44e997560212bf7de9900210b7ed3` | Candidate atomic anchors |
| `docs/checkpoints/MH24-BATCH-04-INDEPENDENT-REVIEW-01.md` | `docs/mediahub-chat-tree-map-20261012` | `b31f2f3f1a2e4c594aeed38dc79a83974d2c44fa` | Prior record-level review |

B1 is immutable normative source under the reviewed instruction. This audit does not reconcile B1 and B2 by implication. B2 classifications are limited to literal text located in the reviewed B2 file; “NOT LOCATED” is not a claim of global absence. All implementation/evidence status remains OPEN unless separately proven.

## 2. Disposition vocabulary

- **COVERED-ANCHOR** — a Batch 04 record names the clause/topic; this is traceability presence, not proof the requirement is atomic or implemented.
- **PARTIAL-MAP** — B2 expresses a related principle but not the exact source detail.
- **EXPLICIT-MAP** — B2 states the same core invariant, without proving implementation.
- **NOT-LOCATED** — exact detail not found in the reviewed B2 clauses.
- **DERIVED-CONTROL** — useful acceptance/security control added beyond literal B1 wording; must be labelled as such.
- **SPLIT/REFINE** — one record covers independently verifiable obligations or loses a source detail.
- **OPEN** — owner decision, canonical contract, acceptance criteria or evidence is missing.

## 3. Clause-by-clause register

### §3 — State Authority

| Clause ID | Literal source atom | Batch 04 link | B2 relation | Audit result / required follow-up |
|---|---|---|---|---|
| B1-03-01 | MediaHub State Authority is the sole canonical source of truth for platform state. | SA4-01 | EXPLICIT, B2 §3 | COVERED-ANCHOR; implementation evidence OPEN. |
| B1-03-02 | Authority owns system state. | SA4-02 | PARTIAL, B2 §§3–4/13 | COVERED-ANCHOR; separate schema/owner trace needed. |
| B1-03-03 | Authority owns MediaHub-object state. | SA4-02 | PARTIAL, B2 §§3–4/13 | SPLIT/REFINE from system state; separate acceptance criterion. |
| B1-03-04 | Authority owns user-configuration state. | SA4-03 | PARTIAL, B2 §§3/13/19 | COVERED-ANCHOR; configuration state machine needed. |
| B1-03-05 | Authority owns resource lifecycle. | SA4-03 | PARTIAL, B2 §§3/13/19 | SPLIT/REFINE from user configuration; lifecycle contract needed. |
| B1-03-06 | Authority is responsible for authorization of state-changing operations. | SA4-04 | PARTIAL, B2 §6 | COVERED-ANCHOR; exact authorization-to-mutation path is a derived acceptance control, not fully specified by this clause. |
| B1-03-07 | Authority is responsible for consistency. | SA4-05 | PARTIAL, B2 §§3/13/19/23 | SPLIT/REFINE; consistency contract and invariants needed. |
| B1-03-08 | Authority is responsible for provenance. | SA4-05 | PARTIAL, B2 §§3/13/19/23 | SPLIT/REFINE; provenance schema and lineage criteria needed. |
| B1-03-09 | Authority is responsible for audit. | SA4-05 | PARTIAL, B2 §§3/13/19/23 | SPLIT/REFINE; audit event/schema and retention criteria needed. |
| B1-03-10 | Authority is responsible for recovery. | SA4-05 | PARTIAL, B2 §§3/13/19/23 | SPLIT/REFINE; recovery state and failure acceptance needed. |
| B1-03-11 | Authority is responsible for migration. | SA4-05 | PARTIAL, B2 §§3/13/19/23 | SPLIT/REFINE; migration contract and provenance preservation needed. |
| B1-03-12 | AI cannot become an alternate canonical platform-state source. | SA4-06 | EXPLICIT, B2 §§3/18 | COVERED-ANCHOR; direct mutation/bypass negative test OPEN. |
| B1-03-13 | Cloud component cannot become an alternate canonical platform-state source. | SA4-06 | EXPLICIT, B2 §§3/18 | COVERED-ANCHOR; remote mutation negative test OPEN. |
| B1-03-14 | Mobile app cannot become an alternate canonical platform-state source. | SA4-06 | EXPLICIT, B2 §§3/18 | COVERED-ANCHOR; mobile write-path negative/contract test OPEN. |
| B1-03-15 | Home Assistant UI cannot become an alternate canonical platform-state source. | SA4-06 | EXPLICIT, B2 §§3/18 | COVERED-ANCHOR; direct UI/backend write boundary OPEN. |
| B1-03-16 | External ecosystem cannot become an alternate canonical platform-state source. | SA4-06 | PARTIAL, B2 §§3/18 | COVERED-ANCHOR; enumerate ecosystem ingress paths and prove no second authority. |
| B1-03-17 | Separate automation engine cannot become an alternate canonical platform-state source. | SA4-06 | EXPLICIT, B2 §§3/18 | COVERED-ANCHOR; direct engine write-path negative test OPEN. |
| B1-03-18 | Ambiguous authority decisions must fail closed. | SA4-07 | EXPLICIT, B2 §§3–4 | COVERED-ANCHOR; deterministic failure contract/evidence OPEN. |
| B1-03-19 | State Authority failure must not create alternate authority. | SA4-07 | EXPLICIT, B2 §§3–4 | COVERED-ANCHOR; fault-injection/recovery evidence OPEN. |

### §4 — Home Assistant Core

| Clause ID | Literal source atom | Batch 04 link | B2 relation | Audit result / required follow-up |
|---|---|---|---|---|
| B1-04-01 | Home Assistant Core is the single source of truth specifically for the Smart Home domain. | HA4-01, HA4-06 | EXPLICIT/PARTIAL, B2 §§3–4/14 | COVERED-ANCHOR; make HA operational state distinct from MediaHub platform state in an accepted authority table. |
| B1-04-02 | HA Core owns integrations. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; capability ownership row needed. |
| B1-04-03 | HA Core owns devices. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; device owner/identity mapping needed. |
| B1-04-04 | HA Core owns entities. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; entity mapping needed. |
| B1-04-05 | HA Core owns states. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; clarify HA state vs canonical MediaHub platform state. |
| B1-04-06 | HA Core owns events. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; event flow/retention contract needed. |
| B1-04-07 | HA Core owns services. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; service invocation boundary needed. |
| B1-04-08 | HA Core owns triggers. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; trigger semantics needed. |
| B1-04-09 | HA Core owns conditions. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; condition semantics needed. |
| B1-04-10 | HA Core owns actions. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; action authorization boundary needed. |
| B1-04-11 | HA Core owns scenes. | HA4-02 | PARTIAL, B2 §14 | SPLIT/REFINE; scene lifecycle needed. |
| B1-04-12 | HA Core owns Smart Home automations. | HA4-02, HA4-05 | PARTIAL, B2 §14 | SPLIT/REFINE; automation owner and AI path need explicit criteria. |
| B1-04-13 | Preserve ordered path: Physical Devices → HA Integrations → HA Core → MediaHub Smart Home Layer → MediaHub API → MediaHub UI. | HA4-03 | PARTIAL, B2 §14 | COVERED-ANCHOR; exact ordered chain and each edge contract remain OPEN. |
| B1-04-14 | HA standard visual UI is not the MediaHub user interface. | HA4-04 | PARTIAL, B2 §2.3 | COVERED-ANCHOR; MH-09 is NOT ACCEPTED, so no implied acceptance. |
| B1-04-15 | Smart Home user interaction is through unified MediaHub UI. | HA4-04, UI4-01 | PARTIAL, B2 §2.3 | COVERED-ANCHOR; UI route inventory and acceptance remain OPEN. |
| B1-04-16 | AI must not bypass HA Core when creating automations. | HA4-05, AUTO4-04 | EXPLICIT, B2 §§14/18 | COVERED-ANCHOR; runtime/API/device bypass negatives OPEN. |
| B1-04-17 | AI must not bypass MediaHub Smart Home Layer when creating automations. | HA4-05, AUTO4-04 | EXPLICIT/PARTIAL, B2 §§14/18 | COVERED-ANCHOR; exact consumer path and enforcement evidence OPEN. |
| B1-04-18 | HA Core is authority for Smart Home domain. | HA4-01, HA4-06 | EXPLICIT/PARTIAL, B2 §§3–4/14 | COVERED-ANCHOR; keep scope domain-specific. |
| B1-04-19 | MediaHub State Authority is authority for platform state. | HA4-06, SA4-01 | EXPLICIT, B2 §3 | COVERED-ANCHOR; conflict resolution between scopes remains OPEN. |

### §5 — MediaHub User Interface

| Clause ID | Literal source atom | Batch 04 link | B2 relation | Audit result / required follow-up |
|---|---|---|---|---|
| B1-05-01 | Provide one user-facing visual environment. | UI4-01 | PARTIAL, B2 §2.3 | COVERED-ANCHOR; route/surface inventory needed. |
| B1-05-02 | Interface is minimalist. | UI4-02 | NOT-LOCATED in reviewed B2 clauses | COVERED-ANCHOR only; owner-approved design criteria needed. |
| B1-05-03 | Predominantly grey styling. | UI4-02 | NOT-LOCATED | COVERED-ANCHOR only; design tokens/reference needed. |
| B1-05-04 | Intuitive navigation. | UI4-02 | NOT-LOCATED | COVERED-ANCHOR only; usability acceptance rubric needed. |
| B1-05-05 | Minimize visual complexity. | UI4-02 | NOT-LOCATED | COVERED-ANCHOR only; measurable review criteria needed. |
| B1-05-06 | Provide a unified control system. | UI4-01 | PARTIAL, B2 §2.3 | COVERED-ANCHOR; function/route scope OPEN. |
| B1-05-07 | UX should feel as close as possible to Apple macOS. | UI4-03 | NOT-LOCATED | COVERED-ANCHOR only; subjective phrase requires an owner-approved rubric, without rewriting B1. |
| B1-05-08 | Retain distinct MediaHub visual identity. | UI4-03 | NOT-LOCATED | COVERED-ANCHOR only; identity/reference decision OPEN. |
| B1-05-09 | Hide technical complexity behind one interface. | UI4-04 | PARTIAL, B2 §§2–3 | COVERED-ANCHOR; distinguish presentation requirement from derived no-authority tests. |
| B1-05-10 | User must not switch among fragmented component interfaces. | UI4-01, HA4-04 | PARTIAL, B2 §2.3 | COVERED-ANCHOR; inventory component UI exposure and exceptions. |

### §6 — Smart Home

| Clause ID | Literal source atom | Batch 04 link | B2 relation | Audit result / required follow-up |
|---|---|---|---|---|
| B1-06-01 | Smart Home support must scale. | SH4-01 | PARTIAL, B2 §14 | COVERED-ANCHOR; scale criteria not quantified. |
| B1-06-02 | Use an extensible adapter/integration layer. | SH4-01 | PARTIAL, B2 §14 | COVERED-ANCHOR; accepted adapter contract OPEN. |
| B1-06-03 | Support lighting. | SH4-02 | PARTIAL, B2 §14 | COVERED-ANCHOR; required/optional/deferred disposition OPEN. |
| B1-06-04 | Support climate. | SH4-02 | PARTIAL, B2 §14 | Same as above. |
| B1-06-05 | Support security systems. | SH4-02 | PARTIAL, B2 §14 | Same as above; safety class and fail-safe behavior needed. |
| B1-06-06 | Support cameras. | SH4-02 | PARTIAL, B2 §14 | Capability/data-access disposition OPEN. |
| B1-06-07 | Support intercoms. | SH4-02 | PARTIAL, B2 §14 | Capability/data-access disposition OPEN. |
| B1-06-08 | Support sensors. | SH4-02 | PARTIAL, B2 §14 | Capability/schema disposition OPEN. |
| B1-06-09 | Support actuators. | SH4-02 | PARTIAL, B2 §14 | Authorization/safety disposition OPEN. |
| B1-06-10 | Support electrical power systems. | SH4-02 | PARTIAL, B2 §14 | Capability/safety disposition OPEN. |
| B1-06-11 | Support network equipment. | SH4-02 | PARTIAL, B2 §14 | Capability/credential boundary OPEN. |
| B1-06-12 | Support controllers. | SH4-02 | PARTIAL, B2 §14 | Identity/ownership disposition OPEN. |
| B1-06-13 | Support hubs. | SH4-02 | PARTIAL, B2 §14 | Identity/ownership disposition OPEN. |
| B1-06-14 | Support wired systems. | SH4-02 | PARTIAL, B2 §14 | Connection/capability matrix OPEN. |
| B1-06-15 | Support wireless systems. | SH4-02 | PARTIAL, B2 §14 | Connection/capability matrix OPEN. |
| B1-06-16 | Equipment discovery is automatic. | SH4-03 | PARTIAL, B2 §§8/14 | COVERED-ANCHOR; discovery semantics and permissions OPEN. |
| B1-06-17 | Determine device identity. | SH4-04 | PARTIAL, B2 §14 | COVERED-ANCHOR; identity schema OPEN. |
| B1-06-18 | Determine manufacturer. | SH4-04 | PARTIAL, B2 §14 | SPLIT/REFINE; field-level evidence and unknown behavior OPEN. |
| B1-06-19 | Determine model. | SH4-04 | PARTIAL, B2 §14 | SPLIT/REFINE; field-level evidence and unknown behavior OPEN. |
| B1-06-20 | Determine connection method. | SH4-04 | PARTIAL, B2 §14 | SPLIT/REFINE; connection taxonomy and unknown behavior OPEN. |
| B1-06-21 | Check compatibility. | SH4-05 | PARTIAL, B2 §§8/14 | COVERED-ANCHOR; compatibility sources/version rules OPEN. |
| B1-06-22 | Offer installation of the required integration. | SH4-06 | PARTIAL, B2 §14 | COVERED-ANCHOR; “offer” vs automatic installation must be specified. |
| B1-06-23 | Create required configuration. | SH4-06 | PARTIAL, B2 §§14/19 | COVERED-ANCHOR; mutation authorization/confirmation policy OPEN. |
| B1-06-24 | Expose the device through unified MediaHub UI. | SH4-07 | PARTIAL, B2 §14 | COVERED-ANCHOR; admitted capability→UI trace OPEN. |
| B1-06-25 | Maximize compatibility. | SH4-01, SH4-07 | PARTIAL, B2 §14 | Product objective, not directly testable until owner defines measurable criteria. |
| B1-06-26 | Do not restrict architecture to one manufacturer. | SH4-01 | PARTIAL, B2 §14 | COVERED-ANCHOR; vendor-neutral conformance criterion OPEN. |
| B1-06-D01 | Discovery must not itself imply trust/enrollment. | SH4-03 | Derived control; B2 §§4/6/14 and MH-17 related | **Not literal B1 wording.** Keep as derived security acceptance criterion with source/dependency labels. |
| B1-06-D02 | Compatibility must be checked before offering integration. | SH4-05 | Derived ordering interpretation | B1 says check compatibility and offer installation but does not unambiguously specify this exact temporal ordering; owner/contract confirmation required. |
| B1-06-D03 | Explicit user confirmation is required for every consequential install/configuration change. | SH4-06 | Derived control | B1 does not specify confirmation scope. Record owner decision rather than present as a verbatim source requirement. |

### §12 — Smart Home Automation

| Clause ID | Literal source atom | Batch 04 link | B2 relation | Audit result / required follow-up |
|---|---|---|---|---|
| B1-12-01 | Support automations. | AUTO4-01 | PARTIAL, B2 §14 | COVERED-ANCHOR; semantics/acceptance OPEN. |
| B1-12-02 | Support scenarios. | AUTO4-01 | PARTIAL, B2 §14 | Define relation to scenes/automations. |
| B1-12-03 | Support scenes. | AUTO4-01 | PARTIAL, B2 §14 | Define HA ownership/semantics. |
| B1-12-04 | Support triggers. | AUTO4-01 | PARTIAL, B2 §14 | Define event and trigger semantics. |
| B1-12-05 | Support conditions. | AUTO4-01 | PARTIAL, B2 §14 | Define condition evaluation semantics. |
| B1-12-06 | Support actions. | AUTO4-01 | PARTIAL, B2 §14 | Define authorization and execution semantics. |
| B1-12-07 | Support schedules. | AUTO4-01 | PARTIAL, B2 §14 | Timezone, recurrence and missed-run behavior OPEN. |
| B1-12-08 | Support events. | AUTO4-01 | PARTIAL, B2 §14 | Event source/schema/retention OPEN. |
| B1-12-09 | Support presence. | AUTO4-01 | PARTIAL, B2 §14 | Presence source, confidence and privacy policy OPEN. |
| B1-12-10 | Support energy automation. | AUTO4-02 | NOT-LOCATED in reviewed B2 clauses | Explicit product scope remains OPEN. |
| B1-12-11 | Support security automation. | AUTO4-02 | NOT-LOCATED in reviewed B2 clauses | Explicit product scope remains OPEN; safety and fail-safe criteria needed. |
| B1-12-12 | AI may help create automations. | AUTO4-03 | PARTIAL, B2 §§14/18 | COVERED-ANCHOR; proposal schema/review flow OPEN. |
| B1-12-13 | AI may help change automations. | AUTO4-03 | PARTIAL, B2 §§14/18 | COVERED-ANCHOR; diff/preview/authorization criteria OPEN. |
| B1-12-14 | AI may explain automation operation. | AUTO4-03 | PARTIAL, B2 §18 | Explanation provenance/uncertainty criteria OPEN. |
| B1-12-15 | AI may create instructions. | AUTO4-03 | PARTIAL, B2 §18 | Scope/source quality criteria OPEN. |
| B1-12-16 | AI may add devices. | AUTO4-03 | PARTIAL, B2 §§14/18 | Device onboarding and authorization criteria OPEN. |
| B1-12-17 | AI receives no independent authority. | AUTO4-04 | EXPLICIT, B2 §§3/14/18 | COVERED-ANCHOR; runtime negative evidence OPEN. |
| B1-12-18 | All changes pass through controlled MediaHub mechanisms. | AUTO4-05 | PARTIAL, B2 §14 | COVERED-ANCHOR; exact path/contract OPEN. |
| B1-12-19 | All changes pass through controlled Home Assistant mechanisms. | AUTO4-05 | PARTIAL, B2 §14 | COVERED-ANCHOR; HA command path/contract OPEN. |
| B1-12-D01 | Every change must produce an auditable result. | AUTO4-05 | Derived acceptance control; B1 says controlled mechanisms but does not expressly require an audit result in this sentence. | Keep as derived control, with audit schema and evidence requirements separate. |

### §15 — Local AI

| Clause ID | Literal source atom | Batch 04 link | B2 relation | Audit result / required follow-up |
|---|---|---|---|---|
| B1-15-01 | Local AI runs directly within MediaHub Core/local system. | LAI4-01 | PARTIAL, B2 §§2.1/18 | COVERED-ANCHOR; locality boundary and offline behavior OPEN. |
| B1-15-02 | Provide local inference. | LAI4-02 | PARTIAL, B2 §18 | Model/backend support and qualification OPEN. |
| B1-15-03 | Provide natural-language interaction. | LAI4-02 | PARTIAL, B2 §18 | Supported modalities/languages and error behavior OPEN. |
| B1-15-04 | Provide analysis. | LAI4-03 | PARTIAL, B2 §18 | Analysis scope/evidence/provenance OPEN. |
| B1-15-05 | Provide user assistance. | LAI4-03 | PARTIAL, B2 §18 | Supported workflows and uncertainty UX OPEN. |
| B1-15-06 | Assist creation of automations. | LAI4-04 | PARTIAL, B2 §§14/18 | Proposal and authorization path OPEN. |
| B1-15-07 | Assist equipment configuration. | LAI4-04 | PARTIAL, B2 §§14/18 | Device capability/authorization path OPEN. |
| B1-15-08 | Create instructions. | LAI4-05 | PARTIAL, B2 §18 | Source quality/provenance acceptance OPEN. |
| B1-15-09 | Provide search. | LAI4-05 | PARTIAL, B2 §§16/18 | Search corpus/index and access filtering OPEN. |
| B1-15-10 | Work locally with data. | LAI4-05 | PARTIAL, B2 §§5/7/18 | Data classes, locality and retention criteria OPEN. |
| B1-15-11 | Support Smart Home. | LAI4-06 | PARTIAL, B2 §14 | Cross-domain capability and HA boundary OPEN. |
| B1-15-12 | Support media system. | LAI4-06 | PARTIAL, B2 §§15–16 | Link to the exact media-domain clauses and accepted contracts. |
| B1-15-13 | Assist with documents. | LAI4-06 | PARTIAL, B2 §19 | Document access/indexing/permission criteria OPEN. |
| B1-15-14 | Provide local intelligent processing. | LAI4-02, LAI4-05 | PARTIAL, B2 §18 | Broad umbrella term; owner must define scope or mark as covered by enumerated functions. |
| B1-15-15 | AI follows advisory/proposal-producing model. | LAI4-07 | EXPLICIT, B2 §§3/18 | COVERED-ANCHOR; output vs command semantics OPEN. |
| B1-15-16 | AI is not State Authority. | LAI4-07 | EXPLICIT, B2 §§3/18 | COVERED-ANCHOR; direct mutation negatives OPEN. |
| B1-15-D01 | Local AI must obey specific data boundary/retention controls. | LAI4-01/05 | Derived from B2 and privacy principles, not a separate literal B1 clause in §15. | Keep as linked cross-cutting acceptance control; do not count as extra literal §15 atom. |
| B1-15-D02 | AI outputs should express uncertainty/provenance rather than canonical fact. | LAI4-03 | Derived acceptance control | Separate from the literal “analysis/help” capabilities and define acceptance criteria. |

### §16 — Local Cluster AI

| Clause ID | Literal source atom | Batch 04 link | B2 relation | Audit result / required follow-up |
|---|---|---|---|---|
| B1-16-01 | Provide distributed computation inside trusted MediaHub Cluster. | CLAI4-01 | PARTIAL, B2 §§9–11 | COVERED-ANCHOR; cluster trust/admission criteria OPEN. |
| B1-16-02 | Support heavier inference. | CLAI4-02 | PARTIAL, B2 §§8–11/18 | Capability profile/resource envelope OPEN. |
| B1-16-03 | Support batch processing. | CLAI4-02 | PARTIAL, B2 §§8–11 | Workload class and failure semantics OPEN. |
| B1-16-04 | Support computer vision. | CLAI4-02 | PARTIAL, B2 §§8–11 | Data access/privacy and capability profile OPEN. |
| B1-16-05 | Support media processing. | CLAI4-02 | PARTIAL, B2 §§8–11/17 | Codec/GPU/resource requirements OPEN. |
| B1-16-06 | Support AI generation. | CLAI4-02 | PARTIAL, B2 §§8–11/18 | Model/safety/resource profile OPEN. |
| B1-16-07 | Support engineering calculations. | CLAI4-02 | PARTIAL, B2 §§8–11/17 | Workload correctness and resource profile OPEN. |
| B1-16-08 | Support Digital Twin workloads. | CLAI4-02 | PARTIAL, B2 §§8–11/17 | Exact workload and data boundary mapping OPEN. |
| B1-16-09 | Support distributed tasks. | CLAI4-02 | PARTIAL, B2 §§8–11 | Scheduling, retries and partial-failure semantics OPEN. |
| B1-16-10 | Access is regulated by MediaHub AI Gateway. | CLAI4-03 | PARTIAL; exact named gateway NOT-LOCATED in reviewed B2 clauses | COVERED-ANCHOR in Batch 04, but named-component acceptance/contract OPEN. |
| B1-16-D01 | Nodes must be independently qualified and route by capability/resources/failure state. | CLAI4-04/05 | Derived detailed control; not fully enumerated in literal §16 text. | Retain as derived acceptance/qualification criteria, not literal source atoms. |

### §17 — Cloud Development AI

| Clause ID | Literal source atom | Batch 04 link | B2 relation | Audit result / required follow-up |
|---|---|---|---|---|
| B1-17-01 | Cloud Development AI is a corporate compute environment for MediaHub company needs. | CDAI4-01 | EXPLICIT/PARTIAL, B2 §§1–2/11 | COVERED-ANCHOR; domain owner and runtime boundary evidence OPEN. |
| B1-17-02 | Cloud Development AI is a separate level after Local Cluster AI. | CDAI4-01 | PARTIAL, B2 §§1–2/11 | Preserve layer ordering and dependency direction in a versioned topology. |
| B1-17-03 | Include website infrastructure. | CDAI4-02 | PARTIAL, B2 §§2/11/17/21 | Named component inventory/owner disposition OPEN. |
| B1-17-04 | Include Trusted Sources Intelligence Engine. | CDAI4-02 | NOT-LOCATED as exact named subsystem in reviewed B2 clauses | Explicit preserve/revise/defer decision needed; generic AI references do not close it. |
| B1-17-05 | Include AI Human Clone. | CDAI4-02 | NOT-LOCATED as exact named subsystem in reviewed B2 clauses | Explicit preserve/revise/defer decision needed; do not infer scope or implementation. |
| B1-17-06 | Include engineering development. | CDAI4-02 | PARTIAL, B2 §§11/17 | Workload scope/ownership OPEN. |
| B1-17-07 | Include Digital Twin workloads. | CDAI4-02 | PARTIAL, B2 §§11/17 | Workload scope/data boundary OPEN. |
| B1-17-08 | Include commercial MediaHub infrastructure. | CDAI4-02 | PARTIAL, B2 §§2/11/21 | Component and environment inventory OPEN. |
| B1-17-09 | Include development infrastructure. | CDAI4-02 | PARTIAL, B2 §§11/17/21 | Ownership/access/lifecycle inventory OPEN. |
| B1-17-10 | Include CI/CD. | CDAI4-02 | PARTIAL, B2 §§11/17/21 | Pipeline ownership and release authorization OPEN. |
| B1-17-11 | Include GPU computing. | CDAI4-02 | PARTIAL, B2 §§8–11/17 | GPU capability/resource contract OPEN. |
| B1-17-12 | Include heavy AI tasks. | CDAI4-02 | PARTIAL, B2 §§8–11/18 | Workload taxonomy and routing criteria OPEN. |
| B1-17-13 | Include storage/processing of permitted data. | CDAI4-02/05 | PARTIAL, B2 §§5–7/11 | Data classification, residency, retention and egress policy OPEN. |
| B1-17-14 | Include commercial infrastructure operations. | CDAI4-02 | PARTIAL, B2 §§2/11/21 | Operational scope/owner inventory OPEN. |
| B1-17-15 | Ordinary users have no direct access to Cloud Development AI/Environment. | CDAI4-03 | EXPLICIT/PARTIAL, B2 §§2.2–2.3/5 | COVERED-ANCHOR; role matrix and cross-domain negative tests OPEN. |
| B1-17-16 | Local AI may request cloud compute. | CDAI4-04 | EXPLICIT/PARTIAL, B2 §§7–8/11/18 | COVERED-ANCHOR; approved request path/reason codes OPEN. |
| B1-17-17 | Local Cluster AI may request cloud compute. | CDAI4-04 | EXPLICIT/PARTIAL, B2 §§7–8/11/18 | SPLIT/REFINE from Local AI requester; separate identity/capability policy needed. |
| B1-17-18 | Cloud compute may be requested if local resources are insufficient. | CDAI4-04 | PARTIAL, B2 §§8/11 | Threshold/measurement/reason-code contract OPEN. |
| B1-17-19 | Escalation requires policy permission. | CDAI4-04/05 | EXPLICIT, B2 §§5–7/18 | COVERED-ANCHOR; enforcement evidence OPEN. |
| B1-17-20 | Escalation requires confidentiality level to permit transfer. | CDAI4-04/05 | EXPLICIT/PARTIAL, B2 §§5–7 | Data classification/transfer policy and negative tests OPEN. |
| B1-17-21 | Authorization requirements must be satisfied. | CDAI4-05 | EXPLICIT, B2 §§5–7 | COVERED-ANCHOR; identity/capability trace OPEN. |
| B1-17-22 | Residency requirements must be satisfied. | CDAI4-05 | EXPLICIT, B2 §§5–7/11 | COVERED-ANCHOR; region/provider enforcement evidence OPEN. |
| B1-17-23 | Egress requirements must be satisfied. | CDAI4-05 | EXPLICIT, B2 §§5–7/11 | COVERED-ANCHOR; destination/egress policy and denial evidence OPEN. |
| B1-17-24 | Cloud is not MediaHub authority. | CDAI4-06 | EXPLICIT, B2 §§3–5/18 | COVERED-ANCHOR; remote mutation negative tests OPEN. |
| B1-17-D01 | Remote result is data, not canonical mutation. | CDAI4-06 | Derived operational expression of cloud non-authority | Keep as derived acceptance criterion linked to B1-17-24. |
| B1-17-D02 | No arbitrary fallback destinations; provider allowlist/qualification required. | CDAI4-07 | Derived detailed control; B1 §17 does not spell out the full fallback policy. | Separate from literal source; needs owner-approved provider/routing policy. |
| B1-17-D03 | Cloud failure must not disable critical local functions. | CDAI4-07 | Derived resilience criterion | Separate acceptance requirement and define “critical local function”; do not attribute as verbatim B1 §17 text. |

## 4. Coverage summary

- Eight source sections were read from the exact B1 `main` blob SHA `9df4892ed0734050ac79732603d15bb414717310`.
- Batch 04 has anchors for all eight sections and 48 unique record IDs, confirmed in the independent review.
- This audit enumerates **153 unique clause/control IDs** across the eight sections, verified by read-back count; the stable IDs in the tables are the audit register. The count includes separate authority actors, HA primitives, device categories, automation primitives, AI functions, cloud subsystems and conditional escalation gates. It intentionally separates D-coded derived controls from literal B1 atoms.
- **No omission-free claim:** this is a human-structured clause decomposition, not an automated formal proof. A subsequent reviewer should validate the row count against a mechanically extracted sentence/bullet inventory and confirm no punctuation/line-wrap item was missed.
- **Coverage is not closure:** all linked Batch 04 records remain OPEN. “COVERED-ANCHOR” confirms a candidate record exists, not that it is truly atomic, accepted in B2, implemented, tested or qualified.
- Batch 04 compound-record findings remain: split/refine at least SA4-05, HA4-02, SH4-02/06, AUTO4-01/03, LAI4-05, CLAI4-02, CDAI4-02/07; retain all derived-control labels in this audit.
- Exact details not located in the reviewed B2 text include the UI style/identity language, explicit energy/security automation categories, the exact named “MediaHub AI Gateway”, and the exact named Trusted Sources Intelligence Engine / AI Human Clone. This is not a decision to remove or amend those B1 requirements.
- Governance conflict between the MH-24 matrix label `RECONCILIATION CANDIDATE` and B2/reconciliation-report acceptance language remains unresolved.

## 5. Actions and next safe step

No B1/B2/matrix/source backlog was edited. No status was upgraded. No tests, qualification, installation, deployment, infrastructure/production action or merge to `main` occurred.

Next: independently validate this register’s extraction/count against the literal B1 file; then make a separately traceable proposal to normalize Batch 04 (48 not 47, split compound records, label derived controls). Keep all statuses OPEN until governance, canonical contract refs, acceptance criteria and evidence exist.
