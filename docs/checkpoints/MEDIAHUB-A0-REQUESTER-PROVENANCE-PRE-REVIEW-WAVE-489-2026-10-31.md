# Wave 489 — A0 issuer/verifier contract provenance pre-review

- Date: 2026-10-31
- Status: **PRE-REVIEW FINDING RECORDED / INDEPENDENT A3 REVIEW NOT RUN / CONTRACT NOT ACCEPTED**
- Scope: read-only semantic review of PR #600's Wave 487 contract against the owner-directed Wave 486 decision.
- Immutable target: PR #600 head `1e98fb9377e2103bdb6a70b1ca369596cea3a9fe`.
- Parent: Wave 486 head `824bb2568b2ac8bb3dceb3608366668e99bab95e`.
- Contract blob: `691b4b52cd6ba80bb822cf64ef5bea5e6e523c61`.
- Wave 486 decision blob: `13e6745463dbc05a7c188423bb45ffb2b210c789`.
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Related cloud-first priority: [PR #595](https://github.com/VlDMlNSh/mediahub-os/pull/595).

## 1. Work performed

Read the complete Wave 487 contract and Wave 486 owner-directed disposition at their recorded refs/blob SHAs. Reviewed authority separation, issuer/principal lifecycle, capability claim semantics, Jarvis-to-A0 ingress, per-consumer verification, revocation, durable idempotency, lease fencing, R-06 audit/privacy and the 40+ acceptance scenarios.

This is an internal static pre-review by the current engineering session. It is **not** the independent source-bound A3 security review required by Wave 486/487, and it is not a formal GitHub approval.

## 2. Finding — authenticated mission requester provenance is underspecified

**Disposition: MUST CLARIFY BEFORE NORMATIVE ACCEPTANCE.**

The contract correctly states that the issuer must authenticate the requesting principal independently of request-supplied claims (Section 3.2), and that Jarvis submits a bounded mission request (Section 5). The capability claim set (Section 4), however, names the issuer, subject, audience, task, operations, resources, constraints, delegation and request binding, but does not explicitly require an authenticated initiator/requester identity or a verifiable authorization relationship between that requester and the submitted mission.

The current wording does not make sufficiently testable:
- which authenticated principal initiated the mission (for example, an admitted Jarvis service principal acting for an owner-approved mission);
- whether that principal is authorized to request this mission/task class and these data/resource bounds;
- how the authenticated requester identity and its authorization decision are bound to the immutable request digest, task ID, issuer decision and durable A0 receipt;
- how the requester/initiator provenance survives Jarvis-to-issuer-to-A0 delegation and is represented in audit evidence without storing credentials.

This is a **contract completeness / confused-deputy prevention gap**, not evidence of a confirmed exploit or a finding that a deployed runtime is vulnerable.

### Required contract clarification

Add a format-neutral authenticated request-origin binding. At minimum define:
1. a stable authenticated requester/initiator principal ID and identity generation, distinct from the A0 execution subject;
2. verified workload identity and authentication context for the request submitter;
3. a policy decision proving that this requester may submit the exact mission/task class, audience, operation/resource scope, environment and data classification;
4. immutable binding of requester, task ID, request digest, correlation ID, issuer decision and A0 receipt;
5. preservation of the original requester and any authorized delegation chain through downstream evidence;
6. explicit deny behavior when requester identity, authorization, delegation provenance or binding is absent, ambiguous, stale or revoked.

Do not assume that Jarvis itself is the human/owner identity. Keep the human/owner approval source, Jarvis service principal, Security Issuer Authority and A0 service principal distinct. The exact identity protocol, claims encoding and trust mechanism remain ADR decisions.

### Required acceptance coverage

Add negative and positive fixtures, at least:
- unknown/unadmitted requester;
- authenticated requester without permission for the requested mission class;
- request digest/task mismatch after authorization;
- valid Jarvis service identity with missing owner/mission authorization evidence;
- delegation chain whose requester provenance is absent or altered;
- replay of a valid request under a different requester or task;
- requester suspension/revocation between initial authorization and A0 durable acceptance;
- audit receipt omitting requester identity generation or authorization decision reference.

Expected behavior: deny before durable acceptance/protected effect, preserve the original receipt on conflicts, and emit sanitized correlated audit evidence.

## 3. Reconciliation with Wave 486

No contradiction found in the following selected target values/boundaries:
- dedicated Security Issuer Authority separate from Jarvis and A0;
- A0 owns its internal queue/lease/cancel/recovery lifecycle;
- every protected consumer independently verifies its own audience and authority;
- capability lifetime 300 seconds equals Wave 486's five-minute maximum;
- revocation freshness maximum 30 seconds;
- R-06 audit/privacy separation and retention targets 365/90 days;
- no authority transfer from transport ACK, model, executor or GitHub Actions.

The requester-provenance finding adds a missing explicit binding; it does not replace or reopen the owner's selected authority split.

## 4. PR / CI / governance evidence

- PR #600: OPEN / DRAFT / UNMERGED; head `1e98fb9377e2103bdb6a70b1ca369596cea3a9fe`; base Wave 486 head `824bb2568b2ac8bb3dceb3608366668e99bab95e`; compare 9 ahead / 0 behind.
- PR #600 changed files: contract, map addendum, Wave 487 report and continuation checkpoint.
- Exact-head workflow-run listing: empty. Combined-status contexts: empty. Formal review submissions: 0. These results mean CI and independent review are **NOT VERIFIED**.
- PR #595 cloud-first priority: OPEN / DRAFT / UNMERGED; head `72a6725dbc7c38e37805e254377d293fcb141e7e`; exact-head workflow runs/statuses empty; formal reviews 0.
- PR #601 Wave 488 runner matrix: OPEN / DRAFT / UNMERGED; head `02f0988cdeac2c6b360946c9a62b7a56f21c142d`; exact-head workflow runs/statuses empty; formal reviews 0.
- Canonical docs branch vs main: 3,455 ahead / 82 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No merge/rebase performed.
- The canonical map blob SHA is `75f62685459ec99ebf8be478f4e9096cdb842b1d`; GitHub Contents returned empty content, but the blob API returned and allowed reading the full 1,204,915-byte blob. Its latest indexed wave heading is Wave 477. Wave 483–488 remain in their separate draft branches/addenda and are not represented as accepted canonical map state.
- Issue #301 remains OPEN and explicitly says the ordered queue is documentary; it does not authorize provider calls, secret reads, workflow dispatch, merge, deployment or acceptance.

## 5. Execution ledger

| Item | Status |
|---|---|
| Wave 487 contract static pre-review | COMPLETED / PRE-REVIEW ONLY |
| Requester-provenance clarification | REQUIRED / NOT IMPLEMENTED |
| Independent A3 review | NOT RUN |
| PR #600 exact-head CI | NOT VERIFIED |
| Gemini Agents 1–3 | NOT RUN |
| Claude / Alamo | NOT RUN; no qualified Alamo identity/route established in this pass |
| Provider calls / secret reads | NOT RUN |
| Runtime changes / tests | NOT RUN |
| Merge / deployment / qualification / acceptance | NOT RUN |
| Contour A | NOT ACCEPTED |
| Contour B | GATED |

No agent controller was invoked. The current Gemini controller's fixed task contract does not accept this review packet; no attempt was made to bypass it. No secrets, provider credentials, model endpoints or local hosts were accessed.

## 6. Next bounded step

1. Amend Wave 487 contract with authenticated requester/initiator binding and the negative fixtures above, preserving the selected Wave 486 authority model.
2. Re-read the amended contract and compare it against the immutable Wave 486 decision and existing MH-12/WB-03…06 contracts.
3. Obtain independent A3 review tied to the amended exact HEAD; then run required exact-head CI.
4. Continue the authoritative hosted runner/workspace/network manifest and Draft 2020-12 schema/negative-fixture work in parallel only where dependencies permit.
5. Do not dispatch Gemini/Claude, read secrets, invoke providers, merge or deploy until the relevant admission and governance gates are verified.

## Direct links

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #595 — cloud-first priority](https://github.com/VlDMlNSh/mediahub-os/pull/595)
- [PR #600 — A0 issuer/verifier contract](https://github.com/VlDMlNSh/mediahub-os/pull/600)
- [PR #601 — hosted runner matrix](https://github.com/VlDMlNSh/mediahub-os/pull/601)
