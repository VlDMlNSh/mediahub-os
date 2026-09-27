from ops.astra_github_coding_protocol import (
    EvidenceEnvelope,
    ExecutionIdentity,
    ProtocolError,
    accept_result,
    validate_fence,
)


def identity():
    return ExecutionIdentity.from_mapping({
        "schema_version": 1,
        "task_id": "ASTRA-P0-001",
        "execution_id": "exec-1",
        "generation": 1,
        "lease_id": "lease-1",
        "owner_id": "mh-dev-01",
        "operation_key": "coding.test",
        "target_sha": "a" * 40,
        "created_at": "2026-09-27T00:00:00Z",
        "expires_at": "2026-09-27T01:00:00Z",
    })


def evidence():
    return EvidenceEnvelope(
        identity=identity(),
        worker="mh-dev-01",
        model="qwen2.5-coder:3b",
        provider="ollama",
        changed_files=("tests/example.py",),
        tests=("pytest -q",),
        security_results=("diff-check PASS",),
        commit_sha="b" * 40,
        remote_sha="b" * 40,
        artifact_sha256="c" * 64,
        terminal_status="SUCCEEDED",
    )


def test_valid_fence():
    validate_fence(
        identity(),
        task_id="ASTRA-P0-001",
        execution_id="exec-1",
        generation=1,
        lease_id="lease-1",
        owner_id="mh-dev-01",
        target_sha="a" * 40,
    )


def test_invalid_target_sha_is_rejected():
    import pytest
    with pytest.raises(ProtocolError):
        ExecutionIdentity.from_mapping({
            "schema_version": 1,
            "task_id": "ASTRA-P0-001",
            "execution_id": "exec-1",
            "generation": 1,
            "lease_id": "lease-1",
            "owner_id": "mh-dev-01",
            "operation_key": "coding.test",
            "target_sha": "not-a-sha",
            "created_at": "2026-09-27T00:00:00Z",
            "expires_at": "2026-09-27T01:00:00Z",
        })


def test_stale_generation_is_fenced():
    import pytest
    with pytest.raises(ProtocolError):
        validate_fence(
            identity(),
            task_id="ASTRA-P0-001",
            execution_id="exec-1",
            generation=2,
            lease_id="lease-1",
            owner_id="mh-dev-01",
            target_sha="a" * 40,
        )


def test_duplicate_identical_result_is_idempotent():
    item = evidence()
    assert accept_result(item, current=item) == item.digest()


def test_duplicate_conflicting_result_is_rejected():
    import pytest
    item = evidence()
    conflicting = EvidenceEnvelope(
        identity=item.identity,
        worker=item.worker,
        model=item.model,
        provider=item.provider,
        changed_files=item.changed_files,
        tests=item.tests,
        security_results=item.security_results,
        commit_sha="d" * 40,
        remote_sha="d" * 40,
        artifact_sha256=item.artifact_sha256,
        terminal_status=item.terminal_status,
    )
    with pytest.raises(ProtocolError):
        accept_result(conflicting, current=item)


def test_duplicate_changed_files_are_conflicting():
    import pytest
    item = evidence()
    conflicting = EvidenceEnvelope(
        identity=item.identity,
        worker=item.worker,
        model=item.model,
        provider=item.provider,
        changed_files=("different.py",),
        tests=item.tests,
        security_results=item.security_results,
        commit_sha=item.commit_sha,
        remote_sha=item.remote_sha,
        artifact_sha256=item.artifact_sha256,
        terminal_status=item.terminal_status,
    )
    with pytest.raises(ProtocolError):
        accept_result(conflicting, current=item)
