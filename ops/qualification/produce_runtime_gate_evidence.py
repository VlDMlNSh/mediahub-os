#!/usr/bin/env python3
"""Fail-closed normalizer for fresh G5/G6 runtime evidence."""
import argparse, hashlib, json

RULES = {
    "G5_CONCURRENCY": ["concurrent_claims", "disjoint_workspaces", "overlap_observed", "duplicate_controller_rejected"],
    "G6_RECOVERY": ["timeout", "executor_failure", "transport_interruption", "stale_claim", "worker_restart", "duplicate_controller", "replay_idempotency", "result_publication_recovery"],
}

def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("gate", choices=sorted(RULES))
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--expected-sha")
    a = p.parse_args()
    raw = json.load(open(a.input, encoding="utf-8"))
    blocked = []
    if raw.get("schema") != "mediahub.astra-gold.runtime-observation.v1": blocked.append("invalid_observation_schema")
    if raw.get("gate") != a.gate: blocked.append("gate_mismatch")
    if raw.get("status") != "PASS": blocked.append("source_observation_not_PASS")
    if a.expected_sha and raw.get("source_sha") != a.expected_sha: blocked.append("source_sha_mismatch")
    if raw.get("independent_runtime_identity") is not True: blocked.append("independent_runtime_identity_missing")
    obs = raw.get("observations") if isinstance(raw.get("observations"), dict) else {}
    for key in RULES[a.gate]:
        if obs.get(key) is not True: blocked.append("observation_not_PASS:"+key)
    result = {"schema":"mediahub.astra-gold.runtime-gate-evidence.v1","status":"PASS" if not blocked else "BLOCKED","gate":a.gate,"source_sha":raw.get("source_sha"),"observations":obs,"blocked_reasons":blocked,"secret_values":"SUPPRESSED"}
    result["evidence_digest"] = digest(result)
    with open(a.output, "w", encoding="utf-8") as f: json.dump(result, f, indent=2, sort_keys=True); f.write("\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
