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
PLACEHOLDERS={"unknown","undefined","none","null","n/a","na","tbd","todo","placeholder","unset"}
G4_PATHS={"CODEX_FCC","CLAUDE_FCC","CODEX_OMNIROUTE","CLAUDE_OMNIROUTE","CLAUDE_CODE_DIRECT"}

def _verify_g4_observations(evidence: dict, source_sha: str) -> dict | None:
    observations=evidence.get("observation_records", evidence.get("observations"))
    if not isinstance(observations,list):
        return {"reason":"g4_observation_records_missing"}
    if len(observations) != 115:
        return {"reason":"g4_observation_records_count_invalid","count":len(observations)}
    command_ids=set()
    counts={path:0 for path in G4_PATHS}
    rounds={path:set() for path in G4_PATHS}
    for index, record in enumerate(observations):
        if not isinstance(record,dict):
            return {"reason":"g4_observation_record_invalid","index":index}
        if record.get("status") != "PASS" or record.get("verification_status") != "PASS":
            return {"reason":"g4_observation_not_pass","index":index}
        path=str(record.get("path",""))
        if path not in G4_PATHS:
            return {"reason":"g4_mandatory_path_invalid","index":index,"path":path}
        round_number=record.get("round")
        if not isinstance(round_number,int) or not 1 <= round_number <= 23:
            return {"reason":"g4_round_invalid","index":index,"round":round_number}
        command_id=str(record.get("command_id",""))
        if not command_id or command_id in command_ids:
            return {"reason":"g4_command_id_not_unique","index":index}
        command_ids.add(command_id)
        counts[path]+=1
        rounds[path].add(round_number)
        if str(record.get("source_sha","")).lower() != source_sha.lower():
            return {"reason":"g4_observation_source_sha_mismatch","index":index}
        for field in ("node_id","component_id","executor_id","provider_or_model_id","transport_id","workspace"):
            value=record.get(field)
            if not isinstance(value,str) or not value.strip() or value.strip().lower() in PLACEHOLDERS:
                return {"reason":"g4_observation_identity_invalid","index":index,"field":field}
        if not isinstance(record.get("exit_status"),int) or record.get("exit_status") != 0:
            return {"reason":"g4_observation_exit_status_invalid","index":index}
        if record.get("timeout") is not False:
            return {"reason":"g4_observation_timeout_invalid","index":index}
        if record.get("marker_present") is not True or record.get("result_validation") is not True:
            return {"reason":"g4_observation_result_validation_invalid","index":index}
        digest=str(record.get("evidence_digest","")).lower()
        if not SHA64.fullmatch(digest):
            return {"reason":"g4_observation_digest_invalid","index":index}
        canonical=dict(record)
        canonical.pop("evidence_digest",None)
        actual=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
        if actual != digest:
            return {"reason":"g4_observation_digest_mismatch","index":index}
    for path in G4_PATHS:
        if counts[path] != 23:
            return {"reason":"g4_path_round_count_invalid","path":path,"count":counts[path]}
        if rounds[path] != set(range(1,24)):
            return {"reason":"g4_round_coverage_invalid","path":path}
    return None

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
    expected_files={"g4_115":"g4-115.json","g5_coordination":"g5-coordination.json","g6_recovery":"g6-recovery.json","a3_independent":"a3-independent.json","clean_worktree":"clean-worktree.json"}
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
        if key=="g4_115":
            g4_error=_verify_g4_observations(evidence,source_sha)
            if g4_error: return {"status":"BLOCKED",**g4_error}
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
        for field in ("node_id","component_id","executor_id","provider_or_model_id","transport_id","workspace"):
            if evidence[field].strip().lower() in PLACEHOLDERS:
                return {"status":"BLOCKED","reason":"manifest_evidence_identity_placeholder","surface":key,"field":field}
        if evidence.get("verification_status") != "PASS": return {"status":"BLOCKED","reason":"manifest_evidence_verification_status_not_pass","surface":key}
        if key == "g4_115":
            binary_identity=evidence.get("binary_identity")
            binary_path=evidence.get("binary")
            if not isinstance(binary_identity,dict) or not isinstance(binary_path,str) or not binary_path.strip():
                return {"status":"BLOCKED","reason":"g4_binary_identity_missing"}
            binary_sha=str(binary_identity.get("sha256","")).lower()
            if not SHA64.fullmatch(binary_sha):
                return {"status":"BLOCKED","reason":"g4_binary_identity_sha_invalid"}
            executable=Path(binary_path)
            if not executable.is_file():
                return {"status":"BLOCKED","reason":"g4_binary_missing","path":binary_path}
            actual_binary_sha=hashlib.sha256(executable.read_bytes()).hexdigest()
            if actual_binary_sha != binary_sha:
                return {"status":"BLOCKED","reason":"g4_binary_identity_sha_mismatch"}
            if evidence.get("executor_id") != "binary:"+actual_binary_sha:
                return {"status":"BLOCKED","reason":"g4_executor_identity_mismatch"}
        if not isinstance(evidence.get("round"),int) or evidence["round"] < 1:
            return {"status":"BLOCKED","reason":"manifest_evidence_round_invalid","surface":key}
        if not isinstance(evidence.get("timestamp"),(int,float,str)) or (isinstance(evidence.get("timestamp"),str) and not evidence.get("timestamp").strip()):
            return {"status":"BLOCKED","reason":"manifest_evidence_timestamp_invalid","surface":key}
        if not isinstance(evidence.get("exit_status"),int):
            return {"status":"BLOCKED","reason":"manifest_evidence_exit_status_invalid","surface":key}
        if not isinstance(evidence.get("timeout"),bool):
            return {"status":"BLOCKED","reason":"manifest_evidence_timeout_invalid","surface":key}
        evidence_canonical=dict(evidence); evidence_canonical.pop("evidence_digest",None)
        evidence_actual=hashlib.sha256(json.dumps(evidence_canonical,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
        if evidence_actual != evidence_digest: return {"status":"BLOCKED","reason":"manifest_evidence_digest_mismatch","surface":key}
        evidence_sha=str(evidence.get("source_sha",""))
        if not SHA40.fullmatch(evidence_sha) or evidence_sha.lower()!=source_sha.lower():
            return {"status":"BLOCKED","reason":"manifest_evidence_source_sha_mismatch","surface":key}
        if evidence.get("secret_values")!="SUPPRESSED": return {"status":"BLOCKED","reason":"manifest_evidence_secret_policy","surface":key}
        if key == "g5_coordination":
            nested_sha=str(evidence.get("running_agent_source_sha",""))
            if not SHA40.fullmatch(nested_sha) or nested_sha.lower()!=source_sha.lower(): return {"status":"BLOCKED","reason":"g5_running_agent_source_sha_mismatch"}
        if key == "g6_recovery":
            scenarios=evidence.get("scenarios")
            if not isinstance(scenarios,dict): return {"status":"BLOCKED","reason":"g6_scenarios_missing"}
            for scenario_name, scenario in scenarios.items():
                if not isinstance(scenario,dict): return {"status":"BLOCKED","reason":"g6_scenario_record_invalid","scenario":scenario_name}
                nested_sha=str(scenario.get("source_sha",""))
                if not SHA40.fullmatch(nested_sha) or nested_sha.lower()!=source_sha.lower(): return {"status":"BLOCKED","reason":"g6_scenario_source_sha_mismatch","scenario":scenario_name}
        if key == "a3_independent":
            nested_source_sha=str(evidence.get("source_sha","")); nested_verified_sha=str(evidence.get("verified_sha",""))
            if not SHA40.fullmatch(nested_source_sha) or not SHA40.fullmatch(nested_verified_sha) or nested_source_sha.lower()!=source_sha.lower() or nested_verified_sha.lower()!=source_sha.lower():
                return {"status":"BLOCKED","reason":"a3_nested_source_sha_mismatch"}
        summary_fields=("status","observations","paths","max_parallel","independence_attested","dirty","source_sha","target_sha","fresh")
        for field in summary_fields:
            if field in data.get(key,{}) and data[key].get(field) != evidence.get(field):
                return {"status":"BLOCKED","reason":"manifest_summary_mismatch","surface":key,"field":field}
    if set(manifest) != set(SURFACES): return {"status":"BLOCKED","reason":"manifest_surface_set_invalid"}
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
