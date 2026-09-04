# MH-23 Contract Versioning

Changes are classified as safe additive, potentially breaking, or breaking. Additive fields/features require unknown-field, default, validation, security and semantic analysis. Semantic/default/authorization/lifecycle/error changes are potentially breaking. Removal of required fields, capability meaning changes, command-semantic changes, State Authority changes or security-boundary changes are breaking.

Breaking changes require explicit version, migration, rollback constraints, tests, evidence and governance.