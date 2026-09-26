from runtime.mediahub_control_plane.model import OperationStatus, Task, TaskStatus
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.service import ControlPlaneService
from runtime.mediahub_control_plane.sqlite_repository import SQLiteControlPlaneRepository

def _begin(repo):
    repo.create_task(Task('t','external',status=TaskStatus.READY,max_attempts=2))
    service=ControlPlaneService(repo); lease=service.claim('t','agent',7)
    op=service.begin_external_operation('t','agent',7,'provider-x','model-y','op-key-1')
    return service,lease,op

def test_ambiguous_operation_is_durable_and_blocks_replay_by_default(tmp_path):
    db=tmp_path/'cp.sqlite'; repo=SQLiteControlPlaneRepository(db)
    service,_,op=_begin(repo); marked=service.mark_external_ambiguous(op.operation_id,'agent',7)
    assert marked.status is OperationStatus.RECONCILIATION_REQUIRED
    assert repo.get_task('t').status is TaskStatus.RECONCILIATION_REQUIRED
    reopened=SQLiteControlPlaneRepository(db)
    assert reopened.get_operation(op.operation_id).status is OperationStatus.RECONCILIATION_REQUIRED
    assert reopened.get_task('t').status is TaskStatus.RECONCILIATION_REQUIRED
    assert reopened.get_operation_by_key('op-key-1').operation_id==op.operation_id

def test_operation_key_deduplicates_external_dispatch_identity():
    repo=InMemoryControlPlaneRepository(); service,_,op=_begin(repo)
    same=service.begin_external_operation('t','agent',7,'provider-x','model-y','op-key-1')
    assert same.operation_id==op.operation_id and len(repo.operations)==1

def test_reconciliation_can_prove_success_without_replay():
    repo=InMemoryControlPlaneRepository(); service,_,op=_begin(repo)
    service.mark_external_ambiguous(op.operation_id,'agent',7)
    resolved=service.reconcile_external_operation(op.operation_id,'agent','SUCCEEDED',{'marker':'proof'})
    assert resolved.status is OperationStatus.RESOLVED and repo.get_task('t').status is TaskStatus.SUCCEEDED

def test_replay_requires_explicit_policy():
    repo=InMemoryControlPlaneRepository(); service,_,op=_begin(repo)
    service.mark_external_ambiguous(op.operation_id,'agent',7)
    try: service.reconcile_external_operation(op.operation_id,'agent','REPLAY_AUTHORIZED')
    except PermissionError: pass
    else: raise AssertionError('replay must require explicit authorization')

def test_restart_promotes_inflight_operation_to_reconciliation(tmp_path):
    db=tmp_path/'cp.sqlite'; repo=SQLiteControlPlaneRepository(db)
    service,_,op=_begin(repo)
    reopened=SQLiteControlPlaneRepository(db); recovered=ControlPlaneService(reopened).recover_inflight_operations()
    assert recovered[0].status is OperationStatus.RECONCILIATION_REQUIRED
    assert reopened.get_task('t').status is TaskStatus.RECONCILIATION_REQUIRED

def test_explicit_replay_authorization_returns_task_to_ready():
    repo=InMemoryControlPlaneRepository(); service,_,op=_begin(repo)
    service.mark_external_ambiguous(op.operation_id,'agent',7)
    resolved=service.reconcile_external_operation(op.operation_id,'agent','REPLAY_AUTHORIZED',allow_replay=True)
    assert resolved.status is OperationStatus.REPLAY_AUTHORIZED
    assert repo.get_task('t').status is TaskStatus.READY
