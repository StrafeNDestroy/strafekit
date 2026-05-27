# Hexagonal Architecture

StrafeKit is built on hexagonal architecture — also known as Ports and Adapters.
This page explains the pattern, why it was chosen, and how it maps to the codebase.

---

## The core problem it solves

In a traditional layered application business logic gets tangled with infrastructure.
The scan service calls subprocess directly. The credential service reads files directly.
Testing requires a real database, real tools, real network.

Hexagonal architecture solves this by enforcing one rule:

> **The core knows nothing about the outside world.**

The core defines what it needs through interfaces called ports.
The outside world connects through implementations called adapters.
Dependencies always point inward — never outward.

---

## The dependency rule

This is the single most important rule in the architecture.

```
core/        NEVER imports from adapters/
adapters/    MAY import from core/
tests/       MAY import from anywhere
```

If you find an import from `adapters` inside `core` — that is a violation.
Redesign the interface so core defines what it needs as a port.

---

## Current folder structure

```
strafekit/
│
├── core/                        ← knows nothing about outside world
│   ├── domain/                  ← the nouns (built)
│   │   ├── enums.py             ← all fixed value sets
│   │   └── exceptions.py        ← custom exception hierarchy
│   │
│   ├── ports/                   ← the contracts (coming)
│   └── services/                ← the verbs (coming)
│
└── adapters/                    ← knows about core, never imported by core
    ├── driven/                  ← database, tools, secrets (coming)
    └── driving/                 ← UI, CLI (coming)
```

---

## The three layers of core

### Domain models — the nouns

Pure data containers. No business logic. No external imports.
Represent the concepts in the problem domain.

Currently built:

```python
# strafekit/core/domain/enums.py
class HostStatus(Enum):
    """Reachability status of a discovered host."""
    ALIVE = "alive"
    DEAD = "dead"
    UNREACHABLE = "unreachable"
    UNKNOWN = "unknown"

class VulnerabilitySeverity(IntEnum):
    """Severity levels ordered low to high."""
    INFO = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()
```

Coming next — dataclass models for `Host`, `Credential`, `Finding`, `Engagement`.

### Ports — the contracts (coming)

Interfaces defined as Python Protocols. The core declares what it needs
from the outside world without knowing how it will be provided.

```python
# example of what a port will look like
class CredentialRepository(Protocol):
    def save(self, credential: Credential) -> None: ...
    def find_by_domain(self, domain: str) -> list[Credential]: ...
```

### Services — the verbs (coming)

Business logic. Orchestrates domain models using ports.
Never touches infrastructure directly.

---

## The two sides of the hexagon

### Driving adapters — things that call the core (coming)

```
adapters/driving/tui/      Textual terminal UI
adapters/driving/cli/      Command line interface
```

### Driven adapters — things the core calls (coming)

```
adapters/driven/db/        SQLite repositories
adapters/driven/tools/     nmap, gobuster, nxc wrappers
adapters/driven/secrets/   OS keyring integration
```

---

## Why this matters for testing

The architecture makes testing trivial. The core has no external dependencies.
Tests replace real adapters with in-memory fakes.

No database required. No tools installed. No network. Pure Python objects.

```python
# current test — no infrastructure needed
def test_vulnerability_severity_ordering() -> None:
    """VulnerabilitySeverity is ordered low to high."""
    assert VulnerabilitySeverity.INFO < VulnerabilitySeverity.LOW
    assert VulnerabilitySeverity.LOW < VulnerabilitySeverity.MEDIUM
    assert VulnerabilitySeverity.MEDIUM < VulnerabilitySeverity.HIGH
    assert VulnerabilitySeverity.HIGH < VulnerabilitySeverity.CRITICAL
```

As domain models and services are built — tests remain this simple.
The architecture enforces it.

---

## Exception hierarchy

The first real pattern in the codebase — the exception hierarchy follows
the same principle. `StrafekitError` is the core base. Everything inherits from it.
Callers catch at whatever level makes sense.

```python
# strafekit/core/domain/exceptions.py
class StrafekitError(Exception): pass       # catch anything StrafeKit
class ScanError(StrafekitError): pass       # catch only scan failures
class StorageError(StrafekitError): pass    # catch only storage failures
class ValidationError(StrafekitError): pass # catch only validation failures
class RequiredFieldError(ValidationError): pass  # most specific
class InvalidFieldError(ValidationError): pass   # most specific
```

---

## Design decisions

**Why hexagonal over layered architecture?**
StrafeKit wraps external tools — nmap, gobuster, nxc. Those tools change.
Versions differ between machines. New tools get added. Hexagonal means
swapping a tool changes one adapter file. Nothing else touches.

**Why Python Protocols over ABCs?**
Protocols use structural typing — if a class has the right methods it
satisfies the protocol without explicit inheritance. Duck typing with
type safety enforced by mypy. More Pythonic, less ceremony.

**Why dataclasses for domain models?**
Domain models are pure data. Dataclasses generate `__init__`, `__repr__`,
and `__eq__` automatically. `frozen=True` makes them immutable where appropriate.
No boilerplate, full type safety.

---

## Further reading

- Original paper by Alistair Cockburn: https://alistair.cockburn.us/hexagonal-architecture
- Clean Architecture by Robert Martin — same concept, different framing
- Python Protocols: https://docs.python.org/3/library/typing.html#typing.Protocol
- Python dataclasses: https://docs.python.org/3/library/dataclasses.html
