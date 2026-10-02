#!/usr/bin/env python3
"""Independent A3 bundle verifier. It never upgrades BLOCKED evidence."""
import argparse, json
from pathlib import Path

REQUIRED = {
    "G4": "g4-115.json",
    "G5": "g5-concurrency.json",
    "G6": "g6-recovery.json",
}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("evidence_dir", type=Path)
    p.add_argument("--source-sha", required=True)
    a = p.parse_args()
    blocked = []
    items = {}
    for key, name in REQUIRED.items():
        path = a.evidence_dir / name
        if not path.is_file():
            blocked.append(key + "_missing")
            continue
        try: data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            blocked.append(key + "_invalid_json")
            continue
        items[key] = data
        if data.get("status") != "PASS": blocked.append(key + "_not_PASS")
        if data.get("source_sha") != a.source_sha: blocked.append(key + "_source_sha_mismatch")
    result = {
        "schema": "mediahub.astra-gold.a3-verification.v1",
        "status": "PASS" if not blocked else "BLOCKED",
        "verifier_role": "A3",
        "independent": True,
        "source_sha": a.source_sha,
        "blocked_reasons": blocked,
        "checked_items": sorted(items),
        "secret_values": "SUPPRESSED",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
