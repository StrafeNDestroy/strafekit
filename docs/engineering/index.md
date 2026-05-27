# Engineering Standards

![CI](https://github.com/StrafeNDestroy/strafekit/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)
![Status](https://img.shields.io/badge/status-active_development-orange)


This section documents the technical decisions, architecture patterns,
and development standards used in StrafeKit.

Written as a reference for the project and as a demonstration of
professional Python development practices.

## About this project

StrafeKit is an active development project built to demonstrate
professional Python engineering practices:

- Hexagonal architecture with clean separation of concerns
- Full CI/CD pipeline with automated quality checks
- Test driven development with pytest
- Type safe Python with mypy strict mode
- Security focused development with bandit
- NASA Power of 10 coding standards


---

## Quick reference

| Topic | Page |
|---|---|
| Naming, types, docstrings, comments | [Style Guide](style.md) |
| Hexagonal architecture rules | [Architecture Rules](architecture.md) |
| Exception patterns and error handling | [Error Handling](error-handling.md) |
| Security requirements | [Security Rules](security.md) |
| NASA Power of 10 coding standards | [NASA Rules](nasa-rules.md) |
| Commit message format | [Commit Messages](commits.md) |
| Daily development workflow | [Workflow](workflow.md) |

---

## The one rule that matters most

```
core/        NEVER imports from adapters/
adapters/    MAY import from core/
```

If you break this rule the architecture collapses. Everything else is style.

---

## Before every commit

```bash
make lint
make type-check
```

## Before every push

```bash
make check
```

---

## Automated enforcement

These run automatically — you cannot commit code that violates them:

| Tool | Enforces |
|---|---|
| ruff | linting and formatting |
| mypy | type checking |
| bandit | security scanning |
| commitizen | commit message format |
| pre-commit | runs all of the above on every commit |

---

## Philosophy

Inspired by systems programming clarity and NASA/JPL Power of 10 standards.
Built for security professionals who need reliable, readable, maintainable tooling.

- Code should read like documentation
- Prefer explicit over implicit
- If it is not obvious why — explain it in a comment
- Reliability over cleverness
- A junior developer should be able to read any function and understand it
