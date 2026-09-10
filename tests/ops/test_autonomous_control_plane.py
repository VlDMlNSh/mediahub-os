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
