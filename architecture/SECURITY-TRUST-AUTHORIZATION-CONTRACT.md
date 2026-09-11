# MediaHub OS — Security / Trust / Authorization Contract

Date: 2026-09-11
Status: PROPOSED ARCHITECTURAL BASELINE

## Governing rule

Security is a prerequisite to command execution, not an observer after mutation. No UI, AI, plugin, device, cloud service or integration may mutate canonical state without passing the same identity, trust, authorization and State Authority path.

## Trust chain

```text
Boot / Runtime Trust Context
    -> authenticated principal
    -> device / workload identity
    -> capability and policy evaluation
    -> authorized command
    -> Consumer Contract
    -> State Authority
```

Authentication proves identity. Authorization determines whether that identity may perform the requested operation. Neither authentication nor readiness is itself mutation authority.

## Identity classes

MediaHub must distinguish at minimum:

- human/user principal;
- MediaHub device principal;
- service/workload principal;
- automation/agent principal;
- external integration principal.

Each principal must have a stable identity, bounded credentials/capabilities and an auditable lifecycle.

## Authorization invariants

- default deny;
- least privilege;
- explicit capability/scope;
- resource and operation checks occur before mutation;
- stale or revoked credentials are rejected;
- unknown device identity is denied or quarantined;
- authorization failure never falls back to a broader role;
- emergency/recovery operations use explicitly defined capabilities, never wildcard authority;
- AI recommendations are never authorization decisions by themselves.

## Device trust

A device is not trusted merely because it is reachable on a local network. Enrollment, identity verification, credential rotation, revocation and quarantine must be explicit MediaHub lifecycle operations.

## Secrets

SOPS + age remain the selected secret-protection primitives. Production plaintext secrets must not be committed to Git, embedded in source, emitted into unrestricted telemetry or exposed to components that do not require them.

## Audit

Security-relevant operations must produce an auditable fact containing, as applicable:

- principal identity;
- device/workload identity;
- command identity;
- target/resource identity;
- authorization decision;
- policy/version identifier;
- timestamp;
- correlation/trace identity;
- resulting canonical revision when mutation occurs.

Audit records are evidence/facts and do not become a second State Authority.

## Failure behavior

| Failure | Required behavior |
|---|---|
| unknown identity | deny/quarantine |
| invalid credential | deny |
| revoked credential | deny |
| insufficient capability | deny |
| ambiguous policy result | fail closed |
| authorization service unavailable | deny mutation unless a previously defined, bounded local policy is explicitly authorized |
| secret unavailable | affected capability unavailable; no insecure fallback |
| compromised/unknown device | quarantine and prevent mutation |

## Observability boundary

Logs, metrics and traces may record security evidence but must not expose credentials, private keys or unrestricted authentication material. Telemetry cannot authorize or mutate state.

## Supply-chain boundary

Release artifacts must pass the existing SBOM, signature and vulnerability gates. Cosign verifies artifact authenticity; Syft provides SBOM evidence; Trivy provides vulnerability/security scanning evidence. These tools do not define MediaHub release authority; they provide evidence consumed by MediaHub release policy.

## Acceptance gates

1. valid principal + authorized command;
2. valid principal + unauthorized command;
3. unknown principal;
4. revoked credential;
5. unknown device;
6. device quarantine;
7. credential rotation;
8. policy ambiguity;
9. security dependency outage;
10. audit evidence completeness;
11. secret-leakage checks;
12. AI/plugin/cloud attempted authority bypass;
13. release artifact signature/SBOM/scan verification.
