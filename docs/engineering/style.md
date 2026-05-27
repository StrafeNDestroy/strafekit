# Style Guide

Automated enforcement via ruff and mypy.
Run `make lint` before committing.

---

## Naming conventions

| Element | Style | Example |
|---|---|---|
| Classes | PascalCase | `CredentialRepository` |
| Functions | snake_case | `scan_host()` |
| Constants | UPPER_SNAKE | `DEFAULT_TIMEOUT` |
| Private | leading underscore | `_internal_helper()` |
| Modules | snake_case | `scan_service.py` |
| Packages | snake_case | `core/` |
| Type aliases | PascalCase | `IPAddress = str` |
| Protocols | PascalCase | `ScanExecutor` |

### Naming philosophy

- Names should be self-documenting
- Avoid abbreviations unless universally understood (ip, url, db, id)
- Boolean variables and functions should read as questions

```python
# wrong
flag = True
check = is_valid(host)

# right
is_alive = True
is_valid = validate_host(host)
```

---

## Type annotations

- Every function must have complete type annotations
- No untyped parameters, no untyped return values
- Use Python 3.12 syntax — not the old typing module forms

```python
# wrong — old style
from typing import List, Dict, Optional
def scan(hosts: List[str]) -> Optional[Dict]:
    ...

# right — Python 3.12 style
def scan(hosts: list[str]) -> dict | None:
    ...
```

Use `TypeAlias` for semantic clarity:

```python
from typing import TypeAlias

IPAddress: TypeAlias = str
Port: TypeAlias = int
Domain: TypeAlias = str
```

---

## Docstrings

Every public module, class, and function requires a docstring.
Google style docstrings throughout.

```python
def scan_host(host: Host, ports: str = "top-1000") -> ScanResult:
    """Scan a single host for open ports and running services.

    Executes nmap against the target host and parses the results
    into a structured ScanResult. Uses the configured scan profile
    from AppConfig.

    Args:
        host: The target host to scan. Must have a valid IP address.
        ports: Port specification in nmap format. Defaults to top 1000.

    Returns:
        ScanResult containing all discovered ports and services.

    Raises:
        ScanError: If nmap is not installed or exits with non-zero status.
        TimeoutError: If the scan exceeds the configured timeout.

    Example:
        >>> result = scan_host(Host(ip="10.10.10.5"), ports="22,80,443")
        >>> print(result.open_ports)
        [22, 80, 443]
    """
```

---

## Comments

- Explain WHY not WHAT
- Code explains what — comments explain intent and reasoning
- Every non-obvious decision needs a comment

```python
# wrong — explains what, code already shows that
# loop through hosts
for host in hosts:
    scan(host)

# right — explains why
# scan in serial not parallel here — target network has IDS
# that triggers on concurrent port scans from single source
for host in hosts:
    scan(host)
```

---

## Import ordering

Ruff enforces this automatically. For reference:

```python
# 1. stdlib
import os
import sys
from pathlib import Path

# 2. third party
import sqlalchemy
from textual.app import App

# 3. local
from strafekit.core.domain.host import Host
from strafekit.core.ports.scan_executor import ScanExecutor
```

---

## Function length

- Aim for under 30 lines — ideal, no questions asked
- 30 to 60 lines — acceptable, question whether it can be split
- Over 60 lines — NASA hard limit, requires explicit justification comment

```python
# if you must exceed 60 lines, say why
def build_engagement_report(engagement: Engagement) -> str:
    # NOTE: exceeds 30 line guideline because report generation requires
    # assembling all sections in sequence. Splitting would obscure the
    # report structure. Each section is a single responsibility.
    ...
```
