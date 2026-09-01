#!/usr/bin/env python3
"""Minimal, offline-first development-host bootstrap for MediaHub OS."""
import argparse, hashlib, json, os, pathlib, platform, shutil, tarfile, tempfile
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "dev-host.json"

def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load():
    return json.loads(CONFIG.read_text(encoding="utf-8"))

def expand(p):
    return pathlib.Path(os.path.expanduser(p))

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def layout(_args):
    cfg = load(); created = []
    for name, value in cfg["paths"].items():
        if name == "secrets": continue
        p = expand(value); p.mkdir(parents=True, exist_ok=True); created.append(str(p))
    print(json.dumps({"status":"LAYOUT_READY","paths":created}, indent=2))

def doctor(_args):
    cfg = load()
    checks = {
        "platform": platform.system(),
        "offline_first": cfg["network"]["default"] == "offline_first",
        "ai_inference_disabled": cfg["resource_policy"]["ai_inference"] == "disabled_by_default",
        "secrets_external": cfg["paths"]["secrets"] == "KEYCHAIN_OR_ENV_ONLY",
        "worker_master_write_forbidden": cfg["authority"]["worker_direct_master_write"] == "FORBIDDEN",
        "deploy_requires_release_artifact": cfg["authority"]["product_deploy"] == "RELEASE_ARTIFACT_ONLY",
    }
    ok = all(v for k, v in checks.items() if isinstance(v, bool))
    print(json.dumps({"status":"OK" if ok else "REVIEW","checks":checks}, indent=2))
    return 0 if ok else 1

def package(args):
    cfg = load(); source = pathlib.Path(args.source).resolve()
    outdir = expand(cfg["paths"]["packages"]); outdir.mkdir(parents=True, exist_ok=True)
    release = args.release; archive = outdir / f"mediahub-os-{release}.tar.gz"
    manifest = {"schema":"mhx-release-package-1.0","release":release,"created_at":now(),"source":str(source),"target":cfg["product_target"]["host_identity"],"deployment":"PACKAGE_THEN_INSTALL"}
    with tempfile.TemporaryDirectory() as td:
        staging = pathlib.Path(td) / "mediahub-os"
        shutil.copytree(source, staging, ignore=shutil.ignore_patterns(".git", ".mhx", "__pycache__"))
        (staging / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        with tarfile.open(archive, "w:gz") as tf: tf.add(staging, arcname="mediahub-os")
    manifest["package"] = archive.name; manifest["package_sha256"] = digest(archive)
    (outdir / f"mediahub-os-{release}.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2)); return 0

def main():
    p = argparse.ArgumentParser(prog="mhx-host"); s = p.add_subparsers(dest="command", required=True)
    s.add_parser("layout").set_defaults(func=layout); s.add_parser("doctor").set_defaults(func=doctor)
    q = s.add_parser("package"); q.add_argument("source"); q.add_argument("release"); q.set_defaults(func=package)
    args = p.parse_args(); return args.func(args)

if __name__ == "__main__": raise SystemExit(main())
