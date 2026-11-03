# MediaHub OS — Colibri duplicate-PR and canonical documentation reconciliation — Wave 524

Date: 2026-11-03

## Scope and disposition

Bounded read-only reconciliation of the current canonical documentation state and the open Wave 521 / Wave 522 documentation proposals. This report does not admit Colibri, qualify a runner, modify runtime code, dispatch cloud agents, access secrets, merge PRs, deploy infrastructure, or accept Contour A.

**Disposition: DOCUMENTATION RECONCILIATION PROPOSED / NOT ACCEPTED. Colibri remains RESEARCHED / NOT ADMITTED / NOT INSTALLED / NOT QUALIFIED.**

## Immutable repository state

- Repository: https://github.com/VlDMlNSh/mediahub-os
- `main` HEAD: `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`.
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Canonical documentation branch HEAD: `d9a289b9113f7567711b641a7017eb814d6c259d`.
- Canonical map blob: `75f62685459ec99ebf8be478f4e9096cdb842b1d` (latest indexed Wave 477).
- Canonical continuation checkpoint blob: `fd312ded05dd1898bd36d776a9669bb02920720d` (latest indexed Wave 392).
- Canonical Master Roadmap blob: `ea7e94e921045253f3e6494438e197c4bafae3a0` (latest indexed Wave 458).
- Functional Baseline 2.0 blob on `main`: `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; status is ACCEPTED / CANONICAL IMMUTABLE REFERENCE POINT. Baseline 1.0 remains historical provenance.

Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) is OPEN and has 237 comments. The newest comment visible on the latest comments page is owner comment [Wave 523](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6577264002), dated 2026-11-02. No Wave 524/525 owner evidence comment was present at the time of this read.

## Open documentation candidates

| PR | Scope | Base / immutable head | Files | State |
|---|---|---|---:|---|
| [#628](https://github.com/VlDMlNSh/mediahub-os/pull/628) | Wave 521 PR #610 ECC preflight reconciliation | docs canonical / `a3e0c26ffb04265ade33057c0bafecb0f22f3f23` | 3 | OPEN / DRAFT |
| [#629](https://github.com/VlDMlNSh/mediahub-os/pull/629) | Wave 522 Colibri GLM-5.2 suitability assessment | stacked on #628 branch / `87ae3296a7f310e02f32f836c17ff3e3e4a1a709` | 3 | OPEN / DRAFT |
| [#630](https://github.com/VlDMlNSh/mediahub-os/pull/630) | Wave 522 Colibri GLM-5.2 admission audit | docs canonical / `a22ee7bd72a79155ce8ffdf6091c6a5dedb625b6` | 4 | OPEN / DRAFT |
| [#625](https://github.com/VlDMlNSh/mediahub-os/pull/625) | Owner-directed two-Ubuntu-runner topology proposal | docs canonical / `01efb5e6264b4cb84aee1d9c0c162be77cd1f264` | proposal | OPEN / READY |

Exact-head check-run lookup for PR #625/#628/#629/#630 returned **0 check-runs** for each tested HEAD. Combined commit status returned **pending / 0 contexts** for all four. Formal PR review submissions: **0**; inline review threads: **0**. Thus exact-head CI and independent review are **NOT VERIFIED**, not PASS. PR #629 is based on the PR #628 branch and is stacked; PR #630 is an alternative Wave 522 candidate based directly on the canonical docs branch. None is canonical or accepted.

## Colibri evidence reconciliation

Both Wave 522 reports cite the same inspected upstream source commit, `JustVugg/colibri@0a5504a1dc64f86fcd0fe7db298b0448c730e7e6`, and support the following common findings:

1. Colibri is a local inference engine, not a hosted GLM API service.
2. GLM-5.2 is documented by the inspected model inventory; GLM-4.7 support is not documented / NOT VERIFIED.
3. GLM-5.2 is listed at approximately 429 GB on disk, with 16 GB minimum and 24 GB recommended RAM.
4. The standard public GitHub-hosted Ubuntu runner's 14 GB SSD cannot hold that model. The standard runner is therefore not a viable Colibri/GLM-5.2 target.
5. The API exposes OpenAI-compatible Chat Completions and Anthropic Messages surfaces. A single generation slot / queued requests is a throughput limitation; authentication is optional by default and must be explicitly enabled before any non-loopback use.
6. No MediaHub Colibri installation, model download, inference, benchmark, provider call, credential use, runner allocation or runtime qualification occurred.

PR #630 provides the more complete admission analysis: it adds the larger 16-vCPU / 64-GB RAM / 600-GB SSD runner as a theoretical capacity-plausible scenario, while explicitly leaving account availability, cost/budget, usable disk, throughput, provenance, isolation and runtime unverified. It also records concrete API admission/security requirements (loopback/private binding, runtime API key, no insecure bind override, no wildcard Host/CORS, model/shard digests and queue/cancellation measurements). PR #629's narrower conclusion—that Colibri is not a fit for the ordinary runner and should remain only a separately qualified local-compute candidate—is compatible with, but less complete than, this analysis.

**Reconciliation decision:** do not merge both Wave 522 proposals as-is and do not close either PR autonomously. Preserve PR #630 as the fuller technical source candidate; reconcile any unique detail from #629 into one consolidated Wave 522 record after independent review. Keep its larger-runner scenario explicitly **CAPACITY-PLAUSIBLE / NOT APPROVED / NOT QUALIFIED**, not as a recommendation to purchase or allocate paid compute. GLM-4.7 remains NOT VERIFIED.

## Runner, controller and authority state

- The current main controller remains the sole policy-authorized Gemini transport. The three child workflows are separate GitHub-hosted Ubuntu jobs; same-host Runner 2 co-location is not implemented by the current main source.
- The owner-directed Runner 1 / Runner 2 arrangement is represented by PR #625, not yet accepted into canonical Bootstrap/map/checkpoint. The canonical Bootstrap still contains older Claude/Alamo placement text; the proposal and newer owner terminology comments require a reviewed, explicit reconciliation. Do not treat PR #625 as deployed runner evidence.
- Runner 1 workflow source is integrated on main through PR #623, but the prior PR-event evidence explicitly skipped live Ollama installation/model pull/inference, FCC authentication smoke, Claude Code invocation and ECC live checkout. Runner 1 runtime remains **NOT RUN / NOT QUALIFIED**.
- Gemini Agents 1/2/3 remain **NOT RUN** for this pass. No controller run ID or child run/job IDs were created for this pass. Existing skipped controller workflow runs are not a dispatch.
- The active ruleset `26108066` is scoped to the default branch and requires five contexts: Astra Cloud Runtime Validation, AI Factory verification, provider contract verification, Astra Verify, and Gemini workflow contract validation (Wave 284). At main HEAD, the check-run collection has 32 entries, but the exact required-context set is not evidenced as all present/terminal-successful; combined status has 0 contexts and a queued unrelated supervisor job remains. Main exact required CI is **NOT VERIFIED**.
- No secret values were accessed. Effective secret/variable presence and scope, trusted-main no-secret probe, independent A3 controller review and Gemini controller admission remain **NOT VERIFIED**.

## Checks performed

- Ref/HEAD reads for `main` and the canonical docs branch.
- Read-back of canonical Bootstrap, map (blob read-back), continuation checkpoint, Master Roadmap and Functional Baseline 2.0.
- Issue #301 latest visible comment page read-back.
- PR metadata/diffs/file lists for #625/#628/#629/#630.
- Exact-head check-run and combined-status reads for PR #625/#628/#629/#630 and `main`.
- Formal review and inline-thread reads for PR #625/#628/#629/#630.

## Not performed

No source/runtime code changes, installs, model downloads, inference, host mutation, runner provisioning, secrets access, Gemini controller dispatch, child workflow launch, merge, deployment, qualification or product acceptance.

## Next bounded work

1. Reconcile Wave 521 (#628) with the single consolidated Wave 522 Colibri record; retain the Wave 522 resource/security constraints and avoid two competing Wave 522 index entries.
2. Establish exact-head documentation CI and obtain independent formal review before merging the documentation chain. Keep every unverified result NOT VERIFIED.
3. Resolve the owner-directed two-runner topology against the canonical Bootstrap and record actual runner identities/capacity before attempting live Runner 1 runtime or Runner 2 co-location.
4. Close controller security/governance gates and the trusted-main no-secret probe before any Gemini agent batch.
5. Keep Colibri unadmitted pending a separately approved resource/budget profile, immutable engine/model artifact provenance, security review and measured runtime tests.

## Canonical navigation

- [Canonical map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Canonical continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #625](https://github.com/VlDMlNSh/mediahub-os/pull/625), [PR #628](https://github.com/VlDMlNSh/mediahub-os/pull/628), [PR #629](https://github.com/VlDMlNSh/mediahub-os/pull/629), [PR #630](https://github.com/VlDMlNSh/mediahub-os/pull/630)
