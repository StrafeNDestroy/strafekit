# Style Guide

## Naming

| Element | Style | Example |
|---|---|---|
| Classes | PascalCase | `CredentialRepository` |
| Functions | snake_case | `scan_host()` |
| Constants | UPPER_SNAKE | `DEFAULT_TIMEOUT` |
| Private | leading underscore | `_internal_helper()` |

## Types — Python 3.12 syntax

```python
def scan(hosts: list[str]) -> dict | None: ...
```

## Docstrings — Google style

```python
def scan_host(host: Host, ports: str = "top-1000") -> ScanResult:
    """Scan a single host for open ports and services.

    Args:
        host: Target host. Must have a valid IP.
        ports: nmap port spec. Defaults to top 1000.

    Returns:
        ScanResult with discovered ports and services.

    Raises:
        ScanError: If nmap fails.
    """
```

## Comments — explain WHY not WHAT

```python
# scan serial — target IDS triggers on concurrent scans
for host in hosts:
    scan(host)
```
