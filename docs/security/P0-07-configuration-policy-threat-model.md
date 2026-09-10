# P0-07 — Configuration / Policy Threat Model v2

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED; no implementation authorization

This model covers the proposed P0-07 boundary and preserves P0-03/P0-04/P0-05/P0-06. Controls are normative architecture requirements, not evidence that runtime controls exist.

## Assets and trust boundaries

Protected assets are the P0-04 canonical revision and its generation/state-version, declarative configuration/policy envelopes, scoped capability decisions, candidate isolation, sanitized diagnostics, and privacy/secret exclusions. Untrusted inputs include users, UI, plugins, AI output, proposals, serialized data, external references, ambient environment, and concurrent callers. Mandatory path: caller → explicit request/capability → P0-07 policy constraint → P0-05 → P0-04 candidate/commit.

## Threats and mitigations

| ID | Threat | Required mitigation / verification expectation |
|---|---|---|
| P07-T01 | Second configuration/policy authority or direct P0-04 mutation | P0-04 is sole canonical mutation authority; P0-05 is mandatory; scan/direct-access negative tests |
| P07-T02 | P0-05 bypass or forged transaction | opaque P0-05 transaction path and P0-04 operation authorization; reject forged/bypassed requests |
| P07-T03 | Self-granted, widened, or ambient capability | default-deny `AuthorizationPolicy`, scoped `AuthorizationContext` hand-off, no grant fields in data; absent/out-of-scope tests |
| P07-T04 | Policy allow becomes hidden authority | policy only constrains authorization; capability plus P0-05/P0-04 authorization still required; allow-without-grant test |
| P07-T05 | Executable policy/configuration or evaluator side effect | declarative value domain, fixed deterministic evaluator, no callbacks/plugins/AI code/imports; execution and side-effect scans |
| P07-T06 | Nondeterministic conflict/precedence result | explicit deny-overrides, ordered tie reporting, deny ambiguity; repeatability/conflict tests |
| P07-T07 | Stale/concurrent writer overwrites current revision | expected generation/state-version, P0-04 commit recheck, one-winner stale rejection; concurrent tests |
| P07-T08 | Implicit rebase, hidden merge, LWW, or partial publication | whole-envelope/unit operations only and atomic P0-04 commit; negative tests for patch/merge/retry/partial result |
| P07-T09 | Candidate/read alias changes canonical state | immutable/value-semantic reads and isolated candidates; mutation-after-read/candidate isolation tests |
| P07-T10 | Resource-exhaustion input or evaluator bomb | bounds before parse/evaluation/copy, bounded result/work; size/depth/node/rule/input/output boundary tests |
| P07-T11 | Unsafe deserialization/type confusion | primitive declarative domain only, schema/type validation, reject object reconstruction; hostile payload tests |
| P07-T12 | Secret/credential leakage or external dereference | default-deny secret/reference fields, sanitization, no provider/dereference path; token/password/reference negative tests |
| P07-T13 | Unauthorized durable retention | transient-only prohibition covering filesystem/database/environment/cache/checkpoint/recovery/hidden persistence; capability and filesystem scans |
| P07-T14 | Privacy overcollection or diagnostic disclosure | minimum data, no personal data by default, bounded sanitized errors; log/error/response inspection |
| P07-T15 | AI proposal mutates or executes | inert proposal only, explicit authorized human/deterministic request conversion; AI mutation/execution negative tests |
| P07-T16 | Plugin escalation or executable hook | scoped explicit capability only through P0-05; no plugin policy callbacks/direct authority; lifecycle/revocation tests after governance decision |
| P07-T17 | Network, filesystem, shell, or subprocess side effect | explicitly prohibited; prohibited-import/capability scans and negative tests |
| P07-T18 | Desired/observed state feedback silently rewrites intent | desired state is declarative; observed state is read-only input; no reconciliation mutation without an explicit future authorized operation |
| P07-T19 | Schema/version/lifecycle confusion | bounded identities, approved schemas, explicit lifecycle and unsupported-version denial; migration/version negative tests |
| P07-T20 | Error oracle reveals policy/grants/state | stable sanitized failure classes, bounded diagnostics, no raw values/internal grants; error-surface tests |

## Security invariants and verification traceability

An implementation entry gate must trace every P07-T01–P07-T20 threat to targeted tests and to P0-04/P0-05 compatibility tests. Required evidence includes authorization/capability matrices; deterministic policy and ambiguity tests; all operation/error paths; bounds at and beyond each approved limit; stale/concurrent/atomicity tests; immutable boundary tests; secret/privacy/credential-reference tests; AI/plugin negative paths; and scans for direct authority, persistence, network, filesystem, subprocess, shell, unsafe deserialization, and executable policy/configuration. Failures must preserve the prior complete canonical revision.

## Residual governance decisions

The threat model does not choose unresolved controls. Governance must decide policy expression/version lifecycle, tenant/project/device scope, exact namespace/schema/capability/scope definitions, numerical limits, permitted conflict modes, credential-reference behavior, persistence/retention/recovery, external provider control, plugin grant lifecycle, and break-glass administration. No implementation, persistence, or governance acceptance is granted by this document.
