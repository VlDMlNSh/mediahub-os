# MediaHub OS — Runner/workspace/network target manifest source discovery, Wave 478

- Date: 2026-10-30
- Work item: CAF-Q-012 (related CAF-Q-007)
- Status: **SOURCE DISCOVERY PARTIALLY COMPLETE / CANDIDATE PROPOSED / ACCEPTANCE OPEN**
- Contour: A
- Target main SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Working branch: `docs/wave478-runner-target-manifest-discovery-20261030`
- Candidate manifest: [MEDIAHUB-RUNNER-WORKSPACE-NETWORK-TARGET-MANIFEST-CANDIDATE-WAVE-478-2026-10-30.json](MEDIAHUB-RUNNER-WORKSPACE-NETWORK-TARGET-MANIFEST-CANDIDATE-WAVE-478-2026-10-30.json)
- Candidate manifest blob SHA: `b2ee53f0f1caed379d0fc15172c1f3f52edacc37`
- Parent issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Result

Repository source discovery found no previously accepted authoritative runner/workspace/network target manifest. The Wave 08 reference architecture and Wave 14 credential/egress architecture define the intended ephemeral-worker and direct-egress principles, but Wave 14 explicitly records the target manifest as UNKNOWN / source discovery open. The activation queue still marks CAF-Q-012 as `SOURCE_DISCOVERY_REQUIRED`.

A versioned candidate has therefore been added as a **proposal only**. It is not an accepted policy, does not authorize agent dispatch, provider calls, secret access, workflow dispatch, or deployment.

## 2. GitHub-hosted standard runner profile (documented facts)

The repository metadata reports `public`. GitHub's current runner documentation states that public repositories can use standard GitHub-hosted Linux x64 runners with 4 vCPU, 16 GB RAM and 14 GB SSD, free and unlimited by minutes. The proposed image label is `ubuntu-24.04`.

GitHub's current Actions limits documentation states:
- GitHub Free standard GitHub-hosted runner concurrency: **20 simultaneous jobs**.
- Maximum execution time for one GitHub-hosted job: **6 hours**.
- GitHub-hosted job concurrency may be subject to account/platform limits and support-controlled changes.

The repository being public is verified; the actual subscription plan of the owner account was not exposed by the connected repository API. Therefore the Free-plan concurrency figure is a planning assumption, not an account-entitlement audit. Do not translate the 20 jobs into a promise of 20 immediately available machines.

## 3. Isolation and storage boundary

GitHub documentation says each non-slim standard hosted job receives a fresh VM. The `GITHUB_WORKSPACE` directory is job-local and may be shared between steps in the same job; it is not a shared filesystem across jobs. Cross-job handoff must use explicit artifacts or commits.

Candidate controls:
- pin the checkout to the immutable task SHA;
- set `persist-credentials: false`;
- default workflow/job permissions to `contents: read`;
- do not persist provider credentials in workspace, cache, artifact, prompt or logs;
- use explicit artifact retention and deletion policy;
- do not use self-hosted runners for untrusted public-repository pull-request code.

VM teardown is part of the hosted-runner lifecycle, but the repository's actual artifact retention, cache policy and cleanup evidence have not been qualified.

## 4. Network and compute boundary

The existing Wave 14 and Wave 18 architecture documents state that hosted-runner egress IPs are dynamic/shared by default and that a stable source IP must not be assumed. The candidate therefore uses direct outbound HTTPS and no fixed-IP dependency by default.

A provider's requirement for source-IP allowlisting would block this standard-runner profile until a separately approved target profile is selected. The current source review did not demonstrate enforceable destination-level network allowlisting on the standard hosted runner network layer. Provider calls remain blocked until destination authorization and effective egress controls are accepted.

No GitHub source guarantees inter-runner bandwidth, low latency, direct peer reachability or a shared high-speed network. The profile is suitable as a candidate for independent bounded jobs; distributed tensor/pipeline model inference is NOT QUALIFIED.

A later read-only benchmark may measure DNS/TLS/connect latency, throughput to explicitly approved endpoints, packet loss where supported, run stability and teardown. No provider endpoint test is authorized by this report.

## 5. Repository and governance snapshot

- `main` HEAD observed: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Repository visibility: public.
- Issue #301: OPEN; last updated 2026-10-30.
- PRs #587, #588 and #589: OPEN; each had 0 formal reviews and 0 inline review threads at inspection time.
- Canonical documentation branch compared with `main`: diverged, 3,455 commits ahead and 82 behind. The new working branch was created from the canonical documentation branch, not from `main`; this report is not a claim that the documentation branch is integrated into `main`.
- Exact current PR head SHAs and complete exact-head CI/ruleset contexts were not available through the inspected response; those gates remain NOT VERIFIED.
- Active SentinelX inventory: one operational host `host_5f7264034bdf0b51` / `Voktors-Mini.Dlink`; Free plan capacity 1/1. `mh-dev-01` and `mh-dev-02` are disabled. No third server is available/qualified for a Claude task.
- Gemini controller source on `main` was read at blob SHA `0a1246f6755020faf8b7e48d07bfff790bbaece3`. It supports bounded modes but live dispatch gates remain separate. No controller probe or agent dispatch was run in this pass.

## 6. Evidence and checks

| Item | Evidence | Result |
|---|---|---|
| Wave 08 reference architecture | blob `712faccec5a35f2ed56b86f23a42cd4a1a5b4710` | Read |
| Wave 14 credential/egress architecture | blob `21ab57f932594bed670583d0eb66d4abb076755f` | Read; target manifest still UNKNOWN |
| Wave 18 direct-egress decision | blob `d7730895d97f84fc8ff25d1fdda61558dbd50696` | Read; target manifest gate open |
| Activation queue | blob `0d4d591f464b976d6920bbd39c87a45a9d4fda59` | CAF-Q-012 remains SOURCE_DISCOVERY_REQUIRED |
| Candidate manifest | blob `b2ee53f0f1caed379d0fc15172c1f3f52edacc37` | Read-back exact match |
| GitHub runner docs | https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job | Current standard runner specs read |
| GitHub runner reference | https://docs.github.com/en/actions/reference/runners/github-hosted-runners | Workspace semantics read |
| GitHub Actions limits | https://docs.github.com/en/actions/reference/limits | Free concurrency and 6h job limit read |
| GitHub Actions secure use | https://docs.github.com/en/actions/reference/security/secure-use | Hosted runner isolation/security guidance read |

No workflow was changed or dispatched. No benchmark, provider call, secret read, agent execution, test suite, merge, deployment or qualification was performed.

## 7. Remaining acceptance work

1. Obtain an accountable authority's acceptance of the exact target profile and its workspace/network controls.
2. Resolve the destination-level egress enforcement gap; otherwise keep provider-connected jobs blocked.
3. Verify actual account plan, effective concurrent-job entitlement and artifact retention settings.
4. Build a read-only, non-secret benchmark only after the workflow target and permitted endpoints are reviewed.
5. Record actual run/job IDs, runner metadata, throughput/latency measurements, artifact digests and cleanup evidence.
6. Obtain independent security/provenance review and update CAF-Q-012 only after the exit evidence is complete.

## 8. State

- Candidate design: **PROPOSED**
- Source discovery: **PARTIALLY COMPLETE**
- Runtime benchmark: **NOT RUN**
- Agent dispatch: **NOT RUN**
- Provider calls / secret access: **NOT RUN**
- Independent review: **NOT VERIFIED**
- Qualification: **NOT QUALIFIED**
- Acceptance: **NOT ACCEPTED**
- Contour A: **NOT ACCEPTED**
- Contour B: **GATED**

Next: obtain review of this candidate manifest and resolve egress-enforcement/authority gaps before creating or dispatching a benchmark workflow.

## 9. Documentation review PR

- Draft PR: [#590 — propose hosted runner target manifest](https://github.com/VlDMlNSh/mediahub-os/pull/590).
- Initial PR head: `13ce12764c5b72f323b4b579ad9660d959027a95`; base: canonical documentation branch.
- PR state at inspection: OPEN / DRAFT / UNMERGED; 0 formal reviews; 0 inline review threads.
- No pull-request workflow runs were returned for the inspected PR head. CI/review status: **NOT VERIFIED**, not PASS.
- PR is documentation-only and requires independent architecture/security review before acceptance.
