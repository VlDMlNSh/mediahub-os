#!/usr/bin/env python3
"""MH-22 qualification executor v1.1: partial evidence is never qualification."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, subprocess, sys, time
from dataclasses import dataclass
from pathlib import Path

R4 = "471f709f5633feab7aeb62dd3ea52effad6d2bc4"
SCHEMA = "mediahub.mh22-qualification-evidence.v1"
EXECUTOR_ID = "mh22-qualification-executor"
EXECUTOR_VERSION = "1.0.1"
PASSES = [
 (1,"architecture_completeness"),(2,"authority"),(3,"identity"),(4,"trust"),
 (5,"security"),(6,"privacy"),(7,"hardware"),(8,"software"),(9,"supply_chain"),
 (10,"device"),(11,"protocol"),(12,"smart_home"),(13,"state_authority_persistence"),
 (14,"network_egress"),(15,"resource_management"),(16,"ai"),(17,"media"),
 (18,"knowledge"),(19,"cloud"),(20,"api_event_integration"),(21,"failure_recovery"),
 (22,"update_migration"),(23,"production_admission")
]
RESULTS={"PASS","FAIL","BLOCKED","NOT_IMPLEMENTED","UNKNOWN","EVIDENCE_GAP"}
COVERAGE={"FULL","PARTIAL","NONE"}

@dataclass
class Result:
    pass_id:int; domain:str; result:str; coverage_status:str; exit_status:int
    test_id:str; logs:str; reproducibility_status:str; review_status:str

def sha(data:bytes)->str: return hashlib.sha256(data).hexdigest()
def git(repo:Path,*args:str)->str:
    p=subprocess.run(["git",*args],cwd=repo,stdin=subprocess.DEVNULL,
                     stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,check=False)
    if p.returncode: raise RuntimeError(p.stdout.strip())
    return p.stdout.strip()
def run(argv:list[str],repo:Path,timeout:int)->tuple[int,str]:
    p=subprocess.run(argv,cwd=repo,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,text=True,timeout=timeout,check=False,
                     env={k:v for k,v in os.environ.items() if k.startswith("LC_") or k in {"PATH","HOME","LANG"}})
    return p.returncode,p.stdout[-20000:]
def mk(pid,domain,result,coverage,code,test_id,logs,review):
    if result not in RESULTS or coverage not in COVERAGE: raise ValueError("invalid evidence state")
    return Result(pid,domain,result,coverage,code,test_id,logs,
                  "PASS" if result=="PASS" else "NOT_ESTABLISHED",review)

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--candidate-commit",required=True)
    ap.add_argument("--r4",default=R4); ap.add_argument("--run-id",required=True)
    ap.add_argument("--output",required=True); ap.add_argument("--manifest",required=True)
    ap.add_argument("--timeout",type=int,default=300); a=ap.parse_args()
    repo=Path(a.repo).resolve(); out=Path(a.output).resolve()
    commit=git(repo,"rev-parse","HEAD"); tree=git(repo,"rev-parse","HEAD^{tree}")
    if commit!=a.candidate_commit: raise SystemExit("candidate commit mismatch")
    if git(repo,"merge-base",a.r4,commit)!=a.r4: raise SystemExit("R4 ancestry validation failed")
    manifest=json.loads((repo/a.manifest).read_text())
    env_id=sha(json.dumps({"python":sys.version,"platform":platform.platform(),
                            "machine":platform.machine(),"executor":EXECUTOR_VERSION},
                           sort_keys=True).encode())[:24]
    started=time.time(); results=[]
    for pid,domain in PASSES:
        spec=manifest.get("adapters",{}).get(str(pid))
        if not spec:
            results.append(mk(pid,domain,"NOT_IMPLEMENTED","NONE",127,
                              f"MH22-P{pid:02d}-adapter-missing",
                              "No adapter; no PASS inferred.","UNREVIEWED")); continue
        coverage=spec.get("coverage_status","NONE")
        if coverage not in COVERAGE:
            results.append(mk(pid,domain,"EVIDENCE_GAP","NONE",125,
                              f"MH22-P{pid:02d}-invalid-coverage",
                              "Invalid coverage_status.","UNREVIEWED")); continue
        if any(spec.get(k) for k in ("network","credentials","user_data")):
            results.append(mk(pid,domain,"BLOCKED","NONE",126,
                              f"MH22-P{pid:02d}-unsafe-adapter",
                              "Adapter violates isolation contract.",
                              spec.get("review_status","UNREVIEWED"))); continue
        argv=spec.get("argv")
        if not isinstance(argv,list) or not argv or any(not isinstance(x,str) for x in argv):
            results.append(mk(pid,domain,"EVIDENCE_GAP","NONE",125,
                              f"MH22-P{pid:02d}-invalid-adapter",
                              "Malformed adapter argv.",spec.get("review_status","UNREVIEWED"))); continue
        try:
            code,logs=run(argv,repo,a.timeout); result="PASS" if code==0 else "FAIL"
        except subprocess.TimeoutExpired as exc:
            code,logs,result=124,str(exc),"BLOCKED"; coverage="NONE"
        results.append(mk(pid,domain,result,coverage,code,
                          spec.get("test_id",f"MH22-P{pid:02d}-custom"),logs,
                          spec.get("review_status","UNREVIEWED")))
    finished=time.time()
    qualified=len(results)==23 and all(x.result=="PASS" and x.coverage_status=="FULL" for x in results)
    bundle={"schema":SCHEMA,"qualification_run_id":a.run_id,
            "candidate":{"candidate_commit":commit,"candidate_tree":tree,"r4_commit":a.r4,
                         "r4_ancestor":True},
            "executor":{"id":EXECUTOR_ID,"version":EXECUTOR_VERSION},
            "environment":{"environment_id":env_id,"network":"NOT_ALLOWED_BY_CONTRACT",
                           "production_credentials":False,"user_data":False,
                           "state_authority_mutation":False,"production_authorization":False,
                           "release_authorization":False},
            "started_at_epoch":started,"finished_at_epoch":finished,
            "passes":[x.__dict__ for x in results],
            "verdict":"QUALIFIED" if qualified else "BLOCKED",
            "invariants":{"partial_coverage_is_not_qualification":True,
                          "full_coverage_required_for_qualification":True,
                          "unknown_is_not_pass":True,"evidence_gap_is_not_pass":True,
                          "not_implemented_is_not_pass":True,"missing_evidence_is_not_pass":True}}
    raw=json.dumps(bundle,sort_keys=True,indent=2).encode(); bundle["bundle_sha256"]=sha(raw)
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(bundle,sort_keys=True,indent=2)+"\n")
    return 0 if qualified else 2
if __name__=="__main__": raise SystemExit(main())
