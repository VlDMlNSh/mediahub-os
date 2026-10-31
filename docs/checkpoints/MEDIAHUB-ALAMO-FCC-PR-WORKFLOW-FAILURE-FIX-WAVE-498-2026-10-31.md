# Wave 498 — fix PR workflow leakage and contract-test assertion

- Date: 2026-10-31
- Status: **FIX IMPLEMENTED / NEW EXACT-HEAD CI QUEUED / NOT VERIFIED**
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/610
- Branch: `contour-a/alamo-fcc-claude-hosted-runner-20261031`
- Failed head: `da48aaf2e876d6e758caf0af593dde3168c8693f`
- Failed workflow run: [41184816539](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41184816539)
- New code head: `2206a3a87f05532a72ac1406fcc1072066524f39`
- Workflow blob: `25a91f827867a10f2eb4f5f6fb347956a6ccb40a`
- Test blob: `99d3af7a33f61e715e95cedf5d401acd2c392c86`

## Failure diagnosis from job logs

1. Contract job `124489516312`: 5 passed, 1 failed. The new assertion searched for a literal backslash-n sequence instead of a newline.
2. Runtime job `124489530484`: PR no-op step succeeded, but the Ollama/FCC install step ran unexpectedly because its workflow_dispatch condition had not been added. It failed before execution because the FCC checkout was correctly skipped and the working directory did not exist. No Ollama installation, model download, FCC server, or Claude request occurred.
3. Dispatch gate job `124489516370`: SUCCESS.
4. Astra Cloud Runtime run `41184816456`: SUCCESS. Astra Verify run `41184816462` was in progress at observation time.

## Fix applied

- Added an explicit `if: github.event_name == 'workflow_dispatch'` guard to the missed Ollama/FCC install step.
- Replaced the brittle escaped-newline contract assertion with a count of manual-dispatch-only guards and explicit PR no-op assertions.
- The PR path remains no-install/no-model/no-network inference; live steps remain manual-dispatch only.

## Current verification state

- New head `2206a3a87f05532a72ac1406fcc1072066524f39`.
- New exact-head runs at observation: Astra Verify `41184878451` QUEUED; Astra Cloud Runtime `41184878441` QUEUED; Alamo runner workflow `41184878541` QUEUED.
- No current exact-head status conclusion yet: **NOT VERIFIED**.
- Independent reviews and review threads: none.
- Live runner smoke NOT RUN; Alamo/Ollama equivalence NOT VERIFIED; no merge, deployment, qualification or acceptance.

## Next gate

Inspect run `41184878541` and the two Astra workflows on the exact current head. Require contract tests to pass and all PR jobs to finish successfully with no unintended install/runtime execution. Then obtain independent security/contract review before merge or owner-authorized manual dispatch.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md


## Follow-up verification — 2026-10-31

- Latest PR head at verification: `6ee33596ec0c1bfa534c2683a4267928206c1de0` (documentation commits after the corrected code commit; workflow/test blobs unchanged).
- Exact-head Alamo workflow run [41184940852](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41184940852): `workflow-contract` job `124489892341` SUCCESS; `dispatch-gate` job `124489892599` SUCCESS; `alamo-local-fcc-claude` job `124489909519` SUCCESS. PR no-op declaration step succeeded; FCC checkout, Ollama install/model pull, Node/Claude installation, live smoke and artifact upload steps were SKIPPED by design for pull_request.
- Exact-head Astra Cloud Runtime run [41184940814](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41184940814), job `124489856820`: SUCCESS.
- Exact-head Astra Verify run [41184940845](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41184940845), job `124489857412`: SUCCESS.
- Therefore all three workflow runs and all three Alamo workflow jobs are terminal SUCCESS on the latest observed PR head. The live inference path remains **NOT RUN**, not green/qualified.
- Independent review remains absent; no review threads. PR #610 remains OPEN, UNMERGED. Alamo/Ollama equivalence remains NOT VERIFIED. No qualification, deployment or acceptance.
