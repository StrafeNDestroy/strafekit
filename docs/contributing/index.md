# Contributing to StrafeKit

| Topic | Page |
|---|---|
| Naming, types, docstrings | [Style Guide](style.md) |
| Hexagonal architecture | [Architecture](architecture.md) |
| Exception patterns | [Error Handling](error-handling.md) |
| Security requirements | [Security](security.md) |
| NASA standards | [NASA Rules](nasa-rules.md) |
| Commit format | [Commits](commits.md) |
| Daily workflow | [Workflow](workflow.md) |

## The one rule that matters most

```
core/        NEVER imports from adapters/
adapters/    MAY import from core/
```

## Before every commit

```bash
make lint && make type-check
```

## Before every push

```bash
make check
```
