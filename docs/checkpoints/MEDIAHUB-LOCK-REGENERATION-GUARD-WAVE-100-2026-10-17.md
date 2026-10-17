# MediaHub OS — Lock regeneration guard, Wave 100

- Date: 2026-10-17
- Status: **GUARD IMPLEMENTED; EXACT-HEAD CI IN PROGRESS; BOOTSTRAP INTEGRITY STILL OPEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Candidate PR: https://github.com/VlDMlNSh/mediahub-os/pull/338
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Candidate branch: `contour-a-schema-validation-consolidation-wave98-20261017`
- Change commit: `29d72044ae77086df3380358816da2e15a940725`
- Changed workflow blob SHA (read-back): `bc6a50bb93ec8ba32aacc7e3b7f973a6311cb072`
- Exact-head validation run observed: [39053283811](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39053283811), run number 198, status **in_progress** at the time of this report.

## Change

Updated `.github/workflows/cloud-agent-lock-generation.yml` to:
1. Capture a unified diff of regenerated lock output against the checked-in lock.
2. Upload the regenerated lock and diff as evidence even if a prior step fails.
3. Fail the workflow on any byte-level lock drift using `git diff --exit-code -- requirements/cloud-agent-schema-validation.lock`, with `git diff --check`.
4. Print the generated lock and SHA-256 digests for both dependency input and lock output.

This adds an explicit reproducibility gate instead of merely generating and publishing a potentially changed lock. Workflow read-back confirms the diff-capture and assertion steps are present. The validation run was in progress; this report does not claim the guard passed or that lock generation completed.

## Integrity boundary and limitations

The generator bootstrap still installs `pip==24.3.1` and `pip-tools==7.4.1` from PyPI without a dedicated hash-locked bootstrap requirements file. Version pinning alone does not establish artifact integrity. This pass does not claim to have solved that issue, nor does it claim byte-for-byte reproducibility until the workflow run and artifact are inspected.

PR #338 remains Draft/open/unmerged. Issue #301 remains open. A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent review and bounded worker/queue qualification remain open. No provider calls, secret access, agent dispatch, deployment, merge or Contour A acceptance occurred.

## Next bounded step

Inspect run 39053283811 and any lock-generation workflow run triggered by the same commit. Download and read back the lock artifact, compare regenerated lock content to the checked-in lock, and record pass/fail. If reproducibility fails, preserve the diff and diagnose drift before modifying pins. Then separately harden bootstrap integrity using a verifiable hash-locked bootstrap or an immutable trusted artifact source.
