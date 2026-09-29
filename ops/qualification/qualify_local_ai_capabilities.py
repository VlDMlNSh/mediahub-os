#!/usr/bin/env python3
"""Bounded read-only local AI capability qualification for Astra."""
from __future__ import annotations
import hashlib, json, platform, subprocess, time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def http(method, url, body=None, timeout=8):
    data=json.dumps(body).encode() if body is not None else None
    req=Request(url,data=data,method=method,headers={"Content-Type":"application/json","Accept":"application/json"})
    started=time.monotonic()
    try:
        with urlopen(req,timeout=timeout) as r:
            raw=r.read(20000)
            return {"status":"HTTP_PASS","http_status":r.status,"latency_seconds":round(time.monotonic()-started,3),
                    "body_preview":raw.decode("utf-8","replace")[:6000]}
    except HTTPError as e:
        return {"status":"HTTP_FAIL","http_status":e.code,"latency_seconds":round(time.monotonic()-started,3)}
    except Exception as e:
        return {"status":"HTTP_FAIL","error":type(e).__name__,"latency_seconds":round(time.monotonic()-started,3)}

def main():
    records=[]
    ollama=http("GET","http://127.0.0.1:11434/api/tags",timeout=5)
    records.append({"component":"Ollama API","probe":ollama})
    if ollama.get("status")=="HTTP_PASS":
        models=[]
        try:
            payload=json.loads(ollama.get("body_preview","{}"))
            models=[m.get("name","") for m in payload.get("models",[])]
        except Exception:
            pass
        target=next((m for m in models if m in ("qwen2.5-coder:3b","qwen2.5-coder-3b:latest")),None)
        if target:
            gen=http("POST","http://127.0.0.1:11434/api/generate",
                     {"model":target,"prompt":"Return exactly MEDIAHUB_LOCAL_AI_OK","stream":False,"options":{"num_predict":16}},
                     timeout=30)
            ok=gen.get("status")=="HTTP_PASS" and "MEDIAHUB_LOCAL_AI_OK" in gen.get("body_preview","")
            records.append({"component":"Ollama bounded generation","model":target,"state":"QUALIFIED" if ok else "FAILED","probe":gen})
        else:
            records.append({"component":"Ollama bounded generation","state":"BLOCKED","reason":"qualified_target_model_not_found","models":models})
    ports=[]
    try:
        p=subprocess.run(["ss","-ltn"],text=True,capture_output=True,timeout=8,check=False)
        for line in p.stdout.splitlines():
            if "127.0.0.1:" in line or "0.0.0.0:" in line or "[::]:" in line:
                ports.append(line.strip())
    except Exception:
        pass
    records.append({"component":"Local listening services inventory","state":"PASS" if ports else "EMPTY","listeners":ports[:100]})
    # Probe only well-known/read-only API paths on discovered local ports.
    candidates=set()
    for line in ports:
        try:
            addr=line.split()[3]
            port=addr.rsplit(":",1)[-1].replace("]","")
            if port.isdigit(): candidates.add(int(port))
        except Exception:
            pass
    for port in sorted(candidates):
        if port==11434: continue
        for path in ("/health","/v1/models"):
            r=http("GET",f"http://127.0.0.1:{port}{path}",timeout=2)
            if r.get("status")=="HTTP_PASS":
                records.append({"component":"Local AI HTTP endpoint","port":port,"path":path,"probe":r})
    qualified=[r for r in records if r.get("state")=="QUALIFIED"]
    evidence=json.dumps({"node":platform.node(),"records":records},sort_keys=True).encode()
    result={"schema":"mediahub.local-ai-capability-qualification.v1",
            "status":"PASS" if qualified else "BLOCKED",
            "node_id":platform.node(),"qualified_capabilities":qualified,
            "records":records,
            "evidence_digest":"sha256:"+hashlib.sha256(evidence).hexdigest(),
            "secret_values":"SUPPRESSED"}
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if qualified else 2)

if __name__=="__main__":
    main()
