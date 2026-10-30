# Wave 486 — Owner-directed A0 issuer governance disposition (2026-10-30)

## Result

**SELECTED TARGET DECISIONS RECORDED / INDEPENDENT REVIEW NOT RUN / NORMATIVE ACCEPTANCE NOT CLAIMED / RUNTIME BLOCKED.**

The owner directed the assistant to select the most appropriate answers based on prior MediaHub discussions. Bootstrap §8 already instructs autonomous technical decision-making and minimal escalation. This pass therefore selected a conservative target rather than returning routine engineering choices to the owner.

Primary artifact: [A0 issuer governance disposition](../architecture/MEDIAHUB-A0-ISSUER-GOVERNANCE-DISPOSITION-WAVE-486-2026-10-30.md).

## Decisions selected

- WB-05 Option A: a separately governed dedicated Security Issuer Authority, logically separate from Jarvis, ASTRA A0, executors and Product State Authority.
- GOV-CAP-02: issuer authority governs service-principal enrollment, suspension, recovery and re-enrollment.
- GOV-CAP-03: mandatory checks at Jarvis ingress, A0 ingress and every protected consumer; each consumer makes its own audience/policy decision.
- GOV-CAP-04: independent Security Trust Custodian role, dual control and managed KMS/HSM-backed trust anchor as the preferred target; product selection deferred to ADR.
- GOV-CAP-05: initial defaults of 5-minute maximum capability lifetime and 30-second maximum revocation-state age; deny when freshness cannot be established; re-check before each protected effect.
- GOV-CAP-06: Jarvis submits a bounded mission request but does not transfer or mint A0 capabilities; issuer grants a separately bound, attenuating A0 capability.
- GOV-CAP-07: durable A0 acceptance receipt plus positive/negative/replay/race evidence, exact-head CI and independent A3 security review.
- R-06: separate Security Audit and Privacy/Data Governance accountabilities; minimal tamper-evident correlated events; fail closed on audit outage for privileged ingress/mutations; initial retention defaults 365 days for security evidence and 90 days for routine task metadata, subject to stricter legal/privacy rules.

## Source reconciliation

- WB-05 source blob: `1b562c6546b1216f2ee89095cd6a78427a967dc5`.
- Wave 149 matrix blob: `9c1a02dc125b37abea9284f0c0aa5deb571f13e7`.
- Wave 484 source reconciliation was re-read. It confirms DEC-DEV-02 Option C is already owner-approved and must not be reopened; it also confirms issuer options A–D had remained unselected.
- Wave 485 contract skeleton was re-read at blob `14cf0194504824a17569433d4478154eb44afc3f`.
- Issue #301 remains open and its objective keeps Cloud Pool/Contour A first.

## Important boundary

The selected document is an owner-directed target disposition, not proof that the issuer, identity registry, KMS/HSM, audit sink or named operational teams exist. Concrete vendors, protocols, token format, key store, identities, endpoints and secret names remain unselected pending source research and ADR. The 5-minute/30-second defaults require load/clock/revocation tests. Retention defaults require privacy/legal validation.

Wave 482 A0-ISSUER-01 remains a HIGH source-level provenance gap, not a confirmed exploit. No runtime code, tests, credentials, provider calls, Gemini/Claude dispatch, host tasks, merge, deployment, qualification or acceptance occurred.

## Git evidence

- Parent: Wave 485 head `37254c9f4ff09c39943f6924534a63dd44b5a431`.
- Branch: `docs/wave486-a0-owner-directed-governance-disposition-20261030`.
- Decision document commit: `2d4cbf79803c83356e97c9830900443e3e736c51`.
- Draft PR: [#599](https://github.com/VlDMlNSh/mediahub-os/pull/599), base Wave 485 branch `docs/wave485-a0-contract-skeleton-20261030-v2`; parent/base SHA `37254c9f4ff09c39943f6924534a63dd44b5a431`.
- PR #599 exact-head workflow runs: empty; formal reviews: 0; inline review threads: 0. CI and independent review are NOT VERIFIED. PR remains Draft/Open/Unmerged. The PR is stacked on PR #598 and must not be merged directly to canonical docs branch.

## Next

Prepare the versioned technology-neutral issuer/verifier contract and test specification from these selected dispositions; perform independent A3 review before runtime changes. Keep the cloud pool first in the roadmap and do not dispatch agents until controller and issuer/capability gates independently pass.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
