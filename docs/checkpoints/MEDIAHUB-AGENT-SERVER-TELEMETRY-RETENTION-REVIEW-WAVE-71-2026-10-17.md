# MediaHub OS — Agent Server Telemetry, Completion Logging and Secret-Retention Review, Wave 71

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Ref: `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`
- Status: **SOURCE-ONLY REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- Tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Related privacy authority: [MH-13 reconstructed privacy/data governance](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MH-13-privacy-data-governance.md)
- Related governance state: [MH-13 governance state](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MH-13-governance-state.md)
- Prior admission record: [Wave 70 reuse inventory](MEDIAHUB-A0-ISSUER-VERIFIER-REUSE-INVENTORY-WAVE-70-2026-10-17.md)

## 1. Scope and evidence boundary

This pass checks the public OpenHands Agent Server documentation for telemetry, completion logging, secret storage and deletion/retention semantics against R-06 and MH-13.

Official source reviewed for discovery:
- [OpenHands/software-agent-sdk — Agent Server README on main](https://github.com/openhands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/README.md)
- [Agent Server event service source on main](https://github.com/openhands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/event_service.py)
- [Telemetry policy source on main](https://github.com/openhands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/telemetry/policy.py)
- [Telemetry event models on main](https://github.com/openhands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/telemetry/models.py)

**Pinning limitation:** this pass did not recover the exact upstream commit/tag/digest admitted or proposed in the MediaHub component crosswalk. The source links above point to a moving `main` ref and are discovery evidence only, not proof about the exact candidate artifact. No source-pinned implementation claim or qualification is made.

## 2. Source-level findings

| Surface | What the reviewed documentation says | MediaHub consequence |
|---|---|---|
| Product telemetry | Disabled by default; delivery requires explicit exporter configuration. The documented event contract is allowlisted and excludes prompts, messages, file contents, paths, secrets, request/response bodies and tracebacks. | Promising minimization boundary, but candidate configuration and exact-version implementation still need source-pinned verification. |
| Consent / revocation | Consent can be unset/granted/denied; `DO_NOT_TRACK=1` is a kill switch. Revocation stops delivery before the settings request returns and discards queued events. | Useful control, but cannot substitute for MediaHub's accepted R-06 authority, audit and policy contract. |
| Telemetry identity | The documented PostHog `distinct_id` can be the deployment-supplied `user_id` verbatim; request-scoped identity can also arrive in a frontend header. | These identifiers may be personal or linkable data. Default telemetry-off is necessary; any exporter requires explicit classification, purpose, minimization, destination and retention approval. |
| Completion logging | `log_completions` is described as recording full prompts, responses and raw provider payloads to local disk for high-fidelity debugging; it is distinct from telemetry and is not forwarded to telemetry. | **High-risk by default for MediaHub.** Must remain disabled unless a separate approved purpose, synthetic/minimized input policy, access controls, bounded retention and deletion evidence exist. Local-only is not equivalent to safe or short-lived. |
| Distributed tracing | Laminar/OpenTelemetry traces go to the configured observability backend. The README says completion logging and tracing are not forwarded to product telemetry. | Backend, processors, exporters, span attributes, sampling, retention and redaction are not fully established by the README alone. Treat traces as a separate egress surface. |
| Conversation/event persistence | Conversations and events are stored on the local filesystem; the documented layout includes per-conversation metadata and `events.jsonl`. | Event logs may contain user content or tool output. No retention period, automatic expiry, backup deletion, or complete erasure guarantee is established by the reviewed README. |
| Secret encryption | `OH_SECRET_KEY` encrypts stored LLM keys, AWS credentials and conversation secrets. Without it, secrets are redacted and not persisted across restarts; changing it makes previously encrypted values unreadable. | Encryption at rest depends on correct key injection and lifecycle. It does not establish workspace/log redaction, memory isolation, key rotation/recovery, or deletion of copies. |
| Authentication / network | README describes session API-key authentication as optional and the default bind address as `0.0.0.0`; it advises restricting access. | Unsafe defaults for any exposed or shared runtime. Candidate admission would require explicit bind/authentication policy, isolated workspace and network controls. |
| Workspace authority | The server has full access to its configured workspace. | Agent workspace must be isolated to a disposable, approved repository/worktree and must not mount User Domain data or ambient credentials. |

## 3. Crosswalk to R-06 and MH-13

MH-13 source reviewed on `main`:
- `docs/architecture/MH-13-privacy-data-governance.md`, blob SHA `e732ff9cacbc9c1189bd83306cdff30906326cf0`.
- `docs/architecture/MH-13-governance-state.md`, blob SHA `7bd2624c3072ecf0a08a430bb8b8214b3d55d3fa`.

The reconstructed MH-13 artifact is recorded as an accepted reconstruction, but not frozen; historical fidelity is partial, and production implementation is not authorized. Its applicable invariants include data minimization, purpose limitation, external-transfer controls, telemetry/log redaction, explicit retention/deletion semantics, protection of derived data and no implicit trust of providers.

| Control | Evidence status | Required admission evidence |
|---|---|---|
| Completion logging off by default and enforced in the exact pinned runtime | PARTIAL — docs describe behavior; exact candidate SHA not established | Exact tag/commit/image digest plus config mapping and code-level read-back |
| Telemetry consent and revocation behavior | DOCUMENTED / NOT INDEPENDENTLY QUALIFIED | Exact-version source and tests or other authorized verification evidence; deployment-specific consent policy |
| Payload allowlist / redaction | DOCUMENTED / NOT INDEPENDENTLY QUALIFIED | Exact-version source review, adversarial fixtures, and proof no prompt/body/secret/path leaks through telemetry |
| Trace exporter and span attributes | OPEN | Exact backend, data schema, processors, egress route, access and retention |
| Local conversation/event/completion-log retention | OPEN | Inventory of all files and copies; retention TTL; expiry/cleanup behavior; backup/cache treatment; deletion evidence |
| Secret encryption and key custody | PARTIAL | Runtime-only key injection; access separation; rotation/recovery semantics; evidence that logs/workspaces do not bypass encrypted storage |
| R-06 accountability and outage handling | OPEN | Filled, accepted disposition with accountable authority, independent security/privacy reviewers, sink outage, durability, reconciliation and retention decisions |
| Exact target manifest / runtime isolation | UNKNOWN / BLOCKED | Accepted runner/workspace/network manifest, filesystem mounts, privileges, egress allowlist, cleanup and recovery boundary |

## 4. Recommended admission disposition

1. Keep OpenHands Agent Server at **CANDIDATE / NOT SELECTED / NOT ADMITTED / RUNTIME-UNVERIFIED**.
2. If it remains under consideration, set completion logging off and telemetry exporter to `none` as the conservative proposed baseline; this is a design recommendation, not a claim that the exact candidate has been configured.
3. Do not pass user-domain data, production secrets or unsanitized prompts into the candidate. Use only approved synthetic/minimized engineering context until MH-13/R-06 and the target manifest permit otherwise.
4. Require explicit retention and deletion contracts for conversation metadata, event logs, completion logs, traces, workspace artifacts, backups and derived artifacts. “Local disk only” does not satisfy retention or deletion requirements.
5. Require session authentication, loopback/private binding or equivalent network isolation, dedicated ephemeral workspace, no ambient secret inheritance, and a documented outbound allowlist before any execution.
6. Preserve the established source pin `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`; next compare the 48-commit upstream delta for telemetry/completion logging, retention, deletion and secret handling. Separately obtain exact package/container digest and source-to-artifact binding before artifact admission; do not infer either from upstream `main`.
7. Keep implementation, installation, test execution, provider calls, credentials, runtime inspection and qualification behind their existing separate authorization gates.

## 5. Verification and disposition

- Read the official Agent Server README and relevant telemetry/event-service source pages for source discovery.
- Read the current `main` MH-13 governance reconstruction and governance-state artifacts by GitHub path; blob SHAs recorded above.
- No package was installed; no test or qualification was run; no provider/model call or credential was used; no workflow was dispatched; no runtime/host or infrastructure was inspected or changed; no merge, rebase or deployment occurred.
- **Disposition: PINNED-SOURCE REVIEW RECONCILED WITH PRIOR WAVES / 48-COMMIT CURRENT-HEAD DELTA IDENTIFIED / ARTIFACT PROVENANCE, R-06 AND TARGET GATES OPEN.**

Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
