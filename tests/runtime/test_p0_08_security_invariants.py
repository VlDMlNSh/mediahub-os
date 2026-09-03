"""Static guard tests for P0-08.1.

These tests deliberately inspect the new P0-08 files only. Runtime authority,
persistence, process execution, and network access remain outside this slice.
"""

from pathlib import Path


ROOT = Path(__file__).parents[2]
P0_08_FILES = (
    ROOT / "runtime/mediahub_runtime/plugin_manifest.py",
    ROOT / "runtime/mediahub_runtime/plugin_capabilities.py",
)


def test_p0_08_1_has_no_forbidden_runtime_imports():
    forbidden = (
        "subprocess",
        "socket",
        "requests",
        "sqlite3",
        "pathlib.Path.open",
        "os.system",
        "os.popen",
    )
    text = "\n".join(path.read_text(encoding="utf-8") for path in P0_08_FILES)
    assert not any(term in text for term in forbidden)


def test_p0_08_1_contains_no_state_authority_or_persistence_symbols():
    forbidden = (
        "StateAuthority",
        "CanonicalStore",
        "PersistenceHandle",
        "MutableState",
        "Transaction",
        "checkpoint",
        "revision",
        "generation",
    )
    text = "\n".join(path.read_text(encoding="utf-8") for path in P0_08_FILES)
    assert not any(term in text for term in forbidden)
