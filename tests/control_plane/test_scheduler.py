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
