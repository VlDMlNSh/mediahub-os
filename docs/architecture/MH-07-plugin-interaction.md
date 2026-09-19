# MH-07 — Plugin Interaction

Status: CANDIDATE.

Plugins may propose, validate and observe through bounded interfaces. They cannot self-grant, request wildcard capability, mutate State Authority directly, modify authorization rules, replace Policy Engine or replace State Authority.

Plugin grants are explicit data and require an independently governed grant path. Dynamic grant/revoke and executable policy loading are outside v1.

Existing P0-07 PluginCapabilityGrant/InertProposal are boundary evidence; production qualification is not inferred.
