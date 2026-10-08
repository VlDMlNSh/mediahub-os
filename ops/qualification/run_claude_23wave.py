#!/usr/bin/env python3
import argparse,json,os,subprocess,time,urllib.request,urllib.error,socket
from pathlib import Path

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--node",required=True); p.add_argument("--model",required=True); p.add_argument("--marker",required=True); p.add_argument("--output",required=True); p.add_argument("--env-file",required=True); p.add_argument("--fcc",required=True)
 a=p.parse_args()
 env=os.environ.copy()
 for raw in Path(a.env_file).read_text().splitlines():
  raw=raw.strip()
  if raw and not raw.startswith("#") and "=" in raw:
   k,v=raw.split("=",1); env[k.strip()]=v.strip()
 host="127.0.0.1"; s=socket.socket(); s.bind((host,0)); port=s.getsockname()[1]; s.close()
 env.update({"HOST":host,"PORT":str(port),"MODEL":"ollama/"+a.model,"ENABLE_MODEL_THINKING":"false","ENABLE_OPUS_THINKING":"false","ENABLE_SONNET_THINKING":"false","ENABLE_HAIKU_THINKING":"false"})
 proc=subprocess.Popen([a.fcc,"--host",host,"--port",str(port)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 rows=[]
 try:
  for _ in range(30):
   try:
    urllib.request.urlopen(f"http://{host}:{port}/health",timeout=2).read(); break
   except Exception: time.sleep(1)
  urllib.request.urlopen(f"http://{host}:{port}/health",timeout=5).read()
  for i in range(1,24):
   payload=json.dumps({"model":"ollama/"+a.model,"max_tokens":32,"temperature":0,"messages":[{"role":"user","content":"Output exactly this token and nothing else: "+a.marker}]}).encode()
   req=urllib.request.Request(f"http://{host}:{port}/v1/messages",data=payload,method="POST",headers={"x-api-key":env.get("ANTHROPIC_AUTH_TOKEN",""),"Content-Type":"application/json"})
   status="EXECUTION_FAILURE"; rc=1
   try:
    with urllib.request.urlopen(req,timeout=290) as resp: d=json.loads(resp.read().decode())
    text="\n".join(x.get("text","") for x in d.get("content",[]) if isinstance(x,dict)).strip()
    if text==a.marker or text.rstrip(".!?")==a.marker: status="PASS"; rc=0
   except Exception: pass
   rows.append({"round":i,"timestamp":int(time.time()),"status":status,"returncode":rc,"marker":a.marker,"model":"ollama/"+a.model,"target_sha":os.environ["GITHUB_SHA"]})
   Path(a.output).write_text("\n".join(json.dumps(x,sort_keys=True) for x in rows)+"\n")
   if status!="PASS": raise SystemExit(2)
 finally:
  proc.terminate()
if __name__=="__main__": main()
