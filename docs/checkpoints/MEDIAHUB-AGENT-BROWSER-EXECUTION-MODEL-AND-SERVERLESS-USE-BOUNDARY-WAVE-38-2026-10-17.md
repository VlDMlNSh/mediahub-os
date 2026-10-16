# MediaHub OS — Agent Browser Execution Model and Serverless-Use Boundary, Wave 38

- Date: 2026-10-17
- Status: CLI EXECUTION VERIFIED / PUBLIC SITE AVAILABILITY INTERMITTENT / DEPLOYMENT MODEL DOCUMENTED
- Contour: A — Developer Fabric
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Previous capability evidence: [Wave 37 agent-browser verification](MEDIAHUB-AGENT-BROWSER-OPERATIONAL-VERIFICATION-AND-REGISTRY-INVENTORY-WAVE-37-2026-10-17.md), blob `2878ba603aa50a55c196172652fb022a5df56cd0`
- Current `main` HEAD reviewed: `6c2e8dbdee81c798b64e65546e7ded07093f100a`
- Documentation-vs-main compare at pass start: DIVERGED, ahead 1978 / behind 14; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`

## 1. Direct answer: can agent-browser work without a separate server?

Yes, when the CLI runs on an already available computer/workstation with its browser runtime. A dedicated application server or user-managed web server is not required for that local execution mode. The installed CLI uses Chrome/Chromium through CDP and can drive the browser process on the connected workstation.

However, the CLI still requires an execution environment and a compatible browser runtime. It is not a browser process that executes solely inside a text conversation. For fully remote execution without a workstation, a hosted browser execution environment is required (for example, an explicitly provisioned cloud sandbox/browser service). Such a service is distinct from a self-managed application server.

## 2. Evidence from this pass

- The installed `agent-browser` core skill was read. It documents a native CLI, Chrome/Chromium via CDP, accessibility snapshots, element refs, sessions and specialized cloud-browser workflows.
- Direct CLI command opened the Wave 37 checkpoint URL and printed the exact URL.
- `agent-browser get url` returned the same target URL.
- The subsequent accessibility snapshot showed GitHub's transient error page, headed `We're having a really bad day.`, with links to Contact Support and GitHub Status. Therefore, CLI execution and navigation command handling succeeded, while the target content was unavailable during this attempt.
- Wave 37 previously recorded a successful content snapshot of the same public GitHub checkpoint. Combined evidence supports basic CLI/browser operation, with intermittent remote-site availability.
- No package installation, browser repair, credentials, authenticated write, test, provider invocation, infrastructure change or deployment occurred.

## 3. Operational decision

Use the installed `agent-browser` CLI on the already connected workstation as the default browser automation route. A separate server is unnecessary for this route. Treat site content extraction as successful only when the snapshot contains the expected page title/content; URL return alone does not prove that the requested page loaded correctly.

For future runs:
1. Load current instructions with `agent-browser skills get core`.
2. Open the grounded target URL.
3. Check the current URL and capture a fresh accessibility snapshot.
4. Confirm expected page identity/content before extracting evidence or interacting.
5. If an outage page appears, capture the result as an availability failure and retry only within the task's reasonable bounded scope.
6. Keep credentials, write actions, tests, host/runtime inspection, provider calls, qualification and infrastructure behind their existing authority gates.

## 4. Scope boundary

This pass documents the execution model and records a bounded live navigation attempt. It does not certify all sites, authentication flows, file transfer, arbitrary browser actions, or long-running reliability. It does not authorize any new infrastructure or hosted browser provisioning.

## 5. Next step

Continue the repository-wide source crosswalk for `profiles/agent-registry.json` after the browser availability issue is clear, then propose the smallest additive admission validator only after existing consumers and contracts are identified.
