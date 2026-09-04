# MH-21 Trust Model

Status: PROPOSED / security semantics require MH-12 evidence.

T0 Core Trusted Domain: State Authority and critical security/runtime primitives.
T1 Authorized Local Services.
T2 Local AI/Compute.
T3 Local Integrations.
T4 Remote Compute: cloud GPU, remote AI, RAG, agents, inference workers.
T5 External Providers: model APIs, SaaS, external data.
T6 Untrusted External World.

Trust is distinct from identity, authentication, authorization, capability and network reachability. VPN, WireGuard, Tailscale and mTLS do not independently grant business authorization.

Default rule: external compute is untrusted data-producing infrastructure until separately evaluated and authorized.
