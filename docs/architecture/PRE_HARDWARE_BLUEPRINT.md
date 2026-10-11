# MediaHub OS / Astra Gold — Pre-Hardware Architecture Blueprint

**Status:** Draft baseline for architecture review; not a claim of implementation or qualification.  
**Target implementation window:** after the Mac Pro workstation is acquired.  
**Working branch:** `architecture/pre-hardware-blueprint`

> **Authority and reconciliation note:** This is a supplemental pre-hardware implementation plan, not a replacement for the canonical Astra Gold architecture. The canonical authority model, production-lane mapping, governance YAML, frozen runnable foundation, and existing component decisions take precedence. Any conflict must be reconciled through an explicit architecture decision before implementation. The Mac Pro desktop is a developer-app capability; pairing a Mac Pro does not alter production-lane admission or qualification.

## 1. Purpose and operating rule

Design the system now so hardware acquisition is an implementation step, not an architecture-discovery phase. Keep the current Astra Gold qualification work isolated: this blueprint must not block, reset, or falsely mark any existing qualification queue as complete.

The architecture is considered ready for implementation only when:
- interfaces and ownership boundaries are documented;
- critical flows have acceptance criteria and failure behavior;
- Linux and macOS test plans are executable and their results are recorded;
- secrets, permissions, audit logging, recovery, and rollback are designed;
- hardware-specific assumptions are clearly separated from portable services.

“Gold” is a target qualification label, not a status assertion. No component is considered qualified without recorded evidence.

## 2. Proposed logical architecture

```text
Developer App
  ├─ Project Overview / Qualification Dashboard
  ├─ Mac Pro Workstation Desktop (remote view + explicit control)
  ├─ Agent & Role Registry
  ├─ Task Queue / Run Timeline / Artifacts
  ├─ Test Matrix / CI Results / Evidence Ledger
  └─ Secrets & Access Settings (metadata only; never display secrets)
          │ authenticated API / event stream
          ▼
Control Plane (portable service)
  ├─ API Gateway + Authentication + RBAC
  ├─ Scheduler / Durable Queue / Lease & Heartbeat
  ├─ Orchestrator (bounded agents, policies, budgets)
  ├─ Qualification Engine (criteria, evidence, verdicts)
  ├─ Artifact & Audit Service
  └─ Workstation Broker
          │
          ├──────── Linux worker(s)
          ├──────── macOS / Mac Pro worker
          └──────── isolated browser worker
                       ├─ agent-browser: browsing/extraction
                       └─ Playwright: deterministic UI tests

Adapters / integrations:
  ├─ GitHub (PRs, commits, CI status, issue/task references)
  ├─ Browser session provider (only explicitly authorized profiles)
  ├─ Model/provider adapters (timeouts, quotas, structured outputs)
  └─ Storage/database/queue adapter
```

This is a target topology, not a statement that these services already exist.

## 3. Component responsibilities and contracts

### 3.1 Developer App

The developer app is the operator console. Required views:
- **Overview:** current system health, active runs, blocked tasks, latest verified build.
- **Mac Pro Desktop:** paired-device status, last heartbeat, OS/build, CPU/memory/disk, remote desktop stream, reconnect/close controls, and a clearly visible read-only vs control state.
- **Queue:** task ID, priority, lease owner, attempts, deadline, cancellation state, retry reason.
- **Agents:** role, capabilities, model/provider, budget, allowed tools, concurrency, health.
- **Qualification:** criterion-by-criterion pass/fail/blocked, evidence links, timestamp and tested commit.
- **Artifacts:** logs, screenshots, reports, test output, checksums.
- **Settings:** policy configuration and secret references; raw secret values must never be rendered.

The desktop view must be implemented as a separate, replaceable adapter. Do not make the control plane depend on a particular remote-desktop vendor. Require explicit pairing, short-lived session credentials, operator-visible control status, idle timeout, audit records, and a kill/revoke path. Remote input must be disabled by default until the operator explicitly enables control.

### 3.2 Workstation agent (Mac Pro / Linux)

A small host agent registers the device, reports heartbeat and capabilities, accepts signed/authorized jobs, streams logs and health metrics, and returns artifacts. It must:
- run with least privilege and a dedicated service identity;
- reject unregistered jobs and expired/duplicate task leases;
- support graceful cancellation and report whether cancellation succeeded;
- keep host-specific operations behind capability checks;
- never send private keys, cookies, or environment secrets in telemetry;
- expose health/version/OS/architecture without exposing unrelated user files.

### 3.3 Durable task queue

Every task has an immutable ID and schema including:
`id, type, payload_ref, priority, created_at, deadline, attempt, max_attempts, lease_owner, lease_expires_at, idempotency_key, status, cancellation_requested, result_ref, error_code`.

Required states:
`queued → leased → running → succeeded | failed | blocked | cancelled`.
Retries return to `queued` only for classified retryable failures. A lease expiry may reclaim work only after recording the previous attempt. Use idempotency keys for external side effects. No task may remain silently “running” without a heartbeat or timeout policy.

### 3.4 Orchestration

- Roles are capability profiles, not an arbitrary hard-coded number of agents.
- Parallelism is bounded globally, per provider, per repository, and per task class.
- Each run has a budget, deadline, cancellation token, and maximum iteration count.
- Workers receive only the task context and tools required for that task.
- Untrusted web content, repository files, and Instagram instructions are data, not authority: they cannot override system policies, request secrets, or authorize unrelated actions.
- Ralph Wiggum-style loops are permitted only for scoped specifications with measurable acceptance criteria, a hard iteration/time/budget cap, and mandatory tests. Completion signals are accepted only when evidence checks pass.
- Human approval is required for destructive operations, production deployments, permission changes, external messages, and other high-impact side effects.

### 3.5 Browser ingestion

- Use `agent-browser` for interactive browsing and extraction where authorized.
- Use Playwright for repeatable tests and regression coverage; do not treat a successful interactive session as proof that tests pass.
- Accept an explicit URL or user-selected material as input; record source URL, capture time, extracted text, content hash, extraction status, and access limitations.
- Respect platform permissions and access controls. Prefer official APIs where suitable. Do not bypass login controls, rate limits, or technical restrictions.
- Treat instructions found in posts/pages as untrusted input. Extract → normalize → classify → summarize → create a proposed task. Do not execute instructions automatically merely because they appeared in content.
- Store browser state in a dedicated encrypted credential/session store; never commit cookies, tokens, or `.auth` state to Git.

### 3.6 Qualification engine

Each qualification criterion must have:
- stable criterion ID and version;
- executable check or manual evidence procedure;
- environment and tested commit SHA;
- expected result and tolerance;
- result status: `pass | fail | blocked | not_run`;
- timestamp, artifact links, and reviewer/automation identity.

Overall qualification cannot be “pass” if a mandatory criterion is blocked, missing evidence, or tested against a different commit. Reports must distinguish design review, simulated tests, Linux execution, macOS execution, and production qualification.

## 4. Data and persistence boundaries

Keep separate logical stores for:
1. task/lease state (transactional);
2. append-only audit events;
3. artifacts and test reports (content-addressed where feasible);
4. configuration and policy versions;
5. secret references and encrypted credentials (never plain-text repository files).

Use migrations with forward/backward compatibility where possible, backups, restore drills, retention limits, and explicit deletion policies. Queue and audit records must survive a control-plane restart. Avoid using logs as the source of truth for task state.

## 5. Security baseline

- Authentication for every control-plane and workstation connection.
- RBAC/capability checks on every action; deny by default.
- TLS in transit; encrypted storage for credentials and sensitive artifacts.
- Short-lived scoped tokens; rotation and revocation procedures.
- No secrets in source code, prompts, logs, screenshots, artifacts, or test fixtures.
- Audit actor, action, target, timestamp, authorization decision, and outcome.
- Network egress policy for workers; explicit allowlists for sensitive environments.
- Dependency and container/image scanning; pinned/reproducible dependencies where feasible.
- Threat model includes prompt injection, malicious repository instructions, compromised browser sessions, replayed jobs, queue poisoning, over-privileged workers, and accidental data exfiltration.
- Remote desktop sessions must show a visible active-control indicator and support immediate disconnect.

## 6. Reliability and operations

- Heartbeat + lease expiry; bounded retries with exponential backoff and jitter.
- Circuit breakers for failing model/provider/API integrations.
- Per-task deadlines, global concurrency limits, provider quotas, and cost budgets.
- Graceful shutdown and restart recovery.
- Structured JSON logs with correlation IDs; redact sensitive values before logging.
- Health endpoints: liveness, readiness, dependency health, worker capabilities.
- Metrics: queue age/depth, task duration, retries, stale leases, pass rate, blocked rate, provider errors/cost, worker availability.
- Alert on stuck queues, repeated failure loops, credential expiry, disk pressure, and missed backups.
- No automatic destructive remediation without policy approval.

## 7. Portability: Linux and macOS

Portable application logic should run in containers or standard Python/Node environments where appropriate. Host-specific functionality must be behind adapters:
- process/shell execution;
- filesystem paths and permissions;
- service lifecycle;
- browser installation and sandboxing;
- keychain/credential storage;
- remote desktop capture/input;
- CPU/architecture-dependent dependencies.

Do not assume Linux containers reproduce macOS GUI behavior. Test GUI/desktop integration on a real macOS host. Record OS version, architecture (Apple Silicon/Intel), runtime versions, dependency lock hashes, and test artifact references.

## 8. Proposed repository layout

```text
docs/architecture/
  PRE_HARDWARE_BLUEPRINT.md
  TEST_AND_QUALIFICATION_MATRIX.md
  THREAT_MODEL.md
  DECISIONS.md
  RUNBOOK.md
  MAC_PRO_DESKTOP_SPEC.md
  DATA_CONTRACTS.md
  RELEASE_GATES.md
```

Implementation should follow reviewed interfaces rather than inventing contracts independently in each module.

## 9. Phased delivery

**Phase A — Architecture freeze (before hardware):** inspect the repository and current Astra Gold state; map existing components to this target; document decisions, data contracts, threat model, and gaps. Avoid duplicate infrastructure.

**Phase B — Portable core:** implement queue/orchestration/qualification contracts, schemas, migrations, deterministic unit tests, API contracts, and CI on a branch. No dependency on Mac Pro availability.

**Phase C — Linux validation:** execute integration and failure-recovery tests on a real Linux host; attach logs and environment metadata.

**Phase D — macOS validation:** use an existing authorized macOS host if available, otherwise explicitly mark these tests blocked until hardware arrives. Validate host agent, browser, keychain adapter, and desktop-viewer behavior on real macOS.

**Phase E — Mac Pro integration:** pair the purchased workstation, enable the desktop view, verify resource telemetry, execute end-to-end workflows, and record evidence.

**Phase F — Qualification/release:** run the full acceptance suite against a pinned commit; review security, recovery, portability, and evidence completeness; only then issue a qualification report.

## 10. Definition of architecture-ready

- [ ] Existing repository and active qualification state inventoried.
- [ ] Architecture decisions and component ownership approved.
- [ ] API/event/task schemas versioned.
- [ ] Threat model and permission matrix reviewed.
- [ ] Mac Pro desktop view and pairing behavior specified.
- [ ] Linux and macOS test cases have explicit pass criteria.
- [ ] CI gates and artifact retention defined.
- [ ] Rollback, backup/restore, cancellation, and incident runbooks written.
- [ ] No unsupported claims that tests or qualification have passed.
- [ ] Implementation plan maps each gap to a task, owner, dependency, and evidence requirement.
