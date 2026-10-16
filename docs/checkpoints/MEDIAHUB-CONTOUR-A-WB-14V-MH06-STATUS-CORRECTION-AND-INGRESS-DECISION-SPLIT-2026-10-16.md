# MediaHub OS — Contour A WB-14V: MH-06 status correction and ingress decision split

- Date: 2026-10-16
- Status: **DOCUMENTARY CORRECTION / OPEN DECISIONS REGISTERED / NOT IMPLEMENTED / NOT TESTED / NOT QUALIFIED**
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Scope: correct a demonstrably false acceptance-status statement in WB-14T and separate the overloaded D-ING-05 issue into distinct decision records. This is not authority to select enum mappings or accept a new contract.
- Boundary: documentation only; no normative schema, runtime code, configuration, or infrastructure changed.

## 1. Result

WB-14V makes the smallest justified correction:
1. WB-14T incorrectly said that MH-06 itself remained proposed pending acceptance. The current accepted source, `docs/architecture/MH-06-ADR-001-health-readiness-semantic-contract.md`, is explicitly **ACCEPTED / GOVERNANCE ACCEPTED** for the scoped MH-06 Core Runtime Services semantics; its implementation authorization remains **NO**.
2. The accepted MH-06 vocabulary and generic domain health schema are not identical. This discrepancy is unresolved and does not invalidate MH-06's accepted scope.
3. The prior D-ING-05 umbrella is split into three open decisions: D-ING-05a domain-health/MH-06 scope mapping; D-ING-05b A0 ingress health challenge/response; D-ING-06 A0 lifecycle state/transition ownership.
4. No enum, transition table, transport, issuer, freshness threshold, or schema was selected. The decision records remain OPEN pending accountable owner/governance acceptance.

## 2. Live source state

At start of this pass:
- `main` HEAD: `ab36db009d034db8dca723691e23b331322287e7`.
- Documentation branch HEAD: `1c3720692cbbcf976ef99f94b9474850f934624c`.
- Compare status: diverged; docs branch ahead 1503 / behind 4; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No merge, rebase, cherry-pick, or main-ref change was attempted.

Live blobs read:
- WB-14T: `4a70802f2eafe264f37a5c47ddf0dc82586db212`.
- WB-14U: `1cd8e23f0f534bcfdc4d4b1d060248adb7705b1f`.
- MH-06 accepted ADR source is identified by WB-14U as blob `7dda05379bd70007dc18acd62ed14fc83f0c9226`.
- Domain health schema discrepancy is identified by WB-14U; its vocabulary contains WARNING but not QUARANTINED, unlike accepted MH-06's scoped vocabulary.

## 3. Correction to WB-14T

**Incorrect wording in WB-14T:** “MH-06 itself remains proposed pending full reconciliation/governance acceptance.”

**Correct interpretation:** MH-06 ADR-001 is already ACCEPTED / GOVERNANCE ACCEPTED for its defined Core Runtime Services health/readiness semantic contract. The implementation authorization in that ADR is NO. A separate unresolved discrepancy remains between the generic domain health schema and MH-06's scoped enum. Acceptance of MH-06 does not automatically authorize implementation, broaden its scope, or decide a mapping for the generic schema.

WB-14T should therefore retain its option analysis but no longer describe acceptance of MH-06 itself as pending. D-ING-05 should be treated as decomposed as below.

## 4. Decision split — all OPEN

### D-ING-05a — Generic domain health schema ↔ accepted MH-06 semantics

- **Question:** Are these two schemas intentionally different in scope, or is a governed mapping/contract change required?
- **Known source facts:** MH-06 accepted health values are UNKNOWN, HEALTHY, DEGRADED, FAILED, QUARANTINED. The generic domain health schema currently contains WARNING and does not contain QUARANTINED.
- **Option A:** Keep distinct scopes and define an explicit, owned mapping only at a named boundary.
  - Benefit: avoids silently changing existing consumers or widening MH-06.
  - Cost: requires mapping ownership, loss/ambiguity rules and versioned evidence.
- **Option B:** Propose a controlled change to the generic schema after its consumers and compatibility impacts are inventoried.
  - Benefit: could reduce duplicate semantics if scopes are genuinely the same.
  - Cost: potentially breaking change; requires schema-owner approval and consumer migration planning.
- **Option C:** Keep both unchanged and prohibit implicit conversion until a decision is accepted.
  - Benefit: safest interim behavior.
  - Cost: cross-domain consumers must remain blocked where mapping is required.
- **Recommendation for review only:** Option C as interim guardrail, then choose A or B only after schema ownership and consumer scope are evidenced.
- **Acceptance:** OPEN. No enum changes applied.

### D-ING-05b — A0 ingress health challenge/response

- **Question:** What contract proves that a specific A0 ingress endpoint answered a fresh challenge for the expected request, identity and contract revision?
- **Required properties:** unpredictable per-probe challenge or equivalent non-replay correlation; request/challenge digest binding; authenticated responder identity; observed/captured time and freshness decision; explicit schema/contract revision; transport-probe outcome distinct from entity health, operation readiness, trust and authorization.
- **Open choices:** challenge generation and TTL, clock-skew policy, responder principal, authentication/integrity mechanism, revision allow-list, response signing vs authenticated transport, and stale/replayed challenge handling.
- **No selected technology:** do not assume HMAC, mTLS, signed JSON, a nonce TTL, or a universal status enum.
- **Acceptance:** OPEN. No health endpoint or schema was created.

### D-ING-06 — Corporation-facing A0 lifecycle state machine

- **Question:** What are the authoritative A0 task lifecycle states and allowed transitions visible to Jarvis?
- **Required separation:** admission disposition; A0 lifecycle state; attempt outcome; independent verifier disposition; qualification/gate result; health/readiness; trust/authorization. They are not one enum.
- **Required transition questions:** accepted-to-started semantics; queued/claimed/running transitions; retry and cancellation races; lease expiry/fencing; late results; terminal-state immutability; indeterminate admission commit and reconciliation; result publication and verifier authority.
- **Authority boundary:** A0 owns ASTRA-internal queue/claim/lease/retry/cancellation/recovery and ASTRA-specific evidence/gate transitions within its accepted contract. Jarvis remains corporation-level mission coordinator. MediaHub Product State Authority alone mutates canonical product state.
- **Evidence gap:** no accepted corporation-facing A0 transition table was found in the sources reviewed. ASTRA governance thresholds and non-normative mission/attempt drafts do not fill this gap.
- **Acceptance:** OPEN. No state enum or transition table was registered.

## 5. Decision register impact

Keep the existing D-ING-01 through D-ING-04 items OPEN:
- D-ING-01 service principal and capability issuer.
- D-ING-02 authentication/integrity profile.
- D-ING-03 durable admission/idempotency authority.
- D-ING-04 independent freshness, expiry and replay policies.

Replace the single overloaded D-ING-05 item with D-ING-05a, D-ING-05b and D-ING-06. Do not renumber unrelated project decisions and do not describe any recommendation as accepted.

## 6. Verification and limitations

Completed:
- Refreshed live branch refs and compare state.
- Read current WB-14T and WB-14U source documents and pinned their blob SHAs.
- Confirmed the exact erroneous sentence and its accepted-source contradiction.
- Created a documentary correction and a split decision packet.

Not performed:
- No tests, schema validators, security scans, qualification, workflow dispatch, provider/model calls, credentials, host/runtime inspection, installs, infrastructure changes, deployment, migration, merge, rebase or cherry-pick.
- No enum/schema/code/configuration changes.
- No implementation, endpoint availability, runtime readiness, qualification or acceptance is claimed.

## 7. Next bounded step

WB-14W: reconcile the decision register and continuation pointers against WB-14V, then inspect whether the owner/governance source defines accountable owners and an acceptance path for D-ING-05a, D-ING-05b and D-ING-06. If not, produce a concise owner decision request; do not decide on the owner's behalf.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
