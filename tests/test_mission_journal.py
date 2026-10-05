from __future__ import annotations

import json

from runtime.mediahub_runtime.mission_journal import MissionJournal, MissionJournalError


def test_journal_starts_and_resumes_same_command(tmp_path):
    journal = MissionJournal(tmp_path / "mission.json")
    first = journal.begin(
        command_id="cmd-1",
        node_id="mh-dev-01",
        target_sha="a" * 40,
        agent_sha="agent-a",
    )
    assert first["status"] == "RUNNING"
    assert first["resume_count"] == 0

    journal.checkpoint(phase="pre_soak_evidence", cycle=2, step={"cycle": 2, "phase": "pre_soak"})
    resumed = journal.begin(
        command_id="cmd-1",
        node_id="mh-dev-01",
        target_sha="a" * 40,
        agent_sha="agent-a",
    )
    assert resumed["resume_count"] == 1
    assert resumed["phase"] == "pre_soak_evidence"
    assert resumed["steps"][-1]["phase"] == "pre_soak"


def test_journal_rejects_different_running_command(tmp_path):
    journal = MissionJournal(tmp_path / "mission.json")
    journal.begin(
        command_id="cmd-1",
        node_id="mh-dev-01",
        target_sha="a" * 40,
        agent_sha="agent-a",
    )
    try:
        journal.begin(
            command_id="cmd-2",
            node_id="mh-dev-01",
            target_sha="b" * 40,
            agent_sha="agent-a",
        )
    except MissionJournalError as exc:
        assert str(exc) == "different_running_command"
    else:
        raise AssertionError("different running command was accepted")


def test_journal_finish_is_durable(tmp_path):
    path = tmp_path / "mission.json"
    journal = MissionJournal(path)
    journal.begin(
        command_id="cmd-1",
        node_id="mh-dev-01",
        target_sha="a" * 40,
        agent_sha="agent-a",
    )
    journal.finish(status="BLOCKED", result={"phase": "distributed_verification"})
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["status"] == "BLOCKED"
    assert data["result"]["phase"] == "distributed_verification"


def test_journal_rejects_agent_change_on_resume(tmp_path):
    journal = MissionJournal(tmp_path / "mission.json")
    journal.begin(
        command_id="cmd-1",
        node_id="mh-dev-01",
        target_sha="a" * 40,
        agent_sha="agent-a",
    )
    try:
        journal.begin(
            command_id="cmd-1",
            node_id="mh-dev-01",
            target_sha="a" * 40,
            agent_sha="agent-b",
        )
    except MissionJournalError as exc:
        assert str(exc) == "agent_sha_changed"
    else:
        raise AssertionError("changed agent identity was accepted")


def test_journal_rejects_invalid_schema(tmp_path):
    path = tmp_path / "mission.json"
    path.write_text(json.dumps({"status": "RUNNING"}), encoding="utf-8")
    journal = MissionJournal(path)
    try:
        journal.load()
    except MissionJournalError as exc:
        assert str(exc) == "invalid_mission_journal"
    else:
        raise AssertionError("invalid journal schema was accepted")
