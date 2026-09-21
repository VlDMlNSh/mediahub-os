from dataclasses import dataclass
from enum import Enum


class LifecycleState(str, Enum):
    ABSENT="absent"; CANDIDATE="candidate"; VALIDATED="validated"; AUTHORIZED="authorized"; PUBLISHED="published"; APPLIED="applied"; SUPERSEDED="superseded"

_ALLOWED={
    LifecycleState.ABSENT:{LifecycleState.CANDIDATE},
    LifecycleState.CANDIDATE:{LifecycleState.VALIDATED},
    LifecycleState.VALIDATED:{LifecycleState.AUTHORIZED},
    LifecycleState.AUTHORIZED:{LifecycleState.PUBLISHED},
    LifecycleState.PUBLISHED:{LifecycleState.APPLIED},
    LifecycleState.APPLIED:{LifecycleState.SUPERSEDED},
    LifecycleState.SUPERSEDED:set(),
}

@dataclass(frozen=True)
class VersionIdentity:
    schema: str
    revision: int
    digest: str
    def __post_init__(self):
        if not isinstance(self.schema,str) or not self.schema: raise ValueError("schema required")
        if not isinstance(self.revision,int) or isinstance(self.revision,bool) or self.revision<0: raise ValueError("invalid revision")
        if not isinstance(self.digest,str) or not self.digest: raise ValueError("digest required")

@dataclass(frozen=True)
class PersistenceContract:
    authority: str
    version: VersionIdentity
    durable: bool=False
    def __post_init__(self):
        if self.authority!="state-authority": raise ValueError("State Authority is canonical")
        if not isinstance(self.durable, bool): raise TypeError("durable must be bool")

@dataclass(frozen=True)
class MigrationContract:
    migration_id: str
    source: VersionIdentity
    target: VersionIdentity
    rollback_supported: bool
    def __post_init__(self):
        if not self.migration_id: raise ValueError("migration id required")
        if not isinstance(self.source, VersionIdentity) or not isinstance(self.target, VersionIdentity): raise TypeError("migration versions required")
        if not isinstance(self.rollback_supported, bool): raise TypeError("rollback_supported must be bool")
        if self.source.revision==self.target.revision: raise ValueError("migration must change revision")

def transition(current: LifecycleState, target: LifecycleState) -> LifecycleState:
    if not isinstance(current, LifecycleState) or not isinstance(target, LifecycleState): raise TypeError("invalid lifecycle state")
    if target not in _ALLOWED[current]: raise ValueError("invalid lifecycle transition")
    return target

def validate_persistence_contract(contract: PersistenceContract) -> PersistenceContract:
    if not isinstance(contract,PersistenceContract): raise TypeError("contract required")
    return contract
