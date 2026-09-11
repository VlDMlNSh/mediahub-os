"""Deterministic, sticky fail-closed selection of approved cloud egress paths."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

from ops.hybrid_cloud_api_egress_adapter import CloudAPIUnavailable, TunnelStatus


@dataclass(frozen=True)
class EgressPath:
    name: str
    interface: str
    source: str


@dataclass
class HybridCloudAPIEgressChain:
    paths: tuple[EgressPath, ...]
    probe: Callable[[str], TunnelStatus]
    _active: int | None = None

    def select(self) -> TunnelStatus:
        order = list(range(len(self.paths)))
        if self._active in order:
            order.remove(self._active)
            order.insert(0, self._active)
        for index in order:
            path = self.paths[index]
            status = self.probe(path.interface)
            if status.healthy:
                self._active = index
                return TunnelStatus(path.interface, True, path.source)
        self._active = None
        raise CloudAPIUnavailable("all approved cloud egress paths are unhealthy")

    @property
    def active(self) -> EgressPath | None:
        return self.paths[self._active] if self._active is not None else None
