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
