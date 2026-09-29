#!/usr/bin/env python3
"""Capture bounded, sanitized runtime evidence for local engineering backends."""
from __future__ import annotations
import hashlib,json,os,platform,shlex,shutil,subprocess,time
from pathlib import Path
BACKENDS={"codex":"MEDIAHUB_CODEX_COMMAND","cursor":"MEDIAHUB_CURSOR_COMMAND"}
FORBIDDEN=(";","&&","||","|",">","<","\n","\r")
PROMPT="print('MEDIAHUB_EXECUTION_BACKEND_QUALIFICATION')"
TIMEOUT=30
def digest(data:str)->str:return "sha256:"+hashlib.sha256(data.encode("utf-8","replace")).hexdigest()
def classify(text:str)->str:
    t=text.lower()
    if any(x in t for x in ("unauthorized","authentication","not authenticated","api key","login")): return "authentication_or_authorization"
    if any(x in t for x in ("usage:","unknown option","unrecognized option","invalid option","unexpected argument")): return "cli_invocation_error"
    if any(x in t for x in ("network","connection","connect","dns","timed out","timeout")): return "network_or_timeout"
    if any(x in t for x in ("permission denied","operation not permitted")): return "permission_error"
    if any(x in t for x in ("model","provider","quota","rate limit")): return "provider_or_quota"
    return "nonzero_exit_unknown"
def qualify(backend_id:str)->dict:
    raw=os.environ.get(BACKENDS[backend_id],"").strip()
    if not raw:
        candidates={"codex":("/usr/local/bin/codex","/usr/bin/codex"),"cursor":("/usr/local/bin/cursor-agent","/usr/bin/cursor-agent","/usr/local/bin/cursor","/usr/bin/cursor")}[backend_id]
        for candidate in candidates:
            if Path(candidate).is_file() and os.access(candidate,os.X_OK): raw=candidate; break
    result={"node_id":platform.node(),"verification_state":"UNVERIFIED","checks":{"node_identity":"PASS" if platform.node()=="mh-dev-01" else "FAIL","binary_identity":"FAIL","bounded_execution":"FAIL"},"secret_values":"SUPPRESSED"}
    if not raw: result["reason"]="command_not_configured"; return result
    if any(token in raw for token in FORBIDDEN): result["reason"]="unsafe_command_syntax"; return result
    try: argv=shlex.split(raw)
    except ValueError: result["reason"]="invalid_command_syntax"; return result
    if not argv: result["reason"]="empty_command"; return result
    if backend_id=="codex" and Path(argv[0]).name=="codex":
        if len(argv)==1 or argv[1]!="exec": argv.insert(1,"exec")
        if "--skip-git-repo-check" not in argv: argv.insert(2,"--skip-git-repo-check")
        if "--full-auto" not in argv: argv.insert(2,"--full-auto")
        if "--" not in argv: argv.append("--")
    if backend_id=="cursor" and Path(argv[0]).name in {"cursor","cursor-agent"} and (len(argv)==1 or argv[1] not in {"agent","exec"}): argv.append("--print")
    if not shutil.which(argv[0]): result["reason"]="executable_not_found"; return result
    result["checks"]["binary_identity"]="PASS"
    started=time.monotonic()
    try:
        proc=subprocess.run([*argv,PROMPT],text=True,capture_output=True,timeout=TIMEOUT,check=False,env={key:os.environ[key] for key in ("PATH","HOME","USER","LOGNAME","SHELL","TERM","XDG_CONFIG_HOME","CODEX_HOME","OPENAI_API_KEY","OPENAI_BASE_URL","OPENAI_ORG_ID","CURSOR_API_KEY","CURSOR_AGENT_API_KEY") if os.environ.get(key)})
    except subprocess.TimeoutExpired: result["reason"]="bounded_execution_timeout"; return result
    except OSError as exc: result["reason"]=f"bounded_execution_oserror_{getattr(exc,'errno','unknown')}"; return result
    combined=(proc.stdout or "")+(proc.stderr or "")
    result.update({"duration_seconds":round(time.monotonic()-started,3),"returncode":proc.returncode,"output_bytes":len(combined.encode("utf-8","replace")),"output_sha256":digest(combined)})
    if proc.returncode!=0: result["reason"]=classify(combined); return result
    if not combined.strip(): result["reason"]="empty_output"; return result
    result["checks"]["bounded_execution"]="PASS"; result["verification_state"]="VERIFIED"; return result
def main()->int:
    try: repo_revision=subprocess.run(["git","rev-parse","HEAD"],text=True,capture_output=True,timeout=10,check=False).stdout.strip()
    except (OSError,subprocess.TimeoutExpired): repo_revision=""
    payload={"schema":"mediahub.execution-backends.v1","status":"PASS","captured_at":int(time.time()),"node_id":platform.node(),"repo_revision":repo_revision,"backends":{b:qualify(b) for b in BACKENDS},"secret_values":"SUPPRESSED"}
    if not repo_revision or payload["backends"]["codex"]["verification_state"]!="VERIFIED": payload["status"]="BLOCKED"
    else: payload["backends"]["cursor"]["verification_state"]="DEFERRED"; payload["backends"]["cursor"]["deferred_reason"]="user_requested_defer"
    payload["evidence_digest"]=digest(json.dumps(payload,sort_keys=True,separators=(",",":")))
    print(json.dumps(payload,sort_keys=True)); return 0 if payload["status"]=="PASS" else 2
if __name__=="__main__": raise SystemExit(main())
