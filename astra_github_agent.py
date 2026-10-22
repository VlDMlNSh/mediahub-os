#!/usr/bin/env python3
"""MediaHub Astra GitHub transport worker."""
from __future__ import annotations
import hashlib, hmac, importlib, json, os, platform, re, subprocess, sys, time, tempfile
from dataclasses import asdict
from pathlib import Path

REPO=os.environ.get("ASTRA_GITHUB_REPO","VlDMlNSh/mediahub-os")
REMOTE=os.environ.get("ASTRA_GITHUB_REMOTE",f"git@github.com:{REPO}.git")
NODE_ID=os.environ.get("ASTRA_NODE_ID",platform.node())
INTERVAL=max(15,int(os.environ.get("ASTRA_POLL_SECONDS","30")))
ROOT=Path(os.environ.get("ASTRA_WORKTREE","/opt/mediahub/astra-worktree"))
STATE=Path(os.environ.get("ASTRA_STATE_DIR","/var/lib/mediahub-astra"))
OPERATIONS={"health","research","architecture","review","documents","coding","coding_v2","qualification","execution_backend_qualification","pre_soak_evidence","timezone_sync","autonomous_qualification_queue","autonomous_gold_mission","reconcile_controller_processes","codex_diagnostic","codex_config_isolation","codex_process_diagnostic","codex_cleanup_stale_probes","codex_provider_diagnostic","codex_gateway_diagnostic","provider_model_qualification","local_component_inventory","local_component_qualification","local_ai_capability_qualification","dual_local_executor_23wave"}
# Generic natural-language tasks must not fall through to a host-side cloud-first gateway.
# These operations require the approved GitHub-hosted controller route; until a provider-safe,
# source-pinned bridge is qualified, this worker rejects them before importing any gateway.
UNADMITTED_GENERIC_GATEWAY_OPERATIONS=frozenset({"research","architecture","review","documents","coding","coding_v2"})
RUNNING_AGENT_SHA=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
AGENT_ID=os.environ.get('ASTRA_AGENT_ID','A0-ASTRA')
WORKER_ID=os.environ.get('ASTRA_WORKER_ID',f"{AGENT_ID}:{os.getpid()}")
CLAIM_LEASE_SECONDS=max(60.0,min(float(os.environ.get('ASTRA_CLAIM_LEASE_SECONDS','21600')),21600.0))
COMMAND_HMAC_MAX_AGE_SECONDS=max(60,int(os.environ.get("ASTRA_COMMAND_HMAC_MAX_AGE_SECONDS","900")))
COMMAND_HMAC_ENV = {
    "mh-dev-01": "ASTRA_NODE_HMAC_KEY_MH_DEV_01",
    "mh-dev-02": "ASTRA_NODE_HMAC_KEY_MH_DEV_02",
    "Voktors-Mac-mini.local": "ASTRA_NODE_HMAC_KEY_VOKTORS_MAC",
}
COMMAND_HMAC_KEY=os.environ.get(COMMAND_HMAC_ENV.get(NODE_ID, ""), "")
COMMAND_SCHEMA_VERSION="mediahub.astra.control-command.v1"
EXECUTED_COMMANDS=STATE/"executed_command_ids"
SAFE_ID_RE=re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
SHA_RE=re.compile(r"^[0-9a-fA-F]{40,64}$")
REQUIRED_COMMAND_FIELDS={"schema_version","command_id","node_id","operation","target_sha","workflow_only","owned_paths","title","description","exclusive_actions","issued_at"}

def _safe_id(value, label):
    return isinstance(value,str) and bool(SAFE_ID_RE.fullmatch(value))

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
    if not _safe_id(NODE_ID, "node identity"):
        return None
    path=ROOT/"control"/"commands"/f"{NODE_ID}.json"
    if not path.exists(): return None
    try: cmd=json.loads(path.read_text(encoding="utf-8"))
    except Exception: return None
    if not isinstance(cmd,dict) or not REQUIRED_COMMAND_FIELDS.issubset(cmd): return None
    if cmd.get("schema_version") != COMMAND_SCHEMA_VERSION: return None
    if not _safe_id(cmd.get("command_id"), "command id"): return None
    if cmd.get("node_id")!=NODE_ID or cmd.get("operation") not in OPERATIONS: return None
    if not _valid_target_sha(cmd.get("target_sha")): return None
    if not isinstance(cmd.get("workflow_only"),bool): return None
    if cmd.get("workflow_only") is True and os.environ.get("ASTRA_WORKFLOW_ONLY") != "1": return None
    if not isinstance(cmd.get("owned_paths"),list) or not all(isinstance(p,str) and p and not Path(p).is_absolute() and ".." not in Path(p).parts for p in cmd["owned_paths"]): return None
    if not isinstance(cmd.get("exclusive_actions"),list) or not all(isinstance(x,str) and x for x in cmd["exclusive_actions"]): return None
    if not isinstance(cmd.get("title"),str) or not isinstance(cmd.get("description"),str): return None
    if not isinstance(cmd.get("issued_at"),int) or isinstance(cmd.get("issued_at"),bool): return None
    if not _command_auth_valid(cmd): return None
    if _current_head().lower() != cmd["target_sha"].lower(): return None
    if _command_already_executed(cmd["command_id"]): return None
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
    if not _safe_id(NODE_ID, "node identity"):
        raise RuntimeError("invalid node identity")
    branch=f"astra-node/{NODE_ID}"
    probe=git_network(["git","ls-remote","--heads","origin",branch],30)
    command_path=f"control/commands/{NODE_ID}.json"
    # The signed command is a consumed transport artifact. It must not remain as a
    # dirty worktree change while publish switches to the node result branch.
    # Restore only this exact command path; never clean unrelated user changes.
    restore=run(["git","restore","--source=HEAD","--",command_path],30)
    if restore.returncode != 0:
        # The command may be untracked on a fresh checkout. Remove only that path.
        cleanup=run(["git","clean","-f","--",command_path],30)
        if cleanup.returncode != 0:
            raise RuntimeError(cleanup.stderr or restore.stderr or "unable to clean consumed command")
    if probe.returncode == 0 and probe.stdout.strip():
        fetched=git_network(["git","fetch","origin",f"{branch}:refs/remotes/origin/{branch}"],120)
        if fetched.returncode != 0:
            raise RuntimeError(fetched.stderr or "unable to fetch node result branch")
        checkout=run(["git","checkout","--detach",f"origin/{branch}"],30)
        if checkout.returncode != 0:
            raise RuntimeError(checkout.stderr or "unable to checkout node result branch")
    elif probe.returncode == 0:
        checkout=run(["git","checkout","--detach","origin/main"],30)
        if checkout.returncode != 0:
            raise RuntimeError(checkout.stderr or "unable to checkout main for new node result branch")
    else:
        raise RuntimeError(probe.stderr or "unable to verify remote result branch")


def publish(result):
    path=ROOT/"control"/"results"/f"{NODE_ID}.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    publish_result=dict(result)
    publish_result.setdefault("secret_values","SUPPRESSED")
    payload=json.dumps(publish_result,indent=2,sort_keys=True)+"\n"
    if os.environ.get("ASTRA_DEFER_RESULT_PUBLICATION") == "1":
        path.write_text(payload,encoding="utf-8")
        return
    STATE.mkdir(parents=True,exist_ok=True)
    staged_result=STATE/f"publish-{NODE_ID}.json"
    staged_result.write_text(payload,encoding="utf-8")
    for args in (["git","config","user.name","Astra Node Agent"],["git","config","user.email","astra-node@localhost"]):
        run(args,30).check_returncode()
    _prepare_publish_branch()
    path.write_text(staged_result.read_text(encoding="utf-8"),encoding="utf-8")
    run(["git","add",str(path.relative_to(ROOT))],30).check_returncode()
    commit=run(["git","commit","-m",f"astra: result {NODE_ID}"],30)
    if commit.returncode not in (0,1): raise RuntimeError(commit.stderr)
    # Never rewrite the remote node branch. A concurrent/stale publisher must fail closed.
    git_network(["git","push","origin",f"HEAD:astra-node/{NODE_ID}"],120).check_returncode()
    run(["git","checkout","--detach","origin/main"],30).check_returncode()
    try:
        staged_result.unlink()
    except FileNotFoundError:
        pass
def _claim_for(cmd):
    runtime_root=ROOT/'runtime'
    if runtime_root.is_dir() and str(runtime_root) not in sys.path: sys.path.insert(0,str(runtime_root))
    from mediahub_runtime.agent_fabric import AgentClaim, ClaimStore
    task_id=str(cmd.get('command_id') or 'github-task')
    operation=str(cmd.get('operation') or 'unknown')
    paths=tuple(cmd.get('owned_paths') or [str(Path('control/commands') / f'{NODE_ID}.json')])
    now=time.time()
    return ClaimStore(STATE/'claims'), AgentClaim(
    agent=AGENT_ID, task_id=task_id, goal=str(cmd.get('title') or operation),
    paths=paths, exclusive_actions=tuple(cmd.get('exclusive_actions') or ('execute',)),
    dependencies=tuple(cmd.get('dependencies') or ()), status='ACTIVE',
    started=now, updated=now, expiry=now+CLAIM_LEASE_SECONDS,
    base_sha=str(cmd.get('base_sha') or ''),
    )
def execute(cmd):
    operation=cmd.get("operation")
    journal = None
    if operation in {"autonomous_qualification_queue", "autonomous_gold_mission"}:
        runtime_root = ROOT / "runtime"
        if runtime_root.is_dir() and str(runtime_root) not in sys.path:
            sys.path.insert(0, str(runtime_root))
        from mediahub_runtime.mission_journal import MissionJournal
        journal = MissionJournal(STATE / "mission-journal.json")
        journal.begin(
            command_id=str(cmd.get("command_id") or ""),
            node_id=NODE_ID,
            target_sha=str(cmd.get("target_sha") or ""),
            agent_sha=RUNNING_AGENT_SHA,
        )
    if operation=="health":
        return {"status":"ready","node_id":NODE_ID,"hostname":platform.node(),
                "platform":platform.platform(),"python":platform.python_version(),
                "transport_version":"self-reexec-v1","agent_source_sha":RUNNING_AGENT_SHA,
                "pid":os.getpid(),"cwd":os.getcwd(),
                "agent_path":str(Path(__file__).resolve()),
                "worktree":str(ROOT.resolve())}
    if operation in {"autonomous_qualification_queue", "autonomous_gold_mission"}:
        provider_evidence_path=Path(os.environ.get("ASTRA_PROVIDER_EVIDENCE_PATH",""))
        evidence_script=ROOT/"ops"/"qualification"/"capture_pre_soak_evidence.py"
        verifier_script=ROOT/"ops"/"qualification"/"verify_pre_soak_bundle.py"
        started=time.time()
        max_cycles=max(1,int(os.environ.get("ASTRA_AUTONOMOUS_MAX_CYCLES","12")))
        retry_seconds=max(30,int(os.environ.get("ASTRA_AUTONOMOUS_RETRY_SECONDS","300")))
        prior = journal.load() if journal else None
        steps=list(prior.get("steps", [])) if prior and prior.get("status") == "RUNNING" else []
        target_sha=cmd.get("target_sha","")
        if journal:
            journal.checkpoint(phase="target_reconciliation", cycle=0)
        if target_sha:
            current_head = run(["git", "rev-parse", "HEAD"], 10).stdout.strip()
            if current_head.lower() != str(target_sha).lower():
                return {"status":"BLOCKED","phase":"target_reconciliation",
                        "reason":"target_sha_not_exact_current_head","target_sha":target_sha,
                        "current_head":current_head}
        cycles=1 if operation=="autonomous_qualification_queue" else max_cycles
        for cycle in range(1,cycles+1):
            if journal:
                journal.checkpoint(phase="cycle_started", cycle=cycle)
            if operation=="autonomous_gold_mission" and cycle>1:
                # A workflow-only mission is pinned to the signed target SHA for its
                # entire bounded retry window. Never advance to a moving origin/main
                # between retries; doing so invalidates the command binding.
                if os.environ.get("ASTRA_WORKFLOW_ONLY") != "1":
                    sync()
                current_head = run(["git", "rev-parse", "HEAD"], 10).stdout.strip()
                if target_sha and current_head.lower() != str(target_sha).lower():
                    return {"status":"BLOCKED","phase":"target_reconciliation",
                            "reason":"target_sha_changed_during_retry","target_sha":target_sha,
                            "current_head":current_head,
                            "cycles":steps}
            cycle_record={"cycle":cycle,"head":run(["git","rev-parse","HEAD"],10).stdout.strip()}
            if journal:
                journal.checkpoint(phase="execution_backend_qualification", cycle=cycle)
            provider_status = "BLOCKED"
            provider_payload = {}
            provider_reason = "provider_evidence_missing"
            local_executor_qualified = False
            if provider_evidence_path.is_file():
                try:
                    provider_payload = json.loads(provider_evidence_path.read_text(encoding="utf-8"))
                    provider_status = provider_payload.get("status","BLOCKED")
                    provider_reason = ""
                    if provider_payload.get("schema") != "mediahub.provider-model-qualification.v1":
                        provider_status = "BLOCKED"; provider_reason = "provider_schema_invalid"
                    elif provider_payload.get("target_sha") != target_sha:
                        provider_status = "BLOCKED"; provider_reason = "provider_target_sha_mismatch"
                    elif provider_payload.get("repo_revision") != target_sha:
                        provider_status = "BLOCKED"; provider_reason = "provider_repo_revision_mismatch"
                    elif provider_payload.get("node_id") != "mh-dev-02":
                        provider_status = "BLOCKED"; provider_reason = "provider_node_identity_invalid"
                    elif not isinstance(provider_payload.get("evidence_digest"), str) or not provider_payload.get("evidence_digest").startswith("sha256:"):
                        provider_status = "BLOCKED"; provider_reason = "provider_evidence_digest_invalid"
                    elif provider_payload.get("status") != "PASS":
                        provider_status = "BLOCKED"; provider_reason = "provider_qualification_blocked"
                    else:
                        qualified = [
                            item for item in provider_payload.get("providers", [])
                            if isinstance(item, dict) and item.get("verification_state") == "QUALIFIED"
                        ]
                        if not qualified:
                            provider_status = "BLOCKED"; provider_reason = "no_qualified_provider"
                except Exception:
                    provider_status = "BLOCKED"
                    provider_reason = "provider_evidence_invalid_json"
            cycle_record["backend"]={
                "returncode": 0 if provider_status == "PASS" else 2,
                "status": provider_status,
                "reason": provider_reason,
                "source": "node_local_provider_evidence",
            }
            steps.append(cycle_record)
            if journal:
                journal.checkpoint(phase="execution_backend_qualification_complete", cycle=cycle, step={"cycle":cycle,"phase":"backend","returncode":0 if provider_status=="PASS" else 2,"status":provider_status})
            if provider_status != "PASS":
                local_script = ROOT/"ops"/"qualification"/"qualify_local_ai_capabilities.py"
                local_probe = subprocess.run([sys.executable,str(local_script)],cwd=ROOT,text=True,capture_output=True,timeout=120,check=False)
                local_executor_qualified = local_probe.returncode == 0
                cycle_record["local_executor"] = {
                    "returncode": local_probe.returncode,
                    "status": "PASS" if local_executor_qualified else "BLOCKED",
                    "stdout": local_probe.stdout[-12000:],
                    "stderr": local_probe.stderr[-8000:],
                }
                if local_executor_qualified:
                    provider_reason = "provider_unavailable_local_executor_qualified"
                else:
                    if operation=="autonomous_gold_mission" and cycle<cycles:
                        time.sleep(retry_seconds)
                        continue
                    return {"status":"BLOCKED","phase":"execution_backend_qualification",
                            "steps":steps,"elapsed_seconds":round(time.time()-started,3)}
            if journal:
                journal.checkpoint(phase="pre_soak_evidence", cycle=cycle)
            if local_executor_qualified:
                evidence_script_local = ROOT/"ops"/"qualification"/"capture_pre_soak_evidence.py"
                evidence=subprocess.run(
                    [sys.executable,str(evidence_script_local),"--target-sha",str(target_sha),
                     "--provider-evidence",os.environ.get("ASTRA_PROVIDER_EVIDENCE_PATH",""),
                     "--local-executor"],
                    cwd=ROOT,text=True,capture_output=True,timeout=900,check=False
                )
            else:
                evidence=subprocess.run([sys.executable,str(evidence_script),"--target-sha",str(target_sha),"--provider-evidence",os.environ.get("ASTRA_PROVIDER_EVIDENCE_PATH","")],cwd=ROOT,text=True,
                                        capture_output=True,timeout=900,check=False)
            cycle_record["pre_soak"]={"returncode":evidence.returncode,
                                      "stdout":evidence.stdout[-12000:],"stderr":evidence.stderr[-8000:]}
            if journal:
                journal.checkpoint(phase="pre_soak_evidence_complete", cycle=cycle, step={"cycle":cycle,"phase":"pre_soak","returncode":evidence.returncode})
            if evidence.returncode != 0:
                if operation=="autonomous_gold_mission" and cycle<cycles:
                    time.sleep(retry_seconds)
                    continue
                return {"status":"BLOCKED","phase":"pre_soak_evidence",
                        "steps":steps,"elapsed_seconds":round(time.time()-started,3)}
            if journal:
                journal.checkpoint(phase="strict_pre_soak_verification", cycle=cycle)
            verifier_args=[sys.executable,str(verifier_script),"evidence","--target-sha",str(target_sha)]
            if local_executor_qualified:
                verifier_args.append("--allow-local-executor")
            verifier=subprocess.run(verifier_args,
                                    cwd=ROOT,text=True,capture_output=True,timeout=300,check=False)
            cycle_record["strict_verifier"]={"returncode":verifier.returncode,
                                              "stdout":verifier.stdout[-12000:],
                                              "stderr":verifier.stderr[-8000:]}
            if journal:
                journal.checkpoint(phase="strict_pre_soak_verification_complete", cycle=cycle, step={"cycle":cycle,"phase":"strict_verifier","returncode":verifier.returncode})
            if verifier.returncode != 0:
                if operation=="autonomous_gold_mission" and cycle<cycles:
                    time.sleep(retry_seconds)
                    continue
                return {"status":"BLOCKED","phase":"strict_pre_soak_verification",
                        "steps":steps,"elapsed_seconds":round(time.time()-started,3)}
            if journal:
                journal.checkpoint(phase="distributed_verification", cycle=cycle)
            distributed_dir = Path(os.environ.get(
                "ASTRA_DISTRIBUTED_EVIDENCE_DIR",
                str(ROOT / ".astra-state" / "distributed-verification"),
            ))
            aggregate_path = Path(os.environ.get(
                "ASTRA_DISTRIBUTED_AGGREGATE_PATH",
                str(distributed_dir / "distributed-verification-result.json"),
            ))
            blocked_reasons = []
            distributed_payload = {}
            if not aggregate_path.is_file():
                blocked_reasons.append("distributed_aggregate_missing")
            else:
                try:
                    distributed_payload = json.loads(
                        aggregate_path.read_text(encoding="utf-8")
                    )
                except Exception:
                    blocked_reasons.append("distributed_aggregate_invalid_json")
            required_nodes=["mh-dev-01","mh-dev-02","Voktors-Mac-mini.local"]
            if distributed_payload:
                if distributed_payload.get("schema") != "mediahub.astra.distributed-verification.v1":
                    blocked_reasons.append("distributed_schema_mismatch")
                if distributed_payload.get("status") != "PASS":
                    blocked_reasons.append("distributed_status_not_PASS")
                if distributed_payload.get("phase") != "distributed_verification":
                    blocked_reasons.append("distributed_phase_invalid")
                if distributed_payload.get("returncode") != 0:
                    blocked_reasons.append("distributed_returncode_not_zero")
                if distributed_payload.get("command_id") != cmd.get("command_id"):
                    blocked_reasons.append("distributed_command_binding_mismatch")
                if distributed_payload.get("node_id") != cmd.get("node_id"):
                    blocked_reasons.append("distributed_node_binding_mismatch")
                if distributed_payload.get("target_sha") != target_sha:
                    blocked_reasons.append("distributed_target_sha_mismatch")
                if distributed_payload.get("producer_identity") != "canonical-distributed-verification-producer-v1":
                    blocked_reasons.append("distributed_producer_identity_mismatch")
                if distributed_payload.get("checked_nodes") != required_nodes:
                    blocked_reasons.append("distributed_node_set_mismatch")
                captured_at = distributed_payload.get("captured_at")
                if not isinstance(captured_at, int) or isinstance(captured_at, bool):
                    blocked_reasons.append("distributed_captured_at_invalid")
                elif int(time.time()) - captured_at > max(60, int(os.environ.get("ASTRA_DISTRIBUTED_MAX_AGE_SECONDS", "900"))):
                    blocked_reasons.append("distributed_evidence_stale")
                if distributed_payload.get("secret_values") != "SUPPRESSED":
                    blocked_reasons.append("distributed_secret_suppression_invalid")
            cycle_record["distributed_verification"]={
                "returncode": 0 if not blocked_reasons else 2,
                "payload": distributed_payload,
                "source": "fresh_downloaded_a2_aggregate",
                "blocked_reasons": blocked_reasons,
            }
            if journal:
                journal.checkpoint(
                    phase="distributed_verification_complete",
                    cycle=cycle,
                    step={
                        "cycle":cycle,
                        "phase":"distributed",
                        "returncode":0 if not blocked_reasons else 2,
                        "status":"PASS" if not blocked_reasons else "BLOCKED",
                    },
                )
            if blocked_reasons:
                return {"status":"BLOCKED","phase":"distributed_verification",
                        "reason":blocked_reasons[0],"steps":steps,
                        "elapsed_seconds":round(time.time()-started,3)}
            if operation == "autonomous_gold_mission":
                queue_env=os.environ.copy()
                queue_env["ASTRA_TARGET_SHA"]=target_sha
                queue_env["ASTRA_QUEUE_STATE_DIR"]=queue_env.get("ASTRA_QUEUE_STATE_DIR",str(ROOT/".astra-state"/"queue"))
                runtime_path=str(ROOT / "runtime")
                queue_env["PYTHONPATH"]=runtime_path + (os.pathsep + queue_env["PYTHONPATH"] if queue_env.get("PYTHONPATH") else "")
                if journal:
                    journal.checkpoint(phase="autonomous_queue", cycle=cycle)
                queue=subprocess.run([sys.executable,"-m","mediahub_runtime.autonomous_queue"],
                                     cwd=ROOT,text=True,capture_output=True,
                                     timeout=int(os.environ.get("ASTRA_QUEUE_RUN_TIMEOUT","3600")),
                                     check=False,env=queue_env)
                queue_payload={}
                try:
                    queue_payload=json.loads(queue.stdout.strip().splitlines()[-1])
                except Exception:
                    queue_payload={"status":"BLOCKED","reason":"queue_output_not_json"}
                cycle_record["autonomous_queue"]={"returncode":queue.returncode,"payload":queue_payload,
                                                  "stdout":queue.stdout[-16000:],"stderr":queue.stderr[-10000:]}
                if journal:
                    journal.checkpoint(phase="autonomous_queue_complete", cycle=cycle, step={"cycle":cycle,"phase":"queue","returncode":queue.returncode,"status":queue_payload.get("status")})
                if queue.returncode != 0 or queue_payload.get("status") != "PASS":
                    result={"status":"BLOCKED","phase":"autonomous_queue","steps":steps,"elapsed_seconds":round(time.time()-started,3)}
                    if journal:
                        journal.finish(status="BLOCKED", result=result)
                    return result
                result={"status":"PASS","phase":"autonomous_queue","steps":steps,
                        "queue":queue_payload,"elapsed_seconds":round(time.time()-started,3)}
                if journal:
                    journal.finish(status="PASS", result=result)
                return result
            result={"status":"PASS","phase":"gold_qualification","steps":steps,
                    "elapsed_seconds":round(time.time()-started,3)}
            if journal:
                journal.finish(status="PASS", result=result)
            return result

        result={"status":"BLOCKED","phase":"autonomous_retry_window_exhausted",
                "steps":steps,"elapsed_seconds":round(time.time()-started,3)}
        if journal:
            journal.finish(status="BLOCKED", result=result)
        return result

    if operation == "reconcile_controller_processes":
        ps=subprocess.run(["/usr/bin/ps","-eo","pid=,args="],text=True,capture_output=True,timeout=10,check=False)
        current=os.getpid()
        matches=[]
        terminated=[]
        for line in ps.stdout.splitlines():
            parts=line.strip().split(None,1)
            if len(parts)!=2: continue
            try: pid=int(parts[0])
            except ValueError: continue
            args=parts[1]
            if pid!=current and "astra_github_agent.py" in args and f"ASTRA_NODE_ID={NODE_ID}" in args:
                matches.append({"pid":pid,"args":args[-1000:]})
                p=subprocess.run(["/bin/kill","-TERM",str(pid)],text=True,capture_output=True,timeout=5,check=False)
                terminated.append({"pid":pid,"returncode":p.returncode})
        time.sleep(2)
        ps2=subprocess.run(["/usr/bin/ps","-eo","pid=,args="],text=True,capture_output=True,timeout=10,check=False)
        remaining=[]
        for line in ps2.stdout.splitlines():
            parts=line.strip().split(None,1)
            if len(parts)==2 and "astra_github_agent.py" in parts[1] and f"ASTRA_NODE_ID={NODE_ID}" in parts[1]:
                try:
                    if int(parts[0])!=current: remaining.append(parts[0])
                except ValueError: pass
        return {"status":"PASS" if not remaining else "BLOCKED","current_pid":current,
                "matched_duplicates":matches,"terminated":terminated,"remaining_duplicates":remaining,
                "node_id":NODE_ID,"credentials":"SUPPRESSED"}

    if operation == "dual_local_executor_23wave":
        import shutil, statistics
        g4_local_bins = [str(Path.home() / ".local" / "bin"), str(Path.home() / ".local" / "npm" / "bin")]
        current_path = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p]
        os.environ["PATH"] = os.pathsep.join(dict.fromkeys(g4_local_bins + current_path))
        expected_g4_sha = str(cmd.get("target_sha") or "").strip().lower()
        actual_g4_sha = run(["git","rev-parse","HEAD"],10).stdout.strip().lower()
        if expected_g4_sha and actual_g4_sha != expected_g4_sha:
            raise RuntimeError("g4_target_sha_not_current_head")
        omni_model = os.environ.get("ASTRA_OMNIROUTE_MODEL", "").strip()
        if not omni_model:
            raise RuntimeError("omniroute_model_binding_missing")
        if omni_model.startswith("llama-cpp//"):
            omni_model = "llama-cpp/" + omni_model[len("llama-cpp//"):]
        if not omni_model.startswith("llama-cpp/"):
            raise RuntimeError("omniroute_model_binding_invalid")
        marker_map = {
            "fcc_codex": "MEDIAHUB_FCC_CODEX_OK",
            "fcc_claude": "MEDIAHUB_FCC_CLAUDE_OK",
            "omni_claude": "MEDIAHUB_OMNI_CLAUDE_OK",
            "omni_codex": "MEDIAHUB_OMNI_CODEX_OK",
            "claude_code_direct": "MEDIAHUB_CLAUDE_CODE_DIRECT_OK",
        }
        rounds = []
        evidence_rounds = []
        base_env = os.environ.copy()
        fcc_env = base_env.copy()
        fcc_file = os.environ.get("ASTRA_FCC_ENV_FILE", "").strip()
        if fcc_file and Path(fcc_file).is_file():
            for raw in Path(fcc_file).read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                fcc_env[key.strip()] = value.strip()
        transport_collision_keys = {"HOST", "PORT", "MODEL", "OLLAMA_BASE_URL", "PROXY_AUTH_ENABLED", "ANTHROPIC_AUTH_TOKEN", "FCC_ENV_FILE"}
        isolated_env = base_env.copy()
        for key in transport_collision_keys:
            isolated_env.pop(key, None)
        isolated_env["OMNIROUTE_CLI_SKIP_REPO_ENV"] = "1"
        fcc_env["ENABLE_MODEL_THINKING"] = "false"
        fcc_env["ENABLE_OPUS_THINKING"] = "false"
        fcc_env["ENABLE_SONNET_THINKING"] = "false"
        fcc_env["ENABLE_HAIKU_THINKING"] = "false"
        fcc_env["CLAUDE_CODE_DISABLE_THINKING"] = "1"
        fcc_env["MAX_THINKING_TOKENS"] = "0"
        fcc_host = fcc_env.get("HOST", "127.0.0.1")
        fcc_port = fcc_env.get("PORT", "8093")
        direct_claude_env = isolated_env.copy()
        direct_claude_env["ENABLE_MODEL_THINKING"] = "false"
        direct_claude_env["ENABLE_OPUS_THINKING"] = "false"
        direct_claude_env["ENABLE_SONNET_THINKING"] = "false"
        direct_claude_env["ENABLE_HAIKU_THINKING"] = "false"
        # Local Qwen2.5-Coder 1.5B rejects Anthropic thinking requests.
        # Force Claude Code compatibility mode for this third-party gateway.
        direct_claude_env["CLAUDE_CODE_DISABLE_THINKING"] = "1"
        direct_claude_env["MAX_THINKING_TOKENS"] = "0"
        direct_claude_env["ANTHROPIC_BASE_URL"] = f"http://{fcc_host}:{fcc_port}"
        if fcc_env.get("ANTHROPIC_AUTH_TOKEN"):
            direct_claude_env["ANTHROPIC_AUTH_TOKEN"] = fcc_env["ANTHROPIC_AUTH_TOKEN"]
        probe_home = tempfile.TemporaryDirectory(prefix="astra-g4-codex-home-")
        probe_config = Path(probe_home.name) / "config.toml"
        probe_config.write_text(
            'approval_policy = "never"\n'
            'web_search = "disabled"\n'
            '[features]\n'
            'multi_agent = false\n'
            'multi_agent_v2 = false\n'
            'apps = false\n'
            'tool_search = false\n'
            'plugins = false\n',
            encoding="utf-8",
        )
        codex_env = isolated_env.copy()
        codex_env["CODEX_HOME"] = probe_home.name
        codex_env["OMNIROUTE_API_KEY"] = "local"
        omni_config = (
            'model = "' + omni_model + '"\n'
            'model_provider = "omniroute"\n'
            '[model_providers.omniroute]\n'
            'name = "OmniRoute"\n'
            'base_url = "http://127.0.0.1:20128/v1"\n'
            'env_key = "OMNIROUTE_API_KEY"\n'
            'wire_api = "responses"\n'
            'requires_openai_auth = false\n'
        )
        probe_config.write_text(
            probe_config.read_text(encoding="utf-8") + omni_config,
            encoding="utf-8",
        )
        def probe(argv, marker, timeout=35, env=None):
            started=time.monotonic()
            try:
                p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,stdin=subprocess.DEVNULL,env=(env or isolated_env),
                                 timeout=timeout,check=False)
                out=(p.stdout or "")[-12000:]
                err=(p.stderr or "")[-12000:]
                return {"status":"PASS" if p.returncode==0 and marker in out else "BLOCKED",
                        "returncode":p.returncode,"duration_seconds":round(time.monotonic()-started,3),
                        "marker_present":marker in out,"stdout_tail":out,"stderr_tail":err}
            except subprocess.TimeoutExpired as exc:
                return {"status":"TIMEOUT","returncode":124,"duration_seconds":round(time.monotonic()-started,3),
                        "marker_present":False,"stdout_tail":str(exc.stdout or "")[-4000:],
                        "stderr_tail":str(exc.stderr or "")[-4000:]}
            except Exception as exc:
                return {"status":"BLOCKED","returncode":1,"duration_seconds":round(time.monotonic()-started,3),
                        "marker_present":False,"error":type(exc).__name__}
        for cycle in range(1,24):
            rec={"cycle":cycle,"head":run(["git","rev-parse","HEAD"],10).stdout.strip(),"executors":{}}
            if cycle == 1:
                rec["inventory"]={}
                for name, candidates in {
                    "fcc-codex":["fcc-codex"],"fcc-claude":["fcc-claude"],
                    "omniroute":["omniroute"],"codex":["codex"],"claude":["claude"],
                    "ecc":["ecc","ecc-cli"],
                }.items():
                    hit=next((shutil.which(x) for x in candidates if shutil.which(x)),None)
                    rec["inventory"][name]=hit or "NOT_FOUND"
                rec["fcc_server_probe"]=probe(["/usr/bin/curl","-fsS","--max-time","5","http://127.0.0.1:8092/v1/models"],"data")
                rec["omniroute_probe"]=probe(["/usr/bin/curl","-fsS","--max-time","5","http://127.0.0.1:20128/v1/models"],"data")
            rec["executors"]["fcc_codex"] = probe(
                ["fcc-codex","exec","--skip-git-repo-check","--sandbox","read-only",
                 "--config","model_reasoning_effort=none",
                 f"Return exactly {marker_map['fcc_codex']}. Do not modify files or use tools."],
                marker_map["fcc_codex"],30,env=fcc_env) if shutil.which("fcc-codex") else {"status":"BLOCKED","reason":"binary_missing"}
            rec["executors"]["fcc_claude"] = probe(
                ["fcc-claude","-p",f"Return exactly {marker_map['fcc_claude']}. Do not modify files or use tools.",
                 "--output-format","text"],marker_map["fcc_claude"],30,env=fcc_env) if shutil.which("fcc-claude") else {"status":"BLOCKED","reason":"binary_missing"}
            if shutil.which("omniroute"):
                rec["executors"]["omni_claude"]=probe(
                    ["omniroute","run","claude","--model",omni_model,"--","-p",
                     f"Return exactly {marker_map['omni_claude']}. Do not modify files or use tools.","--output-format","text"],
                    marker_map["omni_claude"],35,env=isolated_env)
                rec["executors"]["omni_codex"]=probe(
                    ["codex","exec","--skip-git-repo-check","--sandbox","read-only",
                     "--config","model_reasoning_effort=none",
                     f"Return exactly {marker_map['omni_codex']}. Do not modify files or use tools."],
                    marker_map["omni_codex"],35,env=codex_env)
            else:
                rec["executors"]["omni_claude"]={"status":"BLOCKED","reason":"binary_missing"}
                rec["executors"]["omni_codex"]={"status":"BLOCKED","reason":"binary_missing"}
            if shutil.which("claude"):
                rec["executors"]["claude_code_direct"] = probe(
                    ["claude","--print","--output-format","text",
                     f"Return exactly {marker_map['claude_code_direct']}. Do not modify files or use tools."],
                    marker_map["claude_code_direct"],35,env=direct_claude_env)
            else:
                rec["executors"]["claude_code_direct"]={"status":"BLOCKED","reason":"binary_missing"}
            completed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            path_meta = {
                "fcc_codex": ("fcc-codex", "FCC"),
                "fcc_claude": ("fcc-claude", "FCC"),
                "omni_claude": ("omniroute:claude", "OmniRoute"),
                "omni_codex": ("omniroute:codex", "OmniRoute"),
                "claude_code_direct": ("claude", "native-claude-cli-over-fcc-http"),
            }
            for path_key, result in rec["executors"].items():
                executor_identity, transport_identity = path_meta[path_key]
                raw_id=f"{rec['head']}|{path_key}|{cycle}".encode()
                command_id="g4-"+hashlib.sha256(raw_id).hexdigest()[:24]
                started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()-float(result.get("duration_seconds") or 0)))
                item={
                    "command_id": command_id, "path": path_key.upper(),
                    "round": cycle, "source_sha": rec["head"],
                    "executor_identity": executor_identity,
                    "provider_or_transport_identity": transport_identity,
                    "workspace": str(ROOT.resolve()),
                    "started_at": started_at, "completed_at": completed_at,
                    "exit_status": int(result.get("returncode", 1)),
                    "timeout": result.get("status") == "TIMEOUT",
                    "marker": marker_map[path_key],
                    "marker_present": result.get("marker_present") is True,
                    "result_schema": "mediahub.astra-gold.g4-round.v1",
                    "verification_status": result.get("status") if result.get("status") == "PASS" else "BLOCKED",
                }
                item["evidence_digest"]="sha256:"+hashlib.sha256(json.dumps(item,sort_keys=True,separators=(",",":")).encode()).hexdigest()
                evidence_rounds.append(item)
            rounds.append(rec)
        summary={} 
        for key in marker_map:
            vals=[r["executors"].get(key,{}) for r in rounds]
            passed=[v for v in vals if v.get("status")=="PASS"]
            durations=[v["duration_seconds"] for v in passed if isinstance(v.get("duration_seconds"),(int,float))]
            summary[key]={"pass_count":len(passed),"rounds":23,"pass_rate":round(len(passed)/23,3),
                           "median_latency_seconds":round(statistics.median(durations),3) if durations else None,
                           "statuses":{s:sum(1 for v in vals if v.get("status")==s) for s in ("PASS","BLOCKED","TIMEOUT")}}
        ranked=sorted(summary.items(),key=lambda kv:(kv[1]["pass_count"],-(kv[1]["median_latency_seconds"] or 999999)),reverse=True)
        selected=[k for k,v in ranked if v["pass_count"]==23]
        result = {"status":"PASS" if set(selected) == set(marker_map) else "BLOCKED",
                "phase":"23_round_local_executor_qualification","node_id":NODE_ID,
                "rounds":rounds,"evidence_rounds":evidence_rounds,"summary":summary,"selection_order":ranked,"selected_full_pass":selected,
                "ecc_policy":"inventory-only; no authority or provider credentials","credentials":"SUPPRESSED"}
        probe_home.cleanup()
        return result

    if operation == "codex_config_isolation":
        argv=["/usr/local/bin/codex","exec","--ignore-user-config","--skip-git-repo-check","print('MEDIAHUB_CODEX_CONFIG_ISOLATION_OK')"]
        try:
            p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=45,check=False)
            return {"status":"PASS" if p.returncode==0 and "MEDIAHUB_CODEX_CONFIG_ISOLATION_OK" in (p.stdout or "") else "BLOCKED",
                    "argv":argv,"returncode":p.returncode,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:],
                    "secret_values":"SUPPRESSED"}
        except Exception as exc:
            return {"status":"BLOCKED","error":repr(exc),"secret_values":"SUPPRESSED"}
    if operation == "codex_cleanup_stale_probes":
        ps=subprocess.run(["/usr/bin/ps","-eo","pid=,ppid=,cmd="],text=True,capture_output=True,timeout=10,check=False)
        targets=[]
        for line in ps.stdout.splitlines():
            parts=line.strip().split(None,2)
            if len(parts)==3 and "codex exec" in parts[2] and "MEDIAHUB_EXECUTION_BACKEND_QUALIFICATION" in parts[2]:
                try: targets.append(int(parts[0]))
                except ValueError: pass
        terminated=[]
        for pid in targets:
            p=subprocess.run(["/bin/kill","-TERM",str(pid)],text=True,capture_output=True,timeout=5,check=False)
            terminated.append({"pid":pid,"returncode":p.returncode})
        time.sleep(2)
        ps2=subprocess.run(["/usr/bin/ps","-eo","pid=,ppid=,cmd="],text=True,capture_output=True,timeout=10,check=False)
        remaining=[]
        for line in ps2.stdout.splitlines():
            parts=line.strip().split(None,2)
            if len(parts)==3 and "codex exec" in parts[2] and "MEDIAHUB_EXECUTION_BACKEND_QUALIFICATION" in parts[2]:
                remaining.append(parts[0])
        return {"status":"PASS" if not remaining else "BLOCKED","matched_pids":targets,"terminated":terminated,"remaining_pids":remaining,"secret_values":"SUPPRESSED"}
    if operation == "codex_process_diagnostic":
        argv=["/usr/bin/timeout","12","/usr/local/bin/codex","exec","--ignore-user-config","--skip-git-repo-check","print('MEDIAHUB_CODEX_PROCESS_DIAGNOSTIC_OK')"]
        try:
            p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=20,check=False)
            ps=subprocess.run(["/usr/bin/ps","-eo","pid,ppid,stat,etime,cmd"],text=True,capture_output=True,timeout=10,check=False)
            lines=[x for x in ps.stdout.splitlines() if "codex" in x.lower()][:20]
            return {"status":"PASS" if p.returncode==0 and "MEDIAHUB_CODEX_PROCESS_DIAGNOSTIC_OK" in (p.stdout or "") else "BLOCKED",
                    "argv":argv,"returncode":p.returncode,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:],
                    "codex_processes":lines,"secret_values":"SUPPRESSED"}
        except Exception as exc:
            return {"status":"BLOCKED","error":repr(exc),"secret_values":"SUPPRESSED"}
    if operation == "codex_provider_diagnostic":
        argv=["/usr/local/bin/codex","exec","--ignore-user-config","--skip-git-repo-check","print('MEDIAHUB_CODEX_PROVIDER_DIAGNOSTIC_OK')"]
        env={key:os.environ[key] for key in ("PATH","HOME","USER","LOGNAME","SHELL","TERM","XDG_CONFIG_HOME","CODEX_HOME","OPENAI_BASE_URL","OPENAI_ORG_ID") if os.environ.get(key)}
        try:
            p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,stdin=subprocess.DEVNULL,timeout=20,check=False,env=env)
            return {"status":"PASS" if p.returncode==0 and "MEDIAHUB_CODEX_PROVIDER_DIAGNOSTIC_OK" in (p.stdout or "") else "BLOCKED","argv":argv,"returncode":p.returncode,"stdout":p.stdout[-8000:],"stderr":p.stderr[-8000:],"credential_presence":{"OPENAI_API_KEY":bool(os.environ.get("OPENAI_API_KEY"))},"secret_values":"SUPPRESSED"}
        except Exception as exc:
            return {"status":"BLOCKED","error":repr(exc),"secret_values":"SUPPRESSED"}
    if operation == "codex_gateway_diagnostic":
        gateways=[("unorouter","UNOROUTER_API_KEY","https://api.unorouter.com/v1","gpt-5.4"),("zerouter","ZEROUTER_API_KEY","https://api.zerouter.ai/v1","gpt-5.4")]
        results=[]
        for name,key_name,base_url,model in gateways:
            credential_present=bool(os.environ.get(key_name))
            item={"gateway":name,"credential_presence":{key_name:credential_present},"status":"BLOCKED","secret_values":"SUPPRESSED"}
            if not credential_present:
                item["reason"]="credential_missing"; results.append(item); continue
            with tempfile.TemporaryDirectory(prefix="astra-codex-gateway-") as home:
                config=Path(home)/"config.toml"
                config.write_text(f'model = "{model}"\nmodel_provider = "{name}"\n[model_providers.{name}]\nname = "{name}"\nbase_url = "{base_url}"\nwire_api = "responses"\nenv_key = "{key_name}"\n',encoding="utf-8")
                env={key:os.environ[key] for key in ("PATH","HOME","USER","LOGNAME","SHELL","TERM") if os.environ.get(key)}
                env.update({"CODEX_HOME":home,key_name:os.environ[key_name]})
                argv=["/usr/local/bin/codex","exec","--skip-git-repo-check","--model",model,"print('MEDIAHUB_CODEX_GATEWAY_DIAGNOSTIC_OK')"]
                started=time.monotonic()
                try:
                    p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,stdin=subprocess.DEVNULL,timeout=30,check=False,env=env)
                    combined=(p.stdout or "")+(p.stderr or "")
                    item.update({"returncode":p.returncode,"duration_seconds":round(time.monotonic()-started,3),"output_bytes":len(combined.encode("utf-8","replace")),"marker_present":"MEDIAHUB_CODEX_GATEWAY_DIAGNOSTIC_OK" in (p.stdout or ""),"status":"PASS" if p.returncode==0 and "MEDIAHUB_CODEX_GATEWAY_DIAGNOSTIC_OK" in (p.stdout or "") else "BLOCKED"})
                    if item["status"]!="PASS":
                        text=combined.lower()
                        if "403 forbidden" in text and ("country, region" in text or "territory not supported" in text): item["reason"]="provider_region_restricted"
                        elif "401" in text or "unauthorized" in text or "authentication" in text: item["reason"]="authentication_or_authorization"
                        elif "402" in text or "billing" in text or "quota" in text: item["reason"]="billing_or_quota"
                        elif "timeout" in text or "timed out" in text: item["reason"]="network_or_timeout"
                        else: item["reason"]="nonzero_exit_unknown"
                except Exception as exc: item["reason"]=type(exc).__name__
                results.append(item)
        return {"status":"PASS" if any(x["status"]=="PASS" for x in results) else "BLOCKED","phase":"codex_gateway_diagnostic","gateways":results,"secret_values":"SUPPRESSED"}

    if operation == "codex_diagnostic":
        diagnostics=[]
        probes=[["/usr/local/bin/codex","--version"],["/usr/local/bin/codex","exec","--help"]]
        for argv in probes:
            try:
                p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=20,check=False)
                diagnostics.append({"argv":argv,"returncode":p.returncode,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]})
            except Exception as exc: diagnostics.append({"argv":argv,"error":repr(exc)})
        config=Path(os.environ.get("CODEX_HOME",str(Path.home()/".codex")))/"config.toml"
        diagnostics.append({"config_path":str(config),"config_exists":config.exists(),"config_sha256":hashlib.sha256(config.read_bytes()).hexdigest() if config.exists() else ""})
        return {"status":"PASS","node_id":NODE_ID,"diagnostics":diagnostics,"secret_values":"SUPPRESSED"}
    if operation == "local_ai_capability_qualification":
        script=ROOT/"ops"/"qualification"/"qualify_local_ai_capabilities.py"
        if not script.exists(): raise FileNotFoundError(f"local AI capability qualifier not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=300,check=False)
        payload={"returncode":result.returncode,"stdout":result.stdout[-40000:],"stderr":result.stderr[-12000:],"status":"PASS" if result.returncode==0 else "BLOCKED"}
        if result.stdout.strip():
            try: payload["qualification"]=json.loads(result.stdout)
            except json.JSONDecodeError: pass
        return payload
    if operation == "local_component_qualification":
        script=ROOT/"ops"/"qualification"/"qualify_local_components.py"
        if not script.exists(): raise FileNotFoundError(f"local component qualifier not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=300,check=False)
        payload={"returncode":result.returncode,"stdout":result.stdout[-40000:],"stderr":result.stderr[-12000:],"status":"PASS" if result.returncode==0 else "BLOCKED"}
        if result.stdout.strip():
            try: payload["qualification"]=json.loads(result.stdout)
            except json.JSONDecodeError: pass
        return payload
    if operation == "local_component_inventory":
        script=ROOT/"ops"/"qualification"/"inventory_local_components.py"
        if not script.exists(): raise FileNotFoundError(f"local component inventory probe not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=120,check=False)
        payload={"returncode":result.returncode,"stdout":result.stdout[-40000:],"stderr":result.stderr[-12000:]}
        if result.stdout.strip():
            try: payload["inventory"]=json.loads(result.stdout)
            except json.JSONDecodeError: pass
        payload["status"]="PASS" if result.returncode==0 else "BLOCKED"
        return payload
    if operation == "provider_model_qualification":
        script=ROOT/"ops"/"qualification"/"qualify_execution_backends.py"
        if not script.exists(): raise FileNotFoundError(f"provider/model qualification probe not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=300,check=False)
        payload={"returncode":result.returncode,"stdout":result.stdout[-30000:],"stderr":result.stderr[-12000:]}
        if result.stdout.strip():
            try:
                payload["qualification"]=json.loads(result.stdout)
            except json.JSONDecodeError:
                pass
        payload["status"]="PASS" if result.returncode==0 else "BLOCKED"
        return payload
    if operation == "execution_backend_qualification":
        script=ROOT/"ops"/"qualification"/"qualify_execution_backends.py"
        if not script.exists(): raise FileNotFoundError(f"execution backend qualification probe not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=120,check=False)
        return {"returncode":result.returncode,"stdout":result.stdout[-20000:],"stderr":result.stderr[-10000:],"status":"PASS" if result.returncode==0 else "BLOCKED"}
    if operation == "timezone_sync":
        target_timezone="Europe/Moscow"
        commands=[["timedatectl","set-timezone",target_timezone],["sudo","-n","timedatectl","set-timezone",target_timezone]]
        applied=False; attempts=[]
        for argv in commands:
            result=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=30,check=False)
            attempts.append({"command":" ".join(argv[:2])+(" "+argv[2] if len(argv)>2 else ""),"returncode":result.returncode,"stderr":result.stderr[-2000:]})
            if result.returncode==0: applied=True; break
        verify=subprocess.run(["timedatectl","show","-p","Timezone","-p","NTPSynchronized","-p","NTP"],cwd=ROOT,text=True,capture_output=True,timeout=30,check=False)
        values={}
        for line in verify.stdout.splitlines():
            if "=" in line:
                key,value=line.split("=",1); values[key]=value
        return {"status":"PASS" if applied and values.get("Timezone")==target_timezone else "BLOCKED","target_timezone":target_timezone,"applied":applied,"verified_timezone":values.get("Timezone"),"ntp_synchronized":values.get("NTPSynchronized"),"ntp_enabled":values.get("NTP"),"attempts":attempts}
    if operation == "pre_soak_evidence":
        script=ROOT/"ops"/"qualification"/"capture_pre_soak_evidence.py"
        if not script.exists(): raise FileNotFoundError(f"pre-soak evidence producer not found: {script}")
        result=subprocess.run([sys.executable,str(script),"--target-sha",str(cmd.get("target_sha","")),"--provider-evidence",os.environ.get("ASTRA_PROVIDER_EVIDENCE_PATH","")],cwd=ROOT,text=True,capture_output=True,timeout=900,check=False)
        return {"returncode":result.returncode,"stdout":result.stdout[-20000:],"stderr":result.stderr[-10000:],"status":"PASS" if result.returncode==0 else "BLOCKED"}
    if operation == "qualification":
        script=ROOT/"ops"/"qualification"/"astra_gold_executor.py"
        if not script.exists(): raise FileNotFoundError(f"qualification executor not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=int(os.environ.get("ASTRA_QUALIFICATION_TIMEOUT","87000")),check=False)
        payload={"returncode":result.returncode,"stdout":result.stdout[-20000:],"stderr":result.stderr[-10000:]}
        if result.returncode!=0: payload["status"]="BLOCKED"
        return payload
    if operation not in OPERATIONS: raise ValueError("unsupported operation")
    if operation in UNADMITTED_GENERIC_GATEWAY_OPERATIONS:
        # Never convert these commands into an implicit provider/API call from a
        # server-side worker. Use only the approved GitHub-hosted controller route.
        raise RuntimeError("gateway_route_not_admitted")
    # Fail closed if a future operation is added without a concrete handler.
    raise RuntimeError("operation_handler_not_implemented")

def main():
    STATE.mkdir(parents=True,exist_ok=True)
    last_id=published_command_id()
    while True:
        try:
            if not (os.environ.get("ASTRA_ONESHOT") == "1" and os.environ.get("ASTRA_WORKFLOW_ONLY") == "1"):
                sync()
            maybe_reexec_updated_agent(); cmd=read_command()
            if cmd and cmd.get("command_id")!=last_id:
                started=time.time()
                claim_store=None
                claim=None
                try:
                    claim_store, claim = _claim_for(cmd)
                    claim_store.acquire(claim)
                    value,rc=execute(cmd),0
                except Exception as exc:
                    value,rc={'error':repr(exc)},1
                finally:
                    if claim_store is not None and claim is not None:
                        try:
                            result_status = value.get("status") if isinstance(value, dict) else None
                            claim_status = "VERIFIED" if rc == 0 and result_status == "PASS" else "REJECTED"
                            claim_store.release(claim.task_id, claim_status)
                            claim = next((c for c in claim_store.list_claims() if c.task_id == claim.task_id), claim)
                        except Exception as release_exc:
                            value = {**(value if isinstance(value,dict) else {'result':value}), 'claim_release_error':repr(release_exc)}
                            rc=1
                publish({'schema':1,'node_id':NODE_ID,'agent_id':AGENT_ID,'worker_id':WORKER_ID,
                         'command_id':cmd.get('command_id'),'target_sha':cmd.get('target_sha'),
                         'execution_head':run(['git','rev-parse','HEAD'],10).stdout.strip(),'returncode':rc,
                         'claim':asdict(claim) if claim is not None else None,
                         'chain':['task','claim','worker','verification','commit','evidence'],
                         'duration_seconds':round(time.time()-started,3),'result':value,'completed_at':int(time.time())})
                _mark_command_executed(cmd.get("command_id",""))
                mark_published(cmd.get("command_id",""))
                last_id=str(cmd.get("command_id"))
                if os.environ.get("ASTRA_ONESHOT","0")=="1": return
        except Exception as exc:
            (STATE/"last_error.json").write_text(json.dumps({"error":repr(exc),"time":int(time.time())}))
            if os.environ.get("ASTRA_ONESHOT","0")=="1":
                raise
        if os.environ.get("ASTRA_ONESHOT","0")=="1": return
        time.sleep(INTERVAL)

if __name__=="__main__": main()