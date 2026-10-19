# MediaHub OS Contour A — A0 issuer/admission to worker publication trace (Wave 178)

- Date: 2026-10-19
- Status: SOURCE-BOUND REVIEW; governance unresolved; no implementation, dispatch, qualification, or acceptance.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Related proposal: [Wave 177 trusted publisher boundary design](MEDIAHUB-CONTOUR-A-TRUSTED-PUBLISHER-BOUNDARY-DESIGN-WAVE-177-2026-10-19.md)
- Related candidate: [PR #375](https://github.com/VlDMlNSh/mediahub-os/pull/375)

## Exact sources re-read

| Source | Ref/blob SHA | Finding |
|---|---|---|
| `ops/qualification/run_distributed_local_worker.py` | `main`, `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | `load_task()` shape-checks JSON and required fields. `main()` binds task node, configured node, executor, target SHA and clean checkout; no canonical signed A0 envelope verification is shown before branch creation. Worker directly commits/pushes and checks remote SHA. |
| `ops/mesh/admission.py` | `main`, `46e92d3c4f9b9865356443403e9ebd34587996cd` | `admit_executor()` validates node state, a capability record's schema/fields, execution authority and qualification state. This is local record/policy validation; it does not establish an issuer signature, trust-anchor verification, expiry/revocation, replay protection or binding to the worker command/target. |
| `ops/mesh/validators.py` | `main`, `416a7ecaf4add9d0b81f0467cf426d9c7deb3ec7` | Capability validation checks required fields, schema version, executable digest shape and authority enum. The inspected capability path is not itself a cryptographic issuer verifier. Heartbeat validation is a distinct mechanism and must not be treated as command-envelope attestation. |
| `runtime/mediahub_runtime/task_ingress.py` | `main`, `59e1254aa61cc8f55f53bd1e179631e81c441393` | File ingress validates task-contract shape and accepts an `approval_state` field. It does not verify an external issuer/signature in this module. It is a separate local ingress path, not proof of A0 worker authorization. |
| `docs/checkpoints/MEDIAHUB-A0-ISSUER-GOVERNANCE-DECISION-GATE-MATRIX-WAVE-149-2026-10-18.md` | docs branch, `9c1a02dc125b37abea9284f0c0aa5deb571f13e7` | GOV-CAP-01…07 remain unselected/open; accountable issuer, principal lifecycle, verifier, trust-anchor custody, revocation, delegation and independent acceptance decisions remain unresolved. |
| `docs/checkpoints/MEDIAHUB-CONTOUR-A-TRUSTED-PUBLISHER-BOUNDARY-DESIGN-WAVE-177-2026-10-19.md` | docs branch, `1ebfc8342c7c18d211edb1e095c6bb9b0df1de8f` | The separate publisher proposal already records the needed security invariant and tests; it remains proposal-only and does not authorize implementation or dispatch. |

## Trace conclusion

The repository contains useful **local admission/validation components**, but the reviewed paths do not demonstrate an accepted, cryptographically verified A0 issuer/capability bound to the exact worker command, task digest, node/audience, repository, target SHA and publication scope. It would be incorrect to wire `ops/mesh/admission.py` directly into the worker and call the issuer gap closed: its current contract validates a capability-shaped record, not the missing trust lifecycle.

The canonical decision gate remains governance, not library selection. Do not invent a signing scheme, key lifecycle, issuer role or implicit delegation. Preserve the separation between Jarvis mission coordination, ASTRA A0 engineering workflow state, and MediaHub Product State Authority. No product-state authority is inferred for the publisher.

## Next safe implementation boundary

Until issuer decisions are accepted, limit code changes to non-authoritative static policy/negative tests using synthetic fixtures. Do not add a production verifier or mint/consume real credentials. For the publisher proposal, the next engineering-ready artifact should be a contract/test matrix only:
- missing/untrusted issuer and malformed signature;
- capability wrong operation/resource/scope/audience/node;
- task or target digest mismatch;
- expiry, stale revocation state, replay and duplicate command;
- repository/ref mismatch and forbidden/oversized patch;
- tampered worker Git metadata or executable handoff;
- ambiguous run/artifact correlation, failed push and remote SHA mismatch;
- audit sink unavailable and cancellation/recovery races.

A future implementation must derive expected behavior from an accepted issuer/MH-12/R-06 contract, reconstruct output from a clean checkout at immutable target SHA, independently validate the normalized diff, and keep all publish credentials outside the model-controlled process tree.

## Scope and evidence limits

- This was read-only source review plus documentation recording.
- No tests were executed in this pass.
- No worker or workflow was dispatched; no provider called; no credential values read or modified.
- No branch was merged and no deployment or qualification was performed.
- Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**; Contour B remains gated.
