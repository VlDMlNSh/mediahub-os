# MH-24 Batch 04 — Atomic Normalization Proposal 02

**Date:** 2026-10-12  
**Status:** PROPOSAL 02 / OPEN — NOT APPROVED; documentary planning only. This revision incorporates findings R01–R06 from independent review 01; it does not approve the normalization.  
**Scope:** Propose normalization of the 48 historical Batch 04 records against Baseline 1.0 §§3–6, 12, 15–17. Preserve all historical IDs and provenance. No baseline, matrix, governance status, implementation, qualification, or release decision is changed.

## 1. Verified inputs

| Source | Ref | Blob SHA | Role |
|---|---|---|---|
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | `docs/mediahub-chat-tree-map-20261012` | `57b1ecebef504dfabaca57248cd32c8b37a4bc90` | Historical map snapshot used when proposal 01 was drafted; not current at revision 02 |
| `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` | `docs/mediahub-chat-tree-map-20261012` | `f86014d81a2db1b5246b4fc2600812340f1c7d22` | Required process and limits |
| `docs/checkpoints/MH24-ATOMIC-TRACEABILITY-BACKLOG-04.md` | `docs/mediahub-chat-tree-map-20261012` | `26163e6f60b44e997560212bf7de9900210b7ed3` | 48 historical records + 8 cross-cutting issues |
| `docs/checkpoints/MH24-B1-SECTIONS-03-06-12-15-17-CLAUSE-COVERAGE-AUDIT-01.md` | `docs/mediahub-chat-tree-map-20261012` | `d0938f14ed4110545118f075175dee3be412097b` | 153-row source/control register |
| `docs/checkpoints/MH24-B1-SECTIONS-03-06-12-15-17-CLAUSE-COVERAGE-AUDIT-02.md` | `docs/mediahub-chat-tree-map-20261012` | `8b1f02eb07e153be825e39ec7a0289b0105d6156` | Structural count and scope validation |
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Literal source authority for this audit |

The Batch 04 source has 48 unique historical IDs despite its final line saying “47”. This proposal preserves the 48-ID inventory and records the discrepancy rather than silently rewriting the historical artifact. At the time revision 02 was prepared, the current map had Blob SHA `92df5cdaf6b4ec5bc5a470156788a024d5b193c6`; the SHA in proposal 01 is retained above only as historical provenance.

## 2. Normalization rules

1. Historical Batch 04 IDs remain immutable provenance identifiers; do not delete or recycle them.
2. Where a historical record contains multiple independently verifiable obligations, treat it as a **parent/legacy anchor** and propose child IDs below it. Do not mark the parent closed merely because children are drafted.
3. Every child must cite a literal B1 source line/span or be explicitly labelled **DERIVED CONTROL**. Derived controls must not be represented as verbatim B1 requirements.
4. Keep source requirement, B2 mapping, acceptance criteria, implementation evidence, and qualification status as separate fields/stages.
5. All proposed child records remain **OPEN / PROPOSED** until owner/governance approval, canonical contract references, acceptance criteria and evidence exist.
6. This document is a proposed crosswalk, not an updated canonical backlog or a Baseline amendment.

## 3. Proposed disposition for all 48 historical records

Source line numbers below refer to the exact B1 `main` blob SHA listed above.

| Historical ID | B1 source span | Proposed disposition | Proposed child atoms / treatment |
|---|---|---|---|
| SA4-01 | §3 lines 63–63 | RETAIN | SA4-01.a single canonical platform-state authority |
| SA4-02 | §3 lines 65–69 | SPLIT | SA4-02.a system state; SA4-02.b MediaHub-object state; SA4-02.c user configurations; SA4-02.d resource lifecycle |
| SA4-03 | §3 lines 68–69 | SPLIT / REASSIGN | SA4-03.a canonical ownership of user configurations (line 68); SA4-03.b canonical ownership of resource lifecycle (line 69). Cross-link SA4-02.c/.d; lines 65–75 are not a direct source span for these two atoms; avoid duplicate requirements |
| SA4-04 | §3 line 70 | RETAIN + CLARIFY | SA4-04.a State Authority responsibility for authorization of state-changing operations. Enforcement order/negative cases are acceptance controls, not literal B1 detail |
| SA4-05 | §3 lines 71–75 | SPLIT | SA4-05.a consistency; SA4-05.b provenance; SA4-05.c audit; SA4-05.d recovery; SA4-05.e migration. Each needs separate contract/evidence |
| SA4-06 | §3 line 77 | SPLIT | SA4-06.a AI; .b cloud; .c mobile application; .d Home Assistant UI; .e external ecosystem; .f separate automation engine cannot become alternate canonical platform authority |
| SA4-07 | §3 line 79 | SPLIT | SA4-07.a ambiguity → fail closed; SA4-07.b State Authority failure does not create alternate authority |
| HA4-01 | §4 line 85; lines 97–98 | RETAIN | HA4-01.a HA Core is authority for Smart Home domain; cross-link separate State Authority scope |
| HA4-02 | §4 line 87 | SPLIT | HA4-02.a integrations; .b devices; .c entities; .d states; .e events; .f services; .g triggers; .h conditions; .i actions; .j scenes; .k Smart Home automations |
| HA4-03 | §4 lines 89–90 | SPLIT BY EDGE | HA4-03.a Physical Devices→HA Integrations; .b HA Integrations→HA Core; .c HA Core→MediaHub Smart Home Layer; .d Smart Home Layer→MediaHub API; .e MediaHub API→MediaHub UI. Preserve order and direction |
| HA4-04 | §4 line 92 | SPLIT | HA4-04.a HA standard visual UI is not MediaHub UI; HA4-04.b Smart Home user interaction uses unified MediaHub UI |
| HA4-05 | §4 line 94 | RETAIN | AI-generated automation must not bypass HA Core or MediaHub Smart Home Layer |
| HA4-06 | §4 lines 97–98 | RETAIN | Distinct authority scopes: HA Core for Smart Home; MediaHub State Authority for platform state |
| UI4-01 | §5 lines 104, 116 | RETAIN | Unified user-facing visual environment; no forced switching among fragmented component interfaces |
| UI4-02 | §5 lines 107–111, 114 | SPLIT | UI4-02.a minimal (line 107); .b predominantly grey (108); .c intuitive navigation (109); .d minimize visual complexity (110); .e unified control system (111); .f hide technical complexity behind unified UI (114) |
| UI4-03 | §5 lines 112–113 | SPLIT | UI4-03.a macOS-like UX feel; UI4-03.b distinct MediaHub visual identity |
| UI4-04 | No independent literal span assigned yet; candidate cross-links §5 lines 104 and 116 | HOLD / REFRAME / POSSIBLE DERIVED CONTROL | Do not treat lines 104–116 as a new literal atom. Until the owner identifies a distinct residual obligation, retain UI4-04 only as a legacy anchor cross-linked to UI4-01/02/03; alternatively classify the intended presentation/authority-boundary control as DERIVED, with an explicit rationale. No duplicate normative requirement is proposed |
| SH4-01 | §6 line 122; line 136 | SPLIT | SH4-01.a scalable adapter/integration layer; SH4-01.b extensible beyond a single vendor |
| SH4-02 | §6 lines 124–125 | SPLIT BY CAPABILITY CATEGORY | SH4-02.a lighting; .b climate; .c security; .d cameras; .e intercoms; .f sensors; .g actuators; .h power; .i network equipment; .j controllers; .k hubs; .l wired systems; .m wireless systems |
| SH4-03 | §6 line 126 | RETAIN + DERIVED LABEL | Automatic equipment discovery is literal at line 126. “Discovery does not imply trust/enrollment” is a derived security control; keep it separately D-coded, not as verbatim B1. Line 136 belongs only to SH4-01.b / SH4-07 vendor-neutral compatibility and is not a discovery source |
| SH4-04 | §6 lines 127–130 | SPLIT | SH4-04.a identify device; .b identify manufacturer; .c identify model; .d identify connection method |
| SH4-05 | §6 line 131 | RETAIN | Compatibility check; keep any ordering/unknown-compatibility fail-closed behavior as a separately labelled derived acceptance control unless explicitly sourced elsewhere |
| SH4-06 | §6 lines 132–134 | SPLIT | SH4-06.a offer required integration; .b create necessary configuration; .c expose device through unified MediaHub UI. Authorization/explicit-confirmation/rollback are derived controls requiring owner policy |
| SH4-07 | §6 line 136 | RETAIN / CROSS-LINK | Vendor-neutral compatibility objective; do not duplicate UI exposure atom from SH4-06.c |
| AUTO4-01 | §12 line 204 | SPLIT | AUTO4-01.a automations; .b scenarios; .c scenes; .d triggers; .e conditions; .f actions; .g schedules; .h events; .i presence; .j energy automation; .k security automation |
| AUTO4-02 | §12 line 204 | RETAIN / CROSS-LINK | Explicit energy and security automation categories; cross-link AUTO4-01.j/.k, avoid duplicate category claims |
| AUTO4-03 | §12 line 206 | SPLIT | AUTO4-03.a assist create automations; .b assist change automations; .c explain operation; .d create instructions; .e add devices |
| AUTO4-04 | §12 line 206 | SPLIT | AUTO4-04.a AI has no independent authority; .b changes use controlled MediaHub mechanisms; .c changes use controlled Home Assistant mechanisms |
| AUTO4-05 | §12 line 206 | REFRAME | Keep only separately verifiable control-path/result evidence not already assigned to AUTO4-04.b/.c. Audit schema and mandatory result record are proposed derived acceptance controls, not verbatim B1 |
| LAI4-01 | §15 lines 232, 249 | SPLIT | LAI4-01.a runs in MediaHub Core/local system; LAI4-01.b AI is not State Authority/advisory boundary (cross-link LAI4-07 to avoid duplicate atom) |
| LAI4-02 | §15 lines 235–236 | SPLIT | LAI4-02.a local inference; LAI4-02.b natural-language control/interaction |
| LAI4-03 | §15 lines 237–238, 247 | RETAIN / SPLIT IF NEEDED | Analysis and user assistance are distinct capabilities; preserve exact capability labels and avoid implying authority |
| LAI4-04 | §15 lines 239–241, 244 | SPLIT | LAI4-04.a automation creation; .b equipment-setup assistance; .c instruction creation; .d Smart Home support |
| LAI4-05 | §15 lines 242–247 | SPLIT | LAI4-05.a search; .b local data processing; .c media-system management; .d document assistance; .e local intelligent processing. Provenance/privacy/confidence controls stay D-coded unless mapped to explicit B1 text elsewhere |
| LAI4-06 | §15 lines 244–246 | RETAIN / CROSS-LINK | Cross-domain capability references to Smart Home, media and documents; map each to domain-owned contract without creating a second authority |
| LAI4-07 | §15 line 249 | RETAIN | Advisory/proposal-producing model; AI is not State Authority |
| CLAI4-01 | §16 lines 255–256 | RETAIN | Distributed computation within trusted MediaHub Cluster |
| CLAI4-02 | §16 lines 257–265 | SPLIT | CLAI4-02.a heavy inference; .b batch processing; .c computer vision; .d media processing; .e AI generation; .f engineering calculations; .g Digital Twin workloads; .h distributed tasks |
| CLAI4-03 | §16 line 267 | RETAIN | Access to Local Cluster AI is governed by named MediaHub AI Gateway |
| CLAI4-04 | §16 lines 255–267 | REFRAME / DERIVED | Explicit source boundary is trusted cluster + gateway. Claims about no policy/State Authority escalation are useful derived controls; label and trace them separately |
| CLAI4-05 | §16 lines 255–267 | DERIVED ACCEPTANCE CONTROLS | Node capability, resource limits, failure handling, and qualification profiles are not individually enumerated in §16; keep as D-coded acceptance controls with owner-approved contracts |
| CDAI4-01 | §17 lines 273–274 | SPLIT | CDAI4-01.a corporate/company-serving purpose; .b separate level after Local Cluster AI |
| CDAI4-02 | §17 lines 275–287 | SPLIT | CDAI4-02.a Website infrastructure; .b Trusted Sources Intelligence Engine; .c AI Human Clone; .d engineering development; .e Digital Twin workloads; .f commercial MediaHub infrastructure; .g development infrastructure; .h CI/CD; .i GPU computing; .j heavy AI tasks; .k approved-data storage/processing; .l commercial infrastructure operations |
| CDAI4-03 | §17 line 289 | RETAIN | Ordinary users do not get direct access to Cloud Development AI/Environment |
| CDAI4-04 | §17 line 291 | SPLIT | CDAI4-04.a Local AI may request cloud compute; .b Local Cluster AI may request cloud compute; .c local resources insufficient condition; .d policy permission; .e confidentiality permits transfer |
| CDAI4-05 | §17 line 291 | SPLIT | CDAI4-05.a authorization requirements; .b residency requirements; .c egress requirements. Cross-link escalation conditions; do not duplicate requester atoms |
| CDAI4-06 | §17 line 293 | RETAIN | Cloud is not MediaHub authority |
| CDAI4-07 | §17 lines 291–293 | RECLASSIFY | Keep provider allowlist/fallback and cloud-failure continuity as D-coded derived controls, not as literal §17 wording. Split into provider/routing control and local-continuity control |

**Important:** child suffixes above are provisional proposal identifiers, not committed canonical IDs. Assign stable IDs only after review to avoid collision with existing audit IDs and to preserve lineage.

## 4. Source coverage and crosswalk constraints

- The line spans above are intended as reviewable source anchors. A future approved child register should use precise sentence/list-item anchors (for example, §4 line 87 should be atomized by the literal comma-separated primitive list).
- Audit 01's 153 IDs are a source/control register, not a proven one-to-one mapping to Batch 04's 48 records. This proposal must not claim that the 153 IDs are all independent literal B1 requirements.
- Some proposed splits overlap by design to preserve traceability, but canonical child records must avoid duplicate normative obligations. Cross-links are preferable to duplicated requirements.
- Derived security, failure, authorization, provenance, routing, and acceptance controls must be labelled as derived unless a specific literal B1 clause is cited.
- Exact B2 mappings and branch-specific MH dependencies must be reviewed separately; a related B2 section is not proof that a requirement is fully mapped, accepted, implemented, or qualified.

## 5. Approval gates and next action

Before this proposal can become a normalized backlog:

1. Review the split map with the relevant domain owners/governance.
2. Decide which child items are literal B1 atoms versus derived acceptance/security controls.
3. Resolve duplicate/overlapping parent-child obligations and select stable child-ID syntax.
4. Attach exact B1 source spans and separately classified B2 mapping for each approved child.
5. Define owner, canonical contract path/ref, acceptance criteria, and required evidence for each item.
6. Update the canonical backlog only after approval; preserve the original Batch 04 artifact unchanged for provenance.

**Current disposition: OPEN / NOT APPROVED.** No tests or qualification were run. No software was installed. No infrastructure or production system was changed. Baseline 1.0, Baseline 2.0, and the MH-24 matrix were not edited. No merge to `main` was performed.


## 6. Revision 02 — exact child-level anchors and dispositions from review 01

This section narrows the proposal where revision 01 used parent-level or overlapping spans. All child suffixes remain provisional. Line numbers refer only to Baseline 1.0 blob SHA `9df4892ed0734050ac79732603d15bb414717310` on `main`.

### 6.1 Literal source anchors

| Historical parent / proposed child | Exact B1 line(s) | Classification / boundary |
|---|---:|---|
| SA4-02.a | 66 | Literal: system state |
| SA4-02.b | 67 | Literal: MediaHub-object state |
| SA4-02.c / SA4-03.a | 68 | Same source atom; preserve one normative obligation and cross-link, not duplicate |
| SA4-02.d / SA4-03.b | 69 | Same source atom; preserve one normative obligation and cross-link, not duplicate |
| SA4-04.a | 70 | Literal: authorization of state-changing operations |
| SA4-05.a | 71 | Literal: consistency |
| SA4-05.b | 72 | Literal: provenance |
| SA4-05.c | 73 | Literal: audit |
| SA4-05.d | 74 | Literal: recovery |
| SA4-05.e | 75 | Literal: migration |
| HA4-01.a | 85; 97–98 | Literal authority claim and later explicit distinction; keep domain scopes distinct |
| HA4-02.a–k | 87 | One comma-separated literal list; child labels map in order: integrations, devices, entities, states, events, services, triggers, conditions, actions, scenes, Smart Home automations |
| HA4-03.a–e | 90 | Literal ordered chain: Physical Devices → Integrations → HA Core → MediaHub Smart Home Layer → API → UI. Edges are derived traceability subdivisions of this single line, not new B1 sentences |
| HA4-04.a–b | 92 | Literal: standard HA visual UI is not MediaHub UI; user interacts through unified MediaHub UI |
| HA4-05.a | 94 | Literal: AI automation creation must not bypass HA Core or MediaHub Smart Home Layer |
| HA4-06.a–b | 97–98 | Literal distinct authority scopes |
| UI4-01.a | 104 | Literal: unified user-facing visual environment |
| UI4-02.a–f | 107–111, 114 | Six separate list-item anchors, one line per atom as listed in §3 table |
| UI4-03.a–b | 112–113 | Literal: macOS-like feel/UX and distinct MediaHub identity |
| UI4-04 | — | No unique literal atom established; HOLD. Candidate lines 104/116 are already covered by UI4-01 unless owner supplies a distinct interpretation |
| SH4-01.a | 122 | Literal: scalable Smart Home ecosystem through extensible adapter/integration layer |
| SH4-01.b / SH4-07.a | 136 | Literal vendor-neutral compatibility objective; cross-link one obligation rather than duplicate it |
| SH4-02.a–m | 124 | One literal category list; child labels map in source order |
| SH4-03.a | 126 | Literal automatic equipment discovery |
| SH4-04.a–d | 127–130 | Literal identification list, one line per field |
| SH4-05.a | 131 | Literal compatibility check |
| SH4-06.a–c | 132–134 | Literal: propose integration, create configuration, expose device through unified UI |
| AUTO4-01.a–k / AUTO4-02 | 204 | Single literal list. AUTO4-02 is a cross-link to energy/security items, not an independent duplicate category requirement |
| AUTO4-03.a–e / AUTO4-04.a–c / AUTO4-05 | 206 | One literal compound sentence: assistance capabilities and controlled MediaHub/HA mechanisms; audit schema/result record remains DERIVED unless sourced elsewhere |
| LAI4-01.a | 232 | Literal local execution placement |
| LAI4-02.a–b | 235–236 | Literal local inference and natural-language interaction |
| LAI4-03.a–b | 237–238 | Literal analysis and user assistance |
| LAI4-04.a–d | 239–241, 244 | Literal capabilities; use exact individual lines, with line 244 also cross-linked to domain support |
| LAI4-05.a–e | 242–247 | Literal capability list; map each atom to its own line: search 242; local data work 243; Smart Home 244; media 245; documents 246; local intelligent processing 247. Because six lines are listed, revise child labels/count to six atoms rather than five |
| LAI4-06.a | 244–246 | Cross-domain support cross-links only; not a second normative copy of Smart Home/media/documents |
| LAI4-07.a | 249 | Literal advisory/proposal-producing model and no State Authority |
| CLAI4-01.a | 255 | Literal distributed computation within trusted cluster |
| CLAI4-02.a–h | 258–265 | Literal workload list, one line per item |
| CLAI4-03.a | 267 | Literal MediaHub AI Gateway access regulation |
| CLAI4-04 / CLAI4-05 | — | Derived controls only where they add specific constraints not stated in §16; label D-coded and obtain owner-approved contract |
| CDAI4-01.a–b | 273 | Single literal sentence: company-serving cloud compute and distinct level after Local Cluster AI |
| CDAI4-02.a–l | 276–287 | Literal list, one line per listed capability |
| CDAI4-03.a | 289 | Literal: ordinary users have no direct access |
| CDAI4-04.a–e / CDAI4-05.a–c | 291 | One literal compound gate: requester (Local AI/Cluster AI), insufficient local resources, policy permits, confidentiality permits transfer, authorization and residency/egress requirements. Split for traceability, but do not count each split as a separate repeated gate |
| CDAI4-06.a | 293 | Literal: cloud is not MediaHub authority |
| CDAI4-07.a–b | — | Derived provider allowlist/fallback and local-continuity controls; not literal §17 wording |

**Correction note:** the earlier five-child formulation for LAI4-05 is not consistent with the literal lines 242–247. Revision 02 therefore requires six line-level capability atoms across the affected LAI4-05/06 cross-link boundary, while preserving the historical LAI4-05/06 IDs and avoiding an additional canonical ID decision in this proposal.

### 6.2 Overlap disposition register

| Group | Revision 02 disposition |
|---|---|
| SA4-02 ↔ SA4-03 | Lines 68/69 are single literal atoms with multiple historical references. Use one canonical requirement each and cross-link the legacy IDs. |
| HA4-01 ↔ HA4-06 | HA Core owns Smart Home scope (85, 97); MediaHub State Authority owns platform state (98). Preserve two distinct authority scopes, not competing authorities. |
| UI4-01 ↔ UI4-02 ↔ UI4-04 | UI4-01 covers lines 104/116; UI4-02 covers explicit design list; UI4-04 remains HOLD unless a unique residual requirement is approved. |
| SH4-01 ↔ SH4-07 ↔ SH4-06.c | Vendor neutrality is line 136; device exposure through unified UI is line 134. Cross-link but do not duplicate. |
| AUTO4-01.j/.k ↔ AUTO4-02 | Energy/security categories occur in line 204 once. AUTO4-02 is a cross-link, not a second requirement. |
| AUTO4-04 ↔ AUTO4-05 | Line 206 supports controlled MediaHub/HA mechanism and AI non-authority. Audit/result schema is derived unless separately sourced. |
| LAI4-01 ↔ LAI4-07; LAI4-03 ↔ LAI4-05 | Execution placement (232), capability list (235–247), advisory boundary (249) are distinct. Capability children must use exact individual lines; cross-domain support must not duplicate them. |
| CLAI4-01/03 ↔ CLAI4-04/05 | Trusted-cluster placement (255) and gateway (267) are literal; node admission/capability/resource/failure/qualification profiles remain D-coded unless exact source clauses are added. |
| CDAI4-04 ↔ CDAI4-05 ↔ CDAI4-07 | Line 291 is one compound gate. Split its conditions for traceability but keep a shared source-gate reference; provider fallback/local continuity are D-coded. |

### 6.3 Status and approval boundary

- This is proposal revision 02, not approval and not a canonical backlog.
- Historical Batch 04 remains immutable; 48 unique historical IDs are preserved.
- Child IDs are provisional; no new stable ID syntax is selected here.
- B1 and B2 remain separate sources. No semantic reconciliation or matrix-status resolution is implied.
- Every item remains OPEN. Exact source anchors do not imply acceptance, implementation, tests, qualification, release or production authorization.
- No tests/qualification, software installation, deployment, infrastructure/production action or merge to `main` was performed.
