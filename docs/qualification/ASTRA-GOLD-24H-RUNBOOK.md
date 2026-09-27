# Astra Gold — 24/7 launch and qualification runbook

## 1. Truth / current qualification state

The repository contains the core durable scheduler, generation fencing, recovery, GitHub execution qualification, Ollama E2E evidence, deterministic next-task generation, canonical GitHub Transport bootstrap, runtime identity health evidence, and process-manager launcher manifests.

The live three-node transport is **not yet qualified for Astra Gold**.

The blocking fact is operational: fresh commands delivered to `mh-dev-02` are executed by a persistent worker that still reports the legacy health schema. It does not expose `transport_version`, `agent_source_sha`, `pid`, `agent_path`, or `worktree`. Therefore the running process has not been proven to execute the canonical agent from the canonical synchronized worktree.

No 24-hour soak may be declared successful until this boundary is repaired and independently verified.

## 2. Rank — qualification priority

Priority is dependency order, not a quality ranking:

1. **P0 — Process identity and canonical bootstrap**
   - migrate one node to the canonical launcher;
   - obtain fresh health identity;
   - prove executable path and synchronized worktree;
   - prove source SHA equals canonical agent SHA.

2. **P0 — Runtime availability**
   - prove `mediahub_runtime` discovery on the migrated node;
   - prove local Ollama execution;
   - prove bounded coding task, tests, commit, push, and remote SHA.

3. **P0 — Durable autonomous loop**
   - connect scheduler/control-plane state to the persistent worker;
   - verify observe/reconcile/select/claim/isolate/execute/verify/record/commit/push/generate-next cycles after restart.

4. **P0 — Multi-node fencing**
   - prove unique ownership, stale lease rejection, duplicate prevention, and recovery across all three nodes.

5. **P1 — Recovery and backup**
   - crash/restart recovery;
   - backup/restore;
   - recovery drill with evidence.

6. **P1 — Provider/model qualification**
   - local Ollama baseline;
   - Gemini/cloud provider qualification only where authenticated and quota-safe;
   - record model/provider identity and evidence for every execution.

7. **P1 — Security and operational controls**
   - least privilege;
   - secret isolation;
   - protected branches;
   - audit/evidence integrity;
   - failure fencing.

8. **P1 — 24h soak**
   - continuous scheduler operation;
   - no duplicate terminal executions;
   - no unreconciled stale leases;
   - automatic next-task generation;
   - restart/recovery event;
   - evidence ledger completeness.

9. **P0 — Independent qualification**
   - fresh verification of the integrated system;
   - human authorization;
   - final evidence manifest and runbook.

## 3. Blueprint — execution sequence

### Phase A — single-node bootstrap

Target: `mh-dev-01`.

1. Deploy the Linux systemd launcher from `ops/systemd/mediahub-astra-github-bootstrap.service`.
2. Ensure the launcher seeds `/home/mediahub/astra-work` when absent.
3. Start the service through the canonical bootstrap.
4. Send read-only health through GitHub Transport.
5. Require:
   - `transport_version=self-reexec-v1`;
   - current `agent_source_sha`;
   - `agent_path` inside the synchronized worktree;
   - expected `worktree`;
   - stable PID during a bounded observation window.
6. Compare the reported source SHA with the canonical file SHA.
7. Reject qualification if any identity field is stale or missing.

### Phase B — runtime qualification

1. Execute a bounded coding task using the local Ollama model.
2. Verify generated files exactly.
3. Run the task's tests.
4. Verify worker commit SHA.
5. Verify remote SHA equals worker commit SHA.
6. Record artifact SHA256 and model identity.
7. Reject qualification on missing runtime, test failure, push mismatch, or incomplete evidence.

### Phase C — autonomous control loop

1. Start the production scheduler/control-plane service.
2. Create a deterministic task.
3. Observe it being selected and claimed.
4. Verify lease ownership and generation fencing.
5. Execute through GitHub Transport.
6. Verify and record evidence.
7. Commit and push.
8. Reconcile the new remote SHA.
9. Generate the next task from the fresh remote SHA.
10. Repeat for at least two changing cycles.
11. Restart the worker and verify recovery without duplicate next-task generation.

### Phase D — three-node qualification

Repeat the identity and runtime qualification on:

- `mh-dev-01`
- `mh-dev-02`
- `Voktors-Mini.Dlink`

Then execute a contention test in which two nodes cannot validly own the same fenced execution.

### Phase E — resilience

Perform, with evidence:

- worker crash/restart;
- scheduler restart;
- expired lease requeue;
- stale generation rejection;
- conflicting duplicate rejection;
- backup;
- restore;
- recovery drill.

### Phase F — provider/model matrix

For each provider/model actually available:

- provider;
- model;
- node;
- capability;
- latency/duration;
- success/failure;
- tests;
- commit SHA;
- remote SHA;
- artifact SHA256;
- quota/error information.

Local Ollama remains the baseline. Gemini should be added only through an already authenticated, supported integration; this runbook does not assume credentials or quota availability.

### Phase G — 24-hour soak

The soak starts only after all P0/P1 prerequisites are green.

Minimum evidence:

- start/end timestamps;
- scheduler cycles;
- task IDs;
- execution IDs;
- lease transitions;
- generated task IDs;
- commits and remote SHAs;
- model/provider identity;
- failures and retries;
- restart/recovery event;
- zero unresolved fencing violations;
- zero unexplained duplicate terminal executions;
- evidence ledger integrity.

### Phase H — GOLD authorization

GOLD requires all of:

- all P0 gates green;
- all required P1 resilience/security gates green;
- 24h soak complete;
- independent verification;
- backup/restore evidence;
- recovery drill evidence;
- multi-node fencing evidence;
- final evidence manifest;
- operator runbook;
- explicit human authorization.

## 4. Gaps

### Blocking now

- Persistent process manager on the nodes has not been migrated to the canonical launcher.
- Fresh live health still proves execution of the legacy worker copy.
- Runtime availability is not proven on all nodes.
- Production scheduler integration with the GitHub Transport worker is not yet demonstrated end-to-end.
- Three-node fencing is not freshly demonstrated.
- 24h soak has not started and must remain blocked.

### Not yet demonstrated

- restart/crash recovery of the integrated production loop;
- backup/restore on the current production state;
- recovery drill;
- provider/model matrix including Gemini;
- security qualification of the complete live deployment;
- independent GOLD verification.

### Non-blocking repository facts

The repository already contains substantial P0 scheduler and transport functionality and fresh historical evidence for scheduler, recovery, GitHub execution, and Ollama E2E. Historical evidence is retained as evidence but is not substituted for fresh live qualification.

## 5. Evidence rule

A gate is **PASS** only when fresh evidence directly exercises the current integrated system. Previous successful runs, source inspection, worker assertions, or a merged PR alone do not satisfy a live qualification gate.

A gate is **BLOCKED** when its prerequisite cannot be exercised without an unverified deployment boundary.

## 6. Definition of done

Astra is operationally GOLD only when the full loop is continuously executable:

`OBSERVE → RECONCILE → SELECT → CLAIM → ISOLATE → EXECUTE → VERIFY → RECORD → COMMIT → PUSH → RECONCILE → GENERATE_NEXT → OBSERVE`

and the system survives restart, stale work, duplicate delivery, multi-node contention, provider failure, backup/restore, and the complete 24-hour soak with complete evidence.
