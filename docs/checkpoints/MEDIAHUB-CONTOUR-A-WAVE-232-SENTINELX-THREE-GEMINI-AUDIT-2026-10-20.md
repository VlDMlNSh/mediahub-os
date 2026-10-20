# MediaHub Contour A — Wave 232: SentinelX clean-room review and three-agent audit

- Date: 2026-10-20
- Status: **EVIDENCE REVIEW / PROPOSALS ONLY / NOT QUALIFIED**
- Working documentation branch: `work/contour-a-wave216-continuous-qualification-2026-10-20`
- Main SHA observed: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md

## 1. Owner target invariant

All current/legacy servers, local checkouts, credentials, runner registrations, manually installed tools and host-specific configuration are temporary and disposable. They are not the future runtime foundation. The future Contour A must be rebuilt from versioned source of truth with fresh identities and credentials, reproducible artifacts, ephemeral GitHub-hosted execution by default, bounded model/provider routes and egress, artifact-only worker outputs, a separately authorized publisher, auditable provenance, clean install/update/rollback/recovery and a decommission gate.

This is a target invariant, not permission to perform billable provisioning, production deployment, or destructive teardown. Old servers may only be decommissioned after the new clean system is deployed, independently accepted, and demonstrated recoverable with evidence preserved.

## 2. Third-host / GitHub dispatch status

SentinelX host `host_5f7264034bdf0b51` (`Voktors-Mac-mini.local`, macOS 14.7.4 arm64, agent 0.22.0) is online and GitHub CLI is authenticated. Only one SentinelX operational host slot is available on the current Free plan. `mh-dev-01` (`host_58114817a6ab4dd0`) and `mh-dev-02` (`host_5bda3b5006655e9e`) are disabled in SentinelX; GitHub self-hosted runner inventory reports both offline. `Voktors-Mini-Astra-Control` is the only online self-hosted runner, but it is not target infrastructure. The three Gemini workflows actually ran on GitHub-hosted `ubuntu-latest`, not on the Mac self-hosted runner.

The three runs already existed at the first live state check. This pass verified and reused them instead of sending duplicate dispatches:
- A1 run [39370191589](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370191589) produced Draft PR [#403](https://github.com/VlDMlNSh/mediahub-os/pull/403), head `7a939d8805d12b2b56d4c0edabcd63c15b4f3c9a`, report blob `1e59ecb5a37a64bc98d55af1978685858c5b65b3`.
- A2 run [39370202615](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370202615) produced Draft PR [#401](https://github.com/VlDMlNSh/mediahub-os/pull/401), head `0d492cd8998ed60be9b6cef2ad40d3e168907aba`, report blob `b1cfb1e0730f8f94b8f1b4cf29aaa0fd78f89a91`.
- A3 run [39370217605](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370217605) produced Draft PR [#402](https://github.com/VlDMlNSh/mediahub-os/pull/402), head `ccb26d0b65042e3b9d1d87604dc3223cb2a7f9bb`, report blob `ee6688c08135521efa48f33a32ddb730334ba407`.

All three workflows completed successfully, but that says the workflow job completed; it does not prove the report's architectural claims. Exact-head PR checks are `ACTION_REQUIRED`, not PASS:
- #401: Astra Verify `39370284376`; Cloud Runtime `39370284372`.
- #402: Cloud Runtime `39370303319`; Astra Verify `39370303391`.
- #403: Astra Verify `39370356797`; Cloud Runtime `39370356910`.

Correction comments are posted: #401 comment `6283500588`; #402 comment `6283499784`; #403 comment `6283499004`. Keep all three Draft pending truthful revisions and ordinary CI/governance resolution.

## 3. Independent execution-path audit

Primary source reads are bound to main SHA `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`:
- `ops/control/sign_command.py`, blob `fc6943a79cefdf06e59d6e32771d2df551b2f0e9`: signer only. Proposed `verify_signed_command()` exists in unmerged PR #400 and is not called by the distributed local worker.
- `ops/qualification/run_distributed_local_worker.py`, blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`: `load_task()` at line 64 parses `ASTRA_MICRO_TASK_JSON` and checks seven task fields; no HMAC/signature, issuer/capability, revocation/replay or command-task binding is enforced there. Direct git push appears at line 668.
- `.github/workflows/astra-distributed-local-worker.yml`, blob `f650f2416c19dc75b4a0eeec037661c0c6169910`: grants top-level `contents: write`, uses `persist-credentials: true`, and invokes that local worker path.
- `astra_github_agent.py`, blob `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`: the distinct transport worker does verify HMAC/freshness/node/path/target/idempotency, but its own `publish()` also stages/commits and directly pushes to `astra-node/{NODE_ID}`. A per-node branch is not a separately authorized publisher. Setting `secret_values="SUPPRESSED"` is not comprehensive redaction evidence.
- `ops/mesh/admission.py`, blob `46e92d3c4f9b9865356443403e9ebd34587996cd`: checks supplied node/capability/policy structures (active status, capability schema, EXECUTION authority, qualification); it does not authenticate an issuer signature or bind the distributed worker's task to the exact admitted operation/resource.

Thus A1/A3 conflated the two worker paths and overstated “artifact-only publisher” / “implemented and tested” end-to-end assurance. The issuer-to-worker composition, capability revocation/lifecycle, global replay prevention, redaction proof, removal of worker publication credentials and separately authorized publisher remain **OPEN / NOT PROVEN**. PR #400's verifier remains disconnected from production execution. Direct worker Git write/push remains a SEV-1 blocker.

## 4. A2 component research quality

PR #401 identifies candidate primitives: Cosign, Syft, Trivy, SOPS + age, and Harbor. These remain candidates, not approved deployment decisions. Current report does not provide exact upstream release tags/commit SHAs, license-file blob identities, retrieval timestamps or reproducible maintenance evidence for each. It also grouped MPL-2.0 as “permissive”; MPL-2.0 is weak copyleft and should not be presented as equivalent to Apache-2.0/BSD. Review requested a pinned provenance/license crosswalk and practical comparison of OCI registry versus GitHub Actions artifacts + a trusted publisher. No new dependency was installed.

## 5. Governance and exact-head status

GitHub branch-protection endpoint for `main` returns `404 Branch not protected`; repository ruleset list is empty. This is an unresolved integration gate. Do not merge based on green CI alone.

Draft PR #404 — [clean-room rebuild contract](https://github.com/VlDMlNSh/mediahub-os/pull/404), head `80b290206d4e6d40f2ff076a389cfb9f477d2f3b`, report blob `99263efa13b3cf5fe9c0177ca78617ad61614781` — is a design proposal only. Exact-head Astra Verify run `39370493729` and Cloud Runtime Validation `39370493773` are SUCCESS. No cloud resources were provisioned, no production/worker command was dispatched in this pass, no secret values were read or changed, and no host was destroyed.

## 6. Documentation update and verification

Updated the existing working documentation PR #396 branch, not the canonical docs branch:
- commit `32f2117550520e2383a77a2969fe089515b71809` (`docs(contour-a): reconcile Wave 232 agent evidence`);
- map blob `024ed13a2915ff6055487204d227a166f8bd9cb9`;
- checkpoint blob `d49c385b76772182c7e1b493ee212578ee8733be`.
The checkpoint was read back by Contents API with full content; the 1.1 MB map was re-read through blob API after the path Contents read returned an empty body. SentinelX reports the working tree clean, tracking the remote at the new commit. `git diff --check` passed.

This docs branch is still **Draft / non-canonical**. Live comparison shows it DIVERGED from main, 2,561 commits ahead / 33 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. Do not merge or rebase blindly just to refresh the map.

## 7. Next gates

1. Keep PRs #401–#403 Draft until evidence and worker/publisher claims are corrected; resolve `ACTION_REQUIRED` checks through normal review, not bypass.
2. Keep PR #404 design-only pending independent architecture acceptance.
3. Set up explicit main branch-protection/ruleset policy before integration.
4. Implement and test issuer/capability/key lifecycle/revocation/replay, command-to-task binding, artifact-only worker outputs and a separately authorized publisher with no worker write credentials.
5. Define provider and budget gates before billable resources.
6. Perform clean install, recovery and independent G0–G11 qualification before decommissioning old servers.

Contour A remains **NOT_PROVEN / BLOCKED**; G0–G11 remain blocked, G11 human-only, and Contour B remains gated.
