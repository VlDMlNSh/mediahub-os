#!/usr/bin/env python3
"""Read-only inventory of locally installed MediaHub/Astra runtime components."""
from __future__ import annotations
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path

KNOWN = [
    ("OmniRoute", ["omniroute", "omni-route", "omni"], ["/opt/omniroute", "/usr/local/bin/omniroute", "/usr/bin/omniroute"]),
    ("free-claude-code", ["free-claude-code", "claude"], ["/opt/free-claude-code", "/usr/local/bin/claude", "/usr/bin/claude"]),
    ("OpenFlux", ["openflux"], ["/opt/openflux", "/usr/local/bin/openflux", "/usr/bin/openflux"]),
    ("Ollama", ["ollama"], ["/usr/local/bin/ollama", "/usr/bin/ollama"]),
    ("llama.cpp", ["llama-server", "llama-cli"], ["/opt/llama.cpp", "/usr/local/bin/llama-server", "/usr/local/bin/llama-cli"]),
    ("ONNX Runtime", [], ["/opt/onnxruntime"]),
    ("FFmpeg", ["ffmpeg"], ["/usr/bin/ffmpeg", "/usr/local/bin/ffmpeg"]),
    ("OpenCV", [], []),
    ("PaddleOCR", [], []),
    ("Home Assistant", ["hass"], ["/opt/homeassistant", "/srv/homeassistant"]),
    ("RAUC", ["rauc"], ["/usr/bin/rauc", "/usr/local/bin/rauc"]),
    ("restic", ["restic"], ["/usr/bin/restic", "/usr/local/bin/restic"]),
    ("OpenBao", ["bao"], ["/usr/bin/bao", "/usr/local/bin/bao"]),
    ("SOPS", ["sops"], ["/usr/bin/sops", "/usr/local/bin/sops"]),
    ("age", ["age"], ["/usr/bin/age", "/usr/local/bin/age"]),
    ("Cosign", ["cosign"], ["/usr/bin/cosign", "/usr/local/bin/cosign"]),
    ("Syft", ["syft"], ["/usr/bin/syft", "/usr/local/bin/syft"]),
    ("Trivy", ["trivy"], ["/usr/bin/trivy", "/usr/local/bin/trivy"]),
    ("OpenTelemetry", [], ["/opt/opentelemetry"]),
    ("Prometheus", ["prometheus"], ["/usr/bin/prometheus", "/usr/local/bin/prometheus"]),
    ("PostgreSQL", ["psql", "postgres"], ["/usr/bin/psql", "/usr/lib/postgresql"]),
    ("pgvector", [], []),
    ("NATS", ["nats-server"], ["/usr/bin/nats-server", "/usr/local/bin/nats-server"]),
    ("etcd", ["etcd"], ["/usr/bin/etcd", "/usr/local/bin/etcd"]),
    ("gRPC", [], []),
    ("protobuf", ["protoc"], ["/usr/bin/protoc", "/usr/local/bin/protoc"]),
    ("OpenFlux", ["openflux"], ["/opt/openflux", "/usr/local/bin/openflux", "/usr/bin/openflux"]),
]

def cmd(argv, timeout=15):
    try:
        p = subprocess.run(argv, text=True, capture_output=True, timeout=timeout, check=False)
        return {"returncode": p.returncode, "stdout": p.stdout[-12000:], "stderr": p.stderr[-4000:]}
    except Exception as exc:
        return {"error": type(exc).__name__}

def package_versions(names):
    out = {}
    for name in names:
        try:
            out[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            pass
        except Exception:
            out[name] = "error"
    return out

def main():
    records = []
    seen = set()
    for name, executables, paths in KNOWN:
        hits = []
        for exe in executables:
            p = shutil.which(exe)
            if p and p not in hits:
                hits.append(p)
        for raw in paths:
            p = Path(raw)
            if p.exists():
                s = str(p)
                if s not in hits:
                    hits.append(s)
        status = "FOUND" if hits else "NOT_FOUND"
        records.append({"component": name, "status": status, "evidence": hits})
        seen.add(name)

    py_names = [
        "onnxruntime", "opencv-python", "opencv-contrib-python", "paddleocr",
        "grpcio", "protobuf", "opentelemetry-api", "opentelemetry-sdk",
        "psycopg", "psycopg2", "pgvector"
    ]
    python_packages = package_versions(py_names)
    npm = cmd(["npm", "root", "-g"], 10) if shutil.which("npm") else {"returncode": 127, "stdout": "", "stderr": "npm not found"}
    npm_list = cmd(["npm", "list", "-g", "--depth=0", "--json"], 20) if shutil.which("npm") else {"returncode": 127, "stdout": "", "stderr": "npm not found"}
    systemd = cmd(["systemctl", "list-unit-files", "--type=service", "--no-pager", "--no-legend"], 20)
    processes = cmd(["ps", "-eo", "pid=,comm=,args="], 10)

    discovery = []
    needles = ("omni", "claude", "openflux", "astra", "ollama", "llama", "mediahub")
    for line in processes.get("stdout", "").splitlines():
        low = line.lower()
        if any(n in low for n in needles):
            discovery.append(line[-2000:])

    queue = []
    for r in records:
        if r["status"] == "FOUND":
            queue.append({
                "component": r["component"],
                "qualification_state": "DISCOVERED",
                "next_gate": "local_component_runtime_qualification",
                "requirements": ["identity", "version_provenance", "runtime_smoke", "resource_limits", "security_boundary", "recovery_behavior", "evidence_digest"]
            })
    for name, version in python_packages.items():
        queue.append({
            "component": name,
            "qualification_state": "DISCOVERED",
            "next_gate": "local_python_component_qualification",
            "version": version
        })

    result = {
        "schema": "mediahub.local-component-inventory.v1",
        "status": "PASS",
        "node_id": platform.node(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "known_components": records,
        "python_packages": python_packages,
        "npm_global_root": npm,
        "npm_global_inventory": npm_list,
        "systemd_service_inventory": systemd,
        "relevant_processes": discovery,
        "qualification_queue_candidates": queue,
        "secret_values": "SUPPRESSED"
    }
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
