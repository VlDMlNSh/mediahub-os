#!/usr/bin/env python3
"""Read-only discovery/qualification preflight for the OpenFlux desktop-agent candidate."""
from __future__ import annotations
import hashlib, json, os, platform, shutil, subprocess
from pathlib import Path


def probe(argv, timeout=8):
    try:
        p = subprocess.run(argv, text=True, capture_output=True, timeout=timeout, check=False)
        return {"returncode": p.returncode, "stdout": p.stdout[-2000:], "stderr": p.stderr[-1000:]}
    except Exception as exc:
        return {"returncode": -1, "error": type(exc).__name__}


def main():
    candidates = []
    for path in (
        "/Applications/OpenFlux.app",
        str(Path.home() / "Applications/OpenFlux.app"),
        "/opt/OpenFlux/OpenFlux.AppImage",
        "/opt/openflux",
        str(Path.home() / "OpenFlux"),
        str(Path.home() / ".local/bin/openflux"),
    ):
        if Path(path).exists():
            candidates.append(path)

    executable = shutil.which("openflux")
    executable_probe = None
    if executable:
        executable_probe = {"path": executable, "probe": probe([executable, "--version"])}

    process_probe = probe(["ps", "-eo", "pid=,comm=,args="])
    processes = [
        line[-2500:]
        for line in process_probe.get("stdout", "").splitlines()
        if "openflux" in line.lower()
    ]

    evidence = {
        "node": platform.node(),
        "platform": platform.platform(),
        "candidate_paths": candidates,
        "executable": executable_probe,
        "processes": processes,
        "secret_values": "SUPPRESSED",
    }
    digest = hashlib.sha256(json.dumps(evidence, sort_keys=True).encode()).hexdigest()
    state = "DISCOVERED" if candidates or executable or processes else "NOT_FOUND"
    result = {
        "schema": "mediahub.openflux-qualification-preflight.v1",
        "component": "openflux",
        "identity": "EDEAI/OpenFlux",
        "state": state,
        "qualification": "NOT_PROVEN",
        "next_gates": [
            "identity_provenance",
            "version_integrity",
            "sandbox_boundary",
            "non_mutating_probe",
            "isolated_workspace_execution",
            "result_validation",
            "recovery",
            "independent_a3_verification",
        ],
        "evidence": evidence,
        "evidence_digest": "sha256:" + digest,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0)


if __name__ == "__main__":
    main()
