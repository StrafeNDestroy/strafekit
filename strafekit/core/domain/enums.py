"""Enumeration types for StrafeKit domain models."""

from enum import Enum, IntEnum, auto


class VulnerabilitySeverity(IntEnum):
    """Severity levels for security findings. Higher value means more severe."""

    INFO = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


class HostStatus(Enum):
    """Reachability status of a discovered host."""

    ALIVE = "alive"
    DEAD = "dead"
    UNREACHABLE = "unreachable"
    UNKNOWN = "unknown"


class EngagementStatus(Enum):
    """Lifecycle status of a penetration testing engagement."""

    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETE = "complete"
    ARCHIVED = "archived"


class NetworkProtocol(Enum):
    """Network transport protocol."""

    TCP = "tcp"
    UDP = "udp"


class CredentialType(Enum):
    """Format of a discovered credential."""

    PLAINTEXT = "plaintext"
    NTLM = "ntlm"
    NTLMV2 = "ntlmv2"
    MD5 = "md5"
    SHA1 = "sha1"


class SSHKeyType(Enum):
    """SSH key algorithm type."""

    RSA = "rsa"
    ED25519 = "ed25519"
    ECDSA = "ecdsa"


class KerberosTicketType(Enum):
    """Type of Kerberos ticket."""

    TGT = "tgt"
    TGS = "tgs"


class AccessLevel(Enum):
    """Level of access a credential provides on a host."""

    ADMIN = "admin"
    USER = "user"
    ROOT = "root"


class TrustDirection(Enum):
    """Direction of an Active Directory domain trust relationship."""

    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BIDIRECTIONAL = "bidirectional"
