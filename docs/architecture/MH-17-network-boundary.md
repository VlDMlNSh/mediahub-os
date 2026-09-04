# MH-17 — Network Boundary

**Status:** CANDIDATE

Device connectivity is a separate trust zone. LAN, VLAN, isolated networks, Wi-Fi, Ethernet, Bluetooth, USB, WAN and cloud relay are transport/topology contexts, not authorization domains.

Invariants:
- network reachability ≠ authorization;
- VPN ≠ trust;
- TLS ≠ application authorization;
- inbound connectivity does not create control capability.

Adapters must use explicit network/interface scopes and bounded resources. Firewall/port/VLAN changes are outside this document's implementation authority and require separate security/governance approval.

**UNKNOWN:** actual MediaHub deployment topology and firewall policy.