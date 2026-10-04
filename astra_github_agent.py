#!/usr/bin/env python3
"""MediaHub Astra GitHub transport worker."""
from __future__ import annotations
import hashlib, hmac, importlib, json, os, platform, re, subprocess, sys, time
from dataclasses import asdict
from pathlib import Path

REPO=os.environ.get("ASTRA_GITHUB_REPO","VlDMlNSh/mediahub-os")
REMOTE=os.environ.get("ASTRA_GITHUB_REMOTE",f"git@github.com:{REPO}.git")
NODE_ID=os.environ.get("ASTRA_NODE_ID",platform.node())
INTERVAL=max(15,int(os.environ.get("ASTRA_POLL_SECONDS","30")))
ROOT=Path(os.environ.get("ASTRA_WORKTREE","/opt/mediahub/astra-worktree"))
STATE=Path(os.environ.get("ASTRA_STATE_DIR","/var/lib/mediahub-astra"))
OPERATIONS={"health","research","architecture","review","documents","coding","coding_v2","qualification","execution_backend_qualification","pre_soak_evidence","timezone_sync","autonomous_qualification_queue","autonomous_gold_mission","reconcile_controller_processes","codex_diagnostic","codex_config_isolation","codex_process_diagnostic","codex_cleanup_stale_probes","codex_provider_diagnostic","codex_gateway_diagnostic","provider_model_qualification","local_component_inventory","local_component_qualification","local_ai_capability_qualification","dual_local_executor_23wave"}
RUNNING_AGENT_SHA=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
AGENT_ID=os.environ.get('ASTRA_AGENT_ID','A0-ASTRA')
WORKER_ID=os.environ.get('ASTRA_WORKER_ID',f"{AGENT_ID}:{os.getpid()}")
CLAIM_LEASE_SECONDS=max(60.0,min(float(os.environ.get('ASTRA_CLAIM_LEASE_SECONDS','900')),3600.0))
COMMAND_HMAC_MAX_AGE_SECONDS=max(60,int(os.environ.get("ASTRA_COMMAND_HMAC_MAX_AGE_SECONDS","900")))
COMMAND_HMAC_KEY=os.environ.get("ASTRA_COMMAND_HMAC_KEY","")
COMMAND_SCHEMA_VERSION="mediahub.astra.control-command.v1"
EXECUTED_COMMANDS=STATE/"executed_command_ids"
SAFE_ID_RE=re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
SHA_RE=re.compile(r"^[0-9a-fA-F]{40,64}$")
REQUIRED_COMMAND_FIELDS={"schema_version","command_id","node_id","operation","target_sha","workflow_only","owned_paths","title","description","exclusive_actions","issued_at"}

def _safe_id(value, label):
    if not isinstance(value,str) or not SAFE_ID_RE.fullmatch(value):
        raise ValueError(f"invalid {label}")
    return value

def _valid_target_sha(value):
    return isinstance(value,str) and bool(SHA_RE.fullmatch(value))

def _current_head():
    result=run(["git","rev-parse","HEAD"],10)
    return result.stdout.strip() if result.returncode == 0 else ""

def run(argv,timeout=120):
    return subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout,check=False)

def git_network(argv, timeout=120, attempts=4, base_delay=2.0):
    """Run a Git network operation with bounded exponential retry; fail closed after exhaustion."""
    last = None
    for attempt in range(1, attempts + 1):
        result = run(argv, timeout)
        if result.returncode == 0:
            return result
        last = result
        if attempt < attempts:
            time.sleep(min(base_delay * (2 ** (attempt - 1)), 15.0))
    return last

def sync():
    ROOT.parent.mkdir(parents=True,exist_ok=True)
    if not (ROOT/".git").exists():
        subprocess.run(["git","clone","--depth","1",REMOTE,str(ROOT)],check=True,timeout=120)
    else:
        git_network(["git","-C",str(ROOT),"fetch","--depth","50","origin","main"],120).check_returncode()
        git_network(["git","-C",str(ROOT),"fetch","origin",f"+astra-node/{NODE_ID}:refs/remotes/origin/astra-node/{NODE_ID}"],120)
        subprocess.run(["git","-C",str(ROOT),"reset","--hard","origin/main"],check=True,timeout=120)

def maybe_reexec_updated_agent():
    target=ROOT/"astra_github_agent.py"
    if not target.exists():
        return
    target_sha=hashlib.sha256(target.read_bytes()).hexdigest()
    if target_sha != RUNNING_AGENT_SHA:
        os.execv(sys.executable,[sys.executable,str(target),*sys.argv[1:]])

def _canonical_command_body(cmd):
    return json.dumps({k:v for k,v in cmd.items() if k != "signature"}, sort_keys=True, separators=(",", ":")).encode("utf-8")

def _command_auth_valid(cmd):
    if not COMMAND_HMAC_KEY: return False
    signature, issued_at, command_id = cmd.get("signature"), cmd.get("issued_at"), cmd.get("command_id")
    if not isinstance(signature,str) or not signature or not isinstance(issued_at,int) or isinstance(issued_at,bool): return False
    if not isinstance(command_id,str) or not SAFE_ID_RE.fullmatch(command_id): return False
    if abs(int(time.time())-issued_at)>COMMAND_HMAC_MAX_AGE_SECONDS: return False
    expected=hmac.new(COMMAND_HMAC_KEY.encode("utf-8"), _canonical_command_body(cmd), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)

def _command_already_executed(command_id):
    try: return (EXECUTED_COMMANDS/f"{command_id}.done").is_file()
    except OSError: return True

def _mark_command_executed(command_id):
    EXECUTED_COMMANDS.mkdir(parents=True,exist_ok=True)
    tmp=EXECUTED_COMMANDS/f"{command_id}.tmp"
    tmp.write_text(str(int(time.time()))+"\n",encoding="utf-8")
    tmp.replace(EXECUTED_COMMANDS/f"{command_id}.done")

def read_command():
    _safe_id(NODE_ID, "node identity")
    path=ROOT/"control"/"commands"/f"{NODE_ID}.json"
    if not path.exists(): return None
    try: cmd=json.loads(path.read_text(encoding="utf-8"))
    except Exception: return None
    if not isinstance(cmd,dict) or not REQUIRED_COMMAND_FIELDS.issubset(cmd): return None
    if cmd.get("schema_version") != COMMAND_SCHEMA_VERSION: return None
    if not _safe_id(cmd.get("command_id"), "command id"): return None
    if cmd.get("node_id")!=NODE_ID or cmd.get("operation") not in OPERATIONS: return None
    if not _valid_target_sha(cmd.get("target_sha")): return None
    if cmd.get("workflow_only") is not True and not isinstance(cmd.get("workflow_only"), bool): return None
    if cmd.get("workflow_only") is True and os.environ.get("ASTRA_WORKFLOW_ONLY") != "1": return None
    if not isinstance(cmd.get("owned_paths"),list) or not all(isinstance(p,str) and p and not Path(p).is_absolute() and ".." not in Path(p).parts for p in cmd["owned_paths"]): return None
    if not isinstance(cmd.get("exclusive_actions"),list) or not all(isinstance(x,str) and x for x in cmd["exclusive_actions"]): return None
    if not isinstance(cmd.get("title"),str) or not isinstance(cmd.get("description"),str): return None
    if not isinstance(cmd.get("issued_at"),int) or isinstance(cmd.get("issued_at"),bool): return None
    if not _command_auth_valid(cmd): return None
    if _current_head().lower() != cmd["target_sha"].lower(): return None
    command_id=cmd["command_id"]
    if _command_already_executed(command_id): return None
    return cmd

def published_command_id():
    state=STATE/"last_command_id"
    try:
        value=state.read_text(encoding="utf-8").strip()
        if value: return value
    except OSError:
        pass
    ref=f"origin/astra-node/{NODE_ID}"
    try:
        raw=run(["git","show",f"{ref}:control/results/{NODE_ID}.json"],30)
        if raw.returncode==0:
            return str(json.loads(raw.stdout).get("command_id",""))
    except Exception:
        pass
    return ""

def mark_published(command_id):
    tmp=STATE/"last_command_id.tmp"
    tmp.write_text(str(command_id)+"\n",encoding="utf-8")
    tmp.replace(STATE/"last_command_id")

def _prepare_publish_branch():
    _safe_id(NODE_ID, "node identity")
    branch=f"astra-node/{NODE_ID}"
    probe=git_network(["git","ls-remote","--heads","origin",branch],30)
    if probe.returncode == 0 and probe.stdout.strip():
        git_network(["git","fetch","origin",f"{branch}:refs/remotes/origin/{branch}"],120).check_returncode()
        run(["git","checkout","-B",branch,f"origin/{branch}"],30).check_returncode()
    elif probe.returncode == 0:
        run(["git","checkout","-B",branch,"origin/main"],30).check_returncode()
    else:
        raise RuntimeError(probe.stderr or "unable to verify remote result branch")

def publish(result):
    _safe_id(NODE_ID, "node identity")
    path=ROOT/"control"/"results"/f"{NODE_ID}.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    for args in (["git","config","user.name","Astra Node Agent"],["git","config","user.email","astra-node@localhost"]):
        run(args,30).check_returncode()
    _prepare_publish_branch()
    run(["git","add",str(path.relative_to(ROOT))],30).check_returncode()
    commit=run(["git","commit","-m",f"astra: result {NODE_ID}"],30)
    if commit.returncode not in (0,1): raise RuntimeError(commit.stderr)
    git_network(["git","push","origin",f"HEAD:astra-node/{NODE_ID}"],120).check_returncode()
    run(["git","checkout","-B","main","origin/main"],30).check_returncode()
