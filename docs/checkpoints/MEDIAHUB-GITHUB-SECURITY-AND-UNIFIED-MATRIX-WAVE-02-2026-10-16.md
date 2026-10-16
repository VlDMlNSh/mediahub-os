# MediaHub OS — GitHub Security Review and Unified Contract Matrix, Wave 02
Date: 2026-10-16
Repository reviewed: https://github.com/VlDMlNSh/mediahub-os
Security review ref: `main`
Documentation ref for this report: `docs/mediahub-chat-tree-map-20261012`
Main tree SHA: `b45324009ac3aa65322a702c28069b12190bc4b8`
Status: STATIC REVIEW / FINDINGS REQUIRE OWNER TRIAGE / NO SECURITY QUALIFICATION CLAIM

## 1. Scope and confidence

The supplied security report was used as the method checklist. Its `example-repo*`, API-key, password and CVE rows are illustrative placeholders; they are not findings about MediaHub OS.

Live GitHub inventory:
- The connected account's owner-filtered repository listing and owner-affiliation listing each returned one visible repository: `VlDMlNSh/mediahub-os`. This establishes connector-visible coverage, not proof that no other repository exists outside this integration's visibility.
- Repository is public, default branch `main`, ID `1350132846`, reported size 17,506 KB, primary language metadata `Python`, open issue count 106, pushed at 2026-10-16 18:48:10 UTC.
- Recursive main tree: SHA `b45324009ac3aa65322a702c28069b12190bc4b8`, 802 entries, 725 files, 77 directories, not truncated.
- 32 GitHub Actions workflow files are present.
- The code-search index is reported unavailable for this repository. GitHub code search returned no results for several security keywords; those empty results are not evidence of a clean scan.
- GitHub branch-protection endpoint returned HTTP 403 for the connected integration. Repository rulesets endpoint returned an empty list. Protection status therefore remains UNKNOWN.
- Code-scanning, Dependabot-alert and secret-scanning alert endpoints were rejected by the available connector. Alert counts remain UNKNOWN.
- No SAST, SCA, secret scanner, container/IaC scanner or qualification command was executed in this pass. No test, model/provider call, credential access, host/runtime inspection or infrastructure action occurred.

## 2. Security findings

| Finding ID | Severity | Evidence | Assessment | Required action |
|---|---|---|---|---|
| SEC-W02-01 | HIGH | [Astra chat control workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-chat-control.yml), blob `51b17ec2410032772f9baa1de4afedb6b000f3c4` | Public issue-comment trigger can invoke control operations. Authorization checks author association OWNER/MEMBER/COLLABORATOR, while workflow-level token permissions grant `contents: write`, `issues: write`, `actions: write`. This is a broad authority surface for a comment-driven controller. | Freeze use of mutation commands until a dedicated security review confirms identity policy, command signing, replay resistance, exact permission needs, branch/target binding and audit behavior. Prefer separate least-privilege jobs/workflows per operation; read-only status must have read-only token permissions. |
| SEC-W02-02 | HIGH | Same workflow, lines in current source: accepted node inputs `mh-dev-02` and `Voktors-Mac-mini.local`; execution step hard-codes `ASTRA_NODE_ID=mh-dev-01`, then asserts `NODE_ID=mh-dev-02` and `EXECUTOR=codex`. | The validation surface and execution identity disagree. Some advertised node/executor combinations can pass initial parsing and fail later, while the workflow retains historical host identities. This conflicts with the greenfield rule that target topology must derive from approved current inventory. | Disable/retire this legacy control path after owner-authorized review; replace host strings with a canonical, versioned target registry and bind the selected target through every execution step. Keep historical IDs only in the legacy ledger. |
| SEC-W02-03 | HIGH | [Astra autonomous supervisor](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-autonomous-supervisor.yml), blob `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | Workflow grants `actions: write`, dispatches downstream workflows, consumes node HMAC secrets, and a later step sets `persist-credentials: true`. This creates a powerful orchestration boundary. Static evidence alone cannot establish a vulnerability, but it warrants a targeted privilege and untrusted-input review. | Inventory every downstream dispatch and write operation; reduce token permissions per job, use `persist-credentials: false` where Git writes are unnecessary, constrain dispatch targets and verify all signed command claims before execution. |
| SEC-W02-04 | HIGH / UNKNOWN | Branch protection request returned 403; rulesets API returned `[]`. | Required reviews, signed commits, status checks, force-push restrictions and admin bypass policy remain unverified. Empty rulesets alone does not prove that branch protection is absent. | Obtain an owner-visible settings export or GitHub UI evidence for `main` and the documentation branch. Record each control and SHA/date of evidence. |
| SEC-W02-05 | HIGH / UNKNOWN | GitHub code scanning, Dependabot alerts and secret-scanning alerts could not be retrieved through this connector. | Actual alert inventory is unknown. No conclusion about zero findings is supported. | Review Security tab and organization/account settings; export alerts and dismissals with rationale; verify secret-scanning push protection and alert coverage. |
| SEC-W02-06 | MEDIUM | Main tree has 32 workflow files; no `codeql.yml`, `dependabot.yml`, `.gitleaks.toml`, `semgrep.yml`, `trivy` workflow or `CODEOWNERS` file was found by exact path inventory. | Dedicated SAST/SCA/secret-scan automation and explicit code ownership are not visible in the inspected main tree. Existing tests and architecture docs do not replace scanner execution. | Add a controlled security workflow plan: CodeQL or Semgrep; dependency review/Dependabot; Gitleaks or equivalent; Trivy config/image scan where applicable; SARIF/evidence retention; explicit ownership. Pin third-party actions to reviewed full commit SHAs. |
| SEC-W02-07 | MEDIUM | [Secret hygiene gate](https://github.com/VlDMlNSh/mediahub-os/blob/main/tests/test_repo_secret_hygiene.py), blob `21991478bac150146b73beffea7a10a4375e52d4`; [Astra Verify](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-verify.yml), blob `ae59d954f1ca6569a8d047589a2a54fd03e47f5b` | A repository secret-hygiene test exists. The inspected workflow contains a synthetic HMAC smoke-test value and the test deliberately exempts that workflow from its hardcoded-secret assignment check. This may be intentional test data, yet the exception is broad by file name. | Replace the literal with an explicitly generated ephemeral test value or narrow the exception to the exact assignment and document the synthetic-value invariant. Confirm the gate is required and current in branch protection. |
| SEC-W02-08 | MEDIUM | [Gemini read-only audit workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-readonly-audit.yml), blob `0d10efdda251f2ceca43175981c919102303572b`; retry workflow blob `96fcc9ed4e45659d0118f0b9f3593a0c736200f0` | Good controls are present: manual dispatch, read-only contents permission, checkout credentials disabled, selected file list, traversal rejection, workflow-context exclusion, bounded file size, suppressed raw error bodies, bounded retries and short artifact retention. Both workflows still accept a caller-supplied ref and task/context inputs; this needs an authorization and provenance review before being treated as a trusted evidence pipeline. | Pin or allowlist refs, validate paths against an explicit allowlist, record the resolved commit SHA and selected file digests, label model output as untrusted advisory evidence, and ensure output cannot automatically authorize mutations. |
| SEC-W02-09 | LOW / FOLLOW-UP | Main tree has only `requirements-dev.txt` among common root dependency manifests matched by inventory; it specifies `PyYAML>=6.0` and `pytest>=8.0`. | The visible dependency set is small, but no lockfile or SCA result was established. This path inventory is insufficient to conclude that transitive dependencies are absent or safe. | Create a reproducible dependency lock/SBOM path and review all actual runtime/build manifests before choosing the SCA policy. |

## 3. Positive controls observed in source

- `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` blob `8d831c2a8fa333977dd86524099568bae2a8db0e` defines default-deny, least privilege, explicit capability scopes, revocation, fail-closed behavior, audit evidence and a supply-chain boundary. Status is PROPOSED ARCHITECTURAL BASELINE, not production acceptance.
- `docs/architecture/MH-12-security-architecture.md` blob `cf4ebfd5bf471ca676f075c51d3a24906504e490` separates security controls from canonical state mutation and explicitly requires governance review, negative tests and evidence before acceptance.
- `docs/architecture/MH-12-secrets.md` blob `4e4faf00e3d24c1de5a394e78670c68786ac9a1e` defines a secrets lifecycle and bars secret material from source, Git history, logs, telemetry, prompts and diagnostic snapshots.
- Gemini audit workflows are read-only with `contents: read`, `persist-credentials: false`, bounded context inputs and bounded retry behavior.
- `tests/test_repo_secret_hygiene.py` defines high-confidence credential-shape checks, quoted literal assignment checks, evidence suppression checks, workflow secret checks and mutation probes. Source presence establishes a test design only; execution status remains UNKNOWN.

## 4. Security-to-contract traceability matrix

| Matrix ID | Requirement / contract | Canonical source | Evidence required | Gate |
|---|---|---|---|---|
| SEC-MAT-001 | No production credentials in Git history or tracked text | MH-12 secrets + secret hygiene test | Scanner version/config, commit range, findings, suppression rationale, digest | Secret hygiene verified |
| SEC-MAT-002 | SAST coverage for maintained code | Security review policy to be approved | Tool/ruleset/version, scope, SARIF, triage and fixed commit | SAST verified |
| SEC-MAT-003 | Dependency and SBOM coverage | Security / supply-chain contract | Complete manifest inventory, lock resolution, SBOM, CVE snapshot | SCA verified |
| SEC-MAT-004 | CI/CD least privilege | Each workflow YAML + GitHub settings | Trigger graph, permission matrix, action SHA pins, token persistence, write destinations | Workflow security review accepted |
| SEC-MAT-005 | Branch governance | GitHub branch protection / rulesets | Required checks/reviews, bypasses, force-push and deletion settings | Governance verified |
| SEC-MAT-006 | Secret alerts and push protection | GitHub Security settings | Alert export, coverage state, push-protection evidence | Secret control verified |
| SEC-MAT-007 | Controller identity and command integrity | Astra chat-control / supervisor contracts | Authorized principal proof, signed command, expiry, nonce/idempotency, target SHA, target identity, replay negative evidence | Controller qualified |
| SEC-MAT-008 | Target topology integrity | Approved greenfield node registry | Registry ref/SHA, lifecycle status, target-to-runner mapping, stale-identity ledger | Target inventory accepted |
| SEC-MAT-009 | Security evidence provenance | Audit/evidence contract | Commit SHA, blob SHA, run ID, tool/version, UTC time, scope, redaction status, verifier | Evidence accepted |
| SEC-MAT-010 | Independent acceptance | Contour A governance and roadmap | Independent verifier, reproducible evidence, explicit acceptance authority | Contour A accepted before Contour B |

## 5. Priority plan

**P0 — establish safe control authority**
1. Obtain owner-visible evidence for branch protection and security-alert settings.
2. Review and gate the issue-comment Astra controller and supervisor workflow before further mutation commands.
3. Reconcile legacy node identifiers against the approved greenfield inventory; preserve historical names only as historical evidence.
4. Confirm whether exposed credentials ever existed in Git history; if any are confirmed, revoke/rotate first, then remediate history under an explicit owner-authorized procedure.

**P1 — create reproducible security coverage**
5. Add a documented, least-privilege security workflow design with pinned action SHAs and non-mutating pull-request behavior.
6. Establish SAST, SCA/SBOM, secret scanning, and IaC/container coverage appropriate to actual project manifests.
7. Bind secret hygiene and security checks to required branch status checks once branch settings are verified.
8. Record exceptions as narrow path/rule-specific suppressions with owner, rationale, expiry and evidence.

**P2 — converge on the single project contract**
9. Extend the unified matrix with security rows, control owner, implementation owner, evidence URI/digest, verifier, freshness, conflict ID and gate.
10. Cross-link each accepted Baseline 2.0 requirement to the implementation contract, security property, workflow/test, verification evidence and acceptance authority.
11. Generate completeness metrics: requirement coverage, source+SHA coverage, security-gate coverage, unresolved conflicts, orphan requirements, stale evidence and duplicated IDs.

## 6. Evidence and limitations

This pass inspected the complete main tree inventory (802 entries, not truncated), repository metadata, workflow inventory (32 files), selected high-risk workflow bodies, the security/trust contract, MH-12 security architecture, secrets rules, secret-hygiene test source and development dependency manifest.

This pass did not read every one of the 725 files, enumerate every branch head, run SAST/SCA/DAST or secret scanners, access security-alert APIs, inspect private settings through the GitHub UI, execute workflows, call external models, use credentials, run tests, inspect hosts/runtime or change infrastructure. Findings are static-review results and prioritized review items, not confirmed exploitability or a clean security bill of health.

## 7. Next action

Wave 03 should build the canonical source registry and the security control evidence ledger from immutable refs/SHAs, then review the Astra comment controller and autonomous supervisor as the first high-priority workflow pair. Keep main and the documentation branch separate: current live compare reports DIVERGED, documentation ref ahead by 1,643 commits and behind by 10, with merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No branch integration is part of this pass.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
