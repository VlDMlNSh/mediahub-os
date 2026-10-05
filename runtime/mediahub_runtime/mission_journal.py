"""Durable journal for crash-safe Astra command execution.

The journal is local coordination state. It never grants authority and is only
used to resume the exact command/target-SHA pair after an interrupted process.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path


class MissionJournalError(RuntimeError):
    pass


class MissionJournal:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> dict | None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return None
        except (OSError, json.JSONDecodeError) as exc:
            raise MissionJournalError("invalid_mission_journal") from exc
        if not isinstance(data, dict):
            raise MissionJournalError("invalid_mission_journal")
        return data

    def _write(self, data: dict) -> dict:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = dict(data)
        data["updated_at"] = int(time.time())
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(tmp, self.path)
        return data

    def begin(self, *, command_id: str, node_id: str, target_sha: str, agent_sha: str) -> dict:
        existing = self.load()
        if existing and existing.get("status") == "RUNNING":
            if (
                existing.get("command_id") != command_id
                or existing.get("node_id") != node_id
                or existing.get("target_sha") != target_sha
            ):
                raise MissionJournalError("different_running_command")
            existing["resume_count"] = int(existing.get("resume_count", 0)) + 1
            return self._write(existing)

        return self._write({
            "schema": "mediahub.astra.mission-journal.v1",
            "status": "RUNNING",
            "command_id": command_id,
            "node_id": node_id,
            "target_sha": target_sha,
            "agent_sha": agent_sha,
            "phase": "started",
            "cycle": 0,
            "steps": [],
            "resume_count": 0,
            "started_at": int(time.time()),
        })

    def checkpoint(self, *, phase: str, cycle: int | None = None, step: dict | None = None, **extra) -> dict:
        data = self.load()
        if not data or data.get("status") != "RUNNING":
            raise MissionJournalError("journal_not_running")
        data["phase"] = phase
        if cycle is not None:
            data["cycle"] = cycle
        if step is not None:
            steps = list(data.get("steps", []))
            steps.append(step)
            data["steps"] = steps[-64:]
        data.update(extra)
        return self._write(data)

    def finish(self, *, status: str, result: dict | None = None) -> dict:
        if status not in {"PASS", "BLOCKED", "FAILED"}:
            raise MissionJournalError("invalid_journal_status")
        data = self.load()
        if not data:
            raise MissionJournalError("journal_not_running")
        data["status"] = status
        data["finished_at"] = int(time.time())
        if result is not None:
            data["result"] = result
        return self._write(data)

    def clear(self) -> None:
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
