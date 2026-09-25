from ops.astra_node_agent import valid_command

def test_valid_command_accepts_bounded_target():
    assert valid_command({
        "schema": 1, "command_id": "c1", "target": "dev2",
        "action": "STATUS", "expires_at": "2099-01-01T00:00:00Z",
    })

def test_valid_command_rejects_unknown_action():
    assert not valid_command({
        "schema": 1, "command_id": "c2", "target": "dev2",
        "action": "SHELL", "expires_at": "2099-01-01T00:00:00Z",
    })

def test_valid_command_rejects_wrong_target():
    assert not valid_command({
        "schema": 1, "command_id": "c3", "target": "dev3",
        "action": "STATUS", "expires_at": "2099-01-01T00:00:00Z",
    })

def test_valid_command_rejects_expired():
    assert not valid_command({
        "schema": 1, "command_id": "c4", "target": "dev2",
        "action": "SYNC", "expires_at": "2000-01-01T00:00:00Z",
    })
