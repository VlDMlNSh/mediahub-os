# MH-5 — External Service Boundary

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

Cloud services, remote APIs, external compute, and internet services are external/untrusted by default. Encrypted/authenticated transport, VPN, Tailscale, WireGuard, or mTLS establishes transport properties, not State Authority.

External services may exchange bounded requests, proposals, events, or authorized read representations. They cannot become canonical state owners, self-grant capabilities, bypass P0-05, or establish persistence through the consumer path.

Remote failure, partition, timeout, or replay must fail according to the operation's explicit delivery semantics. No hidden synchronization, merge, LWW, or automatic recovery is implied.
