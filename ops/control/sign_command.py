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

def validate_command_shape(command: dict, now: int | None = None) -> None:
    if not isinstance(command, dict): raise ValueError("command must be a JSON object")
    if command.get("schema_version") != SCHEMA_VERSION: raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
    missing=[k for k in REQUIRED_FIELDS if k not in command]
    if missing: raise ValueError("missing required command fields: "+",".join(missing))
    if not isinstance(command["command_id"], str) or not command["command_id"] or len(command["command_id"])>128: raise ValueError("command_id must be a non-empty string <=128 chars")
    if not isinstance(command["node_id"], str) or not command["node_id"]: raise ValueError("node_id must be a non-empty string")
    if not isinstance(command["operation"], str) or not command["operation"]: raise ValueError("operation must be a non-empty string")
    if type(command["issued_at"]) is not int: raise ValueError("issued_at must be an integer Unix timestamp")
    current_time = int(time.time()) if now is None else int(now)
    if abs(current_time-command["issued_at"])>MAX_AGE_SECONDS: raise ValueError("command issued_at is outside the accepted freshness window")

def verify_signed_command(
    command: dict,
    key: str,
    *,
    expected_node_id: str,
    expected_operation: str,
    expected_target_sha: str,
    allowed_paths: set[str] | frozenset[str],
    now: int | None = None,
) -> dict:
    """Verify a signed command against separately supplied trusted admission context.

    This function verifies integrity and exact bindings only. Callers must obtain the
    key and expected bindings/allowed_paths from authenticated policy context; values
    supplied by the command or model output are not an authority source.
    """
    if not key:
        raise ValueError("node-specific HMAC key is required")
    validate_command_shape(command, now=now)
    allowed_fields = set(REQUIRED_FIELDS) | {"signature"}
    unexpected = sorted(set(command) - allowed_fields)
    if unexpected:
        raise ValueError("unexpected command fields: " + ",".join(unexpected))
    signature = command.get("signature")
    if not isinstance(signature, str) or len(signature) != 64 or any(c not in "0123456789abcdef" for c in signature):
        raise ValueError("signature must be a lowercase HMAC-SHA256 hex digest")
    expected_signature = hmac.new(
        key.encode("utf-8"), canonical_command_body(command), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("command signature verification failed")
    if not expected_node_id or command["node_id"] != expected_node_id:
        raise ValueError("command node_id does not match trusted admission context")
    if not expected_operation or command["operation"] != expected_operation:
        raise ValueError("command operation does not match trusted admission context")
    if not expected_target_sha or command["target_sha"] != expected_target_sha:
        raise ValueError("command target_sha does not match trusted admission context")
    target_sha = command["target_sha"]
    if not isinstance(target_sha, str) or len(target_sha) != 40 or any(c not in "0123456789abcdef" for c in target_sha):
        raise ValueError("target_sha must be a lowercase 40-character Git commit SHA")
    if command["workflow_only"] is not True:
        raise ValueError("only workflow_only commands are accepted by this verifier")
    owned_paths = command["owned_paths"]
    if not isinstance(owned_paths, list) or not owned_paths or any(not isinstance(p, str) or not p for p in owned_paths):
        raise ValueError("owned_paths must be a non-empty list of paths")
    if len(owned_paths) != len(set(owned_paths)):
        raise ValueError("owned_paths must not contain duplicates")
    for path in owned_paths:
        parts = path.split("/")
        if path.startswith("/") or chr(92) in path or ":" in path or any(part in {"", ".", ".."} for part in parts) or ".git" in parts:
            raise ValueError("owned_paths contains an unsafe path")
    if not isinstance(allowed_paths, (set, frozenset)) or not allowed_paths:
        raise ValueError("trusted allowed_paths must be a non-empty set")
    if not set(owned_paths).issubset(allowed_paths):
        raise ValueError("owned_paths exceed trusted allowed_paths")
    issued_at = command["issued_at"]
    current_time = int(time.time()) if now is None else int(now)
    if abs(current_time - issued_at) > MAX_AGE_SECONDS:
        raise ValueError("command issued_at is outside the accepted freshness window")
    return dict(command)


def key_env_name(node_id: str) -> str:
    mapping = {
        "mh-dev-01": "ASTRA_NODE_HMAC_KEY_MH_DEV_01",
        "mh-dev-02": "ASTRA_NODE_HMAC_KEY_MH_DEV_02",
        "Voktors-Mac-mini.local": "ASTRA_NODE_HMAC_KEY_VOKTORS_MAC",
    }
    try:
        return mapping[node_id]
    except KeyError as exc:
        raise ValueError("unsupported command node_id") from exc


def resolve_node_key(node_id: str) -> str:
    key = os.environ.get(key_env_name(node_id), "")
    if not key:
        raise ValueError(f"{key_env_name(node_id)} is required")
    return key


def sign_command(command: dict, key: str) -> dict:
    if not key: raise ValueError("node-specific HMAC key is required")
    validate_command_shape(command)
    signed=dict(command)
    signed["signature"]=hmac.new(key.encode("utf-8"),canonical_command_body(signed),hashlib.sha256).hexdigest()
    return signed

def sign_file(path: Path) -> None:
    command=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(command,dict): raise ValueError("command file must contain a JSON object")
    if "issued_at" not in command: command["issued_at"]=int(time.time())
    key = resolve_node_key(str(command.get("node_id", "")))
    signed=sign_command(command,key)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(signed,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    tmp.replace(path)

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: sign_command.py <command-json>")
    try: sign_file(Path(sys.argv[1]))
    except (OSError,ValueError,json.JSONDecodeError) as exc: raise SystemExit(f"BLOCKED: {exc}")
