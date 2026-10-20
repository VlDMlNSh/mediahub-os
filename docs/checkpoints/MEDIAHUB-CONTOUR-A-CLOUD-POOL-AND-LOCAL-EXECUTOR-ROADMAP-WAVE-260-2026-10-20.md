# Wave 260 — Contour A cloud pool roadmap and Gemini scope control (2026-10-20)

## Decision recorded
The development sequence is clarified: finish the existing three-agent Gemini controller only to the minimum secure, reviewable, operationally proven state; do not let repeated Gemini-only hardening consume the entire Contour A schedule. In parallel, inventory and qualify the full candidate cloud-agent/provider pool against the existing registry and architecture. Enable routes incrementally only after their gates pass. Local executors and Jarvis architecture/design begin after cloud-pool deployment and successful operational qualification; their deployment follows a separate full qualification and acceptance gate.

This is a forward plan, not an architecture/governance acceptance, provider entitlement, live dispatch authorization, or proof that any agent is currently available.

## Evidence snapshot
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing cloud-agent issue #301 remains OPEN: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Controller-only Gemini PR #421 remains OPEN and Draft; head `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`, base/main `80be45a70732b1d568164571d4273a6397792c3b`. No review submissions were returned. PR: https://github.com/VlDMlNSh/mediahub-os/pull/421
- The prior exact-head CI successes are recorded in Wave 259; this wave did not run new CI and does not claim those checks apply to any future commit.
- Issue #301 explicitly says the CAF-Q-001…CAF-Q-015 queue is documentary, schemas are candidates pending standards validation/negative fixtures, and no provider routes are verified/enabled. Its current disposition is planning/source evidence only.
- Branch protection could not be independently verified through the available GitHub connection (previous API response 403). No controller dispatch or Gemini invocation occurred.

## Execution plan

### Track A — close the existing Gemini entry point, bounded
1. Obtain genuine independent review for PR #421 covering reusable-workflow caller context, job permissions, fixed scope, secret flow and fail-closed aggregation.
2. Verify branch-protection/ruleset requirements through an authorized read path; retain UNKNOWN if unavailable.
3. Complete a controlled negative caller-context test that cannot invoke Gemini or expose provider secrets, plus positive/negative contract fixtures and actionlint.
4. Revalidate exact-head CI and source SHA. Keep PR Draft/unmerged until all gates and governance requirements pass.
5. Only then request/perform the separately authorized first operational batch; record controller and child run/job IDs, exact refs, conclusions, evidence artifact digests and independent review. This plan does not authorize a live run now.

### Track B — build the broader cloud-agent pool in parallel
1. Reuse `ops/qualification/provider_model_registry.json`; do not create a duplicate registry. Census all existing provider/model registry entries, consumers, schemas, qualification records and relevant roadmap issues.
2. Build a provider-neutral candidate matrix covering: provider/model and stable upstream integration; access/eligibility evidence; free-tier/quota/renewal semantics; authentication/OIDC or runtime-secret requirements; supported regions/data policy; rate limits; task classes; structured-output/tool support; source-bound execution; cost/budget ceiling; cancellation/revocation; fallback rules; provenance/evidence output; maintenance/security posture.
3. Prioritize routes by usable verified capability, not by marketing claims. Candidate research may include available free-tier cloud coding/reasoning providers and hosted agent runtimes discussed in the repository; no provider is marked enabled until source evidence and policy gates are checked.
4. Implement one route at a time behind the same issuer/capability, task-envelope, allowlist, quota, timeout, cancellation, redaction, output-quarantine and evidence-manifest contracts. Keep paid routes disabled unless separately authorized for the exact destination and budget. No VPN/proxy/region spoofing.
5. Validate all schemas with a standards-compliant Draft 2020-12 validator, format assertions and positive/negative fixtures; record tool/version/digests. Independently review semantic reference resolution and route-to-registry mapping.
6. Add pool-level contract tests: unavailable/expired quota, provider refusal, timeout/cancel, malformed output, prompt injection, missing source SHA, secret leakage, ambiguous route, budget exhausted, retry exhaustion and provider fallback. Default is fail closed.
7. Operationally qualify each route with small read-only/non-sensitive tasks first; record exact run IDs, model/provider IDs, task/ref, quota evidence, artifacts/digests, costs (if any), failure/retry behavior and reviewer disposition.
8. Deploy the pool only when there is a reproducible route inventory, accepted schemas/contracts, independent review, policy/authority gates, end-to-end evidence, rollback/revocation drill and documented acceptance. “Pool designed”, “implemented”, “tested”, “qualified”, “deployed” and “accepted” remain distinct states.

### Track C — local executors and Jarvis, after cloud pool acceptance
1. Start a requirements and component-selection study only after Track B deployment plus successful operational qualification/independent acceptance.
2. Compare stable existing open-source components before custom development. Define threat model, trust zones, issuer/capability boundaries, local secret custody, filesystem/network isolation, job lifecycle, resource quotas, audit, recovery, update/supply-chain verification and emergency stop.
3. Preserve strict separation: Jarvis is not the Product State Authority; ASTRA A0 and MediaHub Product State Authority keep their defined independent authorities. No component may mint or bypass issuer/capability.
4. Publish reference architecture, bill of materials, compatibility matrix, threat model, acceptance tests and migration/rollback plan. Deployment only after full qualification and a separate acceptance decision.
5. Contour B remains blocked until Contour A is deployed and independently accepted.

## Parallel working cadence
Each /next should choose the highest-value bounded action across Tracks A and B, avoiding repeated low-yield Gemini-only static checks when an independent provider/schema/registry task is available. Keep at most one well-defined integration wave per change set; attach evidence and update map/checkpoint/roadmap after every wave.

## Explicit non-actions and blockers
- No Gemini/cloud-agent dispatch, provider API calls, secret reads, merge, deployment or qualification was performed in this wave.
- No provider availability, free quota, region eligibility or route enablement is claimed.
- Independent review, authorized branch-protection verification, non-invoking negative caller-context test and standards-compliant schema validation remain open.
- This roadmap entry records the owner's requested sequencing; it does not silently amend Baseline 2.0 or grant runtime capabilities.

## Next bounded step
Census the current provider registry and its consumers, then select the smallest high-value schema-validation/negative-fixture gap that advances multiple cloud routes without invoking any provider. In parallel, keep PR #421 waiting for independent review and authorized protection evidence.

