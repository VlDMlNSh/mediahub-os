from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from threading import RLock


class StateAuthorityError(RuntimeError): pass
class AuthorizationDenied(StateAuthorityError): pass
class ConflictDetected(StateAuthorityError): pass
class DuplicateCommand(StateAuthorityError): pass
class InvalidCommand(StateAuthorityError): pass
class AuthorityUnavailable(StateAuthorityError): pass

@dataclass(frozen=True)
class AuthorizationContext:
    subject: str
    authenticated: bool
    permissions: frozenset[str] = frozenset()

@dataclass(frozen=True)
class Command:
    command_id: str
    correlation_id: str
    operation: str
    path: tuple[str, ...]
    value: object = None
    expected_generation: int | None = None
    authorization: AuthorizationContext | None = None
    source_identity: str = ""
    causation_id: str | None = None

@dataclass(frozen=True)
class Event:
    sequence: int
    event_id: str
    command_id: str
    correlation_id: str
    operation: str
    path: tuple[str, ...]
    generation: int
    state_version: int
    state_digest: str
    source_identity: str = ""
    causation_id: str | None = None
    timestamp: str = ""

class StateAuthority:
    """Single canonical, thread-safe, in-memory mutation authority."""
    def __init__(self, initial_state=None, policy=None):
        self._lock=RLock(); self._state=deepcopy(dict(initial_state or {}))
        self._generation=0; self._version=0; self._sequence=0
        self._events=[]; self._processed={}; self._available=True
        self._policy=dict(policy or {"set":frozenset({"state.write"}),"delete":frozenset({"state.write"})})
        self._token=sha256(b"mediahub-state-authority-v1").hexdigest()
        self._observers=[]
    def set_available(self, available):
        with self._lock: self._available=bool(available)
    def subscribe(self, observer):
        with self._lock: self._observers.append(observer)
    def read(self):
        with self._lock:
            self._require(); return deepcopy(self._state)
    def metadata(self):
        with self._lock: return {"generation":self._generation,"state_version":self._version,"event_sequence":self._sequence,"available":self._available}
    def events(self):
        with self._lock: return tuple(self._events)
    def execute(self, command):
        with self._lock:
            self._require(); self._validate(command)
            if command.command_id in self._processed: raise DuplicateCommand(command.command_id)
            self._authorize(command)
            self._validate_causation(command)
            if command.expected_generation is not None and command.expected_generation != self._generation:
                raise ConflictDetected("stale generation")
            candidate=deepcopy(self._state)
            if command.operation=="set": self._set(candidate,command.path,deepcopy(command.value))
            elif command.operation=="delete": self._delete(candidate,command.path)
            self._state=candidate; self._generation+=1; self._version+=1; self._sequence+=1
            event=Event(self._sequence,f"evt-{self._sequence:012d}",command.command_id,command.correlation_id,command.operation,command.path,self._generation,self._version,self._digest(self._state),command.source_identity,command.causation_id,datetime.now(timezone.utc).isoformat())
            self._events.append(event); self._processed[command.command_id]=event; observers=tuple(self._observers)
        for observer in observers: observer(event)
        return event
    def checkpoint(self):
        with self._lock:
            self._require(); return (self._token,deepcopy(self._state),self._generation,self._version,self._sequence,tuple(self._events),tuple(self._processed.items()))
    def restore(self, checkpoint, authorization=None):
        with self._lock:
            self._require()
            if authorization is None or not isinstance(authorization,AuthorizationContext):
                raise AuthorizationDenied("restore authorization required")
            if not authorization.authenticated or "state.restore" not in authorization.permissions:
                raise AuthorizationDenied("restore authorization denied")
            if not isinstance(checkpoint,tuple) or len(checkpoint)!=7: raise InvalidCommand("invalid checkpoint")
            token,state,generation,version,sequence,events,processed=checkpoint
            if token!=self._token: raise AuthorizationDenied("checkpoint token rejected")
            if not isinstance(state,dict) or generation<0 or version<generation or sequence<0: raise InvalidCommand("invalid checkpoint")
            if not isinstance(events,tuple) or not isinstance(processed,tuple): raise InvalidCommand("invalid checkpoint history")
            if len(events)!=sequence or len(processed)!=sequence: raise InvalidCommand("invalid checkpoint history")
            if any(not isinstance(event,Event) or event.sequence != index for index,event in enumerate(events,1)): raise InvalidCommand("invalid checkpoint events")
            if any(not isinstance(item,tuple) or len(item)!=2 or not isinstance(item[0],str) or not isinstance(item[1],Event) for item in processed): raise InvalidCommand("invalid checkpoint processed map")
            restored_processed=dict(processed)
            if len(restored_processed)!=len(processed) or any(restored_processed.get(event.command_id)!=event for event in events): raise InvalidCommand("invalid checkpoint processed map")
            self._state=deepcopy(state); self._generation=generation; self._version=version; self._sequence=sequence; self._events=list(events); self._processed=restored_processed
    def _require(self):
        if not self._available: raise AuthorityUnavailable("State Authority unavailable; fail closed")
    def _validate(self,c):
        if not isinstance(c,Command) or not c.command_id or not c.correlation_id: raise InvalidCommand("command identity required")
        if c.operation not in self._policy or not c.path or any(not isinstance(x,str) or not x for x in c.path): raise InvalidCommand("invalid command")
        if c.source_identity and not isinstance(c.source_identity,str): raise InvalidCommand("invalid source identity")
        if c.causation_id is not None and (not isinstance(c.causation_id,str) or not c.causation_id): raise InvalidCommand("invalid causation id")
    def _validate_causation(self,c):
        if c.causation_id is None: return
        if not any(event.event_id == c.causation_id for event in self._events): raise InvalidCommand("causation event not found")
    def _authorize(self,c):
        a=c.authorization
        if a is None or not a.authenticated or not self._policy[c.operation].issubset(a.permissions): raise AuthorizationDenied("authorization denied")
    @staticmethod
    def _set(state,path,value):
        cur=state
        for part in path[:-1]:
            child=cur.setdefault(part,{})
            if not isinstance(child,dict): raise InvalidCommand("path crosses scalar")
            cur=child
        cur[path[-1]]=value
    @staticmethod
    def _delete(state,path):
        cur=state
        for part in path[:-1]:
            cur=cur.get(part)
            if not isinstance(cur,dict): raise InvalidCommand("delete path missing")
        if path[-1] not in cur: raise InvalidCommand("delete path missing")
        del cur[path[-1]]
    @classmethod
    def _canonicalize(cls, value):
        if isinstance(value,dict): return tuple((str(k),cls._canonicalize(v)) for k,v in sorted(value.items(),key=lambda item:str(item[0])))
        if isinstance(value,(list,tuple)): return tuple(cls._canonicalize(v) for v in value)
        if isinstance(value,set): return tuple(sorted((cls._canonicalize(v) for v in value),key=repr))
        return value
    @classmethod
    def _digest(cls,state): return sha256(repr(cls._canonicalize(state)).encode("utf-8")).hexdigest()
