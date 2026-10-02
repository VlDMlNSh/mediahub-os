# MH-25 / ASTRA GOLD unified qualification trigger

This non-secret contract triggers qualification of the complete ASTRA GOLD distributed autonomous development system.

Scope:
- system: ASTRA GOLD
- node: mh-dev-01
- controller: mh-dev-02
- coordination: A0 Astra
- roles: A1 Architect / A2 Builder / A3 Verifier
- autonomous controller: command + claim + queue + heartbeat + recovery
- executors: Codex / Claude Code
- transports: FCC / OmniRoute
- auxiliary: ECC, authority none
- qualification mode: whole_system
- minimum executor rounds: 23 per mandatory path
- mandatory paths: Codex/FCC, Claude/FCC, Codex/OmniRoute, Claude/OmniRoute
- concurrency: 2 disjoint claims
- independent verification: A3 required
- 24h soak: mandatory before GOLD_ACTIVE
- fail-closed: true
- historical evidence reuse: false

No credentials are stored here.
