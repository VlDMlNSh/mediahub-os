# WB-14AA — Field/state reconciliation appendix for Jarvis → ASTRA A0 ingress

- Date: 2026-10-16
- Status: **SOURCE-BOUND PROPOSAL / NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED**
- Scope: map the proposed external request envelope and status projection to documented ASTRA-internal concepts; identify unresolved choices and their evidence/acceptance requirements.
- Authority: documentation-only. This appendix does not create a schema, register identifiers, choose a transport, amend an accepted contract, or appoint owners.

## 1. Source basis and limits

| Source | Ref / blob SHA | What it supports |
|---|---|---|
| WB-14AA ingress contract candidate | docs branch / `030273bfe9fd6d44e78b611c011af95d08c88a45` | Candidate logical envelope, operations, lifecycle distinctions and OPEN decisions |
| WB-14AB proposal-ID / decision-owner crosswalk | docs branch / `631d59a3210893012e22850af27eb69338ec377e` | Bounded ID scan; proposed role paths and minimum acceptance evidence, not actual appointments |
| WB-14AC evidence/qualification boundary crosswalk | docs branch / referenced by WB-14AD and current consolidated export | ASTRA evidence/gate rules do not define or accept the external ingress contract |
| WB-14AD governance request | docs branch / `a2367eff5ca2092fa12bda0be4cab75bf4e2ba9d` | Requested owner appointments and approval workflow; not submitted as an owner decision |
| WB-14AF lifecycle cross-route trace | docs branch / `2fe531e302679f6f16d827fd71002460658b8598` | Internal queue/claim/lease/retry/cancellation/recovery concepts and cross-route gaps |
| ASTRA governance/reference sources | main / governance blob `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`; reference architecture blob `7be5fadd3055642e7823c7233f90e978a87e5366` | Intended internal policy only; no proof of implementation conformance |
| MH-12 security architecture | main / `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Identity → authentication → trust → capability → authorization → policy → Consumer Boundary → State Authority |

The crosswalk is a proposal aid, not a substitute for the current primary contract text. ASTRA internal entity names below are semantic anchors, not asserted implementation class names or a newly prescribed storage model. No field names, enum values, schema IDs, transport bindings, TTLs, cryptographic profile, persistence mechanism or API endpoint are frozen here.

## 2. Proposed external-field → internal-concept reconciliation

| Candidate external information | Internal ASTRA concept it must correlate with | Status / mapping rule | Unresolved decision and required evidence |
|---|---|---|---|
| Contract ID and revision | Accepted internal workflow/policy contract revision | Required as provenance in the candidate; exact wire representation OPEN | Contract owner must accept canonical path, version authority, compatibility rules and reviewed SHA. |
| Request ID / correlation ID | External request identity and audit correlation; must not be conflated with mission or attempt identity | Mapping OPEN; distinct identities must remain distinguishable | A0 lifecycle owner + Jarvis API owner must accept uniqueness scope, generation/correlation rules and duplicate/reconciliation behavior. |
| Mission ID | A0-owned admitted engineering mission | External-to-internal mapping OPEN; no claim that the caller may allocate canonical A0 IDs | Accept who allocates the ID, when it becomes durable, and how an accepted request resolves to exactly one mission record. |
| Attempt ID / generation | A0 execution attempt, claim/lease generation or equivalent fencing token | Internal attempts/claims are documented; external projection OPEN | Accept monotonic generation/fencing semantics, stale-worker rejection and target/result commit preconditions. |
| Idempotency key + canonical request digest | Durable admission uniqueness and conflicting-payload detection | Candidate requirement only; key scope, canonicalization and persistence not selected | Accept atomic admission boundary, key reuse scope, digest algorithm/canonicalization, conflict response, retention and lost-ACK reconciliation. |
| Caller principal, issuer/attester, audience, delegation | MH-12 identity/trust/capability/authorization chain and applicable A0 service boundary | Identity text supplied by caller is not proof; trusted issuer/verifier path OPEN | Security/governance decision must evidence enrollment, issuer/verifier responsibilities, audience/scope, delegation, revocation/rotation, integrity and fail-closed behavior. |
| Operation, resource, scope, allowed executor class | ASTRA capability/policy checks and bounded execution authority | Semantics constrained by least privilege; external encoding OPEN | Accept allowed operation/resource model, target binding and policy revision; prove no implicit privilege expansion or silent cloud fallback. |
| Mission intent, constraints, deliverables, acceptance criteria | A0 work item / plan and its evidence/gate requirements | Candidate logical payload; no accepted field schema | A0 contract owner must define required/optional data, validation and immutable intent boundary; qualification authority must accept evidence criteria separately. |
| Target repository/project/artifact + immutable revision/SHA | Internal target binding, executor provenance and evidence target SHA | Internal target/evidence concepts documented; ingress binding OPEN | Accept permitted target types, immutable revision requirement, mismatch handling and evidence binding; no retargeting without a new accepted decision. |
| Created-at, not-before, expiry, freshness/replay context | Request freshness/replay policy | OPEN; must not reuse internal lease/heartbeat/retry values as external TTLs | Security owner must accept trusted-time assumptions, expiry/replay semantics, clock skew and domain-specific retention. |
| Capability reference / signed context | Verifiable authorization context, if chosen | Trust format and cryptographic mechanism OPEN | Accept issuer, verifier, integrity profile, key lifecycle and unavailable-verifier behavior; a label or caller string is insufficient. |
| Policy/contract revision | Revision of rules used for admission/execution | Required provenance concept; exact binding OPEN | Accept which revisions are snapshotted at admission, how later policy changes affect queued work, and what is recorded in audit/evidence. |
| Audit correlation and event timestamps | Append-only/auditable lifecycle and evidence provenance concepts | Required observability intent; exact event model OPEN | Accept event identity/order, attribution, integrity, access control and time provenance; do not imply immutable implementation without evidence. |
| Result/artifact/evidence references | A0 result publication, target-bound evidence, independent verification and gate state | Result envelope and external binding OPEN | Accept request/digest ↔ mission ↔ attempt ↔ executor ↔ target ↔ evidence/verifier correlation, provenance and incomplete-evidence behavior. |
| Cancellation request/correlation | A0-owned cancellation lifecycle and attempt/lease state | External operation proposed; internal race policy does not define wire response | Accept cancellation precedence, terminal-state races, late result disposition and explicit requested/accepted/completed/too-late/indeterminate meanings. |
| Health challenge/response, if required | A0 service identity and a separately defined liveness/readiness/authorization observation | Optional proposal operation; not equivalent to mission state or general MH-06 health | D-ING-05b must decide whether/how a challenge is required; D-ING-05a separately governs generic domain-health ↔ MH-06 mapping. |

**Invariant:** do not collapse request, mission, attempt, claim/lease generation, result, evidence, verification, qualification, release or deployment into one identifier or one status. Exact internal field names are not established by this appendix.

## 3. Candidate external status projection

The following is a semantic projection proposal, not an accepted enum or transition graph. A0 internal lifecycle remains authoritative for A0 work. External statuses should expose only a governed projection and must not become a second queue or lifecycle authority.

| Semantic stage | Candidate external meaning | Internal concept/source basis | Explicit non-implication / unresolved rule |
|---|---|---|---|
| Received / submitted | Request reached the ingress boundary | Request handling | Does not prove durable admission; exact response timing OPEN. |
| Rejected | Request failed identity, authorization, integrity, policy, target or validation checks before admission | Policy/security rejection | Must distinguish rejection from indeterminate commit; exact error taxonomy OPEN. |
| Admission indeterminate | Caller cannot yet know whether durable admission committed | Durable admission / lost-ACK reconciliation requirement | Must resolve to original disposition and must not create a second mission; persistence/commit contract OPEN. |
| Accepted | A0 durably accepted the request and established its mission correlation | A0 admission | Not execution success, verification, qualification or release. Atomic durability evidence and acknowledgment semantics OPEN. |
| Queued | Mission awaits an eligible internal claim | A0 internal queue | Queue implementation and external observation consistency are not proven by documentation. |
| Claimed / leased | A0 has assigned a bounded execution attempt/lease | Internal claim/lease/heartbeat policy | Does not mean execution completed; external generation/fencing representation OPEN. |
| Executing | An admitted attempt is reported as running | Internal attempt/executor lifecycle | Must identify observation source/time; stale observations and lost worker semantics OPEN. |
| Cancellation requested | Cancellation intent recorded/forwarded, not yet terminal | Internal cancellation/recovery | Must not be reported as cancelled until the accepted terminal condition is established. |
| Retry/recovery pending | A0 is considering/recovering work under internal policy | Bounded retry, stale-claim handling and recovery concepts | Retry count/backoff, idempotency and side-effect safety require accepted contract; no guarantee of exactly-once effects. |
| Execution succeeded / failed / cancelled / expired / indeterminate | Attempt or mission execution reached a defined terminal disposition | Internal lifecycle and result publication | Terminal vocabulary, precedence, retryable classification and immutability are OPEN; executor-reported success is not independent verification. |
| Evidence pending / complete / insufficient | Required result/evidence collection state | Evidence publication and gate state | Completeness does not mean evidence independently verified or qualification passed. |
| Verification pending / passed / failed | Independent verifier disposition, where applicable | A3 independent verification boundary | Must name verifier/provenance and target SHA; must not be inferred from executor outcome. |
| Qualification pending / passed / failed / not in scope | Separately authorized qualification outcome | Qualification process and gate | No promotion without approved criteria and revision-bound evidence. |
| Release / deployment state | Separate downstream release/deployment disposition, if in scope | Separate governance/operational gates | Not implied by mission success, evidence completeness or qualification; likely out of ingress scope unless owner accepts otherwise. |
| Health/readiness response | Point-in-time result of a defined probe | Separate service-health contract | Not a mission lifecycle status, not proof of general domain health, and not proof of authorization unless explicitly tested by accepted contract. |

Do not adopt the strings in this table as enums. A later normative contract must define allowed transitions, terminal-state rules, observation timestamps/revisions, stale-read behavior, error mapping, retryability and compatibility.

## 4. Existing internal semantics vs external decisions still OPEN

| Topic | Supported internal/documentary semantics | External decision remains OPEN |
|---|---|---|
| Queue/claim/lease | ASTRA reference/governance documents describe internal queue, claims, lease, heartbeat and stale-claim handling | Admission-to-mission mapping; external generation/fencing; stale-result response; consistency of status reads |
| Timing | Internal policy values recorded in WB-14AF: heartbeat 120 s; lease 600 s; executor timeout 900 s; result-publication timeout 120 s; retry backoff 30 s; max 3 autonomous claims | No value is an external request expiry, capability lifetime, replay window, health challenge freshness or idempotency-retention interval |
| Retry/recovery | Bounded retry and recovery are policy concepts | Attempt generation, durable checkpoint boundary, lost-worker reconciliation, retryable error classes and side-effect/idempotency contract |
| Cancellation | Cancellation/recovery are internal lifecycle concerns | Request ACK, precedence against terminal results, race semantics, late-result handling and terminal-state vocabulary |
| Result/evidence | Target SHA, provenance, immutable evidence and independent A3 verification are documented policy concepts | External envelope fields, correlation keys, verifier identity and status projection |
| Security | MH-12 chain constrains identity, trust, capabilities and authorization; ambiguity fails closed | Accepted issuer/attester/verifier, credentials/key lifecycle, transport, audience, signature/integrity profile and freshness policy |
| Health | D-ING-05a and D-ING-05b have distinct scopes | Accepted generic-health mapping and optional/required A0 challenge-response semantics |
| Authority | DEC-DEV-02 Option C: Jarvis coordinates; ASTRA A0 owns internal engineering lifecycle; Product State Authority alone owns canonical product mutation | External API and status contract acceptance; source wording drift reconciliation through change control |
| Qualification | Evidence completeness, independent verification, qualification, release and deployment are separate | Accepted qualification plan, independent acceptance authority and criteria for this exact ingress implementation |

The source docs describe intended policy. They do **not** establish that any of these behaviors are implemented, deployed, runtime-reliable or qualified.

## 5. Decision/owner/evidence register for follow-up

Owner slots below are roles to be confirmed, not appointments. No accountable individual or delegated approval authority is inferred.

| Existing decision | Unresolved issue to resolve | Accountable role to confirm | Minimum evidence before closure |
|---|---|---|---|
| D-ING-01 | Caller/service identity, issuer/attester/verifier and trust lifecycle | Security/trust-governance owner; Jarvis identity owner; A0 verifier owner | Explicit accepted trust chain, audience/scope/delegation, lifecycle/revocation, integrity and fail-closed behavior |
| D-ING-02 | Accepted caller edge and contract integrity/version governance | Jarvis API/control-plane owner + A0 ingress contract owner + security owner | Source-anchored producer→consumer path, accepted contract revision, compatibility disposition and payload/target binding |
| D-ING-03 | Durable admission, idempotency, duplicate/conflicting payload and uncertain ACK | A0 lifecycle/state owner; Jarvis ACK/API owner; persistence owner only if selected | Atomic commit boundary, key/digest scope, conflict and duplicate outcomes, lost-ACK reconciliation, recovery and retention rules |
| D-ING-04 | Freshness, expiry, replay and time assumptions | Security/trust-governance owner plus affected contract owners | Explicit trusted-time assumptions, freshness/replay/revocation rules and separately scoped retention/expiry values |
| D-ING-05a | Generic domain-health vocabulary ↔ MH-06 health semantics | MH-06/health contract owner | Accepted scope/mapping and change-control record; do not infer from A0 probe |
| D-ING-05b | Whether/how A0 challenge-response ingress health is required and what it proves | A0 service owner + security owner | Accepted challenge correlation, responder identity, freshness/replay behavior and stated limits of probe |
| D-ING-06 | External mission/attempt/cancel/result state projection | A0 lifecycle-contract owner + Jarvis mission/API owner + accepting governance authority | Accepted transition/race/fencing/retry/recovery table; explicit separation of execution, verification, qualification, release and deployment |

For each item, closure must be recorded in the canonical owner/governance register with accountable and accepting authorities, exact reviewed document revision/blob SHA, explicit disposition, compatibility/change-control record, and separately authorized verification/qualification evidence as applicable. WB-14AD is only a prepared request, not proof that the request was submitted or accepted.

WB-14AA proposal-local labels A0-ING-01…09 remain noncanonical. Do not register schema/decision IDs or freeze enums based on this appendix. D-ING-01…04, D-ING-05a, D-ING-05b and D-ING-06 remain OPEN.

## 6. Safety boundaries and explicit non-claims

- No second queue, mission registry, lease authority, result authority or product-state authority is introduced.
- Jarvis requests and coordinates; A0 owns admitted-work lifecycle; Product State Authority alone owns canonical product-state mutation.
- No implicit cloud fallback for a local-only task.
- No exactly-once side-effect guarantee is claimed.
- No runtime implementation, test, validation, qualification, deployment or acceptance is claimed.
- No provider/model calls, credentials, host/runtime inspection, installations, infrastructure changes or branch integration occurred.

## 7. Recommended next step

Wait for an explicit owner/governance disposition on WB-14AD or independently reconcile the exact primary source text for D-ING-01…04, D-ING-05a/05b and D-ING-06. If governance remains pending, keep this appendix non-normative; do not select transport, schema, enums, TTLs, persistence or crypto profile by inference.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).


## 8. Reconciliation with the existing WB-14Q–WB-14Z design series

A source-only follow-up read the existing design/decision series after this appendix was drafted. This appendix is a derivative crosswalk, not a replacement for those earlier, more detailed source-pinned artifacts. Do not re-run their analysis or treat this appendix as a newer normative authority.

| Existing artifact | Current docs-branch blob SHA | Relevant established boundary |
|---|---|---|
| WB-14Q — logical interface design | `2b0cf853a7b5eefe9e75fccdcfed130d53f417c8` | Transport-neutral logical seam; no accepted wire/API contract; no second A0 queue; direct Jarvis local route remains distinct. |
| WB-14R — authority/schema crosswalk | `dc827eb6ad53c03c0bb26a2989e4646f6f5a6b1d` | Existing schemas and command formats cannot be reused as the external A0 wire contract without resolving field/authority collisions. |
| WB-14S — schema ownership and operation map | `6b5159fdbe0c99d34e754047dd7c0a8afde8c61c` | Separate operation-specific submit/admission, status, cancel, result and health response candidates; these are not registered schema IDs. |
| WB-14T — owner/governance decision packet (corrected revision) | `023f44b6712450a8b84e2e99e716fd3cbb2d593e` | Recommendations only; no issuer, transport, persistence, freshness threshold or lifecycle enum selected. |
| WB-14U — health/readiness and lifecycle status ownership | `1cd8e23f0f534bcfdc4d4b1d060248adb7705b1f` | Admission, lifecycle, attempt, verification, qualification, health/readiness, trust and authorization are distinct status domains. |
| WB-14V — MH-06 status correction and decision split | `00cd42afedfb0c52561d967c7c40609f2a4c55fc` | MH-06 ADR-001 is accepted only within its stated scope; D-ING-05a (generic health mapping) and D-ING-05b (A0 challenge/response) remain separate; D-ING-06 lifecycle contract remains OPEN. |
| WB-14W — decision register ownership/acceptance paths | `c5920437c02d98b3f4bec6a356b590a7bef9ce4e` | Proposed roles are not appointments; named accountable owners and formal approval workflow are not evidenced in the reviewed source set. |
| WB-14Z — source-contract census | `95f3af63705f4ad7cd24405df9c7c396886cb3a3` | Existing local file task ingress and signed operational-command path are not proven to be the accepted Jarvis producer → A0 consumer contract; internal policy values do not define external TTLs. |

### Reconciliation outcome

- This appendix is consistent with the existing series when read as non-normative field/state traceability. It does not supersede WB-14Q–WB-14Z or establish an accepted contract.
- Keep D-ING-01…04, D-ING-05a, D-ING-05b and D-ING-06 OPEN. Keep WB-14AA and this appendix PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED.
- Preserve the distinction between the owner-approved DEC-DEV-02 authority split and still-open A0 wire-contract decisions. Preserve the separate Jarvis → A0 engineering route and P0-07 → P0-05 → P0-04 product-mutation route.
- No final schema, enum, transport, issuer, crypto profile, persistence mechanism, TTL or implementation choice follows from the source comparison.
- No tests, validators, qualification, provider/model calls, credentials, host/runtime inspection, installation, infrastructure change, deployment, migration or branch integration occurred.

**Next bounded step:** no further broad source-only re-analysis is justified absent new evidence. Wait for an explicit owner/governance disposition to WB-14AD. Once provided, update only the affected decision/contract records with exact source revision and acceptance evidence; until then keep this work proposal-only.
