# MediaHub Prior-Art Ledger — Wave 03

Status: QUALIFIED FOR IMPLEMENTATION
Date: 2026-09-09

## Scope

Wave 03 establishes native security boundaries for autonomous development:
Credential Broker, Policy Engine, Egress Controller, and their composed gate.

## Design decisions

1. Credentials are references, never values, at the development adapter boundary.
2. Provider credentials are allowlisted by explicit provider identity.
3. Credential files must be regular files, bounded in size, and mode 0600-equivalent.
4. Policy is deterministic and deny-by-default for provider, protocol, data class,
   capabilities, timeout, and prompt size.
5. Production, secrets, state-authority, and host-filesystem capabilities remain denied.
6. Egress is explicit HTTPS destination allowlisting; query, fragment, and userinfo are denied.
7. Authorization and revocation are terminal fail-closed states for the boundary.
8. The composed boundary requires policy + egress + credential checks before admission.

## Prior-art inputs

- Bifrost: separation of routing/provider concerns and security-oriented controls.
- LiteLLM: provider credential abstraction and policy-aware routing concepts.
- OmniRoute: explicit provider registry and local-first gateway boundary.
- Firecracker: least-privilege isolation as an architectural constraint.

These projects remain reference material; no gateway or provider implementation was copied.

## Required qualification tests

- unauthorized access denied
- unknown provider denied
- broad credential permissions denied
- empty/symlink credential denied
- policy provider/protocol/data-class mismatch denied
- forbidden capability denied
- timeout/prompt bounds enforced
- non-HTTPS or URL data in egress policy denied
- unapproved destination denied
- global revoke denies subsequent work
- composed boundary denies if any constituent gate denies

## Non-goals

This wave does not authorize production gateway cutover, provider credential installation,
cloud E2E claims, or replacement of the existing OpenRouter lane. Native Codex/Claude
provider-neutral execution remains the next integration wave.
