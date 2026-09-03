# P0-07 — Configuration / Policy Threat Model v2

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED  
**Runtime implementation:** NOT AUTHORIZED

## 1. Threat-model scope

This threat model covers the proposed P0-07 configuration/policy boundary and its interaction with frozen P0-03–P0-06 contracts. It treats configuration and policy as untrusted declarative data until explicitly validated and authorized.

## 2. Threats and mitigations

| ID | Threat | Required mitigation |
|---|---|---|
| P07-T01 | Second canonical authority | P0-04 remains the sole canonical mutation authority. |
| P07-T02 | P0-05 bypass | All consumer reads/authorized mutations use P0-05. |
| P07-T03 | Self-granted capability | Explicit default-deny authorization; content cannot grant itself capabilities. |
| P07-T04 | Invalid configuration model | Validate identity, namespace, schema/version, ownership/scope, metadata and bounded value domain. |
| P07-T05 | Invalid policy model | Validate bounded rule structure and deterministic evaluator inputs/results. |
| P07-T06 | Config/policy authority confusion | Configuration supplies values; policy constrains/authorizes; neither silently rewrites authority. |
| P07-T07 | Arbitrary mutation surface | Use explicit operations; arbitrary patch/merge semantics are prohibited unless governed. |
| P07-T08 | Stale update | Require expected generation/state version and fail closed on mismatch. |
| P07-T09 | Hidden rebase/LWW | Explicitly prohibit hidden merge, rebase, retry-to-new-version and last-writer-wins. |
| P07-T10 | Partial publication | Validate isolated candidate before atomic publication of the selected unit. |
| P07-T11 | Oversized input | Enforce bounds for size, depth, nodes, collections, strings, identifiers, keys, numeric domain and rule count. |
| P07-T12 | Mutable aliasing | Use immutable/value-semantic results and isolated candidates. |
| P07-T13 | Executable policy injection | Policy is declarative data; arbitrary code, callbacks, shell and plugin execution are prohibited. |
| P07-T14 | Autonomous AI mutation | AI output remains inert proposal data and follows the same explicit authorization path. |
| P07-T15 | Plugin capability escalation | Plugin access is explicit, capability-scoped and default-deny. |
| P07-T16 | Secret leakage | Reject passwords, API keys, tokens, private credentials and raw secret material from canonical config/policy, errors and diagnostics. |
| P07-T17 | Credential dereference | Opaque references do not authorize dereference; external credential resolution is separately governed and denied by default. |
| P07-T18 | Unsafe deserialization | Accept only the approved bounded value domain; prohibit unsafe object reconstruction. |
| P07-T19 | Network side effect | No network operation is authorized by P0-07 architecture. |
| P07-T20 | Filesystem/subprocess side effect | No filesystem mutation, shell or subprocess operation is authorized. |
| P07-T21 | Hidden persistence | P0-07 is transient-only; prohibit database, filesystem, environment durability, caches, checkpoints and recovery copies. |
| P07-T22 | Information leakage | Errors and diagnostics are sanitized, bounded and free of secret/internal authorization material. |
| P07-T23 | Policy ambiguity | Ambiguous/unsupported policy evaluation fails closed; final precedence/conflict semantics require governance. |
| P07-T24 | Scope escalation | Tenant/project/device scope and ownership qualifiers require explicit governance approval. |

## 3. Privacy and data minimization

Configuration and policy MUST minimize personal data and retain only data necessary for the approved purpose. Durable personal-data retention is prohibited in the current transient-only phase. Secrets and raw credentials MUST NOT enter canonical state, diagnostics or error surfaces.

## 4. Authorization boundary

Authorization MUST remain explicit and default-deny. P0-07 MUST use the existing authorization context/policy boundary and P0-05 mediation. Configuration/policy content is never itself an authorization grant.

## 5. Concurrency and atomicity

Future implementation MUST test expected generation/state-version handling, stale rejection, concurrent modification, atomic publication and canonical-state preservation after failure. Hidden merge/rebase/LWW behavior is prohibited.

## 6. Bounds verification

Future implementation MUST verify every normative bound dimension: document/request/response size, nesting depth, node count, collection count, key/identifier/string lengths, numeric domain and policy rule count. Exact numerical limits require governance approval.

## 7. AI and plugin negative paths

Verification MUST prove that AI-originated proposals cannot mutate canonical state or grant capabilities and that plugins cannot bypass P0-05, create authority, escalate capabilities, execute arbitrary code or establish persistence.

## 8. Persistence and credential controls

Persistence is not authorized. Secret material and autonomous external credential dereference are denied by default. Any future persistence or credential-provider integration requires separate governance, architecture, security review and qualification.

## 9. Traceability / future evidence

The implementation test matrix MUST cover:

- authorization/default-deny;
- configuration/policy schema and identity validation;
- operation allow/deny matrix;
- resource bounds;
- immutable/value semantics;
- stale/conflict handling;
- atomic publication and failure preservation;
- sanitized errors/diagnostics;
- AI/plugin negative paths;
- secret/credential rejection;
- persistence prohibition;
- forbidden network/filesystem/subprocess/deserialization capability scans.

## 10. Residual governance risks

The following remain governance decisions rather than implementation choices:

- policy language/predicate expressiveness and lifecycle;
- tenant/project/device scope;
- exact namespaces, schemas and ownership;
- exact capability inventory and qualifiers;
- exact numerical bounds;
- policy precedence and conflict semantics;
- credential-reference semantics;
- persistence, retention, recovery, migration, backup, export and audit;
- external-provider controls;
- plugin grant lifecycle;
- break-glass administration.

Until those decisions are approved, runtime implementation MUST remain blocked.
