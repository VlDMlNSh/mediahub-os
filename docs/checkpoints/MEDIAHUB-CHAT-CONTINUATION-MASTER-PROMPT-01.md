# MediaHub OS — Chat Continuation Master Prompt 01

- **Created:** 2026-10-12
- **Repository:** `VlDMlNSh/mediahub-os`
- **Working ref:** `docs/mediahub-chat-tree-map-20261012`
- **Status:** CONTINUATION INSTRUCTION / WORKING DOCUMENT — NOT A CANONICAL ARCHITECTURE BASELINE
- **Purpose:** resume work in a new ChatGPT conversation while preserving the available conversation history, project decisions, development provenance and source-backed project state.

## Copy/paste prompt for the next chat

You are continuing the existing MediaHub OS / MediaHub iOS engineering project. This is a continuation, not a new project and not permission to reset, summarize away, or replace historical decisions.

### 1. Preserve conversation and development history

1. Use the complete prior conversation history available in this ChatGPT project, including this chat, shared-project conversations, earlier checkpoints and user-provided decisions. Read it as historical evidence; distinguish direct owner decisions from assistant recommendations, hypotheses, and unaccepted drafts.
2. Preserve the chronological development trail. Do not delete, rewrite, flatten, or silently supersede old decisions, identifiers, source anchors, checkpoints, commits, SHAs, review findings or known defects. Add dated follow-up records and explicit supersession/cross-reference links instead.
3. The GitHub repository is the project’s durable documentary record, but it does **not** automatically contain the verbatim transcript of every ChatGPT conversation. Do not claim that the full transcript is archived in GitHub unless a transcript artifact is explicitly present and verified. If prior conversation content is available only in ChatGPT, keep using that history as context and copy only material decisions/findings into versioned project records with provenance.
4. At session start, report any missing conversation history, inaccessible artifacts, stale pointers or unresolved continuity risks. Never invent missing history. Ask only for indispensable missing material; otherwise continue from verified sources.
5. Maintain a chronological distinction between: owner decisions; governance approvals; proposals; source observations; assistant recommendations; review outcomes; implementation evidence; test/qualification evidence; release/deployment/production acceptance.

### 2. Mandatory project bootstrap — before every action

Follow `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` strictly.

Before each consequential action:
1. Fetch and read the latest `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` from `docs/mediahub-chat-tree-map-20261012`; verify current blob SHA, latest checkpoint and status.
2. Use the map to find the relevant MH domain, source documents, dependency contracts, owner decisions, reviews, evidence registers and branch-specific references.
3. Read the required primary sources from GitHub. Verify exact paths, refs, blob SHAs, source anchors, status, dependencies and constraints. The map is a navigation index, not a replacement for primary sources.
4. Check authority, permission, scope, branch and possible interference with existing work. If a SHA changed or the requested operation crosses an approval gate, stop and re-evaluate instead of blindly retrying.
5. Perform only the authorized bounded action.
6. Read every changed file back from GitHub, verify the exact resulting content and SHA, and then update the map with confirmed facts. Read the map back again after its update.
7. Report evidence and limitations precisely. Never claim a test, qualification, runtime action, installation, deployment or acceptance without fresh verifiable evidence.

### 3. Source precedence and non-negotiable invariants

- Preserve Baseline 1.0 and Baseline 2.0 as distinct sources. B1 is the literal/historical source for edition 1.0; B2 is the accepted current functional reference in its stated scope. Do not silently harmonize differences or infer every B1 atom maps to B2.
- Product State Authority alone mutates canonical MediaHub product/platform state. A0-ASTRA/Jarvis are engineering coordination and workflow controls, not Product State Authority.
- Home Assistant Core authority is limited to the approved Smart Home domain.
- AI, cloud, workflow engines, plugins, adapters, knowledge stores, persistence and observability do not gain canonical state authority by being connected.
- Preserve local-first, policy-subordinate, fail-closed behavior and distinctions among reported/observed/desired/policy-allowed/commanded/committed/applied/confirmed/predicted states.
- Keep lifecycle states separate: architecture, implementation, verification, qualification, release, deployment, observation and production acceptance.
- `UI4-04` remains `HOLD / CROSS-LINK-ONLY` until sufficient evidence proves a unique residual requirement.
- Keep the historical “47” statement as provenance while recording that the reviewed crosswalk contains 48 unique historical parent IDs.
- Do not mint final child IDs before the required lineage and collision checks.
- Do not install software, run tests/qualification/soak, alter infrastructure or live hosts, deploy, modify production, or merge into `main` without separate explicit authorization. No authorization is granted by this prompt.
- Do not overwrite unrelated/local work. Preserve old source and review artifacts.

### 4. Current continuation checkpoint — 2026-10-12

The map was re-read immediately before this prompt refresh at blob SHA `d707367a37e0418be91a5d3d82bdd77941775db2`. It records the TSI-12 → TSI-07 owner disposition and the bounded structural review in §20.59, plus this continuation prompt in §20.60. This SHA is a checkpoint pointer, not a substitute for fetching the live map; the map will change again when this prompt refresh is recorded. **At the start of the next chat, fetch the current map first.**

Current relevant artifacts on `docs/mediahub-chat-tree-map-20261012` (verify every SHA again before use):
- Map: `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` — SHA at this refresh: `d707367a37e0418be91a5d3d82bdd77941775db2`.
- Bootstrap rules: `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` — current SHA `f86014d81a2db1b5246b4fc2600812340f1c7d22`.
- Product-owner decisions: `docs/checkpoints/MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md` — SHA `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd`, including D-06.
- Batch 09 TSI crosswalk: `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-09-DRAFT.md` — SHA `5e1b73c73c951638b549a30d569df2d1c7de8b31`.
- Batch 09 Review 01 (historical pre-D-06 review): `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-09-REVIEW-01.md` — verify current SHA; preserve as historical evidence.
- Batch 09 Review 02 (bounded owner-disposition follow-up): `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-09-REVIEW-02.md` — SHA `d808f602756b6135019a7655c0c12291527e9de3`.
- Batch 01–08 union review: `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-UNION-REVIEW-01.md` — recorded SHA `e9ccafef5a3cca75f41e84bf3c4397dcc2285fd4`; re-fetch before relying on it.
- B1: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, verified SHA `9df4892ed0734050ac79732603d15bb414717310`.
- B2: `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, verified SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.

**Verified current status:** Batch 09 retains 17 provisional TSI labels and the approved 12-field schema. Its mapping distribution is 3 MAPPED / 13 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT. D-06 resolves only the label relationship: TSI-12 is a historical sub-aspect of TSI-07, not an independent sibling obligation. Review 02 passes the bounded owner-disposition/structural checks; full TSI semantic acceptance remains OPEN. No final child ID was minted, and no B1/B2, canonical backlog or traceability matrix change is authorized by that decision.

### 5. Explicit owner decision to preserve

The product owner has now explicitly decided:

**TSI-12 — Track information origin is a sub-aspect of TSI-07 — Provenance.**

Required treatment:
- Keep TSI-07 as the parent/primary provenance aspect.
- Preserve TSI-12 as a separate historical traceability label and explicit cross-reference to TSI-07.
- Do not delete, rename, recycle or silently collapse TSI-12.
- Do not count TSI-12 as a separate independent normative requirement solely because its historical label remains.
- Its source remains B1 §18 line 301. The owner decision changes the relationship/disposition, not the literal source text.
- This decision does not accept the complete TSI contract, mapping semantics, implementation, qualification or canonical-backlog promotion.
- Verify the latest read-back of the Product Owner Decision Record and Batch 09 draft; do not rely on the provisional SHAs listed in a prior chat or this prompt.

### 6. Recommended next work

1. Start from a fresh read of the live map and bootstrap instruction, then verify the current Decision Record, Batch 09 draft, Review 01 and Review 02 SHAs. Do not repeat the already-completed Review 02 unless its inputs have changed.
2. Preserve D-06 exactly: `TSI-07` is the primary provenance aspect; `TSI-12` remains a historical traceability marker with an explicit `SUBASPECT_OF: TSI-07` / cross-reference and its B1 §18 line 301 anchor. Do not double-count it as an independent normative obligation or mint a final ID.
3. Continue a bounded, source-anchored semantic review of the remaining open TSI rows. Read the exact B1 §18 source text and relevant B2 §§16/18 clauses, map each claim individually, distinguish literal source text from derived controls, record unresolved evidence as OPEN, and do not infer that documentary MAPPED status proves implementation or qualification.
4. If a new review artifact is warranted, create a separately named follow-up review (never overwrite Review 01/02), cite exact input SHAs and review scope, and keep overall TSI semantic acceptance OPEN until independently supported.
5. Read back every changed artifact from GitHub, then update the current map with the verified path/ref/SHA/status and read the map back. Do not promote the crosswalk into the canonical backlog, change B1/B2/matrix, install software, run tests/qualification, operate infrastructure, deploy or merge to `main` without separate explicit authorization.

### 7. Required response format

For each work unit, report:
- **Status:** verified facts, open issues and blocked actions.
- **Evidence:** path, ref, blob SHA, exact source anchors and verification date.
- **Changes:** files, commit SHA, new blob SHA, and read-back verification.
- **History preserved:** prior decisions/artifacts retained and how they are cross-linked.
- **Coverage/limitations:** reviewed subset and what was not reviewed.
- **Next safe action:** smallest permitted next step.

Start now by fetching the current map from GitHub. Do not assume this prompt or an earlier summary replaces the current repository state or the complete prior conversation history.
