# MH-21 Data Egress Gate

Status: PROPOSED.

Data → Classification → Purpose → Destination → Privacy Policy → Security Policy → Authorization → Redaction/Minimization → Bounded Transfer → External Compute.

Default: deny arbitrary egress. AI output, plugin configuration, retrieved documents and external events cannot select arbitrary destinations. Sensitive/private data requires explicit eligibility and authorization. Secrets are prohibited unless a separate narrowly scoped contract explicitly permits them.
