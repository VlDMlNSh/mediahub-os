# MediaHub OS Contour A — Trusted publisher contract and negative-test matrix (Wave 179)

- Date: 2026-10-19
- Status: DESIGN/TEST MATRIX ONLY; not an issuer decision, implementation, security qualification or acceptance.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous trace: [Wave 178 issuer/admission/publication source trace](MEDIAHUB-CONTOUR-A-A0-ISSUER-ADMISSION-PUBLICATION-TRACE-WAVE-178-2026-10-19.md)
- Publisher proposal: [Wave 177 design](MEDIAHUB-CONTOUR-A-TRUSTED-PUBLISHER-BOUNDARY-DESIGN-WAVE-177-2026-10-19.md)
- Governance: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301), [Wave 149 decision-gate matrix](MEDIAHUB-A0-ISSUER-GOVERNANCE-DECISION-GATE-MATRIX-WAVE-149-2026-10-18.md)

## Purpose and authority boundary

Translate the already documented security invariants into an implementation-independent acceptance matrix. This document does not choose an issuer, signing protocol, key store, principal lifecycle, or product-state authority. Those decisions remain in governance. Fixtures described below must be synthetic; they are test requirements, not claims that tests have run.

Keep distinct: Jarvis mission coordination; ASTRA A0 engineering-workflow state; MediaHub Product State Authority as the only canonical product-state mutation authority; and the still-unassigned accountable security issuer/attester role.

## Minimum result-handoff contract (proposed, not accepted)

The future schema should be versioned and strict, reject unknown authority-bearing fields, bound total bytes/files/individual file size, and carry only:
- command ID and task ID;
- issuer/capability reference plus verifier decision reference (never trust a worker-supplied “approved” boolean);
- repository identity, immutable target commit SHA, node/audience identity and pre-authorized output-ref policy;
- normalized patch or a bounded list of file path/content digests, with a defined canonicalization;
- builder/test/verifier evidence references and digests, tool versions and workflow/run correlation;
- idempotency key, issued-at/expiry metadata, and the verifier's revocation/freshness result reference;
- no credentials, arbitrary commands, worker Git directory, hooks, remote URLs, executable publisher scripts, or claims accepted solely from worker-controlled metadata.

This field list is a design input. Exact required/optional fields, signature format and trusted-context lifecycle cannot be frozen until GOV-CAP-01…07 and related MH-12/R-06 decisions are accepted.

## Required synthetic negative-test matrix

| ID | Synthetic mutation / failure | Required result | Evidence to capture |
|---|---|---|---|
| PUB-01 | Missing issuer identity, unknown trust root or malformed/unverifiable signature | DENY before execution/publication | Stable error code; no credential acquisition |
| PUB-02 | Capability wrong operation/resource/scope/audience/node | DENY | Expected vs presented non-secret claims |
| PUB-03 | Command/task digest or immutable target SHA mismatch | DENY; no rebase/substitution | Bound digests and rejected target |
| PUB-04 | Expired grant, stale/unknown revocation state or principal suspended | DENY fail-closed | Clock/freshness inputs and decision reference |
| PUB-05 | Replay or duplicate command/idempotency key | No second publication; deterministic idempotent outcome | Prior decision/result correlation |
| PUB-06 | Wrong repository, base ref or destination ref outside approved policy | DENY before token mint/push | Repository/ref policy decision |
| PUB-07 | Absolute path, traversal, symlink escape, forbidden path, path collision or case-folding ambiguity | DENY | Canonicalized path list and policy rule |
| PUB-08 | Oversized bundle, excessive file count, binary/unsupported patch or malformed encoding | DENY without unbounded resource use | Enforced size/count limit and error code |
| PUB-09 | Worker-supplied .git data, hooks, remote URL, commit identity, environment or publisher script | Ignore/reject; reconstruct only from clean immutable base | Proof of clean reconstruction and resulting tree digest |
| PUB-10 | Claimed tests/verifier pass not tied to immutable artifact/run | DENY or mark evidence insufficient | Artifact digest, run identity and independent revalidation |
| PUB-11 | Ambiguous/missing workflow, task or artifact correlation | DENY | Correlation failure record |
| PUB-12 | Push fails, branch changes concurrently, or remote SHA differs from expected commit | FAIL; do not report publication success or broaden permission | Push outcome, expected/observed remote SHA |
| PUB-13 | Audit/evidence sink unavailable or tamper check fails | Fail closed before publication, or apply explicitly approved recovery policy | Audit health and recovery state |
| PUB-14 | Cancellation, expiry or revocation races with admission/build/publish | Stop at the earliest safe gate; never publish after invalidation | Ordered lifecycle events |
| PUB-15 | Worker tries to reach publisher filesystem/process or inherit publisher credential | Isolation test must show denial | Runner boundary evidence; no secret values |
| PUB-16 | Workflow retries with a different target/ref or silently falls back to broad token | DENY; no permission widening | Attempt chain and effective permission policy |

## Positive-path requirements (must also be tested later)

1. A valid, governance-approved synthetic command is accepted only for its exact repo/task/node/audience/target/ref/scope.
2. The publisher reconstructs the candidate tree from a clean checkout at the immutable target SHA; worker .git state is never reused.
3. A normalized diff is independently checked against explicit path, file-type, size and content policies.
4. The publish credential is minted only after admission and is not available to the worker, builder, test or verifier process tree.
5. Publication is idempotent; commit SHA and destination ref are read back from the remote and matched exactly.
6. Evidence is bound to the admitted command, exact base SHA, normalized diff digest, resulting commit, workflow run and remote SHA; secrets are excluded.
7. Any missing trust input, ambiguity or failed independent check remains fail-closed.

## Required implementation order after governance

1. Record explicit accountable issuer/attester and trusted-context lifecycle decisions for GOV-CAP-01…07; resolve relevant MH-12/R-06 and runner/workspace/network gates.
2. Freeze a versioned schema and verifier contract against those accepted decisions.
3. Implement pure, credential-free validation and synthetic positive/negative tests in an isolated PR.
4. Independently review threat model, test completeness and runner isolation.
5. Qualify a disposable test-repository/ref publisher using approved synthetic credentials and immutable evidence.
6. Only then consider a controlled integration test; production publication, merge, deployment and acceptance remain separate gates.

## Current GitHub snapshot

- PR #375: OPEN / DRAFT; head `59a9d063778ec11b751cc7309c04e7fe27f3a603`, base `c06015e0b1526e0aaa6a522306052b077455aba5`, 3 changed files. Two exact-head Actions runs are reported successful: [Astra Verify](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39223983372) and [Astra Cloud Runtime Validation](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39223983379). Combined commit status endpoint currently returns pending with zero status contexts; that endpoint is not a substitute for the named Actions runs.
- PR #374: OPEN / DRAFT; head `3b1fc96beeedcc6cb38c7beeb5809f0004c6ac8a`, base `e922349c6e7a49657faf70836b36d96d977a948b`, 12 changed files. Its earlier exact-head CI success does not close issuer, R-06, runner manifest or dependency provenance gates.
- No mergeability field or successful CI run means governance/security acceptance.

## Evidence limits

No tests were executed in this pass; this is a test design matrix only. No worker/workflow was dispatched, no credentials or provider APIs were accessed, and no runtime or production configuration was changed. PR #375 and #374 remain Draft and unmerged. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**; Contour B remains gated.
