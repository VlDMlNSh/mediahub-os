# MediaHub OS — Endpoint Allowlisting and Provider Secret Partitioning Crosswalk, Wave 31

- Date: 2026-10-17
- ID: MH-ENDPOINT-ALLOWLIST-SECRET-PARTITION-31
- Contour: A — Developer Fabric
- Status: READ-ONLY SOURCE REVIEW / REMEDIATION DESIGN / RUNTIME AND QUALIFICATION BLOCKED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Parent: [Provider Secret-Flow and Egress Crosswalk, Wave 30](MEDIAHUB-PROVIDER-SECRET-FLOW-AND-EGRESS-CROSSWALK-WAVE-30-2026-10-17.md)
- Reviewed product ref: `main@b45324009ac3aa65322a702c28069b12190bc4b8`

## 1. Scope

This bounded pass reconciles the exact current source for provider endpoint selection, the hybrid authentication probe, provider qualification workflow secret injection, and the accepted/proposed contract status of MH-12 and MH-21. It proposes a source-backed remediation boundary. It does not modify executable code, dispatch workflows, access secret values, make provider requests, run tests, inspect hosts/runtimes, alter infrastructure or deploy.

## 2. Source anchors

| Source | Blob SHA | Observation |
|---|---|---|
| `runtime/mediahub_runtime/local_providers.py` | `8361b7d6782adaa9dcd4e47b5d9e9940d41bb1a3` | Configurable `MEDIAHUB_FREELLMAPI_URL`; Bearer key sent to `/models` and `/chat/completions` |
| `ops/qualification/hybrid_agent_auth_probe.py` | `1fb0cb41d219eaf26dc830c8585a790c89a5cb50` | Multiple provider probes; configurable endpoint overrides; Gemini key added to query string |
| `ops/qualification/qualify_execution_backends.py` | `acf092d5dd9d67ab187f1b67ab691ca730028306` | Registry-driven multi-provider qualification; keys read from environment; outbound HTTP requests |
| `ops/qualification/provider_model_registry.json` | `62328126fd2cd8879a73bb6812adcacd3e2abe84` | Provider endpoints, credential environment names and models in a shared registry |
| `.github/workflows/astra-provider-qualification.yml` | `d3160088fbef4fce152ed7335f0acaa3bb440378` | Self-hosted provider job receives a broad set of provider secrets at job scope |
| `docs/architecture/MH-12-secrets.md` | `4e4faf00e3d24c1de5a394e78670c68786ac9a1e` | Secret lifecycle requirement; exact store remains non-canonical pending evidence and ADR |
| `docs/architecture/MH-21-data-egress.md` | `242b3090d41f52866889b8c8cf587ff4c95eadb3` | Proposed deny-by-default data-egress decision sequence |
| `docs/architecture/MH-21-egress-control.md` | `aae23e11a70b1a7094d05709f8669040f60c1dcd` | Proposed explicit, identifiable, policy-controlled, logged and bounded destinations |
| `docs/architecture/MH-21-provider-contract.md` | `d2bf7e29eee9ff2e07f4e25bf58229df11ff3cda` | Provider-neutral operation boundary; proposal only |
| `docs/architecture/MH-21-provider-trust.md` | `ad7226a2e7eeeaf412f94e08440db72ac4fe13cf` | Proposed revocable, time-bounded provider approval lifecycle |
| `schemas/ai/ai-provider-adapter.schema.json` | `e0dab7002222451579e649a7d1d29985393d9a42` | Adapter schema includes endpoint/configuration reference but no full destination-policy decision record |
| `schemas/ai/ai-provider-registry.schema.json` | `9537a64bc948b1bea3e2a640670f48e107760a50` | Provider registry and selection policy schema |

## 3. Findings

### 3.1 Endpoint authorization

- The local provider adapter accepts an environment-selected `MEDIAHUB_FREELLMAPI_URL` and performs requests to appended `/models` and `/chat/completions` paths.
- The multi-provider qualification registry contains configured `base_url` values. The qualification client builds request URLs from these values and uses `urllib.request.urlopen`.
- The hybrid auth probe accepts environment overrides for Kimi, UnoRouter, Claude and GigaChat endpoints. Its Gemini probe places the API key in a query parameter.
- The reviewed request paths show timeouts and bounded response reads in the qualification client, but do not show one shared MediaHub destination authorization check before each request. Default HTTPS URLs alone do not constrain configured overrides or redirect targets.
- This is a source-level control gap, not proof of a deployed exploit or evidence that the relevant workflows have run.

### 3.2 Credential transport and logging

- The Gemini hybrid probe appends `key=<secret>` to the request URL. URLs can be copied into reverse-proxy, gateway, exception, tracing or diagnostic logs. The probe emits exception class rather than exception text, which reduces one output path but does not establish end-to-end URL redaction.
- Other probe paths use provider-specific headers or Bearer authorization. GigaChat first sends a Basic credential to its configured token URL, then sends the returned access token to its configured models URL.
- The provider qualification workflow places many provider keys and Cloudflare account identifiers in one self-hosted job environment before checkout and execution. `persist-credentials: false` limits persisted Git credentials; it does not partition provider secrets from the worker process or from code executed by that job.
- The qualification script reads credential names from a shared registry and is designed to evaluate multiple providers. A single job may therefore need multiple credentials for its declared scope, but the current workflow does not demonstrate per-provider job isolation.

### 3.3 Contract status and authority

- MH-12 requires the Generate → Store → Use → Rotate → Revoke → Destroy lifecycle and excludes secrets from source, Git history, logs, telemetry, prompts and implicit exports. Its exact store remains non-canonical.
- MH-21 egress and provider trust controls are marked PROPOSED. They define the correct direction, but their presence does not establish an implemented gate.
- The current authorization seam accepts a typed `AuthorizationContext` with principal and capability and uses explicit grant matching. The reviewed source does not establish a trusted issuer lifecycle, task-bound credential grant, destination decision or revocation proof at the outbound request boundary.
- The provider adapter schema has an endpoint field and configuration reference; it does not alone prove normalization, destination allowlisting, redirect control, DNS/IP treatment or an authorization record for each request.

## 4. Recommended bounded remediation design

### 4.1 Destination policy as a mandatory pre-request gate

Introduce one provider-neutral decision surface, owned by MediaHub, with an immutable policy revision and an explicit result. The request path should follow:

`task + issuer grant → data classification → provider/model identity → normalized endpoint → destination policy → credential resolution → bounded request → sanitized audit`

The policy should cover:

1. Canonical provider ID, exact hostname, scheme, port and permitted path prefixes.
2. HTTPS for external endpoints. Permit HTTP only for an explicitly admitted local endpoint class, such as loopback-only local inference.
3. Reject URL userinfo, fragments, ambiguous encodings and unapproved ports; normalize hostnames before matching.
4. Resolve DNS and apply explicit public/private/link-local/loopback policy. Bind validation to the actual connection to reduce DNS rebinding risk.
5. Revalidate every redirect hop, or disable redirects for credential-bearing requests by default.
6. Define proxy behavior, TLS validation, timeout, maximum request/response size, allowed methods and content types.
7. Keep destination selection out of model output, prompts, plugins and untrusted configuration unless it resolves to an approved registry entry.
8. Fail closed on unknown provider, endpoint, DNS result, policy revision or authorization context.

This is a proposed contract direction; MH-21 remains PROPOSED until governance accepts it.

### 4.2 Credential scope and delivery

- Resolve an opaque credential reference only after task/issuer/tenant, provider, destination and lease authorization succeed.
- Deliver a credential only to the single provider operation or isolated worker that requires it; keep it out of prompts, artifacts, general environment dumps and audit payloads.
- Prefer provider-supported authorization headers. For providers that mandate query parameters, use a dedicated transport path with explicit URL redaction at application, proxy, tracing and error boundaries.
- Record credential reference/version and policy decision IDs in audit evidence, never secret material.
- Keep key custody, provider account identity, execution location and request egress as separate dimensions.

### 4.3 Workflow secret partitioning

Preferred design: split provider qualification into a bounded coordinator and isolated provider-specific worker jobs.

- Coordinator receives provider IDs, target SHA, task/command identity and policy refs, but no provider secrets.
- Each provider worker receives only the one provider credential set and account identifiers required for that provider. Related credentials such as Cloudflare account ID and token stay together only in the Cloudflare worker.
- The coordinator validates and combines sanitized, schema-checked evidence; it does not inherit worker secrets.
- Pin checkout to the approved target SHA, retain `persist-credentials: false`, bind each worker to an approved runner profile, restrict network egress, and avoid sharing writable workspaces between provider workers.
- Keep the existing workflow interface and qualification semantics until a controlled change proposal confirms compatibility; no workflow edit or dispatch is part of this pass.

### 4.4 Evidence and failure handling

Record provider ID, endpoint-policy revision, normalized destination identity, credential reference/version, task and issuer refs, decision outcome, response classification, bounded timing/size fields, and evidence artifact digest. Redact keys, query parameters, authorization headers, prompt contents and provider response bodies. Missing policy, audit acknowledgement, or issuer state must follow the accepted operation-specific fail-closed rule.

## 5. Candidate traceability delta

- CAF-87 — normalized provider endpoint policy and request-time enforcement.
- CAF-88 — task-scoped credential resolution and URL/header secret hygiene.
- CAF-89 — provider-specific qualification secret partitioning and evidence aggregation.
- SRC-097 — pinned source inventory listed in §2.
- EVD-051 — source-read evidence and remediation disposition.

These identifiers are proposed documentary entries in this report; canonical matrix and source-registry synchronization remains outstanding.

## 6. Decision and next step

**Disposition:** keep runtime admission blocked. The immediate next safe step is to map each proposed gate to the accepted A0/MH-12/R-06 authority and target-manifest sources, then draft a minimal change packet with compatibility and rollback criteria. Implement endpoint policy and workflow partitioning only after the governing contracts, exact target and change authority are established.

No workflow dispatch, provider call, secret access, test, qualification, host/runtime inspection, installation, infrastructure change, deployment or branch integration occurred.

## 7. Verification boundary

Evidence is limited to read-only GitHub file retrieval at `main@b45324009ac3aa65322a702c28069b12190bc4b8` and source/blob metadata. Source presence is not runtime proof; workflow configuration is not evidence of a successful or failed run.
