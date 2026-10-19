# Contour A — publisher capability gap analysis (Wave 223)

- Date: 2026-10-20
- Status: DESIGN/GAP ANALYSIS; NOT IMPLEMENTATION OR ACCEPTANCE
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Canonical checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Workflow hardening candidate: https://github.com/VlDMlNSh/mediahub-os/pull/397
- Evidence PR: https://github.com/VlDMlNSh/mediahub-os/pull/396

## Exact source evidence

| Source | Blob SHA | Relevant observation |
|---|---|---|
| `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `8d831c2a8fa333977dd86524099568bae2a8db0e` | Trust chain requires authenticated principal, workload identity, explicit capability/policy evaluation, authorized command and State Authority; default deny; audit records do not become a second authority. |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Lease TTL 600s; heartbeat TTL 120s; executor timeout 900s; evidence freshness 86400s; max 3 parallel claims; G11 human-only; missing evidence blocks qualification. |
| `ops/qualification/run_distributed_local_worker.py` | `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1` | Worker directly performs `git add -A`, commit, push, then verifies the remote SHA (lines 663–680). It writes its own result JSON and digest (lines 694–697). |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Current main grants `contents: write` and sets `persist-credentials: true` on all three checkout steps. Draft PR #397 changes these to read-only and non-persisted checkout credentials. |
| `docs/qualification/CURRENT-TRUTH.generated.md` | `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731` | G0–G11 are BLOCKED; overall NOT_PROVEN / BLOCKED; G11 HUMAN_ONLY. |

## Gap decision

PR #397 is a useful least-privilege improvement and both exact-head CI workflows passed at `8ee730e2a5d9038d6f2764cf00e483bd3a5505e0`. It is not sufficient to establish the publisher boundary: the worker still contains direct Git publication code, and the worker workflow's artifact upload is not itself an authorization decision. A worker-generated result digest is integrity metadata, not proof that the worker was authorized to publish.

The existing security contract is the authoritative policy source, but this source audit did not find a worker-specific issuer/capability implementation that authorizes artifact publication. Do not invent a new State Authority or let model/worker output decide its own permissions.

## Minimum artifact/publisher contract to specify before code

1. **Task identity:** immutable task ID, command ID, issuer/workload identity, approved capability ID and policy version.
2. **Source binding:** immutable target SHA, repository identity, permitted output paths and path count/size bounds.
3. **Result manifest:** each file path, byte length, SHA-256, media/type classification, test/verifier evidence references and bounded result metadata.
4. **Freshness:** lease ID/expiry, cancellation/revocation status, task attempt number, nonce/idempotency key and evidence timestamp.
5. **Worker constraint:** worker can write only in its isolated workspace and upload a bounded artifact; no write-capable repository credential or publisher credential.
6. **Publisher constraint:** separate trusted identity validates issuer/capability, policy version, lease/freshness, immutable base SHA, path allowlist, digests, size limits, evidence bundle and replay protection before creating a branch/PR.
7. **Audit:** record principal, workload identity, task/command ID, authorization result, policy version, target SHA, manifest digest, resulting revision, timestamp and trace ID; never record credentials.
8. **Fail closed:** invalid or ambiguous manifest, expired lease, stale/revoked identity, path traversal, extra files, digest mismatch, duplicate task ID or unavailable authorization must reject publication without fallback.

## Required negative tests

- Unknown issuer and insufficient capability are denied.
- Wrong repository or target SHA is denied.
- Absolute paths, `..`, symlinks escaping workspace and unexpected file count/size are denied.
- Missing, malformed or mismatched SHA-256 is denied.
- Expired/stale lease, cancellation, revoked task and replayed idempotency key are denied.
- Worker-supplied publication branch/URL/permissions cannot override controller policy.
- Missing/failed verifier or test evidence is denied.
- Publisher failure never causes worker fallback to direct Git push.
- Audit event contains required provenance but no credentials.

## Next bounded action

Locate any existing trusted publication implementation and the exact authoritative issuer/capability contract before building another service. Compare it to this minimum contract. Then create a separate Draft design/test-contract PR; do not refactor worker Git publication until capability ownership and write surfaces are explicit. Keep PR #397 Draft pending independent review.

No code was changed in this wave. No merge/deployment occurred. Contour A remains NOT_PROVEN / BLOCKED.
