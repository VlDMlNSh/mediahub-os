# MediaHub OS — Chat Tree Map Addendum, Wave 75

- Date: 2026-10-17
- Working documentation branch: `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`
- Status: **SOURCE-ONLY REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Wave 75 — OpenHands router authorization and delete failure path

Primary report: [OpenHands Router Authorization and Delete Failure Path — Wave 75](../checkpoints/MEDIAHUB-OPENHANDS-ROUTER-AUTH-AND-DELETE-FAILURE-PATH-WAVE-75-2026-10-17.md)

- Exact pinned `api.py` confirms conversation REST routes inherit the shared `/api` router dependencies. `check_session_api_key` still permits requests when `session_api_keys` is empty; the actual target configuration remains unverified. This is a conditional fail-open configuration path, not proof of a live exposure.
- `ConversationService.delete_conversation` calls `safe_rmtree` but ignores its boolean result. `safe_rmtree` returns false on filesystem errors; logical deletion can therefore report success while residual files remain.
- The pinned tree has a `Trash` helper with retry-on-next-start semantics, but the reviewed conversation deletion path does not use it.
- Candidate pin `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1` is 48 commits behind upstream `main`; API, dependencies and conversation service have changed. Main-head source was spot-checked and the same empty-key condition and ignored deletion result remain present in the inspected blobs.
- Required gates: fail-closed startup configuration; principal/capability/conversation binding; deletion state machine with observable failure/retry/verified-erasure; accepted target manifest and source-to-artifact binding.
- Candidate remains NOT SELECTED / NOT ADMITTED / RUNTIME-UNVERIFIED. No tests, install, provider calls, credentials, dispatch, runtime inspection, infrastructure changes or branch integration occurred.
