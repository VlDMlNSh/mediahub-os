#!/usr/bin/env python3
"""Fail-closed G8 verifier with immutable evidence-manifest binding."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

REQUIRED=("g4_115","g5_coordination","g6_recovery","a3_independent","clean_worktree")
SURFACES=("g4_115","g5_coordination","g6_recovery","a3_independent","clean_worktree")
SHA40=re.compile(r"^[0-9a-fA-F]{40}$")
SHA64=re.compile(r"^[0-9a-f]{64}$")
REQUIRED_EVIDENCE_METADATA=("command_id","node_id","component_id","executor_id","provider_or_model_id","transport_id","source_sha","round","timestamp","exit_status","timeout","workspace","verification_status","evidence_digest")

def verify(path: Path) -> dict:
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: return {"status":"BLOCKED","reason":"invalid_g8_bundle","detail":repr(exc)}
    if data.get("fresh") is not True: return {"status":"BLOCKED","reason":"fresh_g8_bundle_required"}
    missing=[x for x in REQUIRED if data.get(x,{}).get("status")!="PASS"]
    if missing: return {"status":"BLOCKED","reason":"g8_prerequisites_not_passed","missing":missing}
    if data.get("g4_115",{}).get("observations") != 115: return {"status":"BLOCKED","reason":"g4_115_count_invalid"}
    if data.get("g4_115",{}).get("paths") != 5: return {"status":"BLOCKED","reason":"g4_path_count_invalid"}
    if data.get("g5_coordination",{}).get("max_parallel") != 2: return {"status":"BLOCKED","reason":"g5_parallelism_contract_invalid"}
    if data.get("a3_independent",{}).get("independence_attested") is not True: return {"status":"BLOCKED","reason":"a3_independence_missing"}
    if data.get("clean_worktree",{}).get("dirty") is not False: return {"status":"BLOCKED","reason":"worktree_not_clean"}
    source_sha=str(data.get("source_sha",""))
    if not SHA40.fullmatch(source_sha): return {"status":"BLOCKED","reason":"bundle_source_sha_invalid"}
    if data.get("secret_values")!="SUPPRESSED": return {"status":"BLOCKED","reason":"secret_policy_invalid"}
    manifest=data.get("evidence_manifest")
    if not isinstance(manifest,dict): return {"status":"BLOCKED","reason":"evidence_manifest_missing"}
    expected_files={
        "g4_115":"g4-115.json",
        "g5_coordination":"g5-coordination.json",
        "g6_recovery":"g6-recovery.json",
        "a3_independent":"a3-independent.json",
        "clean_worktree":"clean-worktree.json",
    }
    for key in SURFACES:
        ref=manifest.get(key)
        if not isinstance(ref,dict): return {"status":"BLOCKED","reason":"manifest_surface_missing","surface":key}
        evidence_path=Path(str(ref.get("path","")))
        expected_name=expected_files[key]
        if evidence_path.name != expected_name or evidence_path.parent.name != "astra-gold":
            return {"status":"BLOCKED","reason":"manifest_evidence_path_invalid","surface":key}
        expected=str(ref.get("sha256","")).lower()
        if not SHA64.fullmatch(expected): return {"status":"BLOCKED","reason":"manifest_digest_invalid","surface":key}
        if not evidence_path.is_file(): return {"status":"BLOCKED","reason":"manifest_evidence_missing","surface":key}
        actual=hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        if actual!=expected: return {"status":"BLOCKED","reason":"manifest_evidence_digest_mismatch","surface":key}
        try: evidence=json.loads(evidence_path.read_text(encoding="utf-8"))
        except Exception: return {"status":"BLOCKED","reason":"manifest_evidence_json_invalid","surface":key}
        if not isinstance(evidence,dict) or evidence.get("status")!="PASS":
            return {"status":"BLOCKED","reason":"manifest_evidence_not_pass","surface":key}
        missing_metadata=[field for field in REQUIRED_EVIDENCE_METADATA if field not in evidence]
        if missing_metadata:
            return {"status":"BLOCKED","reason":"manifest_evidence_metadata_missing","surface":key,"fields":missing_metadata}
        evidence_digest=str(evidence.get("evidence_digest","")).lower()
        if not SHA64.fullmatch(evidence_digest):
            return {"status":"BLOCKED","reason":"manifest_evidence_digest_invalid","surface":key}
        string_fields=("command_id","node_id","component_id","executor_id","provider_or_model_id","transport_id","workspace","verification_status")
        for field in string_fields:
            if not isinstance(evidence.get(field),str) or not evidence[field].strip():
                return {"status":"BLOCKED","reason":"manifest_evidence_metadata_invalid","surface":key,"field":field}
        placeholder_values={"unknown","undefined","none","null","n/a","na","tbd","todo","placeholder","unset"}
        for field in ("node_id","component_id","executor_id","provider_or_model_id","transport_id","workspace"):
            if evidence[field].strip().lower() in placeholder_values:
                return {"status":"BLOCKED","reason":"manifest_evidence_identity_placeholder","surface":key,"field":field}
        if evidence.get("verification_status") != "PASS": return {"status":"BLOCKED","reason":"manifest_evidence_verification_status_not_pass","surface":key}
        if not isinstance(evidence.get("round"),int) or evidence["round"] < 1:
            return {"status":"BLOCKED","reason":"manifest_evidence_round_invalid","surface":key}
        if not isinstance(evidence.get("timestamp"),(int,float,str)) or (isinstance(evidence.get("timestamp"),str) and not evidence["timestamp"].strip()):
            return {"status":"BLOCKED","reason":"manifest_evidence_timestamp_invalid","surface":key}
        if not isinstance(evidence.get("exit_status"),int):
            return {"status":"BLOCKED","reason":"manifest_evidence_exit_status_invalid","surface":key}
        if not isinstance(evidence.get("timeout"),bool):
            return {"status":"BLOCKED","reason":"manifest_evidence_timeout_invalid","surface":key}
        evidence_canonical=dict(evidence)
        evidence_canonical.pop("evidence_digest",None)
        evidence_actual=hashlib.sha256(json.dumps(evidence_canonical,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
        if evidence_actual != evidence_digest:
            return {"status":"BLOCKED","reason":"manifest_evidence_digest_mismatch","surface":key}
        evidence_sha=str(evidence.get("source_sha",""))
        if not SHA40.fullmatch(evidence_sha) or evidence_sha.lower()!=source_sha.lower():
            return {"status":"BLOCKED","reason":"manifest_evidence_source_sha_mismatch","surface":key}
        if evidence.get("secret_values")!="SUPPRESSED":
            return {"status":"BLOCKED","reason":"manifest_evidence_secret_policy","surface":key}
        summary_fields=("status","observations","paths","max_parallel","independence_attested","dirty","source_sha","target_sha","fresh")
        for field in summary_fields:
            if field in data.get(key,{}) and data[key].get(field) != evidence.get(field):
                return {"status":"BLOCKED","reason":"manifest_summary_mismatch","surface":key,"field":field}
    if set(manifest) != set(SURFACES):
        return {"status":"BLOCKED","reason":"manifest_surface_set_invalid"}
    digest=str(data.get("bundle_sha256","")).lower()
    if not SHA64.fullmatch(digest): return {"status":"BLOCKED","reason":"bundle_integrity_invalid"}
    canonical=dict(data); canonical.pop("bundle_sha256",None)
    actual=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    if actual!=digest: return {"status":"BLOCKED","reason":"bundle_integrity_mismatch"}
    return {"status":"PASS","prerequisites_verified":len(REQUIRED),"g4_observations":115,"manifest_surfaces":len(SURFACES)}

def main():
    p=argparse.ArgumentParser(); p.add_argument("bundle",type=Path); a=p.parse_args()
    r=verify(a.bundle); print(json.dumps(r,indent=2,sort_keys=True)); return 0 if r["status"]=="PASS" else 2
if __name__=="__main__": sys.exit(main())
