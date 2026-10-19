# MediaHub OS — project map addendum, Wave 168

- Date: 2026-10-19
- Work branch: `docs/contour-a-wave-163-pypi-publisher-provenance-20261019`
- Status: **DOCUMENTARY CROSSWALK / PROPOSAL ONLY / NOT QUALIFIED**
- Report: [Wave 168 cross-envelope authority-binding review](../checkpoints/MEDIAHUB-A0-CROSS-ENVELOPE-AUTHORITY-BINDING-REVIEW-WAVE-168-2026-10-19.md)
- Governing issue: [#301 — Contour A cloud-agent development fabric](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Related evidence: [Wave 148 ingress trust-boundary revalidation](../checkpoints/MEDIAHUB-A0-INGRESS-TRUST-BOUNDARY-REVALIDATION-WAVE-148-2026-10-18.md), [Wave 149 issuer governance matrix](../checkpoints/MEDIAHUB-A0-ISSUER-GOVERNANCE-DECISION-GATE-MATRIX-WAVE-149-2026-10-18.md), [Wave 134 issuer call-site inventory](../checkpoints/MEDIAHUB-A0-ISSUER-DECISION-PACKET-CALLSITE-INVENTORY-WAVE-134-2026-10-18.md), [Wave 167 credential isolation trace](../checkpoints/MEDIAHUB-A0-MODEL-EXECUTION-CREDENTIAL-ISOLATION-TRACE-WAVE-167-2026-10-19.md).

## Claim → evidence → status

| Claim | Evidence | Status |
|---|---|---|
| Controller command HMAC and worker task authorization are not shown as one binding. | Wave 148 report blob `a0f00dd08e99e913e1f6949843e6943ecb937b15`; Wave 167 report blob `7da957751ae10c38370f0fbc228d98cef3883b96`. | Source-bound finding; issuer contract open |
| Task-file approval state is not, by itself, a signed external approval attestation. | Wave 148 exact source trace of `task_ingress.py` and `astra_gateway.py`. | Open trust boundary |
| Local `AuthorizationContext` and tuple grants do not prove issuer provenance, expiry, audience, scope or revocation. | Wave 134 blob `cd6f6021bc5b617ef0bc581bfe4a6748515ce81e`; Wave 149 blob `9c1a02dc125b37abea9284f0c0aa5deb571f13e7`. | Open trust lifecycle |
| Minimal cross-envelope binding and negative conformance cases are documented. | [Wave 168 report](../checkpoints/MEDIAHUB-A0-CROSS-ENVELOPE-AUTHORITY-BINDING-REVIEW-WAVE-168-2026-10-19.md). | Proposal only; tests not implemented or run |
| Credential isolation remains an independent P0 concern. | Wave 167 report, current-main source pins. | High-priority remediation/containment open |
| Governance status | GOV-CAP-01…07 and R-06 are unresolved in Wave 149; WB-05 Option C remains a proposal under PR #361. | No authority option accepted |

## Required gates before implementation

1. Owner/governance decision on issuer, principal, capability fields, revocation, delegation, replay/idempotency, audit and audit-unavailable behavior.
2. Accepted target runner/workspace/network manifest and actual worker ingress boundary.
3. Shared verifier plus positive/negative conformance tests tied to exact source SHA.
4. Independent security review and source-bound CI evidence.
5. Separate approved remediation for model-process credentials and persistent checkout credentials.
6. Separate gates for publication, merge, deployment and independent acceptance.

This addendum does not amend the canonical map on `docs/mediahub-chat-tree-map-20261012`; it is a work-branch navigation record. It does not authorize runtime dispatch or change Baseline 2.0.
