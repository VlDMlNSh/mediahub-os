# MediaHub OS — CPRG Hosting Alternatives and Reuse-First Readiness, Wave 42

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: DESIGN COMPARISON / HOSTING UNSELECTED / NO IMPLEMENTATION AUTHORIZED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Previous checkpoint: [Wave 41](mediahub-next-continuation-checkpoint-2026-10-17-wave41.md)
- Existing CPRG architecture source: [Central Protected Registration Gateway](2026-09-30-central-protected-registration-gateway.md), blob 6f2d801774179d7cb7e09ae6e7f22645e2a9f13c
- Existing CPRG threat model: [Threat Model and Hardening Plan](2026-09-30-cprg-threat-model-and-hardening.md), blob a1a19ef9a50bc785a948f8034a3ec3e832660284
- Existing identity/recovery sources: [Trust and Identity Contract](2026-09-30-cprg-trust-and-identity-contract.md), blob 502a63fab45971040709ffc5c093bebf38f9dbfa; [Bootstrap, Revocation and Recovery](2026-09-30-cprg-bootstrap-revocation-recovery-protocol.md), blob fe486dcc5723788a90351150f5a0484b74b30692
- Existing candidate register: [Unified Component Candidate and Evaluation Register](../architecture/MEDIAHUB-UNIFIED-COMPONENT-CANDIDATE-AND-EVALUATION-REGISTER-2026-10-15.md), blob 619964539914415891a548a74a1a13b4f05083b6

## 1. Outcome

The project already has a detailed CPRG architecture and threat model. Wave 42 therefore extends that work instead of creating a competing registration design.

**Recommended direction:** retain CPRG as the single logical registration authority with an independently replaceable physical host. Keep the small self-owned Linux server as the first option to evaluate because it may have the lowest incremental hosting cost when suitable hardware already exists. Keep a European VPS as a first-class alternative. Do not select the host until provider eligibility, availability, operating cost, security, and maintenance are compared.

Phone-based enrollment is a temporary operator workflow, not the permanent architecture. The future CPRG host is a dedicated registration appliance, not a general VPN, proxy, developer node, CI runner, model gateway, or data-plane component.

## 2. Hosting and operating alternatives

| Option | Cost profile | Advantages | Main liabilities / unknowns | Current disposition |
|---|---|---|---|---|
| A. Small self-owned Linux host | Potentially lowest recurring hosting cost when hardware already exists; power, connectivity, replacement and operator time remain costs | Administrative control, no VPS rental, physical control of the appliance | Public reachability, ISP/NAT, power and WAN outages, physical security, patching, backup/recovery, hardware age and support lifecycle | **Preferred candidate to evaluate first; not selected** |
| B. European VPS / cloud instance | Recurring rental plus optional backup, traffic and support charges | Stable external reachability, quick replacement, independent physical location, simpler network exposure | Provider trust boundary, recurring cost, provider terms, account/region eligibility, backup and image handling | **First-class alternative; not selected** |
| C. Existing Mac as temporary operator workstation | Low incremental cost if already available; workstation uptime is variable | agent-browser already demonstrated for public GitHub browsing; interactive operator can complete MFA and provider enrollment | Not an always-on isolated registration appliance; user session and workstation security; no qualification for provider enrollment | **Temporary research/operator aid only** |
| D. iPhone manual enrollment | No additional server rental; operator time and phone/VPN costs may apply | Direct use of official provider UI and MFA; useful under the reported server-side access constraint | Manual, difficult to automate and audit at scale; must preserve eligibility and provider terms | **Temporary workflow** |
| E. Free cloud tier / ephemeral workspace | May be zero monetary cost within limits; continuity and quota are uncertain | Useful for experiments or disposable, non-authoritative tasks | Resource suspension/expiry, changing free-tier terms, limited network controls, uncertain persistent storage and regional eligibility | **Research-only fallback; not assumed production-ready** |
| F. Existing central MediaHub/server host | Lowest apparent additional infrastructure cost | Co-location convenience | Conflicts with CPRG's established physical/security separation if it is the same general-purpose MediaHub host; failure and compromise domains become coupled | **Reject as default; reconsider only with explicit architecture change and evidence** |

The cost comparison must use total cost of ownership, not advertised compute price alone: hardware amortization, electricity, network/public IP, backups, maintenance, monitoring, recovery time, and operator time. No current prices were collected in this documentary pass.

## 3. Reuse-first component boundary

The existing repository records OpenBao as a FUTURE-GATED secrets-management candidate and identifies an existing SOPS+age approach for comparison. The default should remain the already approved credential boundary (GitHub Actions Secrets where applicable) until a documented capability gap justifies another secret authority.

| Capability | Reuse-first direction | Admission condition |
|---|---|---|
| Public web research | Existing agent-browser on the connected workstation | Public-source browsing only is verified; provider enrollment and secret entry are not qualified |
| Human enrollment / MFA | Provider's official account UI, operated manually by the owner for now | Account, residence, billing and server-use eligibility confirmed under provider terms |
| Credential storage | Existing GitHub Actions Secrets or approved secret manager | Exact workflow secret name, minimum scope, rotation/revocation and access control established |
| Browser workspace on future Linux host | Reuse an established browser automation/runtime only after comparison; keep browser execution separate from CPRG policy authority | Isolation, browser profile/session disposal, remote access, patch lifecycle and egress controls evidenced |
| Secret manager beyond GitHub | Compare existing SOPS+age and OpenBao candidates before adding a service | Clear need, trust-root design, backup/recovery, operator access and migration plan |
| VPN/network boundary | CPRG's existing registration-only protected path contract | Server-side deny-by-default egress; no general proxy/NAT/full tunnel; destination allowlist and automatic teardown |
| Audit and recovery | Existing CPRG threat, identity, bootstrap/revocation and recovery contracts | Structured secret-free events, integrity, lease expiry, revocation, fail-closed behavior and independent evidence |

A browser automation tool must not become the credential vault or policy authority. CPRG must not persist provider keys outside the explicitly approved secret-management boundary. Browser session cookies, MFA recovery material, and provider secrets must be treated as sensitive and kept out of repository artifacts and audit payloads.

## 4. Non-negotiable architecture

- One logical CPRG authority; the physical host can be replaced without changing its contract.
- Registration traffic is request-scoped, authenticated, authorized, destination-limited, time-limited and audited.
- The VPN path is exclusively for the exact registration operation. No general Internet transit, MediaHub data, storage, developer compute, CI, or model traffic.
- Server-side egress restrictions enforce the boundary independently of client routing.
- Provider eligibility and terms remain authoritative. Geographic hosting or VPN use is not a mechanism to bypass them.
- Secret values stay out of chat, source, registries, commits, command arguments, logs and artifacts.
- CPRG failure blocks registration only; ordinary MediaHub data-plane and developer compute remain independent.
- Deployment, trust-root generation, provider calls, credential use, tests, qualification and infrastructure changes remain gated by separate explicit authorization.

## 5. Evaluation matrix for the next decision pass

Score each hosting option against the same evidence set:
1. Provider account and workload eligibility, by provider and account type.
2. Reachability from the actual operator and intended server network, including NAT/public IP constraints.
3. Monthly recurring cost and one-time hardware/network cost.
4. Security boundary and least-privilege administration.
5. Patch and supported-OS lifecycle.
6. Backup, recovery, host replacement and audit integrity.
7. Registration-only egress enforcement and failure isolation.
8. Secret handoff and browser-session disposal.
9. Provider quota/free-tier behavior, reset semantics, and permitted retry/failover.
10. Operational burden and reversibility.

Use PASS / FAIL / UNKNOWN / CONDITIONAL per criterion with source URLs and observation date. Do not award PASS from a marketing page alone where configuration or qualification evidence is required.

## 6. Status and next step

- CPRG architecture: documented; implementation and qualification remain open.
- Self-owned Linux host: preferred evaluation candidate only; hardware/network facts remain unknown.
- European VPS: approved architectural alternative; provider and plan remain unselected.
- Phone enrollment: temporary operating workflow.
- Secret manager: no additional authority selected.
- Browser automation for provider enrollment: unqualified.
- Provider-specific readiness matrix: still required, based on current workflows, secret names, official policies, quota/reset behavior and region eligibility.

Next bounded pass: map the existing provider workflows and exact secret-name references, then populate provider-by-provider readiness from official public policy sources. Keep provider calls and credential use gated.

## 7. Evidence boundary

Read current documentation branch files and verified live branch comparison through GitHub. agent-browser successfully opened the current documentation-branch checkpoints directory and exposed the existing CPRG documents. This pass performed documentation/source review only. No installation, host/runtime inspection, credential access, provider call, test, qualification, infrastructure change, deployment or merge/rebase/cherry-pick occurred.

- Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
