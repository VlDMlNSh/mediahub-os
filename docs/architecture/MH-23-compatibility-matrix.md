# MH-23 Compatibility Matrix

| Producer | Consumer | Contract | Version | Supported Range | Migration | Rollback | Status |
|---|---|---|---|---|---|---|---|
| State Authority | Runtime | P0-03/P0-06 | frozen baseline | REQUIRES VERIFICATION | validated migration only | explicit | FROZEN/VERIFY LINEAGE |
| Consumer Boundary | Runtime | P0-05 | frozen baseline | REQUIRES VERIFICATION | contract migration | explicit | FROZEN/VERIFY LINEAGE |
| Configuration/Policy | Runtime | P0-07 | candidate | TBD | required | explicit | NOT FROZEN |
| UI | Consumer Boundary | consumer API | TBD | TBD | required | explicit | UNKNOWN |
| AI | Consumer Boundary | AI/tool contract | TBD | TBD | required | explicit | NON-AUTHORITATIVE |
| Plugins | Runtime | plugin API | TBD | TBD | required | quarantine | UNKNOWN |
| Devices | Protocol adapter | device contract | TBD | TBD | enrollment | firmware-dependent | UNKNOWN |
| Media | Media services | media/metadata | TBD | TBD | rebuild/transform | source-preserving | UNKNOWN |
| Knowledge Graph | Consumers | ontology | TBD | TBD | semantic migration | explicit | UNKNOWN |
| Persistence contract | State Authority | persistence contract | TBD | TBD | storage-specific | explicit | NOT AUTHORIZED |
| Installer/Update | OS/Runtime | lifecycle | TBD | TBD | playbook | recovery | UNKNOWN |
| Recovery | Runtime | recovery contract | TBD | TBD | explicit | independently trusted | UNKNOWN |
| Cloud | adapters | provider contract | TBD | TBD | provider migration | explicit | EXTERNAL/UNTRUSTED |
| OS | Runtime | host contract | TBD | TBD | qualification | boot/recovery | UNKNOWN |
| Hardware | OS/Runtime | capability contract | TBD | TBD | qualification | hardware-specific | REQUIRES VERIFICATION |