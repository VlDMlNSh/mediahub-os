# MediaHub OS — Wave 382: autonomous queue task transition test

Date: 2026-10-22

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## User request
Test that the autonomous queue advances from one task to the next without a chat/operator decision.

## Live-run attempt and blocker
The existing Astra autonomous queue supervisor run [39806527991](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39806527991) remains queued. Its sole initial job [119921113939](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39806527991/job/119921113939) requires runner labels `self-hosted, linux, x64, mediahub-control`, hostname `mh-dev-01`, and user `mediahub-runner`. The queue's 24-hour workflow has the same canonical-runner requirement. The user has restricted operations to the third server (Voktors-Mini.Dlink), so starting a workflow that requires mh-dev-01 or dispatching the full three-node queue would violate the current operational boundary. No such dispatch was made.

Issue #301 expressly states that CAF-Q-001…CAF-Q-015 is documentary, not a live scheduler. The supervisor job is not executing and its run has no artifacts. Thus there is no live queue transition evidence from this attempt.

## Bounded test added
Added `test_autonomous_queue_switches_to_next_task_after_verified_completion` to `tests/test_autonomous_queue.py`.

The deterministic test creates two READY tasks assigned only to the third permanent lane (`Voktors-Mac-mini.local`) on one immutable target SHA. It runs the queue cycle three times with a deterministic remote-worker test double:
1. Cycle 1 selects `QUEUE-A`; worker result is recorded as VERIFIED for the target SHA.
2. Cycle 2 suppresses the completed `QUEUE-A` and selects `QUEUE-B`; its result is recorded VERIFIED for the same target SHA.
3. Cycle 3 reports `IDLE/no_ready_tasks`.

The test asserts the exact dispatch sequence `QUEUE-A, QUEUE-B`, target-bound completion evidence, and final IDLE. This validates queue selection/state-transition logic but **does not invoke Claude, dispatch a real remote worker, or prove live autonomous execution**.

## Verification
- Base SHA: `11d04d2f2687e9ba9215e4b67af2e450516960bb`.
- Working branch: `test/autonomous-queue-task-transition-wave382-20261022`.
- Test file commit: `ac9ed4069ac790a4a4c33957e71c2d0a88b565ef`.
- Test-file blob SHA after write: `bd5a7a53f6f4ecffada083426676df1b40b9d3ef`.
- Local test execution: NOT RUN.
- Exact-head CI and independent review: pending PR creation; until results are fetched, NOT VERIFIED.
- Live queue execution / real task switching: BLOCKED / NOT VERIFIED.
- No secrets accessed, no server commands executed, no workflow dispatch issued, no merge performed.

## Acceptance gates
1. Exact-head CI runs the new transition test and the full existing queue test suite.
2. Independent review confirms the test uses only a deterministic worker double and cannot dispatch external work.
3. A later live test must run only on an explicitly approved executor scope, produce two distinct task IDs with real worker run IDs and signed target-bound evidence, verify first task completion before second selection, and end with durable evidence. The current canonical supervisor cannot meet this boundary because it is pinned to mh-dev-01.

## Next step
Run PR CI and review this deterministic test. Separately design a governed third-server-only queue entry point before attempting a live worker transition; do not weaken canonical runner identity or launch the three-node supervisor to simulate success.
