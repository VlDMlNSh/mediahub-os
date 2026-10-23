# MediaHub — Claude Code GitHub-hosted runner / ECC profile investigation (Wave 366)

Date: 2026-10-22  
Status: **DOCUMENTED / PLANNED / NOT DISPATCHED / NOT QUALIFIED / NOT ACCEPTED**

## Canonical references
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on `docs/mediahub-chat-tree-map-20261012`.
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), observed blob `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Master roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md), observed blob `4b45b4bfeb5fcbf2dd409fb98241832283982c95`.
- Main source snapshot observed in repository search: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`. This is a search-result source snapshot, not asserted as the current main HEAD.
- Existing policy: [ASTRA-ECC-INTEGRATION.md](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/operations/ASTRA-ECC-INTEGRATION.md), blob `c707a83777ae5970081bd6bb1e3027c88bbf3fa1`.
- Governing cloud-agent objective: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Bounded follow-up: [Issue #496](https://github.com/VlDMlNSh/mediahub-os/issues/496).

## Findings
1. Issue #301 defines GitHub-hosted ephemeral workers as the default cloud lane, requires outbound HTTPS, runtime-only secret injection, explicit provider/model route and budget controls, and forbids assuming fixed hosted-runner egress or using proxy/region spoofing.
2. Existing ASTRA ECC policy explicitly rejects ECC as a dependency or second controller. It permits selective ECC-derived workflow guidance under `.claude/skills/`; executable worker gates remain authoritative. Any full upstream ECC install must be treated as a policy change, not silently enabled.
3. Existing repository evidence describes a historical local Claude Code → Ollama route on `Voktors-Mini.Dlink`. That is a distinct local lane and does not prove the GitHub-hosted Claude lane works. This pass did not contact the host.
4. The current upstream ECC install contract, release/commit pin, license/security review, and exact compatible Claude Code GitHub Action have not been verified in this pass. The GitHub connector search did not establish a reliable canonical upstream read-back; no upstream source is treated as verified.
5. No existing Claude GitHub-hosted executor workflow was proven by the searches performed. Search hits include historical local executor workflows and generic Astra workers, which are not evidence of a qualified cloud Claude lane.

## Proposed bounded acceptance sequence
1. Read the canonical ECC repository/release and installation docs; pin a reviewed commit/release and record source blob hashes and license.
2. Keep the initial profile opt-in and minimal. Prefer a project-owned `.claude/skills/` subset; do not install ECC's controller, broad hooks, MCP tools, memory, or plugins without separate admission.
3. Inspect the official Claude Code GitHub Actions integration and pin every third-party action to a full commit SHA.
4. Require a GitHub-hosted ephemeral runner label; reject self-hosted runners and all SentinelX/local-host transport for this lane.
5. Establish the provider identity, eligibility/terms, quota, budget and no-paid-fallback behavior before any model invocation. No provider call is authorized by this report.
6. Separate read-only planning from patch-writing and PR promotion. Do not expose repository write tokens to the model process; use least-privilege runtime credentials and avoid `secrets: inherit`.
7. Add non-launching contract tests and negative fixtures first. Live dispatch only through a separately approved admission/controller path after existing governance gates pass.
8. Capture target SHA, workflow/run/job IDs, terminal statuses, artifact digests, exact-head CI, independent security review, and explicit blockers. Empty CI/review results remain NOT VERIFIED.

## Prohibitions and authority boundaries
- No direct dispatch bypassing the approved controller/governance path.
- No Gemini transport through server 3 or this Claude lane.
- No paid provider fallback, credential-value inspection, secret exposure in logs/artifacts, merge, deployment or qualification claim.
- ECC must not become a second controller or acquire issuer/capability, ASTRA A0, or MediaHub Product State Authority.
- A workflow definition, issue, or static test is not runtime qualification.

## Evidence and limitations
- Issue #496 was read back and remains OPEN; its acceptance sequence matches the constraints above.
- ASTRA ECC policy blob read back at `c707a83777ae5970081bd6bb1e3027c88bbf3fa1`.
- Canonical map fetch returned an empty content field, so its exact blob was read via blob API; blob SHA `f04873c9cbbf1ba8d45ccbfd3f6afc8cee916a41`. The map text is large and not printed in full.
- The docs branch is distinct from `main`. This report is a candidate documentation change on a dedicated branch; it is not canonical/accepted until review and integration.
- No tests, workflow dispatch, model/provider calls, host operations, merges or deployments were performed.

## Next step
Verify the canonical upstream ECC source and official Claude Code GitHub Actions contract at immutable refs; then prepare the smallest source-pinned, non-launching contract/profile PR. Keep Issue #496 PLANNED until that evidence and independent review are available.
