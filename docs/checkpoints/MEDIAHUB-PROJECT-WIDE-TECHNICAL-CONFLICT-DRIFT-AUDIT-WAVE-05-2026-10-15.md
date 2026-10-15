# MediaHub OS — Project-Wide Technical Conflict and Drift Audit, Wave 05

- Date: 2026-10-15
- Status: **WIDE DOCUMENTARY AUDIT / SOURCE-ANCHORED FINDINGS / REMEDIATION PARTIAL**
- Scope: current GitHub refs, governing roadmap/checkpoint/map, ASTRA primary authority sources, MH-12 security, owner decision, integrated contract drafts, and recurring component/routing conflicts indexed by the current map.
- This is not a claim of exhaustive byte-level repository scan, runtime audit, test run, qualification, or acceptance.
- No normative baseline, accepted domain contract, ASTRA main-branch file, or implementation was modified in this wave.

## 1. Live ref and branch evidence

Repository: `VlDMlNSh/mediahub-os`

- `main` HEAD: `608d7463011798ca75e36bfce4b749a9caf4f9a0`
- Documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Comparison: `DIVERGED`; docs branch is 1171 commits ahead and 3 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No merge, rebase, cherry-pick, or branch integration was performed.
- Compare metadata lists modifications to ASTRA primary files on main and many docs-only additions on the documentation branch. The divergence is a governance/integration risk; commit counts do not establish that either side is semantically correct.

## 2. Source identity and provenance captured

| Source | Ref | Blob SHA | Role |
|---|---|---|---|
| `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md` | main | `7be5fadd3055642e7823c7233f90e978a87e5366` | Canonical ASTRA reference architecture |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | main | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Machine-readable governance/threshold source |
| `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml` | main | `adc852009c3a79d0e64265a3af8a4910a1388057` | ASTRA unified model |
| `docs/architecture/MH-12-security-architecture.md` | main | `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Security and capability semantics |
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | docs branch | `c6b047cd058c915d04541b0307d81378a3cb8c3d` | Current navigation and conflict index |
| `docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md` | docs branch | `63215cbfce1d4e7db078dcb456a07f0a42f7e1c5` | Continuation state |
| `docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md` | docs branch | `490bb604f90599145ccbb8040af69a54111419c2` | Sequencing and gates |
| `docs/checkpoints/MEDIAHUB-CHAT-TO-GITHUB-OWNER-DECISIONS-AND-CORPORATION-DIRECTION-WAVE-01-2026-10-15.md` | docs branch | `70376a2709e055972ceddc4a280d26992977213c` | Explicit owner decision |
| `docs/architecture/MEDIAHUB-UNIFIED-ARCHITECTURE-CONTRACT-V3-DRAFT-01.md` | docs branch | `28d5f82a80df2002d39c06d2060a822fd7aae258` | Non-normative integration draft |
| `docs/checkpoints/MEDIAHUB-OS-SYSTEM-PASSPORT-V3.md` | docs branch | `2b5d81236b85d44d284015cfb02d9401ab0e7482` | Integrated working passport |
| `docs/checkpoints/MEDIAHUB-OS-VERIFIABLE-ARCHITECTURE-CONTRACT-01.md` | docs branch | `c248956417cc61d66c968a4c58a56e799f653354` | Working verifiable contract |
| `docs/architecture/MEDIAHUB-JARVIS-ASTRA-DISTRIBUTED-AI-CORPORATION-TARGET-ARCHITECTURE-WAVE-01-2026-10-15.md` | docs branch | `c9f1716de8419d66f181fc0a9c465c65a81c7d5b` | Owner-direction target design |

## 3. Confirmed conflict register

### C-01 — ASTRA A0 authority wording vs approved lifecycle split
- **Evidence:** ASTRA reference architecture §1 says A0-ASTRA is the “single MediaHub coordination and state authority”; the unified ASTRA YAML assigns `single_coordination_authority`. MH-12 §2 says security does not own canonical state mutation and State Authority remains the sole canonical mutation authority. The verifiable integration contract ARC-001/ARC-003 and the owner decision record distinguish MediaHub Product State Authority from ASTRA engineering state.
- **Owner decision:** DEC-DEV-02 Option C is explicitly approved. Jarvis coordinates corporation missions; ASTRA A0 owns ASTRA-internal queue/claim/lease/retry/cancellation/recovery/evidence/gate lifecycle; MediaHub Product State Authority alone mutates canonical product state.
- **Status:** CONFIRMED SOURCE-TEXT CONFLICT; owner-choice question CLOSED; normative ASTRA wording remains unreconciled.
- **Remediation:** controlled, clause-level proposal to the owner-approved decision and ASTRA governance contract; do not make an unreviewed broad replace of “state authority”, since ASTRA legitimately owns its own workflow state.

### C-02 — stale decision status in historical artifacts
- **Evidence:** Wave 03 and older roadmap entries still describe A/B/C owner selection as pending; later owner decision record and Wave 04 explicitly state Option C is approved.
- **Status:** CONFIRMED DOCUMENTARY STALENESS, not a live undecided choice.
- **Remediation:** retain old records as historical evidence; add a dated supersession/status note or update only current indexes. Do not erase history or imply old commits were current.

### C-03 — branch divergence and baseline provenance risk
- **Evidence:** live compare is DIVERGED, 1171 ahead / 3 behind; main includes changes to ASTRA reference/unified files while the documentation branch contains integration drafts, maps, and checkpoints. The integrated v3 draft explicitly protects Baseline 2.0 as canonical and Baseline 1.0 as historical.
- **Status:** CONFIRMED INTEGRATION RISK; no merge conflict resolution attempted.
- **Remediation:** maintain source-specific refs/SHA in every crosswalk. Any integration requires separate explicit authorization and a deliberate merge review; do not equate ahead/behind counts with correctness.

### C-04 — canonical Baseline 2.0 vs historical Baseline 1.0 wording/drift
- **Evidence:** roadmap historical sections record a main/docs Baseline 1.0 content-drift finding. The current integrated contract says Baseline 2.0 is the accepted immutable functional reference and Baseline 1.0 is historical literal lineage; no B1→B2 equivalence or automatic supersession.
- **Status:** PROVENANCE/WORDING DRIFT ALREADY RECORDED; no evidence in this wave that B2 was superseded.
- **Remediation:** use B2 for current functional claims; cite B1 only for historical traceability. Any remaining clause mapping must be atom-level and cannot modify either baseline.

### C-05 — authority vs storage/event/transport conflation risk
- **Evidence:** integrated contract v3 and verifiable contract explicitly distinguish Product State Authority from persistence, broker, cache, graph, telemetry, backup, events, transport, provider and executor surfaces. ASTRA governance also prohibits provider/transport State Authority.
- **Status:** RULE IS DOCUMENTED; runtime conformance is not demonstrated here.
- **Remediation:** treat this as a mandatory review invariant for each adapter/schema and any future failover/recovery design; no runtime pass is claimed.

### C-06 — capability issuer and lifecycle contract is incomplete at integration boundary
- **Evidence:** MH-12 §8 requires capability binding to principal, issuer, operation, resource/target, scope, constraints, provenance, lifetime and revocation context. The Jarvis GitHub Adapter draft explicitly says accepted A0 ingress/API, authentication, issuer and queue-state interface must be sourced, not invented.
- **Status:** OPEN INTERFACE CONTRACT GAP; not proof of a deployed security defect.
- **Remediation:** source exact issuer lifecycle, token/capability format, grant/revoke/expiry behavior, and A0 trust boundary from accepted contracts. If no accepted source exists, record a governance/ADR decision need instead of filling defaults.

### C-07 — task DAG, mission envelope, result envelope and retry semantics remain proposed
- **Evidence:** corporation target architecture describes stable IDs, idempotency keys, task DAG, result envelope, partial/blocked/cancelled/unverified states, replay detection and no global exactly-once guarantee as target requirements. Jarvis adapter is explicitly a draft; it is not an accepted wire schema.
- **Status:** DESIGN REQUIREMENTS EXIST; accepted canonical schema/interface is not demonstrated by reviewed sources.
- **Remediation:** crosswalk fields against accepted A0 ingress and existing MH-21 distributed-job contracts before drafting a versioned corporation schema. Preserve “at-least-once/unknown” semantics unless an accepted contract proves otherwise; never claim exactly-once globally.

### C-08 — provider/gateway/route identity ambiguity
- **Evidence:** current map records unresolved FreeLLMAPI `local_gateway` registry classification vs cloud/provider wording, FCC implementation mapping, and OmniRoute/UnoRouter/OpenRouter distinctions. The map explicitly warns that Claude Code is a client/tool surface, not proof of hosted Claude inference; Ollama/Alamo model-runtime provenance remains unverified.
- **Status:** OPEN IDENTITY/TOPOLOGY QUESTIONS; no runtime evidence collected in this wave.
- **Remediation:** maintain distinct identities for client, gateway, transport, provider, model and runtime. Resolve only with pinned source/deployment evidence and non-secret route metadata; do not infer upstream/egress topology from a label.

### C-09 — “qualification ready” labels vs evidence-based qualification
- **Evidence:** ASTRA unified YAML uses status `QUALIFICATION_READY_HYBRID_FABRIC`, while its governance contract requires named gates, runtime thresholds, invariant enforcement, recovery and independent verification; the roadmap and verifiable contract explicitly say component selection or design does not prove installation, execution, qualification or acceptance.
- **Status:** SEMANTIC LABEL RISK; this audit did not validate whether all required qualification evidence exists. The label must not be reported as a passed qualification.
- **Remediation:** keep design readiness distinct from runtime qualification. Where consumers may interpret this field as an achieved gate, propose a status vocabulary clarification under source ownership; do not silently change the canonical file in this wave.

### C-10 — current single-node foundation vs future distributed State Authority
- **Evidence:** integrated contract v3 and verifiable contract state the current MH-03 foundation is single-node/in-memory with no authorized HA or physical persistence in that foundation, while future distributed/HA designs are target-gated.
- **Status:** TARGET/CURRENT-STATE DISTINCTION IS DOCUMENTED; runtime not inspected.
- **Remediation:** retain current foundation as the plan of record until separately authorized implementation and qualification evidence exists. Do not promote PostgreSQL/etcd/NATS/cluster concepts from design to deployed status.

### C-11 — Contour A / Contour B gate
- **Evidence:** roadmap phases 08–10 require authorized Contour A deployment and independent developer-fabric qualification before Contour B product development; owner target architecture repeats this gate.
- **Status:** GOVERNANCE GATE CONFIRMED; deployment/acceptance not established by this documentary wave.
- **Remediation:** keep product implementation in Contour B blocked until required Contour A deployment and independent acceptance evidence are recorded and separately authorized.

### C-12 — map/checkpoint/roadmap contain accumulated historical “next action” text
- **Evidence:** current roadmap contains older dated execution updates with pending decisions that are superseded by later owner decision and later updates; checkpoint also has many chronological continuation sections.
- **Status:** DOCUMENT NAVIGATION/STATUS-HYGIENE RISK, not necessarily a contradiction if dated history is read in order.
- **Remediation:** keep historical logs immutable where useful, but ensure the current top-level continuation checkpoint and map identify the single live next step and point to superseding records. Avoid mass rewriting dated history.

## 4. Remediation performed in this wave

1. Re-read the live branch comparison and the current map, checkpoint, roadmap, owner decision, Wave 04, ASTRA reference, ASTRA governance YAML, ASTRA unified YAML, MH-12, integration contract v3 draft, system passport, verifiable architecture contract, and corporation target architecture.
2. Consolidated the above into a source-anchored register with explicit status distinctions: confirmed conflict, stale historical wording, open interface gap, semantic label risk, target/current distinction, and unverified runtime condition.
3. Did **not** modify normative ASTRA contracts, Baseline 2.0, Baseline 1.0, security contracts, implementation, or qualification artifacts.
4. No tests, qualification, installations, provider/model calls, credential use, host/runtime inspection, infrastructure changes, deployment, merge, rebase, cherry-pick or release performed.

## 5. Prioritized next actions

1. **P0:** prepare clause-by-clause ASTRA authority wording reconciliation against owner-approved DEC-DEV-02 Option C and ASTRA governance semantics; identify each occurrence and its intended namespace before proposing edits.
2. **P0:** source-trace accepted A0 ingress/API, queue/claim/lease/cancellation/replay/recovery semantics, and MH-12 capability issuer lifecycle. Record unknowns as explicit contract gaps.
3. **P0:** crosswalk corporation mission/DAG/result fields against accepted MH-21 distributed-job semantics and A0 ingress; keep schemas draft until owner/source acceptance.
4. **P0:** reconcile provider/gateway/transport/client/model identities using source pins and permitted non-secret evidence; do not make runtime claims.
5. **P1:** create a concise live status index for current blockers and superseded historical decisions, without deleting historical records.
6. **Gate:** any source-level normative ASTRA edits, branch integration, tests, qualification, installation or deployment remain subject to existing change-control and explicit authorization.

## 6. Verification boundary

This is a documentary source review based on fetched GitHub files and a live branch comparison. No repository-wide automated scanner was run, and this report does not assert exhaustive detection of every conflict. The referenced blob SHAs identify the exact documents reviewed in this wave. Re-fetch before subsequent edits because the branch may advance.
