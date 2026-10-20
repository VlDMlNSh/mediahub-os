# MediaHub OS — Wave 243: signed-command boolean timestamp regression

- Date: 2026-10-20
- Status: **SOURCE FIX COMMITTED AND READ-BACK VERIFIED; EXACT-HEAD ASTRA VERIFY STILL RUNNING AT REPORT TIME; VERIFIER REMAINS PROPOSAL ONLY**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Verifier PR #400: https://github.com/VlDMlNSh/mediahub-os/pull/400
- Worker token PR #405: https://github.com/VlDMlNSh/mediahub-os/pull/405
- Previous integration audit: [Wave 242](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-WORKER-PR-STALE-BASE-AND-SECURITY-INTEGRATION-GATE-WAVE-242-2026-10-20.md)
- Verifier proposal: [Wave 231](https://github.com/VlDMlNSh/mediahub-os/blob/work/contour-a-command-verifier-wave231/docs/checkpoints/MEDIAHUB-CONTOUR-A-SIGNED-COMMAND-VERIFIER-WAVE-231-2026-10-20.md)

## Finding

Exact-head CI on the verifier PR previously failed the unit-test job. The captured log for Astra Verify run `39380836754`, job `118489339008`, showed:

```
FAIL: test_rejects_boolean_issued_at
AssertionError: ValueError not raised
FAILED (failures=1)
```

Cause: Python treats `bool` as a subclass of `int`; `isinstance(True, int)` is true. The verifier's check accepted JSON boolean `true` as a Unix timestamp even though the test and schema require an integer timestamp.

## Bounded fix

- Changed the type guard in `ops/control/sign_command.py` from `isinstance(command["issued_at"], int)` to `type(command["issued_at"]) is not int`.
- This rejects booleans while accepting actual integer timestamps; it does not broaden verifier authority or alter the command schema.
- Updated worker branch: `work/contour-a-command-verifier-wave231`.
- Fix commit: `53d509b50ce2c5214c692b4e82dae610344f51ff`.
- Updated source blob SHA: `287e91af8890419bd76db9a1369fbc39f59a14ec`, 7,006 characters.
- Re-read source after update and confirmed the strict type guard exists exactly once.
- Re-read regression test blob SHA `bc4c06081b0664d315ecd67d872088e410b5e25d`; it includes `test_rejects_boolean_issued_at`, which signs the boolean payload and expects a `ValueError`.

## CI evidence at report time

- Astra Cloud Runtime Validation run `39382694133` (run 990) for fix commit `53d509b50ce2c5214c692b4e82dae610344f51ff`: **SUCCESS**.
- Astra Verify run `39382694131` (run 2166) for that exact fix commit: **IN_PROGRESS** at the time of this report. No passing result is claimed here.
- Earlier failed Astra Verify run `39380836754` was on prior PR merge SHA `8601502f482ba5f58c0eb977b1244ce53617123c`; its failing log directly identified the regression.
- The compare against current main `8761f734031ef0b880b974cea24c2463e7a22046` reported the verifier branch diverged: 3 commits ahead / 2 behind, merge base `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- PR #400 remains OPEN/Draft and stale against current main. No rebase, merge or deployment was done in this pass.

## Security boundaries not closed

This fix addresses one type-validation defect only. PR #400 remains a standalone verifier proposal; the worker does not invoke it. The existing worker still has direct git commit/push logic. Issuer authentication, capability/policy evaluation, key rotation/revocation, replay prevention, cancellation/recovery, and separately authorized artifact publication remain open. The branch divergence also remains unresolved.

No worker or agent was dispatched. No secret value or host credential was read or exposed. No production execution, merge, deployment, qualification or acceptance occurred. Issue #301 remains OPEN; Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated on Contour A deployment and independent acceptance.

## Next step

1. Capture the final result and job logs for Astra Verify run `39382694131`; only mark the regression fixed if the exact-head test job passes.
2. Rebase PR #400 onto current main in a controlled operation, rerun the full suite, and resolve its existing two unrelated failures only after reproducing against the baseline.
3. Keep the verifier disconnected from production worker admission until issuer/capability authority, replay/revocation lifecycle, and artifact-only publisher boundaries are implemented and reviewed.
4. Update PR #405 separately; do not treat this verifier fix as worker integration or permission to merge either draft.
