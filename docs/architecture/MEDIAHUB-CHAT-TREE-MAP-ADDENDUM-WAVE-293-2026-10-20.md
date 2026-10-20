# Canonical map addendum — Wave 293 (2026-10-20)

- **Report:** [Exact-head CI repair and revalidation](../checkpoints/MEDIAHUB-EXACT-HEAD-CI-REPAIR-WAVE-293-2026-10-20.md).
- **Candidate head:** `185f55b63121b1aece7e60f6c087ecfceab2721e` on PR #421 branch `contour-a/workflow-call-controller-governance-wave243`; open/Draft/unmerged, not canonical accepted code.
- Corrected the two PyYAML contract assertions to match scalar `needs: probe`; expanded dedicated validation workflow triggers and commands to run Wave 292, reusable workflow, and transport contracts.
- Exact-head checks passed: Astra Verify 39475766199 (453 tests); contract validation 39475766192 (actionlint + 5/5/12/5 tests); Cloud Runtime Validation 39475766251; negative context probe 39475766469; Wave 292 PR probe 39475766513. PR observer reports `pull_request`, `refs/pull/421/merge`, `trusted_controller=false`; model jobs and summary skipped.
- No model/provider invocation, secret access, trusted positive dispatch, merge, deployment, qualification, or acceptance. PR #421/#426 remain open/draft/unmerged with no independent reviews; resolve their overlapping probe-file changes before integration. Effective Actions/org and branch-protection policy remain unverified.
- **Next:** resolve PR overlap and governance/review gates; only after reviewed acceptance on `main`, execute the no-secret default probe mode (`confirm=no`) to capture trusted positive context. Contour A **NOT_PROVEN / BLOCKED**; Contour B gated.
