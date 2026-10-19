# MediaHub OS Contour A — runner manifest and Gemini pool readiness (Wave 181)

- Date: 2026-10-19
- Status: source-backed readiness audit; no runner dispatch, model invocation, code execution, or qualification claimed.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Worker hardening candidate: [PR #375](https://github.com/VlDMlNSh/mediahub-os/pull/375)
- Prior governance blocker register: [Wave 180](MEDIAHUB-CONTOUR-A-GOVERNANCE-DECISION-CLOSURE-REGISTER-WAVE-180-2026-10-19.md)

## 1. Result

The repository does contain runner contracts, so it would be inaccurate to say the runner manifest is absent. However, the current evidence does not establish one accepted, end-to-end authoritative runner/workspace/network target manifest. The source files define runner identity and labels; they do not yet close the separate issuer/capability, publisher-isolation, workspace-cleanliness, network-egress, provenance, and independent-acceptance gates.

SentinelX inspection was attempted before host work. The account currently has no connected operational hosts:
- `Voktors-Mac-mini.local` (`host_5f7264034bdf0b51`) is enrolled but offline; last connected 2026-10-18 12:25 UTC.
- `mh-dev-01` (`host_58114817a6ab4dd0`) is disabled by the user in SentinelX.
- `mh-dev-02` (`host_5bda3b5006655e9e`) is disabled by the user in SentinelX.

No host command or code-writing action was executed because no host is operational. This is an execution blocker, not evidence that the machines or their files are absent.

## 2. Source-bound manifest inventory

| Source | Current main blob SHA | What it establishes | What remains unproven |
|---|---|---|---|
| `control/qualification/canonical-runner-contract.json` | `32ec7bbe371b1cfd3f2f46019ee1d2671980aa26` | Names `mh-dev-01`, label `mediahub-control`, Linux/x64, expected user `mediahub-runner`, and runtime hostname/user checks. | Live runner registration/health; workspace integrity; network policy; issuer authority; publisher isolation. |
| `control/qualification/distributed-runner-contract.json` | `993f51f07c7937165ffb3bfbe59cd0801ea71ec0` | Defines three node identities/labels and explicitly marks only `mh-dev-01` canonical; the other two are non-authoritative. | Accepted relationship to current host inventory; network and workspace contracts; fresh attestation of actual node/user/OS/architecture. |
| `tests/test_canonical_runner_contract.py` | `684c2fa2aceda89dc2e0b3d21416595b3c36d2bc` | Static tests require the unique canonical label and contract file. | The test itself does not prove the runner is online, securely admitted, isolated, or able to publish safely. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Uses dedicated self-hosted labels and runtime hostname/user checks; checks local executables/model availability. | The workflow still declares `contents: write`, uses checkout credentials, and calls a worker path that directly stages/commits/pushes. It is not evidence of an isolated trusted-publisher boundary. |

The exact source refs above are `main` at observed repository tree SHA `c06015e0b1526e0aaa6a522306052b077455aba5`. The canonical documentation branch is separate: `docs/mediahub-chat-tree-map-20261012`.

## 3. Manifest acceptance gaps

Before the manifest can be accepted as the operational target contract, one reviewed version needs to bind, at minimum:

1. **Identity/admission:** node ID, stable host identity, runner label, OS/architecture, user, authority class, and fresh runtime attestation.
2. **Workspace:** immutable base SHA, permitted checkout roots, clean reconstruction rules, forbidden inherited hooks/remotes/credentials, bounded artifact/result paths, and cleanup behavior.
3. **Network:** explicit egress allowlist by purpose, DNS/proxy assumptions, denied inbound listeners, provider/data-route classification, and evidence for enforcement. Do not assume a fixed GitHub-hosted egress IP.
4. **Execution authority:** issuer/verifier contract, capability scope, command/task digest, audience/node, target SHA, expiry/revocation/replay behavior, and separation from Product State Authority.
5. **Publication:** isolated trusted publisher, bounded patch/result bundle, path/symlink/size checks, least-privilege short-lived credential, remote-SHA verification, and durable correlated audit.
6. **Supply chain:** full commit-SHA action pins, dependency provenance, reproducible tool versions, and explicit handling of mutable action/container tags.
7. **Acceptance:** owner/governance decision for open GOV-CAP-01…07 and R-06/MH-12; independent review and a frozen-SHA evidence bundle.

Until these are accepted and verified, fail closed: no self-hosted worker dispatch, no publication authority promotion, and no Contour A qualification claim.

## 4. Three parallel Gemini assignments prepared — not dispatched

The repository has three manual-dispatch engineering workflows on `main` at the observed tree SHA:
- [Gemini Autonomous Engineering](https://github.com/VlDMlNSh/mediahub-os/actions/workflows/gemini-autonomous-engineering.yml) — primary bounded implementation/documentation agent, using `GEMINI_API_KEY`.
- [Gemini Agent 2 — Research and Architecture](https://github.com/VlDMlNSh/mediahub-os/actions/workflows/gemini-agent-2.yml) — independent manifest/component research, using `GEMINI_API_KEY_2`.
- [Gemini Agent 3 — Security and Verification Review](https://github.com/VlDMlNSh/mediahub-os/actions/workflows/gemini-agent-3.yml) — independent threat-model/verification review, using `GEMINI_API_KEY_3`.

These workflows are manual, per-run jobs, not persistent agents. This session's available tools do not expose GitHub workflow-dispatch, and no Gemini invocation was made. The tasks below are ready for manual dispatch by the owner. Each must create its own branch and PR; none may merge or deploy.

### Agent 1 — bounded implementation/evidence task

`W181-A1`: On a dedicated branch from main, implement only a source-backed validator for the existing runner contracts if a clear gap can be fixed without choosing governance policy. Validate required fields, unique node IDs/labels, authority enum, and consistency between canonical and distributed contracts. Add negative fixtures for missing/duplicate node identity, conflicting labels, malformed OS/architecture, and accidental promotion of a non-authoritative node. Do not invent network allowlists, issuer semantics, key storage, or authority decisions. Run only the targeted local tests available in the workflow; report exact commands/results and open a draft PR. If contract semantics are ambiguous, produce a blocker checkpoint instead of changing behavior.

Acceptance: minimal diff; deterministic tests; no secret/credential access; no workflow dispatch; no merge/deploy; evidence references exact paths and SHAs.

### Agent 2 — independent research/architecture task

`W181-A2`: Independently crosswalk `canonical-runner-contract.json`, `distributed-runner-contract.json`, the worker workflow, and Issue #301 against the accepted Baseline 2.0 and current governance matrix. Determine whether an authoritative runner/workspace/network manifest exists elsewhere and distinguish documented policy from runtime proof. Search existing stable GitHub components before proposing new code. Produce a concise evidence table of source refs/SHAs, conflicts, license/provenance where relevant, and the smallest set of decisions needed for acceptance. Do not edit production contracts, call providers, dispatch workers, or merge.

Acceptance: source-linked report and one PR; no unsupported claims of host health or qualification.

### Agent 3 — independent security/verification task

`W181-A3`: Review the runner/workspace/network and publisher path adversarially. Focus on self-hosted runner labels as routing rather than authorization, inherited checkout credentials, `contents: write`, worker-side git push, workspace contamination, symlink/path traversal, untrusted task JSON, egress/data leakage, action/container pinning, cancellation/replay, and audit correlation. Map findings to the Wave 179 negative-test matrix and GOV-CAP-01…07/R-06/MH-12. Return severity, exploit preconditions, source lines/SHAs, and fail-closed acceptance criteria. Review only; do not alter secrets, execute workers, publish code, or merge.

Acceptance: independent findings and test recommendations with exact evidence; separate facts from hypotheses.

## 5. Gemini operating rule for continued /next work

Use the three agents as **parallel, independent workstreams**, not as an unbounded shared write session:
- Agent 1 proposes a minimal implementation or targeted tests.
- Agent 2 independently verifies source truth and existing-component reuse.
- Agent 3 reviews security boundaries and negative cases.
- The coordinating pass reconciles the outputs against the current canonical map, Baseline 2.0, Issue #301, branch heads, and CI. No PR is merged merely because an agent reports success.
- Re-dispatch each agent only with a new bounded task and fresh source refs. These workflows do not stay running after a job ends; persistent scheduling would require a separately approved queue/orchestrator and must not be implied by manual workflow availability.

## 6. Verification and boundaries

- Read-back completed for the two runner-contract JSON files, runner contract test, worker workflow, and Gemini workflow definitions from `main`.
- Static test source was inspected; **the test was not run in this pass**.
- SentinelX capabilities request returned `agent_offline`; host inventory independently showed zero connected hosts and one offline/two user-disabled enrollments.
- No Gemini workflow was dispatched; no model/provider call, host command, code mutation, credential read, merge, deployment, or qualification occurred.
- ASTRA GOLD gates G0–G11 remain BLOCKED in `docs/qualification/CURRENT-TRUTH.generated.md` (main blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`).

## 7. Next step

First manually dispatch Agent 2 with `W181-A2` and Agent 3 with `W181-A3` in separate runs; their read-only reports can proceed while SentinelX hosts are offline. Dispatch Agent 1 only after the crosswalk confirms the validator's expected contract semantics. In parallel, restore SentinelX host availability in the dashboard/on the machines, then re-check capabilities and live node identity before any worker execution. Keep PR #375 Draft and unmerged until the publisher and issuer blockers are independently closed.
