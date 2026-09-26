"""Atomic task leases for parallel autonomous worktrees."""
from __future__ import annotations
import fcntl, json, os, subprocess, time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Self, TextIO
class LeaseDenied(PermissionError): pass
ACTIVE="ACTIVE"; STALE="STALE"; ORPHANED="ORPHANED"; UNKNOWN="UNKNOWN"

def current_process_start_identity(pid: int | None = None) -> str | None:
    pid = os.getpid() if pid is None else pid
    try:
        fields = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8").split()
        if len(fields) > 21: return fields[21]
    except (OSError, ValueError):
        pass
    try:
        result = subprocess.run(["ps", "-p", str(pid), "-o", "lstart="], text=True, capture_output=True, check=False, timeout=2)  # nosec B603
        value = result.stdout.strip()
        return value or None
    except (OSError, subprocess.SubprocessError):
        return None

def _owner_probe(record: dict) -> tuple[bool, bool]:
    pid, start = record.get("pid"), record.get("process_start_identity")
    if not isinstance(pid,int) or isinstance(pid,bool) or not isinstance(start,str) or not start: return False,False
    try: os.kill(pid,0)
    except (ProcessLookupError,PermissionError): return False,True
    except OSError: return False,False
    observed=current_process_start_identity(pid)
    if observed is None: return False,False
    return observed==start,True

def classify_lease_record(record: dict, *, now: float|None=None, owner_probe: Callable[[dict],tuple[bool,bool]]|None=None)->str:
    required=("task_id","worker_id","pid","process_start_identity","worktree","branch","base_sha")
    if any(not record.get(k) for k in required): return UNKNOWN
    if not isinstance(record.get("pid"),int) or isinstance(record.get("pid"),bool): return UNKNOWN
    expires_at=record.get("expires_at")
    if not isinstance(expires_at,(int,float)) or isinstance(expires_at,bool): return UNKNOWN
    live,observable=(owner_probe or _owner_probe)(record)
    if not observable:return UNKNOWN
    if live:return ACTIVE if expires_at >= (time.time() if now is None else now) else STALE
    return ORPHANED

@dataclass
class TaskLease:
    path: Path; task_id: str; worker_id: str; ttl_seconds: int=900; pid:int|None=None; process_start_identity:str|None=None
    worktree:str|None=None; branch:str|None=None; base_sha:str|None=None; checkpoint_id:str|None=None; _handle:TextIO|None=None
    def acquire(self)->None:
        if not self.task_id or not self.worker_id: raise LeaseDenied("task and worker identities are required")
        if self.ttl_seconds<=0: raise LeaseDenied("lease TTL must be positive")
        self.path.parent.mkdir(parents=True,exist_ok=True); handle=open(self.path,"a+",encoding="utf-8")
        try: fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError as exc: handle.close(); raise LeaseDenied("task is already leased") from exc
        self._handle=handle; self.pid=os.getpid() if self.pid is None else self.pid
        self.process_start_identity=current_process_start_identity(self.pid) if self.process_start_identity is None else self.process_start_identity
        now=time.time(); record={"task_id":self.task_id,"worker_id":self.worker_id,"pid":self.pid,"process_start_identity":self.process_start_identity,"worktree":self.worktree or os.environ.get("MEDIAHUB_WORKTREE"),"branch":self.branch or os.environ.get("MEDIAHUB_BRANCH"),"base_sha":self.base_sha or os.environ.get("MEDIAHUB_BASE_SHA"),"checkpoint_id":self.checkpoint_id or os.environ.get("MEDIAHUB_CHECKPOINT_ID"),"created_at":now,"expires_at":now+self.ttl_seconds}
        handle.seek(0); handle.truncate(); json.dump(record,handle,sort_keys=True); handle.flush(); os.fsync(handle.fileno())
    def read_record(self)->dict:
        try:return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError,ValueError):return {}
    def state(self,*,now:float|None=None,owner_probe=None)->str:return classify_lease_record(self.read_record(),now=now,owner_probe=owner_probe)
    def release(self)->None:
        if self._handle is None:return
        fcntl.flock(self._handle.fileno(),fcntl.LOCK_UN); self._handle.close(); self._handle=None
    def __enter__(self)->Self:self.acquire(); return self
    def __exit__(self,exc_type,exc,tb)->None:self.release()
