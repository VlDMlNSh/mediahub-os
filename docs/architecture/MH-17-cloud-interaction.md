# MH-17 — Cloud Interaction

**Status:** PROPOSED / CANDIDATE

Cloud services are external integration participants and untrusted by default. Cloud-originated intents MUST enter the same identity, policy, authorization, scope, safety, and State Authority boundaries as local consumers.

There is no `Cloud → Device` unrestricted direct path. Loss of cloud connectivity MUST NOT remove local safety or previously authorized local operation.

Cloud telemetry and synchronization are evidence/coordination channels; they do not become canonical authority merely by persistence or remote origin.
