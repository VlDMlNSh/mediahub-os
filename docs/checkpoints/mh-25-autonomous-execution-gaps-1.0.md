# MH-25 — Autonomous Execution Gap Register 1.0

Status: LIVE — NO FALSE CLOSURE

Current execution HEAD: `a26d561051976baee2797b47018a83ee6fbd7adf`
Seeded READY task: `ops/agent-fabric/tasks/MH25-QUEUE-001.json`

## First 24h queue test
- Workflow: `.github/workflows/mh25-first-24h-autonomous-queue.yml`
- Activation commit: `6abda158653411f71330b8cd9db1eaaf7a75f7e6`
- Trigger: push path activation; manual dispatch also available.
- Activation commit for the current test: `a26d561051976baee2797b47018a83ee6fbd7adf`.
- Queue seed task: `MH25-QUEUE-001` (READY; test-only bounded surface).
- Intended role: real bounded queue soak, not G0-G9 promotion.
- Run acceptance remains evidence-based; a GitHub workflow being triggered does not equal PASS.
Date: 2026-10-01

| Gate | Status | Evidence / blocker |
|---|---|---|
| G0 worker identity | BLOCKED | Canonical runtime identity has not received fresh independent execution evidence. |
| G1 task/claim contract | PASS — CI | Agent Fabric unit + collision/lease simulation PASS in GitHub Actions run 36921358617 on SHA de281aa4d28c05565f7be84ed59b2150dcf947ad; independent canonical-node runtime verification remains pending. |
| G2 worker E2E | BLOCKED | No fresh canonical-node E2E evidence for current Agent Fabric HEAD. |
| G3 scheduler E2E | BLOCKED | No fresh scheduler E2E evidence for current HEAD. |
| G4 fencing | BLOCKED | Requires multi-node executable evidence. |
| G5 recovery/restore | BLOCKED | Requires executable interruption/restore evidence. |
| G6 fresh qualification | BLOCKED/SCOPED | Required per target-gated runtime/provider; not a blanket Agent Fabric pass. |
| G7 3-node | BLOCKED | SentinelX Free plan exposes one active host; three connected hosts cannot simultaneously execute. |
| G8 GOLD 24h | RUNNING — HISTORICAL SHA | Run #178 / 36872925703 started on ba8eb4a902f7935b33a7fcb6dd8ea927f67670c0; it does not qualify current Agent Fabric changes. A new current-HEAD GOLD is forbidden until G0-G7 pass. |
| G9 independent verification | BLOCKED | Must run after a current-SHA GOLD and inspect evidence independently. |

## Current executable evidence
- Agent Fabric tests: PASS in GitHub Actions run 36920261809, but that run failed only at architecture invariant path checking.
- Manifest validation: PASS in run 36920920287; same run failed at invariant assertion because the referenced text anchors were incorrect.
- The invariant check was subsequently corrected.
- Current workflow fixes are committed; a fresh PASS for the latest HEAD is still required.
- Queue engine is now present at `runtime/mediahub_runtime/autonomous_queue.py`; it uses ClaimStore, bounded A2 builder execution, independent read-only A3 verification, task branches, and evidence. No automatic merge to main.
- SentinelX cannot provide a stable active execution slot for mh-dev-01 under the current Free-plan 1-active-host limit.

## No-go conditions
Do not close G0-G9 from implementation commits, PR existence, historical GOLD, or worker assertions.

## Promotion condition
AUTONOMOUS_DEVELOPMENT = ENABLED only after every gate G0-G9 has fresh PASS evidence tied to one exact HEAD and independently verified evidence bundle.


## SentinelX execution pass — 2026-10-01
- Host mh-dev-01 is connected and pingable.
- SentinelX reports Free plan limit=1; host is currently parked/non-operational from the plan perspective despite zero active hosts being reported.
- SentinelX agent is 0.19.3; mediahub-astra.service is installed but reported inactive (dead).
- Service unit runs as mediahub from /opt/mediahub/astra; SentinelX operator identity is sentinelx, which cannot read /home/mediahub/mediahub-os due Unix permissions.
- Attempted service restart was accepted by SentinelX, but subsequent service status remained inactive; therefore no fresh worker-running evidence was obtained.
- The canonical GitHub repo remains the authoritative source for queue code; SentinelX did not provide valid evidence of the first 24h runner execution.
- No G0/G2/G3/G4/G5/G7/G8/G9 promotion is permitted from this pass.
