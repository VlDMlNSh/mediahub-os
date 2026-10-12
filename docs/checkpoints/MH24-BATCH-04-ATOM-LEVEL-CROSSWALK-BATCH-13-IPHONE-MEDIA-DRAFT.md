# MH-24 — Supplemental Atom-Level Crosswalk: Baseline 1.0 §22 (iPhone Media / AirPlay) — Draft 01

- **Date:** 2026-10-12
- **Working ref:** `docs/mediahub-chat-tree-map-20261012`
- **Status:** DOCUMENTARY DRAFT / SEMANTIC OWNER ACCEPTANCE OPEN / NOT A CANONICAL BACKLOG.
- **Scope:** B1 §22, lines 375–379 at pinned B1 blob SHA `9df4892ed0734050ac79732603d15bb414717310`.
- **Purpose:** break the exact iPhone-to-MediaHub AirPlay / 4K capability and its stated constraints into source-anchored traceability labels, while preserving the existing high-level item `IPHONE-AIRPLAY-4K-01`.
- **ID rule:** `PROVISIONAL/IM-22-xx` labels are temporary traceability labels only. They are not final child IDs, and no final `MH24-B04-...` child IDs are minted by this draft.
- **B1:** `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, SHA `9df4892ed0734050ac79732603d15bb414717310`, §22 lines 375–379.
- **B2:** `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §§8–9, 12, 15, 20, and 22 where applicable.
- **Prior semantic audit:** `docs/checkpoints/MH24-SEMANTIC-AUDIT-BATCH-03.md` @ this branch, SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`, §2 row `IPHONE-AIRPLAY-4K-01`. It records exact AirPlay / 4K AirPlay as a candidate semantic gap; general phone/media support is not equivalence.
- **Traceability matrix:** `docs/checkpoints/mediahub-mh24-traceability-matrix.md` @ working ref, SHA `73377891072bac3c739c44055ceeb0874154f64c`, row 22 “iPhone Media” currently summarizes “AirPlay/4K capability subject to qualification”; it is a section-level row, not implementation evidence.
- **Domain dependency:** MH-18 acceptance `docs/architecture/MH-18-acceptance-criteria.md@mh-18-media-content-architecture-handoff-v2`, SHA `1ce114d92ce401609d536138982a4c89408064dc`, status NOT ACCEPTED / NOT FROZEN. MH-18 evidence register SHA `931e2fe80f2675469e4701f4e59ae483de850dd6`, PROPOSED / AUDIT BASELINE with dated evidence (2026-09-04); it does not establish current runtime presence.
- **Owner schema:** Product Owner Decision Record 01, SHA `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd`, D-05. The 12-field schema/status vocabulary is approved; these individual mappings and semantic acceptance are not.
- **Adjacent sequence verified:** Batch 07 covers B1 §16; Batch 08 §17; Batch 09 §18; Batch 10 §19; Batch 11 §20; Batch 12 §21. Six likely Batch 13 filenames were checked at the current ref and returned 404; this draft uses the first explicit chosen path only and does not assert a global branch-wide absence of similarly themed artifacts.

## Mapping rules used in this draft

- `MAPPED` requires a pinned B2 clause explicitly documenting the same bounded capability or constraint; it is not implementation or qualification evidence.
- `NO_DIRECT_COUNTERPART` is limited to the exact named AirPlay transport/capability in the reviewed B2 clauses. It is not a global repository-absence claim.
- `NOT_REVIEWED` remains for generic media/phone/4K/capability/network/authorization clauses that are relevant but do not establish the specific iPhone → MediaHub AirPlay contract and its per-path acceptance criteria.
- `CONFLICT` is not assigned without explicit contradictory normative text.
- B2 §15 lists general audio/video, phone endpoints, 4K and media codecs subject to platform capability/rights; B2 §§8–9 / §12 / §20 provide capability, network and qualification principles. The reviewed B2 text does not explicitly name AirPlay or establish qualified iPhone-to-MediaHub AirPlay behavior.
- The nine labels below are provisional traceability subdivisions, not nine independently approved product requirements. Preserve `IPHONE-AIRPLAY-4K-01` and matrix row 22 as historical/high-level references.

## Provisional atom records

### IM-22-01 — iPhone-to-MediaHub AirPlay transfer capability

- **Requirement ID:** `PROVISIONAL/IM-22-01` (temporary traceability label; not a final child ID).
- **Owner:** TBD; subsystem/product owner for iPhone media transfer is not confirmed by this draft.
- **Source atom / classification:** B1 §22 line 377 — LITERAL: MediaHub supports redirecting audio and video streams from iPhone to MediaHub, including 4K video, using AirPlay.
- **B2 mapping status:** `NO_DIRECT_COUNTERPART` for the specifically named AirPlay transfer path in the reviewed B2 clauses. B2 §15 has general phone endpoints/audio-video/4K media, but exact AirPlay interoperability and directionality are not explicit.
- **Canonical contract path/ref:** No accepted AirPlay contract verified. B2 §15 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; MH-18 acceptance SHA `1ce114d92ce401609d536138982a4c89408064dc`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define supported sender/device/OS/profile matrix, directionality, protocol/version, capability boundaries, rights and failure behavior; do not imply all iPhone/MediaHub combinations work.
- **Required evidence:** Accepted AirPlay/product contract, supported-device matrix, rights/licensing review and interoperability evidence at exact hardware/software versions.
- **Lifecycle status:** DRAFT / NOT APPROVED; architecture, implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03 `IPHONE-AIRPLAY-4K-01`; MH-18 remains NOT ACCEPTED / NOT FROZEN.
- **Dependencies:** MH-18; MH-17 device/protocol integration; MH-12 security/authorization; MH-10 only if AI-assisted media processing is involved; B2 capability/network/qualification gates.
- **Verification method:** Compare exact B1 §22 with B2 §§8–9, 12, 15, 20; only promote if an accepted source explicitly defines this AirPlay path and its bounded support claims.
- **Change history:** Supplemental traceability label linked to existing `IPHONE-AIRPLAY-4K-01`; no final child ID minted.

### IM-22-02 — 4K video transfer

- **Requirement ID:** `PROVISIONAL/IM-22-02`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §22 line 377 — LITERAL sub-aspect: AirPlay redirection includes 4K video.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §15 includes generic 4K media but does not state 4K iPhone-to-MediaHub AirPlay as a supported, qualified end-to-end path.
- **Canonical contract path/ref:** No accepted 4K AirPlay profile verified; B2 §§8–9, 15, 20 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define accepted resolution/frame-rate/codec combinations and device/network profiles; distinguish desired capability from measured admitted profiles.
- **Required evidence:** Capability profile, codec/device matrix and end-to-end resolution/quality evidence tied to exact versions.
- **Lifecycle status:** DRAFT / NOT APPROVED; capability and qualification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; matrix row 22 is only a section-level summary.
- **Dependencies:** MH-18; MH-17; hardware/network capability admission; rights/security.
- **Verification method:** Confirm explicit 4K AirPlay source coverage and per-profile evidence; generic “4K” listing is not equivalent.
- **Change history:** Keeps 4K traceability explicit without creating a final ID.

### IM-22-03 — Platform and device compatibility

- **Requirement ID:** `PROVISIONAL/IM-22-03`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §22 line 379 — LITERAL constraint: support must account for compatibility.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §§8–9 provide a general capability/platform model, but the checked clauses do not give the AirPlay/iPhone compatibility matrix.
- **Canonical contract path/ref:** No accepted AirPlay compatibility contract verified; B2 §§8–9 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: specify supported iPhone/iOS, MediaHub role/OS, network and receiver combinations; unsupported profiles must fail clearly rather than imply support.
- **Required evidence:** Versioned interoperability matrix, known exclusions and regression evidence per admitted profile.
- **Lifecycle status:** DRAFT / NOT APPROVED; platform-specific verification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; MH-18 acceptance remains open.
- **Dependencies:** MH-17; MH-18; platform profiles under B2 §9.
- **Verification method:** Compare the profile matrix to exact protocol/device contracts and the B1 compatibility requirement.
- **Change history:** Generic capability model kept separate from actual AirPlay compatibility evidence.

### IM-22-04 — Network conditions

- **Requirement ID:** `PROVISIONAL/IM-22-04`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §22 line 379 — LITERAL constraint: network conditions must be considered.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §12 defines logical network planes/direct media routing and network qualification, but does not specify AirPlay-specific network thresholds or degraded behavior.
- **Canonical contract path/ref:** No accepted AirPlay network contract verified; B2 §12 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define network profile assumptions, local/remote reachability boundaries, congestion behavior and clear failure/degradation responses.
- **Required evidence:** Tested network matrix, failure/degradation criteria and observed behavior tied to hardware/OS versions.
- **Lifecycle status:** DRAFT / NOT APPROVED; network interoperability/qualification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; no AirPlay-specific acceptance record found in the checked sources.
- **Dependencies:** MH-17; MH-18; network plane contracts and device capability admission.
- **Verification method:** Compare B1 network-condition clause with B2 §12, then require specific AirPlay acceptance thresholds rather than infer them.
- **Change history:** General direct-media routing does not by itself prove AirPlay behavior.

### IM-22-05 — Authorization

- **Requirement ID:** `PROVISIONAL/IM-22-05`.
- **Owner:** TBD; authorization policy owner for AirPlay sender/receiver and content rights is not identified here.
- **Source atom / classification:** B1 §22 line 379 — LITERAL constraint: authorization must be considered.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §§3–7 contain general authority/security/authorization controls, but the checked clauses do not define AirPlay sender/receiver admission or per-content authorization.
- **Canonical contract path/ref:** No accepted AirPlay authorization contract verified; B2 §§3–7, 15 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define who may initiate/receive streams, device trust/admission, rights-based restrictions and fail-closed behavior when authorization is missing or revoked.
- **Required evidence:** Authorization/rights matrix, supported protocol security model and negative-path evidence at qualification stage.
- **Lifecycle status:** DRAFT / NOT APPROVED; policy and verification OPEN.
- **Reviewer / approval reference:** MH-12 acceptance SHA `40f37f1600c4730e622480d57bd492fa67f9ca4b` is governance review required; MH-18 remains not accepted.
- **Dependencies:** MH-12; MH-17; MH-18; product rights/policy contracts.
- **Verification method:** Confirm the exact authorization path for the supported AirPlay profile and content; general B2 authorization is not proof of AirPlay admission.
- **Change history:** Authorization kept distinct from network reachability and protocol compatibility.

### IM-22-06 — Codec compatibility

- **Requirement ID:** `PROVISIONAL/IM-22-06`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §22 line 379 — LITERAL constraint: codec must be considered.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §15 mentions codecs/transcoding under platform capability and rights, but the checked text does not define AirPlay sender/receiver codec requirements.
- **Canonical contract path/ref:** No accepted AirPlay codec matrix verified; B2 §15 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: enumerate supported codec/container/encoding combinations, transcoding constraints, unsupported-format handling and rights boundaries.
- **Required evidence:** Codec interoperability matrix, licensed/allowed component inventory and format-specific verification evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; component compatibility and qualification OPEN.
- **Reviewer / approval reference:** MH-18 acceptance SHA `1ce114d92ce401609d536138982a4c89408064dc`, NOT ACCEPTED / NOT FROZEN.
- **Dependencies:** MH-18; MH-17; OSS/license/supply-chain gates; target platform profiles.
- **Verification method:** Compare B1 codec constraint with B2 §15; do not treat general transcoding support as a qualified AirPlay path.
- **Change history:** Codec requirements remain provisional and protocol-scoped.

### IM-22-07 — Latency

- **Requirement ID:** `PROVISIONAL/IM-22-07`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §22 line 379 — LITERAL constraint: latency must be considered.
- **B2 mapping status:** `NOT_REVIEWED`; the reviewed B2 clauses do not define AirPlay-specific latency budgets or acceptable playback/interaction behavior.
- **Canonical contract path/ref:** No accepted latency/SLO contract verified; B2 §§8, 12, 15, 20 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define measurement method, media class, target and maximum acceptable latency, and degraded/unavailable behavior per profile.
- **Required evidence:** Repeatable latency measurements and acceptance thresholds for each admitted device/network profile.
- **Lifecycle status:** DRAFT / NOT APPROVED; performance verification OPEN.
- **Reviewer / approval reference:** MH-18 acceptance remains NOT ACCEPTED / NOT FROZEN.
- **Dependencies:** MH-18; MH-17; network/platform qualification.
- **Verification method:** Require explicit thresholds and repeatable evidence instead of qualitative availability claims.
- **Change history:** No unmeasured performance assumption introduced.

### IM-22-08 — Resolution behavior

- **Requirement ID:** `PROVISIONAL/IM-22-08`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §22 line 379 — LITERAL constraint: resolution must be considered.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §15 includes 4K among general media capabilities but does not define AirPlay negotiation, downshift or fallback behavior.
- **Canonical contract path/ref:** No accepted AirPlay resolution-negotiation contract verified; B2 §§8–9, 15, 20 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define requested/negotiated/output resolution states, downgrade policy, user-visible limitations and clear failure behavior.
- **Required evidence:** Resolution negotiation matrix and observed output evidence across admitted device/network profiles.
- **Lifecycle status:** DRAFT / NOT APPROVED; capability and qualification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; matrix row 22 is not acceptance evidence.
- **Dependencies:** MH-18; MH-17; capability/network profiles.
- **Verification method:** Verify requested vs negotiated vs observed resolution for exact supported profiles.
- **Change history:** Distinguishes nominal 4K support from actual per-session resolution.

### IM-22-09 — Available bandwidth

- **Requirement ID:** `PROVISIONAL/IM-22-09`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §22 line 379 — LITERAL constraint: available bandwidth must be considered.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §8 lists network bandwidth in the capability profile, and §12 states the network/plane model, but neither defines AirPlay-specific throughput thresholds or admission policy.
- **Canonical contract path/ref:** No accepted AirPlay bandwidth/admission contract verified; B2 §§8, 12, 15, 20 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define required/observed throughput, overhead/headroom, congestion response and whether the session is admitted, downshifted or denied.
- **Required evidence:** Measured bandwidth profiles, representative load conditions and acceptance thresholds tied to codecs/resolutions.
- **Lifecycle status:** DRAFT / NOT APPROVED; network/performance qualification OPEN.
- **Reviewer / approval reference:** MH-18 remains NOT ACCEPTED / NOT FROZEN; no current AirPlay runtime evidence identified.
- **Dependencies:** MH-17; MH-18; network profiles; capability model and qualification.
- **Verification method:** Compare B1 bandwidth constraint with B2 capability/network model and require measured protocol-specific thresholds.
- **Change history:** B2's inclusion of bandwidth as a generic capability does not by itself satisfy a per-session AirPlay contract.

## Initial mapping disposition

- Rows: 9 provisional traceability labels.
- Distribution: **0 MAPPED / 8 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT**.
- These rows are provisional subdivisions linked to the existing `IPHONE-AIRPLAY-4K-01` audit item and matrix row 22. They are not independently accepted requirements.
- No stable/final child IDs are minted. No collision-check inventory is claimed.
- MH-18 remains NOT ACCEPTED / NOT FROZEN. The cited MH-18 evidence register is historical/proposed and does not prove current media implementation.
- This document is not independently reviewed. Semantic/owner acceptance, protocol support, runtime behavior and qualification remain OPEN.
- B1, B2, the working traceability matrix, canonical backlog and `main` remain unchanged.
