from runtime.mediahub_control_plane.agent_registry import AgentRegistry
from runtime.mediahub_control_plane.model import Agent, AgentStatus, Task, TaskStatus
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.scheduler import TaskScheduler
from runtime.mediahub_control_plane.service import ControlPlaneService


def registry():
    r=AgentRegistry(30,90)
    r.register(Agent('a1','n1','1',AgentStatus.IDLE,('linux','docker')))
    return r


def test_dispatch_selects_then_atomically_claims_and_runs():
    r=InMemoryControlPlaneRepository(); s=ControlPlaneService(r); ar=registry(); q=TaskScheduler(ar)
    r.create_task(Task('t','build',status=TaskStatus.READY,required_capabilities=('docker',)))
    lease=s.dispatch_once('t',q,7)
    assert lease.agent_id=='a1' and lease.generation==7
    assert r.get_task('t').status is TaskStatus.RUNNING


def test_dispatch_loses_cleanly_if_claim_was_taken_after_selection():
    r=InMemoryControlPlaneRepository(); s=ControlPlaneService(r); ar=registry(); q=TaskScheduler(ar)
    r.create_task(Task('t','build',status=TaskStatus.READY))
    original=q.select
    def select_and_race(task):
        d=original(task)
        r.claim_task(task.task_id,'other',1)
        return d
    q.select=select_and_race
    result=s.dispatch_once('t',q,2)
    assert result.agent_id is None and result.reason=='claim_lost_race'
