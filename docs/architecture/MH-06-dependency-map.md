# MH-06 — Dependency Map

Status: PROPOSED / REQUIRES VERIFICATION

Core dependency chain:
MH-1 governance -> MH-2 boundaries -> MH-3 runtime foundation -> MH-4 state/security/trust/authorization -> MH-5 consumer/integration boundary -> P0-03 State Authority -> P0-04 implementation -> P0-05 Consumer Boundary -> P0-06 Core Runtime -> P0-07 Configuration/Policy.

Runtime mutation path remains P0-06 -> P0-05 -> P0-04. P0-07 remains an input/policy dependency and its unresolved mutation-publication gap is not bypassed by MH-6.

Critical dependency cycles require explicit ADR.
