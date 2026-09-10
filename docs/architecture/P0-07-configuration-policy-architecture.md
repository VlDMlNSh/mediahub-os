# P0-07 — Configuration / Policy Architecture v2

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED; **no runtime implementation authorized**
**Baseline:** `d9b5c9db128d8ec75dae6fbd03b5d54950bdddf5`

The key words **MUST**, **MUST NOT**, **REQUIRED**, and **MAY** are normative. This proposal defines data and boundary contracts only. It neither changes frozen P0-03/P0-04/P0-05/P0-06 contracts nor grants acceptance.

## 1. Scope

P0-07 specifies bounded declarative configuration and policy records, their authorization and operation surface, and their placement in the existing State Authority path. It is transient-only. A later approved implementation may add these records to the P0-04 canonical payload only through P0-05; this document does not itself add a store, schema, API, evaluator, or runtime service.

## 2. Non-goals

P0-07 does not authorize persistence; filesystem, database, environment, cache, checkpoint, recovery, backup, export, or hidden local storage; network calls; subprocess/shell execution; unsafe deserialization; installer/update/recovery work; arbitrary JSON Patch or merge; executable rules, callbacks, plugins, or AI code; secret storage or credential dereferencing. It does not choose tenancy, project, device, retention, break-glass, external-provider, or plugin-grant lifecycle policy.

## 3. Configuration model

A **configuration envelope** is an immutable, declarative record containing: `identity`, `namespace`, `schema_version`, `metadata`, and `value`. Identity is the tuple `(namespace, identifier)`; `identifier` is a bounded, canonical, schema-valid string and MUST be unique within its namespace. Namespace identifies the governed configuration family; it is not a filesystem path, URL, capability, or executable name. Exact namespace grammar and schemas remain governance-controlled.

`schema_version` selects the approved declarative schema and is independently compatible with the P0-04 generation/schema gate. `metadata` is bounded, non-secret descriptive data (including declared owner and lifecycle status), never an authority grant. `value` is a bounded value-domain tree of null, booleans, finite numbers, strings, arrays, and maps with string keys only. It MUST NOT contain object instances, functions, bytecode, references with dereference behavior, commands, templates with evaluation semantics, or serialized executable objects.

The declared owner is the accountable domain owner, not the State Authority: P0-04 owns canonical mutation and version sequencing. Lifecycle is `proposed`, `active`, `superseded`, or `retired`; only an approved schema may define allowed transitions. The **authoritative representation** is one immutable P0-04 canonical revision containing accepted envelopes and authority-owned generation/state-version metadata. Copies, requests, candidates, diagnostics, UI models, and caches are non-authoritative.

Configuration expresses **desired state** only. Observed state is runtime fact obtained through the applicable P0-05/P0-06 read boundary; it MUST NOT silently rewrite configuration. A controller may compare desired and observed state only through an explicit authorized operation defined by a later approved contract. No comparison, reconciliation, or read has mutation authority.

## 4. Policy model

A **policy envelope** is immutable declarative data containing `identity`, `policy_version`, `namespace`, `metadata`, `precedence`, and ordered `rules`. Identity is `(namespace, identifier, policy_version)`; replacement creates a new policy version rather than mutating historical meaning. A rule contains a bounded rule identifier, declarative match predicates over an explicitly named evaluation-input field set, and one terminal effect: `allow` or `deny`. Rules contain no executable expression, callback, plugin, script, dynamic import, network reference, or AI-generated executable logic.

The evaluation input MUST be a bounded, canonical value snapshot containing only the requesting principal, requested P0-07 operation, requested resource identity/scope, declared capability, relevant envelope metadata, and explicitly approved non-secret contextual attributes. It MUST NOT contain mutable objects, raw credentials, ambient process/environment state, or unconstrained observed state. The evaluator returns an immutable result: `allow` or `deny`, matched rule identifiers (if safe to disclose internally), policy identities/versions, and a sanitized reason code.

Evaluation is deterministic: same accepted policy set, input, ordering, and versions MUST yield the same result; evaluation MUST have no side effects. Default is **deny**. A matching deny overrides matching allow. If several rules of the same effect match, the ordered tuple `(precedence, policy identity, policy version, rule identifier)` resolves reporting order but not the effect. Duplicate precedence/identity ambiguity, invalid ordering, unsupported schema, or an unresolvable conflict MUST deny; it MUST NOT choose a winner implicitly. Governance must ratify the permitted predicate language and whether additional conflict modes are ever allowed.

P0-07 policy is an authorization constraint layer and is distinct from the existing runtime `AuthorizationPolicy`, which remains the explicit allow-list decision seam for `AuthorizationContext`. P0-07 MUST NOT replace, modify, or bypass it.

## 5. Configuration / policy separation

Configuration may influence only declared desired values and the resource attributes made available to validation or policy evaluation. Policy may constrain whether a requested operation on a configuration/policy resource is authorized, and may constrain admissible values through declared, deterministic validation predicates. Policy MUST NOT implicitly mutate configuration, observed state, grants, ownership, lifecycle, versions, or the evaluation input. It MUST NOT modify configuration values; a denied value remains unchanged and an allowed value is published only by its explicit requested operation.

Authorization is conjunctive and ordered: valid request and capability check → P0-07 policy evaluation → P0-05 request/transaction authorization → P0-04 validation/freshness/integrity → commit. A policy allow is not a capability grant, transaction, commit permission, or authority transition. A policy deny fails closed. No layer may turn policy data, a policy result, or a configuration value into hidden authority.

## 6. Authority model

P0-04 remains the sole canonical mutation authority and owns canonical generation/state-version sequencing, candidate isolation, validation gate, and atomic publication. P0-05 remains the mandatory consumer/integration boundary; callers, P0-06 services, UI, plugins, AI, diagnostics, and external input MUST NOT directly mutate P0-04 or bypass P0-05. P0-07 owns neither a second state store nor a local policy/configuration authority. Read results are immutable/value-semantic; request payloads and candidates are non-authoritative until P0-04 commit.

## 7. Operation model

All mutation operations are explicit whole-envelope operations. They accept a bounded request, `AuthorizationContext`, capability, resource identity, and expected generation/state-version. `validate` is non-mutating; `propose` creates inert proposal data only. No operation accepts JSON Patch, Merge Patch, partial merge, or a caller-selected resulting version.

| Operation | Input / output | Capability | Mutation and canonical authority | Transaction / failure |
|---|---|---|---|---|
| `read` | identity/scope → immutable envelope or absence | `config.policy.read` | none; P0-04 read via P0-05 | no transaction; deny/not-found/invalid input is sanitized and publishes nothing |
| `validate` | proposed whole envelope → bounded validation result | `config.policy.validate` | none | no transaction; invalid/policy-denied result publishes nothing |
| `propose` | whole envelope plus intent → inert proposal identity/data | `config.policy.propose` | no canonical mutation | no transaction; proposal is not approval, grant, or commit |
| `update` | existing identity, complete replacement value/envelope, expected version → new revision | `config.policy.update` | replaces only the named complete resource through P0-04 | REQUIRED; absent/stale/malformed/denied fails closed |
| `replace` | complete bounded namespace set, expected version → new revision | `config.policy.replace` | replaces that declared namespace publication unit only through P0-04 | REQUIRED; no omitted-resource merge; any failure publishes none |
| `reset` | identity, schema-defined approved default selector, expected version → new revision | `config.policy.reset` | explicit replacement with schema-approved default, never ambient/environment value | REQUIRED; missing default/denial/stale fails closed |
| `delete` | identity, expected version → absence/new revision | `config.policy.delete` | removes only explicitly named eligible resource through P0-04 | REQUIRED; protected/in-use/denied/stale/not-found fails closed |

`update` and `replace` are intentionally distinct: update has a single-resource publication unit; replace has a complete namespace-set publication unit. Neither infers omitted fields or resources. Exact eligibility rules, default selectors, and policy-resource operation variants require governance approval before implementation.

## 8. Capability / authorization model

The P0-07 capability namespace is exactly `config.policy.<operation>` for the seven operation names in Section 7. A capability scope MUST bind at least principal, capability string, resource class (`configuration` or `policy`), namespace, and identity selector; unscoped/wildcard scope is denied unless a future governance decision defines it. `read`, `validate`, and `propose` require their listed capabilities; each mutation requires its own listed capability. Missing, malformed, expired, out-of-scope, or unrecognized capability means default-deny and a sanitized `authorization_denied` result.

Capability ownership remains the existing authorization authority. The existing `AuthorizationContext(principal, capability)` carries the caller-declared principal/capability into P0-05; it is not self-authenticating and does not itself confer a grant. The existing `AuthorizationPolicy` remains the explicit default-deny allow-list that decides operation grants. P0-07 policy is additionally constraining, never grant-creating. P0-05 must perform the hand-off and P0-04 must revalidate its operation-sensitive authorization at commit. No configuration, policy, plugin, AI proposal, caller request, or metadata field may self-grant, delegate, widen, or mint a capability.

## 9. Validation and bounds

Validation occurs before expensive processing and again before commit. Every dimension below MUST have an enforced limit; a value marked governance-controlled has no implementation default until ratified. Limits apply independently to request, candidate, canonical result, policy input, response, diagnostics, and nested data as applicable.

| Dimension | Normative enforcement |
|---|---|
| Document/request/response size | bounded byte size before parse, and bounded serialized output; exact limits governance-controlled |
| Nesting depth; node count | bounded structural traversal before evaluation/copy/publication |
| Collection sizes | bounded maps, arrays, namespace resources, and metadata entries |
| Identifier and namespace length | bounded canonical strings and approved grammar |
| String/key length | bounded Unicode/string representation; no unbounded normalization work |
| Numeric domain | finite, schema-approved integer/decimal ranges; NaN/infinity and implementation-dependent coercion denied |
| Policy rule count | bounded per policy and per evaluated policy set |
| Policy evaluation input/result | bounded fields, result size, matched-rule list, and work budget |

Validation MUST reject unknown/unsupported schema or version, duplicate identity, invalid lifecycle/ownership, malformed type, unsafe deserialization, prohibited secret/credential field, unsupported policy construct, and any bound breach. Validators MUST be deterministic and side-effect free.

## 10. Atomicity and concurrency

The publication unit is exactly one complete resource for `update`, one complete declared namespace set for `replace`, one resource deletion, or one schema-defined reset; it is never an individual field or rule. Validation phase constructs an isolated candidate and performs schema, bounds, secret, policy, authorization, generation/version, and P0-04 integrity checks. Commit phase rechecks authorization and expected generation/state-version, then P0-04 atomically publishes the complete unit and advances its authority-owned version.

Every mutation MUST supply the expected observed generation and state version. Absent, incompatible, or stale preconditions reject the operation without publication. Concurrent writers serialize only at P0-04 commit: at most one matching candidate may publish; the other becomes stale and fails closed. Implicit rebase, last-writer-wins, hidden merge, retry-as-success, partial publication, and mutation of a read result are prohibited. Any failure preserves the prior complete canonical revision and does not advance its version.

## 11. Error semantics

Stable outward classes are `invalid_request`, `authorization_denied`, `policy_denied`, `not_found`, `validation_failed`, `bounds_exceeded`, `unsupported_schema`, `stale_generation`, `stale_version`, `conflict`, and `operation_rejected`. They MUST be bounded and sanitized: no secret, raw configuration/policy value, authorization grant detail, filesystem path, network detail, stack trace, or internal evaluator state. Ambiguity and internal failure fail closed as `operation_rejected` unless a safe stable class applies.

## 12. Privacy / data minimization

Only data necessary for declared desired state, policy decision, and bounded diagnostics may enter P0-07. Personal data is disallowed by default unless a later schema/data-classification decision explicitly permits the minimum required field. Logs, errors, proposals, and responses MUST minimize and sanitize data. P0-07 creates no durable retention, audit, export, deletion, or recovery mechanism.

## 13. Persistence boundary

**P0-07 is transient-only until persistence receives separate governance authorization.** Canonical configuration/policy and all supporting proposals, caches, indexes, validation artifacts, diagnostics, recovery copies, checkpoints, and snapshots MUST NOT be made durable. Filesystem-backed configuration, databases, environment-backed durable state, cache-based durability, checkpoints, durable recovery copies, and hidden local persistence are prohibited. P0-04's accepted in-memory scope is preserved; this proposal does not invoke its snapshot/restore facilities as a P0-07 persistence mechanism.

## 14. Credential boundary

Default deny applies to passwords, API keys, tokens, private credentials, secret material, opaque credential references, and external credential dereferencing. Canonical configuration/policy, metadata, proposals, errors, diagnostics, and responses MUST NOT contain them. P0-07 MUST NOT autonomously resolve, fetch, validate, or dereference an external credential reference. A separately governed credential-reference contract is required before any representation, authorization, provider control, retention, or dereference behavior exists.

## 15. Interactions with P0-03 / P0-04 / P0-05 / P0-06

P0-03 supplies transaction, generation/version, isolation, integrity, and failure-preservation semantics. P0-04 is frozen and remains the single in-memory canonical mutation authority; P0-07 cannot change its contract. P0-05 is the mandatory consumer path and preserves opaque transactions, authorization hand-off, sanitized errors, and no bypass. P0-06 services may request P0-07 operations only through P0-05 and acquire neither local configuration/policy authority nor side effects. P0-07 does not alter P0-06's frozen/accepted scope.

## 16. AI boundary

AI output is untrusted inert proposal data. It cannot execute, evaluate policy, select a version, issue a capability, authorize, mutate, commit, trigger reconciliation, or cause network/filesystem/subprocess activity. A human or separately authorized deterministic actor must transform a validated proposal into a normal explicit request; the complete authorization and transaction path still applies.

## 17. Plugin boundary

Plugins are untrusted consumers. They have no direct P0-04 access, no unrestricted mutation, no executable policy hook, and no authority to grant/delegate capabilities. A plugin may use only an explicitly issued, scoped P0-07 capability through P0-05; absent or lifecycle-invalid grants deny. Plugin grant lifecycle, scope delegation, and revocation semantics remain governance-required.

## 18. Security invariants

1. One canonical mutation authority (P0-04) and one consumer path (P0-05).
2. Declarative bounded data only; no arbitrary executable configuration or policy.
3. Default-deny, explicit, scoped, non-self-granting authorization.
4. Deterministic, side-effect-free policy evaluation; deny on ambiguity.
5. Complete-unit atomic publication with generation/version freshness and failure preservation.
6. No persistence, external side effect, unsafe deserialization, secret material, or credential dereference.
7. AI and plugins remain non-authoritative and capability-bounded.

## 19. Governance-required decisions

Governance must approve policy-language expressiveness and version lifecycle; tenant/project/device scope; exact namespaces, schemas, identifier grammar, capability set and scope rules; exact numerical bounds; any permitted conflict semantics; credential-reference semantics; persistence/retention/recovery; external-provider control; plugin grant lifecycle; break-glass administration; protected-resource/delete/reset rules; and implementation/test acceptance evidence. Until then, no unresolved option is silently selected.

## 20. Implementation entry gate

Implementation requires a new governance authorization after the decisions above, an approved schema and capability mapping, threat-to-test traceability, negative tests for every invariant, exact-limit tests, P0-04/P0-05 compatibility evidence, and prohibited-capability scans. This document alone authorizes no code, test, schema, persistence, workflow, installer, recovery, update, or network work.

## 21. Acceptance criteria

- [ ] Governance has ratified all Section 19 decisions and this v2 contract.
- [ ] Configuration and policy envelopes, value domains, identities, lifecycle, and desired/observed-state distinction are schema-defined.
- [ ] Capability scopes and P0-05/P0-04 authorization hand-off are approved and traceable.
- [ ] Every Section 7 operation has request, authorization, validation, transaction, and sanitized failure tests.
- [ ] Bounds, atomicity, stale/concurrent rejection, no merge/rebase/LWW, privacy, secret, AI, plugin, persistence, and side-effect negative paths are verified.
- [ ] Governance separately authorizes any implementation; no acceptance is implied here.
