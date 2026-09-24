"""State authority interface; persistence is intentionally out of scope."""

from abc import ABC, abstractmethod


class StateAuthority(ABC):
    """Canonical boundary for authoritative state mutations."""

    @abstractmethod
    def read(self, key):
        raise NotImplementedError

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def abort(self):
        raise NotImplementedError

    @abstractmethod
    def snapshot(self):
        raise NotImplementedError

    @abstractmethod
    def restore(self, snapshot_reference):
        raise NotImplementedError
