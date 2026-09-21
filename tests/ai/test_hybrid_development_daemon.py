import sys

import pytest

from ops.ai import hybrid_development_daemon as daemon


def test_daemon_treats_matching_terminal_restore_as_clean_exit(monkeypatch, tmp_path):
    class FakeJournal:
        def __init__(self, path):
            self.path = path

        def read_tail(self):
            return {
                "session_id": "s1",
                "baseline_sha": "baseline",
                "r4_sha": "r4",
                "state": "EXPIRED",
            }

    class FakeSession:
        def __init__(self, journal):
            self.journal = journal

    class FakeConversation:
        def __init__(self, journal_path):
            pass

    class FakeDelivery:
        def __init__(self, path):
            pass

    class FakeEgress:
        def __init__(self, paths):
            pass

    class FakeController:
        def __init__(self, *args):
            pass

        def restore(self, *args):
            raise daemon.HybridDevelopmentDenied("terminal restore")

    checkpoint = tmp_path / ".hybrid-development" / "session.jsonl"
    checkpoint.parent.mkdir()
    checkpoint.write_text("terminal\n", encoding="utf-8")
    monkeypatch.setattr(daemon, "ROOT", tmp_path)
    monkeypatch.setattr(daemon, "SessionJournal", FakeJournal)
    monkeypatch.setattr(daemon, "HybridSessionController", FakeSession)
    monkeypatch.setattr(daemon, "TextConversationController", FakeConversation)
    monkeypatch.setattr(daemon, "TaskDeliveryJournal", FakeDelivery)
    monkeypatch.setattr(daemon, "HybridCloudEgressAdapter", FakeEgress)
    monkeypatch.setattr(daemon, "HybridDevelopmentController", FakeController)
    monkeypatch.setattr(daemon, "parse_paths", lambda value: ())
    monkeypatch.setattr(sys, "argv", [
        "daemon", "--session-id", "s1", "--baseline-sha", "baseline",
        "--r4-sha", "r4", "--duration-hours", "1",
        "--health-url", "https://example.invalid/health", "--paths", "vpm:tun:src",
    ])
    assert daemon.main() == 0


def test_daemon_re_raises_restore_error_for_nonterminal_or_mismatched_tail(monkeypatch, tmp_path):
    class FakeJournal:
        def __init__(self, path):
            self.path = path

        def read_tail(self):
            return {"session_id": "other", "state": "EXPIRED"}

    class FakeSession:
        def __init__(self, journal):
            self.journal = journal

    class FakeConversation:
        def __init__(self, journal_path):
            pass

    class FakeDelivery:
        def __init__(self, path):
            pass

    class FakeEgress:
        def __init__(self, paths):
            pass

    class FakeController:
        def __init__(self, *args):
            pass

        def restore(self, *args):
            raise daemon.HybridDevelopmentDenied("restore failed")

    checkpoint = tmp_path / ".hybrid-development" / "session.jsonl"
    checkpoint.parent.mkdir()
    checkpoint.write_text("terminal\n", encoding="utf-8")
    monkeypatch.setattr(daemon, "ROOT", tmp_path)
    monkeypatch.setattr(daemon, "SessionJournal", FakeJournal)
    monkeypatch.setattr(daemon, "HybridSessionController", FakeSession)
    monkeypatch.setattr(daemon, "TextConversationController", FakeConversation)
    monkeypatch.setattr(daemon, "TaskDeliveryJournal", FakeDelivery)
    monkeypatch.setattr(daemon, "HybridCloudEgressAdapter", FakeEgress)
    monkeypatch.setattr(daemon, "HybridDevelopmentController", FakeController)
    monkeypatch.setattr(daemon, "parse_paths", lambda value: ())
    monkeypatch.setattr(sys, "argv", [
        "daemon", "--session-id", "s1", "--baseline-sha", "baseline",
        "--r4-sha", "r4", "--duration-hours", "1",
        "--health-url", "https://example.invalid/health", "--paths", "vpm:tun:src",
    ])
    with pytest.raises(daemon.HybridDevelopmentDenied):
        daemon.main()

def test_daemon_rejects_terminal_tail_with_baseline_or_r4_mismatch(monkeypatch, tmp_path):
    class FakeJournal:
        def __init__(self, path):
            self.path = path

        def read_tail(self):
            return {"session_id": "s1", "baseline_sha": "other", "r4_sha": "other-r4", "state": "STOPPED"}

    class FakeSession:
        def __init__(self, journal):
            self.journal = journal

    class FakeConversation:
        def __init__(self, journal_path):
            pass

    class FakeDelivery:
        def __init__(self, path):
            pass

    class FakeEgress:
        def __init__(self, paths):
            pass

    class FakeController:
        def __init__(self, *args):
            pass

        def restore(self, *args):
            raise daemon.HybridDevelopmentDenied("terminal restore")

    checkpoint = tmp_path / ".hybrid-development" / "session.jsonl"
    checkpoint.parent.mkdir()
    checkpoint.write_text("terminal\n", encoding="utf-8")
    monkeypatch.setattr(daemon, "ROOT", tmp_path)
    monkeypatch.setattr(daemon, "SessionJournal", FakeJournal)
    monkeypatch.setattr(daemon, "HybridSessionController", FakeSession)
    monkeypatch.setattr(daemon, "TextConversationController", FakeConversation)
    monkeypatch.setattr(daemon, "TaskDeliveryJournal", FakeDelivery)
    monkeypatch.setattr(daemon, "HybridCloudEgressAdapter", FakeEgress)
    monkeypatch.setattr(daemon, "HybridDevelopmentController", FakeController)
    monkeypatch.setattr(daemon, "parse_paths", lambda value: ())
    import sys
    monkeypatch.setattr(sys, "argv", [
        "daemon", "--session-id", "s1", "--baseline-sha", "baseline",
        "--r4-sha", "r4", "--duration-hours", "1",
        "--health-url", "https://example.invalid/health", "--paths", "vpm:tun:src",
    ])
    with pytest.raises(daemon.HybridDevelopmentDenied):
        daemon.main()
