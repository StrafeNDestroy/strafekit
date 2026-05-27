# Development Workflow

Day to day workflow for developing StrafeKit.

---

## Setup

```bash
git clone https://github.com/StrafeNDestroy/strafekit.git
cd strafekit
uv sync
source .venv/bin/activate
strafekit
```

---

## Daily workflow

```bash
# 1. write code
nvim strafekit/core/domain/host.py

# 2. run checks locally
make lint
make type-check

# 3. write tests alongside code
nvim tests/unit/core/test_host.py

# 4. run tests with coverage
make test

# 5. run everything before committing
make check

# 6. stage only what belongs in this commit
git status
git add strafekit/core/domain/host.py
git add tests/unit/core/test_host.py

# 7. verify what will be committed
git status

# 8. commit — pre-commit hooks fire automatically
git commit -m "feat(core): add Host domain model"

# 9. push — CI fires automatically on GitHub
git push
```

---

## Make commands

| Command | What it does |
|---|---|
| `make format` | fix formatting automatically |
| `make lint` | check code quality — ruff + bandit |
| `make type-check` | check types — mypy |
| `make test` | run tests with coverage |
| `make check` | run format + lint + type-check + test |
| `make docs` | serve documentation at localhost:9000 |
| `make clean` | remove generated files |

---

## Pre-commit checklist

Before every commit:

- [ ] `make lint` passes
- [ ] `make type-check` passes
- [ ] Tests written for new code
- [ ] Docstrings on all public functions and classes
- [ ] No hardcoded credentials or paths
- [ ] Subprocess calls use argument lists not shell strings
- [ ] New exceptions defined in `exceptions.py`
- [ ] Commit message follows conventional commits format

---

## Adding a dependency

```bash
# runtime dependency
uv add textual

# development dependency
uv add --dev pytest-mock
```

Always commit `pyproject.toml` and `uv.lock` together:

```bash
git add pyproject.toml uv.lock
git commit -m "chore(deps): add pytest-mock"
```

---

## Running the documentation site

```bash
make docs
# opens at http://127.0.0.1:9000
```

---

## Tagging a release

```bash
# bump version in pyproject.toml
# then tag
git tag v0.2.0
git push origin v0.2.0
# GitHub Actions builds and attaches the wheel automatically
```

---

## Installing from GitHub

```bash
# use it — no source code needed
uv tool install git+https://github.com/StrafeNDestroy/strafekit.git

# update to latest
uv tool upgrade strafekit
```
