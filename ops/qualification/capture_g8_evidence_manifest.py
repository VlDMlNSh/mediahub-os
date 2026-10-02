#!/usr/bin/env python3
"""Build an immutable G8 evidence manifest from independent evidence files."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

SURFACES=("g4_115","g5_coordination","g6_recovery","a3_independent","clean_worktree")
FILES={
 "g4_115":"g4-115.json",
 "g5_coordination":"g5-coordination.json",
 "g6_recovery":"g6-recovery.json",
 "a3_independent":"a3-independent.json",
 "clean_worktree":"clean-worktree.json",
}
SHA40=re.compile(r"^[0-9a-fA-F]{40}$")
REQUIRED_EVIDENCE_METADATA=("command_id","node_id","component_id","executor_id","provider_or_model_id","transport_id","source_sha","round","timestamp","exit_status","timeout","workspace","verification_status","evidence_digest")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--evidence-dir",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--source-sha",required=True)
    a=p.parse_args()
    if not SHA40.fullmatch(a.source_sha):
        print(json.dumps({"status":"BLOCKED","reason":"source_sha_invalid"})); return 2
    refs={}
    summary={}
    for key in SURFACES:
        path=a.evidence_dir/FILES[key]
        if not path.is_file():
            print(json.dumps({"status":"BLOCKED","reason":"evidence_file_missing","surface":key})); return 2
        raw=path.read_bytes()
        digest=hashlib.sha256(raw).hexdigest()
        try: payload=json.loads(raw.decode("utf-8"))
        except Exception:
            print(json.dumps({"status":"BLOCKED","reason":"evidence_json_invalid","surface":key})); return 2
        if not isinstance(payload,dict) or payload.get("status")!="PASS":
            print(json.dumps({"status":"BLOCKED","reason":"evidence_not_pass","surface":key})); return 2
        missing_metadata=[field for field in REQUIRED_EVIDENCE_METADATA if field not in payload]
        if missing_metadata:
            print(json.dumps({"status":"BLOCKED","reason":"evidence_metadata_missing","surface":key,"fields":missing_metadata})); return 2
        evidence_digest=str(payload.get("evidence_digest","")).lower()
        if not re.fullmatch(r"[0-9a-f]{64}",evidence_digest):
            print(json.dumps({"status":"BLOCKED","reason":"evidence_digest_invalid","surface":key})); return 2
        string_fields=("command_id","node_id","component_id","executor_id","provider_or_model_id","transport_id","workspace","verification_status")
        for field in string_fields:
            if not isinstance(payload.get(field),str) or not payload[field].strip():
                print(json.dumps({"status":"BLOCKED","reason":"evidence_metadata_invalid","surface":key,"field":field})); return 2
        placeholder_values={"unknown","undefined","none","null","n/a","na","tbd","todo","placeholder","unset"}
        for field in ("node_id","component_id","executor_id","provider_or_model_id","transport_id","workspace"):
            if payload[field].strip().lower() in placeholder_values:
                print(json.dumps({"status":"BLOCKED","reason":"evidence_identity_placeholder","surface":key,"field":field})); return 2
        if payload.get("verification_status") != "PASS":
            print(json.dumps({"status":"BLOCKED","reason":"evidence_verification_status_not_pass","surface":key})); return 2
        if not isinstance(payload.get("round"),int) or payload["round"] < 1:
            print(json.dumps({"status":"BLOCKED","reason":"evidence_round_invalid","surface":key})); return 2
        if not isinstance(payload.get("timestamp"),(int,float,str)) or (isinstance(payload.get("timestamp"),str) and not payload["timestamp"].strip()):
            print(json.dumps({"status":"BLOCKED","reason":"evidence_timestamp_invalid","surface":key})); return 2
        if not isinstance(payload.get("exit_status"),int):
            print(json.dumps({"status":"BLOCKED","reason":"evidence_exit_status_invalid","surface":key})); return 2
        if not isinstance(payload.get("timeout"),bool):
            print(json.dumps({"status":"BLOCKED","reason":"evidence_timeout_invalid","surface":key})); return 2
        evidence_canonical=dict(payload)
        evidence_canonical.pop("evidence_digest",None)
        evidence_actual=hashlib.sha256(json.dumps(evidence_canonical,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
        if evidence_actual!=evidence_digest:
            print(json.dumps({"status":"BLOCKED","reason":"evidence_digest_mismatch","surface":key})); return 2
        if payload.get("fresh") is not True:
            print(json.dumps({"status":"BLOCKED","reason":"evidence_not_fresh","surface":key})); return 2
        source_sha=payload.get("source_sha")
        target_sha=payload.get("target_sha")
        if source_sha is None:
            print(json.dumps({"status":"BLOCKED","reason":"evidence_source_sha_binding_missing","surface":key})); return 2
        if source_sha is not None and (not isinstance(source_sha,str) or not SHA40.fullmatch(source_sha) or source_sha.lower()!=a.source_sha.lower()):
            print(json.dumps({"status":"BLOCKED","reason":"evidence_source_sha_invalid_or_mismatch","surface":key})); return 2
        if target_sha is not None and (not isinstance(target_sha,str) or not SHA40.fullmatch(target_sha) or target_sha.lower()!=a.source_sha.lower()):
            print(json.dumps({"status":"BLOCKED","reason":"evidence_target_sha_invalid_or_mismatch","surface":key})); return 2
        # Cross-gate provenance: nested evidence source identities must bind to the same approved SHA.
        if key=="g5_coordination":
            nested_sha=payload.get("running_agent_source_sha")
            if not isinstance(nested_sha,str) or not SHA40.fullmatch(nested_sha) or nested_sha.lower()!=a.source_sha.lower():
                print(json.dumps({"status":"BLOCKED","reason":"g5_running_agent_source_sha_unbound","surface":key})); return 2
        elif key=="g6_recovery":
            scenarios=payload.get("scenarios")
            if not isinstance(scenarios,dict):
                print(json.dumps({"status":"BLOCKED","reason":"g6_scenarios_missing","surface":key})); return 2
            for scenario_name, scenario in scenarios.items():
                if not isinstance(scenario,dict):
                    print(json.dumps({"status":"BLOCKED","reason":"g6_scenario_record_invalid","surface":key,"scenario":scenario_name})); return 2
                nested_sha=scenario.get("source_sha")
                if not isinstance(nested_sha,str) or not SHA40.fullmatch(nested_sha) or nested_sha.lower()!=a.source_sha.lower():
                    print(json.dumps({"status":"BLOCKED","reason":"g6_scenario_source_sha_unbound","surface":key,"scenario":scenario_name})); return 2
        elif key=="a3_independent":
            for field in ("source_sha","verified_sha"):
                nested_sha=payload.get(field)
                if not isinstance(nested_sha,str) or not SHA40.fullmatch(nested_sha) or nested_sha.lower()!=a.source_sha.lower():
                    print(json.dumps({"status":"BLOCKED","reason":"a3_sha_unbound","surface":key,"field":field})); return 2
        if payload.get("secret_values")!="SUPPRESSED":
            print(json.dumps({"status":"BLOCKED","reason":"evidence_secret_policy","surface":key})); return 2
        refs[key]={"path":str(path),"sha256":digest,"status":"PASS"}
        summary[key]={k:v for k,v in payload.items() if k in ("status","observations","paths","max_parallel","independence_attested","dirty","source_sha","target_sha","fresh")}
    payload={"schema":"mediahub.astra-gold.g8-evidence-manifest.v1","fresh":True,
             "source_sha":a.source_sha,"evidence_manifest":refs,"secret_values":"SUPPRESSED",**summary}
    canonical=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
    payload["bundle_sha256"]=hashlib.sha256(canonical).hexdigest()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","source_sha":a.source_sha,"surfaces":len(refs)}))
    return 0
if __name__=="__main__": sys.exit(main())
