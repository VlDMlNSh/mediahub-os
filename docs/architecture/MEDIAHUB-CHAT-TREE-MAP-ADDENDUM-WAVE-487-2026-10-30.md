## Wave 524 — authenticated requester provenance clarification (2026-11-02)

- Report: [Wave 524 requester-provenance clarification](../checkpoints/MEDIAHUB-A0-REQUESTER-PROVENANCE-CLARIFICATION-WAVE-524-2026-11-02.md); [A0 contract](MEDIAHUB-A0-ISSUER-VERIFIER-CONTRACT-WAVE-487-2026-10-30.md); [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- The Wave 487 contract candidate was amended on its existing PR #600 branch to bind original requester identity/generation, verified workload authentication context, mission-authorization decision, required owner-approval evidence, immutable task/correlation/request digest, durable receipt and R-06 audit provenance.
- Added acceptance fixtures AUTH-15…AUTH-21 and AUD-05. Preserved Wave 486 Option C separation among requester/owner, Jarvis, Security Issuer Authority, A0 and MediaHub Product State Authority.
- Contract blob before: `691b4b52cd6ba80bb822cf64ef5bea5e6e523c61`; after: `1200d343139c8e67a826902b3ade09d4987c537d`; update commit: `7c9c8d4d587602483eafe21d14c39d4a2fd1165b`.
- Status: DRAFT AMENDED / NOT ACCEPTED / NOT IMPLEMENTED. Independent A3 review NOT RUN; exact-head CI NOT VERIFIED; R-06 governance, runner manifest and Draft 2020-12 validation remain open. No secrets, provider calls, dispatch, runtime, merge, deployment or qualification.
- PR #600 remains the working contract branch; PR #602's earlier provenance review is superseded as a source snapshot and must be refreshed against the amended exact head before independent review.

---

# Canonical Map Addendum — Wave 487 (2026-10-30)

## A0 issuer/verifier contract candidate

- Primary artifact: [MEDIAHUB-A0-ISSUER-VERIFIER-CONTRACT-WAVE-487-2026-10-30.md](MEDIAHUB-A0-ISSUER-VERIFIER-CONTRACT-WAVE-487-2026-10-30.md)
- Report: [Wave 487 report](../checkpoints/MEDIAHUB-A0-ISSUER-VERIFIER-CONTRACT-WAVE-487-2026-10-30.md)
- Parent Wave 486 HEAD: `824bb2568b2ac8bb3dceb3608366668e99bab95e`
- Branch: `docs/wave487-a0-issuer-verifier-normative-contract-20261030`
- Status: DRAFT NORMATIVE CANDIDATE / NOT ACCEPTED / NOT IMPLEMENTED / A3 REVIEW NOT RUN.

The contract translates Wave 486 target dispositions into testable semantics: issuer/principal lifecycle, capability claims, Jarvis→A0 attenuation, per-consumer verification, expiry/revocation, durable idempotent ingress, A0 lease fencing, R-06 audit/privacy and acceptance matrix.

Gemini controller feasibility: current controller has fixed generic task strings and fixed FCC-only review mode; exact Wave 487 packet cannot be routed to the requested independent roles. Secret/variable presence is not verified. No dispatch was made.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
