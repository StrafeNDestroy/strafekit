"""Custom exception hierarchy for StrafeKit.

All exceptions inherit from StrafekitError allowing broad or specific catching.

Example:
    >>> try:
    ...     scan_host(host)
    ... except ScanError as e:
    ...     retry(host)
    ... except StrafekitError as e:
    ...     log.error(e)
"""


class StrafekitError(Exception):
    """Base exception for all StrafeKit errors."""

    pass


class CredentialError(StrafekitError):
    """Raised when credential operations fail."""

    pass


class EngagementError(StrafekitError):
    """Raised when engagement state is invalid."""

    pass


class ScanError(StrafekitError):
    """Raised when a scan fails to complete."""

    pass


class SecretError(StrafekitError):
    """Raised when secret store operations fail."""

    pass


class StorageError(StrafekitError):
    """Raised when database operations fail."""

    pass


class ToolNotFoundError(StrafekitError):
    """Raised when a required external tool is not installed."""

    pass


class ValidationError(StrafekitError):
    """Raised when input validation fails."""

    pass


class InvalidFieldError(ValidationError):
    """Raised when a field value is present but invalid."""

    pass


class RequiredFieldError(ValidationError):
    """Raised when a required field is missing or empty."""

    pass
