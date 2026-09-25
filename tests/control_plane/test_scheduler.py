from runtime.mediahub_control_plane.agent_registry import AgentRegistry
from runtime.mediahub_control_plane.model import Agent, AgentStatus, Task, TaskStatus
from runtime.mediahub_control_plane.scheduler import TaskScheduler


def test_scheduler_matches_capabilities_and_ignores_unhealthy_agents():
    r=AgentRegistry(30,90)
    r.register(Agent('a2','n2','1',AgentStatus.IDLE,('linux','git')))
    r.register(Agent('a1','n1','1',AgentStatus.IDLE,('linux','git','docker')))
    r.register(Agent('a0','n0','1',AgentStatus.DEGRADED,('linux','git','docker')))
    t=Task('t1','build',status=TaskStatus.READY,required_capabilities=('linux','docker'))
    assert TaskScheduler(r).select(t).agent_id=='a1'


def test_scheduler_is_deterministic_and_blocks_non_ready():
    r=AgentRegistry(30,90)
    r.register(Agent('a1','n1','1',AgentStatus.IDLE,('linux',)))
    t=Task('t2','build',status=TaskStatus.PENDING,required_capabilities=('linux',))
    assert TaskScheduler(r).select(t).agent_id is None
    assert TaskScheduler(r).select(Task('t3','build',status=TaskStatus.READY,required_capabilities=('gpu',))).reason=='no_eligible_agent'


def test_scheduler_filters_by_architecture():
    r=AgentRegistry(30,90)
    r.register(Agent('arm','n1','1',AgentStatus.IDLE,('linux',), 'arm64'))
    r.register(Agent('x86','n2','1',AgentStatus.IDLE,('linux',), 'x86_64'))
    t=Task('t','build',status=TaskStatus.READY,architecture='arm64')
    assert TaskScheduler(r).select(t).agent_id=='arm'


def test_scheduler_orders_ready_tasks_by_priority_then_id():
    r=AgentRegistry(30,90)
    scheduler=TaskScheduler(r)
    tasks=(Task('b','x',priority=1,status=TaskStatus.READY),Task('a','x',priority=3,status=TaskStatus.READY),Task('c','x',priority=3,status=TaskStatus.READY),Task('z','x',status=TaskStatus.PENDING))
    assert tuple(t.task_id for t in scheduler.order_ready(tasks))==('a','c','b')


def test_scheduler_respects_per_agent_concurrency_capacity():
    r=AgentRegistry(30,90)
    r.register(Agent('a1','n1','1',AgentStatus.IDLE,('linux',)))
    scheduler=TaskScheduler(r, max_concurrency_per_agent=1)
    t=Task('t','build',status=TaskStatus.READY,required_capabilities=('linux',))
    assert scheduler.select(t, active_by_agent={'a1': 1}).reason=='agent_capacity_exhausted'
    assert scheduler.select(t, active_by_agent={'a1': 0}).agent_id=='a1'


def test_atomic_claim_enforces_capacity_at_repository_boundary():
    r=AgentRegistry(30,90); r.register(Agent('a1','n1','1',AgentStatus.IDLE,('linux',)))
    from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
    repo=InMemoryControlPlaneRepository()
    repo.create_task(Task('t1','x',status=TaskStatus.READY)); repo.create_task(Task('t2','x',status=TaskStatus.READY))
    repo.claim_task('t1','a1',1,max_concurrency=1)
    import pytest
    with pytest.raises(ValueError, match='capacity'):
        repo.claim_task('t2','a1',1,max_concurrency=1)


def test_scheduler_prefers_least_loaded_eligible_agent():
    r=AgentRegistry(30,90)
    r.register(Agent('a1','n1','1',AgentStatus.IDLE,('linux',)))
    r.register(Agent('a2','n2','1',AgentStatus.IDLE,('linux',)))
    scheduler=TaskScheduler(r,max_concurrency_per_agent=3)
    task=Task('fair','build',status=TaskStatus.READY,required_capabilities=('linux',))
    assert scheduler.select(task,active_by_agent={'a1':2,'a2':0}).agent_id=='a2'
    assert scheduler.select(task,active_by_agent={'a1':1,'a2':1}).agent_id=='a1'

def test_scheduler_prefers_agent_with_fewer_task_failures_when_load_equal():
    r=AgentRegistry(30,90)
    r.register(Agent('a1','n1','1',AgentStatus.IDLE,('linux',)))
    r.register(Agent('a2','n2','1',AgentStatus.IDLE,('linux',)))
    s=TaskScheduler(r,max_concurrency_per_agent=2)
    t=Task('t','build',status=TaskStatus.READY,required_capabilities=('linux',))
    assert s.select(t,active_by_agent={'a1':0,'a2':0},failure_by_agent={'a1':2,'a2':0}).agent_id=='a2'
