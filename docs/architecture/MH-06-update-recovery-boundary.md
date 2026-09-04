# MH-06 — Update / Recovery Boundary

Status: PROPOSED

Separate runtime restart, application update, host update, data migration, security update and recovery. No update mechanism may silently change the runtime authority model.

Rollback must be explicit, authorized and auditable. Firmware update, secure wipe, restore-over-existing-data and other destructive/critical actions remain outside autonomous runtime recovery and require the appropriate governance/operator gate.
