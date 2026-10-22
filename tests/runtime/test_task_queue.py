from mediahub_runtime import FileTaskQueue, TaskQueueError


def contract(request_id):
    return {"request_id": request_id, "user_command": "bounded"}


def test_enqueue_is_idempotent(tmp_path):
    q = FileTaskQueue(tmp_path)
    first = q.enqueue(contract("r1"))
    second = q.enqueue(contract("r1"))
    assert first == second
    assert len(list((tmp_path / "inbox").glob("*.json"))) == 1


def test_claim_complete_moves_atomically(tmp_path):
    q = FileTaskQueue(tmp_path, lease_seconds=10, clock=lambda: 100.0)
    q.enqueue(contract("r2"))
    lease = q.claim("worker-a")
    assert lease and lease.request_id == "r2"
    assert not (tmp_path / "inbox" / "r2.json").exists()
    assert (tmp_path / "running" / "r2.json").exists()
    q.complete(lease, {"status": "PASS"})
    assert (tmp_path / "done" / "r2.json").exists()
    assert not (tmp_path / "running" / "r2.json").exists()


def test_expired_lease_recovers_to_inbox(tmp_path):
    ticks = iter((100.0, 200.0))
    q = FileTaskQueue(tmp_path, lease_seconds=10, clock=lambda: next(ticks))
    q.enqueue(contract("r3"))
    lease = q.claim("worker-a")
    assert lease
    assert q.recover_expired() == 1
    assert (tmp_path / "inbox" / "r3.json").exists()


def test_wrong_owner_cannot_complete(tmp_path):
    q = FileTaskQueue(tmp_path, lease_seconds=10, clock=lambda: 100.0)
    q.enqueue(contract("r4"))
    lease = q.claim("worker-a")
    bad = type(lease)(lease.request_id, "worker-b", lease.leased_until)
    try:
        q.complete(bad, {})
    except TaskQueueError as exc:
        assert exc.code == "lease_mismatch"
    else:
        raise AssertionError("lease mismatch was not rejected")


def test_request_id_path_traversal_is_rejected(tmp_path):
    q = FileTaskQueue(tmp_path)
    try:
        q.enqueue(contract("../escape"))
    except TaskQueueError as exc:
        assert exc.code == "invalid_request_id"
    else:
        raise AssertionError("unsafe request id accepted")


def test_done_record_has_immutable_lineage_and_verifies(tmp_path):
    q = FileTaskQueue(tmp_path, lease_seconds=10, clock=lambda: 100.0)
    q.enqueue(contract("r5"))
    lease = q.claim("worker-a")
    q.complete(lease, {"status": "PASS", "output_sha256": "abc"})
    assert q.verify_lineage("r5") is True


def test_done_record_tampering_is_rejected(tmp_path):
    q = FileTaskQueue(tmp_path, lease_seconds=10, clock=lambda: 100.0)
    q.enqueue(contract("r6"))
    lease = q.claim("worker-a")
    q.complete(lease, {"status": "PASS"})
    path = tmp_path / "done" / "r6.json"
    data = __import__("json").loads(path.read_text())
    data["evidence"]["status"] = "FAIL"
    path.write_text(__import__("json").dumps(data))
    try:
        q.verify_lineage("r6")
    except TaskQueueError as exc:
        assert exc.code == "lineage_mismatch"
    else:
        raise AssertionError("tampered lineage was accepted")
