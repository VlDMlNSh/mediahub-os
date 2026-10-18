# MediaHub OS — A0 issuer governance decision-gate matrix, Wave 149

- Date: 2026-10-18
- Status: **GOVERNANCE INPUT CROSSWALK / OPTIONS NOT SELECTED / IMPLEMENTATION BLOCKED / NOT QUALIFIED**
- Scope: reconcile the accepted MH-12 security invariants, the WB-05 issuer-authority decision packet, the WB-06 producer/consumer inventory, Wave 134 call-site closure and Wave 148 source revalidation. This is a documentary crosswalk, not an owner decision, independent security review, implementation or qualification.

## 1. Outcome

The prior records do not contain a selected issuer-ownership option or an accepted trusted-context lifecycle. WB-05 explicitly leaves options A–D unselected. The latest bounded evidence still separates:
- Jarvis corporation-level mission coordination;
- ASTRA A0 internal engineering workflow state;
- MediaHub Product State Authority as sole canonical product-state mutation authority;
- security issuance/attestation and verification, whose accountable owner remains undecided.

Accordingly, the next safe step is not to choose a token library or patch the ingress. It is to close the governance questions below with an explicit, source-backed decision and then derive the minimal verifier contract. No user/owner decision is inferred from a request to continue engineering autonomously.

## 2. Source refs and evidence

| Source | Exact ref/blob | Evidence and limit |
|---|---|---|
| MH-12 Security Architecture | `main`, blob `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Canonical path includes identity/authentication/trust/capability/authorization/policy/consumer boundary/State Authority/audit. Capability must bind issuer, principal, operation, resource, scope, constraints, provenance, lifetime and revocation; no self-grant; delegation is explicit, bounded and revocable. Status remains governance review required. |
| WB-05 Issuer Authority and Trusted-Context Owner Decision Packet | `docs/mediahub-chat-tree-map-20261012`, blob `1b562c6546b1216f2ee89095cd6a78427a967dc5` | GOV-CAP-01…07 list seven decisions; options A–D are all PROPOSED and unselected. The document explicitly does not select product/protocol/token/key store. |
| WB-06 AuthorizationContext Producer/Consumer Inventory | `docs/mediahub-chat-tree-map-20261012`, blob `9bd850e869dbd19db9bde2ce08768aaf502c95a2` | Local typed context/tuple-grant path and command-envelope HMAC path are not evidenced as connected to Jarvis→A0 ingress. Bounded inventory, not repository-wide absence proof. |
| Wave 134 trusted-context call-site closure | `docs/mediahub-chat-tree-map-20261012`, blob `cd6f6021bc5b617ef0bc581bfe4a6748515ce81e` | 193 tracked Python blobs scanned at its pinned tree snapshot; three direct constructors were qualification fixtures, not an authoritative production issuer. Trust lifecycle gap remains open. |
| Wave 148 ingress trust-boundary revalidation | report blob `a0f00dd08e99e913e1f6949843e6943ecb937b15` | File ingress accepts shape-checked, file-supplied `approval_state`; no issuer verification or `AuthorizationContext` propagation was established in the inspected path. Two HMAC envelopes remain distinct. |
| Functional Baseline 2.0 | `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Accepted immutable functional reference; architecture artifacts do not imply implementation, verification or qualification. |

## 3. Governance decision gate

| Gate | Decision required | Minimum evidence before implementation | Fail-closed consequence until closed |
|---|---|---|---|
| GOV-CAP-01 | Accountable capability issuer/attester role and its scope | Owner/governance record names the accountable role, grant authority and forbidden grants | No production trusted-context minting |
| GOV-CAP-02 | Service-principal enrollment, suspension, recovery and re-enrollment owner | Accepted lifecycle and authoritative status source | Unknown/unverified principals denied |
| GOV-CAP-03 | Mandatory verifier locations and responsibilities | Named checks at external ingress and protected consumer boundary; negative cases defined | No caller-supplied field or Python type treated as provenance |
| GOV-CAP-04 | Trust-anchor custody, rotation and compromise response | Accountable operator, rotation/revocation process and incident response | Unknown key/issuer or failed verification denied |
| GOV-CAP-05 | Expiry/revocation freshness and in-flight work behavior | Maximum stale window, re-check points, and cancellation/containment semantics | Stale or unobservable authorization denied for protected mutation |
| GOV-CAP-06 | Jarvis→A0 delegation bounds | Operation/resource mapping, audience, scope attenuation, and explicit non-inheritance | No implied corporate or product-state capability transfer |
| GOV-CAP-07 | Acceptance evidence and independent reviewer | Positive/negative test criteria, provenance evidence, reviewer role and separate qualification gate | No ingress acceptance or Contour A qualification claim |

## 4. Cross-cutting R-06 audit/privacy gate

The map's prior R-06 record lists unresolved items: canonical security-flow mapping; principal/delegation scope; lifecycle failure semantics; minimal audit evidence/access/retention; MH-13 status boundaries; and required-audit unavailability behavior. This pass did not retrieve an accepted MH-13 decision or independently accepted R-06 closure, so these remain unresolved rather than being restated as closed.

Before an implementation is selected, governance/security review must specify:
1. Minimum audit fields without secret/token leakage, plus access and retention ownership.
2. Whether audit unavailability blocks each protected operation, and any narrowly defined safe exception.
3. Privacy classification and retention limits for principal, task, target/resource, decision and provenance records.
4. How expiry, revocation, replay rejection, denial and recovery events are recorded and correlated.
5. Independent review and evidence integrity expectations.

No decision is made here on a particular audit product, token format, key store, protocol, availability policy or retention period.

## 5. Technology-neutral verifier contract to derive only after decisions

The accepted contract should require verification of: issuer trust; subject/principal; audience; operation; resource/target; scope and constraints; provenance; issue/expiry times; revocation/freshness state; delegation attenuation; replay/idempotency semantics; and audit availability policy. Malformed, forged, expired, revoked, replayed, wrong-audience, wrong-resource, over-broad, unverifiable or ambiguous inputs must fail closed before protected mutation.

These are contract dimensions derived from MH-12, not a chosen wire schema or claim that the current runtime implements them. The command HMAC envelopes must not be reused as trusted-context tokens without an explicit compatibility/security decision.

## 6. Repository state and bounded action

- `main` HEAD at revalidation: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`; it is divergent from main. No merge/rebase/cherry-pick was performed.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open; its scope explicitly says the tracker does not itself authorize credentials, provider calls, dispatch, infrastructure change, merge or deployment.
- PR [#358](https://github.com/VlDMlNSh/mediahub-os/pull/358) remains Draft/open/unmerged. Its run-correlation CI does not prove issuer lifecycle or qualify Contour A.
- No source code, tests, credentials, provider calls, workflow dispatch, host/runtime access, deployment, merge or qualification was performed in this pass.

**Next step:** obtain/record the explicit GOV-CAP-01…07 and R-06 dispositions under the established owner/governance process. Once recorded, translate only the accepted decisions into a versioned ingress/verifier contract and negative test matrix. Until then, Jarvis→A0 trusted ingress remains blocked; Contour A is NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED; Contour B remains gated.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
