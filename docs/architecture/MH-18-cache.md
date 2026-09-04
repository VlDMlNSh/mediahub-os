# MH-18 — Cache
Status: PROPOSED / NOT ACCEPTED

Cache is bounded, disposable, rebuildable and non-authoritative. Cache entries require scope, key/version, size and expiry/invalidation semantics. Corruption or stale authorization causes invalidation, not fallback to trust. Cache must never be the sole canonical copy or bypass content access policy.