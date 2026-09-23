#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOSTS = ROOT / ".mediahub" / "hosts"

for path in sorted(HOSTS.glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_id") != "mediahub.astra.host-registration":
        raise SystemExit(f"invalid schema: {path}")
    if data.get("location_binding") != "none":
        raise SystemExit(f"host is location-bound: {path}")
    if data.get("credentials_in_repository") is not False:
        raise SystemExit(f"credentials in repository: {path}")
    if data.get("approval_state") not in {"pending", "approved"}:
        raise SystemExit(f"invalid approval state: {path}")

print("HOST_REGISTRATION=PASS")
