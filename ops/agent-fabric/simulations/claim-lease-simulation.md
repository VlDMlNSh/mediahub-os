# MH-25 Claim / Lease Simulation

Status: TEST PLAN — execution evidence required

## Cases

1. Exact path collision
   - Claim A owns `src/a.py`
   - Claim B requests `src/a.py`
   - Expected: B BLOCKED.

2. Parent/child collision
   - Claim A owns `src`
   - Claim B requests `src/a.py`
   - Expected: B BLOCKED.

3. Independent paths
   - Claim A owns `src/a.py`
   - Claim B owns `tests/b.py`
   - Expected: both may be ACTIVE.

4. Lease heartbeat
   - ACTIVE claim heartbeat extends expiry.
   - Expected: updated timestamp and expiry; status remains ACTIVE.

5. Lease expiry
   - expired claim must not block a new claim.
   - Expected: old claim is not an active conflict.

6. Verification gate
   - READY_FOR_VERIFY cannot become INTEGRATED from worker self-report.
   - Expected: independent verifier evidence required.

## Evidence requirement

Each executed case must record command, environment, exit status and observable result.
