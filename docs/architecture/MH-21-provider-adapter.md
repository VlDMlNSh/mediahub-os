# MH-21 Provider Adapter

Status: PROPOSED.

MediaHub → External Compute Contract → Provider Adapter → Provider API. Adapter isolates provider-specific protocol, SDK, errors, streaming, limits and authentication. Canonical domain models must remain provider-neutral unless an ADR explicitly approves coupling.