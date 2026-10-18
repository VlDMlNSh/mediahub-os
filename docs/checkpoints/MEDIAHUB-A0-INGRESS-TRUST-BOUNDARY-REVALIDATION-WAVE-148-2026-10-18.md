# MediaHub OS — A0 ingress trust-boundary revalidation, Wave 148

- Date: 2026-10-18
- Ref: `main` source snapshot and `docs/mediahub-chat-tree-map-20261012` documentation ref
- Status: **BOUNDED SOURCE REVALIDATION / TRUST-ISSUER GAP OPEN / NOT QUALIFIED**
- Scope: re-read the current main implementations of file Task Contract ingress, Astra gateway, typed authorization policy, both command-signing helpers, and the existing Wave 134 source inventory. This is a source-only pass; no runtime execution or security exploitability claim is made.

## 1. Executive result

The source-level trust boundary remains split across three non-equivalent paths:

1. **Task Contract ingress:** JSON inbox file → `FileTaskIngress._read` → `AstraTaskRequest` → `AstraGatewayRuntime.run_bounded`. The ingress validates schema/version, owner, field shape and approval-state enum, but `approval_state` is read from the file itself. The inspected path does not verify an issuer, signed approval attestation, or construct `AuthorizationContext`.
2. **State-authority authorization:** `AuthorizationContext(principal, capability)` is a local typed value; `AuthorizationPolicy` checks a configured tuple grant. Type checking and allow-list matching do not prove who issued the context or its lifetime, audience, resource binding, revocation, delegation or replay properties.
3. **Signed operational command:** `ops/control/sign_command.py` defines `mediahub.astra.control-command.v1`, node-specific HMAC environment names, required fields and a freshness window. The separate `tools/sign_astra_command.py` emits a different `schema: 1` envelope using generic `ASTRA_COMMAND_HMAC_KEY`. No evidence in this bounded trace establishes these two formats as interoperable or the second helper as an authoritative production path.

The seam remains **NOT CLOSED**. Do not select or invent an issuer/token format, ingress API, revocation contract, or exactly-once guarantee in code. These decisions are explicitly open in the project's A0 issuer/lifecycle and governance evidence. The safe next implementation is blocked on the accepted authority/lifecycle contract, not on lack of a possible technical implementation.

## 2. Exact source evidence

All source blobs below were re-read from GitHub on `main`:

| Source | Blob SHA | Direct observation |
|---|---|---|
| `runtime/mediahub_runtime/task_ingress.py` | `59e1254aa61cc8f55f53bd1e179631e81c441393` | `FileTaskIngress._read` parses JSON, checks required fields, schema ID/version, owner, non-empty fields, approval enum and context-ref shape, then constructs `AstraTaskRequest`; `run_pending_bounded` calls `gateway.run_bounded`. |
| `runtime/mediahub_runtime/astra_gateway.py` | `10985e4ad8f682313d08e7492ecc1856a8bce20f` | `AstraTaskRequest` carries request/session/command/approval/context fields, but not `AuthorizationContext`; gateway path remains separate from the typed state-authority context seam. |
| `runtime/mediahub_runtime/authorization.py` | `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | Context is a frozen dataclass with `principal` and `capability`; policy allows only configured `(principal, capability, operation)` tuples. No issuer verification is implemented here. |
| `runtime/mediahub_runtime/consumer_boundary.py` | `98bf2da9cea85da2c82145b4baef417c20b9ae73` | Typed context is required at the consumer boundary; this validates type/allow-list path but does not establish context provenance. |
| `ops/control/sign_command.py` | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | HMAC signer with versioned command schema, per-node key environment names and timestamp freshness check. This signer is not shown to issue the Task Contract's approval state or `AuthorizationContext`. |
| `tools/sign_astra_command.py` | `a4222ac51a47cbfe8288f9af34f1e542c0a4b6a8` | Separate minimal schema and generic key variable; compatibility/active caller remains unestablished. |
| `docs/checkpoints/MEDIAHUB-A0-ISSUER-DECISION-PACKET-CALLSITE-INVENTORY-WAVE-134-2026-10-18.md` | `cd6f6021bc5b617ef0bc581bfe4a6748515ce81e` | Prior bounded inventory says all 193 tracked Python blobs in its pinned main snapshot were scanned; only direct constructors were deterministic qualification fixtures, not an authoritative production issuer. |

Related prior source trace: [WB-07 Ingress and Command-Authority Seam Trace](MEDIAHUB-CONTOUR-A-WB-07-INGRESS-AND-COMMAND-AUTHORITY-SEAM-TRACE-2026-10-15.md), blob `89fab594f9a9ae9a729d63ecb14dad2543edc9af`. The report is read by blob SHA because the Contents API returns 404 for that historical path at the current ref.

## 3. Decision and boundaries

- **No implementation change** to issuer, token, ingress, approval semantics, or state authority is justified by this source-only evidence.
- Keep task-routing labels separate from security capability grants.
- Do not trust file-supplied `approval_state` as an external authorization attestation without a separately accepted producer/trust contract.
- Do not treat HMAC command signatures as interchangeable with the Task Contract or `AuthorizationContext`.
- Preserve Product State Authority as the sole canonical product-state mutation authority. ASTRA A0 remains engineering coordination/queue state, not Product State Authority.
- No tests, credentials, provider calls, worker dispatch, host inspection, deployment, merge or qualification were performed in this pass.

## 4. Repository state and next action

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical documentation map ref: `docs/mediahub-chat-tree-map-20261012`; current map blob before this pass: `e6ed792d3e64df994b7895b6ae0aa1d1a69cfff2`. Contents API returned an empty body; full content was recovered through the blob API (1,058,262 characters).
- Documentation ref vs main: **DIVERGED**, 2,268 ahead / 27 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No branch integration was attempted.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open.
- PR [#358](https://github.com/VlDMlNSh/mediahub-os/pull/358) remains Draft/open/unmerged; exact-head CI has verified the seven run-correlation tests, but that does not close the A0 issuer gate.
- PR [#350](https://github.com/VlDMlNSh/mediahub-os/pull/350) remains Draft/open and currently non-mergeable against the diverged documentation ref.

**Next bounded step:** read the accepted MH-12/MH-13 authority and R-06 audit/privacy decisions together with the WB-05 issuer decision packet; identify the exact owner/governance disposition required for principal, audience/resource/scope, lifetime, revocation, delegation, replay, approval attestation, and audit-unavailable behavior. Only after that decision is recorded should an issuer/verifier implementation and its positive/negative tests be selected. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED**; Contour B remains gated.
