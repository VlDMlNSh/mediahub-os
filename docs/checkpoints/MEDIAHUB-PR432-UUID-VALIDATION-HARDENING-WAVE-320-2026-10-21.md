# Wave 320 — canonical UUIDv4 validation hardening on PR #432 (2026-10-21)

## Status

**PATCHED ON DRAFT PR / READ-BACK VERIFIED / EXACT-HEAD CI RUNNING / NOT QUALIFIED / NO AGENT DISPATCH.**

- PR: https://github.com/VlDMlNSh/mediahub-os/pull/432
- New PR head: `8a6bc17180ff8027edb5c628f8092a4c527212b5`
- Base: `f16e5bae202a78584f273132e7f88c6e25d3142e`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Prior source review: [Wave 319](MEDIAHUB-PR432-SOURCE-SECURITY-REVIEW-WAVE-319-2026-10-21.md)

## Change

Replaced the permissive child input pattern `[0-9a-f-]{36}` with a canonical lowercase UUIDv4 pattern in all three child workflow authorization steps. Added a contract test for one valid UUIDv4 and malformed examples covering all-hyphen input, wrong version, wrong variant, missing separators and invalid hex. This narrows input validation; it does not change credentials, dispatch transport, provider routing, permissions or controller admission.

## Read-back evidence

| File | Blob SHA | Read-back |
|---|---|---|
| `.github/workflows/gemini-autonomous-engineering.yml` | `155a02159912ca371e6f826c51325ca269857aad` | Strict UUIDv4 pattern present |
| `.github/workflows/gemini-agent-2.yml` | `fff1820a6b97d379b23674f36bd62227b7d4dec2` | Strict UUIDv4 pattern present |
| `.github/workflows/gemini-agent-3.yml` | `781df56e8aa7c75ba453c08378611857862b2e44` | Strict UUIDv4 pattern present |
| `tests/test_gemini_reusable_workflow_contract.py` | `65bc0c4b9a7eb58a71bb1b8123cf1ff4305f52af` | Valid/invalid UUID fixture test present |

Commit returned by final test-file update: `8a6bc17180ff8027edb5c628f8092a4c527212b5`. GitHub PR metadata confirms this is the current head and PR remains OPEN / DRAFT / UNMERGED.

## Exact-head CI state at report time

Runs triggered by head `8a6bc17180ff8027edb5c628f8092a4c527212b5` were still running/queued at last inspection:

- [Astra Verify — 39648235100](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235100) — in progress.
- [Workflow contract validation — 39648235554](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235554) — in progress.
- [Cloud Runtime Validation — 39648235456](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235456) — in progress.
- [Non-launching caller-context probe — 39648235621](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235621) — in progress at last poll.
- [Controller probe — 39648235821](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235821) — probe active; `dispatch_and_monitor` skipped as required for a non-launching PR probe.

These are not final pass results; recheck exact-head CI before further integration.

## Execution boundary

No controller agent mode was launched. Gemini Agents 1–3 remain NOT RUN; no controller or child run IDs, no shared dispatch target, and no agent artifact digests exist. Claude Code and agent-browser on Alamo remain NOT RUN because server 3 identity/capability and the allowed non-paid route are unverified. No secret values were read, no provider call was made, and no merge/deployment occurred.

## Next step

Poll exact-head CI until terminal. If all checks pass, request a separate formal security review tied to this exact head and verify the effective minimal token permissions, HMAC secret separation/configuration and governance gates. Keep the controller unmerged and do not dispatch Gemini/Claude until those gates and Alamo qualification are evidenced.
