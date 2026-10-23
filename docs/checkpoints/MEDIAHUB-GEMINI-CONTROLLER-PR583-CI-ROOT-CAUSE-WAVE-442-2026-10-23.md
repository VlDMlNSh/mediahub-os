# Wave 442 — Gemini controller PR #583 exact-head CI root-cause triage

Date: 2026-10-23  
Status: **ROOT CAUSE IDENTIFIED / FIX NOT IMPLEMENTED / NOT QUALIFIED**

## Scope and immutable refs

- Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os)
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301), still open.
- Controller hardening PR: [#583](https://github.com/VlDMlNSh/mediahub-os/pull/583), Draft/open/unmerged.
- PR #583 head: `9de1526e6daa121c62aa85fc707d9a8c6f9e0d4d`; base SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Controller file at PR head: `.github/workflows/gemini-batch-dispatch-controller.yml`, blob SHA `34a065b24ca94593c32699a5479be406f2e24e66`.
- Research PR [#585](https://github.com/VlDMlNSh/mediahub-os/pull/585) head: `85f716005d40fbc03e85762f867eaf235f23629a`; Draft/open/unmerged.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).

## Findings

### PR #583 — two failing jobs share one source-level contract mismatch

1. Astra Verify run [39973058604](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058604), job `120480482676`, failed at **Cloud admission unit tests**.
2. Gemini workflow contract validation run [39973058901](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058901), job `120480483315`, failed at **Run controller transport contracts**.
3. Both logs identify the same failing test: `test_pr_probe_concurrency_isolated_from_long_running_agent_batch`.
4. The test asserts the literal text `group: mediahub-gemini-controller-batch` exists. The actual controller intentionally expresses the group as a GitHub Actions expression:
   `group: ${{ github.event_name == 'pull_request' && format('mediahub-gemini-controller-pr-probe-{0}', github.event.pull_request.number) || 'mediahub-gemini-controller-batch' }}`.
   This isolates pull-request probes from the serialized agent batch but no longer contains the asserted literal line. This is a stale source-string test, not evidence that the runtime concurrency expression is absent.
5. Do not simply weaken/remove the test. Repair it to assert the actual expression and both branches of the intended invariant: PR probe group is PR-specific; non-PR events resolve to the batch group; `cancel-in-progress` is true only for PR probes. Add a negative regression if practical.

## Other exact-head evidence

- PR #583 checks at the observed head: provider contract verification run [39973058613](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058613) SUCCESS; AI Factory verification [39973058680](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058680) SUCCESS; Astra Cloud Runtime Validation [39973058385](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058385) SUCCESS; probe-only run [39973058548](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39973058548) SUCCESS. These do not override the two failures.
- PR #583 formal reviews: zero returned. Combined-status endpoint returned an empty list; treat that as **NOT VERIFIED**, not PASS.
- PR #585 exact-head Astra Verify [39983810741](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39983810741) and Astra Cloud Runtime Validation [39983810755](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39983810755) are now **SUCCESS** on `85f716005d40fbc03e85762f867eaf235f23629a`. Formal reviews: zero; combined-status endpoint empty. PR #585 remains Draft/unmerged and inventory freeze/formal comparison remain NOT READY.
- The current controller workflow source includes the named-artifact invariant: exactly one non-expired `gemini-output` artifact and digests for all non-expired artifacts are required for success. This source review is not runtime qualification.
- No controller dispatch, Gemini child dispatch, provider call, secret access, merge, deployment, or qualification was performed in this pass.

## Disposition

- PR #583: **BLOCKED** until the stale test is corrected and both failing exact-head jobs pass, followed by independent review and re-check of all required gates.
- PR #585: CI **VERIFIED** for the two observed workflows only; review and merge eligibility **NOT VERIFIED**.
- Gemini batch: **NOT RUN**. Do not post an Issue #301 `/next` trigger while controller/governance gates remain unresolved.
- Contour A: **NOT ACCEPTED**; Contour B remains gated.

## Next bounded step

Update `test_pr_probe_concurrency_isolated_from_long_running_agent_batch` so it verifies the actual expression and semantics rather than requiring a stale literal. Run the focused test, then exact-head Astra Verify and controller contract validation; read back the diff and blob SHAs; obtain independent review before considering integration.
