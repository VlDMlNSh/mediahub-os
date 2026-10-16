# MediaHub OS — Contour A WB-14S: ASTRA A0 ingress schema ownership and operation map

- Date: 2026-10-16
- Status: **STRICT CONTRACT DESIGN PACKET / NON-NORMATIVE / REGISTRATION BLOCKED / NOT IMPLEMENTED / NOT TESTED / NOT QUALIFIED**
- Ref: docs/mediahub-chat-tree-map-20261012
- Parent: WB-14Q logical ingress design and WB-14R authority/schema crosswalk.
- Scope: define a strict ownership boundary, operation-specific request/response surfaces, field authority, and typed status domains before any normative JSON Schema is authored.
- Constraint: no transport, authentication technology, capability issuer, freshness threshold, persistence mechanism or target host has been selected by this packet.

## 1. Outcome

WB-14S converts the WB-14Q / WB-14R findings into a schema ownership and operation map. Its central design rule is:

**Use separate, strict schemas for each ingress operation and each response type. Do not make one general-purpose request object that accepts task submission, status query, cancellation, result retrieval and health probing through loosely optional fields.**

The suggested family has five operation pairs:
1. Submit task → admission acknowledgement.
2. Query status → lifecycle status response.
3. Request cancellation → cancellation disposition.
4. Query result → result retrieval response.
5. Health challenge → correlated health/probe response.

These are distinct wire-contract candidates, not registered IDs or a callable API. They do not establish a current endpoint. Status values in the tables are illustrative and must be reconciled with their authoritative owner before a normative schema is created.

The schema family consumes the corporation-level mission/task/result drafts already present in the repository. It must not create a second task DAG, a second A0 queue, or a second evidence authority.

## 2. Source and ref state

| Item | Source / SHA at review | Finding |
|---|---|---|
| main HEAD and recursive tree | main / ab36db009d034db8dca723691e23b331322287e7 | Main was readable; no runtime inspection occurred. |
| documentation branch HEAD/tree | docs branch / a73073974e2a80b544f024ca47f278e20af01d41 | Used as source for this packet. |
| Branch comparison | merge base f0f406feb9f9816b009f4e6e756813541e53b9bc; docs ahead 1489 / behind 4 | Branches remain diverged; no branch integration. |
| WB-14Q ingress design | docs blob 2b0cf853a7b5eefe9e75fccdcfed130d53f417c8 | Logical ingress direction and initial envelope proposal. |
| WB-14R authority/schema crosswalk | current docs blob dc827eb6ad53c03c0bb26a2989e4646f6f5a6b1d | Concrete field collisions, command signer divergence and branch authority conflict. |
| Corporation mission/task/result schema-set draft | docs blob e6c65c9949f45d247a2a57d1806da33737060619 | Existing draft field inventory; not accepted or implemented. |
| WB-03 ingress gap packet | docs blob e2f13fe8250fedef02b27bb221072b582db1f3d1 | API, identity, capability, replay, status and result interfaces remain open. |
| WB-04 capability/trusted-context matrix | docs blob dac5e9eab9ec69ab7d15ac8eea45d7a1c8922387 | Issuer, audience, delegation, expiry/revocation and verifier lifecycle are not accepted. |
| A0 / MH-12 issuer source trace | docs blob 49ca0b69737bf8d44fe3a42daa47fd9157c9097d | Confirms source semantics but no concrete issuer, token format or A0-facing auth profile. |
| MH-12 security architecture | blob cf4ebfd5bf471ca676f075c51d3a24906504e490 | Required principal/capability semantics; cryptographic technology remains UNKNOWN pending evidence/ADR. |
| Contract metadata schema | schemas/core/contract-metadata.schema.json, blob 0e9e6b0233612c37f316fa83e7786325c992af13 | Metadata schema defines a descriptor with required/optional/constraints; it is not itself a ready-made common ingress envelope. |
| Canonical schema tree inventory | docs tree a73073974e2a80b544f024ca47f278e20af01d41 | Static recursive listing found 26 JSON schemas under schemas/. README says 25; this count drift is corrected separately in the same wave. |
| Schema validator | tools/validate_contracts.py, blob 61862cfc763e9bf239af8b19242bc11a21f08d70 | Source says Draft 2020-12, non-empty $id, all-or-nothing schema_id/schema_version/owner, and identity-separation checks. Not executed. |
| Health schema / trust schema | domain health blob 8b85c4c1dd271ca53efb0e4b50fd8654e0f2d58e; trust blob 6cf5d60a1c038f25a85328c8d5cd3040405812d0 | Health and trust are separate domains; health schema and accepted MH-06 ADR currently expose a vocabulary discrepancy. |
| Identity boundary | schemas/identity/identity-boundary.schema.json, blob 1d085bb1f2c458faaeff23bd92d83aa5d1bd3879 | Reserves separate ID slots for request, command, execution, correlation, causation, recovery and other entities; IDs are not credentials. |

Search/read scope was source-pinned to these paths and the current recursive schemas tree. It is not a claim that every repository artifact, external registry or runtime was exhaustively inventoried.

## 3. Ownership model — proposed responsibility, not an accepted owner assignment

| Contract artifact / data | Proposed accountable owner | Producer / source | Authoritative validator or state writer | Must not own |
|---|---|---|---|---|
| Corporation mission envelope | Jarvis contract owner (exact institutional owner to be confirmed) | Jarvis mission coordinator | Jarvis validates its own mission structure; A0 admission separately validates the referenced task contract | A0 queue/claim/lease state or product state |
| Immutable task DAG | Jarvis plans; exact schema owner to be approved | Jarvis builds immutable graph revision | A0 validates admissibility/dependencies before A0-owned queue admission | A second execution queue or independent lifecycle state |
| Submit request envelope | A0 ingress contract owner; assignment not yet accepted | Jarvis sends; transport adapter carries | A0 ingress authenticates caller and validates request/capability/policy before A0 admission | Issuing its own capability, trusting body-declared identity, writing A0 state outside A0 API |
| Admission acknowledgement | ASTRA A0 | A0 admission boundary | A0 is authoritative for whether admission was durably committed | Claiming execution began or that a task succeeded |
| Status query/response | ASTRA A0 status/lifecycle contract owner | Caller requests; A0 returns | A0 owns the lifecycle view and its revision | Jarvis/transport maintaining a shadow A0 state |
| Cancellation request/response | ASTRA A0 lifecycle contract owner; requester may be Jarvis | Jarvis or other authorized principal requests | A0 owns accepted cancellation transition and terminal state | Requester declaring the executor stopped without authoritative evidence |
| Result envelope | ASTRA A0 contract owner for accepted lifecycle; executor is a result producer | Executor submits an untrusted result; A0 records accepted lifecycle association | A0 validates lifecycle/fencing/publication; A3 verifies independently where required | Executor self-certification, product-state mutation or qualification promotion |
| Evidence reference | Evidence-contract owner unresolved; reuse existing evidence record only within its scope | Producer supplies evidence reference and digest | The relevant verifier/gate owner validates references and revisions | Generic status replacement, evidence mutation without a linked new record |
| Capability grant / trusted context | Explicit security/governance issuer to be named | Issuer only; no issuer is accepted today | Accepted verifier at the ingress/consumer boundary | Jarvis, A0 adapter, executor or model self-issuing authority |
| Health challenge/response | Ingress service contract owner; exact owner to be designated | Caller creates fresh challenge; ingress returns correlated response | Caller verifies identity, response correlation, freshness and allowed revision | Establishing authorization, capability, qualification or canonical state |

This table proposes responsibility boundaries only. It does not name a currently operating issuer or create a new authority by implication.

## 4. Operation-specific request / response family

### 4.1 Common structural rules

All future ingress schemas should be authored only under the canonical schemas/ tree; the contracts/ directory must not be revived as a duplicate schema source. Each schema should:
- declare JSON Schema Draft 2020-12 and a non-empty, stable top-level $id;
- include schema_id, schema_version and owner together, and require all three, consistent with the existing validator;
- use an explicit semantic version string in X.Y.Z form;
- reject unrecognized authority-bearing fields and ambiguous alternative payload shapes;
- keep identifiers separate: request_id, command_id, mission_id, dag_id, task_id, attempt_id, execution_id, correlation_id and causation_id are not interchangeable;
- carry digests/immutable revision references where relevant, while leaving canonicalization and digest algorithms to accepted governance;
- exclude raw secrets, bearer tokens, private keys, session material and provider credentials;
- identify the contract owner, lifecycle-state owner and verification owner separately where these differ.

The existing schemas/core/contract-metadata.schema.json is a schema for a metadata description object with required/optional/constraints arrays. It must not be treated as a drop-in common request envelope via a root-level $ref. Reuse the metadata conventions, not its entire root object semantics.

### 4.2 Proposed separate schemas

Candidate names and paths below are unregistered design identifiers only. No schema file is created by this report. The current inventory of 26 schema files showed no exact existing ID for the candidate names; because no authoritative global schema-ID registry was found in the reviewed sources, this is not a formal registration or collision-free guarantee.

| Logical type | Candidate schema ID | Candidate path | Required semantic contents | Authoritative result / rule |
|---|---|---|---|---|
| SubmitRequest | mediahub.astra.a0.ingress.submit-request | schemas/astra/a0/ingress-submit-request.schema.json | schema metadata; request_id; idempotency key; mission/DAG immutable references; target source SHA; payload digest; policy/capability references; correlation and bounded constraints | Caller supplies intent and references; A0 authenticates and evaluates admission. No body field proves caller identity. |
| AdmissionResponse | mediahub.astra.a0.ingress.admission-response | schemas/astra/a0/ingress-admission-response.schema.json | schema metadata; request_id/correlation_id; request digest; admission disposition; A0 request/lifecycle reference when committed; decision timestamp; stable reason code; contract/service revision | A0 is the source of truth for durable acceptance; accepted is not started/succeeded. |
| StatusQueryRequest | mediahub.astra.a0.ingress.status-query-request | schemas/astra/a0/ingress-status-query-request.schema.json | query_id; request/correlation IDs; A0 lifecycle reference and/or mission/task reference within authorized scope; optional known revision for conditional query | Read-only operation. It must not include mutable lifecycle-state fields. |
| StatusResponse | mediahub.astra.a0.ingress.status-response | schemas/astra/a0/ingress-status-response.schema.json | query_id/correlation; A0-owned lifecycle state and lifecycle revision; observation timestamp; attempt references; result/evidence references if present; stable query disposition | A0 supplies the status and revision. Exact A0 lifecycle enum remains open. |
| CancelRequest | mediahub.astra.a0.ingress.cancel-request | schemas/astra/a0/ingress-cancel-request.schema.json | cancellation_id; A0 task/lifecycle reference; reason; correlation; optional expected lifecycle revision to prevent a stale cancel | Requester asks for cancellation; A0 checks authority and current lifecycle state. |
| CancelResponse | mediahub.astra.a0.ingress.cancel-response | schemas/astra/a0/ingress-cancel-response.schema.json | cancellation_id; disposition; current A0 lifecycle reference/revision; response time; reason; correlation | Distinguish received/accepted-for-processing/already-terminal/rejected/indeterminate; acknowledgement is not proof that the worker stopped. Enum requires owner acceptance. |
| ResultQueryRequest | mediahub.astra.a0.ingress.result-query-request | schemas/astra/a0/ingress-result-query-request.schema.json | query_id; task/attempt/result reference; correlation; optional known result revision | Read-only retrieval of an authorized result/evidence reference. |
| ResultResponse | mediahub.astra.a0.ingress.result-response | schemas/astra/a0/ingress-result-response.schema.json | query disposition; mission/task/attempt IDs; target/input digests; executor and route provenance; output references and digests; execution status; separate validation/verifier dispositions; timestamps and limitations | The result producer is not the verifier. A0 publication state, task outcome, A3 verification and qualification state remain separate. |
| HealthChallengeRequest | mediahub.astra.a0.ingress.health-challenge | schemas/astra/a0/ingress-health-challenge.schema.json | caller-generated fresh challenge ID or nonce; canonical challenge digest; requested service/audience; issued/expiry times under future policy; caller correlation | Caller creates and tracks challenge. No value is selected for nonce TTL or crypto profile here. |
| HealthResponse | mediahub.astra.a0.ingress.health-response | schemas/astra/a0/ingress-health-response.schema.json | challenge ID and digest echoed; authenticated responder identity from verifier context; observed/responded timestamps; contract/source revision; probe outcome; response integrity evidence according to accepted security profile | Caller checks challenge match, identity, freshness and allowed revision. Health never grants authorization or proves qualification. |

The exact path/id naming pattern is a candidate convention, not an approved registry. Before schema files are created, a registry owner must approve the namespace, ensure no historic ID collision, set compatibility/deprecation policy, and define generation/validation evidence.

### 4.3 Why distinct response schemas are necessary

A status query is not a task result; cancellation acknowledgement is not terminal cancellation; admission disposition is not lifecycle state; a health probe is not a qualification record. A strict discriminator on every operation and a separate response schema prevent a permissive union from making those state domains interchangeable.

A transport may wrap any of these typed bodies in a common framing protocol. That framing layer must not replace, rename or blur the operation-specific contract fields.

## 5. Field authority and mutability map

| Field group | Submitted by | Trusted source / validator | Mutability rule |
|---|---|---|---|
| request_id, idempotency key, correlation_id | Jarvis/caller | Ingress validates syntax, scope and prior record | Immutable after first receipt; same idempotency key with different canonical digest is a conflict. |
| authenticated principal / audience | Established by accepted authentication boundary, not user body | A0 ingress verifier using accepted identity lifecycle | Caller body cannot override it. |
| capability reference | Caller references a grant | Named issuer/verifier and A0 policy boundary; both remain unresolved | Opaque reference only; no caller-created grant and no scope expansion. |
| mission_id, DAG reference/revision | Jarvis | Mission/DAG contract owner and A0 admission validation | Immutable per submitted revision; new graph revision creates a new reference. |
| target repository/ref/SHA and inputs digest | Jarvis proposes | A0 checks accepted target/source policy and exact immutable SHA binding | Ref name cannot replace SHA; any change requires a new immutable task revision/request digest. |
| requested route and executor constraints | Jarvis proposes | Explicit policy decision owner; A0 verifies route eligibility for A0 route | Requested route is not permission; no implicit fallback or cross-route duplicate dispatch. |
| data classification / egress / allowed actions / owned paths | Caller references policy-bound constraints | Accepted policy engine and executor isolation mechanism | Request cannot broaden policy. Unknown classification/egress fails closed. |
| admission disposition and A0 reference | Not caller-supplied | ASTRA A0 | Only A0 may authoritatively claim durable admission. |
| A0 lifecycle state, lifecycle revision, claim/lease/fencing | Not caller-supplied | ASTRA A0 lifecycle store/controller | Caller, transport and executor cannot directly mutate. Fencing primitive still needs an accepted contract. |
| attempt status, outputs and artifact digests | Executor proposes | A0 validates publication; independent verifier checks result where required | Immutable attempt submission; correction is a linked new record, not silent overwrite. |
| verifier disposition | Independent verifier | A3 or separately accepted verifier authority | Cannot be self-written by producing executor. |
| qualification/gate/release/deployment/product acceptance | Existing authoritative governance owner | ASTRA gate/human release and Product State Authority as applicable | Never inferred from result status or health response. |
| health probe observation | Ingress service emits; caller verifies | Accepted health/identity contract | Observation-only; no task/control state mutation. |
| issuer, grant, revocation status | Accepted issuer/governance system | Verifier checks trust, scope and current status | No issuer chosen by this design; cannot trust caller-supplied text. |

## 6. Status-domain partition

No generic top-level status enum should span all the following domains.

| Domain | Owner | Meaning | Existing/source vocabulary status |
|---|---|---|---|
| Admission disposition | A0 ingress | Whether this submission was durably admitted, rejected, deferred, duplicate or indeterminate | WB-14Q proposal only; not accepted. |
| A0 lifecycle state | ASTRA A0 | Queue, dependency, claim, lease, execution, retry, cancellation, recovery and terminal workflow state | Existing ASTRA semantics and governance exist, but A0-facing wire enum/state transition contract remains open. |
| Attempt outcome | Execution attempt producer proposes; A0 records validated association | Whether one attempt completed, failed, timed out, blocked, was partial or cancelled | Candidate statuses in schema-set draft/WB-14Q are non-normative and differ. |
| Result validation / verifier disposition | A0 publication boundary and independent A3/verifier | Whether result schema/provenance/target/digests and acceptance criteria were verified | Must be independent from worker outcome; exact contract enum remains open. |
| ASTRA qualification gate | ASTRA GOLD qualification schema and governance | Gate-by-gate qualification and release evidence | Governed by ASTRA GOLD qualification contracts; task success cannot set gate PASS. |
| Health condition | MH-06/health contract owner; reconciliation needed against domain schema | Observed condition of service/entity | MH-06 ADR uses UNKNOWN/HEALTHY/DEGRADED/FAILED/QUARANTINED; schemas/domain/health.schema.json instead uses HEALTHY/DEGRADED/WARNING/FAILED/UNKNOWN. This is a source vocabulary conflict, not resolved here. |
| Operation readiness | MH-06 semantic contract owner | Readiness for a specific operation | MH-06 ADR uses UNKNOWN/NOT_READY/READY/DEGRADED/QUARANTINED. Not interchangeable with health, trust or authorization. |
| Trust state | Trust/security contract owner | Current trust disposition | Domain trust schema uses TRUSTED/PENDING/UNTRUSTED/BLOCKED; not synonymous with health/readiness. |
| Authorization decision | Accepted policy/authorization owner | Allow/deny for principal, capability, operation, target and context | No implicit allow; an authenticated identity or healthy service does not grant permission. |
| Canonical product state | MediaHub Product State Authority | Product facts/state mutation | Never owned by Jarvis, A0 ingress, transport, executor, provider or health subsystem by implication. |

Required fix before schema finalization: reconcile the MH-06 ADR health vocabulary with the domain health schema under their owners. Do not silently force the new ingress health response to choose one enum on behalf of the owner. The ingress probe should have a narrow probe outcome plus explicit references/fields for health and readiness where applicable.

## 7. Security and temporal fields that must remain undecided

The following fields are semantic requirements, not a selection of a security technology.

| Topic | Needed contract decision | What this packet deliberately does not choose |
|---|---|---|
| Service principal | Named Jarvis caller and A0 receiver principals, enrollment owner, audience and lifecycle | Principal IDs and enrollment mechanism. |
| Capability issuer | Issuer authority, grant basis, subject/action/resource/scope/constraints/provenance, delegation and attenuation | Issuer identity or token format. |
| Authentication | Evidence accepted by A0 and authenticated context passed to policy checks | HMAC vs signed token vs OAuth/OIDC/mTLS/PKI or other mechanism. |
| Key lifecycle | Trust anchor, custody, rotation, revocation, compromise response and offline behavior | Any key store/library/provider. |
| Freshness | Request age, clock skew, expiry semantics, nonce TTL, revocation freshness and deduplication retention | Numeric thresholds. The ASTRA 86400-second evidence freshness window is not a health nonce TTL. |
| Replay/idempotency | Key scope, canonical digest, durable admission record, same-key/same-payload behavior, conflict behavior, uncertain commit recovery | “Exactly once” execution or side effects. |
| Persistence authority | Single authoritative owner/store and transactional commit point for accepted admission and deduplication record | Database/broker/storage mechanism. No second shadow A0 queue is permitted. |
| Cancellation/revocation during work | When capability is rechecked, how an active job is cancelled/contained, and how late results are fenced | Automatic stop guarantees or race outcomes not yet accepted. |
| Audit | Stable correlation, identity/policy/revision/result references, redaction, access and retention | Event bus/storage mechanism or secret-bearing log payload. |
| Transport | Framing, endpoint discovery, channel authentication, retry behavior and compatibility | GitHub, HTTP, IPC, broker, or any specific topology. |

The issuer source trace and WB-04 lifecycle matrix already establish these are real open contract gaps. WB-14S preserves them rather than replacing them with defaults.

## 8. Registry and schema-tree guardrails

- Canonical JSON schemas live in schemas/. Do not reintroduce duplicate JSON schema files under contracts/.
- Existing validator source requires Draft 2020-12, a non-empty top-level $id, and either all three metadata keys (schema_id/schema_version/owner) or none; the version must be X.Y.Z if constrained.
- The existing metadata descriptor at schemas/core/contract-metadata.schema.json describes required/optional/constraints for a contract. It is not itself the reusable payload envelope definition.
- The 26-file static inventory is source inspection, not schema validation. Validator and test code were read only; no test/validation command was executed.
- Candidate schema IDs above do not exactly match observed existing schema IDs in the reviewed 26-file inventory. No authoritative central ID registry was found in the reviewed paths, so IDs remain provisional and require governed collision registration before use.
- Keep component/gate evidence records as evidence references when that scope fits. Do not overload a component qualification schema into a task result, capability token, request envelope or health response.
- New schema IDs, paths, ownership and semantic versions must be admitted through controlled source change; this design does not authorize schema implementation.

## 9. Failure cases attached to the schema contract

| Condition | Expected contract behavior |
|---|---|
| Operation type unknown or payload schema doesn't match operation | Reject before A0 admission. |
| Extra authority-bearing fields or ambiguous payload union | Reject rather than ignore. |
| Caller-supplied principal differs from authenticated context | Ignore/untrust the body value and deny if identity binding cannot be established. |
| Issuer or capability verifier unknown/unavailable | Fail closed; keep issuer decision open. |
| Capability expired/revoked/out-of-scope or wrong audience | Deny and audit stable reason. |
| Same idempotency key with different digest | Reject conflict; do not create second canonical request. |
| Commit result uncertain | Return indeterminate disposition and require query by existing ID/key before retry. |
| Status query contains a mutation request, or cancel contains an untrusted “approved” boolean | Reject schema or authorization check; operation payloads remain distinct. |
| A0 response claims admission without authoritative lifecycle reference/commit point | Do not treat it as accepted. |
| Cancellation acknowledgement treated as terminal cancellation | Reject that semantic transition; query A0 lifecycle. |
| Stale claim/fencing generation or late result | A0 rejects transition/publication under an accepted fencing contract; exact primitive remains OPEN. |
| Result producer claims its own independent verification or qualification | Treat as untrusted claim; independent authority must supply disposition. |
| Health is used as authentication or authorization | Deny that inference; health is observational only. |
| Health/readiness/trust vocabularies are mixed | Schema-level conflict; block normative schema finalization until owner mapping is accepted. |
| Legacy node ID or old HMAC key map appears as target identity | Do not infer target admission. Keep old transport as history until explicitly reconciled. |

These are requirements, not assertions about current runtime enforcement and not authorization to execute tests.

## 10. Proposed sequencing and unresolved decisions

### Before normative schema files
1. Governance names the accountable schema owner/registry process and verifies ID namespace/collision policy.
2. The owner/governance process decides the A0 service principal and capability issuer lifecycle, including delegation, expiry, revocation and verification semantics.
3. Security governance accepts the authentication/crypto profile or accepts a transport-authenticated context design, and specifies the caller-verifier trust boundary.
4. A0 lifecycle owner specifies the authoritative admission commit point, durable idempotency/deduplication scope, status query consistency, cancellation races, fencing and late-result handling.
5. MH-06/domain owners reconcile health/readiness vocabulary before the health response is finalized.
6. A controlled change reconciles A0 authority wording and old permanent-node topology across branches; branch divergence remains a separate integration blocker.
7. The schema author creates separate Draft 2020-12 JSON Schemas under schemas/ only after these decisions, with one strict request/response schema per operation and source crosswalks in metadata/description.

### Owner/governance decisions still open
- Exact ingress/registry/schema owner and naming/version policy.
- Jarvis/A0 service principals and enrollment authority.
- Capability issuer and delegation/revocation lifecycle.
- Authentication/cryptographic profile and key lifecycle.
- Transport and endpoint, including channel/auth boundary.
- Request, health challenge and revocation freshness policies.
- Persistence/idempotency authority and commit semantics.
- A0 lifecycle/status/cancellation/fencing state machine.
- Health/readiness mapping between MH-06 and the domain health schema.
- Target node/executor inventory and branch-integration strategy.

No choice in this list was made by inference.

## 11. Verification and bounded next step

Source-only checks completed:
- Refreshed current refs/tree and branch compare.
- Read WB-14Q, WB-14R, schema-set draft, WB-03, WB-04 and the MH-12 capability issuer source trace.
- Reviewed all 26 JSON files currently present in the canonical schemas/ tree at path/SHA level and inspected the relevant identity/capability/metadata/health schemas.
- Read the schema validator and README as source; no command was executed.
- Defined proposed owners, operation-separated schema names/paths, field authority/mutability and distinct status domains.
- No implementation, testing, qualification, provider/model calls, credentials, host/runtime inspection, installation, infrastructure work, deployment, migration or branch integration occurred.

Next bounded step: **WB-14T — prepare a decision packet with options and consequences for service principal/capability issuer, authentication profile, durable admission/idempotency authority, freshness policy and health vocabulary reconciliation.** Do not create final JSON Schema files or select transport until these governance blockers are resolved.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
