# MediaHub OS Contour A — Trusted Publisher Boundary Design (Wave 177)

Date: 2026-10-19  
Status: **DESIGN PROPOSAL ONLY — NOT APPROVED, NOT IMPLEMENTED, NOT QUALIFIED**

## Purpose

Resolve the publication-credential compatibility blocker found in Wave 176 without restoring broad ambient write credentials to model-controlled worker processes. This document proposes a reviewable boundary; it is not a governance decision and does not authorize workflow dispatch, credential issuance, merge, or deployment.

## Evidence and scope

- Worker source blob on main: 42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d.
- In ops/qualification/run_distributed_local_worker.py, lines 663–679 stage all changes, create a commit, push HEAD:refs/heads/{branch} to origin, and verify the remote branch SHA with git ls-remote.
- Wave 176 candidate PR [#375](https://github.com/VlDMlNSh/mediahub-os/pull/375) sets workflow contents: read and persist-credentials: false on three checkouts, but the candidate contains no separately defined publishing mechanism.
- Exact-head static CI passed, including synthetic negative fixtures. It does not exercise the self-hosted worker publication path. PR #375 remains Draft/open/unmerged and must not be merged as-is.
- PR warning: [comment #6263244730](https://github.com/VlDMlNSh/mediahub-os/pull/375#issuecomment-6263244730).

## Security invariant

**Model-controlled execution must not possess or be able to recover the credential or authority used by the trusted publication operation.** The publisher must not trust a worker-controlled Git configuration, remote URL, hook, index, branch name, commit metadata, generated script, or ambient credential helper.

## Proposed flow

1. **Admission:** a trusted verifier validates the signed command, issuer/capability, task identity, immutable target SHA, allowed repository, and pre-authorized output branch policy. An untrusted worker cannot broaden any of these values.
2. **Execution:** model/worker runs with no GitHub write token and no publication credential in its environment, filesystem, Git config, command-line arguments, or inherited process tree. Its workspace is treated as untrusted.
3. **Result handoff:** worker produces a constrained result bundle: target SHA, proposed file changes/patch, task/command IDs, and content digests. No worker-supplied credential, remote URL, Git metadata, executable publisher script, or arbitrary publish command is accepted.
4. **Independent validation:** a separate trusted publisher validates schema, size limits, allowed paths, forbidden paths, diff policy, base SHA equality, branch naming/allowlist, and repository identity. It reconstructs the publish tree from a clean checkout at the immutable target SHA; it does not reuse the worker's .git directory or working tree.
5. **Narrow publication:** only after validation does the publisher obtain a short-lived, least-privilege credential for the single permitted repository/ref operation. Credential acquisition must be bound to the admitted command/capability and target; it is not forwarded to the worker. If GitHub's available token model cannot enforce the intended ref scope, document that limitation and add an independent branch/ruleset gate rather than assuming scope that does not exist.
6. **Verification and evidence:** publisher records admitted command ID, issuer/capability decision, target SHA, normalized diff digest, resulting commit SHA, destination ref, push result, remote SHA read-back, credential issuer/type/expiry metadata (never the secret), and artifact provenance. Evidence is immutable or tamper-evident and linked to the workflow run.
7. **Failure behavior:** any missing identity, stale base SHA, invalid path, capability mismatch, policy failure, ambiguous run correlation, or remote SHA mismatch fails closed. No automatic retry may widen permissions or silently change target/ref.

## Alternatives considered

| Option | Security/operational properties | Disposition |
|---|---|---|
| Keep write permission and checkout-persisted token in the model worker | Operationally compatible with current git push, but leaves broad ambient write authority reachable from model-controlled execution and shell tools | Reject as default remediation; requires a separately approved risk exception if ever considered |
| Read-only worker checkout with no publisher | Reduces token exposure but leaves the worker's required push path unresolved; current candidate does not demonstrate publication | Not mergeable as-is |
| Separate trusted publisher with constrained result handoff | Best separation of untrusted execution and write authority; requires a designed issuer/capability contract, validation, isolated publisher, and evidence | Preferred design direction for review, not yet approved |
| Have worker request a short-lived write token directly | Token remains reachable from the untrusted worker/process tree and may be exposed through tools or workspace state | Reject unless the architecture proves a stronger isolation boundary than currently evidenced |

## Required contracts and acceptance gates

Before implementation or any worker dispatch:
- Define who is the issuer and authority for a publish capability; keep Jarvis, ASTRA A0 and MediaHub Product State Authority roles separate.
- Define signed/verified binding among command ID, task ID, target SHA, repository, output branch, allowed path policy, expiry and one-time/replay semantics.
- Specify the publisher's trust root, runner/workspace isolation, credential minting and lifetime, repository/ref restriction, and protection against worker-to-publisher filesystem or process injection.
- Define patch/result schema, limits, canonicalization, clean reconstruction, diff allowlist/denylist, and failure codes.
- Define provenance fields, storage, retention, correlation, and independent verification.
- Review branch protection/rulesets and whether token permissions can actually enforce the proposed ref restrictions.
- Add negative tests for wrong target SHA, wrong repository/ref, replay, malformed result, forbidden path, oversized diff, tampered Git metadata, ambiguous run correlation, failed push, and remote SHA mismatch.
- Obtain independent security review and required governance/change-control approval. Only then implement in a separate PR and test with synthetic fixtures. Any end-to-end publication test must use a disposable test repository/ref and explicitly approved synthetic credentials, never production credentials or an unreviewed worker dispatch.

## Non-goals and remaining blockers

This design does not resolve FCC token propagation into the Claude child process, ambient environment minimization, OS/network isolation, A0 issuer/verifier/lifecycle, R-06 authority/privacy, runner/workspace/network manifest acceptance, or bootstrap dependency publisher provenance. These remain separate gates.

## Disposition

**Preferred proposal:** separate the worker from a trusted, independently validating publisher. **Governance status:** pending review/approval. **Implementation status:** none. **Qualification/deployment/acceptance:** none. Do not merge PR #375 as-is and do not dispatch a worker to test this unresolved path.

## Related evidence

- [Wave 176 credential minimization report](MEDIAHUB-CONTOUR-A-WORKER-CHECKOUT-CREDENTIAL-MINIMIZATION-WAVE-176-2026-10-19.md)
- [PR #375](https://github.com/VlDMlNSh/mediahub-os/pull/375)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
