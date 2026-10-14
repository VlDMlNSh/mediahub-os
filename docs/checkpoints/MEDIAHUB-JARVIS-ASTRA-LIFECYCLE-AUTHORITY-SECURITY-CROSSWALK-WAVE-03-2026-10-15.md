# MediaHub OS — Jarvis / ASTRA Lifecycle Authority and Security Contract Crosswalk, Wave 03

- Date: 2026-10-15
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **SOURCE-ANCHORED CONFLICT RECORD / NOT A DECISION / NOT AN ACCEPTED CONTRACT**
- Scope: next source-bound step after Corporation Contract Reconciliation Wave 02: reconcile ASTRA A0 control-state claims with MH-12 security/state-authority semantics before specifying Jarvis mission ingress, worker identity, task DAG or result protocol.
- This pass is documentary only. No owner decision is inferred and no normative source is modified.

## 1. Live repository/ref status

- Repository: `VlDMlNSh/mediahub-os`; default branch: `main`.
- Documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Live comparison: `main` HEAD `608d7463011798ca75e36bfce4b749a9caf4f9a0`; documentation branch is `DIVERGED`, 1155 ahead / 3 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No merge, rebase, cherry-pick or ref movement was performed.

## 2. Primary sources read

| Source | Ref / live blob SHA | Normative scope / evidence |
|---|---|---|
| `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md` | `main` / `7be5fadd3055642e7823c7233f90e978a87e5366` | Canonical ASTRA reference architecture. §1 says “A0-ASTRA is the single MediaHub coordination and state authority”; §3.2 assigns command ingestion, mission decomposition, dependency ordering, queue, claim/lease, heartbeat/liveness, duplicate-controller rejection, stale-claim handling, result publication, integration and state transitions to the control plane. |
| `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md` | `main` / `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1` | Canonical architectural reconciliation/inventory. §1 repeats “A0-ASTRA = single coordination and MediaHub State Authority”; §14 lists command contract, claims/leases, queue progress, duplicate suppression, heartbeat, result publication, recovery and replay idempotency. |
| `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md` | `main` / `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` | Canonical/qualification-ready design for the distributed autonomous development fabric; includes A0 control plane and command→queue→claim→lease→dispatch→heartbeat→result→replay/recovery lifecycle. Qualification-ready design is not runtime qualification. |
| `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml` | `main` / `adc852009c3a79d0e64265a3af8a4910a1388057` | Machine-readable semantic model assigns A0-ASTRA the role `single_coordination_authority`; lists controller functions including command ingestion, queue, claim leases, heartbeat, liveness, duplicate suppression, restart recovery and result publication. |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `main` / `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Canonical machine-readable governance source. Lease TTL 600s, heartbeat TTL 120s, executor timeout 900s, result-publication timeout 120s, retry backoff 30s, maximum 3 parallel autonomous claims; credential creation authority HUMAN, auxiliary creation disallowed, rotation/revocation/audit required. These are contract values, not evidence that runtime enforces them. |
| `docs/architecture/MH-12-security-architecture.md` | `main` / `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Status ARCHITECTURE COMPLETE / GOVERNANCE REVIEW REQUIRED. Security owns identity, authentication, trust, capability, authorization, policy and isolation, but not canonical state mutation. Capability is issuer/principal/operation/resource/scope/lifetime/revocation-bound; authorization is operation-specific and fail-closed; reachability/VPN/mTLS do not alone authorize an operation. |
| `docs/architecture/MH-12-security-invariants.md` | `main` / `0609be9c3420070434014dad4529e4ccd46b0996` | Proposed → ready for governance review. Includes sole State Authority, authentication ≠ authorization, reachability ≠ trust, capability cannot self-grant/expand, AI/plugin/cloud cannot self-authorize. |
| `docs/architecture/MH-21-hybrid-cloud-distributed-ai.md` | `main` / `a76f6b35ec31d6b8fff2b0a3e8a1fd22bdbec71c` | Authorized to design, not accepted/frozen. External compute is not external authority; remote results are data until local validation and authorized State Authority path; arbitrary egress/fallback is forbidden. |
| `docs/checkpoints/MEDIAHUB-OWNER-DECISION-PACKET-01.md` | documentation ref / `a9f7929f9ac910c3fff1f1fb59f4ee68abf67e42` | Existing DEC-DEV-02 asks for one lifecycle owner across Jarvis and ASTRA; options A/B/C remain open. No new decision ID or inferred owner decision is created by this report. |
| `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md` | documentation ref / `e112cc73178eef5f71b8a814296e4902c2e80390` | Proposed mission envelope and gates G1/G2 remain OPEN: accepted A0 ingress/state owner and identity/capability issuer lifecycle are not resolved. Draft grants no implementation or deployment authority. |
| `docs/checkpoints/MEDIAHUB-CORPORATION-CONTRACT-RECONCILIATION-WAVE-02-2026-10-15.md` | documentation ref / `4dcabff5c4eda918a08ffc3cb3a58ff1a122c802` | Previous handoff explicitly calls for A0 queue/claim/lease/cancellation and security/identity source crosswalk before new corporation-wide schemas. |

## 3. Confirmed conflict — do not resolve by inference

There are two semantically different statements in live primary sources:

1. ASTRA reference architecture and component scheme describe A0-ASTRA as “single MediaHub coordination and state authority.”
2. MH-12 and MH-21 state that MediaHub State Authority is the sole canonical product-state mutation authority, while AI/remote compute and orchestration components cannot create an alternative mutation path. The map and existing owner-decision packet also record ARC-003/017/018 and an open lifecycle-owner conflict.

A defensible interpretation may distinguish ASTRA's **engineering workflow/control state** (queue, claims, leases, evidence and qualification gates) from MediaHub's **canonical product state**. The executor capability matrix already states this boundary, but the broader ASTRA prose still contains the conflicting phrase. This pass does not silently rewrite either normative source.

**Disposition:** DEC-DEV-02 remains `OPEN_CONFLICT`; no architecture owner is selected here. The next decision must establish a typed lifecycle boundary, not simply rename a controller.

## 4. What is reusable now

- ASTRA governance already provides bounded lease/heartbeat/timeout/retry/parallel-claim parameters.
- ASTRA executor capability policy provides dependency readiness, claim/lease/recovery, bounded model admission, target-SHA isolation and independent A3 verification.
- MH-12 provides the identity→authentication→trust→capability→authorization→policy path, revocation and fail-closed semantics.
- MH-21 provides the external-compute/no-external-authority and explicit egress policy.
- The Jarvis adapter draft and existing corporation/DAG crosswalks already contain candidate mission/task/result fields.

Do not create a duplicate queue, a second authority plane, or a new schema before reconciling these sources. The exact accepted A0 ingress API and capability issuer/lifecycle remain unproven/open in the checked evidence.

## 5. Contract implications for the distributed AI corporation

Any later accepted contract should explicitly separate:
- Jarvis mission/planning identity;
- ASTRA engineering queue/claim/lease/evidence authority;
- MediaHub Product State Authority;
- agent and executor identity;
- provider/gateway/upstream model identity;
- worker-node identity and trust/admission state;
- task/result/evidence identities.

User-contributed MediaHub workers remain future opt-in, untrusted-by-default, isolated and revocable. They must not receive central credentials or canonical state mutation authority. Results from local, cloud and user workers remain data until validated.

The local Mac Pro/Alamo route remains the preferred target when suitable and permitted. Claude Code Scenario B remains a target route through a compatible local backend, not evidence that Claude's hosted model executes locally. Local-only requests must fail closed rather than silently fall back to a cloud provider.

## 6. Next roadmap sequence

1. Resolve the source-level wording conflict under existing DEC-DEV-02 governance; preserve all historical IDs and keep A/B/C options visible until the owner/governance record changes.
2. Trace the exact accepted A0 ingress, queue/claim/lease/cancellation/replay interface and its evidence/status contract, using the canonical gate/governance YAML and the relevant ASTRA primary source.
3. Map the identity/capability issuer, audience, scope, expiry, revocation and audit lifecycle to MH-12; do not invent issuer defaults.
4. Reconcile existing agent/provider/task schemas against those accepted interfaces; only then draft a versioned corporation task/result contract.
5. Continue non-secret FCC, FreeLLMAPI/router, Alamo/runtime/model and Codex route identity trace. ECC remains NOT ASSESSED / NOT ADOPTED until authoritative upstream identity and revision are pinned.
6. Preserve Contour A before Contour B, Baseline 2.0 as functional authority, and all separate authorization gates.

## 7. Restrictions and verification boundary

This pass was read-only source analysis plus planning documentation. No normative source, Baseline 2.0 or runtime configuration was modified. No provider/model calls, credentials, host/runtime inspection, installation, tests, qualification, infrastructure changes, deployment, merge, rebase or cherry-pick occurred. No qualification or acceptance status is promoted.
