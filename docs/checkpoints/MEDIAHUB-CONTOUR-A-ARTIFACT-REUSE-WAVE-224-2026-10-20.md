# Contour A Wave 224 — artifact reuse classification

Date: 2026-10-20. Status: design evidence only; no implementation or acceptance.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
Draft worker workflow PR: https://github.com/VlDMlNSh/mediahub-os/pull/397
Evidence PR: https://github.com/VlDMlNSh/mediahub-os/pull/396
Wave 223: https://github.com/VlDMlNSh/mediahub-os/blob/work/contour-a-wave216-continuous-qualification-2026-10-20/docs/checkpoints/MEDIAHUB-CONTOUR-A-PUBLISHER-CAPABILITY-GAP-ANALYSIS-WAVE-223-2026-10-20.md

## Existing components checked

- `.github/workflows/astra-autonomous-supervisor.yml`: creates and signs a `mediahub.astra.control-command.v1` command with `ops/control/sign_command.py`, then uploads `astra-authoritative-command` for downstream distributed verification.
- `.github/workflows/astra-gold-unified-qualification.yml`: signs and uploads a run-specific authoritative command artifact. Downstream qualification is gated by explicit `confirm_launch == true`.
- `ops/mesh/artifacts.py`: digest and basic manifest/schema helper, identified in Wave 219.
- `ops/qualification/run_distributed_local_worker.py`: worker still performs `git add -A`, commit and push (main blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`).

## Decision

The signed command artifacts are command-issuance/transport artifacts, not worker source-change bundles. They do not prove path allowlisting, source-file digest validation, lease/replay protection, or a separate publisher identity. Do not treat command-signing as authority to publish worker-generated code.

No complete worker artifact-only publisher was identified in this bounded source search. Existing reusable primitives are command signing/verification, artifact digest/schema checks, and GitHub Actions artifact transport. The missing boundary is a separate publisher that validates a bounded source manifest against the original task and current policy before creating a branch/PR.

## Next bounded action

Inspect `ops/control/sign_command.py`, its verification counterpart, command schema and distributed-verification workflow. Record the exact signed fields and authority checks, then design a distinct source-artifact envelope and negative-test matrix. Do not change authority contracts until publisher capability ownership is explicit.

No code or workflow was changed. PR #397 is Draft; its Astra Verify and Astra Cloud Runtime Validation checks passed on exact head `8ee730e2a5d9038d6f2764cf00e483bd3a5505e0`. Independent review remains outstanding. Contour A remains NOT_PROVEN / BLOCKED; G0–G11 BLOCKED; G11 HUMAN_ONLY.
