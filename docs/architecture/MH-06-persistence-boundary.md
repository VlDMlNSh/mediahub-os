# MH-06 — Persistence Boundary

Status: PROPOSED / PHYSICAL PERSISTENCE NOT AUTHORIZED.

Runtime services must not create hidden canonical persistence. SQLite, Redis, PostgreSQL, arbitrary files, durable checkpoints and queues are not canonical state stores under MH-6.

Runtime cache is permitted only as explicitly non-authoritative, bounded representation. P0-04 remains persistence-neutral and the physical persistence implementation is outside MH-6 authority.
