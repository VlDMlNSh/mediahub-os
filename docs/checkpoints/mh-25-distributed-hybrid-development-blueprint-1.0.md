# MH-25 — Distributed Hybrid Development Blueprint 1.0

Status: EXECUTION BLUEPRINT / QUALIFICATION GATED
Scope: four GitHub agents + two local executors

## Target topology

A0 Astra — coordinator/control-plane owner
A1 Architect — architecture/contracts
A2 Builder — bounded implementation
A3 Verifier — independent verification

Local executor backends:
- CODEX_LOCAL
- CLAUDE_LOCAL

GitHub is the durable task/evidence/control transport. Local execution occurs only on qualified execution nodes.

## Control chain

TASK -> CLAIM -> DISPATCH -> WORKER -> EXECUTE -> RESULT -> A3 VERIFY -> EVIDENCE -> COMMIT -> PUSH -> GENERATE_NEXT

No stage may silently bypass a previous stage.

## Four-agent responsibilities

A0:
- observe durable state
- reconcile stale claims
- select eligible tasks
- acquire/renew/release claims
- dispatch bounded workers
- enforce provider/workspace/target-SHA fencing
- never act as production authority

A1:
- architecture, contracts, dependency qualification
- no unassigned production writes

A2:
- bounded implementation in isolated worktree
- exactly one owned claim
- no shared-surface concurrent writes

A3:
- independent read-only verification
- validates result, tests, diff, target SHA, evidence
- cannot self-approve A2 output

## Two local executors

CODEX_LOCAL:
- command identity: codex
- env override: MEDIAHUB_CODEX_EXECUTOR

CLAUDE_LOCAL:
- command identity: claude
- env override: MEDIAHUB_CLAUDE_EXECUTOR

Provider adapters are executor-only. They do not own MediaHub state, identity, policy, recovery, release, or authority.

## Workspace model

Every local execution receives:
- unique task id
- unique claim id
- isolated worktree
- exact target SHA
- provider identity
- owner identity
- lease generation
- timeout
- bounded output/result path

Shared contracts, generated files, release metadata and authority surfaces are serialized.

## GitHub Transport operations

START(provider, task_id, target_sha)
STOP(task_id, generation)
STATUS(task_id)
RECONCILE(task_id)
RUN(task_id, provider)
VERIFY(task_id)
CANCEL(task_id)

All operations are durable intents. No secret is placed in a GitHub task.

## Required provider result

A result must contain:
task_id
claim_id
owner_id
generation
target_sha
provider
workspace
started_at
finished_at
exit_status
result_status
changed_files
commit_sha
verification_ref
evidence_ref

Result is rejected if any fencing identity is stale or inconsistent.

## Four-agent scheduling

Default active budget:
- A0: 1 coordinator
- A1: max 1 architecture claim
- A2: max 2 bounded builders
- A3: 1 verifier

Local providers:
- max 2 total
- only disjoint claims
- one provider process per isolated workspace

A2 may use CODEX_LOCAL or CLAUDE_LOCAL. Provider selection is policy-driven and allowlisted; it is never inferred from model names.

## Qualification sequence

D1 identity
D2 provider executable and successful non-interactive probe
D3 isolated worktree execution
D4 simultaneous disjoint claims
D5 timeout/failure/process cleanup
D6 result contract
D7 A3 independent verification
D8 durable GitHub evidence
D9 controller/provider restart and recovery
D10 exact-SHA qualification

Only after D1-D10:
- single-node autonomous cycles
- multi-node qualification
- two consecutive autonomous cycles
- negative/recovery suite
- exact-SHA 24h GOLD soak
- independent G9 verification

## Hard fences

- no credential creation/exposure
- no authentication bypass
- no quota bypass
- no force-push
- no rebase/reset/history rewrite
- no stale-SHA execution
- no duplicate active owner
- no merge before independent verification
- no GOLD from historical SHA
- fail closed on ambiguous critical state

## Current blockers

1. Claude local CLI reaches provider but fresh probe returns HTTP 403 security-policy denial.
2. Codex CLI is installed but successful non-interactive marker execution has not yet been independently evidenced.
3. Dual provider dispatch through the production Astra path is not yet proven.
4. Therefore D3-D10 remain gated.

## Completion definition

The system is complete only when both local providers execute two disjoint tasks concurrently through Astra, both results are independently verified, failure/recovery paths pass, and the exact qualified SHA completes the GOLD soak.
