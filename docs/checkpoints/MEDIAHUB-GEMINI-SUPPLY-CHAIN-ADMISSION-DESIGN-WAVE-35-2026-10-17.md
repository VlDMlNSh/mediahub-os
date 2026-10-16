# MediaHub OS — Gemini Workflow Supply-Chain and Admission Design, Wave 35

- Date: 2026-10-17
- ID: MH-GEMINI-SUPPLY-CHAIN-ADMISSION-35
- Contour: A — Developer Fabric
- Status: SOURCE REVIEW / DESIGN ONLY / WORKFLOW UNCHANGED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- MediaHub `main` HEAD reviewed: `149f5af85962a7a1219a4012e1f4b0b8b335a0a3`
- Workflow blob reviewed: `b81e9cf829d1272fe7ea0db8ce8e4b48adcc272a`
- Prior trust/config report: [Wave 34](MEDIAHUB-GEMINI-TRUST-CONFIG-RECONCILIATION-WAVE-34-2026-10-17.md), blob `00d6b14a1f491bfc2de0b691c54f5d51d09827e4`

## 1. Bounded-pass outcome

This pass attempted to resolve the exact OCI image identity for `ghcr.io/github/github-mcp-server:v0.27.0`, inspected the pinned Google Action's input contract, and specified a minimal admission/evidence design. Public source and repository documentation only.

No workflow edit, dispatch, model/provider invocation, credential access, tests, qualification, host/runtime inspection, installation, infrastructure change, deployment, or branch integration occurred.

## 2. Current repository state

- `main` HEAD: `149f5af85962a7a1219a4012e1f4b0b8b335a0a3`.
- Documentation branch comparison: DIVERGED; ahead 1943 / behind 11.
- Merge base: `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Workflow remains unchanged on `main`; its MCP image reference is the mutable tag `ghcr.io/github/github-mcp-server:v0.27.0`.
- The documentation branch and `main` remain divergent. This pass performs no merge, rebase, cherry-pick, or synchronization.

## 3. OCI identity and provenance determination

The reviewed source association for the MCP server tag points to source commit `2b352ab0b914cde8c16d44200a7cace9f400be71`. That is a source revision, **not** an OCI manifest digest.

The public source/release search and accessible GitHub source pages in this pass did not provide a verifiable, exact `sha256:<64 hex>` manifest digest tied to the image tag and target platform, plus attestations binding that image digest to the source revision and build workflow. Therefore:
- Exact OCI digest: UNKNOWN / BLOCKED.
- Platform-specific manifest selection: UNKNOWN / BLOCKED.
- Signed tag: unavailable for the reviewed source tag; prior source review records it as unsigned.
- Image provenance/SLSA attestation and reproducible binding: UNVERIFIED.
- Do not convert the source commit SHA into an image digest, and do not infer the digest from the tag name.

Required closure evidence: query the OCI registry manifest for the exact repository/tag; record the returned index digest and each supported platform manifest digest; capture registry response timestamp and media type; retrieve and verify available cosign/Sigstore or GitHub artifact attestations; verify repository, workflow identity, source commit, builder identity, and subject digest; store the evidence in a reviewable provenance record. Until then, retain BLOCKED.

## 4. Immutable Action and CLI pin proposal

The reviewed Google Action source reference is `google-github-actions/run-gemini-cli@f77273f4c914e4bf38440cf36a0369cb64a37489`; the Checkout reference candidate is `actions/checkout@11d5960a326750d5838078e36cf38b85af677262`. Prior source review reports GitHub API signature verification for both commits. These are source candidates for a proposed change, not a qualified workflow.

The Action's `action.yml` declares `gemini_cli_version` with default `latest`, and the `settings` input writes project configuration to `.gemini/settings.json`. Thus pinning the Action commit alone does not pin the installed CLI or remove project-settings influence. The previously reviewed CLI `v0.64.0` package SHA-256 `9d4ad33d15dcf35098919c69eb9d98b6dc640567f141d6fc4f8f053c8cbd8dae` remains a candidate only; installation behavior and provenance have not been qualified. Do not label it approved.

Proposal for a future, separately authorized workflow change:
1. Pin each third-party Action to a full immutable commit SHA and retain source provenance for that commit.
2. Pin the CLI to an explicit reviewed version; verify downloaded package integrity and provenance in a controlled preflight. Fail closed on mismatch.
3. Pin the MCP container by verified OCI digest, including explicit platform policy. Keep this item blocked pending section 3 evidence.
4. Replace broad job write permissions with split jobs: unprivileged analysis/artifact generation, then a separately gated publisher that validates the proposed diff and has only the minimum GitHub write scopes.
5. Remove model-controlled access to unrestricted repository writes until the admission boundary below is implemented and independently reviewed.
6. Treat trust bypass as a documented risk acceptance item. Do not remove or rename the trust variable blindly: Wave 34 found conflicting Action-guide and CLI-source names, and project settings/MCP availability depend on workspace trust behavior.

## 5. Independent path/diff admission contract

The model prompt is advisory; it cannot serve as the enforcement boundary. Before any candidate change receives a write-capable GitHub token, a trusted validator outside the model-controlled workspace must evaluate the complete candidate tree/diff.

Mandatory checks:
- Canonical base SHA is resolved before generation and rechecked immediately before publication.
- Changed paths are normalized and matched against an explicit per-task allowlist; reject absolute paths, traversal segments, symlink escapes, case-folding ambiguities, submodule changes, unexpected binary files, and generated files outside scope.
- Enforce maximum changed-file count, per-file and total diff bytes, line count, and rename/delete policy.
- Reject edits to workflow permissions, action refs, trust settings, MCP tool lists, secret references, CODEOWNERS, branch protection policy, validator code, and acceptance policy unless the task's separately authorized allowlist explicitly includes the exact path.
- Scan candidate text for secret-like material and credential-bearing URLs; redact scanner output so evidence itself cannot leak sensitive content.
- Validate patch application and resulting tree identity in a disposable, unprivileged context. This is a design requirement; no test was run in this pass.
- Generate a canonical machine-readable decision record with pass/fail reasons and content hashes. Publisher accepts only the exact tree SHA whose validation record is signed or otherwise bound by a trusted CI identity.
- Require independent review and protected-branch policy. PR creation and merging remain distinct actions; merge/deployment gates remain outside this workflow.

## 6. Sanitized evidence manifest contract

Minimum fields:
- schema/version, task ID, run ID, repository, workflow path and workflow commit;
- base ref and exact base commit SHA;
- candidate branch, head commit/tree SHA, changed paths and per-file diff SHA-256;
- Action commit SHA, CLI version and package digest, MCP OCI index/platform digest, provenance verification result and evidence URLs;
- validator version/commit, policy version/hash, decision, rejected-path count, diff limits and secret-scan summary without matched secret values;
- artifact names, SHA-256 hashes, retention class and UTC creation timestamp;
- reviewer identities/decisions, required checks, and explicit verification exclusions;
- no API keys, bearer tokens, raw environment dumps, prompt secrets, or unredacted scanner matches.

The manifest must be generated by trusted workflow code from actual run metadata, not authored by the model. A missing field, mismatch, failed verification, or unsupported provenance status must fail closed.

## 7. Dependency and acceptance gates

- Clean target: UNKNOWN / BLOCKED. Wave 10 found no owner-accepted exact target manifest; MH-15 remains unaccepted/unfrozen and implementation authorization remains NONE.
- A0, MH-12 and R-06: OPEN. This pass records no closure evidence and grants no acceptance.
- OCI digest/provenance: BLOCKED.
- CLI version/provenance: candidate only; BLOCKED for production pin acceptance.
- External path/diff validator and evidence manifest: DESIGN ONLY; implementation and verification pending.
- Workflow hardening: proposal only; workflow unchanged.
- Contour B product implementation remains behind Contour A deployment and independent acceptance gates.

## 8. Sources reviewed

- MediaHub workflow at main: https://github.com/VlDMlNSh/mediahub-os/blob/149f5af85962a7a1219a4012e1f4b0b8b335a0a3/.github/workflows/gemini-autonomous-engineering.yml
- Google Action `action.yml` at source commit: https://github.com/google-github-actions/run-gemini-cli/blob/f77273f4c914e4bf38440cf36a0369cb64a37489/action.yml
- MCP server source commit: https://github.com/github/github-mcp-server/tree/2b352ab0b914cde8c16d44200a7cace9f400be71
- MCP release page: https://github.com/github/github-mcp-server/releases/tag/v0.27.0
- Clean-target authority reconciliation, Wave 10: `docs/checkpoints/MEDIAHUB-CLEAN-TARGET-MANIFEST-AUTHORITY-RECONCILIATION-WAVE-10-2026-10-16.md`, blob `1f748bf80e08067fd85a7e1b0821cc4d12bda676`
- Trust/config reconciliation, Wave 34: [report](MEDIAHUB-GEMINI-TRUST-CONFIG-RECONCILIATION-WAVE-34-2026-10-17.md)

## 9. Next bounded step

Resolve OCI registry digest and provenance using an authoritative registry/attestation path. If that remains inaccessible, preserve the BLOCKED gate and produce a concise evidence-gap record. Then map the admission design to existing validator and evidence components already present in GitHub before proposing new code. No runtime action, workflow dispatch, provider invocation, test, qualification, infrastructure change, or branch integration is authorized by this report.
