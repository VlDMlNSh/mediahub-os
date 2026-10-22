# MediaHub OS — Contour A WB-14: Jarvis/A0 and Direct-Local Route Source Reconciliation

- Date: 2026-10-15
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **READ-ONLY SOURCE RECONCILIATION / PARTIAL / DECISIONS OPEN / NOT IMPLEMENTED / NOT QUALIFIED**
- Purpose: split the next continuation into small bounded work packages and execute the first source-reconciliation pass against WB13-R01…R12.
- No normative source was modified in the original WB-14 pass. No tests, qualification, model/provider calls, credentials, host/runtime inspection, installation, infrastructure change, deployment, merge, rebase or cherry-pick occurred in that original pass.
- **Wave 364 owner clarification (2026-10-22): Alamo is hosted on `Voktors-Mini.Dlink` (Mac mini 2018, macOS). This resolves host identity only; runtime/profile, provider/egress mode, media backend, capacity and autonomous-route qualification remain unverified.**

## 1. Small-request decomposition

This continuation is divided into the following independently reviewable requests:

1. **WB-14A — Source baseline and identity:** refresh relevant refs and pin exact source blobs for ASTRA A0, task ingress, authorization, signed commands, and direct local execution. **Completed in this document.**
2. **WB-14B — Ingress/authority seam:** trace Jarvis mission request → accepted A0 ingress and determine what source proves versus what remains missing. No schema wiring.
3. **WB-14C — Direct local queue candidate:** compare the existing bounded autonomous queue against Route B needs; distinguish existing behavior from proposed Alamo behavior.
4. **WB-14D — Cross-route lifecycle controls:** map idempotency, queue ownership, lease/fencing, cancellation, retry, restart recovery and result provenance; identify contract gaps.
5. **WB-14E — Provider/data locality and workload admission:** distinguish local client from local inference, pin egress semantics, and record the unknown Alamo/media backend facts.
6. **WB-14F — Contradiction and owner-decision packet:** consolidate only evidenced conflicts and unresolved decisions; recommend options without selecting for the owner.
7. **WB-14G — Documentation reconciliation:** read back all updated artifacts, validate links/SHA and ensure the next checkpoint does not duplicate completed work.

These are documentary sub-requests, not authorization to run tests, inspect hosts, call providers, install software, or deploy.

## 2. Refreshed source pins

Repository: `VlDMlNSh/mediahub-os`; canonical implementation source ref: `main`; working documentation ref: `docs/mediahub-chat-tree-map-20261012`.

| Source | Ref | Blob SHA | Direct evidence relevant to this pass | Limit |
|---|---|---|---|---|
| `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md` | main | `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` | A0 is the ASTRA coordination/state authority; permanent executor pool names mh-dev-01, mh-dev-02 and Voktors-Mac-mini.local; Claude Code client and Claude provider are distinct concepts. | Does not establish Alamo registration or an independent Jarvis→Alamo route. |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | main | `da26185254d9954fcee204f81ecca129bf052e7c` | A0 owns ASTRA queue/claim/evidence state, model/executor admission and resource qualification; specialist roles cannot create authority. | Static policy, not runtime proof. |
| `runtime/mediahub_runtime/autonomous_queue.py` | main | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Permanent executor pool is fixed to three named lanes; task selection binds node_id and executor; claim and queue state are handled by the ASTRA runtime. | No Alamo lane; not proof of an accepted separate local queue lifecycle. |
| `runtime/mediahub_runtime/task_ingress.py` | main | `59e1254aa61cc8f55f53bd1e179631e81c441393` | FileTaskIngress parses JSON files, checks selected schema/shape fields and passes AstraTaskRequest to AstraGatewayRuntime.run_bounded. | Inspected source does not establish authenticated Jarvis caller, trusted inbox writer, or an AuthorizationContext issuer edge. |
| `runtime/mediahub_runtime/astra_gateway.py` | main | `10985e4ad8f682313d08e7492ecc1856a8bce20f` | AstraTaskRequest contains request/session/command/context/approval fields; gateway is a separate bounded intake/execution seam. | The request type itself is not proof of authenticated caller or approval attestation. |
| `runtime/mediahub_runtime/authorization.py` | main | `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | AuthorizationContext is principal + capability; policy allows only explicit configured triples. | No source edge from FileTaskIngress to this context was established in WB-07. |
| `ops/control/sign_command.py` | main | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Defines `mediahub.astra.control-command.v1`, required fields, per-node HMAC key mapping and freshness validation. | Operational command signing is not automatically the Jarvis task-ingress contract. |
| `astra_github_agent.py` | main | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Verifies the same command schema/HMAC/freshness and tracks executed command IDs before dispatch. | Does not establish that FileTaskIngress and this signed-command path are connected. |
| `tools/sign_astra_command.py` | main | `a4222ac51a47cbfe8288f9af34f1e542c0a4b6a8` | Emits a distinct `schema: 1` envelope and uses `ASTRA_COMMAND_HMAC_KEY`. | Active/canonical status remains unknown; do not delete or consolidate by inference. |
| `.github/workflows/astra-autonomous-supervisor.yml` | main | `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | Workflow references the node-specific signer and control-command files. | Workflow presence is not successful runtime qualification or Jarvis-ingress proof. |
| WB-07 ingress seam trace | docs ref | `89fab594f9a9ae9a729d63ecb14dad2543edc9af` | Separates FileTaskIngress, P0 typed authorization and signed command flows; explicitly limits conclusions. | Documentary trace, not complete global caller proof. |
| WB-10 direct local route matrix | docs ref | `62101df270acd1f4e551a8fcaf69f1fe741a8b51` | Owner-directed Route B is separate and must not bypass security/evidence controls; no implementation claimed. | Requirements are not proof that the route exists. |
| WB-11 Alamo/Claude trace | docs ref | `b34b50dc749cade5b32e6ed369fe5b430d1a788e` | Existing external Anthropic and Ollama-backed Claude-compatible workflow patterns differ; neither is proven to be the active Alamo route. | Host identity is Voktors-Mini.Dlink; provider mode and media backend remain unknown. |
| WB-12 topology matrix | docs ref | `87ce2d51c81d3e5c8dfe2517f61878d91a0e069a` | Options A/B/C compared; C is a design recommendation only. | No topology is owner-accepted by this matrix. |
| WB-13 route-adapter matrix (this continuation) | docs ref | `e6fd3e070abb9da21c1a98e1c661cffe86b16e6c` | Defines WB13-R01…R12 and required controls/evidence. | Non-normative; no implementation/qualification. |

## 3. Findings mapped to WB13-R01…R12

| WB-13 requirement | Source-level reconciliation | Disposition |
|---|---|---|
| R01 Stable mission identity | `AstraTaskRequest.request_id` exists and FileTaskIngress rejects duplicate IDs within one read batch; no common Jarvis/A0/Alamo mission envelope is evidenced across both routes. | PARTIAL; define cross-route identity/idempotency contract before implementation. |
| R02 Auditable route policy | WB-10/WB-12 specify policy as a requirement, but reviewed runtime source does not establish a common route-decision authority across A0 and a direct queue. | OPEN; owner/governance decision required. |
| R03 A0 lifecycle authority | Canonical executor matrix and queue reference align A0 with ASTRA queue/claim/lease/evidence lifecycle. | SOURCE-ALIGNED for ASTRA internal route; runtime not qualified here. |
| R04 One Alamo queue owner | Existing permanent pool excludes Alamo; no accepted direct-route queue owner is identified in the inspected sources. | BLOCKED; must name owner and define lifecycle before dispatch. |
| R05 Authenticated caller | Task Contract ingress shape validation and signed operational-command verification are separate seams. | BLOCKED for end-to-end Jarvis ingress; do not treat schema shape as authentication. |
| R06 Approval provenance | Task ingress maps file-supplied approval state into request; WB-07 did not establish trusted writer or attestation issuer. | BLOCKED; define authority and verifiable task/action/resource binding. |
| R07 Provider/egress identity | Unified ASTRA source distinguishes Claude Code local client from Claude/Anthropic provider; repository also has an Ollama-backed Claude-compatible workflow. | UNKNOWN for Alamo; require explicit provider/runtime and egress declaration. |
| R08 Media backend/resource envelope | ASTRA queue pool is coding-oriented and does not establish a qualified Alamo video backend. | BLOCKED; host identity is Voktors-Mini.Dlink; backend and capacity evidence still required. |
| R09 Result/evidence contract | Gateway has a request/result/evidence type, while ASTRA queue has its own evidence lifecycle; a normalized cross-route envelope is not evidenced. | DRAFT CONTRACT NEEDED; do not merge evidence schemas by assumption. |
| R10 Retry/cancel/recovery ownership | ASTRA queue owns its internal lifecycle; no direct Alamo lifecycle is source-pinned. | OPEN/BLOCKED for Route B; avoid dual retry authorities. |
| R11 No second State Authority | ASTRA sources explicitly constrain A0 to its own queue/coordination state; MediaHub Product State Authority remains a separate boundary in D-03 reconciliation. | REQUIRED INVARIANT; preserve domain-scoped authority. |
| R12 Separate readiness gates | WB-07/WB-08 and roadmap distinguish documentary design, implementation, verification, qualification, deployment and acceptance. | REQUIRED INVARIANT; no readiness promotion from this pass. |

## 4. Explicit contradictions and non-contradictions

1. **Not inherently contradictory:** Jarvis as top-level mission coordinator and A0 as owner of ASTRA-internal queue lifecycle can coexist if the route/authority boundary is explicit.
2. **Unresolved authority seam:** FileTaskIngress accepts an `approval_state` field after shape/enum checks; the reviewed path does not show the issuer/attestation edge that would make it trusted approval evidence. This is a source gap, not a confirmed exploit.
3. **Separate trust domains:** signed operational commands (`mediahub.astra.control-command.v1`) and Task Contract JSON (`mediahub.ai.astra-task` v1.0.0) are distinct formats. Do not wire them together or treat signatures as interchangeable without an accepted contract.
4. **Canonicality unknown:** `tools/sign_astra_command.py` emits a second schema/key convention. WB-08 says active/canonical status is unknown; no deletion, rename or key/schema consolidation is justified.
5. **Route B not evidenced as implemented:** the reference autonomous queue only names three permanent nodes and does not include Alamo. Owner direction permits design of a separate route, but is not runtime evidence.
6. **“Local Claude” is ambiguous:** local client placement does not establish local inference; external Anthropic and local Ollama-compatible patterns have different data-egress consequences.
7. **Duplicate WB-13 artifact identity:** project map already contains a WB-13 “Option C route-adapter requirement/failure/verification matrix” with creation commit `dcf8c4746d2e9cb965b24f6e0d86f09f4b2cbabb`, while a later distinct WB-13 file was added by commit `1108abd34a4bd1a8a0643234bfaadb7bbf261146`. This is a document-ID/navigation collision, not proof that either artifact is invalid. Preserve both files and historical IDs; add an explicit map note so future work cites the intended artifact by full filename.

## 5. Owner decisions that remain open

- Select topology target: A (A0-governed), B (direct separate queue), or C (common non-authoritative route adapter).
- Confirm Alamo runtime/profile on Voktors-Mini.Dlink and qualify its provider/egress mode.
- Specify whether Claude means local client to external Anthropic service or local model runtime; identify model/provider and egress policy.
- Identify actual video-generation backend and its license/qualification constraints.
- Name direct-route queue lifecycle owner and define claim/lease/fencing, retry, cancel, restart recovery and idempotency.
- Define route eligibility and who may authorize route change/failover.
- Define trusted Task Contract inbox producer/writer, approval authority/attestation, and the approved Jarvis→A0 ingress.
- Decide whether the second signer helper is active, legacy or superseded after a bounded caller/history trace.

No decision is inferred or accepted by this document.

## 6. Bounded next steps

Proceed in the small-request order from §1:
- **Next: WB-14B** — trace Jarvis mission submission and the accepted A0 ingress without modifying contracts. Produce a caller-to-consumer evidence chain, or a precise gap statement.
- Then WB-14C through WB-14F only after the previous evidence is read back.
- WB-14G closes the documentation pass with SHA/link consistency.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
