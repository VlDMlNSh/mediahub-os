# MediaHub OS — Contour A WB-06 AuthorizationContext Producer/Consumer Source Inventory

- Date: 2026-10-15
- Status: **BOUNDED SOURCE INVENTORY / PARTIAL CLOSURE / NON-NORMATIVE / NOT IMPLEMENTED / NOT QUALIFIED**
- Scope: trace directly inspected source seams for `AuthorizationContext`, capability/principal values and adjacent authorization boundaries. This is not a repository-wide absence proof, runtime finding or security qualification.
- Governing direction: owner-approved DEC-DEV-02 Option C remains in force. Jarvis coordinates corporation-level missions; ASTRA A0 owns ASTRA-internal workflow state; MediaHub Product State Authority alone owns canonical product-state mutation.
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`.

## 1. Result

The bounded trace confirms one typed in-process authorization path around the P0 State Authority seam and one separate command-envelope HMAC path in `astra_github_agent.py`. They are not shown by the inspected evidence to be connected to each other or to a Jarvis→A0 ingress contract.

The `AuthorizationContext` path carries only `principal` and `capability` strings. The policy matches the tuple `(principal, capability, operation)` against configured grants and denies unmatched contexts. `ConsumerBoundary` checks that the context has the expected Python type, then passes it to the State Authority, which applies the configured policy. This establishes a local authorization seam, but not who created the context, whether its fields are authentic, which audience/resource it is bound to, or whether it is current/revocable.

GitHub code-search requests for `AuthorizationContext`, `AuthorizationPolicy`, `capability principal` and `AuthorizationContext(` returned no results in the connected search surface. Because that search surface is non-diagnostic here, its empty result is **not evidence of absence**. The directly inspected package directory and source files support only the paths listed below.

## 2. Source-pinned edge inventory

| Edge / surface | Direct source evidence | Classification | Limits |
|---|---|---|---|
| Public package export | `runtime/mediahub_runtime/__init__.py`, main blob `4ff499f8e489e60e344283ee01e4dad5e72a2646`, exports `AuthorizationContext`, `AuthorizationPolicy`, `ConsumerBoundary`, `OperationRequest`, `InMemoryStateAuthority`. | **EVIDENCED: export surface** | Exporting a type does not establish its runtime producers or trust provenance. |
| Context data model | `runtime/mediahub_runtime/authorization.py`, main blob `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`: frozen dataclass with `principal: str` and `capability: str`. | **EVIDENCED: shape** | No issuer, signature, audience, resource, expiry, provenance, revocation or freshness field appears in this type. This observation is limited to this type. |
| Policy decision | Same `authorization.py` blob: policy converts the context to `(principal, capability, operation)`; exact tuple membership is required; empty grants deny. | **EVIDENCED: local grant verifier** | Does not authenticate the principal or prove that capability was issued by an authorized issuer. |
| Request construction | `runtime/mediahub_runtime/consumer_boundary.py`, main blob `98bf2da9cea85da2c82145b4baef417c20b9ae73`: `ConsumerBoundary.request(operation, context)` validates non-empty operation and `isinstance(context, AuthorizationContext)`, then creates `OperationRequest`. | **EVIDENCED: in-process propagation** | Type-checking does not validate origin, audience, scope, expiry or revocation. |
| Mutation/restore consumers | Same `consumer_boundary.py` blob: begin/snapshot/restore pass `request.context` to the authority; commit/abort rely on operation matching and the transaction's retained context in the authority path. | **EVIDENCED: inspected consumer calls** | No external ingress, serialized context decoding or issuer verification is established by these methods. |
| State Authority enforcement | `runtime/mediahub_runtime/in_memory_state.py`, main blob `0fbc71369d19e09944ba67a60ccb9df802f30a4b`: `_authorize` requires the context type and calls configured policy; begin/snapshot/restore and commit/abort invoke authorization. | **EVIDENCED: local authority check** | Does not establish issuer provenance or an external caller path. |
| Separate signed command envelope | `astra_github_agent.py`, main blob `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`, relevant source lines 19–30, 75–84 and 103–116: per-node HMAC key configuration, required command fields, timestamp-age check, HMAC-SHA256 comparison and executed-command marker check. | **EVIDENCED: distinct command-auth seam** | This is a separate command envelope; inspected evidence does not connect it to `AuthorizationContext`, Jarvis issuer ownership or the P0 consumer boundary. Do not treat it as proof of Jarvis→A0 trust closure. |
| Related test source | `tests/test_astra_command_auth.py`, main blob `8df49fc55e660c13ad54aca9b9dc78132c335dd1`, describes tests for signature, stale command, ID safety, required fields and idempotency marker. | **SOURCE READ ONLY** | No test was executed. This test file concerns the separate command-envelope seam. |
| Capability inventory contract | `tests/test_mesh_capability_inventory_contract.py`, main blob `cf0d03367e48f360ef6c6981e1bf7b4d798bf322`, references inventory-derived capability metadata and asserts authority `NONE` / qualification state `DISCOVERED` in its source. | **SOURCE READ ONLY** | Not run; does not establish a runtime issuer/verifier path for `AuthorizationContext`. |

## 3. Current producer → propagation → consumer trace

1. **Producer:** no authoritative `AuthorizationContext` constructor call site was established from the available code-search surface. The class definition and public export are confirmed; complete construction history is **NOT ESTABLISHED**.
2. **Propagation:** the directly inspected API accepts an already-instantiated `AuthorizationContext` and wraps it in `OperationRequest`. This is an in-process typed handoff, not an authenticated wire/ingress contract.
3. **Policy verification:** `AuthorizationPolicy.decide/require` performs configured tuple matching and fail-closed denial for non-context/unmatched grants.
4. **Consumer:** `ConsumerBoundary` passes context to `InMemoryStateAuthority`; the authority repeats type validation and policy enforcement for protected operations.
5. **Separate command path:** `astra_github_agent.py` checks a signed, timestamp-bounded command envelope and a prior-execution marker. No inspected edge proves this path feeds or verifies the `AuthorizationContext` path.
6. **Jarvis→A0 edge:** issuer/attester authority, identity binding, audience, delegation attenuation, replay contract, expiry/revocation propagation, serialization and end-to-end caller-to-consumer trace remain **NOT ESTABLISHED** by this bounded inventory.

## 4. Capability-value caution

The inspected `AstraGatewayRuntime` source (`runtime/mediahub_runtime/astra_gateway.py`, main blob `10985e4ad8f682313d08e7492ecc1856a8bce20f`) derives labels such as `research`, `architecture`, `review`, `documents` and `coding` from task text for agent routing. Those values are routing/registry capability labels in that code path; the source read does not show them being issued as `AuthorizationContext.capability` grants. Do not conflate task-routing labels with security capabilities.

## 5. Closure classification

- **Confirmed:** local typed context shape; explicit allow-list policy semantics; in-process request propagation; State Authority policy checks; separate HMAC command-envelope logic.
- **Partially established:** protected consumer calls within the inspected P0 State Authority path.
- **Not established:** all context producers/call sites; all serialization/deserialization edges; relationship between command-envelope HMAC and `AuthorizationContext`; Jarvis→A0 issuer/verifier chain; audience/resource/scope binding; revocation/expiry freshness; full repository-wide occurrence/history closure.
- **Not performed:** tests, qualification, runtime/host inspection, model/provider calls, credentials, installation, infrastructure changes or deployment.

No source code or normative contract was changed. No issuer, protocol, token format, key store, endpoint or ownership option was selected.

## 6. Next bounded step

Continue source-only closure by inspecting the directly referenced caller/consumer modules and the repository's tracked source tree for additional constructor, serialization and invocation paths. Use direct file reads and record each source ref/blob SHA. If complete repository-wide closure cannot be established from available GitHub evidence, preserve that limitation explicitly; do not treat search misses as proof of absence. In parallel, issuer-authority alternatives remain unselected until the owner/governance decision is recorded. Jarvis→A0 ingress stays blocked.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
