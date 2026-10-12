# MH-24 Batch 13 — iPhone Media / AirPlay Semantic Review 02

- **Review date:** 2026-10-12
- **Ref:** `docs/mediahub-chat-tree-map-20261012`
- **Status:** BOUNDED SEMANTIC REVIEW — ONE GENERIC MEDIA CONSTRAINT MAPPING CORRECTION PROPOSED; FULL AIRPLAY/OWNER ACCEPTANCE OPEN
- **Scope:** source-anchored comparison of B1 §22 lines 375–379 and B2 §§8, 12, 15, 20, with the current Batch13 draft, Review01, Semantic Audit Batch03 and AT-15. Not runtime/interoperability testing, implementation verification, owner acceptance, qualification, or global repository absence.
- **History:** Batch13 Review01 is preserved unchanged as a structural/source-anchor/status-consistency pass. This Review02 adds a narrowly scoped semantic status recommendation.

## 1. Exact source manifest

| Source | Ref | Blob SHA | Use |
|---|---|---|---|
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | `docs/mediahub-chat-tree-map-20261012` | `9a655f4d889ae9ae30fbef0f9a61f8d6dd9cca23` | Current map/checkpoint at review start |
| `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` | `docs/mediahub-chat-tree-map-20261012` | `f86014d81a2db1b5246b4fc2600812340f1c7d22` | Source/scope/authority protocol |
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Literal §22, lines 375–379 |
| `docs/checkpoints/mediahub-functional-baseline-2.0.md` | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | §8 capability profile; §12 network plane; §15 media/codecs/rights; §20 qualification |
| `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-13-IPHONE-MEDIA-DRAFT.md` | `docs/mediahub-chat-tree-map-20261012` | `1a1cf6f595163d3bbf7036337c057b0621b1e418` | Nine provisional records before semantic disposition |
| `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-13-IPHONE-MEDIA-REVIEW-01.md` | `docs/mediahub-chat-tree-map-20261012` | `abf9c5f669b59434c3a9bb52068b8f226efa129c` | Historical bounded structural review |
| `docs/checkpoints/MH24-SEMANTIC-AUDIT-BATCH-03.md` | `docs/mediahub-chat-tree-map-20261012` | `fcd006e99d812dac5071b34c531f2783f4f54e88` | High-level `IPHONE-AIRPLAY-4K-01` finding |
| `docs/checkpoints/MH24-ATOMIC-TRACEABILITY-BACKLOG-01.md` | `docs/mediahub-chat-tree-map-20261012` | `ec2580f714e8f620bcf85ff7de2ae9242439e5e8` | AT-15 owner decision/evidence gate |
| `docs/checkpoints/mediahub-mh24-traceability-matrix.md` | `docs/mediahub-chat-tree-map-20261012` | `73377891072bac3c739c44055ceeb0874154f64c` | Section-level row 22 only |
| `docs/checkpoints/MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md` | `docs/mediahub-chat-tree-map-20261012` | `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd` | D-04 vocabulary/D-05 schema; no approval of this mapping |
| `docs/architecture/MH-18-acceptance-criteria.md` | `mh-18-media-content-architecture-handoff-v2` | `1ce114d92ce401609d536138982a4c89408064dc` | NOT ACCEPTED / NOT FROZEN |
| `docs/architecture/MH-18-evidence-register.md` | `mh-18-media-content-architecture-handoff-v2` | `931e2fe80f2675469e4701f4e59ae483de850dd6` | Historical/proposed evidence register, not current runtime proof |
| `docs/architecture/MH-17-acceptance-criteria.md` | `arch/mh-17-device-protocol` | `fb8361775b41e72ca05b6e82d6d71fc38dc2def4` | NOT ACCEPTED / NOT FROZEN |
| `docs/architecture/MH-17-evidence-register.md` | `arch/mh-17-device-protocol` | `20a56a55978bc7dd9c6951c838d7eb5f9c98c5c4` | Protocol adapter claims remain scoped by their own evidence status |

## 2. Literal source and direct generic correspondence

B1 §22 line 377 requires redirecting iPhone audio/video streams to MediaHub using AirPlay, including 4K video. B1 line 379 requires consideration of compatibility, network conditions, authorization, codec, latency, resolution and available bandwidth.

B2 §15 line 350 explicitly includes media codecs/transcoding, subject to platform capability and rights. This is a direct documentary correspondence to the **generic codec consideration** in B1 §22 line 379. Accordingly, the `IM-22-06 — Codec compatibility` row can be proposed as `MAPPED` **only for the fact that media codec handling is a stated capability/constraint**. This mapping does not establish AirPlay-specific codec support, sender/receiver negotiation, transcoding behavior, interoperability or qualification.

The other generic B2 similarities must stay conservative:
- B2 §15's general `4K` and `phone endpoints` do not by themselves establish 4K over the specifically named iPhone-to-MediaHub AirPlay path.
- B2 §8 lists network bandwidth as a resource/capability-profile dimension, but does not specify AirPlay streaming admission thresholds, headroom or fallback behavior.
- General authorization/security clauses do not define AirPlay session authorization.
- Generic capability and qualification clauses do not define the actual AirPlay compatibility matrix, latency budget, resolution negotiation or supported network conditions.

## 3. Row-by-row status recommendation

| Row | Current disposition | Review02 recommendation and boundary |
|---|---|---|
| IM-22-01 — iPhone-to-MediaHub AirPlay transfer capability | `NO_DIRECT_COUNTERPART` | Keep. B2 §15 does not name AirPlay or define its directionality/protocol path. Scope narrowly to the checked B2 clauses; do not claim global repository absence. |
| IM-22-02 — 4K video transfer | `NOT_REVIEWED` | Keep. Generic 4K media is not a qualified 4K AirPlay path. |
| IM-22-03 — Compatibility | `NOT_REVIEWED` | Keep. No explicit AirPlay sender/receiver/platform compatibility matrix is defined in the reviewed B2 clauses. |
| IM-22-04 — Network conditions | `NOT_REVIEWED` | Keep. Network/capability architecture does not define per-path Wi-Fi/network conditions or session-admission behavior. |
| IM-22-05 — Authorization | `NOT_REVIEWED` | Keep. Generic security/authorization principles do not constitute a defined AirPlay-session authorization flow. |
| IM-22-06 — Codec compatibility | `NOT_REVIEWED` → **propose `MAPPED`** | B2 §15 explicitly names codecs/transcoding subject to platform capability and rights. Map only that generic media constraint; keep AirPlay-specific codec/profile acceptance OPEN. |
| IM-22-07 — Latency | `NOT_REVIEWED` | Keep. No AirPlay-specific latency budget or measurement/acceptance criterion is present in the reviewed B2 clauses. |
| IM-22-08 — Resolution | `NOT_REVIEWED` | Keep. A generic 4K label does not define resolution negotiation or accepted AirPlay modes. |
| IM-22-09 — Available bandwidth | `NOT_REVIEWED` | Keep. B2 §8 recognizes network bandwidth as a capability dimension but does not specify AirPlay-specific throughput thresholds, headroom or fallback. |

No explicit contradictory normative text was established; `CONFLICT` remains 0. One bounded generic mapping does not close AT-15, accept the AirPlay feature, or alter owner/governance state.

## 4. Proposed corrected distribution and acceptance gates

If the working draft adopts the bounded IM-22-06 correction, the nine-row distribution becomes **1 MAPPED / 7 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT**. These are provisional traceability labels, not independent accepted product requirements.

AT-15 remains **OPEN—OWNER DECISION**. Required follow-up before product acceptance includes explicit feature-scope decision, supported iPhone/iOS and MediaHub receiver matrix, protocol/profile, codec and 4K mode support, compatibility and network admission criteria, authorization boundary, latency/resolution/bandwidth behavior, rights/licensing review and versioned interoperability evidence. MH-17 and MH-18 are both NOT ACCEPTED / NOT FROZEN in their cited branch-specific acceptance docs. The evidence register does not establish present AirPlay runtime availability.

## 5. Conclusion and next bounded action

**Conclusion:** semantic review supports one status correction only: `IM-22-06` may be mapped at the generic media-codec constraint level. All AirPlay-specific semantics remain OPEN. Review01 remains unchanged as historical evidence; Audit Batch03's `IPHONE-AIRPLAY-4K-01`, AT-15 and matrix row 22 are retained.

**Next action:** update only the working Batch13 draft row IM-22-06 and mapping summary, read back the new SHA, then update Passport P-27 and Contract ARC-034/V-27 plus Jarvis/continuation/map pointers. Keep B1, B2, matrix, AT-15 status, canonical backlog and `main` unchanged. No tests, qualification, installation, deployment, host/infrastructure action or merge to `main` was performed.
