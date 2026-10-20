# MediaHub OS — PAT_DISPATCH API read/write and workflow-dispatch probe (Wave 236)

- Date: 2026-10-20
- Repository: `VlDMlNSh/mediahub-os`
- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **PARTIAL PASS — large-file reads and Git-ref writes verified; workflow_dispatch remains blocked**
- Related governance issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Scope

Verify that the repository Actions secret `PAT_DISPATCH` is populated and can read large documentation files and perform a bounded repository write. Separately attempt to dispatch a harmless workflow through the GitHub REST API. The token value was never printed or copied into chat.

## Evidence

### Large-file reads — PASS

A temporary GitHub Actions workflow read the files through the GitHub Contents API using `secrets.PAT_DISPATCH`, decoded the returned base64 payload, and compared the decoded byte count to the API's declared file size.

| File | Decoded bytes | Blob SHA | Result |
|---|---:|---|---|
| `docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md` | 320,659 | `beef785c787702dc174cf9a5515bac8c9f4b292f` | PASS, full payload |
| `docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md` | 861,030 | `b9978ca997f966c1d3fc0c9baa2520a0c5366826` | PASS, full payload |

Successful probe run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39380368212

### Git write scope — PASS

The workflow created a uniquely named temporary ref and deleted it in the same job:

- Create ref: HTTP 201
- Delete ref: HTTP 204
- The temporary workflow branch was subsequently removed; a read-back of the branch endpoint returned 404.
- Successful cleanup run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39381019409

This proves the tested token can read these Contents API files and create/delete Git refs. It does **not** prove every repository permission is functional.

### Workflow dispatch — FAIL / BLOCKED

The probe attempted `POST /repos/VlDMlNSh/mediahub-os/actions/workflows/pat-dispatch-smoke-target.yml/dispatches`. At the time of the attempt, the target workflow existed on `main`. GitHub returned:

```
HTTP 403
Resource not accessible by personal access token
```

Run and logs: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39380932412

The probe workflow itself launched on a push event and successfully read the large files, so Actions execution and secret injection work. However, `PAT_DISPATCH` has **not** been shown to have working workflow-dispatch authority. The 403 does not by itself distinguish a missing Actions write permission from repository/organization policy restrictions.

The temporary target workflow was removed from `main`; the temporary probe branch was removed. No PAT value was exposed in logs.

## Repository refs and cleanup

- `main` before the temporary target test: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`
- `main` after adding and removing the temporary target workflow: `8761f734031ef0b880b974cea24c2463e7a22046`
- The temporary target file is absent from `main`; the two test commits remain in history, so the branch SHA advanced even though the temporary file was removed.
- Canonical documentation branch at report preparation: `3f2ca17f40dffea624b4070e06187c7331086591`
- Existing PR #375 remains open, draft, and unmerged: https://github.com/VlDMlNSh/mediahub-os/pull/375

## Limits and next action

1. In the fine-grained PAT settings, verify repository selection is exactly `VlDMlNSh/mediahub-os` and **Actions: Read and write** is enabled; verify token status/expiry and any organization policy that limits PAT workflow dispatch.
2. Do not paste the token into chat, task JSON, command-line arguments, or logs.
3. Re-run a minimal dispatch probe only after the permission/policy setting is corrected. Keep the token least-privileged; broad access is not evidence that every API operation is allowed.
4. Continue Contour A issuer/capability, publisher separation, and independent acceptance work. This probe does not qualify Contour A.

## Canonical status

- The canonical map is still the map on `docs/mediahub-chat-tree-map-20261012`; it was not overwritten.
- The map's Contents API response remains empty in the available connector, so this pass did not attempt a blind full-file rewrite.
- Contour A remains **NOT PROVEN / BLOCKED**.
