# Astra PRE-SOAK evidence bundle

Astra may enter the 24-hour soak only after a fresh evidence bundle passes this gate.

Required files:

- `transport-health.json`
- `runtime-e2e.json`
- `scheduler-e2e.json`
- `fencing.json`
- `recovery.json`
- `backup-restore.json`
- `provider-model.json`

Every file must be JSON with `"status": "PASS"`.

Run:

```bash
python3 ops/qualification/verify_pre_soak_bundle.py ./evidence
```

The gate is deliberately evidence-only. It does not start, stop, migrate,
restart, or otherwise modify a live node.

A missing or non-PASS item blocks PRE-SOAK. Historical CI results do not satisfy
this gate unless they are copied into the bundle as fresh evidence for the
current deployment and remain independently verifiable.
