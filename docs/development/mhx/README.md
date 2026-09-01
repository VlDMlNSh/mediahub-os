# MHX — MediaHab Local Orchestrator Skeleton v1.0

MVP execution infrastructure for manifest/index/chunk/task/result/cache/status workflows.

## Boundary

MHX is execution infrastructure only. It cannot create VAL records, make governance decisions, approve a baseline, or establish historical equivalence.

## Quick start

```bash
python3 tools/mhx.py init
python3 tools/mhx.py manifest .
python3 tools/mhx.py index
python3 tools/mhx.py chunk --lines 80
python3 tools/mhx.py status
```

The orchestrator keeps the operational state under `.mhx/`; the repository working tree remains the source being indexed. Worker outputs must enter through Result Packs and review before integration.
