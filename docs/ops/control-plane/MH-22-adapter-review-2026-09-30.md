# MH-22 adapter review — 2026-09-30

Status: CANDIDATE COMMANDS IDENTIFIED; NO ADAPTER APPROVED.

Candidate: f792f96179bc1e61646a472781f980b919c09bc7
Executor: mh22-qualification-executor 1.0.0

A repository test is evidence only. It becomes an adapter only after review confirms deterministic execution, exact-candidate scope, isolation, reproducible evidence, and complete semantic coverage of the corresponding MH-22 pass.

Candidate commands:
P1: python -m pytest tests/contracts/test_contract_domain_reconciliation.py
P2: python -m pytest tests/runtime/test_state_authority.py
P3: python -m pytest tests/runtime/test_mh04_source_identity.py
P5: python -m pytest tests/security/test_mh04_state_authority_redteam.py
P13: python -m pytest tests/runtime/test_state_authority.py tests/runtime/test_mh05_restore.py
P16: python -m pytest tests/ai/test_ai_gateway.py tests/ai/test_ai_routing.py tests/ai/test_ai_model_capability.py
P20: python -m pytest tests/contracts/test_mobile_api_compatibility.py tests/runtime/test_mh05_event_projection.py
P21: python -m pytest tests/runtime/test_mh05_restore.py tests/security/test_mh05_restore_reachability.py

All eight are CANDIDATE / PARTIAL, not approved.

P4 P6 P7 P9 P11 P12 P14 P15 P17 P18 P19 P22 P23 remain evidence gaps.

Critical executor constraint: the current executor converts adapter exit code zero directly to PASS. Therefore partial candidates must not be registered in the manifest, because that would incorrectly create qualification PASS.

Next safe action: extend the evidence contract/executor to represent PARTIAL evidence explicitly, or obtain reviewed full-domain adapters before registration.
