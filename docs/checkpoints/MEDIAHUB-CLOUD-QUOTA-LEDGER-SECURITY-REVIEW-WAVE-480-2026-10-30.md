# Wave 480 — cloud quota-ledger contract and gateway security re-evaluation (2026-10-30)

## Status

**DESIGN DRAFT COMPLETE / NOT IMPLEMENTED / NOT TESTED / NOT QUALIFIED / NOT ACCEPTED.**

This pass corrects a repository-identification error in Wave 479 and defines a synthetic-only quota-ledger contract. No gateway was installed or executed; no provider credentials were accessed; no provider API calls or agent dispatches occurred.

## Immutable target and governance snapshot

- Main source SHA retained from the last known main snapshot: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`. The repository search connector did not provide a reliable latest main HEAD in this pass; therefore current main HEAD is **NOT VERIFIED** and must be refreshed before implementation.
- Canonical docs branch: `docs/mediahub-chat-tree-map-20261012`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN. It explicitly orders A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy, runner target acceptance, Draft 2020-12 schema validation with negative fixtures, independent review, then bounded read-only worker.
- Issue #301 says its documentary queue is not a live scheduler and does not authorize credential access, provider calls, dispatch, infrastructure changes, merge or deployment.
- PR [#591](https://github.com/VlDMlNSh/mediahub-os/pull/591) is OPEN/DRAFT/UNMERGED at head `86ebdaeaadb2b4559fd1e0e83f77954b5e359dd9`; workflow runs and combined statuses returned empty arrays; formal reviews/comments returned empty. Exact-head CI and independent review are **NOT VERIFIED**.
- PR #590 remains OPEN/DRAFT; PR #441 remains OPEN/unmerged. PR #437 is MERGED.
- Main `.github/ai/model-router.yml` remains policy-only, with direct provider calls disabled and only the Gemini controller and FCC/OpenRouter Free workflow listed as admitted transports. It still contains a local FCC/Ollama route, which requires separate explicit reconciliation against cloud-only Contour A; this pass does not edit or activate it.
- Gemini controller still has a 3-child batch model and requires the repository admission flag plus exact target, controller secrets, duplicate guard and all remaining gates. The presence or value of secrets/variables was not checked. No controller run was attempted.
- SentinelX latest host listing: zero connected hosts; `Voktors-Mini.Dlink` offline; `mh-dev-01` and `mh-dev-02` disabled. No eligible third host is available; Claude Code task not run.

## Correction to Wave 479 Bifrost identification

Wave 479 incorrectly cited `boelabs/bifrost` as the Bifrost model gateway and attributed a PostgreSQL 18+/Redis 8+ deployment requirement to it. That repository is not the intended Maxim AI gateway. **This attribution is withdrawn.**

The correct project is [maximhq/bifrost](https://github.com/maximhq/bifrost), whose README states Apache-2.0. It is a modular Go gateway with independently versioned transport and plugins. The current release listing observed `Bifrost HTTP v2.3.2` (2026-10-20; commit `a05ea20`), with core `v1.13.1` and framework `v1.10.1` in that release. It also has distinct plugin release versions. Do not treat one gateway tag as the version of every module.

Bifrost has three public repository advisories visible in the current advisory listing:
- GHSA-86gf-xh3g-rvxq — Critical, Bifrost MCP Stdio RCE (2026-09-23).
- GHSA-2qp8-4xgm-fw6g — High, unauthenticated RCE via custom plugin HTTP path on dynamically linked builds (2026-09-23).
- GHSA-w98g-5w9p-p3rc — High, SSRF deny-list incomplete in URL fetching (2026-07-21).

The release v2.3.2 records a Go 1.27.3 security update for CVE-2026-111943 in TLS certificate verification. This is a positive maintenance signal, not proof that the three Bifrost advisories are all remediated in the exact chosen component set. A future audit must map each advisory to affected component/version and patch commit before qualification.

Sources: [Bifrost repository](https://github.com/maximhq/bifrost), [Apache-2.0 license in README](https://github.com/maximhq/bifrost/blob/dev/README.md), [release v2.3.2](https://github.com/maximhq/bifrost/releases), [security advisories](https://github.com/maximhq/bifrost/security/advisories), [provider routing docs](https://github.com/maximhq/bifrost/blob/dev/docs/providers/provider-routing.mdx).

## LiteLLM security and quota semantics re-evaluation

The current LiteLLM documentation is more nuanced than Wave 479 recorded:
- Budget controls require a database; a DB-less deployment does not enforce configured spend budgets and may continue serving requests.
- Current documentation describes Redis cross-pod reservation counters and a `fail_closed_budget_enforcement` option that checks the authoritative database and rejects with 503 if spend cannot be verified against Redis or DB.
- This does **not** establish a provider's actual free-tier quota, provider account identity, free entitlement, or reset policy. Those remain MediaHub-owned state.
- The current official advisory list includes CVE-2026-114612 / GHSA-7hp6-4w63-5g45 (critical privilege escalation), GHSA-3cv6-jpf6-8222 (authenticated SSRF/credential exfiltration), GHSA-g5ff-637f-6q2m (high local file read), and GHSA-w4c7-34wj-hqm8 (critical Enterprise-only unauthenticated file read/master-key exposure).
- The Enterprise-only GHSA-w4c7 advisory lists patched release floors 1.103.10, 1.104.8, 1.105.6 and 1.106.5 for the respective release lines. A blanket "latest version is safe" claim is not acceptable: the October 21 v1.107.0 incident and its signing-key rotation require exact artifact provenance review. Pin by verified digest, not mutable `latest`.

Sources: [LiteLLM budget/rate-limit docs](https://docs.litellm.ai/docs/proxy/users), [production best practices](https://docs.litellm.ai/docs/proxy/prod), [official security page](https://www.litellm.ai/security), [GHSA-7hp6-4w63-5g45](https://github.com/advisories/GHSA-7hp6-4w63-5g45), [GHSA-w4c7-34wj-hqm8](https://github.com/BerriAI/litellm/security/advisories/GHSA-w4c7-34wj-hqm8), [GHSA-3cv6-jpf6-8222](https://github.com/advisories/GHSA-3cv6-jpf6-8222).

## Contract artifact

Added [MEDIAHUB-CLOUD-QUOTA-LEDGER-CONTRACT-WAVE-480-2026-10-30.json](MEDIAHUB-CLOUD-QUOTA-LEDGER-CONTRACT-WAVE-480-2026-10-30.json), status `PROPOSED_NOT_IMPLEMENTED_NOT_ACCEPTED`.

It specifies:
- provider-account + entitlement identity as the quota boundary;
- same-account credentials share quota unless published provider terms prove otherwise;
- atomic reservation before outbound request, idempotent settlement, explicit UNKNOWN state for uncertain network outcomes;
- Retry-After handling and provider-documented reset windows;
- fail-closed behavior for unknown entitlement, unavailable ledger, revoked routes, 401/403 and ambiguous send outcomes;
- MediaHub policy remains authoritative over gateway routing and fallback;
- 15 synthetic acceptance cases (Q001–Q015), including races, key grouping, duplicate settlement, timeout ambiguity, paid fallback denial, revocation and gateway allowlist enforcement;
- secret values and authorization headers are forbidden in registry and evidence.

The contract is intentionally not a runtime JSON Schema and has not been validated by a Draft 2020-12 validator. It is a design artifact only.

## Comparative disposition

| Candidate | New evidence | Remaining blocker | Disposition |
|---|---|---|---|
| LiteLLM | Current docs describe DB-backed budgets, Redis reservations and an explicit fail-closed budget setting. Public security advisories include critical issues and a recent package incident. | Exact stable artifact/digest, patch floors, release provenance, config hardening, advisory mapping, and separation of provider free quotas from gateway spend budgets. | Keep as candidate; no selection. |
| Bifrost (correct project: maximhq/bifrost) | Apache-2.0; modular Go gateway; routing allowlists and virtual-key/provider restrictions documented; current release v2.3.2. | Critical/high advisories across MCP, custom plugins and SSRF; component-level patch mapping; account quota and reset semantics; durable ledger behavior. | Keep as candidate; no selection. |

**Decision: no winner.** Bifrost is not a clean replacement for LiteLLM merely because it is written in Go or uses Apache-2.0. LiteLLM is not acceptable solely because it offers budgets and virtual keys. Both must pass the same synthetic contract, component-level security review, artifact provenance, and fail-closed configuration review.

## Required next qualification gate

1. Reconcile cloud-only policy and Issue #301 gates before any gateway runtime.
2. Freeze exact source tag + commit + artifact digest for each candidate and all separately versioned modules.
3. Map every public advisory to affected/fixed versions and test the chosen exact artifact against the affected code paths.
4. Implement the quota ledger independently of gateway-native budgets. Gateway budget controls are defense-in-depth only.
5. Execute Q001–Q015 using a deterministic fake provider and synthetic account/credential references; test at least two independent ephemeral workers against one shared transactional ledger.
6. Require all 15 cases to pass, with reproducible test output, before considering any live provider qualification.
7. Independent security/provenance review; no new transport allowlist entry until reviewed contract changes and Issue #301 gates pass.

## Execution record

- Contract/report authoring: **SUCCEEDED** (documentation only).
- Contract schema validation: **NOT RUN**.
- Synthetic tests Q001–Q015: **NOT RUN**.
- Gateway installation, source build, benchmark, SBOM, vulnerability scan, signature verification: **NOT RUN**.
- Provider credentials read: **NO**.
- Provider calls: **NOT RUN**.
- Gemini controller / child jobs: **NOT RUN**; no run/job IDs.
- Claude/FCC: **NOT RUN**; no host/session IDs.
- Merge, deployment, runtime qualification, adoption: **NOT RUN**.
- PR #591 exact-head CI and independent review: **NOT VERIFIED**.
- No secrets were accessed or written.

## Next step

A code-level synthetic conformance test harness can be designed on a dedicated branch after the quota-ledger contract receives independent review. Do not install either gateway or contact providers in that step.

## Canonical references

- [Canonical chat tree map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 479 report](MEDIAHUB-CLOUD-MODEL-ROUTER-COMPONENT-SELECTION-WAVE-479-2026-10-30.md) on the separate Wave 479 branch
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
