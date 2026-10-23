from __future__ import annotations

import json

from ops.qualification import run_distributed_local_worker as worker


def test_bounded_claude_write_allows_only_exact_canonical_workspace_boundary(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    monkeypatch.setattr(worker, "ROOT", root)
    target = root / "docs" / "boundary.md"
    output = json.dumps({
        "name": "write",
        "arguments": {"file_path": str(target), "content": "bounded"},
    })

    assert worker._materialize_bounded_claude_tool_output(output, "docs/boundary.md") == "docs/boundary.md"
    assert target.read_text(encoding="utf-8") == "bounded"


def test_bounded_claude_write_rejects_absolute_declared_boundary(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("unchanged", encoding="utf-8")
    monkeypatch.setattr(worker, "ROOT", root)
    output = json.dumps({
        "name": "write",
        "arguments": {"file_path": str(outside), "content": "escape"},
    })

    assert worker._materialize_bounded_claude_tool_output(output, str(outside)) is None
    assert outside.read_text(encoding="utf-8") == "unchanged"


def test_bounded_claude_write_rejects_traversal_boundary(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("unchanged", encoding="utf-8")
    monkeypatch.setattr(worker, "ROOT", root)
    output = json.dumps({
        "name": "write",
        "arguments": {"file_path": str(outside), "content": "escape"},
    })

    assert worker._materialize_bounded_claude_tool_output(output, "../outside.md") is None
    assert outside.read_text(encoding="utf-8") == "unchanged"


def test_bounded_claude_write_rejects_symlink_parent_escape(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    outside = outside_dir / "boundary.md"
    outside.write_text("unchanged", encoding="utf-8")
    (root / "docs").symlink_to(outside_dir, target_is_directory=True)
    monkeypatch.setattr(worker, "ROOT", root)
    output = json.dumps({
        "name": "write",
        "arguments": {"file_path": str(root / "docs" / "boundary.md"), "content": "escape"},
    })

    assert worker._materialize_bounded_claude_tool_output(output, "docs/boundary.md") is None
    assert outside.read_text(encoding="utf-8") == "unchanged"


def test_bounded_claude_write_rejects_symlink_target_escape(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("unchanged", encoding="utf-8")
    (root / "boundary.md").symlink_to(outside)
    monkeypatch.setattr(worker, "ROOT", root)
    output = json.dumps({
        "name": "write",
        "arguments": {"file_path": str(root / "boundary.md"), "content": "escape"},
    })

    assert worker._materialize_bounded_claude_tool_output(output, "boundary.md") is None
    assert outside.read_text(encoding="utf-8") == "unchanged"
