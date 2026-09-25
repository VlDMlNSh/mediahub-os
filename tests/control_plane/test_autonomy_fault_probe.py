from pathlib import Path

from ops import autonomy_fault_probe as probe


def test_pid_from_file_accepts_pid_and_generation():
    path = Path('/tmp/mediahub-test-pid')
    path.write_text('12345:67890\n')
    try:
        assert probe.pid_from_file(path) == 12345
    finally:
        path.unlink()


def test_pid_from_file_rejects_malformed(tmp_path):
    path = tmp_path / 'pid'
    path.write_text('not-a-pid')
    assert probe.pid_from_file(path) is None


def test_fixed_identity_requires_expected_command(monkeypatch):
    monkeypatch.setattr(probe, 'proc_identity', lambda pid: probe.ProcIdentity(pid, '1', '/unexpected'))
    try:
        probe.fixed_identity(42, ('ops/astra_orchestrator.py',))
    except RuntimeError as exc:
        assert 'refusing to signal unexpected process' in str(exc)
    else:
        raise AssertionError('unexpected process identity was accepted')


def test_clean_idle_is_bounded_to_healthy_heartbeat(monkeypatch):
    monkeypatch.setattr(probe, 'heartbeat', lambda: {'state':'RUNNING','failure_streak':0})
    result = probe.scenario_idle()
    assert result['result'] == 'PASS'
