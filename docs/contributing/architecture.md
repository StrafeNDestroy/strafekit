# Architecture Rules

## The dependency rule

```
core/        NEVER imports from adapters/
adapters/    MAY import from core/
tests/       MAY import from anywhere
```

## Layers

| Layer | Location | Purpose |
|---|---|---|
| Domain models | `core/domain/` | Pure data, dataclasses |
| Ports | `core/ports/` | Protocol contracts |
| Services | `core/services/` | Business logic |
| Driven adapters | `adapters/driven/` | DB, tools |
| Driving adapters | `adapters/driving/` | UI, CLI |

## Subprocess — adapters only

```python
# right
class ScanService:
    def __init__(self, executor: ScanExecutor):
        self.executor = executor
    def scan(self, host: Host) -> ScanResult:
        return self.executor.run_nmap(host)
```
