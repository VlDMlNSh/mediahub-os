# MediaHub OS — Cloud-Agent Direct-Egress Decision, Wave 18

- Date: 2026-10-16
- Status: DOCUMENTARY DECISION / PROPOSED / RUNTIME-UNVERIFIED
- Contour: A
- Parent: [Wave 14 credential and egress architecture](MEDIAHUB-CLOUD-NATIVE-CREDENTIAL-AND-EGRESS-ARCHITECTURE-WAVE-14-2026-10-16.md)
- Queue: [Cloud-Agent Activation Queue](MEDIAHUB-CLOUD-AGENT-ACTIVATION-QUEUE-WAVE-11-2026-10-16.json)
- Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Decision

Use GitHub-hosted ephemeral workers as the default Contour A execution environment. The owner's phone and any owner-operated persistent server stay outside the provider credential path. Ordinary jobs require no public inbound listener: the worker initiates outbound HTTPS to GitHub and the explicitly authorized provider endpoint.

Provider credentials remain managed by the provider account/project and are injected at runtime through the approved GitHub Actions secret or environment mechanism. The secret value is excluded from source, task envelopes, prompts, logs, artifacts, caches and evidence manifests. OIDC federation is used only for services that explicitly support the relevant trust flow; it is not a universal substitute for a model-provider API key.

## Network and location boundary

An API key is generally associated with a provider account/project, rather than a physical server. A hosted worker still sends network traffic from its own execution environment. The provider may observe the request's source IP and apply account, service-region, organization, quota, billing or IP-allowlist controls. GitHub-hosted runner egress addresses are dynamic/shared by default, so the architecture assumes no stable source IP.

This design removes the owner's device as a network hop. It does not provide zero network egress, hide the worker's network origin, or guarantee that provider eligibility is independent of account and service-region rules. When provider policy requires a fixed source IP, treat that requirement as an explicit target-profile decision and keep the route blocked until an approved compatible worker/network profile exists.

## Admission of newly authorized agents

For each agent, record its stable provider/model identity, workflow revision, allowed task classes, data classes, destination policy, quota and budget limits, retry policy, expiry, revocation reference and evidence sources. Bind every dispatched task to an immutable source revision and task-specific authorization.

Admission order:
1. Record identity and direct operational evidence.
2. Review the provider's current service and data-handling terms for the intended task.
3. Create a narrow registry candidate with expiry and revocation semantics.
4. Bind task authorization, source SHA, destination, budget and evidence requirements.
5. Validate through the accepted A0 issuer/ingress/lifecycle contract.
6. Dispatch only after A0, R-06, target-manifest, schema-validation and repository-governance gates close.
7. Quarantine results for evidence verification and independent review before PR promotion.

## Current status

The activation queue remains documentary. A0 issuer/lifecycle, R-06 governance, accepted runner/workspace/network target manifest and full v0.2 schema validation remain open. The successful historical Gemini workflow run is evidence for that run and confirms the integration worked in that execution; it does not qualify the general agent fabric or authorize broad task classes.

Proposed queue addition: CAF-Q-015 — owner-server-independent credential and direct-egress profile. This is a planning item, not a live scheduler or active agent dispatch.

## Acceptance criteria

- No owner-operated persistent server in the default provider path.
- No public inbound listener for ordinary agent jobs.
- Runtime-only secret injection with minimal scope.
- Honest provenance for the hosted worker and outbound provider call.
- Per-task provider/model/data authorization and bounded budget.
- Explicit blocked status for missing credentials, policy denial, unknown eligibility or incompatible network requirements.
- Revocable, expiry-bound agent admission.
- Quarantined output and independent review before promotion.
- Separate authorization and evidence for source edits, workflow dispatch, provider calls, tests, qualification and deployment.

## Public-source basis

- GitHub Actions secure use: https://docs.github.com/en/actions/reference/security/secure-use
- GitHub-hosted runners: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- GitHub OIDC: https://docs.github.com/en/actions/concepts/security/openid-connect
- Gemini API terms: https://ai.google.dev/gemini-api/terms
- OpenRouter provider logging: https://openrouter.ai/docs/guides/privacy/provider-logging

No provider calls, secret access, workflow dispatch, tests, installation, host/runtime inspection, infrastructure change, deployment or branch integration occurred in this documentary pass.
