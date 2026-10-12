# MH-24 Batch 04 — Atom-Level Crosswalk Batch 04 Review 01

- **Date:** 2026-10-12
- **Branch:** `docs/mediahub-chat-tree-map-20261012`
- **Status:** **STRUCTURAL AND SOURCE-ANCHOR REVIEW PASS / LINEAGE ISSUE OPEN / SEMANTIC OWNER ACCEPTANCE OPEN**
- **Reviewed draft:** `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-04-DRAFT.md`, SHA `bbc77c484313f261d473bbbc7dd5ea8eeb65e577`.
- **B1:** `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` @ `main`, SHA `9df4892ed0734050ac79732603d15bb414717310`.
- **B2:** `docs/checkpoints/mediahub-functional-baseline-2.0.md` @ `main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Audit 01:** SHA `d0938f14ed4110545118f075175dee3be412097b`; **Proposal 02:** SHA `7e737c8add9e3453062e9fc459790e7010e55689`; **Product Owner Decision Record:** SHA `9117098e22c26708d48ca8ba5954669faa209d68`.
- **Map before review:** SHA `2a44522e65e3488b2d3a44378964302a4fd31d54`.

## 1. Structural verification

1. Fetched the pinned B1, B2, Audit 01, Proposal 02, draft and decision record from GitHub.
2. Parsed the Audit 01 §6 table: 29 control/atom rows, including 26 literal source-traceability entries and 3 D-coded derived controls. The draft preserves all Audit 01 row IDs.
3. Counted the approved 12-field schema on every row: 29/29 rows have 12 fields.
4. Confirmed each status is `NOT_REVIEWED` because Audit 01 relations are partial or derived and no direct B1↔B2 conflict/no-counterpart decision is supported in these §6 rows.
5. Confirmed the draft labels all three D-coded rows as derived and expressly says they are not verbatim B1 wording.
6. Read the B2 §14 Smart Home passage: it defines HA Core operational authority, platform identity/lifecycle/policy ownership, discovery-to-revocation lifecycle and AI no-bypass rule. It does not provide the complete per-capability adapter/acceptance matrix.

## 2. Source-anchor verification

| B1 line | Directly fetched literal source |
|---:|---|
| 122 | `MediaHub должен поддерживать масштабируемую экосистему Smart Home через расширяемый adapter/integration layer.` |
| 124 | `Поддерживаются освещение, климат, безопасность, камеры, домофоны, датчики, приводы, электропитание, сетевое оборудование, контроллеры, hubs, wired systems и wireless systems.` |
| 126 | `Предусматривается автоматическое обнаружение оборудования. При обнаружении устройства MediaHub:` |
| 127 | `- определяет устройство;` |
| 128 | `- определяет производителя;` |
| 129 | `- определяет модель;` |
| 130 | `- определяет способ подключения;` |
| 131 | `- проверяет совместимость;` |
| 132 | `- предлагает установку необходимой интеграции;` |
| 133 | `- создаёт необходимую конфигурацию;` |
| 134 | `- предоставляет устройство через единую MediaHub UI.` |
| 136 | `Цель — максимальная совместимость без ограничения архитектуры конкретным производителем.` |

## 3. Status and schema summary

| Check | Result |
|---|---:|
| Audit 01 §6 IDs | 29 |
| Draft rows | 29 |
| ID sets match | PASS |
| 12-field rows | 29/29 |
| MAPPED | 0 |
| NOT_REVIEWED | 29 |
| NO_DIRECT_COUNTERPART | 0 |
| CONFLICT (B1↔B2 status) | 0 |
| Final child IDs minted | 0 |
| Runtime tests/qualification | Not performed |

## 4. Traceability discrepancy detected

**B1-06-24 / SH4-07 vs Proposal 02 SH4-06.c**

- The Audit 01 row `B1-06-24` attaches the line-134 “device through unified MediaHub UI” atom to historical parent `SH4-07`.
- The later Proposal 02 §6.1/§6.2 assigns B1 line 134 to `SH4-06.c`, while the line-136 vendor-neutral compatibility objective is linked to shared `SH4-01.b / SH4-07.a`.
- This is a legacy parent/source-link discrepancy. The draft preserves both records and flags the newer proposed anchor; it does not silently edit the historical Audit 01 file, mint child IDs or call this a B1-versus-B2 semantic conflict.
- Disposition: **OPEN** pending independent documentary review and owner/governance confirmation.

## 5. Limits and disposition

- **Result:** structural and source-anchor checks PASS; source/parent lineage discrepancy remains OPEN.
- Mapping is not accepted; all 29 rows remain `NOT_REVIEWED`. B1/B2 semantic equivalence is not inferred, and no runtime behavior is validated.
- Product-owner decisions approve schema/status vocabulary only. They do not approve derived controls, capability matrix or this crosswalk.
- B1, B2, main, historical backlog, parent-level crosswalk and previous atom batches were not modified by this review. No tests, qualification, installation, deployment, live-host operation or merge was performed.
- Next safe step: index this batch/review in the map, then continue with B1 §12 Smart Home Automation, carrying forward the source/parent lineage issue as an open traceability gate.
