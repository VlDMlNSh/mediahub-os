# Wave 308 — mandatory per-/next multi-agent, Alamo Claude and browser evidence contract

Date: 2026-10-21  
Status: DOCUMENTATION UPDATED ON WORKING BRANCH; RUNTIME ORCHESTRATION NOT YET QUALIFIED  
Working PR: [#430](https://github.com/VlDMlNSh/mediahub-os/pull/430)  
Controller governance PR: [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421)  
Governing queue: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)  
Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Objective

Make every `/next` attempt a coordinated, auditable multi-executor pass, including the first `/next` in a new chat: three independent Gemini tasks through the approved GitHub Actions controller, one bounded local Claude Code task on Alamo/server 3 through an independently verified non-paid route, and browser inspection via SentinelX plus the agent-browser plugin when web UI state is needed. Require per-lane run evidence and report verification on every pass.

## Changes recorded

1. Updated [Bootstrap instruction](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), adding §1D, a binding per-`/next` orchestration and evidence contract:
   - Gemini 1: research/implementation proposal.
   - Gemini 2: independent contract/test verification.
   - Gemini 3: independent security/governance verification.
   - Claude Code: local-only Alamo lane, strict non-paid auth/billing/fallback verification.
   - Browser lane: SentinelX host identity/capability checks + agent-browser installed-version workflow, with browser evidence and secret hygiene.
   - Required shared immutable task packet, exact run/job/session IDs, artifacts/digests, terminal states, independent read-back and explicit NOT RUN/INCOMPLETE/FAIL outcomes.
2. Corrected the contradictory sentence in §1B so it agrees with §1C: after approved controller integration and gate verification, routine per-`/next` runs do not need a separate owner prompt; controller confirmation and all security/governance gates remain.
3. Added this report and a map addendum. The canonical map itself is intentionally not overwritten from the divergent working branch.
4. No workflow was dispatched, no provider key was read, no Claude task was launched, no browser session was opened, and no server was mutated in this pass.

## Current blockers verified during this pass

- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421) is OPEN / DRAFT / UNMERGED at head `185f55b63121b1aece7e60f6c087ecfceab2721e`. Its body records the controller-only reusable-workflow design as implementation-only pending independent review and governance evidence. The existing design is a manual controller with explicit `mode=agents` and `confirm=yes`; documentation cannot cause it to auto-dispatch by itself.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) explicitly states CAF-Q-001…CAF-Q-015 is documentary, not a live scheduler, and does not itself authorize dispatch or credential use.
- SentinelX host inventory returned one operational host, `host_5f7264034bdf0b51` (`Voktors-Mini.Dlink`, macOS 14.7.4 arm64), and two disabled hosts `mh-dev-01` and `mh-dev-02`. No connected host was positively identified as the designated third server/Alamo in this pass. The account has one active-host slot. Thus this pass cannot claim third-server browser or Claude execution capability.
- The installed agent-browser skill describes the required CLI discovery step `agent-browser skills get core`, but this pass did not find or execute that CLI on the designated third server.
- The Bootstrap change is on the working branch/PR #430, not yet canonical. Project-level ChatGPT instructions are not edited by a repository commit.

## Required per-/next evidence schema

For each Gemini role and the Alamo Claude lane, record:
- role and task ID; immutable source SHA and allowed scope;
- controller run ID and child job/run ID, or Claude host/session/job ID;
- start/end timestamps and terminal status;
- exact commands/tool versions and tests;
- report/artifact URI and SHA-256/blob SHA;
- changed paths and source blob SHAs;
- independent read-back and exact-head CI result;
- budget/auth/billing route status, without secret values;
- blockers, rollback and next step.

The browser lane additionally records the exact SentinelX host ID, browser runtime/version, URL, session/run ID, timestamp and screenshot/accessibility-snapshot evidence. Never record cookies, access tokens, PATs, provider keys or other secret values.

## Status semantics

- `PLANNED`: task packet exists.
- `DISPATCHED`: an actual controller/task invocation is evidenced by a returned ID.
- `RUNNING`: a live status says running.
- `SUCCEEDED`: terminal success from the executor.
- `VERIFIED`: lead has read back evidence and checked exact SHA/tests.
- `QUALIFIED`: all qualification criteria passed.
- `ACCEPTED`: the authorized acceptance authority recorded acceptance.

A file in GitHub or a successful dispatch is not proof of runtime execution, qualification or acceptance. Missing/timeout/stale-SHA evidence must be recorded as NOT RUN, INCOMPLETE or FAIL, never silently green.

## Evidence and hashes

- Working branch: `docs/contour-a-wave302-exact-head-gate-audit-20261021`.
- Working PR #430 HEAD before this Wave 308 update: `da03860666600a23d1feb0949c93b552f10ec39e`.
- Bootstrap source blob read before update: `e21423ac619fdc9ef4381cca40b0e3675277c42c`.
- Bootstrap update commit: `cd737e15688255f52b8a3ee85449cbbd96457731`.
- Bootstrap new blob SHA: `e3f2c9a868bf53bd246852f7c14db7bac5b08f81`.
- Controller PR #421 head observed: `185f55b63121b1aece7e60f6c087ecfceab2721e`.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Disposition

Documentation specifies a mandatory per-`/next` orchestration attempt and evidence review. Operational state remains BLOCKED / NOT_PROVEN until the approved controller gates are closed and integrated, the third server is positively identified and operational, the local Claude route is proven non-paid and compliant, and each actual run produces independently verified evidence. Continue non-agent engineering while these gates are open.
