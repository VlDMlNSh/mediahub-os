# Wave 262 — GitHub-cloud-only agent pool and local Jarvis boundary (2026-10-20)

## Decision recorded
The owner's clarified infrastructure boundary is explicit:

- **Contour A cloud agent pool:** orchestration, scheduling/dispatch, worker execution, task coordination, artifacts, evidence, audit, policy gates and recovery must use GitHub-hosted cloud components. For the initial implementation, GitHub Actions with ephemeral GitHub-hosted runners is the approved execution substrate under existing governance gates.
- **No owner-operated or dedicated physical equipment/servers** may be required to host, coordinate, or execute the cloud pool. Do not make a VPS, self-hosted runner, local workstation, NAS, or always-on listener a dependency of the pool.
- **External model APIs are model endpoints, not pool infrastructure.** Calls to Gemini or other model providers may occur only from authorized GitHub-hosted jobs, using runtime-only secret injection, provider terms/data-route controls, and existing issuer/capability gates. They are not authorization to introduce external orchestration servers or route around the approved controller.
- **Local compute is reserved for Jarvis** and its later local execution needs. Do not couple cloud-pool availability or qualification to current servers. Local executors/Jarvis design and deployment remain a separate later stage after the cloud pool is deployed and independently operationally accepted.
- Contour B remains blocked until Contour A is independently accepted.

## Sources and current evidence
- Canonical map (docs branch) blob: `cae684678cfbe31a88d01d65614420b70dbc7394`.
- Bootstrap instruction blob: `0738dc5abb5cb8c00819628289bb5d90ae193900`; it requires current map/source checks before action and states it does not override normative baseline/governance decisions.
- Issue #301 remains OPEN and says its architecture is GitHub-hosted ephemeral workers with direct outbound HTTPS, runtime-only secret injection, and no assumed fixed egress IP. The task envelope, agent registry and evidence manifest v0.2 remain candidates; standards-compliant Draft 2020-12 validation and negative fixtures remain open. CAF-Q-001…015 are documentary, not a live scheduler.
- Main branch provider registry `ops/qualification/provider_model_registry.json`, blob `62328126fd2cd8879a73bb6812adcacd3e2abe84`, contains 25 provider records; these are candidates, not proof of active access or qualification.
- Existing controller `.github/workflows/gemini-batch-dispatch-controller.yml`, blob `99e5a87825aeb239568f96ecef004a102ff3e53b`, currently contains a `workflow_dispatch` confirmation gate and uses `MEDIAHUB_GITHUB_TOKEN` for API dispatch. This source inspection is not permission to dispatch. PR #421 remains OPEN/Draft at the time of this pass. Controller migration and all launch actions remain governed by review/CI/authorization gates.
- Wave 42 router ADR remains proposed/implementation-gated; third-party router or database services must not be introduced as mandatory cloud-pool infrastructure without a new explicit architecture decision and governance acceptance.

## Architectural implications
1. Treat GitHub Actions + GitHub-hosted ephemeral runners as the initial execution plane; workflows are the job envelope, not a free-standing unconstrained scheduler.
2. Use repository artifacts/checks/run IDs and evidence manifests for verifiable outputs, with bounded retention and data classification. Do not place credentials in logs, artifacts, prompts, query strings or repository content.
3. Persist only the minimum coordination state needed in authorized GitHub-supported mechanisms initially. If GitHub-native facilities cannot satisfy durable queue/lease requirements, document the specific capability gap and request a governance/change-control decision before adding any external hosted database, queue or router. No hidden fallback.
4. Do not use self-hosted runners, remote desktop servers, SentinelX-managed hosts, local shell processes or user-operated hardware as cloud-pool workers.
5. Candidate multi-agent frameworks may be integrated only as libraries/workflow logic inside GitHub-hosted jobs, not as a second controller, external server, or independent authority. ECC remains workflow-practice-only under its canonical integration decision.
6. Provider selection and fallback are constrained by the existing registry, provider terms, current quota/reset evidence, task envelope, data-egress policy, caller capability, budget, timeout/cancellation and fail-closed behavior.
7. Jarvis/local executor infrastructure is a separate phase, intentionally decoupled from Contour A's cloud execution.

## Verification limits
This wave was a documentation/architecture boundary pass. No workflow was dispatched, no provider called, no secret accessed, no code installed, no server touched, no merge/deployment performed, and no route qualified. This report does not claim GitHub-only implementation has been deployed or accepted.

## Next bounded action
Continue the provider-registry consumer census and reusable-component matrix with a hard filter: GitHub-hosted/no customer-managed server. Prototype schema validation, task envelopes, mock providers, evidence manifests and quota reservation tests in CI without provider invocation. If the needed durable state cannot be delivered using authorized GitHub-native components, stop at a documented gap and submit a governance proposal rather than silently introducing another service.

## Navigation
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #421: https://github.com/VlDMlNSh/mediahub-os/pull/421
