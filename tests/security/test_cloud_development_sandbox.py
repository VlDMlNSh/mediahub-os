import pytest

from ops.cloud_development_sandbox import CloudDevelopmentSandbox, SandboxDenied


def test_create_isolates_worktree_and_teardown_is_deterministic(tmp_path):
    sandbox = CloudDevelopmentSandbox.create(tmp_path)
    assert sandbox.root.parent == tmp_path
    assert sandbox.worktree.parent == sandbox.root
    assert sandbox.root.stat().st_mode & 0o777 == 0o700
    sandbox.validate()
    (sandbox.worktree / "artifact.txt").write_text("quarantined", encoding="utf-8")
    sandbox.teardown()
    assert not sandbox.root.exists()


def test_symlink_parent_is_denied(tmp_path):
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real, target_is_directory=True)
    with pytest.raises(SandboxDenied):
        CloudDevelopmentSandbox.create(link)


def test_tampered_marker_is_denied(tmp_path):
    sandbox = CloudDevelopmentSandbox.create(tmp_path)
    sandbox.marker.write_text("tampered", encoding="ascii")
    with pytest.raises(SandboxDenied):
        sandbox.teardown()
    shutil = __import__("shutil")
    shutil.rmtree(sandbox.root)


def test_symlink_worktree_is_denied(tmp_path):
    sandbox = CloudDevelopmentSandbox.create(tmp_path)
    real = tmp_path / "outside"
    real.mkdir()
    sandbox.worktree.rmdir()
    sandbox.worktree.symlink_to(real, target_is_directory=True)
    with pytest.raises(SandboxDenied):
        sandbox.validate()
    sandbox.root.joinpath(".mediahub-cloud-sandbox").unlink()
    sandbox.root.joinpath("worktree").unlink()
    sandbox.root.rmdir()
