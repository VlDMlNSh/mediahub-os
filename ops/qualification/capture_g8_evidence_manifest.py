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
        if payload.get("fresh") is not True:
            print(json.dumps({"status":"BLOCKED","reason":"evidence_not_fresh","surface":key})); return 2
            print(json.dumps({"status":"BLOCKED","reason":"evidence_not_pass","surface":key})); return 2
        source_sha=payload.get("source_sha")
        target_sha=payload.get("target_sha")
        if source_sha is None and target_sha is None:
            print(json.dumps({"status":"BLOCKED","reason":"evidence_sha_binding_missing","surface":key})); return 2
        if source_sha is not None and (not isinstance(source_sha,str) or not SHA40.fullmatch(source_sha) or source_sha.lower()!=a.source_sha.lower()):
            print(json.dumps({"status":"BLOCKED","reason":"evidence_source_sha_invalid_or_mismatch","surface":key})); return 2
        if target_sha is not None and (not isinstance(target_sha,str) or not SHA40.fullmatch(target_sha) or target_sha.lower()!=a.source_sha.lower()):
            print(json.dumps({"status":"BLOCKED","reason":"evidence_target_sha_invalid_or_mismatch","surface":key})); return 2
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
