# MH-18 — Backup / Recovery
Status: PROPOSED / NOT ACCEPTED

Treat media bytes, canonical metadata, configuration, indexes and derivatives separately. Indexes/derivatives are rebuildable where possible. Restore gate: Integrity → Compatibility → Authorization → State/Storage Restore → Validation → Health Gate. Backup existence is not proof of recoverability; restore tests are required evidence.