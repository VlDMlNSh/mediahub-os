# MH-5 — Plugin Boundary

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

Plugins are capability-scoped consumers/integrations, not authorities. Capabilities must be explicit; wildcard authority and self-grant are prohibited.

Plugin output is data/proposal until validated and explicitly authorized. A plugin cannot directly mutate P0-04, bypass P0-05, create persistence, execute arbitrary policy code, or derive new capabilities from its own output.

The full plugin subsystem, grant lifecycle, installation/update trust chain, and exact capability inventory remain separate governance decisions. P0-07's inert plugin proposal boundary is inherited as a baseline, not expanded implicitly by MH-5.
