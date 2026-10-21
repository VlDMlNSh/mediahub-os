# Wave 309 — Controller exact-head status and non-launching evidence (2026-10-21)

Status: **VERIFIED PARTIAL EVIDENCE; AGENT DISPATCH BLOCKED**  
Working PR: [#430](https://github.com/VlDMlNSh/mediahub-os/pull/430)  
Controller governance PR: [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421)  
Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)  
Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Immutable targets inspected

- Documentation working PR #430 head: `2f90c362b88eea07ab3d2f5648143a7115ad40d5`; base `docs/mediahub-chat-tree-map-20261012` at `48fbe986263ec1a93edefecedeac8ec4509094f8`. PR remains OPEN/DRAFT and reports mergeable=false.
- Controller PR #421 head: `185f55b63121b1aece7e60f6c087ecfceab2721e`; base `main` at `80be45a70732b1d568164571d4273a6397792c3b`. PR remains OPEN/DRAFT/UNMERGED; no submitted formal reviews are returned.
- Controller workflow on `main`: blob SHA `99e5a87825aeb239568f96ecef004a102ff3e53b`. It still uses the REST-dispatch/monitoring path and `secrets.MEDIAHUB_GITHUB_TOKEN`; that path remains ON HOLD.
- Candidate reusable child `.github/workflows/gemini-agent-2.yml` on `contour-a/workflow-call-controller-governance-wave243`: blob SHA `9fced7999c0ab5a5a8b9666fd92791726b64fc66`. Its visible guard compares event name and `GITHUB_WORKFLOW_REF` to the exact `...controller.yml@refs/heads/main` string, and the engineering job repeats an exact-ref condition.
- Candidate Wave 292 contract test `tests/test_gemini_controller_positive_context_probe_wave292_contract.py`: blob SHA `e1a229cbfb134d3548df727eab4f644dc221a51f`. This source was inspected statically; no local execution was performed in this pass.

## Current CI / run evidence

For controller PR head `185f55b63121b1aece7e60f6c087ecfceab2721e`, GitHub returned these associated runs:

- Controller-only batch run [39475766513](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766513): overall success. Job `118811194691` no-secret caller-context probe succeeded; job `118811238489` assertion succeeded. Gemini Agent 1 job `118811256463`, Agent 2 job `118811196891`, Agent 3 job `118811196072`, and batch summary job `118811197050` were **skipped**. No artifacts were returned.
- Non-launching caller-context probe run [39475766469](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766469): both jobs succeeded; no artifacts were returned.
- Contract-validation run [39475766192](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766192): validation job succeeded.

These results prove successful non-launching probe/validation jobs only. They do not prove Gemini execution, independent approval, qualification, or acceptance. The successful older run mentioned in PR comments for commit `436c6d386289c77538382f76d7d6102aaa28acbb` is not substituted for current-head evidence.

## Per-lane disposition

| Lane | State | Evidence / blocker |
|---|---|---|
| Gemini Agent 1 | NOT RUN | Controller job skipped; no child run ID or artifact |
| Gemini Agent 2 | NOT RUN | Controller job skipped; no child run ID or artifact |
| Gemini Agent 3 | NOT RUN | Controller job skipped; no child run ID or artifact |
| Alamo Claude Code | NOT RUN | Designated Alamo/server 3 and approved non-paid route not positively identified |
| Browser via SentinelX + agent-browser | NOT RUN | Only active host is `host_5f7264034bdf0b51` (`Voktors-Mini.Dlink`); identity as Alamo/server 3 and browser availability not proven. Two other hosts are disabled. |
| Controller launch | BLOCKED | PR #421 is Draft/unmerged; formal independent review and governed integration gates remain open |

## Governance and security interpretation

- The current main controller remains the legacy REST dispatch route; do not invoke it.
- PR #421 is an implementation proposal, not authority to launch agents. Its recent successful probe jobs intentionally skipped all three Gemini jobs.
- Static child source currently contains an exact main-ref comparison, but this is not a substitute for independent verification of actual reusable-workflow caller-context semantics, bypass resistance, effective permissions, secret flow, immutable third-party action pins, and a negative caller-context test.
- Issue #301 remains OPEN and says CAF-Q-001…CAF-Q-015 is documentary, not a live scheduler. No credential values were accessed, no provider was called, no Gemini/Claude task or browser session was launched, no host was mutated, and no merge/deployment/qualification/acceptance occurred.
- Bootstrap/map/checkpoint documentation changes remain on the working documentation branch. The canonical map itself was not modified.

## Next bounded step

Keep agent execution fail-closed. Reconcile PR #421's current exact head with its probe and negative-caller tests; obtain independent review from an identity other than the PR author; verify immutable action/container provenance and exact-head CI; only then consider governed integration. In parallel, positively identify Alamo/server 3 and verify the non-paid Claude route without changing host state.

## Evidence classification

- Controller probe/contract validation: **SUCCEEDED** for the listed jobs.
- Agent dispatch: **NOT RUN**.
- Independent controller security approval: **NOT VERIFIED**.
- Contour A qualification/acceptance: **NOT QUALIFIED / NOT ACCEPTED**.
