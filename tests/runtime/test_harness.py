import pytest

from mediahub_runtime.harness import HarnessError, MediaHubHarness


def test_harness_executes_allowed_argv_without_shell():
    result = MediaHubHarness().run(["python3", "-c", "print('READY')"])
    assert result.status == "completed"
    assert result.returncode == 0
    assert result.stdout.strip() == "READY"
    assert result.output_bytes > 0


def test_harness_rejects_shell_injection():
    with pytest.raises(HarnessError) as exc:
        MediaHubHarness().run(["bash", "-c", "echo unsafe"])
    assert exc.value.code == "argument_not_allowed"


def test_harness_rejects_privileged_or_destructive_commands():
    for argv in (["sudo", "id"], ["rm", "-rf", "x"], ["git", "reset", "--hard"]):
        with pytest.raises(HarnessError) as exc:
            MediaHubHarness().run(argv)
        assert exc.value.code in {"executable_not_allowed", "argument_not_allowed"}


def test_harness_rejects_credentials():
    with pytest.raises(HarnessError) as exc:
        MediaHubHarness().run(["python3", "-c", "print('x')", "api_key=secret"])
    assert exc.value.code == "credential_argument_rejected"


def test_harness_rejects_cwd_outside_mediahub():
    with pytest.raises(HarnessError) as exc:
        MediaHubHarness().run(["pwd"], "/tmp")
    assert exc.value.code == "cwd_not_allowed"


def test_harness_returns_failed_process_evidence():
    result = MediaHubHarness().run(["python3", "-c", "raise SystemExit(3)"])
    assert result.status == "failed"
    assert result.returncode == 3
    assert result.stderr_sha256
