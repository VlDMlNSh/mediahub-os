# Master Development Roadmap — Priority Amendment: Cloud Agent Pool First (Wave 483, 2026-10-30)

## Decision

**The first delivery priority for MediaHub OS is to design, implement, qualify, deploy and independently accept the Contour A cloud agent pool. Server hardware procurement, provisioning, expansion and Contour B server-side work are deferred until Contour A cloud pool is successfully in production and independently accepted.**

This amendment changes delivery order, not security policy or authority boundaries. It does not authorize secrets access, provider calls, controller dispatch, infrastructure mutation, deployment or bypass of Issue #301 gates.

## New top-level delivery order

### Priority P0 — Cloud Agent Pool / Contour A (FIRST)

Deliver a production-operable, GitHub-hosted, ephemeral cloud execution pool without requiring an owner-operated always-on server or public inbound listener.

Scope:
1. Close A0 issuer, ingress, lease, cancellation and crash-recovery authority gates; close R-06 audit/privacy gates.
2. Identify and accept the authoritative runner/workspace/network target manifest. Workers must initiate outbound HTTPS; do not assume fixed egress IP or provider region eligibility.
3. Validate task-envelope, agent-registry and evidence-manifest v0.2 schemas using standards-compliant JSON Schema Draft 2020-12 validation, format assertions, positive and negative fixtures, pinned tooling and digests.
4. Obtain independent review of schema semantics, issuer/capability, data policy, audit and privacy controls.
5. Harden existing GitHub-hosted Gemini read-only workflows: immutable checkout SHA, strict refs/paths/model allowlists, full-SHA action pins, output quarantine, evidence manifest and least-privilege permissions.
6. Implement the smallest authorized read-only worker/queue slice; use isolated ephemeral GitHub-hosted runners, runtime-only secret injection and fail-closed admission.
7. Qualify the approved free cloud model/provider routes, account/entitlement quota ledger, renewable quota/reset handling, retry/backoff and route isolation. Paid fallback remains denied unless a separate explicit budget authorization exists. No provider credential or route is assumed available merely because configuration exists.
8. Execute controlled controller-owned batches only after all governance gates pass; preserve immutable target SHA, controller/child run IDs, job IDs, artifacts and digests, terminal states, tests and independent review.
9. Add agents to the pool only after identity, issuer, capability, scope, model/provider route, data classification, quota, expiry/revocation and evidence checks pass.
10. Demonstrate safe cancellation, recovery, replay resistance, concurrency isolation, audit completeness, secret non-disclosure and budget/quota fail-closed behavior.
11. Complete production readiness review, deploy the cloud pool, perform an agreed soak/operational observation period, and obtain independent acceptance.

Acceptance exit criteria for P0:
- A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy gates accepted.
- Authoritative runner/workspace/network target manifest accepted.
- All required schemas pass Draft 2020-12 validation and positive/negative fixtures.
- First read-only worker has immutable provenance, isolated execution, secret isolation and independent review.
- Controlled cloud agent execution is repeatable and evidence-complete; quota exhaustion, reset, cancellation, replay and provider uncertainty fail closed.
- Production deployment and soak evidence recorded.
- Independent acceptance explicitly recorded. CI success alone is not deployment or acceptance.

### Priority P1 — Cloud Pool Operational Expansion

Only after P0 acceptance:
- Expand agent roles and bounded parallelism under the accepted issuer/capability model.
- Add further approved free cloud routes/providers after security, data-policy, quota and quality qualification.
- Improve scheduling, renewable quotas, recovery, cost controls, observability and evidence retention.
- Keep patch-writing, PR promotion, merge and deployment as distinct authority gates.

### Priority P2 — Server Hardware / Local Compute Contour

**Blocked until P0 is deployed and independently accepted.**

After the P0 exit criteria are met:
- Reassess actual local-compute requirements and workload split using production cloud-pool measurements.
- Only then select, procure or provision server hardware.
- Qualify SentinelX hosts, local executor identity, capabilities, allowlists, network boundaries and local model routes.
- Integrate server equipment as a separate local-compute contour; it must not become a hidden dependency or transport for the Gemini cloud controller.
- Preserve cloud-first operation and explicit failover policy; do not introduce paid fallback or implicit local authority.

### Priority P3 — Contour B

Contour B remains gated until Contour A cloud pool has production deployment evidence and independent acceptance. Server hardware readiness alone does not unlock Contour B.

## Governance invariants

- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains the controlling ordered execution tracker. Its current sequence is preserved: A0/R-06 → authoritative target manifest → schema validation → independent schema review → Gemini workflow hardening → smallest read-only worker → controlled dispatch → additional agents.
- No owner-operated persistent server or public inbound listener is required for the default cloud pool.
- No proxy/VPN/region-spoofing design; no assumption of stable GitHub-hosted runner egress IP.
- Secrets remain runtime-injected and must never enter repository content, prompts or artifacts.
- No paid fallback by default; no hidden quota exhaustion bypass.
- Jarvis coordinates missions; ASTRA A0 owns its bounded execution authority; MediaHub Product State Authority alone owns canonical product-state mutation.
- Preserve historical IDs and Baseline 2.0 as the functional reference.
- Keep PLANNED, IMPLEMENTED, TESTED, VERIFIED, QUALIFIED, DEPLOYED and ACCEPTED distinct.
- This amendment does not authorize a dispatch, provider call, credential access, infrastructure change, merge or deployment.

## Current evidence and blockers at amendment time

- Issue #301 OPEN; ordered gates remain outstanding.
- PR #594 (Wave 482 issuer source audit) OPEN/DRAFT/UNMERGED; issuer provenance gap documented, no runtime remediation.
- PRs #590–#593 OPEN/DRAFT/UNMERGED; quota-ledger and router design work is not accepted.
- Gemini controller batch: NOT RUN; do not bypass controller gates.
- SentinelX: zero connected hosts; enrolled Mac mini offline; two dev hosts disabled. Local/Claude work is not a dependency for P0 cloud pool.
- Cloud pool production deployment and independent acceptance: NOT VERIFIED / NOT ACHIEVED.
- Server hardware procurement/provisioning: DEFERRED.

## Change control

This is a roadmap-priority amendment recorded as a dedicated document and linked from the canonical map/checkpoint. The legacy roadmap file path specified in earlier project instructions returned GitHub Contents API 404 on both `main` and the canonical documentation branch during Wave 483 retrieval. Its contents were therefore not overwritten or reconstructed from assumptions. The amendment must be incorporated into the canonical master-roadmap artifact once its authoritative path/blob is recovered.

## References

- [Issue #301 — Contour A cloud-agent fabric](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Wave 482 — A0 ingress issuer source audit](MEDIAHUB-A0-INGRESS-ISSUER-SOURCE-AUDIT-WAVE-482-2026-10-30.md)
- [Canonical chat tree map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
