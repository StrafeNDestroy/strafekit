"""Unit tests for StrafeKit domain enums."""

from strafekit.core.domain.enums import HostStatus, VulnerabilitySeverity


def test_host_status_values() -> None:
    """HostStatus enum has all expected values."""
    assert HostStatus.ALIVE.value == "alive"
    assert HostStatus.DEAD.value == "dead"
    assert HostStatus.UNREACHABLE.value == "unreachable"
    assert HostStatus.UNKNOWN.value == "unknown"


def test_vulnerability_severity_ordering() -> None:
    """VulnerabilitySeverity is ordered low to high."""
    assert VulnerabilitySeverity.INFO < VulnerabilitySeverity.LOW
    assert VulnerabilitySeverity.LOW < VulnerabilitySeverity.MEDIUM
    assert VulnerabilitySeverity.MEDIUM < VulnerabilitySeverity.HIGH
    assert VulnerabilitySeverity.HIGH < VulnerabilitySeverity.CRITICAL
