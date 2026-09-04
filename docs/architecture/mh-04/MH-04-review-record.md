# MH-04 Security / Trust / Authorization Foundation — Review Record

Date: 2026-09-04
Status: PROPOSED / REVIEW COMPLETE

## Architectural conclusion
MediaHub uses one governed authority path. Security establishes trust context, resolves principal identity, authenticates it, evaluates bounded capabilities and authorization/policy, and then permits or denies a command. A successful decision never grants direct mutation access. The command proceeds through the inherited Consumer Contract to State Authority, which alone performs canonical mutation; an event then records the fact.

## Subject classes
Human, service, device, integration, AI and cloud principals are distinct security subjects. Runtime services are bounded principals and are not elevated to State Authority merely by being local or trusted.

## Trust rule
T0..T5 are trust contexts, not automatic authorization grants. Reachability, VPN/network access, identity, authentication and authorization remain separate concepts.

## Failure rule
Ambiguous or malformed security context fails closed. Missing/invalid/expired/revoked authorization is denied. Unknown devices/identities may be quarantined. Recovery cannot create shadow authority. Cloud/AI failure does not relax local authorization and permits deterministic local degraded operation where safe.

## Non-mutation rule
Security events, logs, telemetry, health, diagnostics and quarantine state cannot become implicit mutation commands. Any operational response must re-enter the governed command path.

## Technology rule
No concrete IAM, authentication framework, secret store, network security product, sandbox technology or cloud security product is canonicalized by this review.

## Unresolved evidence
Hardware topology, exact Mac mini configuration, production deployment topology, physical persistence, HA/distributed architecture, final cloud/AI architecture, final AI architecture, final plugin sandbox, final UI technology, production security qualification and production update/recovery implementation remain unresolved/candidate as inherited.

## Governance
No parent decision was silently changed. Any conflict with a frozen parent requires `CONTRADICTION / GOVERNANCE CHANGE REQUIRED`. Review completion does not itself grant ACCEPTED or FROZEN status.