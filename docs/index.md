# StrafeKit

![CI](https://github.com/StrafeNDestroy/strafekit/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)
![Status](https://img.shields.io/badge/status-active_development-orange)

Professional penetration testing framework built in Python.

## What it does

StrafeKit integrates third party tools — nmap, gobuster, nxc,
impacket — into a single terminal UI. Manages engagement state,
tracks credentials, and organizes findings across a pentest.

## Features

- Live terminal UI built with Textual
- Credential management with SQLite
- Automated enumeration workflows
- Engagement scoped data — everything tied to one engagement
- Tool modularity — swap tools in and out

## Install

```bash
uv tool install git+https://github.com/StrafeNDestroy/strafekit.git
strafekit
```

See [Getting Started](getting-started.md) for full setup.
