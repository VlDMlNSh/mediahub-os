# Contour A issuer and worker trust-hardening plan — Wave 150 — 2026-10-18

## Purpose
This plan supplements the Master Development Roadmap and the Wave 149 continuation checkpoint. It records the highest-priority source finding from Wave 150 and gives the next chat a concrete, ordered work queue.

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Map addendum: ../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-149-2026-10-18.md
- Master roadmap: MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Wave 149 continuation checkpoint: MEDIAHUB-CONTINUATION-CHECKPOINT-ADDENDUM-WAVE-149-2026-10-18.md
- Wave 150 source report: MEDIAHUB-CONTOUR-A-SIGNED-INGRESS-AND-WORKER-TRUST-GAP-REPORT-WAVE-150-2026-10-18.md
- Governing Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #358: https://github.com/VlDMlNSh/mediahub-os/pull/358

## Priority 0 — accepted issuer contract before implementation
The current worker entry point `ops/qualification/run_distributed_local_worker.py` parses task JSON and validates required fields, node binding, executor, target SHA/current HEAD and clean workspace. The reviewed code does not validate a canonical signed A0 envelope before execution. This is HIGH/BLOCKING for trusted autonomous ingress qualification.

Do not invent a signing scheme or key lifecycle. Obtain explicit accepted decisions for:
- issuer authority and permitted principals;
- principal enrollment, rotation, revocation and compromise response;
- verifier location and trust-anchor custody;
- audience/node binding and capability scope;
- canonical task-envelope digest and target/ref/source SHA binding;
- issued-at/expiry/freshness and clock-skew policy;
- nonce/replay/idempotency behavior and bounded retries;
- delegated authority limits and independent acceptance evidence;
- R-06 audit/privacy retention, redaction and outage/fail-closed behavior.

Only after decisions are accepted, derive a versioned verifier contract and negative-test matrix from the accepted A0/MH-12/R-06 contracts.

## Priority 1 — implement and test signed ingress
- Verify the signed envelope in the worker entry point before any task execution or branch creation.
- Bind `command_id` to the verified envelope, not merely to a workflow input/environment variable.
- Fail closed on missing/invalid signature, unknown/revoked issuer, insufficient capability, wrong audience/node, task digest mismatch, target SHA/ref mismatch, expired/future/stale envelope, replay, invalid idempotency and unavailable trust/revocation state.
- Test malformed/absent fields, signature mutation, wrong key/issuer, expired/future timestamps, stale revocation data, replay, duplicate requests, wrong node/target, changed task digest, unknown capability and verifier outage.
- Do not expose keys, signatures containing sensitive payloads, raw provider responses or secret values in logs/artifacts.

## Priority 2 — authoritative provenance and evidence acceptance
- Capture authoritative GitHub workflow ID/run ID/job ID/attempt/event/ref/source SHA and artifact ID/digest.
- Bind those fields to the accepted task-envelope digest and validated worker result.
- Reject artifacts where schema/status/command/task/node/executor/target/source SHA/branch head do not match; do not trust worker-supplied claims alone.
- Independently compare uploaded artifact digest and remote branch SHA with GitHub-derived metadata; quarantine mismatches and retain an auditable rejection record.

## Priority 3 — execution isolation
- Current `.github/workflows/astra-distributed-local-worker.yml` uses self-hosted runner labels `mediahub-control`, `mediahub-provider`, and `astra-control`; this is not GitHub-hosted ephemeral execution.
- Qualify the actual trust boundary: host identity, account permissions, filesystem/worktree isolation, cleanup, persistent processes, runtime-only secret injection, cancellation, network/data policy, runner reuse and compromise recovery.
- Do not describe this route as deployed/qualified or substitute documentation for independent evidence. GitHub-hosted ephemeral workers remain the preferred target architecture if compatible with required execution capability and policy.

## Priority 4 — queue correlation and registry semantics
- PR #358 fixes substring run matching with exact/fresh correlation and ambiguity rejection. Exact CI evidence exists for its current reviewed head, but the PR is still open/Draft/unmerged; refresh head/status/checks and governance before integration.
- Main still contains old substring matching until the fix is integrated.
- `ops/qualification/provider_model_registry.json` is a qualification candidate catalog, not an authorization source. Only `ops/qualification/qualify_execution_backends.py` is a confirmed consumer in the bounded review; the autonomous queue files reviewed do not reference it. Complete repository-wide consumer mapping before designing runtime binding.
- Keep provider route admission BLOCKED until official documentation, account/project entitlements, data/egress policy, quota/reset, budget, expiry/revocation, observability and negative tests are evidenced.

## Definition of done for next bounded pass
1. Refresh exact refs/SHAs, Issue #301, PR #333/#358 and CI state.
2. Read accepted issuer governance checkpoint and map unresolved owner decisions; do not implement disputed authority semantics.
3. Trace all provider registry and agent registry consumers using repository-wide search/tree evidence.
4. Produce either an accepted-contract-backed implementation with negative tests, or a precise governance blocker with the missing decision owners/fields.
5. Update report/map/checkpoint with read-back blob and commit SHAs.

## Non-negotiable gates
Jarvis remains mission coordination; ASTRA A0 owns only accepted internal engineering queue state; MediaHub Product State Authority alone owns canonical product-state mutation. Human launch authority remains distinct. No self-qualification/self-promotion. No provider policy/region/quota bypass. Contour B remains blocked until Contour A is deployed and independently accepted.

## Wave 150 evidence boundary
Source review and documentation only. No code or runner settings changed; no secrets were read; no model/provider was called; no worker was dispatched; no deployment or qualification occurred.
