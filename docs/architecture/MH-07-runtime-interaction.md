# MH-07 — Runtime Interaction

Status: CANDIDATE.

Runtime consumes only validated and independently authorized representations. Configuration never directly mutates Runtime State. Policy evaluation never mutates Runtime State. Canonical mutation remains Consumer Boundary → State Authority.

Path: candidate → validation → policy → authorization → P0-05 → P0-04 transaction → commit → runtime application → observed state.

Runtime may report incompatibility/application failure; it cannot silently reinterpret unauthorized configuration or create an alternate mutation/persistence channel.
