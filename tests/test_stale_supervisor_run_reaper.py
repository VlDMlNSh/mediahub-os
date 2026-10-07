from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REAPER = ROOT / ".github/workflows/astra-stale-supervisor-run-reaper.yml"


def test_reaper_resolves_authoritative_main_head_not_event_sha():
    source = REAPER.read_text(encoding="utf-8")
    assert 'CURRENT_SHA: ""' in source
    assert 'git/ref/heads/main' in source
    assert 'main_head_resolution_failed' in source
    assert 'current=resolved.stdout.strip()' in source


def test_reaper_has_no_deleted_legacy_workflow_dependency():
    source = REAPER.read_text(encoding="utf-8")
    assert 'mh25-dual-local-executor-23wave.yml' not in source
