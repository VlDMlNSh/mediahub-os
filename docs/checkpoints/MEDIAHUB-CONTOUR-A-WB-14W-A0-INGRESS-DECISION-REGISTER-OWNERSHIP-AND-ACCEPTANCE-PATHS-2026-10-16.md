# MediaHub OS — Contour A WB-14W: A0 ingress decision-register ownership and acceptance paths

- Date: 2026-10-16
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **SOURCE-RECONCILIATION COMPLETE / ROLE OWNERSHIP PARTLY UNSPECIFIED / DECISIONS OPEN / NOT IMPLEMENTED / NOT TESTED / NOT QUALIFIED**
- Scope: reconcile WB-14V's split decisions with the current owner-decision register and governing architecture/security sources; identify accountable acceptance roles only where evidence supports them.
- Boundary: documentation-only. No owner decision is inferred, no normative contract/schema is changed, and no implementation or runtime activity is authorized.

## 1. Result

WB-14V's decision split is coherent and should be preserved:
- D-ING-01 — service principal and capability issuer authority.
- D-ING-02 — authentication and integrity profile.
- D-ING-03 — A0 durable admission/idempotency authority.
- D-ING-04 — freshness, expiry and replay policies.
- D-ING-05a — generic domain health ↔ accepted MH-06 semantics.
- D-ING-05b — A0 ingress health challenge/response.
- D-ING-06 — corporation-facing A0 lifecycle states and transitions.

The owner-decision register (`mediahub-owner-decision-register-2026-10-14.md`) is a product/architecture question register. It does not currently assign named accountable individuals or a formal acceptance workflow for these D-ING records. WB-14T's source list points to an owner-decision register blob, but that reference alone does not assign ownership. MH-12 requires governance approval and implementation/security evidence for acceptance; it does not name the specific approvers for this ingress contract.

Therefore, the acceptance path can be described at a **proposed role level**, but accountable role names, delegated decision rights, and the final approval record remain **NOT ESTABLISHED**. No individual or team is invented here.

## 2. Decision-to-owner/acceptance matrix

| Decision | Technical subject | Proposed accountable role(s), for owner confirmation | Required acceptance evidence | Current state |
|---|---|---|---|---|
| D-ING-01 | Jarvis/A0 service principals, issuer/attester, enrollment, revocation and delegation | Security/trust-governance owner; Jarvis identity owner; A0 verifier/contract owner | Explicit issuer authority; principal/audience enrollment; grant scope and delegation rules; revocation/unavailable behavior; audit obligations; recorded governance decision | OPEN; named owner not evidenced |
| D-ING-02 | Authentication and request integrity | Security-governance owner with ingress contract owner | Approved threat model and profile; end-to-end principal/audience and payload-integrity binding; key/credential lifecycle; replay handling; fail-closed and redaction requirements | OPEN; profile not selected |
| D-ING-03 | Single durable A0 admission/idempotency boundary | ASTRA A0 lifecycle/persistence contract owner; Jarvis caller contract owner for acknowledgement semantics | Accepted ownership boundary; durable commit and duplicate semantics; indeterminate-commit reconciliation; retry behavior; audit/evidence and failure behavior | OPEN; storage/commit mechanism not selected |
| D-ING-04 | Request expiry, clock skew, replay, revocation and evidence freshness | Security/trust-governance owner plus owners of each affected contract | Separate policy per freshness domain; trusted time assumptions; expiry/replay/revocation failure behavior; explicit values or rules accepted in the owning contracts | OPEN; no TTL or universal freshness value selected |
| D-ING-05a | Generic domain health schema vs MH-06 health/readiness semantics | Owners of the generic domain-health schema and MH-06 contract; governance for cross-scope mapping | Confirmed scope distinction or a versioned mapping/change proposal; consumer and compatibility impact; explicit acceptance by the relevant contract owners | OPEN; MH-06 ADR-001 itself is ACCEPTED for its stated scope; implementation authorization remains NO |
| D-ING-05b | Fresh, correlated A0 ingress health challenge/response | A0 ingress contract owner and security-governance owner | Accepted challenge/correlation, responder identity, freshness, contract revision, replay and failure semantics; separation from health/readiness/trust/authorization | OPEN; no endpoint/schema/crypto/TTL selected |
| D-ING-06 | Jarvis-visible A0 task lifecycle state machine | ASTRA A0 lifecycle contract owner with Jarvis mission/API owner; governance acceptance | Accepted state/transition table; admission vs lifecycle vs attempt/verifier/gate/health domains; cancellation/retry/lease/fencing/late-result and indeterminate-commit rules; terminal/result semantics | OPEN; accepted transition table not found |

**Important:** these are recommended role assignments to confirm, not existing assignments or approvals. The sources reviewed do not identify named accountable owners or prove that a particular role has delegated authority to accept these decisions.

## 3. Acceptance path

1. **Name the accountable owners.** The project owner/governance process must identify who owns security/trust policy, the generic domain-health schema, MH-06 cross-scope mapping, the A0 ingress contract and the Jarvis-facing lifecycle contract. A role label alone is not an approval.
2. **Keep independent decision records.** Preserve D-ING-05a, D-ING-05b and D-ING-06 as separate records. Do not merge health schema compatibility, probe protocol and task lifecycle into one enum or decision.
3. **Have each contract owner accept only their scope.** Security/trust decisions must not silently amend domain schemas; MH-06 acceptance must not be broadened beyond its stated Core Runtime Services scope; Jarvis mission coordination must not become A0 lifecycle ownership; A0 must not become Product State Authority.
4. **Record explicit governance disposition.** For each decision, capture approver/authority, selected option or approved contract revision, rationale, affected source paths, compatibility impact, conditions, date and evidence. Silence or a recommendation is not acceptance.
5. **Only then update normative artifacts.** Schema registration, protocol selection, lifecycle tables, implementation, tests, qualification and deployment remain separately gated. No implementation is authorized by this report.

## 4. Source reconciliation

- WB-14V blob SHA at this pass: `00cd42afedfb0c52561d967c7c40609f2a4c55fc`.
- WB-14T corrective addendum blob SHA: `023f44b6712450a8b84e2e99e716fd3cbb2d593e`.
- Owner decision register blob SHA: `8a8847bfc6fd3885c8f87ed6212442098f11482a`.
- MH-06 ADR-001 blob SHA: `7dda05379bd70007dc18acd62ed14fc83f0c9226`.
- MH-12 security architecture blob SHA: `cf4ebfd5bf471ca676f075c51d3a24906504e490`; it states architecture is not production qualification and requires traceability, compatibility, implementation/security evidence, verification, contradiction resolution and governance approval.
- Bootstrap instruction blob SHA: `a3c51f3ddf17827bf6193cce52387a5daad3b6e0`.
- Current project map blob SHA before this update: `a36064899c354859f32c46a6a0117a3cc0b2c50f`.
- Current continuation checkpoint blob SHA before this update: `e7fdb7ab43e8a68f5f309665c94968a5abb931c2`.

Limit: this is a bounded source reconciliation, not a repository-wide governance audit. No evidence found in the inspected sources assigns named owners or a formal approval workflow to the D-ING decisions; this is recorded as an evidence gap, not proof that no such process exists elsewhere.

## 5. Verification and next step

- Documentary consistency checked against WB-14V, its corrected WB-14T addendum, the owner-decision register, MH-06 ADR-001, MH-12 and the bootstrap instruction.
- No tests, schema validators, code edits, credentials/provider calls, host/runtime inspection, installs, infrastructure changes, deployment, migration or branch integration occurred.
- Next bounded step: obtain explicit confirmation of accountable owners and the governance acceptance record for D-ING-01…04 and D-ING-05a/05b/06. Until then, keep the ingress design proposed and implementation blocked.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
