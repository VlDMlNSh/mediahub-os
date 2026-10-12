# MH-24 Batch 04 — Atomic Normalization Proposal 01

**Date:** 2026-10-12  
**Status:** PROPOSAL / OPEN — NOT APPROVED; documentary planning only.  
**Scope:** Propose normalization of the 48 historical Batch 04 records against Baseline 1.0 §§3–6, 12, 15–17. Preserve all historical IDs and provenance. No baseline, matrix, governance status, implementation, qualification, or release decision is changed.

## 1. Verified inputs

| Source | Ref | Blob SHA | Role |
|---|---|---|---|
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | `docs/mediahub-chat-tree-map-20261012` | `57b1ecebef504dfabaca57248cd32c8b37a4bc90` | Current navigation and checkpoint |
| `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` | `docs/mediahub-chat-tree-map-20261012` | `f86014d81a2db1b5246b4fc2600812340f1c7d22` | Required process and limits |
| `docs/checkpoints/MH24-ATOMIC-TRACEABILITY-BACKLOG-04.md` | `docs/mediahub-chat-tree-map-20261012` | `26163e6f60b44e997560212bf7de9900210b7ed3` | 48 historical records + 8 cross-cutting issues |
| `docs/checkpoints/MH24-B1-SECTIONS-03-06-12-15-17-CLAUSE-COVERAGE-AUDIT-01.md` | `docs/mediahub-chat-tree-map-20261012` | `d0938f14ed4110545118f075175dee3be412097b` | 153-row source/control register |
| `docs/checkpoints/MH24-B1-SECTIONS-03-06-12-15-17-CLAUSE-COVERAGE-AUDIT-02.md` | `docs/mediahub-chat-tree-map-20261012` | `8b1f02eb07e153be825e39ec7a0289b0105d6156` | Structural count and scope validation |
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Literal source authority for this audit |

The Batch 04 source has 48 unique historical IDs despite its final line saying “47”. This proposal preserves the 48-ID inventory and records the discrepancy rather than silently rewriting the historical artifact.

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
| SA4-03 | §3 lines 65–75 | SPLIT / REASSIGN | SA4-03.a canonical ownership of user configurations; SA4-03.b canonical ownership of resource lifecycle. Cross-link SA4-02.c/.d; avoid duplicate requirements |
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
| UI4-02 | §5 lines 108–111, 114 | SPLIT | UI4-02.a minimal; .b predominantly grey; .c intuitive navigation; .d minimize visual complexity; .e unified control system; .f hide technical complexity behind unified UI |
| UI4-03 | §5 lines 112–113 | SPLIT | UI4-03.a macOS-like UX feel; UI4-03.b distinct MediaHub visual identity |
| UI4-04 | §5 lines 104–116 | REFRAME / CROSS-LINK | Keep only the independently testable unified-presentation obligation not already assigned to UI4-01/02; avoid duplicate authority requirements. Detailed acceptance criteria require owner-approved interpretation |
| SH4-01 | §6 line 122; line 136 | SPLIT | SH4-01.a scalable adapter/integration layer; SH4-01.b extensible beyond a single vendor |
| SH4-02 | §6 lines 124–125 | SPLIT BY CAPABILITY CATEGORY | SH4-02.a lighting; .b climate; .c security; .d cameras; .e intercoms; .f sensors; .g actuators; .h power; .i network equipment; .j controllers; .k hubs; .l wired systems; .m wireless systems |
| SH4-03 | §6 lines 126–126, 136 | RETAIN + DERIVED LABEL | Discovery as a distinct step is literal. “Discovery does not imply trust/enrollment” is a derived security control; keep it separately D-coded, not as verbatim B1 |
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
