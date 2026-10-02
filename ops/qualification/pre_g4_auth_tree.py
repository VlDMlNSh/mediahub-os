#!/usr/bin/env python3
"""Pre-G4 authentication/execution tree.

This is a smoke qualification only. It deliberately performs one bounded
fresh probe per mandatory G4 path. It does not replace or weaken G4:
ASTRA GOLD still requires the canonical 23x5=115 fresh observations.

The five probes are independent and read-only, so they are executed in a
bounded parallel batch to minimize wall-clock pre-G4 latency.
"""
from __future__ import annotations
import concurrent.futures
import hashlib,json,os,shutil,subprocess,tempfile,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PATHS=(
 ("CODEX_FCC",("fcc-codex",)),
 ("CLAUDE_FCC",("fcc-claude",)),
 ("CODEX_OMNIROUTE",("omniroute",)),
 ("CLAUDE_OMNIROUTE",("omniroute",)),
 ("CLAUDE_CODE_DIRECT",("claude",)),
)
MARKERS={name:f"MEDIAHUB_PRE_G4_{name}_OK" for name,_ in PATHS}
PRE_G4_MAX_PARALLEL=len(PATHS)

def sha256_bytes(value:bytes)->str:
    return hashlib.sha256(value).hexdigest()

def source_sha()->str:
    return subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=True,timeout=10).stdout.strip()

def command_for(path,marker):
    if path=="CODEX_FCC":
        return ["fcc-codex","exec","--skip-git-repo-check","--sandbox","read-only",f"Return exactly {marker}. Do not modify files or use tools."]
    if path=="CLAUDE_FCC":
        return ["fcc-claude","-p",f"Return exactly {marker}. Do not modify files or use tools.","--output-format","text"]
    if path=="CODEX_OMNIROUTE":
        return ["omniroute","run","codex","--model","auto","--","exec","--skip-git-repo-check","--sandbox","read-only",f"Return exactly {marker}. Do not modify files or use tools."]
    if path=="CLAUDE_OMNIROUTE":
        return ["omniroute","run","claude","--model","auto","--","-p",f"Return exactly {marker}. Do not modify files or use tools.","--output-format","text"]
    if path=="CLAUDE_CODE_DIRECT":
        return ["claude","--print","--output-format","text","--bare",f"Return exactly {marker}. Do not modify files or use tools."]
    raise ValueError(path)

def probe_path(path,candidates,head):
    binary=next((shutil.which(x) for x in candidates if shutil.which(x)),None)
    rec={"path":path,"source_sha":head,"timestamp":int(time.time()),"status":"BLOCKED","verification_status":"BLOCKED"}
    if not binary:
        rec["reason"]="executor_binary_missing"
        return rec
    with tempfile.TemporaryDirectory(prefix="astra-pre-g4-") as ws:
        archive=subprocess.run(["git","archive","--format=tar",head],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=False)
        if archive.returncode:
            rec["reason"]="isolated_workspace_creation_failed"
            return rec
        rec["source_archive_sha256"]=sha256_bytes(archive.stdout)
        ext=subprocess.run(["tar","-xf","-"],cwd=ws,input=archive.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=False)
        if ext.returncode:
            rec["reason"]="isolated_workspace_extraction_failed"
            return rec
        started=time.monotonic()
        try:
            p=subprocess.run(command_for(path,MARKERS[path]),cwd=ws,text=True,capture_output=True,stdin=subprocess.DEVNULL,timeout=45,check=False)
            stdout=p.stdout[-4000:]
            rec.update(
                binary=binary,
                binary_sha256=sha256_bytes(Path(binary).read_bytes()) if Path(binary).is_file() else "",
                returncode=p.returncode,
                duration_seconds=round(time.monotonic()-started,3),
                marker=MARKERS[path],
                marker_present=MARKERS[path] in stdout,
                status="PASS" if p.returncode==0 and MARKERS[path] in stdout else "BLOCKED",
                verification_status="PASS" if p.returncode==0 and MARKERS[path] in stdout else "BLOCKED",
                diagnostic_tail=stdout[-1000:],
            )
        except subprocess.TimeoutExpired as exc:
            rec.update(binary=binary,status="TIMEOUT",reason="timeout",verification_status="BLOCKED",diagnostic_tail=str(exc)[:1000])
    return rec

def main()->int:
    head=source_sha()
    with concurrent.futures.ThreadPoolExecutor(max_workers=PRE_G4_MAX_PARALLEL) as pool:
        futures=[pool.submit(probe_path,path,candidates,head) for path,candidates in PATHS]
        observations=[future.result() for future in futures]
    summary={"schema":"mediahub.astra-gold.pre-g4-auth-tree.v1","source_sha":head,
             "fresh_evidence_only":True,"gold_authority":False,"required_g4_rounds":115,
             "probe_count":len(observations),"max_parallel_probes":PRE_G4_MAX_PARALLEL,
             "pass_count":sum(x["status"]=="PASS" for x in observations),
             "observations":observations,"completed_at":int(time.time())}
    print(json.dumps(summary,sort_keys=True))
    return 0 if summary["pass_count"]==len(PATHS) else 2

if __name__=="__main__":
    raise SystemExit(main())
