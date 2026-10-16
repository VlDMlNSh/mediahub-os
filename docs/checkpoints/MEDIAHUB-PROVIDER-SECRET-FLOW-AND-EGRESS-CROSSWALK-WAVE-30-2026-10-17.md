# MediaHub OS — Provider Secret-Flow and Egress Crosswalk, Wave 30

- Date: 2026-10-17
- ID: MH-PROVIDER-SECRET-FLOW-EGRESS-30
- Contour: A — Developer Fabric
- Status: READ-ONLY SOURCE REVIEW / FINDINGS OPEN / RUNTIME AND QUALIFICATION BLOCKED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Parent: Wave 29 OpenHands app-backend bridge threat crosswalk.
- Main HEAD observed: `b45324009ac3aa65322a702c28069b12190bc4b8`
- Main recursive tree: 802 entries, `truncated=false`.

## 1. Scope and evidence

Read-only GitHub source inspection. No credentials were accessed, provider requests made, MCP servers invoked, tests run, workflows dispatched, hosts inspected or infrastructure changed.

| Source | Ref | Blob SHA | Evidence |
|---|---|---|---|
| `docs/architecture/MH-12-secrets.md` | main | `4e4faf00e3d24c1de5a394e78670c68786ac9a1e` | Lifecycle Generate → Store → Use → Rotate → Revoke → Destroy; exact store remains non-canonical pending evidence/ADR |
| `docs/architecture/MH-21-cloud-credentials.md` | main | `7f420277f843f93c938e6a3b98637888ce89be2d` | Proposed; separate identities and provider credentials; least privilege |
| `docs/architecture/MH-21-data-egress.md` | main | `242b3090d41f52866889b8c8cf587ff4c95eadb3` | Proposed classification/purpose/destination/policy/authorization/minimization/bounded transfer gate |
| `docs/architecture/MH-21-egress-control.md` | main | `aae23e11a70b1a7094d05709f8669040f60c1dcd` | Explicit, identifiable, logged, bounded destinations |
| `docs/architecture/MH-21-provider-adapter.md` | main | `d8b61d65435b13202530946687f8c074617f8c67` | Provider adapter boundary remains proposed |
| `docs/architecture/MH-21-provider-contract.md` | main | `d2bf7e29eee9ff2e07f4e25bf58229df11ff3cda` | Provider-neutral operations; proposed |
| `docs/architecture/MH-21-provider-trust.md` | main | `ad7226a2e7eeeaf412f94e08440db72ac4fe13cf` | Revocable, time-bounded provider approval lifecycle; proposed |
| `runtime/mediahub_runtime/local_providers.py` | main | `8361b7d6782adaa9dcd4e47b5d9e9940d41bb1a3` | File-based key loading and HTTP calls to configured base URL |
| `ops/qualification/hybrid_agent_auth_probe.py` | main | `1fb0cb41d219eaf26dc830c8585a790c89a5cb50` | Environment credential lookup and provider model probes |
| `.github/workflows/astra-provider-qualification.yml` | main | `d3160088fbef4fce152ed7335f0acaa3bb440378` | Broad set of provider secrets placed in self-hosted runner environment |
| `schemas/ai/ai-provider-adapter.schema.json` | main | `e0dab7002222451579e649a7d1d29985393d9a42` | Adapter contract schema |
| `schemas/ai/ai-provider-registry.schema.json` | main | `9537a64bc948b1bea3e2a640670f48e107760a50` | Registry schema; includes selection policies such as FAILOVER |
| `.github/workflows/mediahub-agent-fabric-verify.yml` | main | `2cec0ba1f02018f7037417363c707a13bc673117` | Separate repository verification workflow; not evidence of provider qualification |

## 2. Secret-flow and egress matrix

| Path | Observed flow | Current control/evidence | Gap and disposition |
|---|---|---|---|
| Local FreeLLMAPI adapter | Reads a key from a configurable local file; sends it as Bearer authorization to `base_url/models` and `base_url/chat/completions` | Empty/unavailable key fails closed; timeout and response-size bounds exist | `MEDIAHUB_FREELLMAPI_URL` can select the destination. Source does not show an approved-destination allowlist, HTTPS enforcement, or a policy check binding data class/task to that destination. **OPEN / HIGH PRIORITY** |
| Hybrid provider probe | Reads provider credentials from environment; sends provider-specific requests to configured/default model endpoints | Emits a sanitized status summary; exception output is reduced to exception type | Gemini key is placed in a URL query parameter by the source. Query strings may enter upstream/proxy logs. Kimi, Claude, UnoRouter and GigaChat endpoint overrides are environment-configurable; GigaChat bearer token is sent to the configured models URL. Destination policy and log-scrubbing guarantees are not established by this source. **OPEN** |
| Provider qualification workflow | Maps many repository Actions secrets into the job environment on a self-hosted `mh-dev-02` runner | Checkout disables persisted Git credentials; output summary selects limited fields | Environment exposure is broad relative to a single provider/task. Least-privilege secret partitioning, runner isolation and job-level destination binding require source/config evidence and independent review. Workflow is callable; it was not dispatched. **OPEN / HIGH PRIORITY** |
| Provider credential storage/decryption | Current reviewed local adapter reads plaintext key files; probe consumes environment variables | MH-12 requires lifecycle and secret exclusion; exact secret store remains non-canonical | No common vault/broker, envelope-encryption, audited decrypt API or task-scoped JIT resolution path was established in these reviewed sources. **UNKNOWN / GOVERNANCE-GATED** |
| Provider connection routes | No provider-connection HTTP route file was identifiable in the complete current `main` tree by route/name inventory | Provider schemas and adapters exist | This establishes only that the reviewed main tree has no identifiable route artifact under the searched inventory; deployed services/external components remain UNKNOWN. **OPEN** |
| MCP server configuration / calls | No tracked MCP configuration file/path was identifiable in the complete current `main` tree inventory | No source-bound MCP route, server allowlist or invocation audit was available to review | Absence from this repository tree does not prove absence in external tools, deployment configuration or another branch. Obtain exact configuration/source before asserting controls. **UNKNOWN** |
| Model/tool outputs | Provider response enters local adapter return value | Provider adapter is proposed; output validation/authorization remain separate gates | Output must remain untrusted data. No provider result grants tool capability or MediaHub state mutation. **INVARIANT** |

## 3. Key security conclusions

1. Provider credentials are currently evidenced in two distinct consumption patterns: local key files and process environment variables. A unified vault-backed, task-scoped resolution lifecycle is not evidenced by this source set.
2. Configurable destinations and credential-bearing requests need one enforced egress decision before request construction: task identity and issuer → data classification → approved provider/model and exact endpoint → authorization/lease → minimization → bounded request → sanitized audit.
3. Credential delivery should be task-scoped and provider-scoped. A qualification job should receive only the credential references/secrets needed for the provider(s) under qualification, rather than the entire provider inventory.
4. Credentials in URL query parameters are a log-exposure risk. Prefer provider-supported headers where available; if an API mandates query authentication, enforce URL redaction at every logging/proxy/trace boundary and keep the request path tightly bounded.
5. `base_url` / model-endpoint overrides require destination policy enforcement and explicit transport rules. A loopback default is not an allowlist for arbitrary overrides.
6. MCP server inventory, provider-connection routes, deployed environment values, vault selection and actual outbound network policy remain UNKNOWN; source inspection alone cannot establish runtime behavior.

## 4. Required next controls

- Bind credential references to task, issuer, audience, provider/model, lease, expiry and revocation under accepted A0/MH-12 contracts.
- Define R-06 data-classification and provider-routing authority; keep unknown data/destination combinations fail-closed.
- Add an explicit endpoint policy: canonical provider ID, normalized scheme/host/port/path, approved redirects, DNS/IP treatment, TLS requirements, timeout/body limits and audit-redaction rules.
- Partition qualification secrets by provider and workflow job; avoid passing unrelated credentials into a worker process.
- Inventory MCP servers, tool-call routes, provider connection endpoints and deployment configuration from exact source refs before admission.
- Treat returned content as untrusted; tool execution and canonical product-state mutation require separate authorization contracts.
- Require independent source-bound review and separately authorized qualification before runtime admission.

## 5. Disposition

- No technology or vault selected.
- No provider/MCP route accepted.
- No task-scoped credential broker or destination gate claimed implemented.
- OpenHands remains candidate-only; v0.2 task/registry/evidence schemas remain proposed-only.
- A0 issuer/ingress/lifecycle, MH-12, R-06, accepted target manifest and independent qualification remain open.
- No credentials, providers, MCP servers, tests, workflows, hosts or infrastructure were operated in this pass.
