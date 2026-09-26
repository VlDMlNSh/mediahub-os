from __future__ import annotations

import fcntl


def test_command_bus_lock_is_single_owner(tmp_path):
    lock_path = tmp_path / "command_bus.lock"
    first = lock_path.open("a+")
    second = lock_path.open("a+")
    try:
        fcntl.flock(first.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            fcntl.flock(second.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            pass
        else:
            raise AssertionError("second command-bus owner acquired the lock")
    finally:
        second.close()
        first.close()
