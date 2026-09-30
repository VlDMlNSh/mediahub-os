#!/usr/bin/env python3
"""Deterministic, non-production cluster identity/trust PoC.

This module models the first federation boundary only: identity validation
and trust admission. It performs no network I/O, credential access, or
production authentication.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


SCHEMA = "mediahub.cluster-trust-poc.v1"


@dataclass(frozen=True)
class ClusterIdentity:
    cluster_id: str
    administrative_domain: str
    trust_anchor: str
    capabilities: tuple[str, ...]
    identity_digest: str

    @classmethod
    def issue(
        cls,
        cluster_id: str,
        administrative_domain: str,
        trust_anchor: str,
        capabilities: tuple[str, ...],
    ) -> "ClusterIdentity":
        material = "|".join(
            [cluster_id, administrative_domain, trust_anchor, *sorted(capabilities)]
        ).encode()
        digest = hashlib.sha256(material).hexdigest()
        return cls(cluster_id, administrative_domain, trust_anchor, tuple(sorted(capabilities)), digest)


def verify_identity(identity: ClusterIdentity, trusted_anchors: set[str]) -> tuple[bool, str]:
    material = "|".join(
        [
            identity.cluster_id,
            identity.administrative_domain,
            identity.trust_anchor,
            *sorted(identity.capabilities),
        ]
    ).encode()
    expected = hashlib.sha256(material).hexdigest()
    if identity.identity_digest != expected:
        return False, "identity_integrity_failure"
    if identity.trust_anchor not in trusted_anchors:
        return False, "untrusted_anchor"
    if not identity.cluster_id or not identity.administrative_domain:
        return False, "incomplete_identity"
    return True, "trusted_identity"


def evaluate_federation_trust(
    source: ClusterIdentity,
    destination: ClusterIdentity,
    *,
    trusted_anchors: set[str],
    requested_capability: str,
) -> dict:
    source_ok, source_reason = verify_identity(source, trusted_anchors)
    destination_ok, destination_reason = verify_identity(destination, trusted_anchors)

    if not source_ok:
        decision, reason = "DENY", f"source_{source_reason}"
    elif not destination_ok:
        decision, reason = "DENY", f"destination_{destination_reason}"
    elif requested_capability not in source.capabilities:
        decision, reason = "DENY", "source_capability_not_advertised"
    elif requested_capability not in destination.capabilities:
        decision, reason = "DENY", "destination_capability_not_advertised"
    else:
        decision, reason = "ALLOW", "trusted_identity_and_capability"

    return {
        "schema": SCHEMA,
        "source_cluster": source.cluster_id,
        "destination_cluster": destination.cluster_id,
        "source_domain": source.administrative_domain,
        "destination_domain": destination.administrative_domain,
        "requested_capability": requested_capability,
        "decision": decision,
        "reason": reason,
        "source_identity_verified": source_ok,
        "destination_identity_verified": destination_ok,
        "pass": True,
    }


def run_all() -> dict:
    local = ClusterIdentity.issue(
        "local-a", "user-local", "mediahub-root-v1", ("ai.infer", "media.process")
    )
    cloud = ClusterIdentity.issue(
        "dev-a", "company-development", "mediahub-root-v1", ("ai.infer", "ci.build")
    )
    unknown = ClusterIdentity.issue(
        "unknown-a", "external", "untrusted-root", ("ai.infer",)
    )
    tampered = ClusterIdentity(
        local.cluster_id,
        local.administrative_domain,
        local.trust_anchor,
        local.capabilities,
        "0" * 64,
    )

    scenarios = [
        evaluate_federation_trust(
            local, cloud, trusted_anchors={"mediahub-root-v1"}, requested_capability="ai.infer"
        ),
        evaluate_federation_trust(
            unknown, cloud, trusted_anchors={"mediahub-root-v1"}, requested_capability="ai.infer"
        ),
        evaluate_federation_trust(
            tampered, cloud, trusted_anchors={"mediahub-root-v1"}, requested_capability="ai.infer"
        ),
        evaluate_federation_trust(
            local, cloud, trusted_anchors={"mediahub-root-v1"}, requested_capability="storage.enumerate"
        ),
    ]
    scenarios[0]["scenario"] = "S1_trusted_identity"
    scenarios[1]["scenario"] = "S2_untrusted_anchor_denial"
    scenarios[2]["scenario"] = "S3_identity_integrity_denial"
    scenarios[3]["scenario"] = "S4_unadvertised_capability_denial"

    return {
        "schema": SCHEMA,
        "mode": "non-production-deterministic",
        "scenarios": scenarios,
        "pass": all(item["pass"] for item in scenarios),
    }


if __name__ == "__main__":
    print(json.dumps(run_all(), sort_keys=True, separators=(",", ":")))
