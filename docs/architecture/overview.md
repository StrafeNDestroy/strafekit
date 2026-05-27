# Architecture Overview

StrafeKit is designed as a local penetration testing platform.
This page covers the high level architectural decisions and why they were made.

---

## What StrafeKit is

A local tool that runs on your attack box during an engagement.
It integrates third party security tools into a single terminal UI,
manages engagement state, tracks credentials, and organizes findings.

```
nmap + gobuster + nxc + impacket
            ↓
        StrafeKit
            ↓
    Single terminal UI
    Engagement database
    Credential store
    Findings tracker
```

---

## Core architectural decisions

### Hexagonal architecture

The codebase is organized around hexagonal architecture — also called
Ports and Adapters. Business logic lives in the core and knows nothing
about databases, tools, or the UI. See [Hexagonal Architecture](hexagonal.md)
for the full explanation.

### Terminal UI — Textual

StrafeKit runs entirely in the terminal. No browser, no separate server,
no Java runtime. Built with Textual — a Python TUI framework built on asyncio.

Why terminal:
- Works over SSH on a remote attack box
- No separate window to manage during an engagement
- Keyboard driven — faster than mouse during active testing
- Single process — scans, results, and UI in one place

### SQLite for storage

Engagement data lives in a SQLite database — one file per engagement.
Portable, queryable, no server process required.

Why SQLite over PostgreSQL:
- Single user, single machine — no concurrent network clients
- One file = easy to backup, archive, or hand off
- Built into Python — no installation required
- Handles the write frequency of a pentest engagement comfortably

### asyncio for concurrency

Multiple scans run simultaneously without blocking the UI.
Textual is built on asyncio — scan workers post messages to the UI
through an event queue. The UI reacts when data arrives.

```
nmap worker     → message queue → Hosts panel
gobuster worker → message queue → Web panel
spray worker    → message queue → Creds panel
```

---

## Current state

StrafeKit is in active development. This documents what is built
and what is planned.

### Built

```
✅ Project infrastructure     pyproject.toml, uv, Makefile
✅ CI/CD pipeline             GitHub Actions — lint, type check, test
✅ Documentation site         MkDocs Material hosted on GitHub Pages
✅ Domain enums               HostStatus, VulnerabilitySeverity, etc
✅ Exception hierarchy        StrafekitError and all children
```

### In progress

```
🔧 Domain models              Host, Credential, Finding, Engagement
🔧 Ports                      CredentialRepository, ScanExecutor
🔧 Services                   ScanService, SprayService
🔧 Driven adapters            SQLite, nmap, gobuster wrappers
🔧 Driving adapters           Textual UI, CLI
```

---

## Technology stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.12+ | Core language |
| UI | Textual | Terminal interface |
| Database | SQLite + SQLAlchemy | Engagement data storage |
| Concurrency | asyncio | Non-blocking scan execution |
| Secrets | keyring | OS keyring integration |
| Testing | pytest | Unit and integration tests |
| Type checking | mypy strict | Static type safety |
| Linting | ruff | Code quality and formatting |
| Security linting | bandit | Security issue detection |
| Docs | MkDocs Material | Documentation site |
| CI/CD | GitHub Actions | Automated quality checks |
| Packaging | uv + hatchling | Dependency management |

---

## Design principles

These principles guide every decision in the codebase.

**Reliability over cleverness** — code that is easy to read and reason
about is more valuable than clever one-liners during an engagement.

**Explicit over implicit** — no magic. Every dependency is injected,
every configuration is explicit, every error is named.

**Testable by design** — hexagonal architecture ensures the core logic
can be tested without any real infrastructure. Fast, isolated, reliable tests.

**Security by default** — StrafeKit handles sensitive engagement data.
Credentials are encrypted at rest. No secrets in code. No shell injection vectors.

**NASA Power of 10** — coding standards adapted from NASA/JPL safety
critical systems. Simple control flow, bounded loops, validated inputs,
checked return values. See [NASA Rules](../contributing/nasa-rules.md).
