# Contour A Wave 225 — signed-context reuse boundary

Date: 2026-10-20. Status: source analysis only; no implementation or acceptance.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
Draft hardening PR: https://github.com/VlDMlNSh/mediahub-os/pull/397
Evidence PR: https://github.com/VlDMlNSh/mediahub-os/pull/396
Wave 224: https://github.com/VlDMlNSh/mediahub-os/blob/work/contour-a-wave216-continuous-qualification-2026-10-20/docs/checkpoints/MEDIAHUB-CONTOUR-A-ARTIFACT-REUSE-WAVE-224-2026-10-20.md

## Exact source observations

- `ops/control/sign_command.py`, blob `fc6943a79cefdf06e59d6e32771d2df551b2f0e9`: defines `mediahub.astra.control-command.v1`, requires command identity, node, operation, target SHA, workflow_only, owned_paths, exclusive_actions and issued_at; enforces a bounded freshness window; signs canonical JSON with node-specific HMAC-SHA256. This is command issuance/signing.
- `tests/control/test_sign_command.py`, blob `af3b93c1ed482d1058873a1cea65237b79ca6b74`: covers signature computation, tamper sensitivity, missing required fields, stale command, and secret suppression.
- `ops/qualification/produce_distributed_node_attestation.py`, blob `d2d423325558e877845f848314ceaf583a71fd8e`: produces node-bound evidence with command ID, node ID, target SHA, producer identity, auth key ID and HMAC signature.
- `ops/qualification/produce_distributed_verification_evidence.py`, blob `ee3a1fa1d364da5a6d57a47ab0cfdbd3d0897a6f`: validates per-node evidence against expected command/node/SHA and checks HMAC signature with constant-time comparison; emits bounded aggregate evidence.
- `.github/workflows/astra-distributed-verification.yml`, blob `648f56badd2b919b822b4fe4b61f285cca99ed93`: read-only repository permission, node-specific HMAC secrets, uploads fresh attestations; evidence transport is not a state authority.

## Reuse decision

Reuse the command identity/target-SHA/freshness conventions and existing signed attestation pattern as references for provenance. Do not reuse a node attestation as a source-artifact signature without a distinct schema and subject: an attestation says which node performed bounded checks, while a source artifact manifest describes files proposed for publication. The current source audit did not identify a dedicated verifier for the command signer itself outside the command signer and the distributed evidence verification path.

## Missing contract elements for a source artifact publisher

- Separate schema and version for worker output manifest.
- Explicit issuer/workload identity and publisher capability authorized by the governing policy.
- Repository ID, immutable target SHA, task ID, lease and cancellation/revocation state.
- Normalized relative-path allowlist; reject traversal, symlink escapes, unexpected file types and oversized bundles.
- Per-file SHA-256 and total size bound; verify digest after transport.
- Fresh test/verifier evidence references and evidence digest.
- Idempotency/replay protection and duplicate task rejection.
- Separate publisher identity with no credentials exposed to the worker.
- Audit record binding decision, policy version, manifest digest and resulting commit/PR SHA.
- Negative tests for all invalid states; fail closed when policy service or evidence is unavailable.

## Next action

Read the authoritative A0 issuer/capability contract and the current command admission/queue claim implementation, then map each required publisher decision to an existing owner. Do not introduce a second authority or infer write permission from a valid HMAC alone. Keep PR #397 Draft; its two CI workflows passed on exact head `8ee730e2a5d9038d6f2764cf00e483bd3a5505e0`. Current truth remains NOT_PROVEN / BLOCKED.
