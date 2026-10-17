# OSS adapter boundary

Every adapter MUST expose only a MediaHub-owned contract.

Required properties:
1. explicit capability identifier;
2. upstream version/provenance;
3. input/output contract;
4. timeout/resource limits;
5. authorization context;
6. audit/provenance linkage;
7. deterministic failure mapping;
8. degraded-mode behavior;
9. shutdown/restart behavior;
10. rollback/replacement path.

Forbidden:
- direct State Authority mutation;
- hidden persistence;
- hidden network egress;
- unbounded subprocess execution;
- upstream schema becoming a MediaHub public contract;
- bypass of authorization or release gates.

## Optional orchestration adapters

`runtime/mediahub_runtime/oss_adapters/orchestration.py` provides a bounded
LangGraph task-envelope validator, an explicitly invoked Temporal client
connector, and an OpenTelemetry span helper. The validator rejects malformed
correlation IDs, custom payload objects, and oversized/deep JSON-like payloads.
These are opt-in adapters, not a replacement queue, state authority,
authorization system, or qualification verifier. Importing the module performs
no network calls and starts no workers.

Install into an isolated environment using
`oss/manifests/python-requirements-oss.txt`. The Linux/Python 3.12 transitive
lock is recorded in `oss/manifests/python-linux-py312.lock`. Rebuild the lock
when platform or Python version changes; do not treat it as a cross-platform
lock. Temporal stays disconnected unless `ASTRA_TEMPORAL_ENDPOINT` is set and a
caller explicitly invokes `connect_temporal`. No production workflow should be
routed through these adapters until separate integration and qualification
checks pass.
