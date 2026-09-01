#!/usr/bin/env python3
import argparse, hashlib, json, os, pathlib, shutil, sys
from datetime import datetime, timezone

ROOT = pathlib.Path.cwd()
ORCH = ROOT / ".mhx"

def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def canonical(o): return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
def read_json(path): return json.loads(path.read_text(encoding="utf-8"))

def manifest(args):
    base=pathlib.Path(args.path).resolve(); files=[]
    excludes={".git", ".mhx", "__pycache__"}
    for p in sorted(base.rglob("*")):
        if not p.is_file() or any(x in excludes for x in p.parts): continue
        b=p.read_bytes(); rel=p.relative_to(base).as_posix()
        files.append({"source_id":"SRC-LOCAL","path":rel,"type":p.suffix.lstrip(".") or "file","size":len(b),"content_hash":sha256_bytes(b)})
    out={"schema":"manifest-1.0","generated_at":now(),"root":str(base),"files":files}
    write_json(ORCH/"master/manifest.json",out); print(json.dumps(out,indent=2,ensure_ascii=False))

def index(args):
    m=read_json(ORCH/"master/manifest.json"); arts=[]
    for f in m["files"]:
        aid="ART-"+sha256_bytes(f["path"].encode())[:12]
        arts.append({"artifact_id":aid,"path":f["path"],"revision":"R0","content_hash":f["content_hash"],"status":"DISCOVERED","source":"SRC-LOCAL"})
    write_json(ORCH/"master/artifact-index.json",{"schema":"artifact-index-1.0","generated_at":now(),"artifacts":arts})
    print(f"indexed {len(arts)} artifacts")

def chunk(args):
    idx=read_json(ORCH/"master/artifact-index.json"); root=pathlib.Path(read_json(ORCH/"master/manifest.json")["root"]); rows=[]
    for a in idx["artifacts"]:
        p=root/a["path"]
        if not p.exists(): continue
        text=p.read_text(encoding="utf-8",errors="replace")
        lines=text.splitlines()
        size=max(1,args.lines)
        for i in range(0,len(lines),size):
            body="\n".join(lines[i:i+size])+"\n"
            cid="CH-"+sha256_bytes((a["artifact_id"]+a["revision"]+str(i)).encode())[:12]
            rows.append({"chunk_id":cid,"parent_artifact":a["artifact_id"],"revision":a["revision"],"path":a["path"],"range":{"start":i+1,"end":min(i+size,len(lines))},"hash":sha256_bytes(body.encode()),"summary":"line chunk"})
    write_json(ORCH/"master/chunk-index.json",{"schema":"chunk-index-1.0","generated_at":now(),"chunks":rows}); print(f"created {len(rows)} chunks")

def task(args):
    t={"task_schema":"1.0","task_id":args.task_id,"task_class":args.task_class,"objective":args.objective,"base_revision":args.base_revision,"input_artifacts":args.artifacts,"required_chunks":args.chunks,"constraints":args.constraints or [],"do_not_rules":["do_not_create_governance_records","do_not_infer_historical_identity","do_not_modify_master"],"context_level":args.context,"impact":{"governance":args.governance,"historical":args.historical,"baseline":args.baseline}}
    t["task_hash"]=sha256_bytes(canonical({k:v for k,v in t.items() if k!="task_hash"})); write_json(ORCH/f"tasks/pending/{args.task_id}.json",t); print(json.dumps(t,indent=2,ensure_ascii=False))

def normalize(args):
    raw=read_json(pathlib.Path(args.input)); result={"result_schema":"1.0","result_id":args.result_id,"task_id":raw["task_id"],"worker_id":raw["worker_id"],"input_revision":raw.get("input_revision"),"status":raw.get("status","UNKNOWN"),"findings":raw.get("findings",[]),"evidence":raw.get("evidence",[]),"sources":raw.get("sources",[]),"unknowns":raw.get("unknowns",[]),"conflicts":raw.get("conflicts",[]),"risks":raw.get("risks",[]),"changed_artifacts":raw.get("changed_artifacts",[]),"confidence":raw.get("confidence","UNKNOWN"),"recommended_action":raw.get("recommended_action"),"provenance":{"generated_by":raw["worker_id"],"generated_at":now(),"input_hash":sha256_bytes(pathlib.Path(args.input).read_bytes())}}
    result["result_hash"]=sha256_bytes(canonical(result)); write_json(ORCH/f"results/normalized/{args.result_id}.json",result); print(json.dumps(result,indent=2,ensure_ascii=False))

def cache(args):
    p=ORCH/f"cache/results/{args.task_hash}.json"
    if p.exists(): print(json.dumps(read_json(p),indent=2,ensure_ascii=False)); return 0
    print("CACHE_MISS"); return 1

def status(args):
    dirs=["tasks/pending","tasks/running","tasks/completed","tasks/failed","results/normalized","results/reviewed"]
    s={d:len(list((ORCH/d).glob("*.json"))) if (ORCH/d).exists() else 0 for d in dirs}
    s.update({"development_phase":"EXECUTION_ARCHITECTURE","governance":{"external_state":"FROZEN","do_not_modify":True}}); write_json(ORCH/"master/state.json",s); print(json.dumps(s,indent=2))

def init(args):
    for d in ["master","tasks/pending","tasks/running","tasks/completed","tasks/failed","results/raw","results/normalized","results/reviewed","cache/results","revisions"]: (ORCH/d).mkdir(parents=True,exist_ok=True)
    write_json(ORCH/"master/evidence-ledger.json",{"schema":"evidence-ledger-1.0","records":[]}); status(args)

def main():
    p=argparse.ArgumentParser(prog="mhx"); sp=p.add_subparsers(dest="cmd",required=True)
    q=sp.add_parser("init"); q.set_defaults(func=init)
    q=sp.add_parser("manifest"); q.add_argument("path"); q.set_defaults(func=manifest)
    q=sp.add_parser("index"); q.set_defaults(func=index)
    q=sp.add_parser("chunk"); q.add_argument("--lines",type=int,default=80); q.set_defaults(func=chunk)
    q=sp.add_parser("task"); ss=q.add_subparsers(dest="sub",required=True); c=ss.add_parser("create"); c.add_argument("task_id"); c.add_argument("objective"); c.add_argument("--task-class",default="T1"); c.add_argument("--base-revision",default="R0"); c.add_argument("--artifacts",nargs="*",default=[]); c.add_argument("--chunks",nargs="*",default=[]); c.add_argument("--constraints",nargs="*",default=[]); c.add_argument("--context",default="CXT-1"); c.add_argument("--governance",action="store_true"); c.add_argument("--historical",action="store_true"); c.add_argument("--baseline",action="store_true"); c.set_defaults(func=task)
    q=sp.add_parser("result"); ss=q.add_subparsers(dest="sub",required=True); c=ss.add_parser("normalize"); c.add_argument("input"); c.add_argument("result_id"); c.set_defaults(func=normalize)
    q=sp.add_parser("cache"); q.add_argument("task_hash"); q.set_defaults(func=cache)
    q=sp.add_parser("status"); q.set_defaults(func=status)
    args=p.parse_args();
    if args.cmd!="init" and not ORCH.exists(): print("MHX_NOT_INITIALIZED",file=sys.stderr); return 2
    return args.func(args) or 0
if __name__=="__main__": sys.exit(main())
