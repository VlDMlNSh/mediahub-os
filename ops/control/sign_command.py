#!/usr/bin/env python3
"""Authoritative Astra GitHub control-command signer (Option A)."""
from __future__ import annotations
import hashlib, hmac, json, os, sys, time
from pathlib import Path

SCHEMA_VERSION = "mediahub.astra.control-command.v1"
REQUIRED_FIELDS = ("schema_version","command_id","node_id","operation","target_sha","workflow_only","owned_paths","title","description","exclusive_actions","issued_at")
MAX_AGE_SECONDS = max(60, int(os.environ.get("ASTRA_COMMAND_HMAC_MAX_AGE_SECONDS", "900")))

def canonical_command_body(command: dict) -> bytes:
    return json.dumps({k:v for k,v in command.items() if k != "signature"}, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def validate_command_shape(command: dict) -> None:
    if not isinstance(command, dict): raise ValueError("command must be a JSON object")
    if command.get("schema_version") != SCHEMA_VERSION: raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
    missing=[k for k in REQUIRED_FIELDS if k not in command]
    if missing: raise ValueError("missing required command fields: "+",".join(missing))
    if not isinstance(command["command_id"], str) or not command["command_id"] or len(command["command_id"])>128: raise ValueError("command_id must be a non-empty string <=128 chars")
    if not isinstance(command["node_id"], str) or not command["node_id"]: raise ValueError("node_id must be a non-empty string")
    if not isinstance(command["operation"], str) or not command["operation"]: raise ValueError("operation must be a non-empty string")
    if not isinstance(command["issued_at"], int): raise ValueError("issued_at must be an integer Unix timestamp")
    if abs(int(time.time())-command["issued_at"])>MAX_AGE_SECONDS: raise ValueError("command issued_at is outside the accepted freshness window")

def sign_command(command: dict, key: str) -> dict:
    if not key: raise ValueError("ASTRA_COMMAND_HMAC_KEY is required")
    validate_command_shape(command)
    signed=dict(command)
    signed["signature"]=hmac.new(key.encode("utf-8"),canonical_command_body(signed),hashlib.sha256).hexdigest()
    return signed

def sign_file(path: Path) -> None:
    key=os.environ.get("ASTRA_COMMAND_HMAC_KEY","")
    if not key: raise ValueError("ASTRA_COMMAND_HMAC_KEY is required")
    command=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(command,dict): raise ValueError("command file must contain a JSON object")
    if "issued_at" not in command: command["issued_at"]=int(time.time())
    signed=sign_command(command,key)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(signed,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    tmp.replace(path)

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: sign_command.py <command-json>")
    try: sign_file(Path(sys.argv[1]))
    except (OSError,ValueError,json.JSONDecodeError) as exc: raise SystemExit(f"BLOCKED: {exc}")
