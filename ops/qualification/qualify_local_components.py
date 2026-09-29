#!/usr/bin/env python3
"""Bounded, read-only qualification of discovered local MediaHub/Astra components."""
from __future__ import annotations
import hashlib, json, os, platform, shutil, subprocess, time
from pathlib import Path

COMPONENTS = [
    ("OmniRoute", ["omniroute"], ["--version"]),
    ("free-claude-code", ["free-claude-code"], ["--version"]),
    ("free-coding-models", ["free-coding-models"], ["--version"]),
    ("Claude Code", ["claude"], ["--version"]),
    ("Codex CLI", ["codex"], ["--version"]),
    ("Node.js", ["node"], ["--version"]),
    ("Bun", ["bun"], ["--version"]),
    ("Ollama", ["ollama"], ["--version"]),
    ("llama.cpp", ["llama-server","llama-cli"], ["--version"]),
    ("FFmpeg", ["ffmpeg"], ["-version"]),
    ("RAUC", ["rauc"], ["--version"]),
    ("restic", ["restic"], ["version"]),
    ("OpenBao", ["bao"], ["version"]),
    ("SOPS", ["sops"], ["--version"]),
    ("age", ["age"], ["--version"]),
    ("Cosign", ["cosign"], ["version"]),
    ("Syft", ["syft"], ["version"]),
    ("Trivy", ["trivy"], ["--version"]),
    ("Prometheus", ["prometheus"], ["--version"]),
    ("PostgreSQL", ["psql"], ["--version"]),
    ("NATS", ["nats-server"], ["--version"]),
    ("etcd", ["etcd"], ["--version"]),
    ("protobuf", ["protoc"], ["--version"]),
]

def run(argv, timeout=10):
    try:
        p=subprocess.run(argv,text=True,capture_output=True,timeout=timeout,check=False)
        return {"returncode":p.returncode,"stdout":p.stdout[-3000:],"stderr":p.stderr[-2000:]}
    except Exception as e:
        return {"returncode":-1,"error":type(e).__name__}

def main():
    records=[]
    for name, exes, args in COMPONENTS:
        exe=next((shutil.which(x) for x in exes if shutil.which(x)),None)
        if not exe:
            records.append({"component":name,"state":"NOT_FOUND"}); continue
        v=run([exe,*args])
        ok=v["returncode"]==0
        records.append({"component":name,"state":"RUNTIME_PASS" if ok else "RUNTIME_FAIL","executable":exe,"version_probe":v})
    processes=run(["ps","-eo","pid=,comm=,args="])
    relevant=[x[-2500:] for x in processes.get("stdout","").splitlines() if any(n in x.lower() for n in ("omniroute","free-claude-code","fcc-server","free-coding-models","openflux","claude","astra"))]
    qualified=[r["component"] for r in records if r["state"]=="RUNTIME_PASS"]
    evidence=json.dumps({"records":records,"relevant_processes":relevant,"node":platform.node()},sort_keys=True).encode()
    result={"schema":"mediahub.local-component-qualification.v1","status":"PASS" if qualified else "BLOCKED","node_id":platform.node(),"qualified_runtime_components":qualified,"records":records,"relevant_processes":relevant,"evidence_digest":"sha256:"+hashlib.sha256(evidence).hexdigest(),"secret_values":"SUPPRESSED"}
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if qualified else 2)
if __name__=="__main__": main()
