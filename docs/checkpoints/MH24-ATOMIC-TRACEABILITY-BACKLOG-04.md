# MH-24 Atomic Traceability Backlog — Batch 04

**Date:** 2026-10-12  
**Status:** OPEN BACKLOG / DOCUMENTARY PLANNING ONLY  
**Scope:** Baseline 1.0 §§3–6, §12, §§15–17, which GAP REPORT 01 identified as lacking dedicated atomic anchors. This is not a Baseline amendment, closure report or implementation authorization.

## 1. Verified sources

| Source | Ref | Blob SHA | Scope/status |
|---|---|---|---|
| specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md | main | 9df4892ed0734050ac79732603d15bb414717310 | Historical provenance; exact clauses |
| docs/checkpoints/mediahub-functional-baseline-2.0.md | main | 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f | Declares accepted/canonical B2; no implementation inferred |
| docs/checkpoints/mediahub-mh24-traceability-matrix.md | main | 8bdd364493ebbe2ef6f87400f80bc7eca8fb95c6 | Rows 3–6, 12, 15–17; status conflict open |
| docs/checkpoints/MH24-ATOMIC-TRACEABILITY-GAP-REPORT-01.md | docs/mediahub-chat-tree-map-20261012 | 1f500d468dd7e9a9b9ca477a06344dd850410374 | Confirms missing anchors |
| docs/architecture/MH-10-CHAT-MASTER-PROMPT.md | main | 6ea847ddbf1604878303572b21b506102b23c930 | AI advisory/non-authority |
| docs/architecture/MH-21-CHAT-MASTER-PROMPT.md | main | 61d552db4d1a1abefa2cef9f44eebcf634d11111 | Cloud boundary, controlled egress |
| docs/architecture/MH-17-master-prompt.md | main | a750ee5b292043a1f1b18ec317a4b5b2c44aad24 | Device identity/trust/capability |
| architecture/MH-03-master-prompt.md | architecture/mh3-runtime-foundation-20260930 | e99035f596e236645bf8f2235fc4d375716ce476 | Runtime/State Authority; proposed status |
| docs/architecture/mh-04/MH-04-master-prompt.md | architecture/mh-04-security-trust-authorization | 78b6374daedf30ed9290dde19e7ee43a495faf05 | Identity, capability, authorization, fail-closed |
| docs/architecture/mh-04/MH-04-acceptance-criteria.md | architecture/mh-04-security-trust-authorization | a75f5c1849ad67cc380a0ba3552bf7f2c5ec82b6 | PROPOSED / REVIEW COMPLETE; approval and freeze separate |
| docs/architecture/MH-05-consumer-integration-boundary.md | architecture/mh-05-consumer-integration-boundary | 6718905825c0f91ef21494d518b7e87dacb26ae0 | PROPOSED; implementation NOT AUTHORIZED |
| docs/architecture/MH-05-acceptance-criteria.md | architecture/mh-05-consumer-integration-boundary | db18ab4416516240af394a6a9f57831f95edb802 | NOT ACCEPTED — REQUIRES VERIFICATION |
| docs/architecture/MH-09-master-prompt.md | architecture/mh-09-presentation-ui | b20577df2a4fdd32efc2a040a7b7a1f4a5302dee | UI consumer/non-authority |
| docs/architecture/MH-09-acceptance-criteria.md | architecture/mh-09-presentation-ui | 09dd9a3bab69ea039152a3aeaaac830b8961ab8b | NOT ACCEPTED; implementation authorization NOT GRANTED |

MH-03/MH-04/MH-05/MH-09 sources are branch-specific. Their presence does not imply acceptance, freeze, synchronization to main or production authorization.

## 2. Atomic requirements

All entries remain OPEN. B2 relation is a documentary classification, not an implementation claim. Closure requires exact B2 mapping, canonical contract path/ref, owner decision where applicable, acceptance criteria and evidence.

| ID | B1 source | Atomic requirement | Candidate B2 mapping / dependencies | Closure evidence required | Status |
|---|---|---|---|---|---|
| SA4-01 | §3 opening | MediaHub State Authority is the single canonical source of platform state. | B2 §3; MH-03/P0-03/P0-04 | Versioned authority contract, owner/ref and authority-path evidence. | OPEN |
| SA4-02 | §3 responsibility list | State Authority owns system state and MediaHub-object state. | B2 §§3–4/13; MH-03/MH-14 | Object/schema inventory mapped to authoritative mutation owner. | OPEN |
| SA4-03 | §3 responsibility list | User configurations and resource lifecycle remain under the canonical authority path. | B2 §§3/13/19; MH-03/MH-14/MH-16 | Configuration/resource state machine and mutation-path trace. | OPEN |
| SA4-04 | §3 responsibility list | State-changing operations require authorization before canonical mutation. | B2 §6; MH-04/MH-05 are not accepted/frozen | Principal→capability→policy→authorization→consumer boundary→State Authority trace and negative cases. | OPEN |
| SA4-05 | §3 responsibility list | Consistency, provenance, audit, recovery and migration preserve authority identity and canonical history. | B2 §§3/13/19/23; MH-14/MH-16/MH-20/MH-23 | Per-lifecycle contract, provenance and recovery/migration acceptance evidence. | OPEN |
| SA4-06 | §3 prohibition | AI, cloud, mobile, HA UI, external ecosystems and automation engines cannot become alternate platform-state authorities. | B2 §§3/18; MH-03/04/05/09/10/21 | Actor/path inventory and bypass-negative tests. | OPEN |
| SA4-07 | §3 fail-closed | Ambiguous authority decisions fail closed; State Authority failure never creates fallback authority. | B2 §§3–4; MH-03/04/05 | Failure contract, deterministic rejection, fault-injection evidence and recovery criteria. | OPEN |
| HA4-01 | §4 first paragraph | HA Core is the sole operational/device-state authority for Smart Home. | B2 §3; MH-05/MH-17 | Accepted STATE-HA contract ref/SHA defining HA-owned state. | OPEN |
| HA4-02 | §4 responsibility list | HA Core owns integrations, devices, entities, states, events, services, triggers, conditions, actions, scenes and Smart Home automations. | B2 §14; MH-05/MH-17 | Capability/ownership matrix for each primitive and downstream representation. | OPEN |
| HA4-03 | §4 architecture chain | Preserve Physical Devices → HA Integrations → HA Core → MediaHub Smart Home Layer → MediaHub API → MediaHub UI. | B2 §14/matrix row 4; MH-05/09/17 | Versioned flow diagram and contract ref for every edge. | OPEN |
| HA4-04 | §4 UI paragraph | HA standard UI is not MediaHub UI; Smart Home user interaction uses unified MediaHub UI. | B2 §2.3; MH-09 acceptance NOT ACCEPTED | UI boundary contract, route inventory and governance decision. | OPEN |
| HA4-05 | §4 AI paragraph | AI-created automations do not bypass HA Core or MediaHub Smart Home Layer. | B2 §§14/18; MH-10/05/17 | Proposal/command path and bypass-negative tests. | OPEN |
| HA4-06 | §4 final distinction | Preserve separate authority scopes: HA Core for Smart Home, State Authority for platform state. | B2 §3; MH-03/05/17 | Cross-domain authority table, conflict contract and scope-escalation negatives. | OPEN |
| UI4-01 | §5 opening | Provide one coherent MediaHub user-facing visual environment rather than fragmented component interfaces. | B2 §2.3/product principles; MH-09 NOT ACCEPTED | UI domain/route inventory, dependency direction and governance acceptance. | OPEN |
| UI4-02 | §5 visual requirements | Preserve minimal, predominantly grey, intuitive, low-complexity visual language. | Exact design tokens not established by B2 text checked; MH-09 | Design tokens, accessibility constraints, approved design reference and visual acceptance criteria. | OPEN |
| UI4-03 | §5 UX/identity | UX should feel close to macOS while retaining distinct MediaHub identity. | Subjective intent; MH-09 | Owner-approved interpretation, reference set and review rubric. | OPEN |
| UI4-04 | §5 complexity clause | Hide component/backend complexity behind unified presentation without granting UI authority. | B2 §§2–3; MH-05/09 | Read-model/command contracts, authority-negative tests and error-state acceptance. | OPEN |
| SH4-01 | §6 opening | Support a scalable adapter/integration layer not restricted to one vendor. | B2 §14; MH-05/17 | Accepted adapter contract and vendor-neutral capability model. | OPEN |
| SH4-02 | §6 domain list | Scope includes lighting, climate, security, cameras, intercoms, sensors, actuators, power, network equipment, controllers, hubs, wired and wireless systems. | B2 §14; MH-05/17 | Domain/capability catalogue marking required, optional, unsupported and candidate. | OPEN |
| SH4-03 | §6 discovery | Equipment discovery must not imply trust or enrollment. | B2 §§8/14; MH-17 | Discovery→identity→trust→capability→authorization lifecycle and spoofing/unknown-device negatives. | OPEN |
| SH4-04 | §6 identification bullets | Identify device, manufacturer, model and connection method on discovery. | B2 §§8/14; MH-17 | Versioned identity schema, unknown-field behavior and evidence provenance. | OPEN |
| SH4-05 | §6 compatibility | Check compatibility before offering/configuring an integration. | B2 §8; MH-17 | Compatibility matrix, version constraints and fail-closed handling of unknown compatibility. | OPEN |
| SH4-06 | §6 install/configure | Required integration installation/configuration is controlled and authorized; define which consequential changes require user confirmation. | B2 lifecycle; MH-05/17/16 | Approved onboarding state machine, permission/confirmation UX and rollback evidence. | OPEN |
| SH4-07 | §6 UI/goal | Expose admitted device capabilities through unified MediaHub UI while preserving vendor-neutral extensibility. | B2 §14/matrix rows 6/28; MH-05/09/17 | Capability→domain model→authorized read model→UI trace and conformance tests. | OPEN |
| AUTO4-01 | §12 automation inventory | Support automations, scenarios, scenes, triggers, conditions, actions, schedules, events and presence workflows. | B2 §14; MH-05/06/17 | Capability matrix and supported/unsupported semantics per primitive. | OPEN |
| AUTO4-02 | §12 categories | Energy and security automation are explicit functional categories. | B2 §14; MH-04/05/17 | Safety class, permissions, fail-safe behavior and category-specific acceptance criteria. | OPEN |
| AUTO4-03 | §12 AI assistance | AI may help create/change automations, explain them, generate instructions and add devices. | B2 §§14/18; MH-10/05/17 | Proposal schema and review/preview/explanation/rejection workflow. | OPEN |
| AUTO4-04 | §12 no AI authority | AI has no independent authority to change automation or device state. | B2 §§3/14/18; MH-10/04/05 | Authorization contract and adversarial direct-tool/API/device bypass tests. | OPEN |
| AUTO4-05 | §12 controlled mechanisms | Every AI-originated automation change traverses controlled MediaHub/HA mechanisms and produces an auditable result. | B2 §14; MH-05 is proposed and implementation unauthorized | End-to-end command trace, audit schema, rejection and unknown-outcome tests. | OPEN |
| LAI4-01 | §15 location | Local AI runs within MediaHub Core/local system and respects local data boundaries. | B2 §§2.1/18; MH-10/03/14 | Local capability profile, data-flow inventory and offline evidence. | OPEN |
| LAI4-02 | §15 inference/NL | Local AI provides inference and natural-language interaction within qualified model/backend capabilities. | B2 §18; MH-10 | Model/backend contracts, resource envelope and qualification evidence. | OPEN |
| LAI4-03 | §15 analysis/help | Local AI supports analysis/user assistance without presenting uncertain inference as canonical fact or authorization. | B2 §§3/18; MH-10 | Provenance/confidence contract, uncertainty UX and no-authority tests. | OPEN |
| LAI4-04 | §15 automation/setup | Local AI assists automation creation and equipment setup only through approved proposal/policy/authorization paths. | B2 §§14/18; MH-10/05/17 | Use-case matrix, proposal schema, authorization trace and denied-path tests. | OPEN |
| LAI4-05 | §15 instructions/search/data | Local AI supports instructions, search and local data processing with provenance, privacy and access controls. | B2 §§7/16/18; MH-10/14/19 | Retrieval/data classification contract, source provenance and access-control tests. | OPEN |
| LAI4-06 | §15 cross-domain | Smart Home, media and document assistance preserves each domain's authority and authorization boundary. | B2 §§3/14–18; MH-05/10/18/19 | Domain capability/command matrix and boundary-negative tests. | OPEN |
| LAI4-07 | §15 advisory model | Local AI is advisory/proposal-producing and never State Authority. | B2 §§3/18; MH-10 | AI output/command distinction and mutation-path bypass tests. | OPEN |
| CLAI4-01 | §16 distributed execution | Local Cluster AI computes only within the trusted MediaHub Cluster. | B2 §§9–11; MH-10/21/03 | Cluster trust model, node identity/admission contract and topology qualification. | OPEN |
| CLAI4-02 | §16 workload list | Workloads include heavy inference, batch, computer vision, media processing, generation, engineering calculations, Twin workloads and distributed jobs. | B2 §§8–11/17–18; MH-10/19/21 | Workload taxonomy, resource requirements, capability profiles and unsupported-case behavior. | OPEN |
| CLAI4-03 | §16 gateway | Cluster AI access/routing is governed by MediaHub AI Gateway. | B2 §§8/10–11/18; MH-10/21 | Gateway contract, authenticated workload identity, admission policy and decision logs. | OPEN |
| CLAI4-04 | §16 authority boundary | Cluster nodes/workloads gain no State Authority, policy authority or unrestricted access through membership. | B2 §§3/6/10–11/18; MH-03/04/10/21 | Node/workload escalation, credential-scope and cross-domain negative tests. | OPEN |
| CLAI4-05 | §16 capability/failure | Routing respects node capability, resource limits, failure/unknown outcomes and qualified workload profile. | B2 §§8–10; MH-10/21/22 | Scheduler contract, capacity/failure plan and independently reviewed evidence when authorized. | OPEN |
| CDAI4-01 | §17 corporate domain | Cloud Development AI is a corporate compute domain distinct from the local user cluster. | B2 §§1–2/11; MH-21/23 | Network/identity/data-plane boundary and domain ownership decision. | OPEN |
| CDAI4-02 | §17 component inventory | Cloud scope includes website, Trusted Sources, AI Human Clone, engineering/Twin, commercial/development infrastructure, CI/CD, GPU, heavy AI, approved-data storage/processing and commercial operations. | B2 §§2/11/17/21; MH-21/19/20/23 | Subsystem inventory with owner, purpose, data class, access scope, evidence and lifecycle. | OPEN |
| CDAI4-03 | §17 user access | Ordinary users do not gain direct Cloud Development Environment access merely by being MediaHub users. | B2 §§2.2–2.3/5; MH-21/04/09 | Identity/role matrix and negative tests for user/developer cross-access. | OPEN |
| CDAI4-04 | §17 controlled escalation | Local/cluster AI may request cloud compute only if local resources are insufficient, policy allows and confidentiality permits transfer. | B2 §§7–8/11/18; MH-10/21 | Routing contract with reason codes, resource threshold, data class and denial path. | OPEN |
| CDAI4-05 | §17 egress/residency | Escalation satisfies authorization, residency and egress requirements before local data transfer. | B2 §§5–7/11; MH-04/21 | Data-flow inventory, residency/egress policy, audit and unauthorized-destination negatives. | OPEN |
| CDAI4-06 | §17 cloud non-authority | Cloud Development AI is not State Authority; remote results are data, not canonical mutations. | B2 §§3/18; MH-03/10/21 | Remote result contract, provenance/validation and direct-mutation negative tests. | OPEN |
| CDAI4-07 | §17 provider/failure | Providers remain candidates until evidence/ADR/qualification; arbitrary fallback/destinations are forbidden and cloud failure cannot disable critical local operation. | B2 §§1/8–11; MH-10/21/22 | Provider decisions, fallback allowlist, local critical-capability matrix and failure qualification. | OPEN |

## 3. Cross-cutting issues

| ID | Issue | Required disposition | Status |
|---|---|---|---|
| X4-01 | Platform authority vs HA Smart Home authority | Define scopes and conflict boundaries without flattening authorities or creating a second platform authority. | OPEN |
| X4-02 | Exact B1 to B2 mapping | Classify each item EXPLICIT, PARTIAL, NOT LOCATED IN B2 or CONFLICT and cite exact clauses. | OPEN |
| X4-03 | Branch-only MH-03/04/05/09 sources | Keep refs/status separate; do not imply merge, acceptance, freeze or production. | OPEN |
| X4-04 | User confirmation | Owner defines which discovery/configuration/automation/device operations require explicit confirmation. | OPEN |
| X4-05 | UI visual intent | Convert subjective appearance language into approved design criteria without silently changing B1. | OPEN |
| X4-06 | AI data/capability profiles | Establish policy-driven classification/routing with explicit denial and degraded-mode semantics. | OPEN |
| X4-07 | Security/acceptance | MH-04 is PROPOSED / REVIEW COMPLETE; MH-05 is PROPOSED / GOVERNANCE REVIEW REQUIRED and implementation unauthorized; MH-09 is NOT ACCEPTED. | OPEN |
| X4-08 | Matrix governance conflict | Matrix says RECONCILIATION CANDIDATE while B2/report say accepted/closed; this backlog does not resolve it. | OPEN |

## 4. Closure protocol

For each item record: exact B1 clause/SHA; exact B2 clause/SHA and mapping classification; matrix row; canonical MH contract path/ref/SHA; decision owner; acceptance criteria; implementation/evidence refs; independent qualification status where required; unresolved contradictions; release and production authorization state. Related principles in B2 alone do not close an item.

## 5. Actions not taken

No Baseline, matrix, branch-specific primary source or implementation was changed. No statuses were upgraded. No software was installed, tests/qualification run, deployment or infrastructure/production action performed, and no merge to main occurred.

**Next step:** independently review these 47 atomic records and eight cross-cutting issues, then perform literal clause-level coverage against the eight source sections before consolidating Batch 01–04 into the master traceability register.
