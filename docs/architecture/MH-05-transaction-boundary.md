# MH-5 — Transaction Boundary

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

The consumer transaction handle is opaque. It identifies an authorized State Authority transaction without exposing the internal transaction object.

Required properties inherited from P0-05/P0-04:

- forged handles are rejected;
- operation-specific authorization applies;
- transaction lifecycle is controlled by State Authority;
- candidate state remains isolated until commit;
- commit is atomic;
- generation/state-version freshness is checked;
- stale commits fail closed;
- abort invalidates the candidate;
- no alternate transaction engine exists in the consumer layer.

The Consumer Boundary may carry a transaction reference but does not own transaction truth. It cannot rebase stale transactions, manufacture generations, select canonical versions, or publish independently.
