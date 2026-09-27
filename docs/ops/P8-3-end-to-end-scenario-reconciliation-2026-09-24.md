# P8.3 — End-to-end state scenario reconciliation

Status: SCENARIO_RECONCILIATION / P8.3 NOT CLOSED

## Scope

This artifact records deterministic evidence for normal, degraded, recovery and revoked/denied-authorization state surfaces already represented by the repository tests. It does not claim a production or external end-to-end run, and it does not treat health/reachability as authorization.

## Scenario matrix

- Normal: session lifecycle, bounded dispatch and authorized gateway paths are covered by existing tests.
- Degraded: provider/cluster degraded states are represented by existing routing, resilience and qualification tests; this artifact does not assert external outage behavior.
- Recovery: session/controller/delivery restore and provenance checks are covered by existing tests.
- Revoked or denied authorization: explicit authorization denial and safe-stop paths are covered; this artifact does not infer revocation semantics where only denial is tested.

## Closure

P8.3 remains OPEN until a deterministic acceptance surface ties these scenarios together as one executable cross-domain sequence.

## Source evidence


### tests/ai/test_hybrid_session.py
SHA256: cedd3186395d21112d6d3c253f94f94b22d80fe471c24add9a08483c85102d01
### tests/ai/test_hybrid_development_controller.py
SHA256: 452655c9ed75c604add6ac64205fd9129780b742e5357bd7e7073b7b24d8b691
### tests/ai/test_hybrid_dispatcher.py
SHA256: 9403654bc8fb58e6d177e8fe395d33ec4830d27ee2040280539c12d999ae7c72
### tests/ai/test_ai_gateway.py
SHA256: 2872fbcfc40b281911a6aeb0cf692e889120c4dae5e6d19a4574db20c70a69c1
### tests/runtime/test_mh04_qualification_edges.py
SHA256: d920a1a7e07c543d21c0449f76906824165e57153420f8a46d2c50e95050264b
### tests/security/test_mh05_health_not_authorization.py
SHA256: 8d7da0c6b6a9fdaedfa62b56715984af444640ffe357eb354348a2b335b4f393
