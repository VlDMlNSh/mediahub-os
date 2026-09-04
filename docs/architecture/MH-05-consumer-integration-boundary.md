# MH-5 — Consumer / Integration Boundary

**MEDIAHUB OS 11.x LTS / MEDIAHUB iOS**

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED
**Implementation:** NOT AUTHORIZED
**Branch:** `architecture/mh-05-consumer-integration-boundary`

## 1. Purpose

MH-5 defines the canonical boundary through which UI, APIs, CLI, voice, AI, automation, plugins, diagnostics, device/protocol adapters, management clients, internal services, future SDKs, cloud services, and unknown external sources interact with MediaHub Core.

The boundary preserves one canonical mutation authority: P0-04 State Authority. P0-05 remains the mandatory consumer/integration mediation boundary. MH-5 adds architectural semantics around that frozen contract; it does not redefine P0-03/P0-04/P0-05/P0-06.

## 2. Evidence baseline

The following evidence is inherited, not reconstructed:

- P0-04 governance commit `0621009bc444c2d6ef8aaf1170a22a2284e38fa6` explicitly accepts/freezes the in-memory State Authority, with persistence and production/appliance integration excluded.
- P0-05 governance commit `97a01977f521ba8304a455b5d7504896235ddea7` explicitly accepts/freezes the Consumer Boundary around P0-04. It records implementation commit `303a766257b90c4356dcffc8967a5574e8e22e7a`, 10/10 targeted tests, 136/136 full regression, capability/persistence scans, exact HEAD, clean worktree, and synchronized branch.
- P0-06 governance commit `f0e1e7898337c3f6718a8b7fa63cd12885292ddf` explicitly keeps P0-04/P0-05 frozen and records 12/12 targeted tests and 148/148 full regression.

The repository copy of P0-03 inspected on the P0-05 implementation branch is currently marked `Contract Draft / Controlled Implementation Gate`; therefore the MH-5 evidence register must distinguish repository-observed document state from the separately supplied governance baseline. No historical status is upgraded merely because a later architecture depends on it.

## 3. Canonical boundary

```text
External / UI / AI / Plugin / Device / API / Service
                         |
                         v
              Integration Boundary
                         |
                         v
                  Consumer Contract
                         |
                         v
            Identity + Capability Context
                         |
                         v
                Authorization / Policy
                         |
                         v
                P0-05 Consumer Boundary
                         |
                         v
                P0-03 / P0-04
                 State Authority
                         |
                         v
                    Domain Event
                         |
                         v
                    Observers
                         |
                         v
               Future Persistence Contract
```

Transport is not the authority boundary. HTTP, gRPC, WebSocket, MQTT, Unix sockets, brokers, VPNs, Tailscale, WireGuard, mTLS, or any future transport remain implementation details unless separately governed.

## 4. Authority rule

A consumer may request, propose, observe, normalize, or transform data. It never becomes owner of canonical runtime state merely because it is authenticated, local, privileged, connected, or technically capable of sending a request.

Only an explicitly authorized operation may become a command. Only State Authority may publish canonical mutation.

## 5. Semantic separation

The following distinctions are normative:

- input ≠ command;
- command ≠ authorization;
- authorization ≠ State Authority;
- event ≠ command;
- proposal ≠ execution;
- observation ≠ mutation;
- discovery ≠ trust;
- authentication ≠ authorization;
- reachability ≠ trust;
- admin identity ≠ unrestricted authority.

## 6. Canonical request path

```text
input
 → classify / validate / bound
 → identify caller
 → resolve explicit capability
 → authorize operation and target
 → construct command or inert proposal
 → P0-05 mediation
 → P0-04 State Authority transaction where mutation is required
 → atomic publication or fail-closed rejection
 → bounded result / event
```

A proposal cannot skip command conversion and authorization. An event cannot be interpreted as a command. A read cannot expose mutable internals.

## 7. Consumer classes

| Consumer | Default role | Mutation authority | Trust default |
|---|---|---:|---|
| UI | read/request | none | authorized local consumer |
| API client | request/read | none | external until authorized |
| CLI | request/read/admin request | none | authorized local consumer |
| Voice | input/proposal/request | none | untrusted input |
| AI | proposal/recommendation | none | untrusted execution environment |
| Automation | proposal/request | none | explicitly scoped service |
| Plugin | proposal/integration | none | capability-scoped untrusted |
| Diagnostics | observe/report | none | observation-only |
| Device adapter | normalize/observe/request | none | untrusted until enrolled |
| Protocol adapter | normalize/translate | none | untrusted until verified |
| External service | request/event exchange | none | external/untrusted |
| Cloud | external compute/service | none | external/untrusted |
| Management tool | privileged request | none | privileged but bounded |
| Future SDK | contract consumer | none | explicit capability only |
| Internal service | service consumer | none | identity and capability required |
| Test harness | controlled verifier | none | test-only authority context |
| Unknown source | data only | none | deny/untrusted |

## 8. Trust zones

1. **Trusted Core:** State Authority and explicitly trusted core runtime components.
2. **Authorized Local Service:** identified service with explicit capabilities.
3. **Local Consumer:** UI/CLI/management client subject to authorization.
4. **Integration Zone:** plugins, adapters, automation, device/protocol boundaries.
5. **AI/External Compute Zone:** AI agents and cloud/external compute.
6. **Remote/External Zone:** remote APIs and services.
7. **Unknown Zone:** undiscovered, unauthenticated, malformed, or unverified sources.

Trust is explicit, scoped, revocable, and operation-specific. Network locality does not elevate a zone.

## 9. Persistence boundary

No MH-5 consumer path creates persistence. Cache, export, index, content metadata, knowledge graph, digital twin, or diagnostic records do not become canonical runtime state by implication. Future durable storage remains behind a separate Persistence Contract and governance gate.

## 10. Security invariants

MH-5 adopts the required invariants: single mutation authority, no hidden escalation, default deny, no self-grant, no wildcard authority, no mutation from observation, no execution from proposal, no authority from identity/authentication alone, operation-specific authorization, bounded processing, fail-closed boundary violations, unknown capability/caller/device denial, external-service exclusion from Core authority, and no persistence side-channel.

## 11. Status

This document is an architectural baseline candidate. It is **PROPOSED**, not ACCEPTED or FROZEN. Acceptance requires evidence reconciliation, contradiction closure or explicit disposition, security review, and governance decision.
