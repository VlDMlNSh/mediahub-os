# MediaHub OS — Corporation Contract Reconciliation, Wave 02

- Date: 2026-10-15
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **SOURCE-ONLY RECONCILIATION / PLAN UPDATE / NOT AN ACCEPTED NORMATIVE CONTRACT**
- Purpose: continue the source crosswalk for the distributed AI corporation without duplicating existing contracts or promoting unverified implementation status.

## 1. Live repository state

- Repository: `VlDMlNSh/mediahub-os`; default branch: `main`.
- Documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Live compare at pass start: `main` HEAD `608d7463011798ca75e36bfce4b749a9caf4f9a0`; documentation branch DIVERGED, 1149 ahead / 3 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No merge, rebase, cherry-pick or ref movement was performed.

## 2. Current source anchors re-read

| Source | Ref / blob SHA | Reconciliation |
|---|---|---|
| `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` | documentation ref / `a6b9f3b48c7fd6c8e5ef2b75944affae4a73f5ea` | Requires live map/bootstrap read, primary-source review, evidence-bound statuses, post-write read-back and no merge without explicit authorization. |
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | documentation ref / `b77199432491ad94329bb9328aacf2a3059909e9` | Already records corporation proposal crosswalk (§20.264), responsibility/interface matrix (§20.265), and DAG/result crosswalk (§20.266). This pass adds a new bounded reconciliation record rather than duplicating those summaries. |
| `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` | `main` / `e549692f207fbc91d9b9b9b92b8e665404f07290` | Existing target architecture already defines the Mac Pro central node, Alamo local inference route, FCC integration layer, separate Codex path, local-only fail-closed routing, provider route controls, owned GPU pool and future user-contributed compute boundary. |
| `docs/checkpoints/MEDIAHUB-JARVIS-CORPORATION-ARCHITECTURE-PROPOSAL-CROSSWALK-WAVE-01-2026-10-15.md` | `main` / `721e4c994d4800df4605af52630ea75339971a27` | Confirms the high-level corporation proposal is already partially represented; open gaps include DAG/result contracts, ECC assessment, provider identity and FCC/Alamo route evidence. |
| `docs/checkpoints/MEDIAHUB-JARVIS-CORPORATION-RESPONSIBILITY-INTERFACE-MATRIX-WAVE-01-2026-10-15.md` | documentation ref / `d5934af98552ddee99ac5658dfffc8a3049f5cad` | Separates Jarvis, ASTRA A0, Product State Authority, planner/DAG, agent registry, dispatcher, Claude Code, Alamo/runtime, FCC, provider gateway, Codex, workers, verifier, policy and GitHub adapter. |
| `docs/checkpoints/MEDIAHUB-DISTRIBUTED-TASK-DAG-AND-RESULT-CONTRACT-CROSSWALK-WAVE-01-2026-10-15.md` | documentation ref / `3669fb53d33d68e00186d40f3b4eaa6f9f5f0666` | Reuses ASTRA dependency/lease/recovery and A3 verification policy, but does not claim one accepted corporation-wide task/result schema exists. |
| `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md` | documentation ref / `e112cc73178eef5f71b8a814296e4902c2e80390` | Keeps Jarvis mission submission separate from ASTRA internal queue/claim/lease/gate state; draft only, exact A0 ingress/issuer contract still requires primary-source confirmation. |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | documentation ref / `9ad83781a8da53d1a8f540ede54eba95281f01c0` | Existing canonical ASTRA policy covers dependency-aware dispatch, claim/lease/heartbeat/recovery, bounded executor admission, target-SHA isolation and independent A3 verification within ASTRA's authority. |

## 3. Findings and decisions

1. **Do not invent a second controller or queue.** Jarvis coordinates missions; ASTRA A0 remains the sole writer of ASTRA-internal queue, claim, lease, retry/cancellation and gate state under its accepted contract. Product State Authority remains the only canonical product-state writer.
2. **Do not duplicate narrow schemas.** The AI inference request schema describes an inference operation; the component evidence record describes component/gate evidence. Neither should be repurposed as a complete task DAG or per-task result protocol.
3. **The local-first direction is already represented in the accepted target architecture.** Local-only must fail closed; no silent cloud fallback. Cloud/provider routing remains policy-gated, and per-hop identity/egress evidence remains necessary.
4. **Claude Code Scenario B remains a target, not verified behavior.** Claude Code is the client/tool surface; Alamo is the intended local inference endpoint in the target architecture. Actual compatibility, exact FCC mapping, Alamo-to-runtime identity and route evidence are not qualified by documentation alone.
5. **User-contributed MediaHub remain future opt-in workers.** They must be untrusted by default, isolated, resource-bounded, revocable and limited to minimum policy-approved data. No worker gains authority by returning a result.
6. **ECC upstream assessment is blocked at source identity/retrieval.** The configured GitHub connector did not return file metadata for the expected `affaan-m/everything-claude-code` file URLs, and the search surface surfaced mirror/fork material rather than a revision-pinned authoritative source. No license, current upstream revision, code side effects or component provenance is claimed verified. ECC remains NOT ASSESSED / NOT ADOPTED; do not install or import it.
7. **Branch divergence is an active integration blocker.** This pass must remain documentation-branch-only; no branch integration is implied.

## 4. Remaining contract gaps

- Exact accepted A0 mission ingress, identity/capability issuer, worker identity lifecycle and cancellation/retry interface.
- Agent/executor profile and eligibility schema aligned with existing registries.
- Corporation-wide task DAG contract: stable task identity, dependency edges, immutable input/base revision, idempotency/replay semantics, cancellation propagation, bounded retries and integration gate.
- Structured task result envelope with executor/route identity, input and contract revisions, artifacts/digests, status, checks, limitations and verifier evidence.
- Evidence-bound mapping of FCC, FreeLLMAPI, OmniRoute/UnoRouter, Alamo, local runtime/model and separate Codex route.
- Revision-pinned ECC upstream source, license, provenance, hooks/scripts/MCP permission review, overlap map and explicit admission recommendation.

## 5. Next development plan

1. Read the accepted ASTRA A0 queue/claim/lease/cancellation contracts and security/identity sources; record exact path, section and blob SHA for each interface.
2. Reconcile the existing provider/agent registries and schemas against the task/result gaps; no new schema until overlap and historical IDs are checked.
3. Continue non-secret source/config-history reconciliation for FCC, FreeLLMAPI, OmniRoute/UnoRouter, Alamo/runtime/model and Codex route identity. Do not access credentials or invoke providers.
4. Retry ECC source-only review only after resolving the authoritative upstream repository/ref. If source identity cannot be established, keep it blocked and assess alternative already-pinned components instead.
5. Prepare a versioned corporation task/result contract proposal for owner/governance review only after steps 1–4. No acceptance, implementation, qualification or deployment status is inferred.

## 6. Restrictions and verification boundary

This pass was read-only source analysis plus documentation planning. No model/provider calls, credential access, host/runtime inspection, installation, tests, qualification, configuration or infrastructure changes, deployment, merge, rebase or cherry-pick occurred. No normative contract or Baseline 2.0 was modified; no status was promoted.


## 7. ASTRA capability-matrix ref drift — source-backed delta (2026-10-15)

- Compared the same path on live refs: `main` blob `da26185254d9954fcee204f81ecca129bf052e7c` labels A0 `Global coordination/state`; documentation branch blob `9ad83781a8da53d1a8f540ede54eba95281f01c0` narrows this to `ASTRA workflow/control state` and explicitly excludes canonical MediaHub product state.
- Cross-checked `MH-12-security-architecture.md@main` blob `cf4ebfd5bf471ca676f075c51d3a24906504e490` and `MH-12-security-invariants.md@main` blob `0609be9c3420070434014dad4529e4ccd46b0996`: they specify a layered authorization path and sole canonical mutation authority, while the invariants document remains proposed/ready for governance review.
- Disposition: confirmed documentation-ref drift, not a runtime defect or evidence of deployed enforcement. The docs clarification is consistent with owner-approved DEC-DEV-02 Option C, but it is not merged into `main`. No source contract was rewritten and no branch integration occurred.
- Keep P0-07→P0-05 caller/adapter edge NOT ESTABLISHED, issuer/attester/verifier lifecycle OPEN, and P0-05 D6 OPEN. See the detailed source trace in [Wave 07](MEDIAHUB-A0-LIFECYCLE-MH12-CAPABILITY-ISSUER-SOURCE-TRACE-WAVE-07-2026-10-15.md), blob `49ca0b69737bf8d44fe3a42daa47fd9157c9097d`.
- Next: continue existing schema/ID inventory only from exact source files; do not draft a normative corporation wire schema before ingress/identity ownership and branch conflict are resolved. No tests, installation, provider calls, credentials, host/runtime inspection, qualification, infrastructure changes, deployment or branch integration.
