# MediaHub OS Contour A — PR #376 exact-head CI and integration readiness (Wave 192)

- Date: 2026-10-19
- Scope: read-only PR/CI/branch comparison and acceptance-gap assessment. No merge or PR mutation.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous cross-layer review: [Wave 191](MEDIAHUB-CONTOUR-A-AUTHORIZATION-LAYER-BOUNDARY-AND-INTEGRATION-GAPS-WAVE-191-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- PR: [#376](https://github.com/VlDMlNSh/mediahub-os/pull/376)

## Exact refs and current state

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- PR #376 head: `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`.
- Base: `main` at `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Compare API: `ahead`, ahead_by 1, behind_by 0, one commit.
- Changed files: only `tests/test_gemini_workflow_parity.py` (+96 lines).
- PR is open, Draft, unmerged; GitHub reports mergeable=true and mergeable_state=clean. This is not approval to merge.
- Exact-head check runs:
  - [Astra Cloud Runtime Validation](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39231107098) — completed, success, check name `validate`, head `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`.
  - [Astra Verify](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39231107074) — completed, success, check name `verify`, same head.
- Combined commit status endpoint returned `pending` with no legacy statuses; two actual check runs above are completed-success. Do not confuse these separate GitHub status surfaces.
- Branch protection API returned 403 Resource not accessible by integration. Required-review rules and protection settings therefore remain **unverified**, not absent.
- Issue #301 remains open. PR #374 and #375 remain open Draft/unmerged.

## What PR #376 proves — and does not prove

The single added test file checks presence/parity of three manual Gemini workflows, distinct secret references, hosted runner and timeout, MCP tool allowlist, checkout credential persistence, explicit no-merge/no-deploy prompt text, and detects nine mutable action/container references.

Passing tests and CI prove the test file passed in the current CI context. They do not prove Gemini credentials work, that a Gemini run was dispatched, that post-run PR branch/base/path constraints are enforced, that mutable references are safe, or that the workflow has been security-qualified. The test explicitly retains write permissions and treats mutable refs as detected findings, not remediated dependencies.

Wave 188's authority gap remains: prompt-level scope does not itself enforce server-side branch/path constraints. Exact MCP OCI digest/provenance is unresolved. The PR is intentionally Draft and should not be promoted solely because the current checks pass.

## Merge/readiness decision

**Do not merge or mark ready on this evidence alone.** This is a readiness assessment, not a new block imposed on behalf of a human reviewer. Before promotion, require:
1. authorized review of workflow token authority and branch/path restrictions;
2. immutable, provenance-verified dependency pins, including exact MCP image digest;
3. enforced post-run checks for expected branch prefix, PR base and allowed changed paths, plus rejection of direct writes to protected refs;
4. evidence that the protection/review policy is configured, obtained from a suitably authorized view;
5. fresh CI at the exact candidate head after any remediation.

No branch-protection state was inferred from the 403. No tests were run locally in Wave 192; no workflow dispatch, secret access, host command, merge, deployment or qualification occurred.

## Environment and overall qualification

SentinelX currently reports zero connected hosts; the Mac mini is offline, and `mh-dev-01` / `mh-dev-02` are disabled by the user. Codex Tasks has no registered environments. ASTRA GOLD current truth on main blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731` shows G0–G11 BLOCKED and overall `NOT_PROVEN / BLOCKED`.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
