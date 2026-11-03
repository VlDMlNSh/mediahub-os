# Wave 489 — A0 requester-provenance contract pre-review

- [Wave 489 pre-review report](../checkpoints/MEDIAHUB-A0-REQUESTER-PROVENANCE-PRE-REVIEW-WAVE-489-2026-10-31.md)
- Immutable review target: PR #600 / Wave 487 contract head `1e98fb9377e2103bdb6a70b1ca369596cea3a9fe`; contract blob `691b4b52cd6ba80bb822cf64ef5bea5e6e523c61`.
- Static pre-review identified an underspecified authenticated requester/initiator binding between mission submitter, issuer authorization, immutable request digest, A0 receipt and audit evidence. This is a contract-completeness finding, not a confirmed exploit.
- Required follow-up: add requester identity generation, mission-class authorization, request/receipt binding and negative fixtures; then obtain independent A3 review and exact-head CI.
- Wave 486 authority split and 5-minute/30-second defaults were found consistent with the Wave 487 draft.
- Status: pre-review only; independent A3 review NOT RUN; PR #600 remains DRAFT / NOT ACCEPTED / NOT IMPLEMENTED.
- No agents, providers, secrets, runtime tests, merge, deployment or qualification were run.
- Parent: PR #600 head `1e98fb9377e2103bdb6a70b1ca369596cea3a9fe`.
