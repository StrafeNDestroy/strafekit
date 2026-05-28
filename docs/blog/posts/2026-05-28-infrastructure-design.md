---
date: 2026-05-28 
authors:
  - strafendestroy
categories:
  - Infrastructure
---

# Industry Infrastructure
Upgrading my projects structure from zero to hero.



<!-- more -->

## Introduction
For a long time I had been making python projects here and there but never had the experience
of how to organize a project for not just myself but other contributors. Like many others 
I didn't design my programs, I just start coding. I had been fascinated with how python projects
on github looked so different and organzied compared to mine which normally just had a scripts
folder and maybe some libs. So I decided to learn how to set something up that might be on 
some industry teams. 

Good structure for a blog post or documentation page. Here's the expanded version with short sections for each:

---

Here's the full content with links embedded:

---

## Project Manager

I had originally wanted to use `pipx` but then learned of the modern [uv](https://docs.astral.sh/uv) Python
manager. It replaces several separate tools:

| Tool | Purpose | uv equivalent |
|---|---|---|
| `pip` | installing packages | `uv add` / `uv pip install` |
| `pipx` | installing global CLI tools | `uv tool install` |
| `venv` | creating virtual environments | `uv venv` / `uv sync` |
| `pip-tools` | generating lockfiles | `uv lock` / `uv sync` |
| `pyenv` | managing Python versions | `uv python install` |

uv is 10-100x faster than pip but honestly the main appeal was a single
tool instead of learning and maintaining five separate ones.

### Initializing a project

```bash
uv init --name strafekit
# creates:
#   pyproject.toml    ← project manifest
#   .python-version   ← pinned Python version
#   README.md         ← empty readme
#   hello.py          ← sample file (delete this)
```

### Creating the environment and lockfile

```bash
uv sync
# creates:
#   .venv/     ← virtual environment
#   uv.lock    ← exact pinned versions of every dependency
```

### Adding packages

Updates `pyproject.toml` and `uv.lock` automatically.

```bash
uv add textual sqlalchemy        # runtime dependencies
uv add --dev pytest mypy ruff    # development only
```

---

## Code Quality
Code quality tools find problems and enforce consistency before code is
committed.

### Linting — [ruff](https://docs.astral.sh/ruff)
Finds real code problems unused imports, undefined names, bad patterns,
naming convention violations. Reports issue and location to fix.
```bash
uv run ruff check strafekit/
```


### Formatting — [ruff](https://docs.astral.sh/ruff)
Enforces visual style indentation, quote style, line length,
bracket placement. Fixes automatically with no intervention.
```bash
uv run ruff format strafekit/
```

### Type checking — [mypy](https://mypy.readthedocs.io)
Verifies type annotations are correct without running the code. Catches type
errors at development time rather than runtime. As someone who came from `C` I
find it invaluable to explicit types. I would rather find out before runtime
than get a random type error during an engagement.  
```bash
uv run mypy strafekit/
```

---

## Code Security
Security tools catch vulnerabilities in your own code and your dependencies
before they reach production.

### Static analysis — [bandit](https://bandit.readthedocs.io)
```bash
uv run bandit -r strafekit/
```

### Dependency scanning — [safety](https://pypi.org/project/safety)
Checks every package in `uv.lock` against a database of known CVEs. Catches
vulnerable dependencies before they become a problem. Especially now that
packagemanagers are the target for large scale vulnerability distribution.
```bash
uv run safety check
```

---

## Documentation Generation
API Documentation is generated from docstrings pulled automatically from the source code. 
 

### Static site — [mkdocs](https://www.mkdocs.org)
Builds a complete HTML documentation website from markdown files. Handles
navigation, search, theming, and deployment to GitHub Pages.
```bash
uv run mkdocs serve           # local preview at localhost:9000
uv run mkdocs gh-deploy       # deploy to GitHub Pages
```

### Theme — [mkdocs-material](https://squidfunk.github.io/mkdocs-material)
The Material for MkDocs theme. Provides the dark theme, navigation tabs,
search, code highlighting, and mobile support.

### API reference — [mkdocstrings](https://mkdocstrings.github.io)
Reads Python docstrings from source code and renders them as API reference
pages automatically. Write the docstring once and it appears in both the code
and the documentation.
Here's the updated section:

---

### API reference — [mkdocstrings](https://mkdocstrings.github.io)

Reads Python docstrings from source code and renders them as API reference
pages automatically. Write the docstring once and it appears in both the code
and the documentation.

The `:::` calling convention maps directly to the Python import path.
If you can import it you can document it:

```python
# the import path
from strafekit.core.domain.enums import HostStatus

# the mkdocstrings path — identical
::: strafekit.core.domain.enums.HostStatus
```

You can document at different levels:

```markdown
# entire module — documents everything in the file
::: strafekit.core.domain.enums

# specific class
::: strafekit.core.domain.enums.HostStatus

# specific function
::: strafekit.core.domain.host.Host.is_alive
```

**Example — `docs/api/domain.md`:**

```markdown
# Domain Models

## Enums

::: strafekit.core.domain.enums

## Exceptions

::: strafekit.core.domain.exceptions
```

**The rendered output** mkdocstrings takes this docstring in your source:
```python
class HostStatus(Enum):
    """Reachability status of a discovered host."""

    ALIVE = "alive"
    DEAD = "dead"
    UNREACHABLE = "unreachable"
    UNKNOWN = "unknown"
```

And renders it in the docs site as:
```
HostStatus
──────────
Reachability status of a discovered host.

Members:
    ALIVE         "alive"
    DEAD          "dead"
    UNREACHABLE   "unreachable"
    UNKNOWN       "unknown"
```
As you add classes and docstrings to your source the API docs
update automatically on the next deploy with no changes to the
markdown file needed.



### Docstring coverage — [interrogate](https://interrogate.readthedocs.io)
Measures what percentage of public functions and classes have docstrings.
Fails the build if coverage drops below the configured threshold.
```bash
uv run interrogate strafekit/
```

---

## Testing
Testing tools verify the code works correctly and measure how much of it
is actually exercised by tests.

### Test runner — [pytest](https://docs.pytest.org)
Finds and runs all test files. Reports which tests pass, which fail, and
why. The testing levels are unit, integration, and end to end.
```bash
uv run pytest
```

### Async support — [pytest-asyncio](https://pytest-asyncio.readthedocs.io)
Allows writing async test functions naturally. Required because StrafeKit
uses asyncio and Textual throughout.
```python
async def test_scan_host() -> None:
    result = await scan_host(Host(ip="10.10.10.5"))
    assert result is not None
```

### Coverage — [pytest-cov](https://pytest-cov.readthedocs.io)
Measures what percentage of source code is executed during tests. Generates
reports showing exactly which lines were never hit by any test.
```bash
uv run pytest --cov=strafekit --cov-report=term-missing
```

### Mocking — [pytest-mock](https://pytest-mock.readthedocs.io)
Replaces real dependencies with fakes during testing. Allows testing business
logic without a real database, real tools, or real network access.

### Parallel execution — [pytest-xdist](https://pytest-xdist.readthedocs.io)
Runs tests across multiple CPU cores simultaneously. Reduces test suite
run time significantly as the suite grows.

---

## Standards Enforcement
Standards enforcement tools ensure consistent practices such as
formatting,linting, security checks are followed on
every commit — automatically, without relying on memory or discipline.

### Pre-commit hooks — [pre-commit](https://pre-commit.com)
Runs a configured set of checks before every `git commit`. If any check
fails the commit is blocked until the issue is fixed. Catches problems
before they ever enter git history.
```bash
uv run pre-commit install
```

Runs on every commit: ruff lint, ruff format check, trailing whitespace,
end of file newline, YAML validation, TOML validation, private key detection.

### Commit messages — [commitizen](https://commitizen-tools.github.io/commitizen)
Enforces conventional commit message format on every commit. Invalid
messages are rejected before the commit completes. As with error when possible 
I like to be explicit in my commits, makes auditing much easier.  

```
feat(core): add Host domain model
fix(creds): handle duplicate entries
scan(nmap): add async wrapper
```

---
## CI/CD Pipline
The CI/CD pipeline runs the full quality suite automatically on every push
to GitHub. Should any of the tests fail the project does not get pushed to the repo. 

## CI workflow — quality checks:
```bash
yamlFormat check  → ruff format --check
Lint          → ruff check
Security      → bandit
Type check    → mypy
Test          → pytest --cov
```

## Docs workflow — documentation deployment:
This workflow allows me to automaticall deploy and update my program documentaion/blog to a 
static website hosted on github. Having browser based documentaion that is navigable 
is a huge plus for any future contributors.  
```bash
yamlBuild docs    → mkdocs build
Deploy        → mkdocs gh-deploy → gh-pages branch → GitHub Pages
```




## Packaging
Packaging tools turn your source code into something others can install
and use without needing the source.

### Build system — [hatchling](https://hatch.pypa.io/latest)
Packages StrafeKit into a distributable wheel file. Reads `pyproject.toml`
to know what to include and how to build it.
```bash
uv build
# creates dist/strafekit-0.1.0-py3-none-any.whl
```

### Distribution — [uv](https://docs.astral.sh/uv)
Anyone can install StrafeKit directly from GitHub without cloning:
```bash
uv tool install git+https://github.com/StrafeNDestroy/strafekit.git
strafekit
```
