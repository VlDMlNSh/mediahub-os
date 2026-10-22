# Wave 348 — revised remaining effort estimate after repository-wide evidence reconciliation

- Date: 2026-10-22
- Status: **PARTIALLY IMPLEMENTED / LIVE AGENT BATCH NOT VERIFIED / LOCAL ROUTE NOT QUALIFIED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Current controller: [gemini-batch-dispatch-controller.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml)
- Current test PR: [#437](https://github.com/VlDMlNSh/mediahub-os/pull/437)
- Docs/evidence PR: [#441](https://github.com/VlDMlNSh/mediahub-os/pull/441)

## Correction to Wave 346

The prior 12–25 hour estimate was too conservative as a remaining-effort estimate. It treated controller implementation, CI harness and recurring bridge as if they were largely unbuilt, and added worst-case maxima across independent work packages. That double-counted work already evidenced in repository history. It also conflated elapsed time waiting for independent review/host reconnection with active engineering hours.

The estimate is superseded by this Wave 348 assessment. Historical work is not re-labelled as current runtime qualification: the evidence below reduces remaining implementation effort, but does not claim the present end-to-end cycle has passed.

## Reconciled evidence already present

1. **Controller transport and bridge are implemented on main.** Current controller source was read at blob SHA 9453403bba899a2400ee3fb874d32badd034c704. It has a safe default probe, explicit agents + confirm=yes, an owner-only exact /next Issue #301 bridge, a batch admission flag, one immutable target SHA, three fixed child workflow roles, HMAC-signed child inputs, per-child correlation IDs, ambiguous dispatch reconciliation, duplicate-comment suppression and terminal child monitoring.
2. **Candidate controller CI and no-launch probe previously passed.** Wave 317/318 evidence records five successful exact-head runs on candidate PR #432 head 269b57b8b9c412261c97c4811bd49cbb4122ba03: contract validation [39647070718](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070718), controller PR probe [39647070682](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070682), Astra Verify [39647070683](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070683), Cloud Runtime Validation [39647070609](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070609), caller-context probe [39647070781](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070781). These were candidate/negative-path checks; the agent-dispatch job was skipped.
3. **The chat-to-GitHub event layer was exercised.** Wave 318 records issue-comment run [39647870697](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647870697) for an owner-authored comment that did not match /astra; the existing workflow skipped. This confirms comment creation can produce an issue_comment event, but it is not proof that the exact /next controller path dispatched children.
4. **Three separate Gemini workflows have historical successful execution evidence.** Wave 213 records Agent 1 run [39370191589](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370191589), Agent 2 [39370202615](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370202615), and Agent 3 [39370217605](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370217605), with successful validators on source SHA 25033753415fcbecdc7b2fe53085ed1bf2e4b8b4. This proves historical child workflows can execute; it is not a current batch run correlated to the present controller.
5. **The HMAC test repair is narrowly scoped.** PR #437 changes only the contract-validation workflow and two test files (124 additions, 5 deletions). The current validation workflow on main already runs the transport-contract suite and includes its own workflow path filter. PR #437 adds the child signed-dispatch runtime test to that filter and adds a test step. Its goal is to fix syntax/fixture defects and execute child authorization tests, not redesign the controller.
6. **Local host access has partially recovered.** SentinelX ping and capability summary succeeded for host host_5f7264034bdf0b51, hostname Voktors-Mini.Dlink. A read-only command confirmed macOS ARM64 and /opt/homebrew/bin/ollama client version 0.34.4, but the Ollama server was not running/reachable. claude and agent-browser were not found on PATH. This is a short preflight gap, not evidence that the entire local executor needs to be built from scratch.

## Current gaps that still count

- PR #437 exact-head status/run endpoints and formal review endpoint currently return empty results. Therefore its current head e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14 remains CI/review NOT VERIFIED by current connected evidence.
- PR #441 is documentation-only and remains open; current exact-head status/review are also not verified. It is not itself a runtime blocker if its docs are not being merged into main, but its evidence must not be mistaken for acceptance.
- The trusted-main positive no-secret probe and the current controller's actual owner /next → controller → three-child path have not been evidenced as a successful end-to-end run.
- The current run must capture controller run ID, three child run IDs, terminal conclusions, outputs/artifact digests and useful-work evidence.
- The local Ollama/Claude executor has not completed a bounded task. The approved non-paid route, executable/route identity, browser and paid-fallback denial still need qualification.
- The controller's own pull_request.paths excludes the PR #437 test-only paths, but the dedicated contract-validation workflow separately filters the workflow/test paths. Treat this as a visibility/coverage consideration, not by itself proof that all CI is bypassed. The decisive check is the dedicated contract workflow on the exact PR head.

## Revised effort estimate (active engineering time)

| Remaining work | Base estimate | Why |
|---|---:|---|
| Reconcile PR #437 exact-head CI, repair any remaining narrow test issue, obtain substantive independent security review | 0.5–1.5 h | Small 3-file test/CI change; controller architecture is already implemented |
| Run the safe trusted-main probe and verify actual trigger/governance/token behavior without exposing credentials | 0.5–1 h | Probe and bridge code exist; work is runtime evidence and any small fix |
| First current controller-owned Gemini batch, monitor three children and verify output/artifact provenance | 0.5–1.5 h | Child workflows exist and have historical success; current correlation and result acceptance are missing |
| Restore/qualify local Ollama/Claude route and prove one bounded task with no paid fallback | 1–2 h | Host responds, binary exists; daemon/route/CLI and browser still unverified |
| Final end-to-end repeatability, regression evidence and documentation read-back | 0.5–1 h | Bridge/controller/reporting patterns already exist |
| **Expected remaining active effort** | **3–6 h** | Assumes no new architectural defect and prompt access/review |

**Contingency:** budget **6–10 active hours** if current HMAC tests fail again, token permissions or the trusted-main probe require a source change, or the local executor requires installation/routing repairs. The earlier 25-hour upper bound is not supported as the central estimate by current evidence.

**Calendar elapsed time:** likely **0.5–2 working days**, depending primarily on review latency, GitHub Actions availability, and SentinelX/route stability. This is distinct from hands-on hours.

**After acceptance:** target **5–10 minutes of orchestration and triage per /next**, with child/local execution asynchronous. This remains a target, not a measured service-level result.

## Why the run is not called successful yet

Successful static CI, a non-launching probe, a comment-event smoke test and historical child-workflow successes are distinct evidence classes. None alone proves that the current trusted controller has launched all three current child workflows on the same target SHA and that the local executor has completed its separately authorized task. This is a much smaller remaining proof/qualification job than a fresh implementation, but the missing runtime evidence must still be collected.

## Next bounded sequence

1. Re-run/inspect exact-head CI for PR #437 and get independent source-level security review; repair only observed failures.
2. Once required gates pass, run the safe trusted-main probe without secrets/provider calls.
3. Admit one explicitly authorized controller batch and record controller + child IDs, target SHA, terminal conclusions, output reports and digests.
4. Separately stabilize Ollama/Claude on the confirmed host, verify approved no-paid-fallback route and browser allowlist, then run one bounded local task.
5. Update the acceptance record only after both routes have terminal evidence. Do not equate this report's estimate with execution or acceptance.

No agent batch, trusted-main probe, local model/provider call, merge, deployment or acceptance was performed while producing this estimate.
