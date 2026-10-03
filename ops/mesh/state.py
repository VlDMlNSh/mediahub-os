NODE_EVENTS = {
    "DISCOVERED": {"activate":"ACTIVE", "block":"BLOCKED", "quarantine":"QUARANTINED"},
    "ACTIVE": {"stale":"STALE", "block":"BLOCKED", "quarantine":"QUARANTINED", "retire":"RETIRED"},
    "STALE": {"heartbeat":"ACTIVE", "block":"BLOCKED", "quarantine":"QUARANTINED"},
    "BLOCKED": {"retire":"RETIRED"},
    "QUARANTINED": {"retire":"RETIRED"},
    "RETIRED": {},
}
REPLICA_EVENTS = {
    "DECLARED": {"transfer":"TRANSFERRING", "fail":"FAILED"},
    "TRANSFERRING": {"verify":"VERIFIED", "fail":"FAILED"},
    "VERIFIED": {"available":"AVAILABLE", "fail":"FAILED"},
    "AVAILABLE": {"stale":"STALE", "fail":"FAILED"},
    "STALE": {"recover":"RECOVERY_REQUIRED", "fail":"FAILED"},
    "FAILED": {"recover":"RECOVERY_REQUIRED"},
    "RECOVERY_REQUIRED": {"transfer":"TRANSFERRING", "fail":"FAILED"},
}

def _transition(table, current: str, event: str) -> str:
    try:
        return table[current][event]
    except KeyError as exc:
        raise ValueError(f"invalid state transition: {current} + {event}") from exc

def transition_node_state(current: str, event: str) -> str:
    return _transition(NODE_EVENTS, current, event)

def transition_replica_state(current: str, event: str) -> str:
    return _transition(REPLICA_EVENTS, current, event)
