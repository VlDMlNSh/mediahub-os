# MediaHub OS — Wave 280: generic worker gateway fallback and route-admission fix

- Date: 2026-10-20
- Status: **SOURCE DEFECT CONFIRMED / FAIL-CLOSED FIX IN DRAFT PR / EXACT-HEAD CI PASS / INDEPENDENT REVIEW OPEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Proposed fix: [Draft PR #425](https://github.com/VlDMlNSh/mediahub-os/pull/425)
- Related gates: [controller-only cloud transport PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421); [single legacy-workflow retirement proposal #423](https://github.com/VlDMlNSh/mediahub-os/pull/423)

## Summary

Tracing the signed node-control command from issuer/signer through the worker found that six accepted language-task operation values reached a generic host-side gateway fallback, instead of a controller-admitted cloud route. The fallback passes a plain dictionary into `AstraGatewayRuntime.run_bounded()`, but the gateway requires an `AstraTaskRequest`. The validation path therefore returns a failed dataclass result; the worker then tries to publish that object through `json.dumps()`, which cannot serialize the dataclass. In `main()`, publication is outside the inner command-execution exception handler and occurs before the command is marked executed; source control flow therefore permits repeated retry after publication fails.

Separately, the fallback instantiates a cloud-first provider orchestrator on the node worker. That is not an admitted cloud-agent transport under the current Contour A rule: the GitHub-hosted Actions controller and fixed-scope child workflows are the sole launch path for cloud agents. Simply converting the dictionary into a request object would have re-enabled a route that has not passed the controller/issuer/provider gates.

## Exact source snapshot

- `main`: `80be45a70732b1d568164571d4273a6397792c3b`.
- `astra_github_agent.py`: `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`.
- `runtime/mediahub_runtime/astra_gateway.py`: `10985e4ad8f682313d08e7492ecc1856a8bce20f`.
- `runtime/mediahub_runtime/autonomous_task.py`: `f2287c962cfc1eac16cf8480dc359def1ce516fa`.
- `ops/control/sign_command.py`: `fc6943a79cefdf06e59d6e32771d2df551b2f0e9`.
- Existing control-command coverage: `tests/test_astra_github_agent_contract.py`, blob `7dc0b70c9b5c3e0ef664749d5527b71740cb1656`.

Source links:
- [Signed worker/control command handling](https://github.com/VlDMlNSh/mediahub-os/blob/main/astra_github_agent.py)
- [Node-specific command signer](https://github.com/VlDMlNSh/mediahub-os/blob/main/ops/control/sign_command.py)
- [Gateway task validation](https://github.com/VlDMlNSh/mediahub-os/blob/main/runtime/mediahub_runtime/astra_gateway.py)
- [Bounded lifecycle result model](https://github.com/VlDMlNSh/mediahub-os/blob/main/runtime/mediahub_runtime/autonomous_task.py)

## Entry-chain evidence

The worker reads `control/commands/{NODE_ID}.json` and validates schema version `mediahub.astra.control-command.v1`, node identity, allowed operation, target SHA, command freshness, HMAC, exact current HEAD, and an executed-command replay marker. This is a signed **control-command**, not a `mediahub.ai.astra-task` Task Contract; the two envelopes must not be conflated.

The six operations reaching the generic fallback are:

- `research`
- `architecture`
- `review`
- `documents`
- `coding`
- `coding_v2`

The fallback also makes the `ASTRA_RUNTIME_ROOT` search and imports `AstraGatewayRuntime`, whose default orchestrator has provider/API adapters. It supplies keys `task_id`, `title`, `description`, and `capability` rather than the `AstraTaskRequest` fields `request_id`, `session_id`, and `user_command`. The gateway's `_validate_task` explicitly rejects non-`AstraTaskRequest` input.

The worker's supervisor handles exceptions from `execute(cmd)` inside an inner `try`, but calls `publish(... result=value ...)` after that block. `publish()` JSON-encodes the result before `_mark_command_executed()` and `mark_published()`. A non-JSON-serializable dataclass result can escape to the outer loop's `last_error.json` handler before those command-completion markers. This conclusion is from source control-flow inspection; the pre-fix loop was not live-run in this audit.

## Bounded fix proposed in PR #425

[PR #425](https://github.com/VlDMlNSh/mediahub-os/pull/425) is based on `main` at `80be45a70732b1d568164571d4273a6397792c3b`, head `ce44a47b0d327a5cca9593e529fe97b492ffaa4a`.

- Add an explicit set for the six generic gateway-only operations and return the stable rejection `gateway_route_not_admitted` **before importing or invoking the gateway**.
- Remove the old generic `AstraGatewayRuntime().run_bounded(dict)` call and its implicit `ASTRA_RUNTIME_ROOT` discovery fallback from this command worker.
- Reject any future allowed operation lacking a concrete handler with `operation_handler_not_implemented`, rather than silently falling through to a provider.
- Preserve explicit concrete handlers such as `health`, qualification and diagnostics.
- Add mock-only tests asserting all six operations fail closed before gateway import, the health handler remains concrete, and the old fallback is absent.

This does not implement a new cloud execution path and does not claim coding/research work has become available through this worker. Such work must be reintroduced only through the approved GitHub-hosted controller or another separately admitted and governed executor path.

## Exact-head verification

- [Astra Verify #39453835133](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39453835133): **SUCCESS**.
- [Astra Cloud Runtime Validation #39453835149](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39453835149): **SUCCESS**.
- Changed paths: `astra_github_agent.py` and `tests/test_astra_github_gateway_route_admission.py` only.
- PR #425 remains OPEN / DRAFT / UNMERGED. The review submissions endpoint returned no independent reviews.

## Verification boundaries

CI compiled the repository and ran the repository's unit-test workflow, including the new regression tests. The fix was verified through exact-head Actions results and source read-back, not through a live node command or provider request. No host was accessed, no secret was read, no provider/model was invoked, no Gemini agent was dispatched, and no merge, deployment, release, Contour A qualification or acceptance occurred.

## Next gates

1. Obtain independent review of PR #425, with explicit review of the controller-only transport boundary and fail-closed behavior.
2. Continue PR #421's separate independent review, exact-head required checks, caller-guard/secret-boundary review and the controlled negative caller-context test that must not launch Gemini.
3. Keep PR #423 as the single legacy-workflow retirement proposal; PR #422 is closed as its duplicate. Do not merge any Draft automatically.
4. Trace the external A0 mission producer/writer and the actual trusted issuer/approval verifier before accepting a new Task Contract schema. Preserve the distinction among signed control-command, Task Contract, A0 coordination authority and canonical Product State Authority.

Contour A remains **NOT_PROVEN / BLOCKED**. Contour B remains blocked pending Contour A deployment and independent acceptance.
