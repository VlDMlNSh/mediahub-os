from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parents[1]))
from ops.astra_failover_router import FailoverRouter, RouteCandidate, proxy_policy

def candidate(name,healthy=True,lease=True,transport="local-cli"):
    return RouteCandidate(name,frozenset({"code_patch","static_audit"}),healthy,lease,"LOCAL_TRUSTED",transport)

def test_unhealthy_executor_is_never_selected():
    assert FailoverRouter().select("t1","code_patch",[candidate("goose",False),candidate("qwen")]).executor_id=="qwen"

def test_lease_loss_blocks_executor():
    r=FailoverRouter(lambda task,executor: executor!="goose")
    assert r.select("t1","code_patch",[candidate("goose"),candidate("qwen")]).executor_id=="qwen"

def test_all_failed_is_fail_closed():
    d=FailoverRouter().select("t1","code_patch",[candidate("goose",False),candidate("qwen",False)])
    assert d.executor_id is None and d.reason=="BLOCKED_NO_QUALIFIED_EXECUTOR"

def test_failed_primary_is_replaced():
    assert FailoverRouter().failover("t1","code_patch",[candidate("goose"),candidate("qwen")],"goose").executor_id=="qwen"

def test_untrusted_pr_requires_proxy():
    assert proxy_policy(candidate("goose"),True).startswith("BLOCKED_")
    p=RouteCandidate("proxy",frozenset({"code_patch"}),True,True,"ISOLATED_PROXY","local-proxy")
    assert proxy_policy(p,True)=="ALLOW"

def test_capability_mismatch_blocks():
    c=RouteCandidate("goose",frozenset({"documentation"}),True,True,"LOCAL_TRUSTED","local-cli")
    assert FailoverRouter().select("t1","code_patch",[c]).executor_id is None

def test_inventory_ignores_unqualified_executor():
    inventory={"executors":[
        {"name":"bad","qualification":"UNQUALIFIED","status":"HEALTHY","capabilities":["code_patch"]},
        {"name":"good","qualification":"QUALIFIED","status":"HEALTHY","capabilities":["code_patch"]},
    ]}
    assert FailoverRouter().select_inventory("t1","code_patch",inventory).executor_id=="good"

def test_external_pr_blocks_direct_local_cli_from_inventory():
    inventory={"executors":[
        {"name":"aider","qualification":"QUALIFIED","status":"HEALTHY",
         "capabilities":["code_patch"],"transport":"local-cli","trust_boundary":"LOCAL_TRUSTED"}
    ]}
    decision=FailoverRouter().select_inventory("t1","code_patch",inventory,external_pr=True)
    assert decision.executor_id is None
