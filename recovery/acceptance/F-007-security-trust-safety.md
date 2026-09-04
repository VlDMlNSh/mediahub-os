# MediaHub — F-007 Security / Trust / Safety

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED

## Functional requirements

### General security
- MediaHub protects devices, users, local network, remote access, data, automations, clusters, integrations and Developer infrastructure.

### Trust model
- MediaHub distinguishes discovered, identified and trusted devices.
- MediaHub distinguishes authenticated/authorized users from mere presence.
- MediaHub distinguishes trusted MediaHub nodes, trusted cluster nodes, Developer MediaHub and cloud infrastructure.
- Discovery does not imply trust.

### Device onboarding security
- New equipment is discovered and identified where possible before being trusted.
- MediaHub determines an appropriate integration/trust path and can safely isolate unknown or untrusted equipment until understood.

### Remote access
- MediaHub User App supports remote operation.
- Remote access uses a protected access mechanism.
- Remote operation does not grant privileges beyond those assigned to the corresponding user/account.

### Developer access
- MediaHub Developer App is a distinct privileged application class.
- Developer App has a separate elevated authorization model.
- The single designated MediaHub Developer is a distinct privileged/trusted MediaHub instance.
- Developer privileges are not automatically granted to ordinary MediaHub instances or ordinary User Apps.
- Developer capabilities include authorized access to cloud development, distributed compute, developer tooling, engineering infrastructure and advanced diagnostics.

### Automation safety
- Automations cannot bypass authorization, security policies or safety constraints.
- Additional confirmation/authorization may be required for critical operations such as locks/access systems, security systems, high-risk electrical/energy actions, network infrastructure, destructive data operations, firmware operations and cluster/system changes.

### Isolation
- Unknown or insufficiently trusted devices/integrations can be kept isolated until their identity and behavior are sufficiently understood.

### Auditability
- Security-relevant actions maintain traceability of Actor → Authentication → Authorization → Action → Result.
- Remote actions additionally maintain Remote App → Secure Session → User → Authorization → MediaHub → Action → Result.

## Explicitly deferred technical decisions

1. Remote-access protocol.
2. VPN and transport security details.
3. TLS, keys and certificates.
4. Passwords, passkeys and biometric mechanisms.
5. MFA.
6. Trust enrollment and trust anchors.
7. Cluster trust model.
8. Developer MediaHub trust model.
9. Cloud Development authentication.
10. Emergency access and recovery.
11. Threat model.
12. Security levels.
13. Exact safety classes and confirmation policy.
