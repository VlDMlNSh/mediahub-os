# MediaHub OS — MH-24 Semantic Traceability Audit, Batch 01

**Audit date:** 2026-10-12  
**Status:** DOCUMENTARY AUDIT — PARTIAL; NO IMPLEMENTATION OR QUALIFICATION CLAIM  
**Scope:** Passport 1.0 sections 3–9 (State Authority, Home Assistant Core, UI, Smart Home, manufacturers, Kincony/KCS, wired systems).  
**Purpose:** Record exact clause coverage and gaps in the existing 68-row MH-24 matrix without changing either baseline.

## 1. Sources read and verified

| Source | Ref | Blob SHA | Use |
|---|---|---|---|
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Primary requirements for passport §§3–9 |
| `docs/checkpoints/mediahub-functional-baseline-2.0.md` | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Current document-declared functional reference; clauses §§3–4, 14, 21–22 |
| `docs/checkpoints/mediahub-mh24-traceability-matrix.md` | `main` | `8bdd364493ebbe2ef6f87400f80bc7eca8fb95c6` | Existing section-level matrix; rows 3–9 |
| `docs/architecture/mh-04/MH-04-acceptance-criteria.md` | `architecture/mh-04-security-trust-authorization` | `a75f5c1849ad67cc380a0ba3552bf7f2c5ec82b6` | State authority/security acceptance gate |
| `docs/architecture/mh-04/MH-04-evidence-register.md` | `architecture/mh-04-security-trust-authorization` | `dcf91d19cc494155e3c006a95f1ba35665d90e94` | Inherited contracts vs open topology/security evidence |
| `docs/architecture/MH-05-consumer-integration-boundary.md` | `architecture/mh-05-consumer-integration-boundary` | `6718905825c0f91ef21494d518b7e87dacb26ae0` | Consumer boundary; proposed, implementation not authorized |
| `docs/architecture/MH-05-acceptance-criteria.md` | `architecture/mh-05-consumer-integration-boundary` | `db18ab4416516240af394a6a9f57831f95edb802` | MH-05 acceptance gate |
| `docs/architecture/MH-05-dependency-map.md` | `architecture/mh-05-consumer-integration-boundary` | `7ad2d3fe528a88326401eb1310cc08ab75d5b842` | Proposed dependency chain |
| `docs/architecture/MH-05-evidence-register.md` | `architecture/mh-05-consumer-integration-boundary` | `0f8a3a3d8d16d1953ffa452484061a42a2312132` | Evidence/provenance caveats |
| `docs/architecture/MH-17-acceptance-criteria.md` | `arch/mh-17-device-protocol` | `fb8361775b41e72ca05b6e82d6d71fc38dc2def4` | Device/protocol acceptance gate |
| `docs/architecture/MH-17-evidence-register.md` | `arch/mh-17-device-protocol` | `20a56a55978bc7dd9c6951c838d7eb5f9c98c5c4` | Separates schemas from missing implementation evidence |

**Path-resolution note:** attempts to fetch `docs/architecture/STATE-HA-INTEGRATION-CONTRACT.md` and the listed MH-04/MH-05/MH-17 acceptance files from `main` returned 404. The specialized MH-04/MH-05/MH-17 documents cited above were fetched from their branch refs as directed by the map. The exact canonical path/ref of the named “STATE-HA integration contract” is still unresolved; do not infer that no such document exists anywhere in the repository.

## 2. Requirement-level findings

| Passport § / requirement ID | Passport 1.0 requirement | Baseline 2.0 mapping | Domain / dependency | Acceptance and evidence status | Finding |
|---|---|---|---|---|---|
| §3 / SA-01 | MediaHub State Authority is the sole canonical platform-state authority. | §3 authority table; §4 invariants 1, 14–15; §10 cluster model; §13 storage; §25 downstream implementation work. | MH-03 / MH-04 / MH-14 / MH-20; depends on P0-03/P0-04 and consumer boundary P0-05. | B2 architecture decision is explicit. MH-04 acceptance remains `PROPOSED / REVIEW COMPLETE`; actual topology and production security qualification are not established. MH-05 is `NOT ACCEPTED — REQUIRES VERIFICATION`; authority uniqueness remains an explicit gate. | **Architecture covered; implementation/qualification open.** Do not convert “one logical authority” into a claim of implemented distributed consensus or production readiness. |
| §3 / SA-02 | Critical canonical state must not be governed by unconditional Last Write Wins; disconnected secondary nodes do not become independent authority. | §4 invariants 14–15; §10 cluster model; §25 leader election/quorum/replication and consistency-class work. | MH-03 / MH-14 / MH-20; consistency, fencing, quorum and recovery dependencies. | Baseline says the invariant; §25 explicitly carries implementation work forward. No current runtime evidence was part of this documentary pass. | **Normative invariant covered; mechanism/evidence open.** |
| §4 / HA-01 | Home Assistant Core is the single operational authority for Smart Home state and entities; MediaHub layers must not bypass it. | §3 authority table and invariants 2/13; §14 Smart Home lifecycle; §4 authority separation. | MH-05 consumer boundary → MH-17 device/protocol integration → HA Core. | B2 architectural decision is explicit. MH-05 acceptance remains open; MH-17 acceptance is `NOT ACCEPTED / NOT FROZEN`. Named HA integration contract exact path/ref not resolved during this pass. | **Authority rule covered; contract trace and acceptance open.** Need exact HA contract, command/event lifecycle, adapter authorization and negative-path evidence. |
| §5 / UI-01 | Unified, minimal MediaHub UI. | Matrix row 5 points to MH-09, but this batch did not inspect MH-09 primary documents. | MH-09; depends on consumer/API contracts, not State Authority ownership. | Not assessed beyond existing matrix row. | **Deferred; no conclusion.** |
| §6 / SH-01 | Extensible Smart Home adapter/integration layer under HA operational authority. | §14 Smart Home lifecycle; §21 OSS/adoption gates; §22 versioned contracts and API/event model. | MH-05 / MH-17; HA Core; policy and device capability admission. | MH-05 acceptance checklist is open. MH-17 acceptance is open. Its evidence register records schemas as present but real protocol adapters, discovery, enrollment, certificate/mTLS/PKI, simulator and authorized production commands as not found/unknown in its 2026-09-04 audit. That is historical branch evidence, not a fresh exhaustive scan of current main. | **Architecture covered; implementation evidence incomplete/dated.** Refresh only under an authorized implementation/evidence task. |
| §7 / VENDOR-01 | Passport names Центр Свет, Arlight, Maytoni, Kincony, Dahua, Hikvision, Ajax, Keenetic and Ubiquiti as target ecosystems; vendor support must be extensible and qualified. | B2 §§14 and 21 provide general Smart Home lifecycle and component-adoption gates; the exact vendor names listed in Passport §7 were not found in B2 text. | MH-05 / MH-17; per-vendor adapter, license/API/security review, capability qualification and evidence. | Existing matrix row 7 says “qualification-gated vendor adapters” but has no implementation artifact or qualification evidence. MH-17 acceptance is open. | **Specific vendor list not explicitly preserved in B2 text; candidate semantic omission.** Requires owner decision: preserve the exact target list in an accepted appendix/contract or explicitly disposition individual vendors. Do not infer vendor support from architecture language. |
| §8 / KINCONY-01 | Kincony/KCS: USB discovery, model and firmware identification, compatibility checks and controlled firmware-update proposal. | General B2 §§14, 21–22 do not name Kincony/KCS; no exact Kincony/KCS clause found in B2. | MH-17 device identity/discovery/firmware lifecycle; MH-05 boundary; user confirmation and policy/security. | Matrix row 8 has no implementation artifact or qualification evidence. MH-17 evidence register records device discovery/enrollment implementation and real adapters as not found/unknown in its historical audit. | **Specific requirement not explicitly preserved in B2 text; implementation/evidence gap.** Firmware write/update must not be inferred as available. |
| §9 / WIRED-01 | Support DALI, RS-485 and KNX through gateways/adapters/integration boundaries. | B2 §§14 and 21–22 provide generic integration/adoption semantics; exact protocol names DALI, RS-485 and KNX were not found in B2 text. | MH-17 protocols/adapters; MH-05 consumer boundary; vendor gateway qualification and safety/failure semantics. | Matrix row 9 contains no implementation artifact or qualification evidence. MH-17 acceptance remains open. | **Exact protocol scope not explicitly preserved in B2 text; candidate semantic omission.** Require protocol-specific capability/evidence inventory before claiming support. |

## 3. Explicit search results in Baseline 2.0

The following exact strings are present in Passport 1.0 but absent from the current Baseline 2.0 document text fetched from `main`: `Центр Свет`, `Arlight`, `Maytoni`, `Kincony`, `KCS`, `Dahua`, `Hikvision`, `Ajax`, `Keenetic`, `Ubiquiti`, `DALI`, `RS-485`, `KNX`.

For authority, `Home Assistant Core` is present in Baseline 2.0 (§3 and §4). These are literal text-presence results only. They do not prove that an equivalent requirement is absent from all MH branch documents or other referenced contracts.

## 4. Decisions and safe next steps

1. **Do not edit Baseline 1.0 or 2.0 in this audit batch.** Record specific semantic omissions and seek explicit owner/governance disposition before changing canonical references.
2. Resolve the exact path/ref for the named HA integration contract using the map and repository tree/branch inventory; do not create a replacement contract merely because one guessed path returned 404.
3. Keep MH-04, MH-05 and MH-17 acceptance statuses as stated in their cited primary documents. A frozen inherited P0 contract does not automatically accept/freeze the whole downstream MH domain.
4. A later batch should continue with Passport §§10–14 (wireless/network, optional Ubiquiti controller, automation, voice priority and AI/cloud boundary), using the same requirement-level evidence schema.
5. No implementation, tests, qualification, deployment, infrastructure changes or merge to `main` were performed or authorized by this audit.

## 5. Limitations

This is a documentary comparison of specified files and branch-specific acceptance/evidence records. It is not an exhaustive repository-wide search, code audit, runtime test, qualification, or proof of product behavior. A 404 for a guessed path is a path-resolution failure, not proof of global absence.
