# MH-03 Runtime Dependencies

Dependency classes:
1. Mandatory foundation: State Authority and required Core Runtime Services.
2. Required-for-feature: dependencies needed only by a particular capability.
3. Optional/external: cloud, AI, external knowledge and nonessential integrations.

Rules:
- dependency readiness is not authorization;
- dependency ordering must be deterministic;
- cycles are configuration/architecture errors and block readiness;
- optional dependency loss must not force unsafe fallback;
- no dependency may silently become canonical state authority.

Concrete orchestration technology remains CANDIDATE.
