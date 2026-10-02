#!/usr/bin/env python3
"""Session-scoped 115-round evidence producer; never grants GOLD authority."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,tempfile,time,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(os.environ.get("ASTRA_115_EVIDENCE_DIR",str(ROOT/"evidence"/"session-115")))
ROUNDS=23
PATHS=(("CODEX_FCC",("fcc-codex",),"FCC/Codex"),("CLAUDE_FCC",("fcc-claude",),"FCC/Claude"),
("CODEX_OMNIROUTE",("omniroute",),"OmniRoute/Codex"),("CLAUDE_OMNIROUTE",("omniroute",),"OmniRoute/Claude"),
("CLAUDE_CODE_DIRECT",("claude",),"Claude Code direct"))
MARKERS={p:f"MEDIAHUB_115_{p}_OK" for p,_,_ in PATHS}
def sha256_file(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def executable_identity(binary):
    p=Path(binary)
    return {"path":str(p),"sha256":sha256_file(p) if p.is_file() else "","size_bytes":p.stat().st_size if p.is_file() else 0}
def validate_record(rec):
    required=("command_id","round","path","component_id","node_id","source_sha","executor_id","provider_or_model_id","transport_id","provider_or_transport_id","timestamp","timeout_seconds","timeout","workspace","exit_status","status","verification_status","marker","marker_present","result_validation")
    if any(rec.get(k) in (None,"") for k in required): return False
    if not re.fullmatch(r"[0-9a-fA-F]{40}",str(rec.get("source_sha",""))): return False
    if not re.fullmatch(r"MH115-[0-9]{2}-[A-Z0-9_]+-[0-9a-f]{32}",str(rec.get("command_id",""))): return False
    if not re.fullmatch(r"[0-9a-f]{64}",str(rec.get("evidence_digest",""))): return False
    if rec["round"]<1 or rec["round"]>ROUNDS: return False
    if rec.get("verification_status") not in {"PASS","BLOCKED"}: return False
    for field in ("node_id","executor_id","provider_or_model_id","transport_id","provider_or_transport_id","workspace"):
        value=rec.get(field)
        if not isinstance(value,str) or not value.strip() or value.strip().lower() in {"unknown","undefined","none","null","n/a","na","tbd","todo","placeholder","unset"}: return False
    if rec.get("status")=="PASS" and not isinstance(rec.get("binary_identity"),dict): return False
    if rec["status"]=="PASS" and rec.get("verification_status")!="PASS": return False
    if rec["status"]=="PASS" and not rec.get("marker_present"): return False
    if rec["status"]=="PASS" and rec.get("result_validation") is not True: return False
    return True
def source_sha(): return subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,timeout=10,check=True).stdout.strip()
def run(argv,cwd,timeout=45):
    started=time.monotonic()
    try:
        p=subprocess.run(argv,cwd=cwd,text=True,capture_output=True,stdin=subprocess.DEVNULL,timeout=timeout,check=False)
        return {"returncode":p.returncode,"duration_seconds":round(time.monotonic()-started,3),"stdout_tail":p.stdout[-4000:],"stderr_tail":p.stderr[-4000:]}
    except subprocess.TimeoutExpired as e:
        return {"returncode":124,"duration_seconds":round(time.monotonic()-started,3),"stdout_tail":str(e.stdout or "")[-2000:],"stderr_tail":str(e.stderr or "")[-2000:],"timeout":True}
def provider_identity(path, binary):
    if path in {"CODEX_FCC","CLAUDE_FCC"}:
        return "fcc-wrapper:" + binary
    if "OMNIROUTE" in path:
        return "omniroute:" + binary
    return "direct:" + binary

def command_for(path,marker):
    if path=="CODEX_FCC": return ["fcc-codex","exec","--skip-git-repo-check","--sandbox","read-only",f"Return exactly {marker}. Do not modify files or use tools."]
    if path=="CLAUDE_FCC": return ["fcc-claude","-p",f"Return exactly {marker}. Do not modify files or use tools.","--output-format","text"]
    if path=="CODEX_OMNIROUTE": return ["omniroute","run","codex","--model","auto","--","exec","--skip-git-repo-check","--sandbox","read-only",f"Return exactly {marker}. Do not modify files or use tools."]
    if path=="CLAUDE_OMNIROUTE": return ["omniroute","run","claude","--model","auto","--","-p",f"Return exactly {marker}. Do not modify files or use tools.","--output-format","text"]
    if path=="CLAUDE_CODE_DIRECT": return ["claude","--print","--output-format","text","--bare",f"Return exactly {marker}. Do not modify files or use tools."]
    raise ValueError(path)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    try: head=source_sha()
    except Exception as e: print(json.dumps({"status":"BLOCKED","reason":repr(e)})); return 2
    manifest={"schema":"mediahub.astra-gold.session-115-wave.v1","status":"RUNNING","source_sha":head,"rounds_minimum_per_path":ROUNDS,"mandatory_path_count":5,"total_observations_minimum":115,"fresh_evidence_only":True,"workspace_artifact_policy":"ephemeral_workspace_with_source_archive_digest","historical_evidence_reuse":False,"fail_closed":True,"started_at":int(time.time()),"observations":[]}
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    for n in range(1,ROUNDS+1):
        for path,candidates,transport in PATHS:
            command_id=f"MH115-{n:02d}-{path}-{uuid.uuid4().hex}"
            rec={"schema":"mediahub.astra-gold.round-evidence.v1","command_id":command_id,"round":n,"path":path,"component_id":path,"node_id":os.uname().nodename,"source_sha":head,"executor_id":"UNRESOLVED","provider_or_model_id":transport,"transport_id":transport.split("/")[0],"provider_or_transport_id":transport,"timestamp":int(time.time()),"verification_status":"UNVERIFIED","timeout_seconds":45,"timeout":False,"workspace":None,"marker":MARKERS[path],"marker_present":False,"result_validation":False,"evidence_digest":""}
            binary=next((shutil.which(x) for x in candidates if shutil.which(x)),None)
            if binary is None: rec.update(status="BLOCKED",reason="executor_binary_missing",workspace=None)
            else:
                with tempfile.TemporaryDirectory(prefix=f"astra-115-{n:02d}-") as ws:
                    archive=subprocess.run(["git","archive","--format=tar",head],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=False)
                    if archive.returncode!=0: rec.update(status="BLOCKED",reason="isolated_workspace_creation_failed")
                    else:
                        archive_sha256=hashlib.sha256(archive.stdout).hexdigest()
                        rec["source_archive_sha256"]=archive_sha256
                        ext=subprocess.run(["tar","-xf","-"],cwd=ws,input=archive.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=False)
                        if ext.returncode!=0: rec.update(status="BLOCKED",reason="isolated_workspace_extraction_failed")
                        else:
                            result=run(command_for(path,MARKERS[path]),Path(ws),45)
                            marker=MARKERS[path] in result["stdout_tail"]
                            identity=executable_identity(binary)\n                            rec.update(result,binary=binary,binary_identity=identity,executor_id="binary:"+identity["sha256"],provider_or_model_id=provider_identity(path,binary),provider_or_transport_id=provider_identity(path,binary),transport_id=path.split("_")[1] if "_" in path else "DIRECT",workspace=ws,workspace_ephemeral=True,exit_status=result["returncode"],marker=MARKERS[path],marker_present=marker,result_validation=(result["returncode"]==0 and marker),status="PASS" if result["returncode"]==0 and marker else ("TIMEOUT" if result["returncode"]==124 else "BLOCKED"),verification_status="PASS" if result["returncode"]==0 and marker else "BLOCKED",timeout=(result.get("timeout") is True))
            if not validate_record(rec):
                rec.update(status="BLOCKED",verification_status="BLOCKED",reason="round_evidence_schema_invalid",exit_status=rec.get("returncode"))
            digest_payload=dict(rec); digest_payload.pop("evidence_digest",None); rec["evidence_digest"]=hashlib.sha256(json.dumps(digest_payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
            manifest["observations"].append(rec)
            (OUT/f"{n:02d}-{path}.json").write_text(json.dumps(rec,indent=2,sort_keys=True)+"\n")
            (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    summary={}
    for path,_,_ in PATHS:
        vals=[x for x in manifest["observations"] if x["path"]==path]; passed=sum(x["status"]=="PASS" for x in vals)
        summary[path]={"rounds":len(vals),"pass_count":passed,"pass_rate":round(passed/ROUNDS,3)}
    manifest["summary"]=summary; manifest["completed_at"]=int(time.time()); manifest["status"]="PASS" if all(v["pass_count"]==ROUNDS for v in summary.values()) else "BLOCKED"
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    return 0 if manifest["status"]=="PASS" else 2
if __name__=="__main__": raise SystemExit(main())
