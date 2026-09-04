# MH-15 — Reverse Master Prompt

Return implementation evidence to MH-15 architecture authority.

Report only facts supported by current evidence. For each item provide: STATUS, EVIDENCE, IMPACT, ARCHITECTURAL CONFORMANCE, UNKNOWNs, and REQUIRED FOLLOW-UP.

STATUS values: VERIFIED / OBSERVED / PROPOSED / UNKNOWN / REQUIRES VERIFICATION / NOT AUTHORIZED / ACCEPTED.

Check specifically: hardware identity; firmware/EFI; bootloader; kernel; OS; systemd; process/service identities; capabilities; filesystem and mounts; temporary storage; devices; network/firewall; sandboxing; secrets; CI/build; supply chain; update path; recovery; resource limits; thermal/power; time; observability; failure domains; privileged operations; shell access; development/production separation.

Never convert an implementation observation into domain authority. Explicitly flag any path where host privilege, filesystem mutation, shell execution, device access, container privilege, or administrator action could bypass MediaHub authorization or State Authority.

Do not recommend implementation changes inside this response unless they are framed as architecture findings requiring ADR/governance.

Final verdict must state whether evidence is sufficient for the relevant MH-15 acceptance gate. If not, return REQUIRES VERIFICATION.
