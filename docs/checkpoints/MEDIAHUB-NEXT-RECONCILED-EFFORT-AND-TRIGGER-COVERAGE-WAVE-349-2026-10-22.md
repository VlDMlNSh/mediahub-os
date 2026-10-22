# Wave 349 — reconciled effort, historical evidence and controller trigger coverage

- Date: 2026-10-22
- Status: **IMPLEMENTED IN PR / CI RUNNING / AGENT BATCH NOT RUN / NOT QUALIFIED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Prior estimate correction: [Wave 348 revised estimate](MEDIAHUB-NEXT-REVISED-EFFORT-ESTIMATE-WAVE-348-2026-10-22.md)
- Trigger-coverage fix: [PR #443](https://github.com/VlDMlNSh/mediahub-os/pull/443)
- Related HMAC-test repair: [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Scope and correction

Wave 346's 12–25 active-hour figure is superseded. Wave 348 reconciled it to 3–6 active engineering hours, with 6–10 hours only as contingency. This pass further separates work already evidenced from missing current qualification evidence. It does not restart controller, GitHub transport, three child workflows, or browser automation from scratch.

The owner reports that manual execution of all three Gemini agents and a real agent-browser task were already completed. Repository evidence independently confirms historical successful Gemini child workflow runs listed below. The browser completion is recorded here as **OWNER-REPORTED historical execution**; a matching current-run artifact was not found in the repository search performed in this pass. Prior browser work is not to be repeated merely because the executable was absent from a recent PATH inventory.

## Historical evidence reused (not repeated)

- Three successful Gemini workflow runs on source SHA `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`: [Agent 1 run 39370191589](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370191589), [Agent 2 run 39370202615](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370202615), [Agent 3 run 39370217605](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370217605). Their summaries reportedly include successful actionable-output validation and non-expired artifacts.
- Candidate controller/probe runs recorded in Wave 348: [39647070718](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070718), [39647070682](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070682), [39647070683](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070683), [39647070609](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070609), [39647070781](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070781). These were candidate/negative-path checks, not a current successful three-child batch.
- Issue-comment event smoke test: [run 39647870697](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647870697) exercised a non-matching comment and skipped as expected.
- Owner previously confirmed the GitHub settings exist: `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY`, and `MEDIAHUB_GEMINI_BATCH_ENABLED`. Values were not read. Historical/manual operation supports not repeating basic transport setup; it does not establish current effective token scope, current batch correlation, or current trusted-main qualification.
- User reports successful prior agent-browser use. That historical task is not repeated; current host/route readiness remains separate and is only revisited if required to execute a new bounded local task.

## New bounded engineering change

PR #443: [fix(contour-a): cover Gemini contract changes in controller probe](https://github.com/VlDMlNSh/mediahub-os/pull/443), head commit `66f8cfc1bbd83bbb686ee8a1bbcea9589b182590`.

- Controller workflow blob SHA after change: `3becd61702b3cad5a40f7d2a4de0b7fd6aee4b4f`.
- Contract-validation workflow blob SHA after change: `9f362069cdb5a7c200d93e2057e3f0d338bb81c0`.
- New regression test blob SHA: `918192c6887775ccd6d800c1c44198b513c4db8b`.
- Controller `pull_request.paths` now includes the Wave 284 contract-validation workflow and the HMAC/controller contract tests affected by PR #437, plus the new regression test.
- Contract validation now runs the regression test. The test checks that the controller's no-secret PR probe filter covers the relevant paths and that the validation workflow runs the regression.
- This change only fixes CI/probe visibility. It does not enable dispatch on pull requests; controller dispatch remains guarded by trusted `main`, owner-only exact `/next` or explicit workflow inputs, the batch flag, token and HMAC gates.

## Current exact-head checks

At the time of the first check for PR #443 head `66f8cfc1bbd83bbb686ee8a1bbcea9589b182590`:
- Combined status endpoint returned an empty list: **NOT VERIFIED** by that endpoint.
- Workflow-run endpoint returned active runs:
  - Controller probe run **39748357615** — queued
  - Contract validation run **39748357460** — in progress
  - Astra Verify run **39748357515** — in progress
  - Cloud Runtime Validation run **39748357531** — in progress
- Formal PR review endpoint returned zero reviews. No successful conclusion or independent review is claimed here; these runs must be polled to terminal state.

PR #437 head remains `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`; the queried exact-head status and workflow-run endpoints returned empty results and formal reviews were zero. Treat that as **NOT VERIFIED**, not PASS. PR #441 remains a documentation-only open PR; it is not a runtime qualification result.

## Recalculated remaining active effort

This estimate assumes the historical runs and existing components are reused, no basic transport/browser task is rebuilt, and no new architecture defect appears.

| Remaining work | Active effort |
|---|---:|
| Finish PR #443 CI and obtain focused independent review; fix only demonstrated failures | 0.25–0.75 h |
| Resolve PR #437 exact-head test evidence/review only if still needed after current validation and its own branch CI | 0.25–0.75 h |
| One current trusted-main no-secret probe and review of caller/governance evidence | 0.25–0.5 h |
| One controller-owned batch: capture controller + three child IDs, terminal outcomes, useful outputs and artifact digests | 0.5–1 h |
| Read-back and final evidence/acceptance record | 0.25–0.5 h |
| **Expected remaining active effort to first current Gemini batch** | **1.5–3.5 h** |

**Contingency:** 4–6 active hours if a gate exposes a source defect, permissions problem, or a failed child needing repair. This is lower than Wave 348 because historical workflow success and candidate CI are explicitly reused; it is not a guarantee that asynchronous reviews/CI complete within those hours.

**Separate local executor line:** prior browser work is not rebuilt. A new bounded Ollama/Claude task still needs a reachable runtime and an evidenced permitted non-paid route; the last current host check found Ollama client 0.34.4 but no reachable server, and did not find Claude/agent-browser on PATH. Allow approximately 0.5–1.5 active hours only if a new local task remains a required acceptance criterion and the host reconnects; otherwise keep it blocked without delaying the independent Gemini route.

## Current status and next step

- Trigger coverage fix: **IMPLEMENTED IN PR #443; CI RUNNING**.
- Historical three-agent workflow executions: **VERIFIED HISTORICALLY**.
- Current controller → three-child correlated batch: **NOT RUN / NOT VERIFIED**.
- Token transport: historical/manual operation and owner report acknowledged; effective present scope is not re-tested by reading secrets. Only investigate it if a live, authorized controller run fails or non-secret permissions evidence requires it.
- Prior agent-browser work: **OWNER-REPORTED HISTORICAL EXECUTION**; no duplicate task performed.
- Local Ollama/Claude route: **NOT QUALIFIED for a new task** based on the last observed runtime evidence.
- Contour A: **PARTIALLY IMPLEMENTED / NOT YET ACCEPTED**.

Next: poll PR #443 runs to terminal state; address only observed failures; obtain substantive review. Do not post an owner `/next` trigger or launch the batch until all applicable gates are accepted. Then use one immutable target SHA and record the controller run ID, three child IDs, terminal conclusions, artifacts/digests and useful-work evidence.

## Direct links

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #443](https://github.com/VlDMlNSh/mediahub-os/pull/443)
- [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437)
- [PR #441](https://github.com/VlDMlNSh/mediahub-os/pull/441)
