# MediaHub OS — Source-Pinned Issuer/Verifier Reuse Inventory, Wave 70

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Ref: `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`
- Status: **SOURCE-ONLY INVENTORY / CANDIDATES / NOT SELECTED / ACCEPTANCE OPEN**
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Prior decision proposal: [Wave 69](MEDIAHUB-A0-ISSUER-AND-JARVIS-INGRESS-DECISION-PROPOSAL-WAVE-69-2026-10-17.md)

## 1. Scope and result

This pass compares existing public GitHub projects against the A0-owned capability issuer + GitHub Actions transport proposal. It is a source-level fit assessment, not a dependency audit, implementation, qualification or selection decision.

**Result:** no reviewed repository establishes a complete, ready-to-admit A0 issuer/verifier lifecycle for MediaHub. Reuse is promising for separate primitives—policy evaluation and artifact signature/provenance verification—but those primitives do not collectively become an accepted capability protocol without an explicit contract and integration review.

## 2. Source-pinned candidates

| Candidate | Source ref / README blob SHA | Reusable role | Important boundary |
|---|---|---|---|
| [sigstore/cosign](https://github.com/sigstore/cosign) | `main` / `293d76bc813a579636e1030575ce604959b17615` | Artifact/container signing and signature verification; keyless, key-pair, KMS and bring-your-own-PKI options are described by README | Does not define MediaHub mission authorization, A0 issuer authority, task capability scope, lease/fencing, cancellation or revocation semantics |
| [sigstore/sigstore](https://github.com/sigstore/sigstore) | `main` / `c5ad9511694219b85ddbe3bf7951784c50303407` | Shared signing interfaces, including ECDSA, Ed25519, RSA and DSSE/in-toto; OIDC client code | Library primitives only; does not establish a complete deployment trust model or MediaHub-specific issuer contract |
| [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | `main` / `860399b5b7ac265f89508796831990a45eb485c4` | Declarative, context-aware policy evaluation for authorization decisions | Policy evaluation is distinct from authenticated identity, capability issuance, integrity verification, durable audit, revocation and lease lifecycle |
| [spiffe/spire](https://github.com/spiffe/spire) | `main` / `95ba30aa3dcd011dc79babaa472ec94c31f76a9c` | Workload identity, SPIFFE IDs/SVIDs, workload attestation and workload-to-workload trust | Adds a trust/runtime architecture; compatibility with ephemeral GitHub-hosted runners and the no-owner-operated-server constraint remains unverified |

The SHAs above identify the exact README blobs read during this pass; they do not pin releases, binaries, transitive dependencies or executable artifacts.

## 3. Fit against MediaHub admission requirements

| Requirement | Candidate coverage from reviewed README | Disposition |
|---|---|---|
| Artifact integrity and provenance | Cosign / Sigstore offer signing and verification primitives | Candidate primitive; select format, identity constraints, trust roots and verification policy separately |
| Declarative authorization policy | OPA is a policy engine | Candidate primitive; caller identity and trusted policy input remain external requirements |
| Workload identity | SPIRE provides workload identity and attestation mechanisms | Conditional candidate; operational topology and GitHub runner integration need evidence |
| A0 issuer authority and delegation | No reviewed README establishes MediaHub's accepted A0 issuer | OPEN |
| Audience, repository/ref/commit/task binding | Must be specified and independently verified in the MediaHub contract | OPEN |
| Expiry, rotation, revocation, replay/idempotency | No end-to-end MediaHub lifecycle established by this inventory | OPEN |
| Lease/fencing, cancellation, recovery | Requires integration with ASTRA lifecycle semantics | OPEN |
| R-06 audit, retention, outage and reconciliation | Requires accepted governance disposition and evidence sink policy | OPEN |
| Accepted runner/workspace/network target | Separate owner-accepted target manifest required | OPEN |

## 4. Recommended reuse boundary

For the next design revision, evaluate a narrow composition rather than a new cryptographic subsystem:

1. GitHub Actions remains transport/execution, with immutable repository/ref/commit/workflow identity as inputs to authorization.
2. A0 remains the proposed authority for issuing a task-scoped capability, conditional on a named decision authority, accepted trust root and documented issuer path.
3. An independent verifier validates issuer, audience, expiry/revocation status, task scope, immutable source SHA and lifecycle/fencing claims.
4. OPA may evaluate policy only after the identity and request context are authenticated and normalized.
5. Cosign/Sigstore may verify signed evidence/artifacts using a separately accepted identity and trust policy.
6. SPIRE remains optional and conditional; avoid adding a long-lived identity service until its fit with GitHub-hosted ephemeral execution is demonstrated.

This is a design direction for review, not an accepted component selection. Do not treat OPA, Cosign or SPIRE individually as the A0 issuer.

## 5. Open gates and next action

- A0 issuer/delegation and ingress contract: OPEN.
- R-06 accountable authority, independent reviewers, retention/outage/reconciliation decisions: OPEN.
- Owner-accepted runner/workspace/network target manifest: UNKNOWN / BLOCKED.
- Capability schema and semantic-reference validation: OPEN.
- Implementation, tests, qualification and workflow dispatch: require separate explicit authorization after admission gates close.

Next bounded action: inspect the repository's existing internal signer/verifier and capability candidates by exact path/SHA against this matrix, then prepare a minimal interface crosswalk. Preserve source refs and report mismatches rather than introducing code.

## 6. Verification and authorization boundary

This pass read public GitHub README content and current project records only. No packages were installed, no tests or qualification were run, no provider/model calls or credentials were used, no workflow was dispatched, and no runtime/host or infrastructure was inspected or changed. No merge, rebase or branch integration occurred.

**Disposition: SOURCE-ONLY INVENTORY COMPLETE FOR THIS PASS / NO COMPONENT SELECTED / ADMISSION OPEN.**

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
