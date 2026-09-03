# P0-07 — Configuration / Policy Threat Model

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

## Threats and controls

1. Second canonical store — configuration/policy authority remains in P0-04.
2. P0-05 bypass — consumer access must use P0-05.
3. Self-granted capability — authorization remains explicit and default-deny.
4. Stale update — expected generation/version and fail-closed stale handling.
5. Implicit rebase / last-writer-wins — prohibited.
6. Executable policy — prohibited pending governance approval.
7. Autonomous AI mutation — prohibited; AI proposals remain inert data.
8. Plugin escalation — capability scope must remain explicit and bounded.
9. Secret leakage — secrets excluded from canonical config/policy, errors, and diagnostics.
10. Oversized input — bounded depth, nodes, strings, keys, and collections are required; exact limits require governance approval.
11. Unsafe deserialization — unsafe object reconstruction is prohibited.
12. External side effects — network, filesystem, subprocess, and shell execution are prohibited.
13. Durable retention — persistence, recovery, backup, migration, export, and audit retention require separate governance approval.
14. Mutable aliases — implementation must use immutable/value-semantic results and isolated candidates.
15. Information leakage — failures and diagnostics must be sanitized and bounded.

## Privacy constraints

Configuration/policy architecture must minimize personal data, avoid durable personal-data retention by default, and prevent secrets or raw credentials from entering canonical state, diagnostics, or errors.

## Forbidden capabilities

No second authority, P0-05 bypass, direct P0-04 mutation, self-grant, implicit rebase, last-writer-wins, autonomous AI mutation, unrestricted plugin mutation, network side effects, filesystem mutation, subprocess/shell execution, durable persistence, unsafe deserialization, or secret leakage.

## Verification and traceability

Future implementation must provide a test matrix covering authorization, bounds, immutability/value semantics, stale/conflict handling, atomic publication, sanitization, AI/plugin negative paths, and forbidden-capability scans. Exact resource sub-limits, policy evaluator semantics, namespaces, schemas, operations, and capabilities require governance approval before implementation.

## Governance-required decisions

Policy language expressiveness/version lifecycle, scope, credential-reference boundary, persistence/recovery/migration/backup, retention/export/audit, external-provider control, plugin grant lifecycle, break-glass administration, exact bounds and conflict semantics remain unresolved.
