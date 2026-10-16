# MediaHub OS — Russia-Hosted Runner Boundary and Provider-Key Enrollment Design, Wave 41

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: ARCHITECTURE RECONCILIATION / PROVIDER GEOGRAPHY GATE OPEN
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- User constraint incorporated: the server is hosted in Russia; provider registration/key-management pages may be unavailable there because of provider or jurisdictional location restrictions.
- Previous source baseline: [Wave 40 OpenHands current-head reconciliation](MEDIAHUB-OPENHANDS-CURRENT-HEAD-DELTA-AND-ROUTE-BOUNDARY-RECONCILIATION-WAVE-40-2026-10-17.md)
- Applicable contracts: `docs/architecture/MH-12-secrets.md`, `MH-21-cloud-credentials.md`, `MH-21-data-egress.md`, `MH-21-egress-control.md`, `MH-21-provider-trust.md`.

## 1. Decision

Provider enrollment and provider execution are separate control planes. A Russian-hosted runtime must not be expected to browse provider registration pages, create accounts, complete identity checks, or obtain API keys. Browser automation must not be part of the production key-provisioning path.

The owner/operator may create a provider account and key through a browser in a location where the provider explicitly offers the service and where the action complies with provider terms and applicable law. The key is then entered directly into an approved secret store, such as a GitHub Actions repository/environment secret when that storage scope is approved. The key must never transit through chat messages, source files, logs, artifacts, model prompts, screenshots, or repository commits.

This operator-side enrollment path only solves the account/key-entry interface problem. It does **not** establish that requests from a Russian-hosted runner are eligible or permitted. Provider-origin geography, account eligibility, IP allowlists, sanctions/export controls, contractual region limits, data residency and provider policy must be evaluated independently.

## 2. Required control-plane split

| Plane | Responsibility | Allowed location | MediaHub gate |
|---|---|---|---|
| Account and key enrollment | Human account setup, identity verification, key creation and rotation | Operator browser in a provider-authorized location | Human action; provider terms and legal eligibility checked |
| Secret custody | Store a key under a stable secret reference; restrict readers and audit rotation | Approved secret store; prefer GitHub Actions environment-scoped secrets for CI when contractually suitable | MH-12; least privilege; masked logs; no key echo |
| Job dispatch | Select an approved provider profile and execution target | GitHub control plane / authorized orchestrator | Provider and target policy admission |
| Provider invocation | Send inference request using a scoped secret | Only an explicitly approved execution region and network path | Provider trust, egress allowlist, data classification, purpose authorization |
| Evidence | Record provider ID, secret reference (never secret value), execution region/target, request class, policy decision, result status, quota and timestamps | Sanitized evidence store | R-06 audit/privacy and retention rules |

## 3. Geographic admission policy

Each provider profile must express or reference:
- provider legal identity and service/product;
- account/organization eligibility and allowed regions;
- permitted execution regions and source-network/IP constraints;
- API endpoint and explicit egress destination class;
- data classes allowed for transmission and retention/training terms;
- authentication mechanism and secret reference;
- quota/rate-limit policy and rotation owner;
- evidence freshness and a revocation path.

Admission must fail closed when a required eligibility or region fact is unknown, stale, or contradictory. A secret being present, a registration page being reachable, or a prior HTTP 200 response is insufficient proof of geographic eligibility.

If the Russian-hosted runner falls outside provider policy, quarantine that provider for this target and route eligible workloads to another provider/target whose geography is explicitly approved. Do not use a VPN, proxy, remote browser, third-party relay, alternate identity, or hosted runner to disguise the actual execution origin or bypass a location restriction. A different execution target is eligible only after its true region, network egress, data path and provider terms are independently approved.

## 4. Existing MediaHub source evidence

- `docs/architecture/MH-12-secrets.md` states that secrets include API keys and must be bounded/auditable; secrets must stay out of source, Git history, logs, telemetry, AI prompts and diagnostic snapshots. Exact secret store remains non-canonical pending evidence and ADR.
- `docs/architecture/MH-21-cloud-credentials.md` separates MediaHub, user, workload, service and provider identities; credentials are least-privilege, scoped, rotatable, observable and auditable.
- `docs/architecture/MH-21-data-egress.md` establishes default-deny arbitrary egress and explicit authorization for sensitive/private data.
- `docs/architecture/MH-21-provider-trust.md` explicitly includes region and legal constraints in provider evaluation.
- `.github/workflows/gemini-autonomous-engineering.yml` passes `secrets.GEMINI_API_KEY` to the configured Gemini action. This demonstrates a secret injection path, not provider registration capability or regional eligibility.
- `.github/workflows/astra-provider-qualification.yml` binds numerous provider credentials to a self-hosted runner labelled `mediahub-provider`. That label alone does not establish the runner's region, the provider's regional eligibility, or approval of every provider listed.

## 5. Implementation boundary and current disposition

This wave is a source-backed design decision only. No secret was accessed, created, changed, or tested. No provider was called. No workflow, runner, network, infrastructure or deployment configuration was changed. The current Russian hosting detail is owner-supplied context; the exact egress IP, provider-specific terms and provider eligibility have not been independently verified.

Current status:
- Operator-side enrollment separation: DESIGN ACCEPTED.
- Secret custody contract: PARTIALLY DEFINED; canonical store/ADR remains open.
- Provider-by-provider regional eligibility: OPEN.
- Russian runner egress region/IP and routing evidence: UNKNOWN.
- Provider execution admission for any geography-restricted service: BLOCKED until the specific provider/target pair is verified.
- Runtime/qualification/deployment: CLOSED pending separate authorization.

## 6. Next bounded step

Build a provider-by-provider admission matrix from existing provider profiles and workflows. For each entry, classify account/key enrollment, secret reference, actual execution target, known region restrictions, egress evidence, data eligibility and quota/rotation behavior. Preserve existing IDs and registry contracts. No credentials, tests, provider calls, host inspection or infrastructure actions are part of that pass.

- Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
