# Contour A head-bound schema-validation CI — Wave 158

Date: 2026-10-18
Status: **HEAD-BOUND SCHEMA CI VERIFIED / CANDIDATE ONLY / NOT QUALIFICATION**

## Exact refs

- Repository: `VlDMlNSh/mediahub-os`.
- Canonical docs base: `docs/mediahub-chat-tree-map-20261012` at `28816f6b523c8cbc878ebd0575b17bc419669889`.
- Code candidate: [PR #363](https://github.com/VlDMlNSh/mediahub-os/pull/363), open/Draft/unmerged.
- Candidate HEAD after CI provenance fix: `15f4646c70e33a1c9e45483ae437750776093993`.
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301), open.
- Prior correction record: [PR #366](https://github.com/VlDMlNSh/mediahub-os/pull/366), docs-only Draft.

## Change implemented

Updated `.github/workflows/cloud-agent-schema-validation.yml` to:
- checkout `github.event.pull_request.head.sha` for pull-request events, falling back to `github.sha` for push/workflow_dispatch;
- assert the actual checkout HEAD equals the intended source SHA;
- record both `event_sha` and `commit_sha`, plus PR base/head SHAs, run ID and attempt;
- fail if a pull-request artifact's `commit_sha` does not equal `pr_head_sha`;
- name the artifact using the checked-out source SHA and run ID.
- Keep read-only repository permissions, pinned action commit SHAs, hash-locked dependencies and GitHub-hosted `ubuntu-24.04` runner.

Workflow blob SHA after update: `47f3f26f823f458ac7a8b7e666ee9cfed6da8be7`.
Commit that updated workflow: `15f4646c70e33a1c9e45483ae437750776093993`.

## CI evidence and artifact read-back

- Run [39163165440](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39163165440), attempt 1: completed successfully; all nine substantive steps passed.
- Artifact ID: `12149676123`; GitHub digest and downloaded archive SHA-256 both `sha256:6aef1787671bc54207790e124d11585807527749f20c63d2e2c79219d4d59417`.
- Provenance JSON verified:
  - `commit_sha` = `pr_head_sha` = `15f4646c70e33a1c9e45483ae437750776093993`;
  - `event_sha` = `0e66b5a4a8803da5642379d197b139316418c331`, the synthetic `refs/pull/363/merge` commit;
  - `pr_base_sha` = `28816f6b523c8cbc878ebd0575b17bc419669889`;
  - `run_id` = `39163165440`, `run_attempt` = `1`.
- Schema report: PASS, 182 checks, 0 failures: 3 positive fixtures, 13 mutation negatives and 166 generated nested-required negatives.
- Semantic report: PASS, 1 positive bundle, 26 negative cases rejected, 0 failures.
- All three schema pins match the canonical schema blob IDs recorded in Wave 155.
- The artifact's archive digest was checked against GitHub metadata and matches exactly.

## Decision and limits

This closes the narrow CI identity gap for PR #363's schema-validation run: the workflow's provenance now proves which source SHA was checked out even though the GitHub event itself is a merge-ref event.

It does **not** prove issuer/grant/revocation authority, freshness/replay prevention, live provider route qualification, signed A0 ingress, artifact authenticity beyond GitHub artifact metadata, target-manifest acceptance, or self-hosted worker isolation. Schema/semantic reports are synthetic fixture checks. No merge, deployment, provider calls, secret reads, or worker-runtime changes were performed.

PR #363 remains Draft/open/unmerged pending independent review. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains gated.

## Next bounded step

Independently review the workflow change and validator negative coverage; then trace the actual worker dispatch path to define an architecture-aligned test seam for issuer signature, audience/node binding, freshness, replay marker and target SHA/current HEAD binding. Do not invent a token format or promote the fixture suite into a live authority contract.
