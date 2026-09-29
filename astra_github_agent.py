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
OPERATIONS={"health","research","architecture","review","documents","coding","coding_v2","qualification","execution_backend_qualification","pre_soak_evidence","timezone_sync","autonomous_qualification_queue","autonomous_gold_mission","codex_diagnostic","codex_config_isolation","codex_process_diagnostic","codex_cleanup_stale_probes","codex_provider_diagnostic","codex_gateway_diagnostic"}
RUNNING_AGENT_SHA=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

def run(argv,timeout=120):
    return subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout,check=False)

def sync():
    ROOT.parent.mkdir(parents=True,exist_ok=True)
    if not (ROOT/".git").exists():
        subprocess.run(["git","clone","--depth","1",REMOTE,str(ROOT)],check=True,timeout=120)
    else:
        subprocess.run(["git","-C",str(ROOT),"fetch","--depth","50","origin","main"],check=True,timeout=120)
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
    if operation in {"autonomous_qualification_queue", "autonomous_gold_mission"}:
        # Stateful autonomous qualification coordinator. It owns progression,
        # retries transient blockers with bounded backoff, and never converts a
        # missing/failed evidence gate into PASS.
        backend_script=ROOT/"ops"/"qualification"/"qualify_execution_backends.py"
        evidence_script=ROOT/"ops"/"qualification"/"capture_pre_soak_evidence.py"
        verifier_script=ROOT/"ops"/"qualification"/"verify_pre_soak_bundle.py"
        gold=ROOT/"ops"/"qualification"/"astra_gold_executor.py"
        started=time.time()
        max_cycles=max(1,int(os.environ.get("ASTRA_AUTONOMOUS_MAX_CYCLES","12")))
        retry_seconds=max(30,int(os.environ.get("ASTRA_AUTONOMOUS_RETRY_SECONDS","300")))
        steps=[]
        target_sha=cmd.get("target_sha","")
        if target_sha:
            ancestry=run(["git","merge-base","--is-ancestor",target_sha,"HEAD"],30)
            if ancestry.returncode != 0:
                return {"status":"BLOCKED","phase":"target_reconciliation",
                        "reason":"target_sha_not_ancestor_of_current_main","target_sha":target_sha,
                        "current_head":run(["git","rev-parse","HEAD"],10).stdout.strip()}
        # The legacy queue remains a single-pass compatibility operation.
        cycles=1 if operation=="autonomous_qualification_queue" else max_cycles
        for cycle in range(1,cycles+1):
            if operation=="autonomous_gold_mission" and cycle>1:
                sync()
                ancestry=run(["git","merge-base","--is-ancestor",target_sha,"HEAD"],30) if target_sha else None
                if ancestry is not None and ancestry.returncode != 0:
                    return {"status":"BLOCKED","phase":"target_reconciliation",
                            "reason":"target_sha_not_ancestor_of_current_main","target_sha":target_sha,
                            "current_head":run(["git","rev-parse","HEAD"],10).stdout.strip(),
                            "cycles":steps}
            cycle_record={"cycle":cycle,"head":run(["git","rev-parse","HEAD"],10).stdout.strip()}
            backend=subprocess.run([sys.executable,str(backend_script)],cwd=ROOT,text=True,
                                   capture_output=True,timeout=120,check=False)
            cycle_record["backend"]={"returncode":backend.returncode,
                                     "stdout":backend.stdout[-12000:],"stderr":backend.stderr[-8000:]}
            steps.append(cycle_record)
            if backend.returncode != 0:
                if operation=="autonomous_gold_mission" and cycle<cycles:
                    time.sleep(retry_seconds)
                    continue
                return {"status":"BLOCKED","phase":"execution_backend_qualification",
                        "steps":steps,"elapsed_seconds":round(time.time()-started,3)}
            evidence=subprocess.run([sys.executable,str(evidence_script)],cwd=ROOT,text=True,
                                    capture_output=True,timeout=900,check=False)
            cycle_record["pre_soak"]={"returncode":evidence.returncode,
                                      "stdout":evidence.stdout[-12000:],"stderr":evidence.stderr[-8000:]}
            if evidence.returncode != 0:
                if operation=="autonomous_gold_mission" and cycle<cycles:
                    time.sleep(retry_seconds)
                    continue
                return {"status":"BLOCKED","phase":"pre_soak_evidence",
                        "steps":steps,"elapsed_seconds":round(time.time()-started,3)}
            verifier=subprocess.run([sys.executable,str(verifier_script),"evidence"],
                                    cwd=ROOT,text=True,capture_output=True,timeout=300,check=False)
            cycle_record["strict_verifier"]={"returncode":verifier.returncode,
                                              "stdout":verifier.stdout[-12000:],
                                              "stderr":verifier.stderr[-8000:]}
            if verifier.returncode != 0:
                if operation=="autonomous_gold_mission" and cycle<cycles:
                    time.sleep(retry_seconds)
                    continue
                return {"status":"BLOCKED","phase":"strict_pre_soak_verification",
                        "steps":steps,"elapsed_seconds":round(time.time()-started,3)}
            # Distributed verification has no live producer in the current
            # repository. Refuse to invent evidence; expose this as the next
            # explicit admission gate instead of silently skipping it.
            distributed_candidates=list((ROOT/"ops"/"qualification").glob("*distributed*")) if (ROOT/"ops"/"qualification").exists() else []
            if not distributed_candidates:
                return {"status":"BLOCKED","phase":"distributed_verification",
                        "reason":"no_dedicated_distributed_verification_producer",
                        "steps":steps,"elapsed_seconds":round(time.time()-started,3)}
            for candidate in distributed_candidates:
                if candidate.suffix==".py":
                    distributed=subprocess.run([sys.executable,str(candidate)],cwd=ROOT,text=True,
                                               capture_output=True,timeout=1800,check=False)
                    cycle_record["distributed_verification"]={"script":str(candidate.relative_to(ROOT)),
                                                              "returncode":distributed.returncode,
                                                              "stdout":distributed.stdout[-12000:],
                                                              "stderr":distributed.stderr[-8000:]}
                    if distributed.returncode != 0:
                        return {"status":"BLOCKED","phase":"distributed_verification",
                                "steps":steps,"elapsed_seconds":round(time.time()-started,3)}
            qualification=subprocess.run([sys.executable,str(gold)],cwd=ROOT,text=True,
                                         capture_output=True,
                                         timeout=int(os.environ.get("ASTRA_QUALIFICATION_TIMEOUT","87000")),
                                         check=False)
            cycle_record["gold"]={"returncode":qualification.returncode,
                                  "stdout":qualification.stdout[-12000:],
                                  "stderr":qualification.stderr[-8000:]}
            return {"status":"PASS" if qualification.returncode==0 else "BLOCKED",
                    "phase":"gold_qualification","steps":steps,
                    "elapsed_seconds":round(time.time()-started,3)}
        return {"status":"BLOCKED","phase":"autonomous_retry_window_exhausted",
                "steps":steps,"elapsed_seconds":round(time.time()-started,3)}

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
        # Probe configured OpenAI-compatible gateways without exposing credentials.
        import tempfile
        gateways = [
            ("unorouter", "UNOROUTER_API_KEY", "https://api.unorouter.com/v1", "gpt-5.4"),
            ("zerouter", "ZEROUTER_API_KEY", "https://api.zerouter.ai/v1", "gpt-5.4"),
        ]
        results = []
        for name, key_name, base_url, model in gateways:
            credential_present = bool(os.environ.get(key_name))
            item = {"gateway": name, "credential_presence": {key_name: credential_present},
                    "status": "BLOCKED", "secret_values": "SUPPRESSED"}
            if not credential_present:
                item["reason"] = "credential_missing"
                results.append(item)
                continue
            with tempfile.TemporaryDirectory(prefix="astra-codex-gateway-") as home:
                config = Path(home) / "config.toml"
                config.write_text(
                    f'model = "{model}"\\n'
                    f'model_provider = "{name}"\\n'
                    f'[model_providers.{name}]\\n'
                    f'name = "{name}"\\n'
                    f'base_url = "{base_url}"\\n'
                    f'wire_api = "responses"\\n'
                    f'env_key = "{key_name}"\\n',
                    encoding="utf-8")
                env = {key: os.environ[key] for key in ("PATH","HOME","USER","LOGNAME","SHELL","TERM") if os.environ.get(key)}
                env.update({"CODEX_HOME": home, key_name: os.environ[key_name]})
                argv=["/usr/local/bin/codex","exec","--skip-git-repo-check","--model",model,
                      "print('MEDIAHUB_CODEX_GATEWAY_DIAGNOSTIC_OK')"]
                started = time.monotonic()
                try:
                    p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,
                                     stdin=subprocess.DEVNULL,timeout=30,check=False,env=env)
                    combined=(p.stdout or "")+(p.stderr or "")
                    item.update({"returncode":p.returncode,
                                 "duration_seconds":round(time.monotonic()-started,3),
                                 "output_bytes":len(combined.encode("utf-8","replace")),
                                 "marker_present":"MEDIAHUB_CODEX_GATEWAY_DIAGNOSTIC_OK" in (p.stdout or ""),
                                 "status":"PASS" if p.returncode==0 and "MEDIAHUB_CODEX_GATEWAY_DIAGNOSTIC_OK" in (p.stdout or "") else "BLOCKED"})
                    if item["status"] != "PASS":
                        text=combined.lower()
                        if "403 forbidden" in text and ("country, region" in text or "territory not supported" in text):
                            item["reason"]="provider_region_restricted"
                        elif "401" in text or "unauthorized" in text or "authentication" in text:
                            item["reason"]="authentication_or_authorization"
                        elif "402" in text or "billing" in text or "quota" in text:
                            item["reason"]="billing_or_quota"
                        elif "timeout" in text or "timed out" in text:
                            item["reason"]="network_or_timeout"
                        else:
                            item["reason"]="nonzero_exit_unknown"
                except Exception as exc:
                    item["reason"]=type(exc).__name__
                results.append(item)
        return {"status":"PASS" if any(x["status"]=="PASS" for x in results) else "BLOCKED",
                "phase":"codex_gateway_diagnostic","gateways":results,"secret_values":"SUPPRESSED"}

    if operation == "codex_diagnostic":
        diagnostics=[]
        probes=[
            ["/usr/local/bin/codex","--version"],
            ["/usr/local/bin/codex","exec","--help"],
        ]
        for argv in probes:
            try:
                p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=20,check=False)
                diagnostics.append({"argv":argv,"returncode":p.returncode,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]})
            except Exception as exc:
                diagnostics.append({"argv":argv,"error":repr(exc)})
        config=Path(os.environ.get("CODEX_HOME",str(Path.home()/".codex")))/"config.toml"
        diagnostics.append({"config_path":str(config),"config_exists":config.exists(),"config_sha256":hashlib.sha256(config.read_bytes()).hexdigest() if config.exists() else ""})
        return {"status":"PASS","node_id":NODE_ID,"diagnostics":diagnostics,"secret_values":"SUPPRESSED"}
    if operation == "execution_backend_qualification":
        script=ROOT/"ops"/"qualification"/"qualify_execution_backends.py"
        if not script.exists():
            raise FileNotFoundError(f"execution backend qualification probe not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=120,check=False)
        payload={"returncode":result.returncode,"stdout":result.stdout[-20000:],"stderr":result.stderr[-10000:]}
        payload["status"]="PASS" if result.returncode == 0 else "BLOCKED"
        return payload
    if operation == "timezone_sync":
        target_timezone = "Europe/Moscow"
        commands = [
            ["timedatectl", "set-timezone", target_timezone],
            ["sudo", "-n", "timedatectl", "set-timezone", target_timezone],
        ]
        applied = False
        attempts = []
        for argv in commands:
            result = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, timeout=30, check=False)
            attempts.append({
                "command": " ".join(argv[:2]) + (" " + argv[2] if len(argv) > 2 else ""),
                "returncode": result.returncode,
                "stderr": result.stderr[-2000:],
            })
            if result.returncode == 0:
                applied = True
                break
        verify = subprocess.run(
            ["timedatectl", "show", "-p", "Timezone", "-p", "NTPSynchronized", "-p", "NTP"],
            cwd=ROOT, text=True, capture_output=True, timeout=30, check=False,
        )
        values = {}
        for line in verify.stdout.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                values[key] = value
        return {
            "status": "PASS" if applied and values.get("Timezone") == target_timezone else "BLOCKED",
            "target_timezone": target_timezone,
            "applied": applied,
            "verified_timezone": values.get("Timezone"),
            "ntp_synchronized": values.get("NTPSynchronized"),
            "ntp_enabled": values.get("NTP"),
            "attempts": attempts,
        }
    if operation == "pre_soak_evidence":
        script=ROOT/"ops"/"qualification"/"capture_pre_soak_evidence.py"
        if not script.exists():
            raise FileNotFoundError(f"pre-soak evidence producer not found: {script}")
        result=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True,timeout=900,check=False)
        return {"returncode":result.returncode,"stdout":result.stdout[-20000:],"stderr":result.stderr[-10000:],
                "status":"PASS" if result.returncode == 0 else "BLOCKED"}
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
