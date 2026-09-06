# MH-05 Evidence Format Note — non-self-referential execution identity

This note records the evidence-format correction for MH-05.

The implementation baseline is the stable provenance reference. Individual GitHub Actions runs are immutable execution records and must be evaluated using the exact revision recorded by the workflow itself. The evidence artifact must not copy a mutable `current HEAD` value into the same branch, because a documentation commit necessarily changes HEAD and would make that field immediately stale.

Current qualification remains OPEN. Automated execution is not independent security qualification. Persistence, HA, recovery expansion, production release, and unrelated capabilities remain unauthorized.
