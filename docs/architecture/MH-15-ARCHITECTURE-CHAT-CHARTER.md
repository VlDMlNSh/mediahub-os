# MH-15 — Architecture Chat Charter

Status: ARCHITECTURE WORK IN PROGRESS

## Purpose

MH-15 is the authoritative architecture discussion for OS / Appliance architecture of MediaHub OS 11.x LTS / MediaHub iOS.

## Scope

Host hardware, firmware/boot boundary, kernel, host OS, runtime host, process/service model, least privilege, systemd, containerization, filesystem, devices, network, firewall, hardening, CI/build, supply chain, updates, recovery, resources, thermal/power, time, observability, failure domains, privileged operations, secrets, sandboxing, legacy hardware, OS lifecycle, and appliance qualification.

## Non-scope

This chat MUST NOT perform implementation or become a development workspace. It may define architecture, decisions, invariants, evidence requirements, acceptance criteria, and master/reverse-master prompts.

## Authority invariant

The host provides execution; MediaHub defines authority.

Hardware, firmware, kernel, OS, systemd, container runtime, filesystem, database, shell, administrator, and observability are infrastructure mechanisms and MUST NOT silently become canonical MediaHub State Authority.

## Governance

Architecture -> ADR -> Governance Authorization -> Implementation -> Verification -> Evidence -> Acceptance.

MH-15 does not authorize OS installation, storage mutation, firmware/kernel changes, container installation, firewall deployment, hardening deployment, or persistence implementation.

## Evidence rule

Unknown hardware/software properties remain UNKNOWN / REQUIRES VERIFICATION. No production claim may be inferred from assumptions.
