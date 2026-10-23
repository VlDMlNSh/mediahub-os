from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "freellmapi-qualification.yml"


def load_workflow():
    # BaseLoader keeps GitHub Actions' unquoted `on` key as a string.
    return yaml.load(WORKFLOW_PATH.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


def test_push_and_pull_request_checks_run_on_github_hosted_runner_only():
    workflow = load_workflow()
    triggers = workflow["on"]
    assert "push" in triggers
    assert "pull_request" in triggers
    assert "workflow_dispatch" in triggers

    contract = workflow["jobs"]["contract"]
    assert contract["if"] == "github.event_name != 'workflow_dispatch'"
    assert contract["runs-on"] == "ubuntu-latest"

    serialized = yaml.dump(contract)
    for forbidden in (
        "FREELLMAPI_KEY_FILE",
        "FREELLMAPI_URL",
        "secrets.",
        "Authorization",
    ):
        assert forbidden not in serialized

    steps = contract["steps"]
    install = next(step for step in steps if step.get("name") == "Install test dependencies")
    assert "requirements-dev.txt" in install["run"]
    verify = next(
        step for step in steps
        if step.get("name") == "Verify adapter and qualification admission contracts"
    )
    assert "tests/ai/test_cloud_orchestrator_failover.py" in verify["run"]
    assert "tests/test_freellmapi_qualification_workflow_contract.py" in verify["run"]


def test_live_qualification_requires_explicit_dispatch_and_exact_main_sha():
    workflow = load_workflow()
    inputs = workflow["on"]["workflow_dispatch"]["inputs"]
    assert inputs["confirm"]["required"] == "true"
    assert inputs["confirm"]["type"] == "boolean"
    assert inputs["confirm"]["default"] == "false"
    assert inputs["target_sha"]["required"] == "true"
    assert inputs["target_sha"]["type"] == "string"

    gate = workflow["jobs"]["dispatch_gate"]
    assert gate["if"] == "github.event_name == 'workflow_dispatch'"
    assert gate["permissions"] == {}
    gate_step = gate["steps"][0]
    assert gate_step["env"]["CONFIRM"] == "${{ inputs.confirm }}"
    assert gate_step["env"]["TARGET_SHA"] == "${{ inputs.target_sha }}"
    assert gate_step["env"]["CURRENT_SHA"] == "${{ github.sha }}"
    assert gate_step["env"]["SOURCE_REF"] == "${{ github.ref }}"
    assert gate_step["env"]["TRIGGER_ACTOR"] == "${{ github.actor }}"
    assert gate_step["env"]["REPO_OWNER"] == "${{ github.repository_owner }}"
    for marker in (
        '[[ "$CONFIRM" == "true" ]]',
        '[[ "$SOURCE_REF" == "refs/heads/main" ]]',
        '[[ "$TRIGGER_ACTOR" == "$REPO_OWNER" ]]',
        '[[ "$TARGET_SHA" =~ ^[0-9a-f]{40}$ && "$TARGET_SHA" == "$CURRENT_SHA" ]]',
    ):
        assert marker in gate_step["run"]
    assert gate["outputs"]["admitted"] == "${{ steps.gate.outputs.admitted }}"

    concurrency = workflow["concurrency"]
    assert "github.event_name == 'push'" in concurrency["group"]
    assert "'freellmapi-live-qualification'" in concurrency["group"]
    assert "'freellmapi-live-qualification-live'" in concurrency["group"]
    assert concurrency["cancel-in-progress"] == "${{ github.event_name != 'workflow_dispatch' }}"

    qualify = workflow["jobs"]["qualify"]
    assert qualify["needs"] == "dispatch_gate"
    assert "needs.dispatch_gate.outputs.admitted == 'true'" in qualify["if"]
    assert "github.event_name == 'workflow_dispatch'" in qualify["if"]
    assert "inputs.confirm == true" in qualify["if"]
    assert "inputs.target_sha == github.sha" in qualify["if"]
    assert "github.ref == 'refs/heads/main'" in qualify["if"]
    assert "github.actor == github.repository_owner" in qualify["if"]
    assert qualify["runs-on"] == ["self-hosted", "linux", "x64", "mediahub-control"]


def test_live_provider_credentials_and_inference_are_confined_to_self_hosted_job():
    workflow = load_workflow()
    serialized_contract = yaml.dump(workflow["jobs"]["contract"])
    serialized_gate = yaml.dump(workflow["jobs"]["dispatch_gate"])
    serialized_live = yaml.dump(workflow["jobs"]["qualify"])

    for unsafe_value in ("FREELLMAPI_KEY_FILE", "FREELLMAPI_URL", "FREELLMAPI_MODEL"):
        assert unsafe_value not in serialized_contract
        assert unsafe_value not in serialized_gate
        assert unsafe_value in serialized_live

    assert "LIVE_QUALIFIED" in serialized_live
    assert 'test "$(hostname)" = "mh-dev-01"' in serialized_live
    assert 'test "$(id -un)" = "mediahub-runner"' in serialized_live
