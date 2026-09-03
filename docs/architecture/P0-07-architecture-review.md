# P0-07 — Architecture Review

**Status:** REVIEW — CHANGES REQUIRED BEFORE GOVERNANCE ACCEPTANCE
**Reviewed PR:** #15
**Base:** `implementation/p0-06-core-runtime-services`

## Executive decision

P0-07 has a sound high-level security direction, but the current proposal is not sufficiently specified to serve as an implementation-grade architecture contract. Governance acceptance should not be granted yet.

The main deficiency is not a direct security violation; it is underspecification of the canonical data model, operation surface, policy/configuration separation, validation semantics, conflict semantics, and capability model. These gaps would allow materially different implementations while all claiming conformance.

## Confirmed strengths

- P0-04 remains the sole canonical mutation authority.
- P0-05 remains the mandatory consumer boundary.
- No second state/configuration authority is introduced.
- Configuration and policy are explicitly non-executable proposals.
- Stale handling, no implicit rebase, and no last-writer-wins are preserved.
- AI proposals remain inert.
- Persistence, network, filesystem, subprocess, and unsafe deserialization remain outside scope.
- Secret leakage and mutable-alias risks are explicitly recognized.

These points are consistent with the frozen P0-06 contract, which requires service requests to delegate through P0-05 to P0-04 and forbids second authority, rebasing, arbitrary execution, network/filesystem side effects, and hidden persistence. citeP0-06-contract

## Findings

### P0-07-R01 — Missing canonical configuration model

**Severity:** BLOCKER

The proposal says configuration is bounded/versioned/declarative/value-semantic, but does not define a canonical representation: namespace, identity, schema/version field, metadata, value domain, ownership, or lifecycle.

Without this, implementation cannot establish what constitutes one configuration document, how two documents are compared, or what exactly P0-04 publishes.

**Required:** define a normative configuration envelope and field semantics before implementation authorization.

### P0-07-R02 — Missing canonical policy model

**Severity:** BLOCKER

Policy is described as deterministic rule data, but no normative policy object, rule structure, evaluation result, deny/allow precedence, default behavior, or conflict semantics is defined.

**Required:** define the minimal deterministic policy model and explicitly state whether evaluation is pure observation or an authorized runtime operation.

### P0-07-R03 — Configuration/policy separation is underspecified

**Severity:** HIGH

The proposal distinguishes configuration from policy conceptually but does not define whether policy may constrain configuration, whether configuration may select a policy, or whether policy can be embedded inside configuration.

**Required:** define directional dependency rules. Default recommendation: configuration supplies declarative values; policy supplies constraints/decisions; neither embeds executable behavior or implicitly changes the authority model.

### P0-07-R04 — Operation surface is missing

**Severity:** BLOCKER

The proposal refers to reads/mutations but does not enumerate operations. This leaves open whether implementation may introduce arbitrary patch/merge/delete/reset semantics.

**Required:** enumerate initial operations and their authorization requirements, including read, validate, propose/update, replace, and any explicit reset/delete semantics if actually needed.

### P0-07-R05 — Capability model is missing

**Severity:** HIGH

The proposal requires explicit authorization but does not define P0-07 capabilities/namespaces or their relationship to existing `AuthorizationPolicy`.

**Required:** define exact capability names, scope, default-deny behavior, and whether capability checks are delegated through P0-05 or merely reused as an implementation seam.

### P0-07-R06 — Validation and bounds are not normative

**Severity:** HIGH

"Bounded" is insufficient without required limits or a governance-controlled limits table. Exact limits can remain governance-tunable, but the architecture must define which dimensions are bounded: depth, nodes, collections, identifier length, string length, numeric domain, document size, and policy rule count.

**Required:** define a normative resource-bound dimensions table and failure behavior.

### P0-07-R07 — Conflict semantics incomplete

**Severity:** HIGH

Generation/version and stale rejection are preserved, but the proposal does not define conflict behavior for independent config/policy documents, cross-document updates, or validation-time versus commit-time conflicts.

**Required:** specify atomicity unit and conflict rules; no hidden merge/rebase/LWW.

### P0-07-R08 — Persistence exclusion is clear but future boundary is incomplete

**Severity:** MEDIUM

The proposal correctly excludes persistence, but implementation guidance should state that persistence/recovery/migration/backup is a future governance-controlled layer and must not be smuggled into P0-07 through caches, checkpoints, or environment-backed stores.

**Required:** add explicit transient-only rule for this phase.

### P0-07-R09 — Credential references need a hard boundary

**Severity:** HIGH

The proposal identifies credential-reference semantics as governance-required but does not define the current prohibition. Until separately approved, canonical config/policy should not contain secret material or dereferenceable credential handles whose resolution causes external side effects.

**Required:** make current phase default-deny for credential material and external credential dereference.

## Security decision

No direct unsafe capability is authorized by PR #15. The principal risk is implementation divergence caused by underspecification. Therefore this review recommends **CHANGES REQUIRED**, not a security waiver.

## Required next revision

Revise the architecture and threat model to add:

1. normative configuration envelope;
2. normative policy envelope/rule model;
3. config↔policy dependency rules;
4. explicit operation matrix;
5. capability namespace/scope matrix;
6. validation/resource-bounds matrix;
7. atomicity/conflict matrix;
8. transient-only/persistence boundary;
9. credential-reference default-deny boundary;
10. implementation entry-gate criteria tied to these artifacts.

No runtime implementation should begin until these are approved by governance.

## Classification

- Existing P0-03–P0-06 authority and delegation semantics: ACCEPTED / FROZEN baseline.
- P0-07 architecture: PROPOSED.
- Findings above: REVIEW findings, not historical facts.
