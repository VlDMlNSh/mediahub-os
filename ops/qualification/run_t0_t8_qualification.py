#!/usr/bin/env python3
"""Canonical ASTRA GOLD T0->T8 qualification orchestrator.

This process prepares and verifies the complete pre-soak qualification only.
It never starts G9, never authorizes launch, and never fabricates missing
physical evidence. Missing or stale evidence is a hard BLOCK.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
STATE=Path(os.environ.get("ASTRA_STATE_DIR","/var/lib/mediahub-astra"))
EVIDENCE=STATE/"qualification_evidence"
SOURCE_SHA=os.environ.get("GITHUB_SHA","").lower()
MANDATORY_G4=("CODEX_FCC","CLAUDE_FCC","CODEX_OMNIROUTE","CLAUDE_OMNIROUTE","CLAUDE_CODE_DIRECT")

def run(name, argv, timeout):
    started=time.monotonic()
    p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout,check=False)
    return {"name":name,"returncode":p.returncode,"elapsed_seconds":round(time.monotonic()-started,3),
            "stdout":p.stdout[-12000:],"stderr":p.stderr[-8000:]}

def block(stage, reason, steps):
    result={"schema":"mediahub.astra-gold.t0-t8-run.v1","status":"BLOCKED",
            "stage":stage,"reason":reason,"source_sha":SOURCE_SHA,
            "steps":steps,"secret_values":"SUPPRESSED"}
    print(json.dumps(result,indent=2,sort_keys=True))
    return 2

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-sha",default=SOURCE_SHA)
    args=parser.parse_args()
    source=str(args.source_sha).lower()
    steps=[]
    if len(source)!=40 or any(c not in "0123456789abcdef" for c in source):
        return block("T0","invalid_source_sha",steps)
    head=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=False)
    if head.returncode!=0 or head.stdout.strip().lower()!=source:
        return block("T0","exact_source_sha_mismatch",steps)

    EVIDENCE.mkdir(parents=True,exist_ok=True)

    # T0/T1/T2: deterministic local preflight and bounded provider discovery.
    for name,argv,timeout in (
        ("T0_runtime_preflight",[sys.executable,"-m","compileall","-q","runtime","tests","astra_github_agent.py"],120),
        ("T0_unit_tests",[sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py"],600),
        ("T1_local_executor_pre_g4",[sys.executable,"ops/qualification/pre_g4_auth_tree.py"],180),
        ("T2_provider_model_probe",[sys.executable,"ops/qualification/qualify_execution_backends.py"],180),
    ):
        step=run(name,argv,timeout); steps.append(step)
        if step["returncode"]!=0:
            return block(name,"stage_failed",steps)

    # T3/T4: mandatory physical executor qualification. This is never simulated.
    step=run("T3_T4_G4_115",[sys.executable,"ops/qualification/session_115_wave.py"],int(os.environ.get("ASTRA_G4_TIMEOUT_SECONDS","7200")))
    steps.append(step)
    if step["returncode"]!=0:
        return block("T4","fresh_115_wave_not_passed",steps)

    # Require a real G4 evidence record and exact five-path/23-round contract.
    g4=EVIDENCE/"g4-115.json"
    if not g4.is_file():
        return block("T4","g4_evidence_missing",steps)
    try:
        g4data=json.loads(g4.read_text(encoding="utf-8"))
    except Exception:
        return block("T4","g4_evidence_invalid_json",steps)
    if g4data.get("status")!="PASS" or g4data.get("observations")!=115 or g4data.get("paths")!=5:
        return block("T4","g4_evidence_contract_failed",steps)
    if str(g4data.get("source_sha","")).lower()!=source:
        return block("T4","g4_source_sha_mismatch",steps)

    # T5/T6/T7 are supplied by their dedicated producers. This orchestrator
    # verifies; it does not synthesize attestations.
    verifier_specs=(
        ("T5","g5_coordination.json","verify_g5_coordination_attestation.py"),
        ("T6","g6_recovery.json","verify_g6_recovery_evidence.py"),
        ("T7","a3-independent.json","verify_a3_evidence.py"),
    )
    for stage,filename,verifier in verifier_specs:
        evidence=EVIDENCE/filename
        if not evidence.is_file():
            return block(stage,"fresh_evidence_missing:"+filename,steps)
        step=run(stage+"_verify",[sys.executable,"ops/qualification/"+verifier,str(evidence)],300)
        steps.append(step)
        if step["returncode"]!=0:
            return block(stage,"independent_verifier_failed",steps)
        try: data=json.loads(evidence.read_text(encoding="utf-8"))
        except Exception: return block(stage,"invalid_evidence_json",steps)
        if data.get("status")!="PASS" or str(data.get("source_sha","")).lower()!=source:
            return block(stage,"evidence_not_fresh_pass_or_source_mismatch",steps)

    # T8: immutable pre-soak bundle is the only admission artifact.
    clean=EVIDENCE/"clean-worktree.json"\n    clean_payload={"schema":"mediahub.astra-gold.clean-worktree.v1","status":"PASS" if not subprocess.run(["git","status","--porcelain"],cwd=ROOT,text=True,capture_output=True,check=False).stdout.strip() else "BLOCKED","command_id":"T8-CLEAN-"+source[:12],"node_id":os.uname().nodename,"component_id":"clean_worktree","executor_id":"git:"+source,"provider_or_model_id":"git-local","transport_id":"local","source_sha":source,"round":1,"timestamp":int(time.time()),"exit_status":0,"timeout":False,"workspace":str(ROOT),"verification_status":"PASS","secret_values":"SUPPRESSED","fresh":True,"dirty":bool(subprocess.run(["git","status","--porcelain"],cwd=ROOT,text=True,capture_output=True,check=False).stdout.strip())}\n    canonical=dict(clean_payload); clean_payload["evidence_digest"]=__import__("hashlib").sha256(json.dumps(canonical,sort_keys=True,separators=(",",":")).encode()).hexdigest(); clean.write_text(json.dumps(clean_payload,indent=2,sort_keys=True)+"\\n",encoding="utf-8")\n    step=run("T8_capture_manifest",[sys.executable,"ops/qualification/capture_g8_evidence_manifest.py","--evidence-dir",str(EVIDENCE),"--output",str(EVIDENCE/"g8-pre-soak.json"),"--source-sha",source],300)
    steps.append(step)
    if step["returncode"]!=0:
        return block("T8","g8_manifest_capture_failed",steps)
    bundle=EVIDENCE/"g8-pre-soak.json"
    if not bundle.is_file():
        return block("T8","g8_bundle_missing",steps)
    step=run("T8_verify_bundle",[sys.executable,"ops/qualification/verify_g8_pre_soak_bundle.py",str(bundle)],300)
    steps.append(step)
    if step["returncode"]!=0:
        return block("T8","g8_bundle_verification_failed",steps)
    try: final=json.loads(bundle.read_text(encoding="utf-8"))
    except Exception: return block("T8","g8_bundle_invalid_json",steps)
    if final.get("fresh") is not True or final.get("status")!="PASS" or str(final.get("source_sha","")).lower()!=source:
        return block("T8","g8_admission_contract_failed",steps)

    result={"schema":"mediahub.astra-gold.t0-t8-run.v1","status":"TEST_SOAK_ADMITTED",
            "stage":"T8","source_sha":source,"g4_observations":115,
            "g4_paths":list(MANDATORY_G4),"g9_started":False,
            "human_launch_authorization":False,"secret_values":"SUPPRESSED",
            "steps":steps,"elapsed_seconds":round(sum(x["elapsed_seconds"] for x in steps),3)}
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
