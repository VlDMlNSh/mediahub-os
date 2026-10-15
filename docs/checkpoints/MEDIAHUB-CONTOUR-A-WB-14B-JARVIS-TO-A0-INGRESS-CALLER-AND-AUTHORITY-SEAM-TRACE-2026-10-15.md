# MediaHub OS — Contour A WB-14B: Jarvis-to-A0 Ingress Caller and Authority Seam Trace

- Date: 2026-10-15
- Status: **BOUNDED READ-ONLY SOURCE TRACE / END-TO-END INGRESS NOT ESTABLISHED / CONTRACT GAPS RECORDED**
- Parent continuation: WB-14 in `main` blob `4dead9e249603679f4193a5a0b0b0a13a04aa177`; this is the WB-14B subpass on documentation branch `docs/mediahub-chat-tree-map-20261012`.
- Scope: trace the best-evidenced current task-ingress and operational-command paths and determine whether the tracked source proves a Jarvis mission producer connected to an accepted A0 ingress. No contract wiring or code changes.

## 1. Result

**No end-to-end Jarvis → accepted ASTRA A0 ingress caller-to-consumer chain was established in this bounded source pass.**

The source does establish a local file-based Task Contract consumer that converts JSON into `AstraTaskRequest` and calls `AstraGatewayRuntime.run_bounded`. Separately, it establishes a signed operational-command workflow and verifier path. The reviewed sources do not connect either path to an authenticated Jarvis principal, issuer-backed `AuthorizationContext`, or a canonical corporation mission envelope.

This is a traceability/contract gap, not a claim that no such path exists in external, generated, uninspected or deployment context. No exploitability conclusion is drawn.

## 2. Refreshed source pins

Repository tree snapshot on `main`: HEAD `ab36db009d034db8dca723691e23b331322287e7`, 800 entries, `truncated=false`. Documentation branch remains separate and divergent; no integration was performed.

| Source | Ref | Blob SHA | Direct evidence | Limitation |
|---|---|---|---|---|
| `runtime/mediahub_runtime/task_ingress.py` | main | `59e1254aa61cc8f55f53bd1e179631e81c441393` | `FileTaskIngress.read_pending()` enumerates local `*.json`; `_read()` validates selected schema/shape; `run_pending_bounded()` invokes `gateway.run_bounded(task, policy=...)`. | No authenticated Jarvis producer, inbox writer authority or wire/service ingress is shown in this module. |
| `runtime/mediahub_runtime/astra_gateway.py` | main | `10985e4ad8f682313d08e7492ecc1856a8bce20f` | `AstraTaskRequest` carries request/session/command/context/approval fields; gateway implements bounded intake/execution and emits result/evidence structures. | Request shape does not establish caller authentication or attested approval. |
| `runtime/mediahub_runtime/authorization.py` | main | `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | Typed `AuthorizationContext` and explicit tuple allow-list policy exist. | No traced producer edge from Task Contract ingress to this context; no issuer, audience, expiry or revocation lifecycle established by this source pin. |
| `ops/control/sign_command.py` | main | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Signs the node-bound `mediahub.astra.control-command.v1` operational envelope using node-specific HMAC key names and timestamp freshness bounds. | This is a command signer, not evidence of a Jarvis mission/Task Contract producer. |
| `astra_github_agent.py` | main | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Verifies the matching command envelope, HMAC/freshness and command IDs before its dispatch path. | No source edge connects this verifier path to `FileTaskIngress` or the P0 typed authorization path. |
| `tools/sign_astra_command.py` | main | `a4222ac51a47cbfe8288f9af34f1e542c0a4b6a8` | Produces a distinct `schema: 1` envelope using `ASTRA_COMMAND_HMAC_KEY`. | Active/canonical status remains unknown; no disposition inferred. |
| `.github/workflows/astra-autonomous-supervisor.yml` | main | `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | Workflow materializes a `mediahub.astra.control-command.v1` envelope, invokes `ops/control/sign_command.py`, and later verifies/dispatches the prepared command through workflow steps. | Workflow source demonstrates an operational-command automation path, not a Jarvis→TaskIngress or accepted external service ingress. No workflow run was inspected or claimed. |
| `.github/workflows/astra-chat-control.yml` | main | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | Parses bounded chat commands and dispatches explicit workflow operations including `run-gold` / `run-worker`. | This is a GitHub workflow control surface; source reviewed does not show it calling `FileTaskIngress` or authenticating a corporation-wide Jarvis mission envelope. |
| `runtime/mediahub_runtime/mission_journal.py` | main | `518577c35e0bc00aed9be4c8f5b6594de66b5700` | Durable journal records command ID, node ID, target SHA, agent SHA and execution status. | Local execution journal is not a mission submission API, capability issuer or Jarvis ingress. |
| `runtime/mediahub_runtime/execution_adapter.py` | main | `f40f8092b63966434f619396b0e8091ceef91a97` | Executes a configured backend command using a bounded argument vector and returns backend result. | Backend execution seam alone does not establish route admission, queue ownership or Jarvis caller identity. |
| `.github/agent-system/contracts.md` | main | `184e986cfb116bccf29e4aded9fb47e5d05a3e92` | Contains conceptual mission/task/result contract sections. | Does not define an accepted Jarvis→A0 wire/API contract or caller-verifier chain. |
| Jarvis Control Plane and GitHub Adapter Contract Draft 01 | docs branch | `e112cc73178eef5f71b8a814296e4902c2e80390` | Describes proposed Jarvis role, mission envelope and A0 submission intent; explicitly leaves exact API/authentication/issuer to accepted source contracts. | Design draft only; not a sourced API or runtime connection. |
| Owner decision record / corporation direction | docs branch | `70376a2709e055972ceddc4a280d26992977213c` | Records owner-approved lifecycle split and hybrid-routing direction; engineering missions requiring ASTRA lifecycle controls should use sourced A0 interface. | Owner direction does not supply the missing API, principal, issuer, wire schema or implementation evidence. |
| WB-14 parent reconciliation | main | `4dead9e249603679f4193a5a0b0b0a13a04aa177` | Decomposes WB-14A…G and identifies WB-14B as the next ingress/authority pass. | Parent artifact is on divergent main, not this docs branch; this report is a subpass, not a merge. |

## 3. Proven source flow vs missing edge

### Proven locally

1. Local JSON Task Contract files → `FileTaskIngress._read()`.
2. Schema/shape checks → `AstraTaskRequest`.
3. `FileTaskIngress.run_pending_bounded()` → `AstraGatewayRuntime.run_bounded()`.
4. Separate signed operational-command flow: workflow prepares envelope → `ops/control/sign_command.py` signs it → workflow artifact/steps → `astra_github_agent.py` verifies and dispatches the command.
5. Separate typed authorization seam: an already-created `AuthorizationContext` is evaluated by the local policy/consumer boundary path described in WB-07.

### Not established

- A tracked Jarvis producer that creates the Task Contract consumed by `FileTaskIngress`.
- A trusted inbox writer/ACL contract and producer identity.
- A network/API ingress or service principal accepted as the canonical Jarvis→A0 interface.
- A link from the file Task Contract path to `AuthorizationContext` issuance and verification.
- An issuer-backed sensitive approval attestation. `approval_state` is a file-provided string with enum validation in the inspected ingress, not independently verifiable approval provenance.
- A formal relationship between the signed operational command schema and the Task Contract schema. They are distinct trust domains and must not be treated as interchangeable.
- An end-to-end direct Jarvis→Alamo/local executor caller or queue lifecycle.

## 4. WB13-R01…R12 implications

| Requirement | WB-14B source result | Status |
|---|---|---|
| R01 Stable mission identity | Local request ID exists and duplicates are rejected within one inbox batch; no common cross-route mission envelope proven. | PARTIAL |
| R02 Auditable route policy | Workflow selection exists in limited GitHub command surfaces; no accepted corporation-wide route decision point is proven. | OPEN |
| R03 A0 lifecycle authority | Canonical ASTRA matrix and queue references support A0-owned ASTRA lifecycle. | SOURCE-ALIGNED DESIGN; runtime not qualified here |
| R04 Alamo queue owner | No Alamo route/lifecycle edge in inspected ingress/queue sources. | BLOCKED |
| R05 Caller identity/capability | Shape checks and HMAC operational-command verification are separate. | BLOCKED end-to-end |
| R06 Approval provenance | File-supplied approval enum has no attestation edge in this trace. | BLOCKED |
| R07 Provider/egress | Not resolved by the ingress path. | UNKNOWN |
| R08 Media backend/resources | No direct local-media ingress or admitted Alamo backend shown. | BLOCKED |
| R09 Result/evidence envelope | Gateway and ASTRA queue expose distinct result/evidence structures; no common Jarvis envelope proven. | DRAFT CONTRACT NEEDED |
| R10 Retry/cancel/recovery | A0 has its own lifecycle; no direct local lifecycle established. | BLOCKED for Route B |
| R11 No second State Authority | Existing owner direction keeps Product State Authority separate and ASTRA state domain-scoped. | REQUIRED INVARIANT |
| R12 Readiness gate separation | Design documents and workflow definitions do not prove execution/qualification/acceptance. | REQUIRED INVARIANT |

## 5. Precise gaps and bounded recommendations

1. **Jarvis→A0 ingress:** source and accept one canonical interface contract before implementation. It must name caller/service principal, receiver, versioned mission envelope, target/source binding, acknowledgement semantics, error taxonomy, idempotency, authorization, audit and result return. Do not invent endpoint, protocol or token technology in this trace.
2. **Trusted Task Contract producer:** decide whether this local file ingress remains an internal adapter with OS-level producer controls or is retired in favor of a separately authenticated service ingress. This is an owner/governance choice; the current trace does not select one.
3. **Sensitive approval:** replace trust in caller-supplied `approval_state` with a contract that verifies approval provenance and task/action/resource scope before sensitive execution. Do not infer that this change is implemented.
4. **Operational command vs task ingress:** retain the formats as separate until a documented adapter contract explains their relation. Do not assume an HMAC command signature automatically authenticates the Task Contract or grants execution capability.
5. **Route B:** direct Alamo dispatch remains a proposal; it requires its own caller authentication, queue lifecycle owner, result adapter and explicit route/data policy. It cannot reuse the absence of A0 as a reason to omit controls.
6. **Search boundary:** source tree and the named call sites/workflows were reviewed. No tests, runtime execution or security scans were run; no claim of a repository-wide semantic absence proof is made.

## 6. Status and next sub-request

- WB-14B: **COMPLETED AS A BOUNDED SOURCE TRACE; END-TO-END INGRESS REMAINS UNESTABLISHED**.
- No code, normative contracts or workflows changed.
- No tests, provider/model calls, credentials, host/runtime inspection, installation, infrastructure changes, deployment or branch integration.
- Next: **WB-14C — compare `runtime/mediahub_runtime/autonomous_queue.py` and related queue contracts against direct-local Route B requirements**, pinning queue ownership, node binding, claim/lease, retry/cancel/recovery and result semantics. Do not run tests or alter the queue implementation.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
