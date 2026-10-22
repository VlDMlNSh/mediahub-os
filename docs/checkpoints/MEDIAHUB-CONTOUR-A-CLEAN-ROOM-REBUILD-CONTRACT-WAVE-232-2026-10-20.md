# MediaHub OS Contour A — clean-room rebuild contract (Wave 232)

- Date: 2026-10-20
- Status: **PROPOSAL / NOT ACCEPTED / NOT DEPLOYED**
- Base: `main` at `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`
- Work branch: `work/contour-a-clean-room-blueprint-wave232`
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Wave 231 verifier proposal: https://github.com/VlDMlNSh/mediahub-os/pull/400

## 1. Decision framing

The current developer servers and the connected SentinelX host are temporary engineering access paths, not the target runtime. The eventual Contour A system must be provisioned from a clean, versioned source of truth with new identities, new credentials, reproducible artifacts and independently verifiable evidence. It must not require a surviving legacy host, a pre-existing local checkout, a hand-edited machine, or a persistent self-hosted runner to bootstrap.

This document does **not** authorize a cloud purchase, a production deployment, a destructive teardown, or a change to accepted baselines. It specifies the target contract and evidence needed before those actions. Existing servers are retained only as temporary, explicitly non-production bridges until the new target passes independent acceptance and a separate decommission checklist is satisfied.

## 2. Source-bound facts

| Claim | Source / ref | SHA | Status / limit |
|---|---|---|---|
| Current accepted functional reference is Baseline 2.0; implementation is not inferred from design | `docs/checkpoints/mediahub-functional-baseline-2.0.md` @ `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Accepted, canonical, immutable |
| Distributed developer-fabric topology is accepted as a target, not runtime-qualified | `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` @ `main` | `e549692f207fbc91d9b9b9b92b8e665404f07290` | Target architecture only; clean-room reset needs explicit mapping |
| Trust chain requires authenticated principal, workload identity, capability/policy evaluation and authorized command | `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` @ `main` | `8d831c2a8fa333977dd86524099568bae2a8db0e` | Proposed architectural baseline; issuer lifecycle still unresolved |
| Component choices require version pinning, security/provenance review and acceptance tests | `components/COMPONENT-REGISTRY.yaml` @ `main` | `3ad109ba5ec9b095d0fac851514caadcefbe2f69` | Registry baseline; selected components are not thereby deployed |
| Component ownership stays with MediaHub; OSS blocks do not become state/authority owners | `architecture/COMPONENT-ARCHITECTURE-DECISIONS.md` @ `main` | `42b2701f0d6a1014435e96118e41e33025dbff08` | Accepted component-selection baseline |
| MH-15 host, OS, trust, resource, recovery and evidence gates remain unaccepted | `docs/architecture/MH-15-acceptance-criteria.md` @ `main` | `082642e67dc66cb359a5566773c143854cafaa00` | Not accepted |
| MH-16 installer/update/recovery architecture remains proposed and implementation-not-authorized | `docs/architecture/MH-16-installer-recovery-update-architecture.md` @ `main` | `f3ad2401f00a4062b39eed640e0c5c5f70064312` | Governance acceptance pending |
| Existing distributed worker still parses task JSON without execution-side signature/issuer/capability verification and can publish directly | `ops/qualification/run_distributed_local_worker.py` @ `main`; `.github/workflows/astra-distributed-local-worker.yml` @ `main` | `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`; `f650f2416c19dc75b4a0eeec037661c0c6169910` | Current blocker, not a target design |

The documentation branch `docs/mediahub-chat-tree-map-20261012` is currently **DIVERGED** from main: compare reports 2,533 commits ahead and 33 behind. Do not merge/rebase it as part of this blueprint. The canonical map Contents wrapper returned an empty body with blob SHA `2187b4ca50792fe073f0979442c0f73432a2f6f9`; the same blob was retrieved through the blob API and contains 1,094,624 bytes. Its recorded latest increment remains Wave 206, so documentation reconciliation remains open.

## 3. Target clean-room topology

1. **Source of truth:** protected GitHub repository refs, accepted Baseline 2.0, versioned architecture/contract documents, and traceable governance decisions. A server-local checkout is never authoritative.
2. **Control plane:** Jarvis coordinates organization-level engineering missions; ASTRA A0 owns only ASTRA-internal queue/claim/gate state. Neither becomes MediaHub Product State Authority. GitHub Actions may execute engineering jobs but cannot become product-state authority.
3. **Default execution:** ephemeral GitHub-hosted runners for CI, research and bounded agent tasks. Self-hosted execution is optional and separately gated; it is not required to install, recover or qualify the initial clean system.
4. **Worker boundary:** each worker receives an immutable base SHA, a narrowly scoped task, read-only source credentials where possible, and no ambient repository-write credential. Model output, patch, logs and manifests are quarantined artifacts.
5. **Trusted publication boundary:** a separate publisher reconstructs the candidate from the immutable base, validates issuer/capability and policy context, checks changed paths and diff semantics, recomputes hashes, verifies attestation/signature, enforces freshness/replay/revocation policy, then uses a narrowly scoped short-lived write grant. It records exact base/head/blob SHAs and verifies the remote result. Workers never push directly.
6. **Model routing:** explicit provider/model registry, policy-driven route decision, privacy/data-egress classification, quota/error accounting and fail-closed behavior. Local-only mode never silently falls back to cloud. Provider credentials are injected only into the smallest required step and never into untrusted worker/model environments.
7. **Secrets:** use the selected SOPS + age primitives for encrypted configuration and versioned secret references. Runtime plaintext is short-lived, scoped and excluded from logs, artifacts and source. Credential rotation/revocation and disaster recovery require evidence.
8. **Infrastructure:** deployment definitions, runner images, action versions, toolchains, schemas, SBOM and policy are versioned and pinned. The new target receives fresh identities and trust roots; no legacy server's host key, runner registration, filesystem, secret store or hidden local configuration is imported.
9. **Observability/evidence:** non-authoritative telemetry plus signed, immutable job/result manifests. Evidence records identity, workflow/run, input refs, base SHA, toolchain/action digests, outputs and verification status. Telemetry never authorizes mutation.
10. **Recovery:** clean bootstrap, update, rollback, restore and credential-rotation procedures are tested on a disposable environment before acceptance. A successful backup command alone is insufficient; restore must be exercised and verified.

## 4. Clean-room deployment sequence

| Stage | Required output | Exit evidence | No-go condition |
|---|---|---|---|
| A — contract freeze candidate | source register, requirement crosswalk, authority/identity decisions | every requirement points to source and owner; unresolved items are explicit | missing issuer/capability contract or baseline conflict |
| B — reproducible build | pinned runner/toolchain/container definitions, SBOM and provenance | two clean builds have comparable, explained outputs; all action refs are pinned | mutable/unpinned dependency or untracked local state |
| C — isolated execution | ephemeral worker with bounded workspace, network and filesystem | negative tests prove no write token, secret leakage or out-of-scope mutation | worker can publish or read unrelated credentials |
| D — trusted result publication | artifact-only worker and independent publisher | signed manifest, diff/path checks, exact base binding, replay/revocation tests, remote SHA readback | direct worker push or caller-controlled authority inputs |
| E — model routing | explicit provider policies and quota/error behavior | tests prove privacy modes, no silent fallback, budget limits and credential isolation | unknown route defaults to broader egress |
| F — lifecycle and recovery | clean install, update, rollback, restore and key rotation | disposable-environment drills with logs and evidence | recovery depends on a legacy host or undocumented manual state |
| G — independent qualification | complete G0–G11 evidence bundle and independent review | each gate has its required evidence and authorized disposition | self-review used as independent acceptance |
| H — decommission legacy | signed inventory, preserved evidence, recovery confirmation, credential revocation | new system is accepted and independently recoverable; old identities revoked | new system not accepted, evidence not preserved, or rollback path unproven |

These are proposed sequencing stages, not replacements for the repository's existing G0–G11 gates. G11 remains human-only. Contour B remains blocked until Contour A has been deployed and independently accepted.

## 5. Immediate implementation backlog

1. Close the issuer/capability/key-lifecycle/replay contract before wiring the Wave 231 verifier into any executor.
2. Replace direct worker publication with quarantined artifacts and a separately authorized publisher; no worker write credentials.
3. Add a clean-room CI qualification job using ephemeral GitHub-hosted runners and no dependency on self-hosted runner labels.
4. Add policy tests for immutable base binding, allowed path sets, symlinks/path traversal, diff reconstruction, artifact tampering, stale/revoked credentials, replay, cancellation and publisher failure.
5. Pin all actions and toolchains to reviewed immutable versions; record provenance and SBOM.
6. Define the provider/compute deployment target and budget before provisioning billable resources. Do not infer an approved provider or cost ceiling from current server connectivity.
7. Accept MH-15/MH-16 lifecycle and recovery contracts before production provisioning or destructive cleanup.
8. Execute a clean install and independent recovery drill, then qualify G0–G11. Only after that, execute the legacy-server decommission plan.

## 6. Current-wave execution record

Three Gemini GitHub Actions workflows were dispatched from `main` SHA `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4` with independent bounded scopes:
- A1 architecture/issuer/capability: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370191589
- A2 OSS/clean-room architecture research: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370202615
- A3 independent security review: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370217605

Final status read: all three runs completed `success` and created Draft PRs #401–#403; independent read-back findings and unresolved claims are recorded in §8 below. Their results are unverified proposals until artifact, tool success, branch/PR, refs and evidence are read back. The dispatches do not prove the three agents are always-on; they are finite GitHub Actions runs.

## 7. Scope and non-claims

- This is architecture/design work only. No cloud resource was created, no current server was repurposed as production, no existing server was destroyed, no secret value was read, and no production worker was dispatched.
- No test or qualification result is claimed for this document. Only GitHub metadata/source reads and workflow dispatch/status checks were performed.
- The clean-room topology is a proposal and is **not accepted, implemented, qualified, deployed or production-authorized**.
- Contour A remains **NOT_PROVEN / BLOCKED**; G0–G11 remain blocked; G11 is human-only.


## 8. Independent read-back of Wave 232 Gemini results

All three runs finished successfully, but the artifacts contain tool failures and the reports are not accepted as authoritative.

- **A1 / PR #403** — report blob `1e59ecb5a37a64bc98d55af1978685858c5b65b3`. Run output records 11 successful and 4 failed tool calls, including an unsupported `update_topic` call, initial PR tool schema error, and a Gemini free-tier input-token quota error. More importantly, its “separately authorized publisher verified” and “fully implemented and tested” assertions are overstated: `astra_github_agent.py` blob `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` pushes from the worker process to `astra-node/{NODE_ID}`; `ops/qualification/run_distributed_local_worker.py` blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1` is another direct-push worker path. The workflow blob `f650f2416c19dc75b4a0eeec037661c0c6169910` still grants `contents: write` and sets `persist-credentials: true`. No evidence shows that the standalone `ops/mesh/admission.py::admit_executor()` result is composed into the `astra_github_agent.py` command execution path.
- **A2 / PR #401** — report blob `b1cfb1e0730f8f94b8f1b4cf29aaa0fd78f89a91`. The shortlist (Cosign, Syft, Trivy, SOPS, age) aligns with existing component references, but the report lacks pinned upstream tags/commit SHAs and dated release evidence needed to reproduce its maintenance/license claims. Harbor is not an accepted component merely because the agent suggests it; keep it reference-only/future-gated until a separate decision and qualification.
- **A3 / PR #402** — report blob `ee6688c08135521efa48f33a32ddb730334ba407`. It identifies direct push and replay/key lifecycle concerns, but its conclusion “publisher separation validated as artifact-only” contradicts the direct worker push code. The claim that result/telemetry secrets are automatically scrubbed also needs a source-bound sanitizer path and negative tests; it is not accepted from the report alone.
- Independent review comments were added to PR #403 (comment `6283536354`), PR #402 (`6283537187`) and PR #401 (`6283538001`). All three PRs remain Draft/unmerged. No runtime code, secret, worker, infrastructure or acceptance gate was changed by the agent runs.
- PR #404 exact-head CI on `80b290206d4e6d40f2ff076a389cfb9f477d2f3b`: Astra Verify run `39370493729` SUCCESS; Astra Cloud Runtime Validation run `39370493773` SUCCESS. These verify existing repository checks on the proposal branch; they do not qualify the proposed clean-room architecture.

Disposition: preserve all three agent PRs as unaccepted research proposals until the corrections are made and the exact source claims are re-verified. Contour A remains `NOT_PROVEN / BLOCKED`; G0–G11 blocked, G11 human-only.


## 9. Exact-head CI status of agent PRs (2026-10-20)

GitHub run read-back confirms that the agent dispatch runs and their PR CI are different signals:

- A2 PR #401 head `0d492cd8998ed60be9b6cef2ad40d3e168907aba`: [Astra Verify 39370284376](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370284376) and [Cloud Runtime 39370284372](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370284372) both completed with conclusion `action_required`; no jobs were returned.
- A3 PR #402 head `ccb26d0b65042e3b9d1d87604dc3223cb2a7f9bb`: [Cloud Runtime 39370303319](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370303319) and [Astra Verify 39370303391](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370303391) both `action_required`; no jobs were returned.
- A1 PR #403 head `7a939d8805d12b2b56d4c0edabcd63c15b4f3c9a`: [Astra Verify 39370356797](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370356797) and [Cloud Runtime 39370356910](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370356910) both `action_required`; no jobs were returned.

Therefore the three Gemini workflow runs passed their own output validator, but the resulting PRs have **no successful exact-head CI evidence** at this read-back. Keep all three Draft/unmerged. Do not confuse these `action_required` checks with test failures or passes; the returned evidence shows that the jobs did not run/are gated.
