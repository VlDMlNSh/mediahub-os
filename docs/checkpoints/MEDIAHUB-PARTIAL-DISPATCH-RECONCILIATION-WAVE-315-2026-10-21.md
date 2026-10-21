# Wave 315 — Partial-dispatch reconciliation fix (2026-10-21)

## Summary

Implemented a bounded fix in PR #432 to preserve the complete batch audit trail when one of the three GitHub API dispatch requests fails. Added a regression contract test and corrected one stale test assertion after the first CI attempt failed. Latest exact-head CI is green for the checked workflows. PR remains Draft/unmerged; no Gemini agent-mode dispatch occurred.

## Canonical transport boundaries

- Gemini Agents 1–3: only through the approved GitHub Actions controller and GitHub API transport, using controller-confined `MEDIAHUB_GITHUB_TOKEN`. One common immutable target SHA is used.
- Alamo/server 3: local Claude Code only; never a Gemini transport/fallback.
- Browser: separate @SentinelX/agent-browser path, only after host identity, capabilities and allowlist are verified.
- Never use `secrets: inherit`; do not read or print secret values.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
PR: https://github.com/VlDMlNSh/mediahub-os/pull/432

## Code changes on PR #432

PR branch: `fix/gemini-controller-api-dispatch-wave312-final`
Latest exact PR head: `8e420af1f8646895d574da709e5d327436d0f8d2`

- Controller `.github/workflows/gemini-batch-dispatch-controller.yml`: blob SHA `8181ff2739273a8a5f1f7522752b4772c8659b40`.
  - Adds a per-child record before attempting the POST.
  - Catches individual dispatch failures without printing upstream exception text.
  - Continues through all three bounded dispatch attempts.
  - Monitors every accepted child run, preserves failed/timeout states, writes a complete per-agent summary, and exits nonzero unless all three dispatches and child runs succeed.
- Test `tests/test_gemini_transport_controller_contract.py`: blob SHA `a7cc2fc0c9ad60e74a2e742606a32f12cfbe2a99`.
  - Adds contract coverage for partial dispatch recording, accepted-child reconciliation, complete summary and fail-closed status.
  - Corrects the pre-existing assertion to match the updated result map.

Commits made to the PR branch:
- Controller reconciliation: `238ce9cc21d53f44fe5e2c126f13f48523c4a2ed`
- Partial-dispatch regression test: `886e6e0489c2a44d009114f5d277ac04a587bad8`
- Assertion correction: `8e420af1f8646895d574da709e5d327436d0f8d2`

## CI evidence on latest exact head

All listed runs reference `8e420af1f8646895d574da709e5d327436d0f8d2` and completed successfully:
- [Workflow contract validation #39643552206](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39643552206) — SUCCESS, includes controller transport contract tests.
- [Astra Verify #39643552160](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39643552160) — SUCCESS.
- [Astra Cloud Runtime Validation #39643552345](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39643552345) — SUCCESS.
- [Controller PR-context probe #39643552498](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39643552498) — SUCCESS; agent dispatch job SKIPPED as required.
- [Reusable workflow caller-context probe #39643552522](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39643552522) — SUCCESS; PR caller denied.

An earlier attempt at head `238ce9cc21d53f44fe5e2c126f13f48523c4a2ed` failed because the test still asserted the previous result-map expression. That failure was diagnosed from the job log, the assertion was corrected, and the later exact-head validation passed. This is retained as provenance, not hidden.

## Gate status

- Partial-dispatch code fix: IMPLEMENTED.
- Regression contract: IMPLEMENTED.
- Exact-head CI: VERIFIED for the listed runs.
- Independent security review: NOT RECORDED (zero formal reviews observed for PR #432).
- Effective GitHub App/token permission scope: NOT VERIFIED.
- HMAC secret configuration/separation: NOT VERIFIED by a non-disclosing admin mechanism.
- Trusted-main non-launching probe: NOT VERIFIED by the PR-context probe; must be separately authorized and evidenced.
- Governance/branch-protection evidence: NOT VERIFIED.
- Gemini Agents 1–3: NOT RUN; no controller dispatch ID or child run IDs for this wave.
- Alamo Claude / @SentinelX browser: NOT RUN; host identity/capabilities were not positively verified in the prior pass.

## Next acceptance gates

1. Independent reviewer inspects exact head `8e420af1f8646895d574da709e5d327436d0f8d2`, including HMAC canonicalization, child target checkout, dispatch correlation and partial-failure behavior.
2. Verify minimal effective transport-token permissions without exposing credentials.
3. Verify HMAC key presence/separation without reading its value.
4. Review governance and authorize any trusted-main no-secret probe.
5. Only after all gates pass, decide whether a real agent dispatch is authorized. Do not use Alamo as Gemini transport.

## Provenance limitations

The controller code and test were read back from the PR branch after updates. Latest PR head and CI run SHAs were re-queried from GitHub. No agent-mode workflow was dispatched, no secrets were accessed, no merge or deployment occurred. This report records implementation and CI verification, not qualification or acceptance.
