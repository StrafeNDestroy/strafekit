# Workflow

## Setup

```bash
git clone https://github.com/StrafeNDestroy/strafekit.git
cd strafekit
uv sync
source .venv/bin/activate
```

## Daily

```bash
make lint          # check before committing
make type-check    # check types
make test          # run tests
make check         # run everything
make docs          # serve docs at :9000
```

## Adding dependencies

```bash
uv add textual
uv add --dev pytest-mock
git add pyproject.toml uv.lock
git commit -m "chore(deps): add pytest-mock"
```

## Install from GitHub

```bash
uv tool install git+https://github.com/StrafeNDestroy/strafekit.git
uv tool upgrade strafekit
```
