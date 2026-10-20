# MediaHub OS Contour A — Wave 247: issuer-to-publisher trace

- Date: 2026-10-20
- Status: SOURCE AUDIT COMPLETE; no safe production integration path; NOT PROVEN / BLOCKED.
- Issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Working branch: `work/contour-a-wave247-issuer-publisher-trace-2026-10-20`, based on docs HEAD `577501f8954376b0044de350d6d67e949dfb0fc2`.
- main HEAD: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.
- docs HEAD: `577501f8954376b0044de350d6d67e949dfb0fc2`; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`; docs/main = 2,562 ahead / 39 behind. No merge/rebase.
- Bootstrap blob `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`; Master Roadmap blob `beef785c787702dc174cf9a5515bac8c9f4b292f`; Baseline 2.0 blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` (accepted/canonical/unchanged).
- Map/checkpoint before update: `3e71ed85a6bdfd730111452cfc8ad081372a8f6b` / `03b5791ddb814c2eacda95858ffcd50668106f14`. Proposed new blobs: `7e3870d0b1e4f81733508044ebcf8e7aa97bb18f` / `1d8c8bf184781284221d1ac566391d3606573385`.

## Trace and facts

1. **Ingress/issuer:** [astra-chat-control.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-chat-control.yml), blob `51b17ec2410032772f9baa1de4afedb6b000f3c4`, accepts issue comments, gates by OWNER/MEMBER/COLLABORATOR association, parses `/astra`, then validates task-file fields. It has `contents: write`, `issues: write`, `actions: write`. This is not an accepted cryptographic issuer/capability decision.
2. **Signer:** [sign_command.py](https://github.com/VlDMlNSh/mediahub-os/blob/main/ops/control/sign_command.py), main blob `fc6943a79cefdf06e59d6e32771d2df551b2f0e9`, signs HMAC commands using node-key environment variables. The reviewed control/worker path does not invoke it as an admission verifier.
3. **Queue:** the control path reads a task file and checks `status == READY`; no atomic claim, lease/cancellation, replay ledger or revocation check is established here. Issue #301 states CAF-Q-001…CAF-Q-015 is documentary, not a live scheduler.
4. **Worker:** [run_distributed_local_worker.py](https://github.com/VlDMlNSh/mediahub-os/blob/main/ops/qualification/run_distributed_local_worker.py), blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`, parses task JSON and checks required fields, but does not verify signature/issuer/capability/policy/replay/revocation. It still stages all changes, commits and directly pushes a worker branch. [Worker workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-distributed-local-worker.yml), blob `f650f2416c19dc75b4a0eeec037661c0c6169910`, grants `contents: write` and persists checkout credentials on three checkouts.
5. **Artifact/publisher:** [PR #399](https://github.com/VlDMlNSh/mediahub-os/pull/399) adds schema blob `015f89715e6714afcb838841a813503a57ec494c` and structural validator blob `a37dfcd70a6be8bbff11abfe77ef9523902f9096`. State is `PROPOSED_UNVERIFIED`; this code does not authenticate authority, check revocation/replay, recompute the patch digest from bytes, or publish.

## Exact refs / CI

- PR #396: Draft head `5358d1f7918f41ec11c59fb67f433655d9be7cb2`, base docs `d18dfb64efa536142c39e00bf94a807511c0e460`; 31 ahead / 29 behind current docs. No reviews; no PR-triggered run returned for that exact head.
- PR #397: Draft head `8ee730e2a5d9038d6f2764cf00e483bd3a5505e0`, base main `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`; 3 ahead / 6 behind current main. Exact-commit lookup: Astra Verify [39332175846](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39332175846) and Cloud Runtime Validation [39332175994](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39332175994) SUCCESS. No review/approval.
- PR #399: exact-head CI [39368438967](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39368438967), [39368438984](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39368438984), [39368439034](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39368439034) SUCCESS on head `723269f9ff2a69cff8ec45fa140f23e4648b3825`, 6 behind current main; no review.
- PR #400: isolated verifier at head `53d509b50ce2c5214c692b4e82dae610344f51ff`, 3 ahead / 6 behind. Exact-head CI [39382694131](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39382694131) and [39382694133](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39382694133) SUCCESS. Review is COMMENTED, not approval; HMAC possession alone is not distinct issuer identity, and key lifecycle/replay/context hardening remain.
- PR #405: head `59951fb247a6251b1693d5f0bc807c96480f7424`, 2 ahead / 6 behind; exact-head CI [39377730257](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39377730257), [39377730292](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39377730292) SUCCESS. Review is COMMENTED, not approval; direct worker publication remains.
- main combined-status returned no entries (not a pass). Branch metadata says `protected=false`, rulesets returned `[]`; detailed protection endpoint returned 403 for this integration, so full settings were not readable.
- [Wave 246](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-GEMINI-DISPATCH-CREDENTIAL-SCOPE-REVIEW-WAVE-246-2026-10-20.md), blob `6902ef234922486e656bba04bade34f7a32f37bb`, records A1/A2/A3 workflow tokens with write-capable GitHub MCP scopes. No Gemini dispatch was submitted in this pass.

## Contract proposal and next tests

Keep the bundle untrusted. Trusted admission must bind issuer, capability, policy digest/version, audience/repository/action, command/task/node, exact base/target SHA, allowed paths, expiry/revocation, nonce and an atomic cancellable claim/lease receipt. Worker returns only a patch and manifest without publication credentials. A separate publisher independently validates the receipt, re-hashes actual patch bytes, checks exact path/mode semantics and current base, rejects traversal, symlinks, submodules, unexpected files and secret-bearing output, and publishes with its own short-lived least-privilege credential.

Negative fixtures must cover invalid signature/issuer, wrong audience/action/repository/identity/SHA, expiry/revocation, replay, policy digest mismatch, missing lease, patch digest/size mismatch, missing/extra/unsafe paths, symlink/submodule/mode changes, stale base, artifact reuse and publisher retry/idempotency. No production code or tests were run in this wave because accepted trust inputs and queue-claim semantics do not yet exist.

The Master Roadmap blob currently ends at Wave 152 while map/checkpoint navigation is at Wave 246; roadmap reconciliation remains open and was not silently rewritten. Baseline 2.0 is unchanged. Jarvis, ASTRA A0 and MediaHub Product State Authority remain separate. No worker/Gemini dispatch, secret/host change, merge, deployment or gate promotion occurred. Contour A remains NOT PROVEN / BLOCKED; G0–G11 BLOCKED, G11 HUMAN_ONLY; Contour B remains gated.

**Next concrete step:** obtain governance acceptance for issuer/capability/policy and atomic claim/lease/revocation semantics, then wire verification into trusted admission and implement artifact-only worker output plus a separate publisher. Keep all candidates Draft until independent review and fresh exact-head evidence pass.
