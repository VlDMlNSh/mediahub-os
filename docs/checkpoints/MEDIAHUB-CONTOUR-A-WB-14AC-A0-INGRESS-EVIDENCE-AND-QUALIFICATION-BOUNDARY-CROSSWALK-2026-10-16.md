# MediaHub OS — Contour A WB-14AC: A0 ingress evidence and qualification-boundary crosswalk

- Date: 2026-10-16
- Status: **SOURCE CROSSWALK COMPLETE FOR REVIEWED FILES / EVIDENCE RULES REUSABLE WITHIN SCOPE / JARVIS-FACING ACCEPTANCE CONTRACT NOT ESTABLISHED**
- Scope: trace the accepted ASTRA GOLD qualification/evidence sources against WB-14AA's proposed Jarvis → ASTRA A0 ingress result boundary.
- Boundary: documentation-only source reconciliation. No qualification, test, runtime, provider, credential, installation or infrastructure activity.

## 1. Finding

The repository has a canonical ASTRA GOLD qualification-and-launch gate schema and supporting reference architecture. They establish strong internal requirements for target-SHA-bound evidence, immutable evidence records, mandatory metadata, fresh evidence, independent A3 verification, no self-qualification, and fail-closed behavior when evidence is missing or contradictory.

These sources do **not** by themselves establish the missing accepted Jarvis-facing A0 API, caller/issuer trust chain, external mission/result schema, or the contract owner/acceptance authority. Internal evidence policy can constrain a future ingress contract; it cannot be silently promoted into that external API.

## 2. Source anchors and exact scope

| Source | Ref / blob SHA | Source-backed rule | Boundary / limitation |
|---|---|---|---|
| ASTRA GOLD Qualification/Launch Schema | `main`, `aef6229477ed8ec45e45170f98ea87f7ba75ca29` | Canonical machine-readable qualification/launch gate; independent verification assigned to A3; self-qualification disabled; registration does not imply qualification/launch; required launch inputs include approved source SHA, launch target, fresh evidence bundle, A3 verification record, soak record and rollback target; evidence metadata list is explicit | Defines ASTRA qualification/launch gates, not Jarvis ingress authentication, request/ack/status/result/cancel API or admission commit semantics |
| ASTRA GOLD Reference Architecture | `main`, `7be5fadd3055642e7823c7233f90e978a87e5366` | Qualification needs fresh evidence at exact source SHA; evidence plane records command/node/component/executor/provider-or-model/source SHA/round/timestamp/exit status/timeout/verification status/digest; completed-round evidence is immutable; contradictions become RECONCILIATION_REQUIRED → BLOCKED; A3 independently verifies and executors cannot certify their own qualification | Reference architecture explicitly does not grant qualification; it does not select the Jarvis-facing contract or identity issuer |
| ASTRA GOLD Governance Contract | `main`, `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Declares the qualification schema as source of truth; specifies internal gate registry, evidence metadata and internal timing configuration; no secrets in evidence; independent A3 required | Internal evidence freshness and result-publication timeout are not automatically request TTL, capability expiry, probe TTL or idempotency retention |
| ASTRA Executor Capability Matrix | docs branch `9ad83781a8da53d1a8f540ede54eba95281f01c0`; main `da26185254d9954fcee204f81ecca129bf052e7c` | A0 owns internal workflow/claim/lease/evidence/gate state; A3 is a separate verifier; evidence is immutable and target-SHA-bound; contradictions require reconciliation | Docs/main wording differs on the A0 authority row; do not integrate branches or resolve the drift in this report. Both versions lack the external Jarvis ingress contract |
| WB-14Z ingress source census | docs branch `95f3af63705f4ad7cd24405df9c7c396886cb3a3` | Existing local-file Task Contract consumer and signed operational-command workflow are separate; neither proves an authenticated Jarvis producer → accepted A0 consumer chain | The ingress producer, issuer-backed context, external schema and durable admission contract remain unestablished |
| WB-14AA candidate | docs branch `030273bfe9fd6d44e78b611c011af95d08c88a45` | Proposes external status/result/evidence distinctions and request/target/policy correlation | Explicitly PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED |

## 3. Evidence boundary for a future ingress contract

The following mapping is safe as a **candidate acceptance checklist**, not as an accepted wire schema:

1. **Request/admission identity:** correlate a submitted mission and every acknowledgement to an immutable request identity/digest; define duplicate, conflicting-digest and uncertain-commit behavior in the separately accepted A0 ingress contract.
2. **Target binding:** bind work and its resulting artifacts/evidence to the approved repository/project/artifact target and exact source/target revision. A moving branch name alone is not sufficient evidence of which source was qualified.
3. **Execution evidence:** preserve executor identity, relevant provider/transport identity where applicable, workspace, command/attempt, timestamp, exit status, timeout, result validation and evidence digest according to the ASTRA GOLD schema. Do not put credentials/secrets into evidence.
4. **Independent verification:** represent A3 verification as a separate attributable disposition; executor/A2 claims must not self-certify verification or qualification.
5. **Qualification and promotion:** keep task completion, evidence completeness, verification, qualification, release and deployment separate. The presence of an evidence record or registered component is not a PASS or launch authorization.
6. **Freshness domains:** apply ASTRA qualification-evidence freshness only to its documented evidence/gate scope. External request freshness, capability expiry, replay windows, health challenge freshness and deduplication retention require explicit independent policy in the accepted ingress/security contracts.
7. **Contradictions and missing evidence:** preserve RECONCILIATION_REQUIRED/BLOCKED semantics where relevant; do not let an ingress adapter resolve a conflict by changing source, authority or evidence. Missing/ambiguous trust or required evidence must not silently bypass the owning policy.
8. **Acceptance record:** record the exact contract revision/blob SHA, source references, explicit authorized owner/governance disposition, compatibility impacts and separately approved qualification plan before any promotion.

## 4. Cross-contract gaps that remain OPEN

| Gap | Existing source helps with | Still missing for Jarvis → A0 |
|---|---|---|
| Caller identity / issuer / authorization | MH-12 layered trust and ASTRA fail-closed constraints | Accepted issuer/attester, enrolled principal, audience/scope, verifier and revocation lifecycle |
| Mission API / response | WB-14AA candidate operation semantics | Accepted endpoint/transport/schema/version, request and acknowledgement envelope, error taxonomy |
| Durable admission / retries | ASTRA internal queue/recovery/idempotency design | Accepted external idempotency key scope, commit point, duplicate/conflict response and lost-ACK reconciliation |
| Lifecycle/result mapping | Internal A0 lifecycle and evidence/gate policy | Accepted Jarvis-visible state projection, cancellation/fencing races and terminal-result semantics |
| Evidence and verification | Canonical ASTRA qualification schema and A3 architecture | Accepted cross-boundary result/evidence reference contract and named acceptance authority |
| Contract governance | Owner register and WB-14W role-level recommendations | Named accountable owners, delegated authority, formal approval workflow and explicit accepted contract revision |

Do not conflate owner-register D-03 with D-ING-03, or DEC-DEV-02 Option C with an external ingress API approval. Keep D-ING-05a generic health mapping, D-ING-05b A0 challenge/response, and D-ING-06 lifecycle mapping separate.

## 5. Branch/source drift and verification limits

The ASTRA Executor Capability Matrix has different blob SHAs and wording between `main` and the documentation branch. The docs branch scopes A0 to ASTRA-internal workflow/control state and excludes canonical product-state authority; the main row is broader/ambiguous. This report records that discrepancy without editing either normative source, merging branches or asserting that the docs-branch wording is integrated into main.

This pass fetched and compared source documents only. It did not run schema validators, tests, workflows, runtime probes or qualification. No runtime or deployment state is inferred.

## 6. Disposition and next step

- Reuse the ASTRA GOLD evidence/qualification rules as constraints for future A0 ingress contract review, within their existing scope.
- Keep WB-14AA and its A0-ING-01…09 labels proposal-local and non-normative.
- Keep external ingress owner/issuer/API/admission/lifecycle acceptance OPEN.
- Keep Contour A qualification/acceptance distinct from Contour B product work; do not claim A0 is deployed, qualified or accepted.
- Next bounded step: assemble a source-linked governance request that asks the project owner to appoint accountable contract/security/lifecycle owners and confirm the approval workflow. The request should present the open choices without choosing them or authorizing implementation.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
