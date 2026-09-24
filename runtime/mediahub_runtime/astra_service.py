"""Minimal resident Astra health/runtime process for systemd installation."""
from __future__ import annotations

import os
import time

from .astra_gateway import AstraGatewayRuntime


def main() -> None:
    # Keep the installed service intentionally inert until an application/API
    # boundary submits Task Contracts. No arbitrary shell listener is exposed.
    AstraGatewayRuntime()
    mode = os.environ.get("MEDIAHUB_RUNTIME_MODE", "local_first")
    print(f"ASTRA_RUNTIME_READY mode={mode}", flush=True)
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
