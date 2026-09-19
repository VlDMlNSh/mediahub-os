# MH-07 — Configuration / Policy Architecture v0.1

Status: CANDIDATE — governance acceptance/freeze not granted.

Configuration describes desired behavior. Policy evaluates whether an operation is permissible under declared conditions. Authorization determines whether a principal may perform the concrete operation. Runtime State records what is actually true. P0-04 State Authority remains the only canonical mutation authority.

Canonical path: Proposal → validation → policy evaluation → independent authorization → P0-05 Consumer Boundary → P0-04 transaction → atomic commit → runtime application → observed state.

v1 is device-local, transient, bounded, declarative and non-executable. No tenant/project/fleet/cloud canonical scope; no hidden inheritance, merge, priority, LWW, retry or rebase.

P0-03…P0-06 remain frozen baselines. P0-07 mutation publication remains blocked by the documented authorization/API gap.
