# Architecture Rules

The hexagonal architecture dependency rule is the most important rule in this codebase.
Breaking it collapses the separation between business logic and infrastructure.

---

## The dependency rule

```
core/        NEVER imports from adapters/
adapters/    MAY import from core/
tests/       MAY import from anywhere
```

Dependencies point inward — toward the core. Never outward.

If you find yourself importing from `adapters` inside `core` — stop.
Redesign the interface so the core defines what it needs as a port.

---

## The three layers

```
driving adapters    →    core    ←    driven adapters
(Textual, CLI)           ↑            (SQLite, nmap, gobuster)
                         │
                      ports
                    (interfaces / Protocols)
```

| Layer | Location | Rule |
|---|---|---|
| Domain models | `core/domain/` | Pure data, no external imports |
| Ports | `core/ports/` | Protocols defining contracts |
| Services | `core/services/` | Business logic, imports ports only |
| Driven adapters | `adapters/driven/` | Implements ports — database, tools |
| Driving adapters | `adapters/driving/` | Calls services — UI, CLI |

---

## Subprocess calls

All external tool execution must go through the adapter layer.
Never call subprocess directly from core code.

```python
# wrong — subprocess in core logic
class ScanService:
    def scan(self, host: Host) -> ScanResult:
        result = subprocess.run(["nmap", host.ip])

# right — core calls port, adapter handles subprocess
class ScanService:
    def __init__(self, executor: ScanExecutor):
        self.executor = executor

    def scan(self, host: Host) -> ScanResult:
        return self.executor.run_nmap(host)
```

---

## Nouns vs verbs

```
Noun → dataclass       holds data, validates, compares
Verb → regular class   performs operations, contains logic
```

| Location | Type | Example |
|---|---|---|
| `core/domain/` | dataclass | `Host`, `Credential`, `Finding` |
| `core/services/` | regular class | `ScanService`, `SprayService` |
| `core/ports/` | Protocol | `ScanExecutor`, `CredentialRepository` |
| `adapters/` | regular class | `NmapExecutor`, `SQLiteRepository` |

---

## File and path operations

Always use `pathlib.Path` — never string concatenation.

```python
# wrong
path = "/home/user/engagements/" + engagement_name + "/results.txt"

# right
path = Path("/home/user/engagements") / engagement_name / "results.txt"
```
