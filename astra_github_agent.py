#!/usr/bin/env python3
"""MediaHub Astra GitHub transport worker."""
from __future__ import annotations
import json, os, platform, subprocess, time
from pathlib import Path

REPO=os.environ.get("ASTRA_GITHUB_REPO","VlDMlNSh/mediahub-os")
REMOTE=os.environ.get("ASTRA_GITHUB_REMOTE",f"git@github.com:{REPO}.git")
NODE_ID=os.environ.get("ASTRA_NODE_ID",platform.node())
INTERVAL=max(15,int(os.environ.get("ASTRA_POLL_SECONDS","30")))
ROOT=Path(os.environ.get("ASTRA_WORKTREE","/opt/mediahub/astra-worktree"))
STATE=Path(os.environ.get("ASTRA_STATE_DIR","/var/lib/mediahub-astra"))
OPERATIONS={"health","research","architecture","review","documents","coding"}

def run(argv,timeout=120):
    return subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout,check=False)

def sync():
    ROOT.parent.mkdir(parents=True,exist_ok=True)
    if not (ROOT/".git").exists():
        subprocess.run(["git","clone","--depth","1",REMOTE,str(ROOT)],check=True,timeout=120)
    else:
        subprocess.run(["git","-C",str(ROOT),"fetch","--depth","1","origin","main"],check=True,timeout=120)
        subprocess.run(["git","-C",str(ROOT),"reset","--hard","origin/main"],check=True,timeout=120)

def read_command():
    path=ROOT/"control"/"commands"/f"{NODE_ID}.json"
    if not path.exists(): return None
    try: cmd=json.loads(path.read_text())
    except Exception: return None
    if cmd.get("node_id")!=NODE_ID or cmd.get("operation") not in OPERATIONS: return None
    return cmd

def publish(result):
    path=ROOT/"control"/"results"/f"{NODE_ID}.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    for args in (["git","config","user.name","Astra Node Agent"],["git","config","user.email","astra-node@localhost"],
                 ["git","checkout","-B",f"astra-node/{NODE_ID}"],["git","add",str(path.relative_to(ROOT))]):
        run(args,30).check_returncode()
    commit=run(["git","commit","-m",f"astra: result {NODE_ID}"],30)
    if commit.returncode not in (0,1): raise RuntimeError(commit.stderr)
    run(["git","push","--force-with-lease","origin",f"astra-node/{NODE_ID}"],120).check_returncode()
    run(["git","checkout","-B","main","origin/main"],30).check_returncode()

def execute(cmd):
    operation=cmd.get("operation")
    if operation=="health":
        return {"status":"ready","node_id":NODE_ID,"hostname":platform.node(),
                "platform":platform.platform(),"python":platform.python_version()}
    if operation not in OPERATIONS: raise ValueError("unsupported operation")
    from mediahub_runtime.astra_gateway import AstraGatewayRuntime
    return AstraGatewayRuntime().run_bounded({
        "task_id":cmd.get("command_id","github-task"),"title":cmd.get("title",operation),
        "description":cmd.get("description",""),"capability":operation})

def main():
    STATE.mkdir(parents=True,exist_ok=True)
    last_id=""
    while True:
        try:
            sync(); cmd=read_command()
            if cmd and cmd.get("command_id")!=last_id:
                started=time.time()
                try: value,rc=execute(cmd),0
                except Exception as exc: value,rc={"error":repr(exc)},1
                publish({"schema":1,"node_id":NODE_ID,"command_id":cmd.get("command_id"),
                         "returncode":rc,"duration_seconds":round(time.time()-started,3),
                         "result":value,"completed_at":int(time.time())})
                last_id=str(cmd.get("command_id"))
        except Exception as exc:
            (STATE/"last_error.json").write_text(json.dumps({"error":repr(exc),"time":int(time.time())}))
        time.sleep(INTERVAL)

if __name__=="__main__": main()
