# MediaHub OS — Provider Identity and Egress Contract Crosswalk, Wave 05

- Date: 2026-10-14
- Status: SOURCE-ANCHORED DOCUMENTARY RECONCILIATION / OPEN CONFLICTS / NOT ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED
- Governing baseline: accepted Functional Baseline 2.0; Baseline 1.0 remains historical unless separately accepted.
- Purpose: reconcile provider names, local/cloud semantics, route policy and evidence requirements without reading credentials, calling providers or changing runtime configuration.

## 1. Result

The primary architecture and registries do not currently describe FreeLLMAPI with a single unambiguous classification. The architecture text explicitly calls it a cloud-model provider path; both agent/provider registry metadata classify it as `local_gateway` / `local_gateway`-class and the provider fabric marks it `PENDING`. These statements could describe separate layers (a local gateway process forwarding to cloud providers), but the repository does not currently bind that interpretation to an immutable implementation/deployment identity. This remains an OPEN CONTRACT CONFLICT; do not silently edit either source to force agreement.

OmniRoute and UnoRouter are separate identities in the provider registry, with distinct credential-reference names. The agent registry also identifies `omniroute` as a transport/gateway rather than an agent. Similar naming is not evidence of equivalence to UnoRouter, OpenRouter, FreeLLMAPI, or a model/provider.

Local-only behavior is not optional: the distributed AI architecture and Jarvis draft both require fail-closed routing with no silent cloud fallback. This is a target invariant, not evidence that runtime routing already enforces it.

## 2. Source anchors

| Source | Blob SHA | Relevant statement | Evidence class |
|---|---|---|---|
| `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` | `e549692f207fbc91d9b9b9b92b8e665404f07290` | §1 describes FreeLLMAPI as a cloud-model provider path; §2/§4 show Claude Code → FCC → FreeLLMAPI and/or Alamo; §4 says topology is logical, not deployment proof; §7 requires local-only fail-closed behavior | Primary architecture intent |
| `profiles/providers/astra-gold-hybrid-agent-fabric.yaml` | `acf3ad43e68bf49ffa5a1d2c89f64bd363c0e181` | `unorouter` uses `UNOROUTER_API_KEY`; separate `claude` entry references `OMNIROUTE_API_KEY`; `freellmapi` is `local_gateway`, credential ref `local_key_file`, status `PENDING` | Provider registry declaration |
| `profiles/agent-registry.json` | `993cbbe1b2b2a88da7d8884a897b404f055981a8` | Separate `unorouter`, `freellmapi`, and `claude` entries; Claude record identifies gateway `omniroute`; transport/gateway classification says OmniRoute is not an agent | Agent registry declaration |
| `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md` | `e112cc73178eef5f71b8a814296e4902c2e80390` | §5 requires immutable route record and local-only fail-closed; §8 leaves provider classification open; §9 routing gate is OPEN | Proposed control-plane contract |
| `schemas/mediahub-component-evidence-record.schema.json` | `2e62a9d0174e2c72e23ac88edc3094d13b4e336a` | Draft fields support egress policy, provider identity, evidence and separate qualification/release/acceptance statuses | Proposed evidence schema |

## 3. Provider identity crosswalk

| Stable logical identity | Declared role | Observed local evidence from Wave 02 | Current status | Do not infer |
|---|---|---|---|---|
| `freellmapi` | Architecture: cloud-model/provider path. Registry: `local_gateway`, `PENDING` | No process/service identified by bounded checks on the two online nodes | CONFLICT / NOT PROVEN | That it is necessarily a cloud-hosted service, necessarily local, or deployed at all |
| `omniroute` | Transport/gateway referenced by Claude provider entry | macOS CLI v3.8.50 present; connectivity not tested; no bounded Linux executable match | CLI PRESENT / ROUTE NOT PROVEN | Authentication success, upstream provider identity, or equivalence to OpenRouter/UnoRouter |
| `unorouter` | Separate provider/gateway registry identity | No runtime call; local presence/connectivity not established in Wave 02 | DECLARED / NOT PROVEN | That UnoRouter is OmniRoute or that the names are aliases |
| `fcc` | Required Claude Code integration/control layer | No standalone `fcc` command identified in bounded inventory | IMPLEMENTATION MAPPING UNKNOWN | That no library/container/service integration exists |
| `ollama` | Local inference runtime | Linux service active and model tags listed; macOS CLI present but daemon unavailable | LINUX SERVICE PRESENT / NOT QUALIFIED; MACOS SERVER UNAVAILABLE | Model provenance, client compatibility, secure endpoint or successful inference |
| `alamo` | Logical name for intended local inference endpoint | No exact deployment identity bound to Ollama in evidence | TARGET / IDENTITY NOT PROVEN | That Alamo is simply an alias for a specific Ollama process or that the intended Mac Pro endpoint is active |
| `claude-code` | Engineering client/agent surface | CLI version observed on both online nodes | CLI PRESENT / ACTUAL ROUTE UNKNOWN | That a hosted Claude model processed a task or that the client is routed locally |

## 4. Required route decision record

Before every task dispatch, the proposed control plane must persist a revision-bound, immutable route decision with at least:

- `mission_id`, `task_id`, `policy_revision`, `configuration_revision`, and creation time;
- task purpose/classification and data sensitivity;
- `egress_mode`: `local_only`, `approved_hybrid`, or `approved_cloud`;
- explicit allowed destinations/provider identities and denied destinations;
- selected executor, transport/gateway identity, upstream provider identity and exact model identity/digest where available;
- locality boundary for every hop (client, gateway, upstream provider), not merely the gateway's location;
- auth principal/capability reference (identifier only, never secret), budget/quota ceiling and authorization decision;
- fallback rule and reason; local-only fallback must be `none`;
- result provenance and redacted evidence references;
- terminal disposition: executed, held, rejected, failed, or cancelled.

If any required route identity, locality, egress permission or model/provider provenance is unknown, the route is not eligible for dispatch under local-only mode. It must hold/fail closed, not broaden permissions.

## 5. Decision options for the unresolved FreeLLMAPI classification

These are analysis options, not accepted owner decisions.

### Option A — Local gateway, cloud upstream (recommended as the first hypothesis to verify)

Interpret `local_gateway` as the process's deployment location and the architecture's “cloud provider path” as its upstream. This reconciles the words without changing either source, but only if immutable deployment/source evidence proves a local service and identifies every upstream/egress hop.

Consequences: the registry must eventually distinguish `gateway_location=local` from `upstream_class=cloud_provider`; local-only mode must exclude this route unless its upstream is also local and egress-free. Provider and model identities must be emitted separately.

### Option B — Provider is cloud-hosted; registry classification is stale/wrong

This requires source evidence that FreeLLMAPI is not a local gateway in the deployed topology and a reviewed registry correction. Do not change the registry based only on the architecture wording.

Consequences: route egress is cloud; local-only must deny it; credentials and data-transfer policy require explicit cloud authorization.

### Option C — Distinct local gateway and upstream provider identities

Split the current overloaded `freellmapi` record into stable gateway and upstream identities, preserving the historical ID as an alias/compatibility reference with an explicit deprecation mapping. This is the cleanest normalized contract if implementation evidence confirms two distinct components, but it is a schema/registry change requiring owner/governance review.

Consequences: no hidden gateway/upstream conflation; stronger route evidence and policy enforcement; migration and historical-ID collision checks required.

**Recommendation:** retain the conflict and verify source/deployment identity before selecting A, B or C. No owner decision is implied.

## 6. Project-wide matrix row additions required

For every provider/gateway/model/runtime component, the unified traceability matrix should separate:

1. stable logical ID and historical aliases;
2. component kind: client, executor, local runtime, gateway/transport, upstream provider, model;
3. source/package/release identity and digest;
4. actual deployment node/location for each hop;
5. upstream destination and data-egress class;
6. supported protocol/API and compatibility evidence;
7. authentication principal/capability and secret reference identifier only;
8. model identity/digest/license/provenance where applicable;
9. route eligibility by data class and privacy mode;
10. fallback policy, quota/budget limits and outage behavior;
11. runtime observation, functional verification, qualification, release and acceptance as separate states;
12. immutable evidence URI/digest, captured time and independent reviewer.

Do not overwrite or renumber existing historical component IDs. New identities require an explicit alias/deprecation map and collision review.

## 7. Invariants preserved

- Product State Authority remains the sole canonical product-state writer.
- ASTRA A0 remains the sole writer of ASTRA-internal queue/claim/lease/heartbeat/gate state under its accepted contract.
- Jarvis submits bounded missions and consumes evidence; it does not write ASTRA queue internals or self-approve.
- GitHub Adapter is constrained by least-privilege repository, branch, path and operation capabilities.
- Local-only is fail-closed and never silently falls back to Anthropic, OmniRoute, FreeLLMAPI or another cloud route.
- No provider calls, credential reads, tests, qualification, installation, host changes, merge, release or deployment were performed in this pass.

## 8. Next bounded step

Inspect non-secret repository source/configuration history and deployment descriptors to identify exact FreeLLMAPI, OmniRoute, UnoRouter and FCC implementation identities; separately reconcile historical PASS artifacts to exact gate ID, target SHA, workflow/run ID, artifact digest and independent verifier. Do not infer missing evidence or run providers to fill gaps. Keep this document and the unified matrix PROPOSED until the domain owners/governance accept the resolution.
