import pytest
from mediahub_runtime import LineageError, TaskEvidenceLineage, sha256_json


def test_lineage_is_deterministic():
    contract = {"request_id": "r1", "b": 2, "a": 1}
    evidence = {"status": "PASS", "bytes": 4}
    first = TaskEvidenceLineage.create("r1", contract, evidence)
    second = TaskEvidenceLineage.create("r1", {"a": 1, "b": 2, "request_id": "r1"}, evidence)
    assert first == second
    assert first.verify(contract, evidence)
    assert len(first.lineage_sha256) == 64


def test_lineage_detects_contract_tamper():
    lineage = TaskEvidenceLineage.create("r2", {"request_id": "r2", "value": "x"}, {"status": "PASS"})
    assert not lineage.verify({"request_id": "r2", "value": "y"}, {"status": "PASS"})


def test_lineage_detects_evidence_tamper():
    lineage = TaskEvidenceLineage.create("r3", {"request_id": "r3"}, {"status": "PASS"})
    assert not lineage.verify({"request_id": "r3"}, {"status": "FAIL"})


def test_nonfinite_json_rejected():
    with pytest.raises(LineageError):
        sha256_json({"value": float("nan")})
