# Canonical map addendum — Wave 285 (2026-10-20)

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md) on [canonical branch](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).
- Continuation checkpoint: [current continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md).
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md).
- Full source trace and field matrix: [Wave 285 A0 ingress, issuer, approval and producer trace](../checkpoints/MEDIAHUB-A0-INGRESS-ISSUER-APPROVAL-PRODUCER-TRACE-WAVE-285-2026-10-20.md).
- Related Wave 284 probe triage: [report](../checkpoints/MEDIAHUB-GEMINI-CALLER-PROBE-STARTUP-FAILURE-TRIAGE-WAVE-284-2026-10-20.md) and [map addendum](MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-284-2026-10-20.md).
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Separate controller candidate: [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421).

## Confirmed source gap

On `main` at `80be45a70732b1d568164571d4273a6397792c3b`, `runtime/mediahub_runtime/task_ingress.py` (blob `59e1254aa61cc8f55f53bd1e179631e81c441393`) parses flat JSON from an injected inbox and passes the plain `approval_state` string into `AstraTaskRequest`. `runtime/mediahub_runtime/astra_gateway.py` (blob `10985e4ad8f682313d08e7492ecc1856a8bce20f`) uses the value `approved` as the sensitive-action gate; the inspected path does not independently verify a trusted issuer/approval record or signature. The service entry point `runtime/mediahub_runtime/astra_service.py` (blob `6aa2d09fc8737ccc0ba7f05bd13a15a0ebde7129`) is inert and does not bind the file ingress.

No authoritative producer, inbox ACL or separate verifier was established in this bounded trace. This is **UNKNOWN / NOT PROVEN**, not proof that an external writer does not exist and not proof of an exploit or executed action. No runtime source was changed.

## Contract layering and guardrails

- The typed `AuthorizationContext` currently carries only `principal` and `capability`; the local allow-list does not establish external issuer provenance.
- Signed control commands, node-attestation HMACs and heartbeat authentication are separate contracts, not proof of task-approval issuance.
- The canonical governance YAML G11 approval is human-only and SHA/evidence-bound, but the inspected ingress path does not consume this record.
- Cloud-agent task envelope v0.2 and the Wave 269 mission envelope are proposed artifacts, not accepted replacements for the hard-coded local task contract.
- Wave 149 GOV-CAP issuer/attestation ownership decisions remain unresolved; Wave 278 preserves the distinction between A0 engineering coordination state and MediaHub Product State Authority.

## Next gate

Identify the authoritative task writer, actual inbox/runtime binding and ACL; resolve issuer/approval ownership and A0 vs Product State Authority semantics under governance; then choose one canonical contract extension point and add synthetic static/mock-only negative tests. No production verifier/schema, live dispatch or alternate queue is authorized by this addendum.

For PR #421, the dedicated read-only Wave 284 observer successfully captured an actual PR caller context and verified that it was not the trusted controller without invoking Gemini. The next exact-head `Astra Verify` run must cover the Wave 284 caller and observer paths after the lint target was corrected; PR remains OPEN/DRAFT/UNMERGED pending independent review and branch/ruleset evidence. No Gemini dispatch, secrets/provider call, merge, deployment or qualification occurred.

**Disposition:** ingress trust boundary NOT PROVEN / BLOCKED; Contour A NOT_PROVEN / BLOCKED; Contour B remains gated.
