# MH-18 — Plugin Interaction
Status: PROPOSED / NOT ACCEPTED

Plugins may provide codec adapters, metadata providers, importers/exporters, provider integrations and analyzers. Capability scopes must be explicit. Plugin ≠ Content Authority and plugin ≠ State Authority. Plugin input/output is data until authorized. No unrestricted filesystem, network, secrets or media-library access.