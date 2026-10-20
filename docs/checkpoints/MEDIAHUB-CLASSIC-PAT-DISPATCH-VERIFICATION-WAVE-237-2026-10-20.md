# MediaHub OS — Classic PAT workflow_dispatch verification (Wave 237)

- Date: 2026-10-20
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **PASS for workflow_dispatch using `MEDIAHUB_GITHUB_TOKEN`; temporary test files removed**
- Governance tracking: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Objective

Determine whether the classic PAT stored as Actions secret `MEDIAHUB_GITHUB_TOKEN` can dispatch a harmless workflow, after the earlier fine-grained PAT secret `PAT_DISPATCH` returned HTTP 403. Neither token value was printed, passed in arguments, or committed.

## Test design

Two temporary workflows were added to `main`:

- `.github/workflows/mediahub-token-dispatch-smoke-target.yml`: only `workflow_dispatch`; one bounded job that verifies the event name and prints a PASS line.
- `.github/workflows/mediahub-token-dispatch-smoke-caller.yml`: push-triggered only by its own file path; sends a REST `POST /actions/workflows/mediahub-token-dispatch-smoke-target.yml/dispatches` using `secrets.MEDIAHUB_GITHUB_TOKEN`.

The caller did not echo the token. On non-204 responses it prints the API response body only.

## Evidence — PASS

- Caller run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39383103249
- Caller run ID: `39383103249`; job ID: `118496508757`; conclusion: `success`.
- Caller log: `workflow_dispatch_http_status=204` and `PASS: MEDIAHUB_GITHUB_TOKEN dispatched the temporary smoke target`.
- Dispatched target run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39383110978
- Target run ID: `39383110978`; event: `workflow_dispatch`; conclusion: `success`.
- Target job ID: `118496536978`; conclusion: `success`.
- Commit that triggered caller: `48cd45187a3a7c52368204577ab7857e85b44606`.
- Caller and target were subsequently deleted from `main`. Re-read of both paths returned 404.
- Final `main` HEAD after cleanup: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.

This establishes that the classic PAT secret can dispatch this temporary workflow. It does not validate the payloads, authorization policy, replay/revocation controls, or safe operation of the Gemini engineering workflows themselves.

## Documentation read-path status

- Master Roadmap read-back on canonical documentation ref: blob SHA `beef785c787702dc174cf9a5515bac8c9f4b292f`; 317,131 Unicode characters returned by the file connector (the previous byte-counting Actions probe verified 320,659 decoded bytes).
- Canonical map path `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md`: the available file connector again returned empty content, blob SHA `59973971096b716664e7c6cb6286af6fe84e4a1a`. No blind rewrite attempted. The map was not updated in this wave.
- Canonical documentation branch remains distinct from `main`; test changes were made and removed on `main`, not promoted into the documentation branch.

## Security and next step

1. Dispatch capability is now proven with `MEDIAHUB_GITHUB_TOKEN`; the earlier 403 remains specific to the tested `PAT_DISPATCH` secret/configuration.
2. Because the classic token was described as having broad full access, do not use it as a general-purpose credential for model-execution jobs. Prefer a least-privilege fine-grained PAT or GitHub App installation token scoped to the repository and only required permissions. Revoke/rotate the broad classic token after migrating any dependent workflow.
3. Keep model worker and publisher credentials separate. A successful dispatch is not an issuer/capability boundary and does not justify giving the worker write/publish authority.
4. Continue A0 issuer/capability contract and worker/publisher separation work; add negative tests for forged, stale, replayed, revoked, or over-scoped envelopes before qualification.

## Contour A status

**NOT PROVEN / BLOCKED.** This wave proves only a narrow API operation. It does not qualify the autonomous engineering environment or authorize Contour B.
