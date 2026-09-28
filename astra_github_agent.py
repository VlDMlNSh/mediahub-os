#!/usr/bin/env python3
"""MediaHub Astra GitHub transport worker."""
from __future__ import annotations
import hashlib, importlib, json, os, platform, subprocess, sys, time
from pathlib import Path

REPO=os.environ.get("ASTRA_GITHUB_REPO","VlDMlNSh/mediahub-os")
REMOTE=os.environ.get("ASTRA_GITHUB_REMOTE",f"git@github.com:{REPO}.git")
NODE_ID=os.environ.get("ASTRA_NODE_ID",platform.node())
INTERVAL=max(15,int(os.environ.get("ASTRA_POLL_SECONDS","30")))
ROOT=Path(os.environ.get("ASTRA_WORKTREE","/opt/mediahub/astra-worktree"))
STATE=Path(os.environ.get("ASTRA_STATE_DIR","/var/lib/mediahub-astra"))
OPERATIONS={"health","research","architecture","review","documents","coding","coding_v2","qualification","execution_backend_qualification"}
RUNNING_AGENT_SHA=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

def run(argv,timeout=120):
    return subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout,check=False)

def sync():
    ROOT.parent.mkdir(parents=True,exist_ok=True)
    if not (ROOT/".git").exists():
        subprocess.run(["git","clone","--depth","1",REMOTE,str(ROOT)],check=True,timeout=120)
    else:
        subprocess.run(["git","-C",str(ROOT),"fetch","--depth","1","origin","main"],check=True,timeout=120)
        subprocess.run(["git","-C",str(ROOT),"reset","--hard","origin/main"],check=True,timeout=120)

def maybe_reexec_updated_agent():
    target=ROOT/"astra_github_agent.py"
    if not target.exists():
        return
    target_sha=hashlib.sha256(target.read_bytes()).hexdigest()
    if target_sha != RUNNING_AGENT_SHA:
        os.execv(sys.executable,[sys.executable,str(target),*sys.argv[1:]])

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
    run(["git","push","--force","origin",f"astra-node/{NODE_ID}"],120).check_returncode()
    run(["git","checkout","-B","main","origin/main"],30).check_returncode()

def execute(cmd):
    operation=cmd.get("operation")
    if operation=="health":
        return {"status":"ready","node_id":NODE_ID,"hostname":platform.node(),
                "platform":platform.platform(),"python":platform.python_version(),
                "transport_version":"self-reexec-v1","agent_source_sha":RUNNING_AGENT_SHA,
                "pid":os.getpid(),"cwd":os.getcwd(),
                "agent_path":str(Path(__file__).resolve()),
                "worktree":str(ROOT.resolve())}
    if operation == "execution_backend_qualification":
        script=ROOT/"ops"/"qualification"/"qualify_execution_backends.py"
        if not script.exists():
            raise FileNotFoundError(f"execution backend qualification probe not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=120,check=False)
        payload={"returncode":result.returncode,"stdout":result.stdout[-20000:],"stderr":result.stderr[-10000:]}
        payload["status"]="PASS" if result.returncode == 0 else "BLOCKED"
        return payload
    if operation == "qualification":
        script=ROOT/"ops"/"qualification"/"astra_gold_executor.py"
        if not script.exists():
            raise FileNotFoundError(f"qualification executor not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=int(os.environ.get("ASTRA_QUALIFICATION_TIMEOUT","87000")),check=False)
        payload={"returncode":result.returncode,"stdout":result.stdout[-20000:],"stderr":result.stderr[-10000:]}
        if result.returncode != 0:
            payload["status"]="BLOCKED"
        return payload
    if operation not in OPERATIONS: raise ValueError("unsupported operation")
    configured=os.environ.get("ASTRA_RUNTIME_ROOT","").strip()
    candidates=[]
    if configured:
        candidates.append(Path(configured))
    candidates.extend([ROOT/"runtime",Path("/opt/mediahub/astra/runtime"),Path("/home/mediahub/dev/mediahub-os-autonomous/runtime"),Path("/Users/voktor/astra-work/runtime")])
    runtime_root=None
    for candidate in candidates:
        if (candidate/"mediahub_runtime"/"astra_gateway.py").exists():
            runtime_root=candidate
            break
    if runtime_root is None:
        raise ModuleNotFoundError("mediahub_runtime runtime root not found; checked: " + ", ".join(str(p) for p in candidates))
    runtime_root=str(runtime_root.resolve())
    package_dir=Path(runtime_root)/"mediahub_runtime"
    if not package_dir.is_dir() or not (package_dir/"__init__.py").is_file():
        raise ModuleNotFoundError("mediahub_runtime package is incomplete at " + str(package_dir))
    if runtime_root not in sys.path:
        sys.path.insert(0,runtime_root)
    os.environ["PYTHONPATH"]=runtime_root + (os.pathsep + os.environ["PYTHONPATH"] if os.environ.get("PYTHONPATH") else "")
    importlib.invalidate_caches()
    try:
        from mediahub_runtime.astra_gateway import AstraGatewayRuntime
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "mediahub_runtime import failed; runtime_root=" + runtime_root +
            "; package_dir=" + str(package_dir) +
            "; sys_executable=" + sys.executable
        ) from exc
    return AstraGatewayRuntime().run_bounded({
        "task_id":cmd.get("command_id","github-task"),"title":cmd.get("title",operation),
        "description":cmd.get("description",""),"capability":operation})

def main():
    STATE.mkdir(parents=True,exist_ok=True)
    last_id=""
    while True:
        try:
            sync(); maybe_reexec_updated_agent(); cmd=read_command()
            if cmd and cmd.get("command_id")!=last_id:
                started=time.time()
                try: value,rc=execute(cmd),0
                except Exception as exc: value,rc={"error":repr(exc)},1
                publish({"schema":1,"node_id":NODE_ID,"command_id":cmd.get("command_id"),
                         "target_sha":cmd.get("target_sha"),
                         "execution_head":run(["git","rev-parse","HEAD"],10).stdout.strip(),
                         "returncode":rc,"duration_seconds":round(time.time()-started,3),
                         "result":value,"completed_at":int(time.time())})
                last_id=str(cmd.get("command_id"))
        except Exception as exc:
            (STATE/"last_error.json").write_text(json.dumps({"error":repr(exc),"time":int(time.time())}))
        time.sleep(INTERVAL)

if __name__=="__main__": main()
