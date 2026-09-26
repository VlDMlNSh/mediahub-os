import pytest
from runtime.mediahub_control_plane.lease import LeaseManager

def test_valid_renewal():
    m = LeaseManager(10); lease = m.issue("t", "a", 100)
    renewed = m.renew(lease, "a", 1, 105)
    assert renewed.status.value == "RENEWED" and renewed.expires_at == 115

def test_expired_renewal_rejected():
    m = LeaseManager(10); lease = m.issue("t", "a", 100)
    with pytest.raises(PermissionError): m.renew(lease, "a", 1, 111)

def test_wrong_agent_rejected():
    m = LeaseManager(10); lease = m.issue("t", "a", 100)
    with pytest.raises(PermissionError): m.renew(lease, "b", 1, 105)

def test_stale_generation_rejected():
    m = LeaseManager(10); lease = m.issue("t", "a", 100)
    with pytest.raises(PermissionError): m.renew(lease, "a", 2, 105)

def test_expiry_is_explicit():
    m = LeaseManager(10); lease = m.issue("t", "a", 100)
    expired = m.expire(lease, 111)
    assert expired.status.value == "EXPIRED"
