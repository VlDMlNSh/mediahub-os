# Linux / macOS Test and Qualification Matrix

**Status:** Planned tests; no pass is implied until an execution artifact is attached.  
**Applies to:** MediaHub OS, Astra Gold orchestration, workstation agent, browser ingestion, developer-app Mac Pro desktop.

## Result vocabulary

- `PASS`: test ran against a pinned commit in the named environment and all assertions passed.
- `FAIL`: test ran and one or more assertions failed.
- `BLOCKED`: environment, permission, hardware, or dependency unavailable.
- `NOT RUN`: no execution attempted.
- `NOT APPLICABLE`: justified by an approved architecture decision.

Every result must include commit SHA, environment metadata, command/test ID, timestamp, exit status, and artifact link/checksum.

## Test matrix

| ID | Area | Test / acceptance criterion | Linux | macOS | Evidence |
|---|---|---|---|---|---|
| ARC-001 | Architecture | Component inventory maps current code to target boundaries; gaps have owners | Planned | Planned | Inventory + decision log |
| API-001 | Contracts | API schemas validate good and malformed requests; unknown fields follow documented policy | Planned | Planned | Test report |
| QUEUE-001 | Queue | Concurrent workers cannot own the same unexpired lease | Planned | Planned | Race test log |
| QUEUE-002 | Recovery | Worker killed mid-task; lease expires and task recovers without duplicate side effects | Planned | Planned | Event trace |
| QUEUE-003 | Idempotency | Retried task with same idempotency key does not duplicate an external side effect | Planned | Planned | Fake-adapter assertions |
| QUEUE-004 | Cancellation | Cancellation is acknowledged, persisted, and distinguished from success | Planned | Planned | Run timeline |
| ORCH-001 | Orchestration | Global/provider/task concurrency caps are enforced under load | Planned | Planned | Load report |
| ORCH-002 | Budgets | Deadline, iteration cap, and cost budget stop the loop deterministically | Planned | Planned | Run log |
| ORCH-003 | Prompt injection | Untrusted page/repo content cannot change policy, reveal secrets, or trigger unauthorized tools | Planned | Planned | Adversarial fixtures |
| QUAL-001 | Qualification | Missing or stale evidence cannot produce overall PASS | Planned | Planned | Unit tests |
| QUAL-002 | Qualification | Report binds every result to one exact commit and environment | Planned | Planned | Sample report |
| SEC-001 | Access control | Unauthenticated and unauthorized operations are denied by default | Planned | Planned | Security test output |
| SEC-002 | Secrets | Secret canaries do not appear in logs, artifacts, screenshots, or exception messages | Planned | Planned | Redaction scan |
| SEC-003 | Replay | Expired/replayed job credentials and duplicate job submissions are rejected or idempotently handled | Planned | Planned | Security test output |
| SEC-004 | Audit | Every privileged action records actor, target, decision, time, and outcome | Planned | Planned | Audit query/export |
| STORE-001 | Persistence | Control-plane restart preserves queued/running recovery state and audit history | Planned | Planned | Restart test |
| STORE-002 | Backup | Backup restore reproduces task/config state within documented RPO/RTO | Planned | Planned | Restore report |
| OPS-001 | Observability | Logs include correlation IDs and redact secrets; metrics expose queue age and stale leases | Planned | Planned | Logs/metrics snapshot |
| HOST-001 | Host agent | Agent reports OS/architecture/runtime and rejects unsupported capabilities safely | Planned | Planned | Host diagnostics |
| HOST-002 | Host agent | Graceful stop and forced termination produce distinct final states | Planned | Planned | Process/run log |
| BROW-001 | Browser | Authorized public or user-selected URL extraction records source, timestamp, hash, and extraction status | Planned | Planned | Fixture + output |
| BROW-002 | Browser | Login-required content fails clearly when no authorized session exists; no control bypass | Planned | Planned | Negative test |
| BROW-003 | Browser | Playwright regression flow is repeatable and produces trace/screenshots on failure | Planned | Planned | Trace artifact |
| DESK-001 | Desktop UI | Paired Mac Pro status, heartbeat, OS/build and health are visible in developer app | N/A or Linux agent test | Blocked until Mac host available | Screenshot + telemetry |
| DESK-002 | Desktop UI | Read-only is default; explicit enable shows active-control indicator; disconnect revokes session | Planned on compatible host | Blocked until Mac host available | Video/screenshot + audit |
| DESK-003 | Desktop UI | Reconnect, stale session, lost network and expired token states are handled safely | Planned | Blocked until Mac host available | E2E run |
| PORT-001 | Portability | Dependency lock/install/build/test succeeds on supported Linux versions | Planned | Planned | CI matrix |
| PORT-002 | Portability | macOS filesystem paths, permissions, keychain integration and browser installation are validated | N/A | Blocked until suitable macOS host | CI/manual report |
| E2E-001 | End-to-end | URL → extraction → proposal → approval → task queue → bounded run → tests → evidence report | Planned | Planned | End-to-end report |
| E2E-002 | End-to-end | Provider outage, database outage and worker crash recover without silent task loss | Planned | Planned | Fault-injection report |

## Environment capture

For every execution record:
- OS name/version/build, architecture, CPU and memory;
- shell, Python/Node versions, package-manager version;
- dependency lockfile hash and browser version;
- repository commit SHA and dirty/clean state;
- exact command and selected test IDs;
- start/end timestamps, exit code, stdout/stderr artifact;
- relevant configuration version with all secrets redacted.

## CI gating policy

1. Pull requests: formatting/lint, type checks, unit tests, schema checks, secret scan, dependency scan.
2. Main branch: all PR gates plus integration tests and migration checks.
3. Release candidate: Linux and macOS matrix, recovery/fault tests, security regression suite, E2E tests, artifact completeness.
4. Qualification: all mandatory criteria PASS on the exact release commit; BLOCKED/NOT RUN cannot be silently counted as PASS.
5. A platform unavailable in CI remains BLOCKED and must be called out in the release report.

## Required failure-injection scenarios

- Kill worker after lease acquisition and after side effect but before acknowledgement.
- Restart control plane while tasks are queued and running.
- Expire a lease while a worker is paused.
- Return 429, timeout, malformed response, and provider outage.
- Fill disk and simulate artifact-store unavailability.
- Revoke a browser session during extraction.
- Submit malicious web content that requests secret disclosure or unauthorized action.
- Lose desktop connection during a remote-control session.
- Reuse an expired or revoked workstation token.

## Completion rule

This matrix is a plan until populated with real results. Simulated tests and mocked macOS tests must be labeled as such and never substituted for execution on real Linux/macOS hosts.
