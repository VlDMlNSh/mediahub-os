# MediaHub OS — Contour A WB-14R: A0 ingress authority reconciliation and schema crosswalk

- Date: 2026-10-16
- Status: **SOURCE-BOUND RECONCILIATION / DESIGN RECOMMENDATIONS / NORMATIVE DECISIONS OPEN / NOT IMPLEMENTED / NOT TESTED / NOT QUALIFIED**
- Target documentation ref: docs/mediahub-chat-tree-map-20261012
- Scope: continue WB-14Q with a source-pinned review of authority wording, field-level schema reuse, command-contract collisions and branch-specific evidence.
- Change boundary: documentation only. No normative ASTRA contract, schema, runtime source, configuration or infrastructure was modified. No tests or qualification were run.

## 1. Result

WB-14R advances the formal ASTRA A0 ingress design in four ways:

1. It reconciles the owner-approved Jarvis / ASTRA A0 / Product State Authority split against ASTRA authority statements on both live branches.
2. It maps WB-14Q ingress fields against existing identity, capability, inference, command, task, result, executor and evidence artifacts, distinguishing reusable meaning from incompatible wire formats.
3. It identifies contract collisions that must be resolved before a schema can be normative: incompatible operational command envelopes, overloaded identity/capability schemas, conflicting status vocabularies and a request envelope that does not yet separate submit/status/cancel/result payloads cleanly.
4. It distinguishes docs-branch scoped authority wording from still-unreconciled main wording and identifies old executor-lane identities still stated as permanent target topology.

**Conclusion:** the logical direction “Jarvis → authenticated A0 ingress interface → A0-owned admission/lifecycle” is supported by owner direction. No accepted, end-to-end corporation-level Jarvis-to-A0 wire contract was evidenced in this pass. Keep transport, capability issuer, authentication technology, persistence/idempotency owner, schema registry and final status vocabulary open. Do not reuse old node-bound command transport as the target mission interface.

## 2. Live refs and branch reconciliation

Observed at the start of this pass:

| Ref | HEAD / tree | Result |
|---|---|---|
| main | HEAD/tree SHA ab36db009d034db8dca723691e23b331322287e7 | Includes four commits not present on the docs branch. |
| docs/mediahub-chat-tree-map-20261012 | HEAD 3ca310c94f8746e2b47a8927ce66ec881484105d | Current working documentation branch. |
| Comparison | merge base f0f406feb9f9816b009f4e6e756813541e53b9bc; docs ahead 1481 / behind 4 | Diverged; no merge, rebase, cherry-pick or main ref movement. |

The four commits ahead on main introduce two documentary sources and modify the historical Baseline 1.0 file. The main-only documents are:
- WB-14 source reconciliation: [MEDIAHUB-CONTOUR-A-WB-14-JARVIS-A0-AND-DIRECT-LOCAL-ROUTE-SOURCE-RECONCILIATION-2026-10-15.md](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-14-JARVIS-A0-AND-DIRECT-LOCAL-ROUTE-SOURCE-RECONCILIATION-2026-10-15.md), blob SHA 4dead9e249603679f4193a5a0b0b0a13a04aa177.
- Corporation proposal crosswalk: [MEDIAHUB-JARVIS-CORPORATION-ARCHITECTURE-PROPOSAL-CROSSWALK-WAVE-01-2026-10-15.md](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/MEDIAHUB-JARVIS-CORPORATION-ARCHITECTURE-PROPOSAL-CROSSWALK-WAVE-01-2026-10-15.md), blob SHA 721e4c994d4800df4605af52630ea75339971a27.

These were read and used to avoid repeating their source-inventory work. The main-only WB-14 packet's next step is labelled WB-14B, while the docs-branch continuation has WB-14P → WB-14Q → WB-14R. These are branch-local work sequences, not proof that either branch can be integrated. The main-only Baseline 1.0 modification was not imported or reinterpreted; Baseline 2.0 remains the canonical functional baseline and Baseline 1.0 remains historical.

No branch integration was attempted.

## 3. Authority wording reconciliation

### 3.1 Owner decision and controlling target split

The owner-decision record on the docs branch, [Owner Decisions and Corporation Direction](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CHAT-TO-GITHUB-OWNER-DECISIONS-AND-CORPORATION-DIRECTION-WAVE-01-2026-10-15.md), blob SHA 70376a2709e055972ceddc4a280d26992977213c, records explicit approval of DEC-DEV-02 lifecycle split:

- Jarvis coordinates corporation-level missions, bounded decomposition, permitted route selection and mission-result tracking.
- ASTRA A0 owns ASTRA-internal queue, claim, lease, heartbeat/liveness, retry/cancellation, recovery and ASTRA-specific evidence/gate transitions within its accepted contract.
- MediaHub Product State Authority remains the sole canonical product-state mutation authority.
- Executors, transports, providers, models and adapters gain no authority by implication.

The approved lifecycle split is not the same decision as the route-topology “Option A/B/C” matrix. Avoid referring to DEC-DEV-02 as bare “Option C”: the route-adapter workstream separately used A/B/C for different topology alternatives, creating an ID/name collision.

### 3.2 Exact source discrepancy table

| ID | Source and live revision | Direct observation | Reconciliation status / proposed treatment |
|---|---|---|---|
| AUTH-01 | Reference architecture: docs blob b354acfa4cff595583a7f1778371143e9868f293; main blob 7be5fadd3055642e7823c7233f90e978a87e5366 | Docs branch §1 scopes A0 to ASTRA GOLD engineering coordination and ASTRA-internal queue/claim/gate state only, explicitly excluding Product State Authority. Main §1 still says “single MediaHub coordination and state authority.” | Docs branch is aligned more closely to owner direction; main remains conflicting. Do not treat the docs text as already integrated into main. |
| AUTH-02 | Complete component scheme: docs blob d321565a6e0fac1eef329adec67a35ba795b63aa; main blob 54ba34ce53d1d7ecd97eef459be7d055b4fd19b1 | Docs branch §1 scopes A0 to ASTRA-internal queue/claim/gate state. Main §1 still calls A0 the single coordination and MediaHub State Authority. | Same branch-specific conflict. Controlled reconciliation is required; no silent rewrite of normative/historical sources. |
| AUTH-03 | Unified ASTRA Markdown: docs blob 610a611f42d19a55ab7a172e00068c40c5ce5da5; main blob e2067dc41b52983fc4e0b2549fb6af3c099cbc60 | Both §3 still say “A0 Astra is the single coordination authority.” Surrounding content is ASTRA-scoped, but the sentence does not explicitly bound its scope. | Proposal: narrow it to “A0 Astra owns ASTRA-internal engineering workflow coordination and state under the accepted A0 contract.” Preserve Jarvis corporation-level mission coordination and Product State Authority boundaries. Not patched here. |
| AUTH-04 | Unified ASTRA YAML: docs blob f5040aeb479176508d5b0ca35eb742a6db818867; main blob adc852009c3a79d0e64265a3af8a4910a1388057 | Docs YAML specifies A0 engineering coordination for ASTRA-internal workflow state only and excludes canonical Product State Authority; main uses the broader single-coordination-authority role. | Docs YAML is more precisely scoped. Reconcile versions through the approved process; do not normalize by assumption. |
| AUTH-05 | Qualification/launch schema: docs blob 0b86b07dfa916d4485ce1f8f54d19de136d98491; main blob aef6229477ed8ec45e45170f98ea87f7ba75ca29 | Docs branch annotates state_authority A0-ASTRA as ASTRA internal queue/claim/gate state only and excludes Product State Authority. Main has the same key but omits that explanatory comment. | Docs wording is explicit; main remains ambiguous. The comment is not a substitute for controlled synchronization and does not prove runtime behavior. |
| AUTH-06 | Reference architecture docs §3.3, docs blob b354acfa4cff595583a7f1778371143e9868f293; unified ASTRA Markdown § executor pool, docs blob 610a611f42d19a55ab7a172e00068c40c5ce5da5; main versions also reviewed | Both branches continue to call mh-dev-01, mh-dev-02 and Voktors-Mac-mini.local permanent production executor lanes. | Conflicts with the greenfield bootstrap rule that old host identities are legacy context only. Preserve history; target host/executor identities remain UNKNOWN/BLOCKED until an owner-sourced target inventory exists. |
| AUTH-07 | Bootstrap instruction, docs blob a3c51f3ddf17827bf6193cce52387a5daad3b6e0, compared with the above reference/unified sources | Bootstrap says old server identities, paths and runtime observations are historical and are never target requirements/evidence; the ASTRA executor pool still labels old names as permanent. | Direct documentary contradiction. Reconcile target topology in a controlled change. This audit does not choose replacement nodes. |
| AUTH-08 | ASTRA GOLD governance contract, both refs blob 1d3ac25e7817f365807ad85d0d7c9007bd48bebf | Governance is the machine-readable source for ASTRA gates/numeric thresholds, but it does not establish a corporation ingress wire contract or capability issuer. | Reuse numeric ASTRA thresholds only by reference and within their scope. Do not clone them into mission schemas or infer an issuer from governance ownership. |

### 3.3 Suggested canonical authority sentence — proposal only

Candidate text for a future controlled source patch:

> Jarvis is the corporation-level mission coordinator and selects only policy-permitted routes. ASTRA A0 owns ASTRA-internal engineering workflow state—queue admission, claims/leases, heartbeat/liveness, retry/cancellation, recovery and ASTRA-specific evidence/gate transitions—under the accepted A0 contract. MediaHub Product State Authority alone owns canonical MediaHub product-state mutation. No executor, model, provider, transport, cloud controller or adapter acquires either authority by implication.

This is a proposal for review, not an accepted replacement. Exact A0 responsibilities must still be reconciled against the canonical qualification schema and accepted ASTRA contracts before implementation.

### 3.4 Legacy topology is a separate reconciliation axis

Even where docs-branch authority language is already scoped, the same sources retain an explicitly named three-lane production topology. A wording change alone is insufficient. The target must not inherit old hostnames, user paths, old node IDs, per-node HMAC environment names or old worktree locations as defaults. Until an owner-sourced target inventory exists, target host identity, executor bindings and deployment paths remain UNKNOWN. This audit does not replace the old values with invented ones.

## 4. Field-level crosswalk: WB-14Q ingress request

Source pins used:
- WB-14Q proposal: blob 2b0cf853a7b5eefe9e75fccdcfed130d53f417c8.
- Corporation mission/task/result schema-set draft: blob e6c65c9949f45d247a2a57d1806da33737060619.
- Agent/task/provider schema inventory: current docs blob 81d6435b2571f7c261d08b763b6fc30c4d3c6207.
- ASTRA capability policy: docs blob 9ad83781a8da53d1a8f540ede54eba95281f01c0; main blob da26185254d9954fcee204f81ecca129bf052e7c.
- MH-12 Security Architecture: blob cf4ebfd5bf471ca676f075c51d3a24906504e490.
- Identity-boundary schema: blob 1d085bb1f2c458faaeff23bd92d83aa5d1bd3879.
- Device identity schema: blob 2caf58faf58eff2de82984a28109eb1aae87675d.
- Device capability schema: blob fe80659b570ac58829f10410feb5c700388f87c0.
- Mesh capability schema: blob d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c.
- AI model capability schema: blob d84b2ddcc91326ba31f55513c0703c9707d68d64.
- AI inference request schema: blob e59c72b4a2a62b2372da57c6699ab12ebe25122f.
- Agent registry: blob 993cbbe1b2b2a88da7d8884a897b404f055981a8.
- Component-evidence record draft: docs blob 2e62a9d0174e2c72e23ac88edc3094d13b4e336a.

| WB-14Q field group | Existing coverage / exact scope | Crosswalk result |
|---|---|---|
| Schema identity/version | AI inference request has its own ID/version; identity boundary fixes its own 1.0.0 version; component evidence uses record_schema_version; A0 commands use a different version field. | Partial but non-uniform conventions. Do not register new A0 IDs until ownership, naming, compatibility and version policy are accepted. |
| Request/correlation/parent IDs | Identity-boundary schema defines request, correlation and causation ID slots. Task ingress has request_id. | Reuse identifier-separation concepts, then define uniqueness scope, parent/causation semantics and lifetime. Do not equate request_id, command_id, mission_id, task_id, execution_id and attempt_id. |
| Mission/task/DAG/dependencies | ASTRA capability matrix defines dependency readiness and same-base-SHA requirements. The corporation schema-set draft proposes a mission envelope, immutable task DAG and distinct task/attempt identifiers. | No accepted corporation-wide DAG wire schema identified. Continue the existing draft family instead of creating a second graph model; define DAG identity/revision and dependency references before A0 submission becomes normative. |
| Issuer/principal/audience/credential reference | MH-12 defines principal classes and identity → authentication → trust; credentials are distinct from principal, session, capability and authorization. It does not select the technology or concrete ingress principal schema. | Semantic requirements exist; concrete caller/audience representation and issuer are OPEN. A body-provided issuer string cannot prove authenticated identity. Credential reference can only be a non-secret reference. |
| Capability reference/scope/constraints | MH-12 requires principal, issuer, operation, target/resource, scope, constraints, provenance, lifetime and revocation context. Domain capability describes device-exposed operations; AI model capability describes inference operations; mesh capability describes component/executable metadata. | These are not interchangeable with an authorization capability/token. No accepted security-capability wire schema or issuer lifecycle was found. Keep capability_ref opaque until the issuer/delegation/revocation contract is accepted. |
| Signature/algorithm/key ID/value | MH-12 leaves cryptographic mechanisms UNKNOWN pending evidence and ADR. Operational command signer uses node-specific HMAC keys; a second signer emits another envelope. | WB-14Q inline signature fields are illustrative only. Do not choose HMAC, detached signature, mTLS, token format, canonicalization or key registry by assumption. |
| issued_at/expires_at/freshness | Operational command signer uses integer Unix issued_at and max-age validation; WB-14Q uses RFC3339-like placeholders. MH-12 does not settle the crypto profile. | Timestamp representation and freshness are not interoperable yet. Select one canonical representation, clock-skew rule, expiry semantics and replay-retention scope. Do not inherit old command max-age as ingress policy by default. |
| Operation / command identity | Operational command has operation, node-bound command_id, target SHA and exclusive-action metadata. AI inference operation is limited to inference actions such as generate/classify/embed/transcribe/transform. | Neither vocabulary defines Jarvis→A0 operations. Create a separate versioned operation vocabulary; keep operational command IDs separate from mission requests. |
| Target source / target SHA / input digest | ASTRA control commands require exact target_sha; A0 qualification binds results to source SHA. Schema-set draft proposes target/input digests. | Strong reusable invariant, but repository/ref/SHA, task revision, digest algorithm and canonicalization must be explicit. A mutable branch name cannot substitute for immutable commit binding. |
| Route / route policy / executor profile | WB-10 and WB-13 distinguish the A0 route and separately governed direct-local route. Agent registry has IDs, tiers and declared capabilities; ASTRA matrix covers admission requirements. | Route provenance is required new cross-domain data. Registry declarations do not prove live presence, authorization or qualification. No implicit fallback or duplicate cross-route dispatch. |
| Owned paths / allowed actions | Operational command has owned_paths and exclusive_actions. ASTRA policy requires isolated workspaces and bounded claims. | Reuse the safety concept, not the node-bound operational-command definitions. Task path/action restrictions require accepted capability and workspace enforcement. |
| Data class / egress | Component-evidence draft includes data classification and egress policy. MH-12 treats cloud as external/untrusted by default and requires fail-closed authorization. | Partial descriptor coverage only; it is evidence metadata, not a request-time enforcement API. Bind values to accepted policy IDs and an admission decision. |
| Budget / deadline / attempts / retry | ASTRA governance defines internal lifecycle thresholds; corporation schema draft proposes bounded budgets and deadlines. | Reference ASTRA limits by contract/revision rather than copying numbers into ingress schema. Retry ownership belongs to A0 for the A0 route; ingress must not become a second retry controller. |
| Payload digest / idempotency key | Schema-set draft proposes canonical payload binding; ASTRA transport tracks executed command IDs. No accepted corporation admission-store contract was identified. | No global exactly-once side-effect guarantee. Define key scope, digest algorithm, durable admission boundary, retention, same-key/different-digest rejection and uncertain-commit recovery. |
| Health challenge / nonce / response digest | Existing health command defines node-bound command/result files and warns against reusing old IDs/results; it does not define a caller-generated challenge plus response correlation. | WB-14Q challenge-response is new contract surface. Correlate a fresh challenge, request digest, expected responder identity and response time. Existing health command is not this protocol. |
| Acknowledgement / status / cancellation | No accepted corporation-wide A0 acknowledgement, query-status or cancellation wire schema was established. | Define operation-specific request/response schemas or a strict discriminated union. ACCEPTED means durably admitted, not started; cancellation acknowledgement does not prove execution stopped. Include INDETERMINATE for uncertain commit. |
| Task result / artifacts / independent verifier | Schema-set draft proposes task result/evidence reference. Component evidence is for component/gate/deployment evidence, not generic per-task output. AstraGatewayRuntime has a separate request/result/event type. | Reuse the task-result draft as candidate. Reference component/gate evidence by stable identity and digest only where its semantics fit; do not reuse the application gateway result as A0 lifecycle result. Worker cannot self-certify VERIFIED or qualification PASS. |
| Result state / A0 lifecycle / admission decision | WB-14Q's candidate status list differs from the prior task-result draft; MH-06 has separate health and readiness values. | These are distinct state domains. Separate admission disposition, A0 lifecycle state, attempt outcome, verifier disposition, qualification gate and health/readiness. Align each enum to its owning contract before versioning. |
| Time/resource/health evidence/revision | Component evidence has observed_at, source SHA, artifact digest and policy/gate revisions; governance has a separate evidence freshness window. | Health nonce TTL, request freshness, evidence freshness and qualification freshness are not interchangeable. Define each independently. |

## 5. Existing contract and schema collisions

### COLL-01 — Two operational command signers are not one contract

- ops/control/sign_command.py, SHA fc6943a79cefdf06e59d6e32771d2df551b2f0e9, declares mediahub.astra.control-command.v1 and requires schema_version, command_id, node_id, operation, target_sha, workflow_only, owned_paths, title, description, exclusive_actions and issued_at. It uses per-node HMAC environment keys for old identities and freshness validation.
- tools/sign_astra_command.py, SHA a4222ac51a47cbfe8288f9af34f1e542c0a4b6a8, emits schema: 1, command_id, node_id, operation, issued_at and signature using generic ASTRA_COMMAND_HMAC_KEY.
- docs/qualification/ASTRA-HEALTH-COMMAND-CONTRACT.md, SHA 5a06ec6a649c378793063d0f4f9a8a532621c11d, documents a schema: 1 health example without several fields required by the node-specific signer.

These sources demonstrate distinct command conventions and a documentation alignment gap. The sources do not establish that the generic signer is canonical/active. Do not delete, consolidate, execute or wire either into Jarvis ingress from this finding. Reconcile operational command history separately from the new corporation ingress contract.

### COLL-02 — FileTaskIngress is not Jarvis→ASTRA A0 ingress

- runtime/mediahub_runtime/task_ingress.py, SHA 59e1254aa61cc8f55f53bd1e179631e81c441393, accepts file-based mediahub.ai.astra-task v1.0.0 with request_id, session_id, user_command and approval_state, then forwards it to AstraGatewayRuntime.run_bounded.
- The source validates approval_state against an enum, but this source trace did not establish a trusted attestation issuer or who wrote the input file.
- runtime/mediahub_runtime/astra_gateway.py, SHA 10985e4ad8f682313d08e7492ecc1856a8bce20f, has separate bounded task/result/event types and provider/runtime routing. runtime/mediahub_runtime/authorization.py, SHA 4d8df5d3c1c26f7f133a8093cd270635b085f4d5, provides a simple explicit allow-list seam over principal/capability/operation; this source trace did not identify a complete authorization edge from FileTaskIngress to that seam.

Treat these as a distinct application-runtime ingress/execution path, not proof that Jarvis→A0 authentication, mission DAG, claim/lease, result-publication or cancellation contracts are implemented. A submitted approval_state string is not a trusted approval attestation.

### COLL-03 — “Capability” means different things across schemas

- Domain capability = device-exposed operations.
- AI model capability = supported inference modalities/operations.
- Mesh capability = registered component/executable identity, declared authority class and qualification state.
- MH-12 capability = scoped authorization grant tied to principal, issuer, operation/resource, constraints, provenance, lifetime and revocation.

Do not reuse any of the first three as an authorization token or capability issuer. A future A0 ingress should consume only an opaque capability reference validated by the accepted security/capability authority.

### COLL-04 — Identity identifiers are not credentials

The identity-boundary schema reserves IDs for device, adapter, capability, event, command, execution, request, correlation, causation and recovery. The device identity schema centers on mediahub_id/vendor/model/serial. Neither proves service-principal authentication or grants authority. Keep identifier relationships explicit; never trust an issuer field in JSON as proof of the sender's identity.

### COLL-05 — Health and readiness have scoped semantics

Accepted MH-06 ADR-001 defines health statuses UNKNOWN, HEALTHY, DEGRADED, FAILED and QUARANTINED, and operation-scoped readiness verdicts UNKNOWN, NOT_READY, READY, DEGRADED and QUARANTINED. This is scoped to MH-06 Core Runtime Services and is observational/non-authoritative. It does not define the A0 wire-health challenge/response.

WB-14Q's lowercase handshake illustration (ready, not_ready, degraded) must not be copied as the universal MediaHub health vocabulary. Keep transport/identity probe outcome distinct from MH-06 health and operation readiness. Agree mapping and contract owner before finalizing a health-response schema.

### COLL-06 — Draft task-result statuses differ

WB-14Q's candidate list and the earlier schema-set draft's attempt_status list are not identical; neither is registered as normative. Admission dispositions such as ACCEPTED/REJECTED are not task lifecycle terminal states. Before schema creation, define separate types and transitions with A0 as lifecycle owner, the result producer as untrusted and A3 verifier disposition independent of A0 qualification gates.

### COLL-07 — Authentication fields are premature

WB-14Q includes credential_ref and inline signature fields, but MH-12 leaves cryptographic profile and technology UNKNOWN pending evidence and ADR. The final wire model might use transport-authenticated context, an enveloped signature or another accepted pattern; this report selects none. Avoid a schema that assumes one before the security/capability contract is accepted.

### COLL-08 — Draft content is not a deployed contract

The mission/task/result schema-set draft, WB-13 route-adapter matrix, WB-10 direct-local route matrix, WB-05 identity trace and WB-14Q are design/evidence documents with explicit limits. They define requirements and provenance, not proof that a production A0 endpoint exists.

## 6. Recommended contract inventory, with reuse boundaries

Do not recreate the full mission/task/result family from scratch. Carry forward the existing non-normative corporation schema-set draft as the field inventory, then add the A0 ingress envelope layer and make authority boundaries explicit.

| Contract family | Responsibility | Candidate source/reuse | Remaining decision |
|---|---|---|---|
| Corporation mission envelope | Mission identity, requester provenance reference, bounded objective, constraints, policy revision and correlation | Existing mission-envelope proposal in schema-set draft | Jarvis contract owner, canonicalization, identity linkage |
| Immutable task DAG | Task IDs, DAG ID/revision, dependencies, target/input revisions, acceptance criteria | Existing task-DAG proposal + ASTRA dependency-readiness semantics | Accepted schema/version and graph invariants |
| A0 submit request | Authenticated caller context, request/idempotency identity, operation, immutable mission/DAG reference, capability ref and digest | New A0-specific contract surface; WB-14Q illustrative fields | Operation discriminator, serialization and accepted A0 service principal |
| A0 admission acknowledgement | Durable admission disposition, canonical request/digest, A0 lifecycle reference, timestamp and stable reason | New A0-specific contract surface | Persistence commit point and response consistency |
| A0 status query/response | Read-only lifecycle view with schema/revision and correlation | No accepted generic A0 wire schema found | State enum and query consistency |
| A0 cancellation request/response | Request cancellation and distinguish processing from terminal state | ASTRA lifecycle semantics only | Cancellation races and late-result behavior |
| Task result envelope | Attempt identity, target/input digest, executor/route provenance, status, artifact refs and verifier disposition | Existing schema-set draft; AstraGatewayRuntime result is not equivalent | Result states, verifier relation and artifact storage |
| Evidence reference | Immutable URI/record ID + digest + source/policy revision/time + producer/reviewer identity references | Component evidence schema only where component/gate semantics fit | Shared evidence-reference registry and retention/access policy |
| A0 ingress health challenge/response | Fresh challenge, request digest, authenticated responder, observation times, accepted contract/source revision and probe outcome | New A0-specific contract; MH-06 gives scoped health/readiness semantics, not wire protocol | Nonce TTL, clock skew, service principal, channel/signature auth and revision allow-list |
| Capability verification reference | Consume an issuer-produced scoped/revocable grant without letting Jarvis or adapter self-issue | MH-12 semantics only | Issuer, delegation, attenuation, expiry, revocation and key lifecycle |

For Submit/Status/Cancel/Result, define separate versioned request/response schemas or a strict operation discriminator and operation-specific payload union. Do not require a complete mission/task body for status query or cancellation. Structurally reject ambiguous payload variants, and keep acknowledgement separate from lifecycle state.

## 7. Fail-closed behaviors required before implementation

| Case | Required disposition |
|---|---|
| Missing/unknown schema ID or unsupported major version | Reject before A0 admission; record stable reason. |
| Invalid authentication, wrong audience, unknown/revoked principal or unavailable verifier | Deny; no fallback to another identity or transport. |
| Missing capability, unknown issuer, scope expansion or unverifiable revocation state | Fail closed; no self-issued capability. |
| Expired/replayed request, digest mismatch or same idempotency key with different payload | Reject or quarantine; never silently create another canonical task. |
| Admission timeout after possible commit | Mark indeterminate; query by existing request/idempotency key before retry. |
| Cycle/missing dependency, mutable target ref without immutable SHA or input-digest mismatch | Reject/defer under accepted A0 admission semantics. |
| Cross-route duplicate dispatch | Deny unless an accepted cross-route idempotency/fencing contract proves it safe. |
| Stale claim/expired lease/old fencing generation | Reject state transition and late result. |
| Untrusted approval_state or approval without subject/action/resource/expiry/provenance binding | Treat as unapproved; require an accepted approval authority. |
| Invalid result schema, artifact digest, target SHA or verifier provenance | Quarantine; no VERIFIED, qualification, release or acceptance promotion. |
| Replayed/stale health challenge, wrong responder or unsupported contract revision | Fail readiness; retain diagnostics distinctly from successful readiness. |
| Attempt to mutate canonical product state through A0 ingress or executor result | Deny; use Product State Authority contract. |

These are proposed contract requirements, not claims of current enforcement and not authorization to run tests.

## 8. Suggested wording and schema changes for later controlled review

**Not applied by this report.**

1. Reconcile main's broad A0 authority phrases against scoped docs-branch wording, owner DEC-DEV-02 and qualification/governance contracts.
2. Update the unified ASTRA Markdown so “single coordination authority” explicitly means ASTRA-internal engineering coordination, not corporation-level mission coordination.
3. Replace permanent production-lane statements that hard-code old node identities with an owner-approved target inventory reference. Until then, target executor bindings are UNKNOWN/BLOCKED; preserve old identities as history.
4. Align the health-command document with the operational signer contract or explicitly classify it as historical. Do not consolidate signer families without source/owner decision.
5. Register new schema IDs only after schema ownership/version policy and identity/capability authority are accepted.
6. Separate admission disposition, A0 lifecycle state, attempt outcome, verifier disposition, qualification state and health/readiness values into typed fields.
7. Record historical source-pin corrections in a new evidence artifact rather than rewriting old reports. WB-05 cites an earlier schema-inventory blob; this pass pins the currently retrieved docs-branch inventory at 81d6435b2571f7c261d08b763b6fc30c4d3c6207 and the schema-set draft at e6c65c9949f45d247a2a57d1806da33737060619.

## 9. Decisions still genuinely open

- A0 ingress service principal and capability issuer.
- Authentication/cryptographic profile and key lifecycle.
- Transport choice; the logical interface remains transport-neutral.
- Durable admission/idempotency owner and commit semantics.
- Schema registry, naming/versioning and compatibility/deprecation policy.
- Clock-skew, request-expiry, health nonce TTL, revocation propagation and replay-retention policy.
- Final A0 lifecycle/status machine and cancellation race semantics.
- Approved target executor/node inventory and lane topology.
- Controlled reconciliation/branch integration strategy between main and docs branch.

These are blockers, not invitations to substitute defaults.

## 10. Verification boundary and next step

Completed:
- Refreshed main/docs refs, tree identities and comparison state.
- Read WB-14Q and the existing schema-set/route-adapter drafts.
- Compared main/docs versions of ASTRA authority and launch sources and pinned differing blob SHAs.
- Read relevant identity, capability, inference, health, command, task-ingress, gateway, authorization and evidence sources.
- Used main-only WB-14 and corporation proposal crosswalk to avoid repeating their prior source inventory.
- Created this source-pinned crosswalk without editing normative source contracts.

Not performed:
- No tests, security scan, qualification, workflow dispatch, provider/model invocation, credential access, host/runtime inspection, install, infrastructure change, deployment, migration, merge, rebase or cherry-pick.
- No code or normative schema was edited.
- No claim of ingress availability, runtime readiness, qualification or acceptance is made.

Next bounded step: **WB-14S — draft a strict schema ownership/field-mapping packet** from this crosswalk, with operation-specific request/response discriminators and explicit type separation. Present unresolved issuer, security-profile, freshness and persistence choices for owner/governance approval. Do not create or implement final JSON Schemas until these ownership and security choices are accepted.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
