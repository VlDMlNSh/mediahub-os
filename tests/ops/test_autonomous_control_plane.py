import inspect
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_controller_and_watchdog_are_valid_shell():
    for name in ("ops/autonomous_os_loop.sh", "ops/autonomous_watchdog.sh"):
        result = subprocess.run(["bash", "-n", str(ROOT / name)], capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr


def test_autonomous_code_has_no_history_rewrite_commands():
    paths = [ROOT / "ops/autonomous_os_loop.sh", ROOT / "ops/autonomous_watchdog.sh", ROOT / "ops/local_autonomous_agent.py"]
    forbidden = ("git reset", "git rebase", "git commit --amend", "force-push", "--force")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert not any(token in text for token in forbidden), path


def test_controller_requires_r4_clean_baseline_and_ancestor_commit():
    text = (ROOT / "ops/autonomous_os_loop.sh").read_text(encoding="utf-8")
    assert "merge-base --is-ancestor 471f709f5633feab7aeb62dd3ea52effad6d2bc4 HEAD" in text
    assert 'git status --porcelain' in text
    assert 'git merge-base --is-ancestor "$BASE_HEAD" "$POST_HEAD"' in text


def test_agent_does_not_treat_noop_as_success():
    text = (ROOT / "ops/local_autonomous_agent.py").read_text(encoding="utf-8")
    assert "LOCAL_AGENT_NOOP: no admissible downstream change" in text
    assert "return 30" in text
    assert "commit.returncode != 0" in text


def test_watchdog_validates_controller_ownership_before_termination():
    text = (ROOT / "ops/autonomous_watchdog.sh").read_text(encoding="utf-8")
    assert 'owned=0' in text
    assert 'ps -p "$pid" -o args=' in text
    assert 'if [ "$owned" -eq 0 ] || [ "$stale" -eq 1 ]' in text


def test_agent_runs_deterministic_lint_repair_before_verification():
    text = (ROOT / "ops/local_autonomous_agent.py").read_text(encoding="utf-8")
    assert 'str(RUFF), "check", "--fix"' in text
    assert 'LOCAL_AGENT_BLOCKED: deterministic lint repair failed' in text


from ops.local_autonomous_agent import fallback_patch, safe_patch, state


def test_fallback_patch_is_applyable_and_idempotent(tmp_path, monkeypatch):
    from ops import local_autonomous_agent as agent
    target = tmp_path / "tests" / "test_mediahub_free_model_catalog.py"
    target.parent.mkdir()
    target.write_text(
        "from mediahub_free_model_catalog import FREE_MODEL_CANDIDATES\n\n"
        "def test_provider_list_is_stable_and_unique():\n"
        "    listed = providers()\n"
        "    assert listed == tuple(sorted(set(listed)))\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(agent, "ROOT", tmp_path)
    patch = fallback_patch()
    assert safe_patch(patch)
    assert patch.startswith("--- a/tests/test_mediahub_free_model_catalog.py")
    target.write_text(target.read_text() + "\ndef test_catalog_has_unique_provider_model_pairs():\n", encoding="utf-8")
    assert fallback_patch() == ""


def test_safe_patch_rejects_wrong_target():
    patch = fallback_patch().replace("tests/test_mediahub_free_model_catalog.py", "tests/not_allowed.py")
    assert not safe_patch(patch)


def test_safe_patch_rejects_multiple_targets():
    patch = fallback_patch()
    if not patch:
        return
    extra = "--- a/tests/other.py\n+++ b/tests/other.py\n@@ -1 +1 @@\n-x\n+y\n"
    assert not safe_patch(patch + extra)


def test_safe_patch_rejects_new_file_rename_and_mode_changes():
    patch = fallback_patch()
    if not patch:
        return
    assert not safe_patch(patch.replace("--- a/", "new file mode 100644\n--- /dev/null\n--- a/", 1))
    assert not safe_patch(patch.replace("--- a/", "rename from tests/test_mediahub_free_model_catalog.py\n--- a/", 1))
    assert not safe_patch(patch.replace("--- a/", "old mode 100644\n--- a/", 1))


def test_safe_patch_rejects_protected_path_and_malformed_hunk():
    patch = fallback_patch()
    if not patch:
        return
    assert not safe_patch(patch.replace("tests/test_mediahub_free_model_catalog.py", ".github/workflows/x.yml"))
    assert not safe_patch(patch.replace("@@ -26,3 +26,6 @@", "@@ malformed"))


def test_state_rejects_unknown_state():
    import pytest
    with pytest.raises(ValueError):
        state("UNKNOWN_STATE")


def test_fallback_source_has_no_network_or_credential_usage():
    from ops import local_autonomous_agent as agent
    source = inspect.getsource(agent.fallback_patch)
    assert "urllib" not in source
    assert "credential" not in source.lower()
    assert "socket" not in source.lower()
    assert "subprocess" not in source


def test_exact_target_rejects_additional_staged_path(monkeypatch):
    from ops import local_autonomous_agent as agent

    class Result:
        stdout = "tests/test_mediahub_free_model_catalog.py\nops/extra.py\n"
        returncode = 0

    monkeypatch.setattr(agent, "run", lambda *args, **kwargs: Result())
    assert not agent.exact_target()


def test_exact_target_accepts_only_target(monkeypatch):
    from ops import local_autonomous_agent as agent

    class Result:
        stdout = "tests/test_mediahub_free_model_catalog.py\n"
        returncode = 0

    monkeypatch.setattr(agent, "run", lambda *args, **kwargs: Result())
    assert agent.exact_target()
