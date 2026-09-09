#!/usr/bin/env python3
"""Compatibility entry point for the MediaHub Cloud Development Adapter."""
from cloud_development_adapter import (
    ADAPTER_ID,
    AdapterDenied,
    CloudDevelopmentAdapter,
    ProviderProtocolError,
    ProviderRequest,
    ProviderResult,
    SandboxSpec,
)

__all__ = [
    "ADAPTER_ID",
    "AdapterDenied",
    "CloudDevelopmentAdapter",
    "ProviderProtocolError",
    "ProviderRequest",
    "ProviderResult",
    "SandboxSpec",
]
