# Contour A master-roadmap addendum — Wave 149 — 2026-10-18

## Purpose
Make the current Contour A work queue durable and resumable from any ChatGPT chat through `/next`. This addendum supplements the Master Development Roadmap; it does not silently rewrite or supersede its existing historical sections.

- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 149 map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-149-2026-10-18.md)
- [Wave 149 checkpoint](MEDIAHUB-CONTINUATION-CHECKPOINT-ADDENDUM-WAVE-149-2026-10-18.md)
- [Detailed Wave 149 report](MEDIAHUB-CONTOUR-A-CROSS-CHAT-CONTINUATION-AND-NEXT-WORK-REPORT-WAVE-149-2026-10-18.md)
- Governing Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Worker run-correlation PR #358: https://github.com/VlDMlNSh/mediahub-os/pull/358
- Documentation working PR #333: https://github.com/VlDMlNSh/mediahub-os/pull/333

## Current state (must refresh on every /next)
- Contour A remains **IN PROGRESS / NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
- Documentation branch is `docs/mediahub-chat-tree-map-20261012`. Keep it distinct from `main` and PR #333's unmerged working branch.
- PR #358 last fetched as open, Draft, unmerged, mergeable; head `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`; base `main` SHA `c06015e0b1526e0aaa6a522306052b077455aba5`. Focused test is present in the PR diff but execution needs job-log proof.
- Issue #301 remains the governing provider identity/capability, data-policy, route, quota, expiry/revocation and evidence tracker; refresh current issue state before actions.
- Provider list/model IDs/free quotas in Wave 148 are unverified hypotheses. No route has been admitted or enabled by Waves 148–149.
- Manual provider-assisted development is a fallback, not evidence of autonomous queue integration. Require authenticated policy-compliant access, bounded task, exact base SHA, allowed paths, reviewable branch/PR/patch, test evidence, and independent review. Never claim provider/agent connectivity without observed dispatch, run, artifact and provenance evidence.

## Ordered execution queue
### A. Refresh state and tests
1. Fetch current `main` and documentation branch heads, exact SHAs and comparison; refresh Issue #301 and PR #333/#358.
2. Inspect PR #358's exact workflow run, job and step logs to confirm `Worker run correlation regression tests` ran on the exact current head. Green workflow status alone is not enough.
3. If focused tests did not run, choose an authorized reproducible path and preserve logs, exit status and tested source SHA. Do not label tests as passed without evidence.

### B. Canonical provider registry and route admission
4. Enumerate the repository tree and locate the existing canonical provider registry/schema. Previous code-keyword searches returning no results do not prove absence. Do not create a parallel registry.
5. Never read or print credential values. Record only non-secret secret references, owner/project scope and policy metadata.
6. Verify Cloudflare Workers AI, Groq and Gemini official documentation first, then account/project-level quotas, exact model IDs, reset timezone, limits and terms. If entitlement cannot be observed, status remains BLOCKED.
7. Resolve Z.ai/SiliconFlow model/secret-name mismatches, then Mistral/OpenRouter/Hugging Face/Novita. Additional candidates remain unverified; SambaNova/DeepSeek Trial/MiMo stay HOLD until evidence.
8. Provider admission states: CANDIDATE → DOCS_VERIFIED → ACCOUNT_VERIFIED → POLICY_APPROVED → TESTED → ENABLED. Every transition requires dated evidence; stale/unknown/conflicting evidence fails closed. Fallback provider is a separate destination and requires policy/budget approval.

### C. Queue security and provenance
9. Enforce canonical signed A0 envelope validation: issuer, capability, audience/node, expiry/freshness, task digest, target/ref/source SHA, replay/idempotency and revocation.
10. Bind execution evidence to authoritative GitHub workflow/run/job/attempt/event/ref/source SHA/artifact ID and artifact digest plus the task-envelope digest.
11. Treat workflow titles and dispatch permissions as correlation/transport metadata, not authorization. Reject empty/ambiguous/stale/mismatched correlation; preserve fail-closed behavior.
12. Verify immutable-source execution, isolated ephemeral workspace, runtime-only secrets, cancellation/retry/recovery/terminal-state reconciliation and artifact quarantine. Keep provider output untrusted and independently reviewed.

### D. Qualification and release gates
13. Maintain distinct states for design, implementation, test, verification, qualification, release, deployment and independent acceptance.
14. Preserve required executor-path rounds, recovery, independent A3 review, pre-soak/current 24-hour soak and human-only G11 launch gate; verify current normative contract before claiming any gate satisfied.
15. Contour B remains blocked until Contour A is deployed and independently accepted. No worker/provider may self-qualify or self-promote.

## Authority and operational limits
- Jarvis: mission coordination.
- ASTRA A0: only accepted internal engineering queue authority.
- MediaHub Product State Authority: sole canonical product-state mutation authority.
- Human retains launch authority.
- No issuer/capability bypass, no self-promotion, no VPN/proxy/region spoofing to bypass provider terms, data/egress controls, quotas or account restrictions. No paid fallback without explicit destination and budget approval.
- Old-server state is history, not target configuration or qualification evidence; new hardware remains governed by the clean-slate target rule.

## Next pass definition of done
A bounded pass must produce: live ref/state snapshot; source-backed finding; code/test or documented blocker; exact artifact/blob/commit SHA; read-back verification; updated map/checkpoint; and a concrete next step. No claims without observable evidence.

## Wave 149 evidence boundary
This addendum defines work and continuation; it does not itself run tests, call providers, inspect credentials, dispatch workers, merge PRs, deploy infrastructure or qualify Contour A.
