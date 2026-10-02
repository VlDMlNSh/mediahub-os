# ASTRA GOLD — 24H AUTONOMOUS DEVELOPMENT BLUEPRINT

Status: execution blueprint; does not grant GOLD or launch authority.

## 1. Objective

Establish a fail-closed MediaHub development loop in which ASTRA:

1. receives bounded work through the GitHub transport;
2. reconciles the exact source SHA before execution;
3. claims disjoint work with a shared coordination authority;
4. executes only admitted operations/providers;
5. publishes immutable, provenance-bound evidence;
6. recovers from timeout, worker restart, stale claim, transport interruption and replay;
7. runs continuous development only while the canonical worker and all required gates remain healthy;
8. never self-promotes to GOLD and never bypasses provider credentials, GitHub permissions, runner admission or platform quotas.

## 2. Control-plane topology

ChatGPT session
  -> GitHub repository / control plane
  -> control/commands/<node>.json
  -> canonical ASTRA GitHub worker
  -> bounded executor / qualification backend
  -> control/results/<node>.json
  -> GitHub evidence / branch
  -> verification and gate reducers
  -> next queued task

The chat is an operator/control surface, not a hidden always-on process. A chat turn cannot itself remain alive for 24 hours.

## 3. 24/7 development loop

### Phase A — identity and boundary

- exact repository and branch identity;
- exact target SHA;
- canonical worker identity;
- clean worktree;
- node identity;
- no credentials in repository/evidence;
- no destructive Git operations.

### Phase B — execution admission

- task exists in the queue;
- owned paths are explicit;
- claim is disjoint from active claims;
- shared surfaces are serialized;
- provider/model identity is resolved;
- unresolved credentials cause BLOCKED, not fallback fabrication.

### Phase C — implementation

- bounded task execution;
- one active writer per shared boundary;
- ephemeral verification workspaces;
- ordinary Git push only;
- no force push/history rewrite;
- tests required for material changes.

### Phase D — verification

- fresh CI;
- source SHA equals tested SHA;
- evidence integrity verified;
- independent verifier for A3;
- failed gate stops promotion.

### Phase E — recovery

The loop must tolerate and record:

- executor timeout;
- executor failure;
- transport interruption;
- stale claim;
- worker restart;
- duplicate controller;
- replay;
- publication/reconciliation failure.

Recovery is diagnostic/reconciliatory and must not silently re-execute a published command.

### Phase F — soak

G9 is a mandatory uninterrupted 24-hour soak after G4/G5/G6/G7/G8 pass. It cannot be shortened to prove GOLD.

### Phase G — launch

G10 may become LAUNCH_READY only after all required fresh evidence is present. G11 requires explicit human authorization. ASTRA cannot authorize itself.

## 4. Qualification order

G0_IDENTITY
-> G1_BOUNDARY
-> G2_CONTROL_PLANE
-> G3_EXECUTION_PATH
-> G4_23_WAVE_QUALIFICATION
-> G5_CONCURRENCY
-> G6_RECOVERY
-> G7_INTEGRATED_A3
-> G8_PRE_SOAK
-> G9_24H_SOAK
-> G10_LAUNCH_READY
-> G11_LAUNCH

G4 remains 23 fresh rounds for each of five mandatory paths = 115 observations.

## 5. Current execution blockers

The last physical G4 evidence is bound to source SHA 70e60da17fd94f65d00fdaf4679866d5d61ec0cc and contains 115 observations but zero PASS observations. Therefore G4 is BLOCKED and downstream gates cannot be represented as passed.

Observed classes include:

- FCC transport/authentication failure;
- OmniRoute provider credential/authentication failure;
- Claude Code direct login absence;
- Codex/FCC timeout/reconnect.

No credential may be inferred, generated or bypassed by ASTRA.

## 6. FreeLLMAPI

FreeLLMAPI may be treated as a candidate local gateway only. Installation/running status is not qualification. Provider/model admission requires fresh evidence preserving upstream provider identity and credential isolation.

Qwen3.8 is not added to the mandatory G4 matrix retroactively. A separate fresh qualification is required if it becomes an admitted candidate.

## 7. 24/7 operational constraints

"24/7" means continuous availability of the worker and queue, not unlimited external compute or API access.

The system remains subject to:

- GitHub API and Actions limits;
- self-hosted runner availability;
- upstream provider rate limits and credentials;
- local CPU/RAM/storage/network capacity;
- model/provider availability;
- ChatGPT/tool-session limits.

No design may claim "without limits" by bypassing or evading those controls.

## 8. Activation boundary

The repository can prepare and verify the complete control plane through GitHub Transport. Starting/enabling a physical daemon on a host is a separate machine-side action. If the canonical runner is not already active, GitHub-only changes cannot truthfully be reported as having started the physical worker.

Desktop is therefore excluded from ordinary development and qualification work. It is permitted only when a physical host action is strictly impossible through the GitHub transport.

## 9. Required final evidence bundle

A real GOLD claim requires, at minimum:

- G0-G8 fresh evidence;
- exact source SHA binding;
- G4 115/115 PASS;
- G5 concurrency evidence;
- G6 recovery evidence;
- independent G7/A3 evidence;
- G8 pre-soak PASS;
- uninterrupted G9 24h soak PASS;
- G10 launch-ready reducer output;
- explicit human G11 authorization.

Until all are present, the state is NOT_PROVEN/BLOCKED.

## 10. Execution rule for future /continue turns

On each continuation:

1. read current GitHub branch/PR tip;
2. read current CI and qualification evidence;
3. classify blockers;
4. fix the smallest safe blocker through GitHub Transport;
5. commit;
6. verify fresh CI/evidence;
7. enqueue only the next admissible task;
8. never reuse stale PASS evidence;
9. never claim physical execution unless fresh physical evidence exists.

This document is an operational blueprint, not a qualification result.
