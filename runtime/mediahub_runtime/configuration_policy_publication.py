"""P0-07 publication adapter mediated exclusively by P0-05."""

from __future__ import annotations

from dataclasses import dataclass

from .authorization import AuthorizationContext
from .configuration_policy import Configuration, Policy
from .configuration_policy_operations import (
    ConfigurationPolicyOperationBoundary,
    ConfigurationPolicyOperationRequest,
)
from .consumer_boundary import ConsumerBoundary, ConsumerBoundaryError


@dataclass(frozen=True)
class PublicationResult:
    resource_type: str
    revision: int


class ConfigurationPolicyPublicationAdapter:
    """Publish one complete document through the frozen P0-05 boundary."""

    def __init__(self, consumer_boundary: ConsumerBoundary, operation_boundary: ConfigurationPolicyOperationBoundary) -> None:
        if type(consumer_boundary) is not ConsumerBoundary:
            raise ValueError("invalid consumer boundary")
        if type(operation_boundary) is not ConfigurationPolicyOperationBoundary:
            raise ValueError("invalid operation boundary")
        self._consumer = consumer_boundary
        self._operations = operation_boundary

    def publish(self, *, resource_type: str, resource: str, payload: Configuration | Policy, context: AuthorizationContext) -> PublicationResult:
        if resource_type not in {"configuration", "policy"}:
            raise ConsumerBoundaryError("operation_rejected")
        request = ConfigurationPolicyOperationRequest(
            resource_type=resource_type,
            operation="replace",
            resource=resource,
            context=context,
            payload=payload,
        )
        self._operations.authorize(request)

        before = self._consumer.read()
        if not isinstance(before, dict):
            raise ConsumerBoundaryError("operation_rejected")
        expected_version = before.get("version")
        if type(expected_version) is not int or expected_version < 0:
            raise ConsumerBoundaryError("operation_rejected")

        tx = self._consumer.begin(self._consumer.request("begin", context), {resource_type: payload.as_dict()})
        try:
            self._consumer.update(tx, {resource_type: payload.as_dict(), "expected_version": expected_version})
            self._consumer.commit(self._consumer.request("commit", context), tx)
        except Exception:
            try:
                self._consumer.abort(self._consumer.request("abort", context), tx)
            except Exception:
                pass
            raise

        after = self._consumer.read()
        if not isinstance(after, dict):
            raise ConsumerBoundaryError("operation_rejected")
        revision = after.get("version")
        if type(revision) is not int or revision <= expected_version:
            raise ConsumerBoundaryError("stale_transaction")
        return PublicationResult(resource_type=resource_type, revision=revision)
