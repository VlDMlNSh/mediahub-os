# Wave 483 — Cloud Agent Pool First priority decision (2026-10-30)

## Owner direction and disposition

The owner directs that development, controlled launch, operationalization and independent acceptance of the GitHub-hosted cloud-agent pool (Contour A) take priority over deployment of owned/local server hardware. Server hardware becomes the second phase, beginning only after Contour A is deployed and independently accepted. This is a sequencing decision, not a waiver of governance or a dispatch authorization.

## Plan change

The Master Development Roadmap now begins with a dated strategic priority supersession. The cloud-first critical path is:

1. Issue #301 gates: A0 issuer/ingress/lease/cancel/recovery; R-06 audit/privacy; authoritative runner/workspace/network target manifest; standards-compliant Draft 2020-12 schema validation and negative fixtures; independent schema/semantic review.
2. Harden approved GitHub-hosted transports: immutable checkout SHA, strict allowlists, full-SHA actions, output quarantine, evidence manifest, runtime-only secrets, idempotency/replay, quota and data-egress controls; no paid fallback.
3. Implement the smallest authorized read-only worker and deterministic fake-provider tests.
4. Run a bounded cloud pilot only after admission gates pass.
5. Operationalize and independently qualify Contour A; record deployment and production acceptance separately.
6. Only then resume server hardware qualification, activation, procurement/install and service placement.
7. Contour B remains gated until Contour A deployment and independent acceptance; hardware acceptance does not substitute for this gate.

Hardware inventory and compatibility research may continue as non-blocking documentation. Hardware deployment must not be placed on the cloud-pool critical path absent a newly accepted dependency.

## Current evidence and blockers

- Main SHA observed: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`; canonical documentation base observed: `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`.
- Issue #301 is OPEN and remains the governing queue. It explicitly places A0/R-06/target-manifest/schema/review before worker dispatch.
- PRs #590–#594 were OPEN/DRAFT/UNMERGED at last refresh. Recent documentation PR exact-head CI and reviews are NOT VERIFIED when API results are empty.
- Router policy remains policy-only, direct provider calls disabled, paid fallback disabled and unknown routes fail-closed; no live cloud pool is proven.
- SentinelX reports zero connected hosts; Voktors-Mini.Dlink offline; mh-dev-01 and mh-dev-02 disabled.
- Gemini and Claude dispatches, provider calls, secret reads, server activation, deployment and acceptance were NOT RUN / NOT VERIFIED.

## Acceptance criteria before hardware phase

All six conditions are mandatory:
1. Approved GitHub-hosted Contour A deployment exists.
2. Exact-head CI and governance contexts are verified.
3. A0 issuer/capability, replay, lease/cancel/recovery, R-06 and authoritative target manifest are accepted.
4. A bounded read-only pilot has immutable provenance and independent evidence verification.
5. Secret isolation, provider/model allowlists, data-egress, quota/budget and no-paid-fallback are demonstrated.
6. Independent Contour A qualification and explicit production acceptance are recorded.

## Next step

Wave 484 should continue the first unfinished dependency from Issue #301, not hardware setup: formalize issuer/capability and durable replay/lease/cancel/recovery contracts, then independently review them. In parallel only where independent, close R-06 and target-manifest evidence. No controller dispatch before all gates pass.

## References

- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Canonical chat tree map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 482 A0 ingress source audit](MEDIAHUB-A0-INGRESS-ISSUER-SOURCE-AUDIT-WAVE-482-2026-10-30.md)


## Post-write verification

- PR: [#595](https://github.com/VlDMlNSh/mediahub-os/pull/595), OPEN / DRAFT / UNMERGED; head `a89e2ad983018e715ec688dd6e9bdc4fbf8adbb0`; base canonical docs branch at `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`; 5 commits ahead / 0 behind; mergeable true at last check.
- Exact-head workflow runs: empty; combined status contexts: empty; formal PR review comments: empty. CI and independent review **NOT VERIFIED**. PR remains Draft.
- Re-read exact changed artifacts: Master Roadmap blob `f811303becbb49232cd2337b9e124f9610e52e83` (829,132 chars); canonical map blob `5f4e552f7ae344b7f4b1cee9da84a750908b7548` (1,206,366 chars); checkpoint blob `7d06046a03f525f4a48ac2cdee4a8126df591ce9` (505,473 chars); report blob before this verification append `2b2931f284f1da944eea2a71ec09ec4c849708ac`; map addendum blob `4f750c8399f94d47373a8789a32c4d639688b4f2`.
- Compare against canonical docs base: 5 commits ahead / 0 behind; 5 expected files only (roadmap, canonical map, checkpoint, report, addendum); no deletions.
- No runtime code changes, tests, agent dispatch, provider calls, secret access, server activation, deployment or acceptance.
