"""Static validation for MediaHub external connector boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONNECTORS = ROOT / "profiles" / "connectors"


def load(name: str) -> dict:
    return json.loads((CONNECTORS / name).read_text(encoding="utf-8"))


def main() -> None:
    tinyfish = load("tinyfish.json")
    cloud = load("cloud-service-registry.json")
    boundary = load("github-cloud-boundary.json")

    assert tinyfish["authentication"] == "user_owned_api_key"
    assert tinyfish["credential_scope"] == "github_actions_only"
    assert tinyfish["credentials_in_repository"] is False

    assert cloud["host_credentials_allowed"] is False
    assert cloud["long_lived_cloud_credentials_allowed"] is False
    assert cloud["default_authentication"] == "github_oidc"
    assert cloud["paid_resource_provisioning"] == "disabled_by_default"
    assert cloud["providers"]["tinyfish"]["zero_cost_default"] is True
    assert cloud["providers"]["tinyfish"]["metered_execution"] == "explicit_opt_in"

    assert boundary["local_host_credentials"] is False
    assert boundary["long_lived_cloud_credentials_on_host"] is False
    assert boundary["cloud_authentication"] == "oidc_preferred"
    assert boundary["fail_closed"] is True
    print("CONNECTOR_BOUNDARY=PASS")


if __name__ == "__main__":
    main()
