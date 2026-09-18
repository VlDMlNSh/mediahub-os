"""Persistent systemd runner for the hybrid-development controller."""
from __future__ import annotations

import argparse
import signal
import time
from datetime import timedelta
from pathlib import Path

from ops.ai.hybrid_development_controller import (
    HybridDevelopmentController,
    HybridDevelopmentDenied,
)
from ops.ai.hybrid_session import HybridSessionController, SessionJournal
from ops.ai.task_delivery import TaskDeliveryJournal
from ops.ai.text_conversation import TextConversationController
from ops.hybrid_cloud_egress import HybridCloudEgressAdapter, TransportCandidate

ROOT = Path(__file__).resolve().parents[2]


def parse_paths(value: str) -> tuple[TransportCandidate, ...]:
    result = []
    for priority, item in enumerate(value.split(","), 10):
        name, interface, source = item.split(":", 2)
        result.append(TransportCandidate(name, interface, source, priority))
    if not result:
        raise ValueError("at least one egress path is required")
    return tuple(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--baseline-sha", required=True)
    parser.add_argument("--r4-sha", required=True)
    parser.add_argument("--duration-hours", type=float, required=True)
    parser.add_argument("--health-url", required=True)
    parser.add_argument("--paths", required=True)
    parser.add_argument("--interval", type=float, default=5.0)
    args = parser.parse_args()
    if args.duration_hours <= 0 or args.interval <= 0:
        raise SystemExit("duration and interval must be positive")
    state = ROOT / ".hybrid-development"
    state.mkdir(parents=True, exist_ok=True)
    session = HybridSessionController(SessionJournal(state / "session.jsonl"))
    conversation = TextConversationController(journal_path=state / "conversation.json")
    delivery = TaskDeliveryJournal(state / "delivery.json")
    egress = HybridCloudEgressAdapter(parse_paths(args.paths))
    controller = HybridDevelopmentController(session, conversation, delivery, egress, args.health_url)
    session_checkpoint = state / "session.jsonl"
    if session_checkpoint.exists():
        controller.restore(args.session_id, args.baseline_sha, args.r4_sha)
    else:
        controller.start(args.session_id, args.baseline_sha, args.r4_sha, timedelta(hours=args.duration_hours))

    stopping = False
    def stop(_signum, _frame):
        nonlocal stopping
        stopping = True
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    while not stopping:
        snap = controller.poll()
        if snap.state.value == "SAFE_STOP":
            return 2
        try:
            controller.preflight()
        except HybridDevelopmentDenied:
            pass
        if controller.state.value == "SAFE_STOP":
            return 2
        if session.session is None or session.session.state.value in {"EXPIRED", "STOPPED", "SAFE_STOP"}:
            return 0
        time.sleep(args.interval)
    controller.stop("systemd stop")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
