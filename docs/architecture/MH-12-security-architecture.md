# MH-12 — Security Architecture

**Status:** ARCHITECTURE COMPLETE / GOVERNANCE REVIEW REQUIRED

## 1. Purpose

Define the security authority model for MediaHub without introducing a second canonical mutation path.

## 2. Authority separation

Security controls:
- identity;
- authentication;
- trust;
- capability;
- authorization;
- policy enforcement;
- security boundaries;
- isolation/failure domains;
- secrets;
- compromise detection, containment and recovery.

Security does **not** own canonical state mutation. State Authority remains the sole canonical mutation authority.

## 3. Canonical request path

External/Input → Integration Boundary → Consumer Contract → Identity → Authentication → Trust → Capability → Authorization → Policy → Command/Proposal → Consumer Boundary → State Authority → Event → Audit/Observability.

A security-sensitive operation that does not receive explicit authorization must not reach canonical mutation.

## 4. Principal model

Canonical semantic principal classes:
- HumanPrincipal
- ServicePrincipal
- DevicePrincipal
- PluginPrincipal
- AIPrincipal
- WorkloadPrincipal
- RecoveryPrincipal
- UpdatePrincipal
- AuditPrincipal

Principal ≠ credential ≠ session ≠ capability ≠ authorization.

## 5. Identity

Identity lifecycle: enrollment → activation → suspension/revocation/expiration → recovery or re-enrollment. Identity does not imply privilege.

## 6. Authentication

Authentication answers “who are you?”. It establishes an AuthenticationContext but does not grant an operation. Exact technology is UNKNOWN until evidence and ADR.

## 7. Trust

Trust is explicit, contextual and revocable. Discovery, localhost, LAN reachability, VPN, signed package, authenticated user, administrator status, or cloud presence do not automatically establish unrestricted trust.

## 8. Capability

A capability is bounded by principal, issuer, operation, resource/target, scope, constraints, provenance, lifetime and revocation context. Capability attenuation may narrow authority but may not expand it. Capability cannot self-grant.

## 9. Authorization

Authorization is explicit, operation-specific, identity-bound, context-aware, policy-aware, auditable and fail-closed. Ambiguity resolves to DENY/appropriate safe containment. Authorization never bypasses Consumer Boundary or State Authority.

## 10. Human/service separation

Human and service principals remain distinct. Human privilege is not automatically inherited by services. Delegation, when required, must be explicit, bounded, auditable, revocable and time/context/capability constrained.

## 11. Plugins

Plugins are extensions, not authorities. No self-grant, wildcard privilege, direct State Authority access, unrestricted filesystem/network/subprocess, or Consumer Boundary bypass. Signature/provenance is not by itself runtime authorization.

## 12. AI

AI is treated as a potentially untrusted computational principal. Canonical path: AI → Recommendation/Proposal → Policy → Authorization → Command → Consumer Boundary → State Authority. AI confidence is not authorization. AI cannot self-authorize or grant itself capabilities.

## 13. Devices

Device lifecycle: Discovered → Untrusted → Verified → Enrolled → Authorized → Active, with Suspended/Quarantined/Revoked states. Presence ≠ authentication; authentication ≠ authorization; device trust ≠ State Authority.

## 14. Cloud and network

Cloud is external/untrusted by default. Network reachability ≠ trust. Localhost ≠ trust. VPN ≠ authorization. mTLS, if selected, authenticates a channel/peer but does not itself authorize operations. Physical topology, ports and segmentation are REQUIRES VERIFICATION.

## 15. Secrets and cryptography

Secrets lifecycle: Generate → Store → Use → Rotate → Revoke → Destroy. Secrets must not enter source, Git, ordinary logs, telemetry, diagnostic snapshots or AI prompts by default. Storage mechanism and cryptographic profile remain technology decisions requiring evidence and ADR.

## 16. Supply chain / update / recovery

Supply chain follows Source → Dependency → Build → Artifact → Sign → Registry → Deployment → Runtime. Updates require authenticated provenance, integrity, compatibility, version policy and health/recovery gates. Recovery is a separate security boundary. Neither update nor recovery identity automatically becomes unrestricted runtime authority.

## 17. Audit and observability

Audit records accountability: who, when, operation, target, capability, authorization/policy context and result. Observability reports security state. Diagnostics investigates. Neither observability nor diagnostics becomes mutation authority.

## 18. Incident response

Detect → Classify → Contain → Investigate → Eradicate → Recover → Verify → Close. Credential, plugin, AI, device, certificate, signing-key, update and privilege incidents require revocation/quarantine/containment as applicable.

## 19. Defense in depth

Identity → Authentication → Trust → Capability → Authorization → Policy → Boundary → Isolation → Validation → Resource limits → Cryptographic integrity → Audit → Observability → Incident response → Recovery.

## 20. Failure-domain invariant

Compromise of UI, plugin, AI, device adapter, cloud, observability, diagnostics, update or recovery environment must not automatically compromise State Authority or another protected domain.

## 21. Technology neutrality

JWT/OAuth/OIDC/RBAC/ABAC/capability-token formats/mTLS/PKI/Keychain/Vault/TPM/Secure Enclave/WireGuard/Tailscale/API gateway/IDS/IPS/SIEM and specific crypto libraries remain CANDIDATE/UNKNOWN until evidence + ADR + verification.

## 22. Acceptance boundary

This document records architecture, not production qualification. Acceptance requires traceability to MH-1…MH-11, compatibility with P0-03…P0-07, implementation evidence, negative security tests, verification evidence, contradiction resolution and governance approval.
