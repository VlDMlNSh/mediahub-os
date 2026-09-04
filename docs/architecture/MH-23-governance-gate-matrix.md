# MH-23 Governance Gate Matrix

| Gate | Required evidence | Decision |
|---|---|---|
| Architecture | contract + compatibility + ADR | Governance approval |
| Implementation | explicit implementation authorization | separate from architecture |
| Verification | exact target + reproducible tests/scans | pass required |
| Qualification | functional/security/privacy/resource/recovery evidence | pass required |
| Release | artifact provenance/digest/SBOM | approval |
| Migration | preflight/validation/rollback/evidence | promote only on pass |
| Production | qualification + operational readiness | governance state |
| EOL | migration/disposition/privacy/security evidence | explicit closure |

No gate is inferred from another gate.