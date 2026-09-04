# MH-12 Security Boundaries

Boundaries cover State Authority, Core Runtime, local services, UI, API/CLI, plugins, device adapters/devices, AI, automation, cloud/internet, updates, recovery, diagnostics, development/CI/CD, registries, operators and emergency operators.

Rule: every crossing requires explicit identity, authentication, trust, capability, authorization and applicable policy; data and requests remain non-authoritative until authorized. Network reachability, localhost, LAN, VPN, authentication, signatures or installation do not independently establish runtime trust.

Failure: deny, quarantine or safe degradation according to operation. No boundary may create a second State Authority.
