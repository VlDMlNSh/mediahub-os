#!/usr/bin/env python3
"""Bounded Git-backed Astra node worker.
Only executes the fixed command vocabulary below; command payloads are never shell.
"""
from __future__ import annotations
import json, os, subprocess, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NODE=os.environ.get("ASTRA_NODE","dev2")
BUS=ROOT/"ops"/"control_bus"
STATE=ROOT/".autonomous"/"node_bus"/NODE
COMMAND=BUS/f"{NODE}.command.json"
RESULT=STATE/"status.json"
INTERVAL=int(os.environ.get("ASTRA_NODE_POLL","20"))
ALLOWED={"STATUS","SYNC","PREPARE","STOP","RESUME"}
def run(args):
    return subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=120)
def atomic(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    tmp.replace(path)
def refresh_transport():
    if os.environ.get("ASTRA_NODE_AUTO_SYNC", "1") != "1":
        return True, "disabled"
    r=run(["git","fetch","origin","engineering/mh21-sandbox-lifecycle-20260910"])
    if r.returncode:
        return False, (r.stderr or r.stdout)[-500:]
    r=run(["git","merge","--ff-only","origin/engineering/mh21-sandbox-lifecycle-20260910"])
    if r.returncode:
        return False, (r.stderr or r.stdout)[-500:]
    return True, "synced"


def publish_result():
    if os.environ.get("ASTRA_NODE_AUTO_PUBLISH", "1") != "1":
        return True, "disabled"
    r=run(["git","notes","--ref=refs/notes/astra-control-bus","append","-F",str(RESULT),"HEAD"])
    if r.returncode:
        return False, (r.stderr or r.stdout)[-500:]
    r=run(["git","push","origin","refs/notes/astra-control-bus"])
    if r.returncode:
        return False, (r.stderr or r.stdout)[-500:]
    return True, "published"

def snapshot(action="STATUS",result="OK",detail=""):
    r=run(["git","rev-parse","HEAD"])
    clean=not bool(run(["git","status","--porcelain"]).stdout.strip())
    atomic(RESULT,{"schema":1,"node":NODE,"action":action,"result":result,
        "detail":detail,"head":r.stdout.strip(),"clean":clean,
        "ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())})
    published, publish_detail = publish_result()
    if not published:
        atomic(RESULT,{"schema":1,"node":NODE,"action":action,"result":"FAILED",
            "detail":"result publication failed: "+publish_detail,
            "head":r.stdout.strip(),"clean":clean,
            "ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())})
def valid_command(cmd):
    if not isinstance(cmd,dict) or cmd.get("schema")!=1:
        return False
    if cmd.get("target") not in (NODE,"*"):
        return False
    action=str(cmd.get("action",""))
    ident=str(cmd.get("command_id",""))
    expires=str(cmd.get("expires_at",""))
    if action not in ALLOWED or not ident or not expires:
        return False
    try:
        expiry=time.strptime(expires,"%Y-%m-%dT%H:%M:%SZ")
        return time.mktime(expiry) >= time.time()
    except ValueError:
        return False

def execute(action):
    if action=="STATUS":
        snapshot(); return
    if action=="SYNC":
        r=run(["git","fetch","origin","engineering/mh21-sandbox-lifecycle-20260910"])
        if r.returncode: snapshot(action,"FAILED",r.stderr[-500:]); return
        r=run(["git","merge","--ff-only","origin/engineering/mh21-sandbox-lifecycle-20260910"])
        snapshot(action,"OK" if r.returncode==0 else "FAILED",(r.stderr or r.stdout)[-500:]); return
    if action=="PREPARE":
        r=run(["git","status","--porcelain"])
        snapshot(action,"OK" if r.returncode==0 else "FAILED",r.stdout[-500:]); return
    snapshot(action,"ACK","bounded state transition accepted")
def main():
    STATE.mkdir(parents=True,exist_ok=True)
    last=""
    while True:
        try:
            synced, detail = refresh_transport()
            if not synced:
                snapshot("TRANSPORT","FAILED",detail)
                time.sleep(INTERVAL)
                continue
            cmd=json.loads(COMMAND.read_text()) if COMMAND.exists() else {}
            ident=str(cmd.get("command_id",""))
            action=str(cmd.get("action",""))
            if valid_command(cmd) and ident!=last:
                if action in {"STOP","RESUME"}:
                    snapshot(action,"ACK","execution gate changed by controller")
                else:
                    execute(action)
                last=ident
        except Exception as exc:
            snapshot("ERROR","FAILED",str(exc)[-500:])
        time.sleep(INTERVAL)
if __name__=="__main__":
    main()
