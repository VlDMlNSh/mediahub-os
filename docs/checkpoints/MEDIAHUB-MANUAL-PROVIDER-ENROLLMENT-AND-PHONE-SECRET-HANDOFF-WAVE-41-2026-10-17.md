# MediaHub OS — Manual Provider Enrollment and Phone-Originated Secret Handoff, Wave 41

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: OWNER-DIRECTED OPERATING CONSTRAINT RECORDED / DESIGN ONLY
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- MediaHub `main` HEAD at pass start: `6c2e8dbdee81c798b64e65546e7ded07093f100a`
- Documentation branch compare at pass start: DIVERGED, ahead 1994 / behind 14; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`
- Previous checkpoint: [Wave 40](mediahub-next-continuation-checkpoint-2026-10-17-wave40.md)

## 1. Owner-provided operating constraint

The owner reports that provider registration/API-key pages may be blocked when opened from the Russia-hosted server. Until a provider-specific, policy-compliant path is established, account enrollment and API-key creation are to be performed manually by the owner on a phone, using a VPN only where permitted by the provider's terms and applicable law.

This is an operating assumption supplied by the owner; this pass did not test provider registration pages, region eligibility, a VPN, or any API credentials.

## 2. Execution boundary

- The Russia-hosted server is not the registration browser and must not be treated as the operator's browser identity.
- The owner performs account sign-in, eligibility checks, enrollment, MFA and API-key creation manually on the phone.
- Provider terms and regional eligibility remain authoritative. A VPN must not be used to falsify residence, billing identity, business location, or other eligibility facts. If a provider disallows the region/account, mark that provider BLOCKED and choose an eligible provider or documented alternative.
- ChatGPT, issue text, pull-request descriptions, commits, logs, workflow output and repository files are not credential-entry channels.
- After creating a key, the owner enters it directly into the intended GitHub Actions secret or approved secret manager through its official UI. Use the exact secret name required by the selected workflow. Never commit the key, add it to a JSON/YAML registry, include it in a command line, or paste it into this chat.
- Prefer a provider-supported, narrowly scoped, revocable key; apply quota/billing limits and expiration where supported. Record only non-secret metadata: provider, secret name, purpose, scope, creation date, expiry/rotation date and owner.
- If a key has appeared in chat, a commit, a log, an artifact or a workflow output, treat it as exposed and rotate/revoke it using the provider's official console.

## 3. Browser and server roles

`agent-browser` remains suitable for public-source research on the connected workstation. Do not run provider registration or secret entry through a Russia-hosted server browser under the current operating assumption. Browser automation for account enrollment is out of scope for this pass; the owner-directed flow is manual phone operation.

The phone/VPN path does not itself prove that a provider accepts the account, permits use from the server's region, or supports the intended workload. Verify these separately through the provider's official policy and dashboard.

## 4. Secret handoff sequence

1. Select a provider only after checking availability, account eligibility, API terms, rate limits and quota behavior.
2. Owner creates the account/key manually on the phone through the provider's official interface.
3. Owner adds the key directly to the correct GitHub Actions repository/environment secret. Enable environment protection and required reviewers where supported and proportionate.
4. Keep workflow permissions least-privilege and avoid printing environment variables or request headers.
5. Use a metadata-only handoff record; do not capture or share the secret value.
6. A later, separately authorized provider smoke test may validate access. This pass did not invoke providers, read secrets, dispatch workflows, or run tests.

## 5. Reuse-first implementation implications

- Keep provider metadata and credential references in the existing registry; never store credential values there.
- Keep provider enrollment separate from server execution and agent orchestration.
- Before quota-based failover, require explicit provider-specific eligibility, quota/error classification, bounded retries, idempotency, rate limits and audit evidence. Do not rotate across keys to evade provider quotas or account restrictions.
- Treat manual enrollment as an operational prerequisite, not proof of provider integration or qualification.

## 6. Evidence and limitations

The `agent-browser` core skill loaded and the public MediaHub repository root opened successfully on the connected workstation. This verifies public GitHub navigation only. No provider registration, VPN behavior, secret entry, credential access, provider call, test, installation, host/runtime inspection, infrastructure change, deployment or qualification occurred.

## 7. Next bounded step

Produce a provider-by-provider readiness matrix using public policy documentation and current repository workflow/secret-name references: eligible account path, required secret name, free-tier/quota behavior, rotation semantics, server-region constraints and evidence required before an authorized smoke test. Keep provider calls and credential use behind explicit authorization.

- Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
