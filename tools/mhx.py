#!/usr/bin/env python3
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile
from datetime import datetime, timezone

ROOT = pathlib.Path.cwd()
ORCH = ROOT / ".mhx"
RESULT_STATUSES = {"FOUND","NOT_FOUND","OBSERVED","INFERRED","UNVERIFIED","CONFLICT","UNKNOWN"}
TASK_STATES = {"PENDING","RUNNING","COMPLETED","FAILED","BLOCKED"}
REVIEW_STATES = {"PENDING","ACCEPT","REJECT","CLARIFY"}

def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def canonical(o): return json.dumps(o, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()
def write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def read_json(path): return json.loads(path.read_text(encoding="utf-8"))
def fail(msg, code=2): print(msg,file=sys.stderr); return code
def require_init(): return ORCH.exists() and (ORCH/"master").exists()
def safe_rel(path):
    p=pathlib.Path(path)
    if p.is_absolute() or ".." in p.parts: raise ValueError("unsafe path")
    return p
def governance_blocked(t):
    impact=t.get("impact",{})
    return any(bool(impact.get(k)) for k in ("governance","historical","baseline"))
def next_revision():
    p=ORCH/"master/state.json"
    if p.exists():
        s=read_json(p); return f"R{int(s.get('revision_number',0))+1}"
    return "R1"

def init(args):
    for d in ["master","tasks/pending","tasks/running","tasks/completed","tasks/failed","results/raw","results/normalized","results/reviewed","cache/results","cache/related","review","revisions","rollback"]:
        (ORCH/d).mkdir(parents=True,exist_ok=True)
    if not (ORCH/"master/evidence-ledger.json").exists():
        write_json(ORCH/"master/evidence-ledger.json",{"schema":"evidence-ledger-1.0","records":[]})
    state={"schema":"mhx-state-1.0","revision":"R0","revision_number":0,"development_phase":"EXECUTION_ARCHITECTURE","governance":{"external_state":"FROZEN","do_not_modify":True}}
    write_json(ORCH/"master/state.json",state)
    print("MHX_INITIALIZED"); return 0

def manifest(args):
    base=pathlib.Path(args.path).resolve(); files=[]; excludes={".git",".mhx","__pycache__"}
    for p in sorted(base.rglob("*")):
        if not p.is_file() or any(x in excludes for x in p.parts): continue
        b=p.read_bytes(); files.append({"source_id":"SRC-LOCAL","path":p.relative_to(base).as_posix(),"type":p.suffix.lstrip(".") or "file","size":len(b),"content_hash":sha256_bytes(b)})
    out={"schema":"manifest-1.0","generated_at":now(),"root":str(base),"files":files,"content_hash":sha256_bytes(canonical(files))}
    write_json(ORCH/"master/manifest.json",out); print(f"manifest: {len(files)} files")

def index(args):
    m=read_json(ORCH/"master/manifest.json"); previous={}
    ip=ORCH/"master/artifact-index.json"
    if ip.exists(): previous={a["path"]:a for a in read_json(ip).get("artifacts",[])}
    arts=[]
    for f in m["files"]:
        old=previous.get(f["path"]); revision=old["revision"] if old and old["content_hash"]==f["content_hash"] else (old["revision"] if old else "R0")
        status="INDEXED" if old and old["content_hash"]==f["content_hash"] else "DISCOVERED"
        aid=old["artifact_id"] if old else "ART-"+sha256_bytes(f["path"].encode())[:12]
        arts.append({"artifact_id":aid,"path":f["path"],"revision":revision,"content_hash":f["content_hash"],"status":status,"source":"SRC-LOCAL"})
    write_json(ip,{"schema":"artifact-index-1.0","generated_at":now(),"artifacts":arts})
    print(f"indexed {len(arts)} artifacts")

def chunk(args):
    idx=read_json(ORCH/"master/artifact-index.json"); root=pathlib.Path(read_json(ORCH/"master/manifest.json")["root"]); rows=[]; size=max(1,args.lines)
    for a in idx["artifacts"]:
        p=root/a["path"]
        try: text=p.read_text(encoding="utf-8")
        except (UnicodeDecodeError,OSError): continue
        lines=text.splitlines()
        for i in range(0,len(lines),size):
            body="\n".join(lines[i:i+size])+"\n"
            rows.append({"chunk_id":"CH-"+sha256_bytes((a["artifact_id"]+a["revision"]+str(i)+sha256_bytes(body.encode())).encode())[:12],"parent_artifact":a["artifact_id"],"parent_revision":a["revision"],"content_hash":sha256_bytes(body.encode()),"path":a["path"],"range":{"start":i+1,"end":min(i+size,len(lines))},"summary":f"lines {i+1}-{min(i+size,len(lines))}","tags":[]})
    write_json(ORCH/"master/chunk-index.json",{"schema":"chunk-index-1.0","generated_at":now(),"chunks":rows})
    print(f"created {len(rows)} chunks")

def task_create(args):
    t={"task_schema":"1.0","task_id":args.task_id,"task_class":args.task_class,"objective":args.objective,"base_revision":args.base_revision,"input_artifacts":args.artifacts,"required_chunks":args.chunks,"constraints":args.constraints,"do_not_rules":["do_not_create_governance_records","do_not_infer_historical_identity","do_not_modify_master"],"known_unknowns":[],"dependencies":[],"expected_output":args.expected_output,"context_level":args.context,"impact":{"governance":args.governance,"historical":args.historical,"baseline":args.baseline},"state":"PENDING"}
    if args.context not in {"CXT-0","CXT-1","CXT-2","CXT-3","CXT-4"}: return fail("INVALID_CONTEXT")
    t["task_hash"]=sha256_bytes(canonical({k:v for k,v in t.items() if k!="task_hash"}))
    if governance_blocked(t) or args.task_class=="T6":
        t["state"]="BLOCKED"; t["block_reason"]="GOVERNANCE_IMPACT"; t["blocked_at"]=now()
        write_json(ORCH/f"tasks/failed/{args.task_id}.json",t); print("TASK_BLOCKED_GOVERNANCE"); return 3
    write_json(ORCH/f"tasks/pending/{args.task_id}.json",t); print(json.dumps(t,indent=2,ensure_ascii=False)); return 0

def task_claim(args):
    src=ORCH/f"tasks/pending/{args.task_id}.json"; dst=ORCH/f"tasks/running/{args.task_id}.json"
    if not src.exists(): return fail("TASK_NOT_FOUND")
    t=read_json(src); t["state"]="RUNNING"; t["claimed_at"]=now(); t["worker_id"]=args.worker_id
    os.replace(src,dst); print("TASK_RUNNING")

def normalize(args):
    raw=read_json(pathlib.Path(args.input)); status=raw.get("status","UNKNOWN")
    if status not in RESULT_STATUSES: return fail("INVALID_RESULT_STATUS")
    result={"result_schema":"1.0","result_id":args.result_id,"task_id":raw["task_id"],"worker_id":raw["worker_id"],"input_revision":raw.get("input_revision"),"status":status,"findings":raw.get("findings",[]),"evidence":raw.get("evidence",[]),"sources":raw.get("sources",[]),"unknowns":raw.get("unknowns",[]),"conflicts":raw.get("conflicts",[]),"risks":raw.get("risks",[]),"changed_artifacts":raw.get("changed_artifacts",[]),"confidence":raw.get("confidence","UNKNOWN"),"recommended_action":raw.get("recommended_action"),"provenance":{"generated_by":raw["worker_id"],"generated_at":now(),"input_hash":sha256_bytes(pathlib.Path(args.input).read_bytes())}}
    result["result_hash"]=sha256_bytes(canonical(result)); out=ORCH/f"results/normalized/{args.result_id}.json"; write_json(out,result)
    task=ORCH/f"tasks/running/{result['task_id']}.json"
    if task.exists():
        t=read_json(task); t["state"]="COMPLETED"; t["completed_at"]=now(); t["result_id"]=args.result_id
        os.replace(task,ORCH/f"tasks/completed/{result['task_id']}.json")
    print(json.dumps(result,indent=2,ensure_ascii=False))

def cache(args):
    exact=ORCH/f"cache/results/{args.task_hash}.json"
    if exact.exists(): print(json.dumps({"match":"EXACT","result":read_json(exact)},indent=2,ensure_ascii=False)); return 0
    related=sorted((ORCH/"cache/related").glob(f"{args.task_hash[:12]}-*.json"))
    if related:
        print(json.dumps({"match":"RELATED","results":[read_json(p) for p in related]},indent=2,ensure_ascii=False)); return 0
    print(json.dumps({"match":"NONE"})); return 1

def cache_store(args):
    result=read_json(pathlib.Path(args.result)); write_json(ORCH/f"cache/results/{args.task_hash}.json",result)
    if args.related: write_json(ORCH/f"cache/related/{args.task_hash[:12]}-{result['result_id']}.json",result)
    print("CACHE_STORED")

def review(args):
    rp=ORCH/f"results/normalized/{args.result_id}.json"
    if not rp.exists(): return fail("RESULT_NOT_FOUND")
    result=read_json(rp)
    record={"review_schema":"1.0","result_id":args.result_id,"decision":args.decision,"reviewer":"PRIMARY","reviewed_at":now(),"notes":args.notes or ""}
    write_json(ORCH/f"results/reviewed/{args.result_id}.json",record); print(f"RESULT_{args.decision}"); return 0

def revision(args):
    accepted=[]
    for p in sorted((ORCH/"results/reviewed").glob("*.json")):
        r=read_json(p)
        if r["decision"]=="ACCEPT": accepted.append(r["result_id"])
    parent=read_json(ORCH/"master/state.json").get("revision","R0"); rev=next_revision()
    out={"revision":rev,"parent_revision":parent,"created_at":now(),"integrated_tasks":args.tasks or [],"accepted_results":accepted,"modified_artifacts":[],"new_artifacts":[],"new_evidence":[],"superseded_artifacts":[],"review":{"reviewer":"PRIMARY","status":"READY"}}
    write_json(ORCH/f"revisions/{rev}.json",out); print(json.dumps(out,indent=2)); return 0

def integrate(args):
    rp=ORCH/f"results/normalized/{args.result_id}.json"; rv=ORCH/f"results/reviewed/{args.result_id}.json"
    if not rp.exists() or not rv.exists(): return fail("RESULT_NOT_REVIEWED")
    if read_json(rv)["decision"]!="ACCEPT": return fail("RESULT_NOT_ACCEPTED")
    result=read_json(rp)
    if result["status"] in {"CONFLICT","UNKNOWN","UNVERIFIED"}: return fail("RESULT_NOT_INTEGRABLE")
    backups=[]; backup=ORCH/f"rollback/{result['result_id']}-{now().replace(':','')}.json"
    try:
        for item in result.get("changed_artifacts",[]):
            path=safe_rel(item["path"]); target=ROOT/path; old=target.read_bytes() if target.exists() else None
            backups.append({"path":str(path),"old":old.decode("utf-8") if old is not None else None})
            target.parent.mkdir(parents=True,exist_ok=True); content=item.get("content")
            if content is None: raise ValueError(f"missing content for {path}")
            fd,tmp=tempfile.mkstemp(dir=str(target.parent),prefix=".mhx-",text=True)
            with os.fdopen(fd,"w",encoding="utf-8") as f: f.write(content)
            os.replace(tmp,target)
            if "content_hash" in item and sha256_bytes(content.encode())!=item["content_hash"]: raise ValueError(f"hash mismatch {path}")
        write_json(backup,{"result_id":result["result_id"],"created_at":now(),"files":backups})
    except Exception as e:
        for b in reversed(backups):
            target=ROOT/pathlib.Path(b["path"])
            if b["old"] is None:
                if target.exists(): target.unlink()
            else: target.write_text(b["old"],encoding="utf-8")
        return fail(f"INTEGRATION_ROLLED_BACK: {e}")
    state=read_json(ORCH/"master/state.json"); n=int(state.get("revision_number",0))+1; state.update({"revision":f"R{n}","revision_number":n,"last_integrated_result":result["result_id"],"updated_at":now()}); write_json(ORCH/"master/state.json",state)
    print(f"INTEGRATED {result['result_id']} -> R{n}"); return 0

def status(args):
    dirs=["tasks/pending","tasks/running","tasks/completed","tasks/failed","results/normalized","results/reviewed","review","revisions"]
    s={d:len(list((ORCH/d).glob("*.json"))) if (ORCH/d).exists() else 0 for d in dirs}
    s.update(read_json(ORCH/"master/state.json") if (ORCH/"master/state.json").exists() else {"revision":"R0"}); print(json.dumps(s,indent=2,ensure_ascii=False)); return 0

def main():
    p=argparse.ArgumentParser(prog="mhx"); sp=p.add_subparsers(dest="cmd",required=True)
    q=sp.add_parser("init"); q.set_defaults(func=init)
    q=sp.add_parser("manifest"); q.add_argument("path"); q.set_defaults(func=manifest)
    q=sp.add_parser("index"); q.set_defaults(func=index)
    q=sp.add_parser("chunk"); q.add_argument("--lines",type=int,default=80); q.set_defaults(func=chunk)
    q=sp.add_parser("task"); ss=q.add_subparsers(dest="sub",required=True)
    c=ss.add_parser("create"); c.add_argument("task_id"); c.add_argument("objective"); c.add_argument("--task-class",default="T1"); c.add_argument("--base-revision",default="R0"); c.add_argument("--artifacts",nargs="*",default=[]); c.add_argument("--chunks",nargs="*",default=[]); c.add_argument("--constraints",nargs="*",default=[]); c.add_argument("--expected-output",default="result pack"); c.add_argument("--context",default="CXT-1"); c.add_argument("--governance",action="store_true"); c.add_argument("--historical",action="store_true"); c.add_argument("--baseline",action="store_true"); c.set_defaults(func=task_create)
    c=ss.add_parser("claim"); c.add_argument("task_id"); c.add_argument("worker_id"); c.set_defaults(func=task_claim)
    q=sp.add_parser("result"); ss=q.add_subparsers(dest="sub",required=True); c=ss.add_parser("normalize"); c.add_argument("input"); c.add_argument("result_id"); c.set_defaults(func=normalize)
    q=sp.add_parser("cache"); q.add_argument("task_hash"); q.set_defaults(func=cache)
    q=sp.add_parser("cache-store"); q.add_argument("task_hash"); q.add_argument("result"); q.add_argument("--related",action="store_true"); q.set_defaults(func=cache_store)
    q=sp.add_parser("review"); q.add_argument("result_id"); q.add_argument("decision",choices=["ACCEPT","REJECT","CLARIFY"]); q.add_argument("--notes"); q.set_defaults(func=review)
    q=sp.add_parser("revision"); q.add_argument("--tasks",nargs="*",default=[]); q.set_defaults(func=revision)
    q=sp.add_parser("integrate"); q.add_argument("result_id"); q.set_defaults(func=integrate)
    q=sp.add_parser("status"); q.set_defaults(func=status)
    args=p.parse_args()
    if args.cmd!="init" and not require_init(): return fail("MHX_NOT_INITIALIZED")
    try: return args.func(args) or 0
    except (KeyError,ValueError,FileNotFoundError) as e: return fail(f"MHX_ERROR: {e}")
if __name__=="__main__": sys.exit(main())
