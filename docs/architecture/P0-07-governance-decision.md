# P0-07 — Governance Decision v1.0

**Status:** ACCEPTED — IMPLEMENTATION AUTHORIZED
**Production qualification:** NOT GRANTED

## 1. Decision basis

This decision governs the P0-07 Configuration / Policy Architecture v2 and Threat Model v2 on the P0-06 frozen baseline.

Architecture/security review result: **PASSED**.

P0-04 remains the sole canonical mutation authority and P0-05 remains the mandatory consumer boundary. P0-07 introduces no alternate authority.

## 2. Approved configuration model

Configuration is bounded, declarative, non-executable data represented as a value envelope with:

- stable identity;
- namespace;
- schema/version;
- ownership/scope;
- metadata;
- value.

Approved initial scope is **device-local runtime configuration**. Tenant/project/multi-device scope is not authorized in P0-07 v1.

Configuration may supply desired-state input but does not become observed runtime state authority.

## 3. Approved policy model

Policy is bounded, declarative, non-executable data with:

- stable identity;
- namespace;
- version;
- ownership/scope;
- ordered rule collection.

P0-07 v1 approves a **minimal deterministic predicate domain only**. No arbitrary expression language, dynamic evaluation, embedded code, callbacks, plugin predicates, shell commands, network actions, or AI executable directives are permitted.

Policy evaluation is deterministic and deny-by-default.

For P0-07 v1, policy precedence is:

1. malformed/unsupported policy -> DENY;
2. explicit DENY -> DENY;
3. explicit ALLOW with no conflicting DENY -> ALLOW;
4. no matching rule -> DENY;
5. ambiguity/conflict -> DENY.

No implicit priority inheritance, merge, override, or last-writer-wins behavior is authorized.

## 4. Approved configuration/policy relationship

Configuration supplies values. Policy constrains or authorizes their use.

Policy cannot mutate configuration. Configuration cannot grant capabilities or modify authorization semantics.

The authority path remains:

```text
caller
  -> P0-07 explicit request
  -> authorization
  -> P0-05
  -> P0-04 transaction
  -> isolated candidate
  -> validation
  -> atomic commit
```

## 5. Approved operation surface

P0-07 v1 authorizes only these operations:

- `read`
- `validate`
- `propose`
- `update`
- `replace`
- `reset`
- `delete`

`update` means replacement of an explicitly identified approved value/document. Arbitrary JSON Patch, merge, deep merge, scripting, query execution, or implicit transformation is not authorized.

`propose` is inert and never publishes.

Mutation operations require an active P0-05/P0-04 transaction and expected generation/state-version preconditions.

## 6. Approved capability inventory

The following exact capabilities are approved for P0-07 v1:

```text
configuration.read
configuration.validate
configuration.propose
configuration.update
configuration.replace
configuration.reset
configuration.delete

policy.read
policy.validate
policy.propose
policy.update
policy.replace
policy.reset
policy.delete
```

No wildcard capability, capability inheritance, capability creation by configuration/policy content, or self-grant is authorized.

Capability scope is device-local and operation-specific. Any broader qualifier requires a new governance decision.

## 7. Approved resource bounds

P0-07 v1 implementation MUST enforce these maximums:

| Dimension | Maximum |
|---|---:|
| Document size | 256 KiB |
| Request size | 256 KiB |
| Response size | 256 KiB |
| Nesting depth | 8 |
| Total value nodes | 512 |
| Collection elements | 128 per collection |
| String length | 4096 bytes |
| Identifier length | 128 bytes |
| Object key length | 128 bytes |
| Object keys per object | 64 |
| Policy rules | 64 |
| Namespace/schema identifier length | 128 bytes |

Non-finite numeric values are rejected. Numeric domain is limited to finite JSON-compatible scalar numbers accepted by the implementation contract.

Bounds are hard limits. Exceeding any limit fails closed and cannot partially publish.

## 8. Approved concurrency and atomicity

A publication unit is one complete configuration or policy document.

Required publication semantics:

```text
read authoritative generation/version
-> construct isolated candidate
-> validate candidate
-> begin authorized transaction
-> verify expected generation/version
-> atomic commit
```

Stale generation/state-version mismatch MUST fail closed.

No implicit retry, rebase, merge, conflict resolution, or last-writer-wins publication is authorized.

Cross-document and cross-operation atomicity is not authorized by P0-07 v1.

## 9. Approved credential and secret boundary

The following are prohibited from canonical configuration/policy data, diagnostics and errors:

- passwords;
- API keys;
- access/refresh tokens;
- private credential material;
- raw secret material.

Opaque references are inert identifiers only and MUST NOT trigger autonomous dereference.

External credential providers and credential resolution are **NOT AUTHORIZED** in P0-07 v1.

## 10. Approved persistence boundary

P0-07 v1 is **transient-only**.

No filesystem, database, environment-backed durability, cache durability, checkpoint, recovery copy, backup/export-as-storage, or implicit restoration is authorized.

Persistence requires a separate governance decision and separate architecture/security qualification.

## 11. Approved AI and plugin boundary

AI-originated configuration/policy output remains inert proposal data.

AI cannot mutate, authorize, publish, resolve conflicts, create capabilities, or execute policy behavior.

Plugins receive only explicitly granted P0-07 capabilities. Plugins cannot escalate capabilities, create authority, bypass P0-05, execute arbitrary code, or establish persistence.

Plugin grant lifecycle is limited to explicitly configured device-local grants in P0-07 v1; dynamic self-service grant creation is prohibited.

## 12. Break-glass administration

No break-glass administrative mutation path is authorized in P0-07 v1.

Any emergency administrative path requires a separate governance/security decision with explicit authentication, authorization, audit and recovery semantics.

## 13. Error and privacy requirements

Failures MUST be bounded and sanitized.

Malformed input, unsupported schema/version, bound violation, missing capability, stale state, invalid operation, and policy ambiguity MUST fail closed.

Personal data is minimized and not durably retained by P0-07 v1.

## 14. Implementation entry gate

Implementation is authorized only for the exact decisions in this document and the accepted P0-07 v2 architecture/security artifacts.

Implementation MUST provide:

- exact schemas for the approved envelopes;
- deterministic validation;
- immutable/value-semantic API boundaries;
- exact operation/capability enforcement;
- all approved resource bounds;
- stale/conflict negative tests;
- policy deny-by-default tests;
- secret/credential rejection tests;
- AI/plugin negative-path tests;
- forbidden persistence/network/filesystem/subprocess/deserialization scans;
- full regression evidence;
- exact commit, clean tree and synchronized branch/PR evidence.

Any deviation from this decision is a governance change, not an implementation detail.

## 15. Decision

**P0-07 ARCHITECTURE: ACCEPTED.**

**P0-07 THREAT MODEL: ACCEPTED.**

**P0-07 IMPLEMENTATION: AUTHORIZED within this exact v1 scope.**

**P0-07 PRODUCTION QUALIFICATION: NOT GRANTED.**
