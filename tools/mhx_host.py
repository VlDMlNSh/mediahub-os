#!/usr/bin/env python3
"""Minimal, offline-first development-host bootstrap for MediaHub OS."""
import argparse, hashlib, json, os, pathlib, platform, shutil, sys, tarfile, tempfile
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "dev-host.json"
SENSITIVE_NAMES = {".env", ".env.local", ".env.production", "credentials.json", "secrets.json", "id_rsa", "id_ed25519", "known_hosts", "authorized_keys"}
SENSITIVE_DIRS = {".ssh", ".gnupg", ".aws", "keychain", "secrets"}

def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
def load(): return json.loads(CONFIG.read_text(encoding="utf-8"))
def expand(p): return pathlib.Path(os.path.expanduser(p))
def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""): h.update(block)
    return h.hexdigest()

def validate_source(source):
    violations = []
    for p in source.rglob("*"):
        rel = p.relative_to(source)
        if any(part in SENSITIVE_DIRS for part in rel.parts) or rel.name in SENSITIVE_NAMES or rel.name.startswith(".env."):
            violations.append({"path": rel.as_posix(), "reason": "sensitive_path"})
        if p.is_symlink(): violations.append({"path": rel.as_posix(), "reason": "symlink_not_allowed"})
    return violations

def layout(_args):
    cfg = load(); created = []
    for name, value in cfg["paths"].items():
        if name == "secrets": continue
        p = expand(value); p.mkdir(parents=True, exist_ok=True); created.append(str(p))
    print(json.dumps({"status":"LAYOUT_READY","paths":created}, indent=2))

def doctor(_args):
    cfg = load()
    checks = {"platform": platform.system(), "offline_first": cfg["network"]["default"] == "offline_first", "ai_inference_disabled": cfg["resource_policy"]["ai_inference"] == "disabled_by_default", "secrets_external": cfg["paths"]["secrets"] == "KEYCHAIN_OR_ENV_ONLY", "worker_master_write_forbidden": cfg["authority"]["worker_direct_master_write"] == "FORBIDDEN", "deploy_requires_release_artifact": cfg["authority"]["product_deploy"] == "RELEASE_ARTIFACT_ONLY", "inbound_services_disabled": cfg["network"]["inbound_services"] == "disabled_by_default"}
    ok = all(v for v in checks.values() if isinstance(v, bool))
    print(json.dumps({"status":"OK" if ok else "REVIEW","checks":checks}, indent=2)); return 0 if ok else 1

def package(args):
    cfg = load(); source = pathlib.Path(args.source).resolve()
    if not source.exists() or not source.is_dir(): print("SOURCE_NOT_FOUND", file=sys.stderr); return 2
    violations = validate_source(source)
    if violations:
        print(json.dumps({"status":"PACKAGE_REFUSED","violations":violations}, indent=2)); return 4
    outdir = expand(cfg["paths"]["packages"]); outdir.mkdir(parents=True, exist_ok=True)
    release = args.release; archive = outdir / f"mediahub-os-{release}.tar.gz"
    manifest = {"schema":"mhx-release-package-1.1","release":release,"created_at":now(),"source":"LOCAL_WORKSPACE","target":cfg["product_target"]["host_identity"],"deployment":"PACKAGE_THEN_INSTALL","privacy_scan":"PASSED","symlinks":"REJECTED"}
    with tempfile.TemporaryDirectory() as td:
        staging = pathlib.Path(td) / "mediahub-os"
        shutil.copytree(source, staging, ignore=shutil.ignore_patterns(".git", ".mhx", "__pycache__"), symlinks=False)
        (staging / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        with tarfile.open(archive, "w:gz") as tf: tf.add(staging, arcname="mediahub-os", recursive=True)
    manifest["package"] = archive.name; manifest["package_sha256"] = digest(archive)
    (outdir / f"mediahub-os-{release}.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2)); return 0

def main():
    p = argparse.ArgumentParser(prog="mhx-host"); s = p.add_subparsers(dest="command", required=True)
    s.add_parser("layout").set_defaults(func=layout); s.add_parser("doctor").set_defaults(func=doctor)
    q = s.add_parser("package"); q.add_argument("source"); q.add_argument("release"); q.set_defaults(func=package)
    args = p.parse_args(); return args.func(args)

if __name__ == "__main__": raise SystemExit(main())
