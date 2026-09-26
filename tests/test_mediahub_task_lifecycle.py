import pytest

from ops.mediahub_task_lifecycle import Evidence, TaskStage, verify_done, validate_stage_transition


def complete(stage=TaskStage.CLOSE, status="SUCCEEDED"):
    return Evidence(
        task_id="t1", requirement="change one thing", agent_id="a1", execution_id="e1",
        model="ollama/qwen", host="df3", lease_id="l1", generation=1,
        changed_files=("x.py",), tests=("pytest x",), test_results=("PASS",),
        qualification_evidence=("marker",), commit="abc", push="origin/abc",
        post_verification="clean", stage=stage, status=status,
    )


def test_lifecycle_is_strictly_ordered():
    validate_stage_transition(TaskStage.DISCOVER, TaskStage.PLAN)
    validate_stage_transition(TaskStage.VERIFY, TaskStage.RECORD)
    with pytest.raises(ValueError):
        validate_stage_transition(TaskStage.EXECUTE, TaskStage.COMMIT)


def test_done_requires_all_evidence():
    assert verify_done(complete()).done
    incomplete = complete()
    object.__setattr__(incomplete, "push", None)
    with pytest.raises(ValueError):
        verify_done(incomplete)


def test_done_cannot_be_declared_from_failed_execution():
    failed = complete(status="FAILED")
    with pytest.raises(ValueError):
        verify_done(failed)


def test_done_cannot_be_declared_before_close():
    evidence = complete(stage=TaskStage.VERIFY)
    with pytest.raises(ValueError):
        verify_done(evidence)
