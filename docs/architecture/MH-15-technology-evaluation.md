# MH-15 — Technology Evaluation

Status: EVALUATION ONLY; NO IMPLEMENTATION AUTHORIZATION

| Technology/mechanism | Role | Status | Gate |
|---|---|---|---|
| Apple Mac mini Server 2011 | candidate host hardware | CANDIDATE | forensic qualification |
| Linux distribution | candidate host OS | CANDIDATE | compatibility + lifecycle ADR |
| systemd | host lifecycle/supervision | CANDIDATE | implementation evidence + ADR |
| Containers | deployment/isolation | CANDIDATE | threat model + ADR |
| AppArmor/SELinux | mandatory-access-control candidate | CANDIDATE | OS compatibility/security review |
| seccomp | syscall restriction candidate | CANDIDATE | service threat model |
| namespaces/cgroups | process/resource isolation | CANDIDATE | runtime compatibility |
| Host firewall | network exposure control | CANDIDATE | network model + verification |
| Signed artifacts/SBOM | supply-chain controls | REQUIRED DIRECTION | concrete toolchain evidence |

## Evaluation rules

- No technology becomes canonical merely because it is common or convenient.
- Selection requires compatibility, security, lifecycle, reproducibility, recovery and resource evidence.
- Host mechanisms never acquire canonical MediaHub state authority.
- Technology choice does not authorize installation or configuration.

## Current verdict

No host technology stack is ACCEPTED/FROZEN. Exact OS, kernel, supervisor, container runtime and sandbox combination remain REQUIRES VERIFICATION.
