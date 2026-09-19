# MH-07 — Proposal Boundary

Status: CANDIDATE.

Proposals from UI, CLI, AI, automation, plugins, diagnostics, adapters or external services are inert inputs. Proposal acceptance validates bounds/provenance but does not publish state.

A proposal cannot grant capabilities, invoke executable policy, dereference opaque references, persist itself or mutate State Authority. It follows the same validation → policy → authorization path as other requests.

Existing P0-07 proposal/plugin boundary is the implementation baseline. Autonomous execution is prohibited.
