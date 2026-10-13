# P0-07 D7 — canonical state-version crosswalk

Date: 2026-10-13
Status: READ-ONLY SOURCE CROSSWALK / PARTIAL / NOT ACCEPTED / NOT FROZEN

## Evidence

Read from `main`:
- `runtime/mediahub_runtime/in_memory_state.py` — `0fbc71369d19e09944ba67a60ccb9df802f30a4b`
- `runtime/mediahub_runtime/generation.py` — `4e4fe0e40d67c18c918881d79dc2cc9933988b2c`
- `runtime/mediahub_runtime/authorization.py` — `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`
- `runtime/mediahub_runtime/consumer_boundary.py` — `98bf2da9cea85da2c82145b4baef417c20b9ae73`
- `runtime/mediahub_runtime/state.py` — `a2115b81f52a63feb357e484bd982a6a32641d81`

## Findings

The inspected in-memory authority stores a canonical integer `state_version`. Transactions capture the current generation and version. Commit checks transaction status, authorization, generation ID, binary/schema compatibility, and exact current-version freshness; successful commit advances the current version. Generation compatibility requires matching generation ID, binary version, schema version and state version. Restore checks checkpoint ownership, integrity, generation compatibility and self-test, then advances the current version rather than resetting to the checkpoint's historical version.

P0-05 delegates through opaque consumer transaction handles. P0-04 authorization uses explicit principal/capability/operation grants and default-deny, but the inspected module does not identify the issuer or authentication lifecycle. These files do not demonstrate a complete trusted P0-07 → P0-05 → P0-04 caller path.

## Disposition

D7 is PARTIAL: in-memory version/generation mechanics are source-evidenced, but accepted ownership of generation/schema change control and end-to-end revision binding are NOT EVIDENCED in this source set. Persistence, crash recovery, migration and runtime qualification are not proven; the implementation explicitly states persistence is out of scope.

P0-07 mutation/publication remains BLOCKED — GOVERNANCE/API GAP. P0-05 v1.1 remains NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN. Qualification remains NO-GO / NOT PROVEN.

Next: re-read map-selected MH-14 persistence, MH-16 lifecycle/migration and MH-22 qualification primary artifacts; identify whether they specify an accepted change-control owner and evidence path. No tests, runtime actions, deployment or merge were performed.


## Follow-up — governance-question deduplication and metadata/change-control boundary (2026-10-13)

- Re-read the existing P0-05 v1.1 candidate (docs/checkpoints/p0-05-consumer-contract-v1.1-candidate-for-governance-review-2026-10-12.md, live docs-branch blob 79e2b4865c47b5394ade266cd3cd7cfbe3097717). Its D7 already asks whether the candidate becomes P0-05 v1.1 or a separately governed domain-operation contract. Do not create a duplicate owner question or a new decision ID.
- Existing owner directions in docs/checkpoints/mediahub-owner-decisions-2026-10-12.md retain D7 C → B: inspect versioning/change-control rules first; propose v1.1 only if in scope, otherwise route a separately governed contract. This direction is not adoption, acceptance, freeze or implementation authorization.
- Current main tree SHA 1d45bbccbbbd27309c39cb9e9351bb291cdb47a8 contains schemas/core/contract-metadata.schema.json blob 0e9e6b0233612c37f316fa83e7786325c992af13, which requires schema_id, semver-shaped schema_version, owner, required/optional fields and constraints. This is a metadata-shape contract only; it does not define who is authorized to change/freeze a schema, compatibility rules, migration approvals, immutable revision binding, or cross-component evidence ownership.
- P0-06 governance packet blob 95d5d7292e55e1bc438d0742137988888d651e7a says changes to P0-04/P0-05 semantics, authority invariants, persistence scope or P0-06 security boundary invalidate its implementation authorization and require a new governance decision. This is relevant change-control evidence, but it is scoped to P0-06 and does not establish the missing cross-domain owner for P0-07 D7.
- Therefore no additional owner question is needed at this stage: the candidate already contains the unresolved D7 choice. The next useful step is to prepare a source-anchored comparison of the existing candidate's D7 scope against the schema metadata and MH-14/MH-16/MH-22 gates, then route that same existing decision to its owner. Do not change its wording or mark it answered without owner disposition.
- D7 remains PARTIAL / NOT ACCEPTED / NOT FROZEN; P0-07 mutation/publication BLOCKED — GOVERNANCE/API GAP; P0-05 v1.1 NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN; qualification NO-GO / NOT PROVEN.


## Source-anchored comparison: D7 scope against MH-14 / MH-16 / MH-22 (2026-10-13)

| Source | Live source blob | What the source normatively establishes | What it does not establish for D7 |
|---|---|---|---|
| MH-14 persistence architecture | `5e14084033f417722a1b04b5d5d47649dcfcda48` | Persisted records/snapshots need version and provenance metadata; recovery validates integrity, schema and compatibility and submits a candidate to State Authority; migration is explicit/versioned; persistence cannot authorize or promote canonical state. Physical persistence implementation is not authorized. | No accepted owner for schema/generation/revision change control; no end-to-end contract tying runtime revision to persistence, migration, restore and release evidence. MH14-D009 explicitly says MH-14 does not independently resolve P0-07's mutation-publication gap (decision-log blob `a2f49b9f4e09e3d2becdc2e72807319674a30239`). |
| MH-16 installer/recovery/update architecture | `f3ad2401f00a4062b39eed640e0c5c5f70064312` | Host, application, data and security versions must remain distinct; migration contracts are explicit/versioned and include source/target versions, preconditions, authorization, validation, recovery, compatibility and rollback capability; lifecycle mechanisms must not become State Authority. | Status remains proposed, governance acceptance pending, not frozen and implementation not authorized. It does not name an accepted cross-domain owner or approve one canonical generation/schema/revision change-control scheme. |
| MH-16 completion record | `e4ea4e3a37540cc104243c236e2e5c1c32ea35d6` | Records completion of an architectural pass and lists explicit non-claims. Changes to canonical architecture require an explicit governance update. | Does not claim MH-16 acceptance/freeze, universal rollback, completed production code, or accepted cross-domain change-control ownership. |
| MH-22 production/qualification/operations | `17bb2a9fdc34a0ee7c324e78e412616b5e377bb4` | Requires unique release identity (product/version/build/commit/artifact digest/channel/environment/dependencies/signature/SBOM where applicable/qualification record), explicit evidence and governance freeze. | Architecture is not accepted/frozen; release identity and current-HEAD qualification remain unverified in the evidence register. It specifies production evidence, not the owner of canonical schema/generation changes or the P0-05 v1.1 vs separate-contract choice. |
| MH-22 evidence register | `188a85e3a31cb545fd781e6db237d655d721ec1c` | Current-head qualification, release identity, artifact signature/SBOM, restore and disaster-recovery evidence remain unknown/requiring verification; production acceptance not granted. | No evidence that a complete cross-domain change-control owner/path has been accepted. Unknown remains unknown; this is not proof of a defect or universal absence. |

### D7 disposition from this comparison

1. **Already established:** version/provenance metadata is required; migration must be explicit and versioned; persistence/recovery must validate compatibility and submit candidate state to State Authority; product mutation authority remains singular; release qualification requires exact candidate identity and evidence.
2. **Still not established:** an accepted owner and approval path for generation/schema/revision changes; compatibility policy across runtime, persistence, migration and restore; immutable binding from those versions to release/qualification evidence; whether the proposed P0-07 domain-operation hand-off is normatively within P0-05 v1.1 or belongs in a separately governed contract.
3. **Recommended route (not a decision):** keep the existing P0-05 candidate D7 question as the sole owner interface. Resolve its scope first; separately name an accountable governance owner for cross-domain version/change-control coherence and require source-SHA-bound evidence. Do not treat this recommendation as owner approval, contract acceptance, freeze or implementation authorization.
4. **No status promotion:** D7 remains PARTIAL / NOT ACCEPTED / NOT FROZEN; P0-07 mutation/publication remains BLOCKED — GOVERNANCE/API GAP; P0-05 v1.1 remains NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN; qualification remains NO-GO / NOT PROVEN. P0-07 D2 independent review is a separate open gate.
