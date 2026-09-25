#!/usr/bin/env python3
"""Fail-closed installer driven only by trusted, hashed manifests."""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess,sys,tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT=Path(os.environ.get("MEDIAHUB_ROOT","/home/mediahub/dev/mediahub-os-autonomous")).resolve()
MANIFEST=ROOT/"config"/"astra_executor_install_manifest.json"
ALLOWED=frozenset({"aider","goose","openhands","qodo","pr-agent","pullfrog","sweep","tabby"})
@dataclass(frozen=True)
class InstallSpec:
    name:str; package:str; version:str; sha256:str; executable:str; index_url:str|None=None

def prefix()->Path:
    p=Path(os.environ.get("MEDIAHUB_EXECUTOR_PREFIX",str(Path.home()/".local/mediahub-executors"))).expanduser().resolve()
    if ROOT==p or ROOT in p.parents: raise ValueError("executor prefix inside repository")
    p.mkdir(parents=True,exist_ok=True); return p

def specs()->tuple[InstallSpec,...]:
    if not MANIFEST.exists(): return ()
    d=json.loads(MANIFEST.read_text(encoding="utf-8"))
    if d.get("schema_version")!=1: raise ValueError("unsupported manifest")
    out=[]
    for r in d.get("executors",[]):
        if r.get("name") not in ALLOWED: raise ValueError("executor not allowlisted")
        digest=str(r.get("sha256","")).lower()
        if len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest): raise ValueError("invalid SHA-256")
        out.append(InstallSpec(str(r["name"]),str(r["package"]),str(r["version"]),digest,str(r["executable"]),r.get("index_url")))
    return tuple(out)

def run(argv:list[str],timeout:int=180):
    if not argv or any(not isinstance(x,str) or not x for x in argv): raise ValueError("invalid argv")
    return subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout,check=False)

def install(s:InstallSpec)->dict:
    p=prefix()/s.name; p.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="astra-install-") as td:
        wheel_dir=Path(td); argv=[sys.executable,"-m","pip","download","--disable-pip-version-check","--no-deps","--only-binary=:all:","--dest",str(wheel_dir),f"{s.package}=={s.version}"]
        if s.index_url: argv += ["--index-url",s.index_url]
        r=run(argv)
        if r.returncode: raise RuntimeError(f"download failed: {s.name}")
        wheels=sorted(wheel_dir.glob("*.whl"))
        if len(wheels)!=1: raise RuntimeError(f"expected one wheel: {s.name}")
        digest=hashlib.sha256(wheels[0].read_bytes()).hexdigest()
        if digest!=s.sha256: raise RuntimeError(f"SHA-256 mismatch: {s.name}")
        r=run([sys.executable,"-m","pip","install","--disable-pip-version-check","--no-deps","--no-index","--find-links",str(wheel_dir),"--target",str(p),str(wheels[0])])
        if r.returncode: raise RuntimeError(f"install failed: {s.name}")
    return {"name":s.name,"status":"INSTALLED","version":s.version,"sha256":s.sha256,"prefix":str(p)}

def main(argv:list[str])->int:
    if argv not in (["plan"],["install"]): return 2
    if argv==["plan"]: print(json.dumps({"schema_version":1,"installable":[s.name for s in specs()]},indent=2)); return 0
    print(json.dumps({"schema_version":1,"results":[install(s) for s in specs()]},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main(sys.argv[1:]))
