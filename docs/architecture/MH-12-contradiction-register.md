# MH-12 Contradiction Register

C-01 Security authorization vs P0-05 transaction authorization: REQUIRES VERIFICATION / governance resolution before mutation authorization changes.
C-02 P0-07 capability authorization vs P0-04 transaction authorization: BLOCKED by approved API/authorization bridge gap.
C-03 Recovery vs State Authority: recovery must use explicit separate gate; no silent bypass.
C-04 Update vs runtime authority: update cannot increase privilege silently.
C-05 Diagnostic access vs sensitive runtime operations: normal authorization path remains mandatory.
C-06 Observability vs enforcement: RESOLVED — observability reports; security enforces.

No contradiction may be resolved by silently changing a frozen baseline.
