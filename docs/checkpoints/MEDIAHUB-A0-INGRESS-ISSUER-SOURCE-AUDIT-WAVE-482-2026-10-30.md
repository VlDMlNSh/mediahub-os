# Wave 482 — A0 task-ingress issuer and approval-provenance source audit (2026-10-30)

## Status

**SOURCE AUDIT COMPLETE / ISSUER EDGE NOT ESTABLISHED / RUNTIME CHANGE BLOCKED BY ISSUE #301.**

This is a bounded read-only source audit of the current main implementation. It does not change runtime behavior, execute tasks, access credentials, inspect a live host, call a provider, or authorize workflow dispatch.

## Immutable target and source pins

- Repository: VlDMlNSh/mediahub-os
- Main target SHA observed from repository commit search: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7.
- Canonical documentation branch: docs/mediahub-chat-tree-map-20261012.
- `runtime/mediahub_runtime/task_ingress.py` blob: `59e1254aa61cc8f55f53bd1e179631e81c441393`.
- `runtime/mediahub_runtime/astra_gateway.py` blob: `10985e4ad8f682313d08e7492ecc1856a8bce20f`.
- `runtime/mediahub_runtime/authorization.py` blob: `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`.
- `runtime/mediahub_runtime/autonomous_queue.py` blob: `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`.
- `ops/control/sign_command.py` blob: `fc6943a79cefdf06e59d6e32771d2df551b2f0e9`.
- `astra_github_agent.py` blob: `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`.
- Prior source reconciliation: WB-14 report at main blob `048376919db64de57e96e3ca56207eaf8a82f295`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN and orders A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy gates before bounded worker admission.

## Finding A0-ISSUER-01 — FileTaskIngress trusts caller-supplied approval_state (HIGH)

### Source trace

1. `FileTaskIngress._read()` in `runtime/mediahub_runtime/task_ingress.py` parses JSON from each `*.json` file in the configured inbox.
2. It requires `approval_state` as a non-empty string and accepts the literal values `not_required`, `approved`, `pending`, or `rejected`.
3. It copies that value directly into `AstraTaskRequest(approval_state=...)`. The ingress does not verify a signature, issuer identity, principal, capability, action/resource binding, approval expiry, revocation state, or replay receipt.
4. `FileTaskIngress.run_pending_bounded()` passes those requests directly to `AstraGatewayRuntime.run_bounded()`.
5. `AstraGatewayRuntime.run()` classifies a small set of sensitive action keywords and permits the sensitive action when `task.approval_state == "approved"`. The inspected path does not obtain an authenticated `AuthorizationContext` or independently resolve an approval attestation.
6. `runtime/mediahub_runtime/authorization.py` defines a fail-closed `AuthorizationPolicy` over explicit (principal, capability, operation) grants, but no call edge from FileTaskIngress or AstraGatewayRuntime to this policy was found in the inspected source.

### Security interpretation

The current source proves that the local Task Contract's approval string is treated as an authorization input by the gateway's sensitive-action gate. The source does **not** prove that the inbox is writable by an untrusted principal or that an attacker can reach this path; therefore this report does not claim a confirmed exploitable vulnerability. It does establish that approval provenance is not enforced within the reviewed ingress-to-gateway call path.

**Disposition: BLOCKED for issuer-backed approval qualification.** A JSON field equal to `approved` is not cryptographic or independently verifiable approval evidence.

### Required remediation design (not implemented)

- Treat `approval_state` as descriptive/untrusted input only; never use it as an authorization decision.
- Define an issuer-owned, signed approval/capability envelope with exact principal, capability, operation, resource/task identity, immutable target where applicable, issued-at, expiry, audience, unique grant/nonce and revocation/version reference.
- Verify the envelope at the authoritative A0 ingress boundary before constructing an authorized execution context.
- Bind authorization to the exact operation and resource; reject wildcard or ambiguous scope.
- Enforce expiry, revocation, audience, issuer allowlist, signature algorithm/key ID and replay prevention using durable atomic receipts.
- Keep Jarvis mission coordination, ASTRA A0 execution authority and MediaHub Product State Authority distinct. A Jarvis request must not self-issue A0 capability; A0 must not mutate product state outside its own domain.
- Preserve a fail-closed behavior when issuer, key state, revocation state, durable replay store or audit sink is unavailable.

No key format, issuer identity, trust root, or secret name is selected by this report. Those decisions remain subject to the governance contract and existing issuer/key lifecycle sources; do not invent or provision keys.

## Related source observations

- `authorization.py` is a minimal explicit allow-list policy; its existence alone does not prove it is wired into this ingress path.
- `sign_command.py` signs a distinct `mediahub.astra.control-command.v1` command format using per-node HMAC environment variables and a freshness window. The Task Contract format is different; no verified bridge between the two formats was found.
- `astra_github_agent.py` validates the signed control-command format and records executed command IDs in local state. This does not prove that FileTaskIngress uses that verifier or that replay receipts are durable/atomic across crashes and concurrent workers.
- The ASTRA queue defines a separate claim lease and permanent executor pool. This source does not establish a lease/cancel/recovery contract for FileTaskIngress requests.

## Proposed negative fixtures (NOT EXECUTED)

1. Change `approval_state` from `pending` to `approved` without a signed issuer envelope — must remain unauthorized.
2. Valid signature from unknown issuer/key ID — deny.
3. Valid issuer but wrong audience — deny.
4. Approval for operation A replayed for operation B — deny.
5. Approval for resource/task A replayed for resource/task B — deny.
6. Expired approval — deny.
7. Revoked approval or stale issuer/key version — deny.
8. Duplicate nonce under concurrent ingress — exactly one receipt accepted.
9. Replay after process restart — deny through durable receipt.
10. Revocation-store or audit-store outage — fail closed.
11. Malformed, duplicate-key or ambiguous envelope — deny.
12. Task request contains `approval_state=approved` but no authenticated AuthorizationContext — deny.

These are proposed fixtures only. No test code was added or executed in this pass.

## Governance and execution record

- Issue #301 remains OPEN and controlling.
- No runtime source was modified.
- No credentials or secret values were accessed.
- No provider/model API was called.
- No Gemini controller or child workflow was dispatched.
- SentinelX latest host inventory: zero connected hosts; enrolled Mac mini offline; two dev hosts disabled. No Claude task was run.
- No CI was triggered for this documentation branch at report creation.
- No merge, deployment, qualification or acceptance occurred.

## Next step

Continue the Issue #301 ordered work: define the issuer/capability authority and durable replay/lease/cancel/recovery contracts against existing source and governance records; do not wire new authorization behavior until the contract and independent review are accepted. In parallel, R-06 audit/privacy requirements and the authoritative runner/workspace/network target manifest must be resolved before bounded worker admission.

## References

- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [WB-14 source reconciliation](https://github.com/VlDMlNSh/mediahub-os/blob/f0448f28c7cfa61e4450c38529f09afbfdbbc7c7/docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-14-JARVIS-A0-AND-DIRECT-LOCAL-ROUTE-SOURCE-RECONCILIATION-2026-10-15.md)
- [Wave 205 truth-ranked audit](https://github.com/VlDMlNSh/mediahub-os/blob/f0448f28c7cfa61e4450c38529f09afbfdbbc7c7/docs/checkpoints/MEDIAHUB-CONTOUR-A-TRUTH-RANKED-AUDIT-READINESS-WAVE-205-2026-10-19.md)
- [Canonical chat tree map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
