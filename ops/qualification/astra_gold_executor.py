#!/usr/bin/env python3
"""Bounded Astra GOLD qualification executor."""
from __future__ import annotations
import json, os, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = Path(os.environ.get("ASTRA_EVIDENCE_DIR", str(ROOT / "evidence")))
REQUIRED = ("transport-health.json","runtime-e2e.json","scheduler-e2e.json","fencing.json","recovery.json","backup-restore.json","provider-model.json")

def run(argv, timeout=300):
    p = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)
    return {"command":" ".join(argv),"returncode":p.returncode,"stdout":p.stdout[-12000:],"stderr":p.stderr[-8000:]}

def qualification_pass():
    checks = [
        run(["python3","-m","compileall","-q","runtime","tests","astra_github_agent.py"]),
        run(["python3","-m","unittest","discover","-s","tests","-p","test_*.py"],600),
        run(["python3","ops/qualification/verify_pre_soak_bundle.py","evidence"]),
    ]
    evidence = {}
    for name in REQUIRED:
        path=EVIDENCE/name
        if not path.is_file(): evidence[name]="MISSING"; continue
        try: evidence[name]=json.loads(path.read_text(encoding="utf-8")).get("status","INVALID_STATUS")
        except Exception: evidence[name]="INVALID_JSON"
    git=run(["git","status","--short"])
    head=run(["git","rev-parse","HEAD"])
    blocked=[]
    if any(c["returncode"] != 0 for c in checks): blocked.append("qualification_check_failed")
    if any(v != "PASS" for v in evidence.values()): blocked.append("fresh_pre_soak_bundle_not_all_PASS")
    if git["returncode"] != 0 or git["stdout"].strip(): blocked.append("worktree_not_clean")
    return {"status":"PASS" if not blocked else "BLOCKED","head":head["stdout"].strip(),
            "checks":checks,"pre_soak_evidence_status":evidence,"blocked_reasons":blocked}

def main():
    started=time.time()
    duration=int(os.environ.get("ASTRA_QUALIFICATION_SECONDS","86400"))
    interval=max(60,int(os.environ.get("ASTRA_QUALIFICATION_INTERVAL_SECONDS","600")))
    deadline=started+duration
    last=None
    while time.time() < deadline:
        last=qualification_pass()
        print(json.dumps({"schema":"mediahub.astra-gold-qualification.v1","executor":"test-astra",
                          "iteration":last,"secret_values":"SUPPRESSED",
                          "elapsed_seconds":round(time.time()-started,3)},sort_keys=True))
        if last["status"]=="PASS": return 0
        # A blocked pre-soak is a queue gate, not a 24h soak. Return immediately
        # so the canonical worker can advance to the evidence-producing wave.
        if "fresh_pre_soak_bundle_not_all_PASS" in last.get("blocked_reasons", []):
            return 2
        time.sleep(min(interval,max(0,int(deadline-time.time()))))
    final={"schema":"mediahub.astra-gold-qualification.v1","status":last["status"] if last else "BLOCKED",
           "executor":"test-astra","iteration":last,"elapsed_seconds":round(time.time()-started,3),
           "secret_values":"SUPPRESSED","completed_due_to":"qualification_window_elapsed"}
    print(json.dumps(final,indent=2,sort_keys=True))
    return 0 if final["status"]=="PASS" else 2

if __name__=="__main__":
    raise SystemExit(main())
