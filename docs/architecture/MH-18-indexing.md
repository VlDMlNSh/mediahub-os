# MH-18 — Indexing
Status: PROPOSED / NOT ACCEPTED

Canonical Catalog → Index Builder → Search Index. Index is DERIVED, REBUILDABLE and NON-AUTHORITATIVE. Builders consume canonical read models, use bounded work and versioned schemas. Corrupt/stale index is invalidated and rebuilt; it cannot mutate or replace canonical catalog.