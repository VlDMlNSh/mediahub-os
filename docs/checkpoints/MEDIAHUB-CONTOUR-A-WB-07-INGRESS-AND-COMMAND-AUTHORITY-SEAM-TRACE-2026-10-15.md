# MediaHub OS — Contour A WB-07 Ingress and Command-Authority Seam Trace

- Date: 2026-10-15
- Status: **BOUNDED SOURCE TRACE / PARTIAL CLOSURE / NON-NORMATIVE / NOT QUALIFIED**
- Scope: directly inspect tracked source-tree entries and selected ingress, gateway, signer, verifier, and authorization modules on `main`. No code was changed and no executable checks were run.
- Guardrail: this is a source-level boundary trace, not a claim of a confirmed exploitable vulnerability or a repository-wide absence proof.

## 1. Outcome

This pass established a second, relevant trust boundary: the local file-based `FileTaskIngress` parses a JSON Task Contract, checks schema identifiers and selected fields, then converts it into an `AstraTaskRequest` and calls `AstraGatewayRuntime.run_bounded`. In the inspected code, this path does not create or carry `AuthorizationContext`, and its `approval_state` value is accepted from the task file after an enum check. The code read does not establish who is authorized to write the inbox or whether a separate upstream authority attests the approval value. Therefore, this is a boundary/ownership question, not by itself proof of an exploitable bypass.

A separate signed-command flow exists: `ops/control/sign_command.py` uses schema `mediahub.astra.control-command.v1`, per-node HMAC environment-variable names, and freshness checks when signing; `astra_github_agent.py` validates the command HMAC, timestamp age and command ID before its dispatch path. A second helper, `tools/sign_astra_command.py`, creates a different, minimal envelope (`schema: 1`) with a generic `ASTRA_COMMAND_HMAC_KEY`. The inspected source does not establish whether this second helper is active, legacy, or called by a production path. The two envelope formats and key-resolution conventions must not be assumed interoperable.

## 2. Direct source evidence (main blob SHAs)

| Source | Evidence | Classification / limitation |
|---|---|---|
| Repository tree | GitHub recursive tree response for `main`: 799 entries, `truncated=false`. Relevant tracked paths included the modules listed below. | **EVIDENCED: tree snapshot**; not a semantic search of every possible generated/external caller. |
| `runtime/mediahub_runtime/task_ingress.py` | Blob `59e1254aa61cc8f55f53bd1e179631e81c441393`. `FileTaskIngress._read` parses JSON; checks required fields, schema ID/version, owner, non-empty IDs/command/approval state, enum membership and context-ref shape; constructs `AstraTaskRequest`. `run_pending_bounded` passes parsed requests to `gateway.run_bounded`. | **EVIDENCED: local file ingress path**. No `AuthorizationContext` issuer verification in this file. Inbox writer/permission and upstream approval attestation are not established here. |
| `runtime/mediahub_runtime/astra_gateway.py` | Blob `10985e4ad8f682313d08e7492ecc1856a8bce20f`. `AstraTaskRequest` has request/session/command/context/approval fields, not `AuthorizationContext`; `run_bounded` validates the task, then executes `run`; sensitive-action handling relies on `approval_state == "approved"`. `_capability` derives routing labels from command text. | **EVIDENCED: gateway seam**. Routing labels are not shown to be security grants. No source edge from this path to the P0 State Authority `AuthorizationContext` policy was established. |
| `runtime/mediahub_runtime/authorization.py` | Blob `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`. Context holds `principal` and `capability`; policy matches a configured `(principal, capability, operation)` tuple. | **EVIDENCED: separate local policy seam**. No link from Task Contract ingress to this context was established. |
| `ops/control/sign_command.py` | Blob `fc6943a79cefdf06e59d6e32771d2df551b2f0e9`. Defines `mediahub.astra.control-command.v1`, required command fields, node-specific key environment names, timestamp freshness check and HMAC-SHA256 signing. | **EVIDENCED: signer implementation**. No invocation relationship to `FileTaskIngress` established. |
| `astra_github_agent.py` | Blob `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`. Reads command JSON, checks required fields, validates HMAC and age, then checks command ID against execution markers before dispatch. | **EVIDENCED: verifier/dispatch seam**. Not proven to be the same path as file Task Contract ingress or the P0 State Authority path. |
| `tools/sign_astra_command.py` | Blob `a4222ac51a47cbfe8288f9af34f1e542c0a4b6a8`. Produces `schema: 1`, `command_id`, `node_id`, `operation`, `issued_at`, and `signature` using generic `ASTRA_COMMAND_HMAC_KEY`. | **EVIDENCED: second envelope producer**. Whether used, obsolete or connected to a verifier remains unknown. |
| `ops/mesh/state.py` | Blob `d02780894cfb5d3c0fc7878d57a08fac2e428efc`. Inspected as a candidate source file; no `AuthorizationContext`, `principal`, `capability`, issuer, or signature terms were present in the source. | **BOUNDED FILE OBSERVATION ONLY**; not evidence that mesh state has no trust role elsewhere. |
| `runtime/mediahub_runtime/agent_fabric.py` | Blob `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd`. Claim/lease records are JSON persisted; documented in module as coordination state, not domain authority. | **EVIDENCED: coordination seam**; not an authorization issuer. |
| `runtime/mediahub_runtime/astra_context.py` | Blob `9a30c0a3299e6b3a47bc03f55f4d26d2d9f14ad9`. Builds bounded advisory memory context; prompt text explicitly treats durable memory as untrusted and not authorization/policy/source of truth. | **EVIDENCED: memory-context handling**; unrelated to issuing `AuthorizationContext`. |
| `runtime/mediahub_runtime/astra_security.py` | Blob `ff4ba9b581cf30e0f2d6bbed70c5290d93bfa27d`. Provides secret-like value scanning/redaction. | **EVIDENCED: memory secret hygiene utility**; not a principal/capability issuer or signature verifier. |

## 3. End-to-end seam map

1. **File Task Contract path:** JSON inbox file → `FileTaskIngress._read` schema/shape checks → `AstraTaskRequest` → `AstraGatewayRuntime.run_bounded` → gateway policy/routing/execution path.
2. **P0 authorization path:** an already-instantiated `AuthorizationContext` → `ConsumerBoundary` → `InMemoryStateAuthority` → allow-list policy. The inspected source does not establish a producer edge from Task Contract ingress into this path.
3. **Signed command path:** command JSON → `astra_github_agent.py` HMAC/freshness/ID checks → command dispatch. `ops/control/sign_command.py` appears structurally aligned with that command schema/key convention, but a full caller-to-signer-to-verifier invocation trace was not established in this pass.
4. **Second signer helper:** `tools/sign_astra_command.py` emits a different schema/key convention. No connection to the verifier was established.

## 4. Questions requiring owner/governance resolution

- Is the Task Contract inbox trusted by filesystem ownership/ACL and a controlled producer, or must the contract itself carry authenticated provenance?
- Who is authoritative for `approval_state`, and what evidence must bind an approval to a request/action?
- Is `tools/sign_astra_command.py` active, retained historical code, or superseded? Which command schema and key-resolution convention is canonical?
- Should signed operational commands and product authorization contexts remain distinct trust domains, and if so, what explicit adapter/authority boundary is required?
- Which path, if any, is the approved Jarvis→ASTRA A0 ingress? No owner decision is inferred from this source trace.

No option is selected here. Do not consolidate schemas, change key names, or wire ingress to the State Authority based only on these observations.

## 5. Non-actions and closure status

- No tests, security scans, qualification or runtime execution.
- No credentials read or used; no provider/model calls.
- No host/runtime inspection, installation, infrastructure changes, deployment or branch integration.
- No code or normative contract changed.
- **Confirmed:** local file-ingress/gateway seam, separate P0 typed authorization seam, signed command verification seam, and a second signer-helper format.
- **Not established:** inbox writer trust boundary, approval attestation authority, canonical signer helper, complete signer-to-verifier call graph, and any end-to-end Jarvis→A0 issuer/verifier chain.

## 6. Next bounded step

Perform a read-only reference/caller trace for the two signer helpers and the `FileTaskIngress` entry point: inspect tracked call sites, workflow/script references and contract documentation. Record direct evidence and avoid interpreting no-result searches as proof of non-use. Then present the unresolved authority choices to the owner; do not change security contracts or wire paths before a decision.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
