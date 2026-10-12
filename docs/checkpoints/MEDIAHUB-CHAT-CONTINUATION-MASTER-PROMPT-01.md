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

### 4. Prior continuation checkpoint — 2026-10-12 (historical pointer snapshot)

The map was re-read immediately before this prompt refresh at blob SHA `d707367a37e0418be91a5d3d82bdd77941775db2`. It records the TSI-12 → TSI-07 owner disposition and the bounded structural review in §20.59, plus this continuation prompt in §20.60. This SHA is a checkpoint pointer, not a substitute for fetching the live map; the map will change again when this prompt refresh is recorded. **At the start of the next chat, fetch the current map first.**

Current relevant artifacts on `docs/mediahub-chat-tree-map-20261012` (verify every SHA again before use):
- Map: `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` — SHA at this refresh: `d707367a37e0418be91a5d3d82bdd77941775db2`.
- Bootstrap rules: `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` — current SHA `f86014d81a2db1b5246b4fc2600812340f1c7d22`.
- Product-owner decisions: `docs/checkpoints/MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md` — SHA `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd`, including D-06.
- Batch 09 TSI crosswalk: `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-09-DRAFT.md` — SHA `5e1b73c73c951638b549a30d569df2d1c7de8b31`.
- Batch 09 Review 01 (historical pre-D-06 review): `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-09-REVIEW-01.md` — verify current SHA; preserve as historical evidence.
- Batch 09 Review 02 (bounded owner-disposition follow-up): `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-09-REVIEW-02.md` — SHA `d808f602756b6135019a7655c0c12291527e9de3`.
- Batch 09 Review 03 (bounded semantic consistency review): `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-09-REVIEW-03.md` — SHA `184a99ef85143c2ad3048dca5c8d85b17f8651a3`; full TSI semantic acceptance remains OPEN.
- Working System Passport v3: `docs/checkpoints/MEDIAHUB-OS-SYSTEM-PASSPORT-V3.md` — current blob SHA `8ec8ed05e3a4f303fb8a93a63c2d77c7defd3fd6`.
- Working Verifiable Architecture Contract 01: `docs/checkpoints/MEDIAHUB-OS-VERIFIABLE-ARCHITECTURE-CONTRACT-01.md` — current blob SHA `4a5510a4246ddfed60dd94be9502203a62da48d0`; 30 ARC requirements / 23 verification checks, not canonically accepted.
- Jarvis Global Master Prompt 01: `docs/checkpoints/MEDIAHUB-JARVIS-MASTER-PROMPT-01.md` — current blob SHA `7865342dc5b3af0a01cf6f92ee765460d80a23c1`.
- Batch 07 Local Cluster AI draft: `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-07-DRAFT.md` — current blob SHA `d6323442e3059dda091d0ad8b2a33fa91cad6ea0`.
- Batch 07 Review 02: `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-07-REVIEW-02.md` — current blob SHA `0af17bf0db6f8b1c93d01aae3e8a8b5d8a0d9064`.
- Current map pointer before this prompt refresh: `573e152b769b0c03b9f1e9d20c8b205168577930`; always re-fetch the live map at the next session start.
- Batch 01–08 union review: `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-UNION-REVIEW-01.md` — recorded SHA `e9ccafef5a3cca75f41e84bf3c4397dcc2285fd4`; re-fetch before relying on it.
- B1: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, verified SHA `9df4892ed0734050ac79732603d15bb414717310`.
- B2: `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, verified SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.

**Verified current status:** Batch 09 retains 17 provisional TSI labels and the approved 12-field schema; distribution remains 3 MAPPED / 13 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT, with full TSI acceptance OPEN. D-06 keeps TSI-12 as a historical sub-aspect of TSI-07. Batch 07 retains 11 provisional records; after Review 02, its working distribution is 1 MAPPED / 9 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT. The sole MAPPED row (B1-16-01 / CLAI4-01) denotes bounded documentary capability correspondence only, not full Local Cluster AI contract acceptance. Review 01 remains historical; Review 02 is the new semantic follow-up. Full domain acceptance, implementation and qualification remain OPEN. No final child ID was minted, and no B1/B2, canonical backlog or traceability matrix change was authorized by these reviews.

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

1. Start with a fresh read of the live map and bootstrap instruction; the map SHA quoted above is historical, not an active pointer.
2. Read back the current Passport v3, Verifiable Architecture Contract 01, Jarvis master prompt, gap reconciliation, D-06, Batch 09 draft and Reviews 01–03. Trust only the SHAs recorded in the live map and current artifacts.
3. Continue restoring the full MH-01…MH-25 project map source-by-source: verify each domain's canonical paths, branch/ref/commit, master/reverse handoff, owner decisions, dependencies, acceptance/evidence registers and unresolved conflicts. Do not infer closure from a chat, branch name or document existence.
4. Keep Passport v3 and Contract 01 synchronized as integrated WORKING DRAFTS. Review 03 is complete; do not repeat it unless an input changed. Do not promote either document to a globally accepted baseline without independent review and explicit owner/governance acceptance.
5. Resolve the still-open owner/governance disposition for the named TSI subsystem and its contract boundary. Preserve D-06 exactly; do not mint final child IDs or promote Batch 09.
6. Source-batch sequence correction (verified 2026-10-12): Batch 07 already covers B1 §16 Local Cluster AI (draft SHA `9d9663107a0ffba4316ab47bc8974e537a901f46`, Review 01 SHA `4c665414776414efdc0855c395c290466b035423`); Batch 08 covers B1 §17 Cloud Development AI; Batch 09 covers B1 §18 Trusted Sources Intelligence Engine. Do not recreate Batch 07. The next sequential uncovered source section is B1 §19 AI Human Clone. Create a separately named provisional Batch 10 under the approved 12-field schema, pin B1/B2 refs and relevant privacy/identity/security/media clauses, preserve the matrix row 19 and keep semantic/owner acceptance OPEN. Keep the remaining statuses OPEN until supported.
7. Read back every changed artifact and update the live map with its exact SHA/status. No installs, tests, qualification, infrastructure/host changes, deployments or merge to `main` without separate explicit authorization.

### 7. Required response format

For each work unit, report:
- **Status:** verified facts, open issues and blocked actions.
- **Evidence:** path, ref, blob SHA, exact source anchors and verification date.
- **Changes:** files, commit SHA, new blob SHA, and read-back verification.
- **History preserved:** prior decisions/artifacts retained and how they are cross-linked.
- **Coverage/limitations:** reviewed subset and what was not reviewed.
- **Next safe action:** smallest permitted next step.

Start now by fetching the current map from GitHub. Do not assume this prompt or an earlier summary replaces the current repository state or the complete prior conversation history.

### 8. Refresh history — 2026-10-12

The previous next-work block directed the session to perform the first source-anchored TSI semantic follow-up. That bounded work is now recorded in Batch 09 Review 03, SHA `184a99ef85143c2ad3048dca5c8d85b17f8651a3`; the instruction above supersedes that completed next step while preserving D-06, Review 01 and Review 02. Current Passport/Contract/Jarvis prompt pointers are listed in §4 above. The live map must still be fetched at the start of the next session; no fixed map SHA in this prompt replaces that requirement.


- 2026-10-12 — corrected the next source-batch pointer after a live read-back confirmed Batch 07 already covers B1 §16; the next sequential uncovered section is B1 §19 AI Human Clone, subject to source-anchor and branch inventory checks. This is a routing correction only; no requirement or mapping status changed.

- 2026-10-12 — refreshed active Passport, Contract, Jarvis prompt and Batch07 pointers after Review02: Passport `8ec8ed05e3a4f303fb8a93a63c2d77c7defd3fd6`; Contract `4a5510a4246ddfed60dd94be9502203a62da48d0`; Jarvis prompt `7865342dc5b3af0a01cf6f92ee765460d80a23c1`; Batch07 draft `d6323442e3059dda091d0ad8b2a33fa91cad6ea0`; Review02 `0af17bf0db6f8b1c93d01aae3e8a8b5d8a0d9064`. The next bounded source section remains B1 §19 AI Human Clone; complete MH map restoration remains in parallel.
