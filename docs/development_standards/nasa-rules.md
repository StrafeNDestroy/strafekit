# NASA Power of 10 Rules

Originally written by Gerard Holzmann at NASA/JPL for safety-critical systems.
Adapted here for Python and security tooling.

These rules exist because the cost of failure matters.
For NASA — spacecraft. For StrafeKit — engagement integrity.

---

## Rule 1 — Simple control flow

- No deeply nested conditions — maximum 2 levels before extracting a function
- Prefer early returns over nested if/else
- No complex one-liner comprehensions that sacrifice readability
- Control flow should be obvious and traceable

```python
# wrong — deeply nested
def process_host(host):
    if host:
        if host.is_alive():
            if host.has_services():
                for service in host.services:
                    if service.is_vulnerable():
                        report(service)

# right — early returns, flat structure
def process_host(host):
    if not host:
        return
    if not host.is_alive():
        return
    if not host.has_services():
        return
    for service in host.services:
        if service.is_vulnerable():
            report(service)
```

---

## Rule 2 — Bounded loops

- All loops over external or user-supplied data must have a maximum iteration bound
- Unbounded loops over network data are never acceptable
- Document the bound and why it was chosen

```python
# wrong — unbounded
for host in external_hosts:
    scan(host)

# right — bounded with documented reason
MAX_HOSTS = 1024  # reasonable upper limit for a single engagement
for i, host in enumerate(external_hosts):
    if i >= MAX_HOSTS:
        logger.warning("Host limit reached, truncating at %d", MAX_HOSTS)
        break
    scan(host)
```

---

## Rule 3 — No dynamic allocation in hot paths

- Initialize data structures at startup, not inside loops
- Pre-allocate result containers before scanning begins
- Avoid creating large objects repeatedly inside tight loops

```python
# wrong — allocating inside the loop
def scan_network(hosts: list[Host]) -> list[ScanResult]:
    for host in hosts:
        results = []          # re-allocated every iteration
        results.append(scan(host))
    return results

# right — allocate once before the loop
def scan_network(hosts: list[Host]) -> list[ScanResult]:
    results: list[ScanResult] = []    # allocated once
    for host in hosts:
        results.append(scan(host))
    return results
```

---

## Rule 4 — Function length

- Aim for under 30 lines — ideal, no questions asked
- 30 to 60 lines — acceptable, question whether it can be split
- Over 60 lines — hard limit, requires explicit justification comment
- Beyond 60 lines almost always means the function has multiple responsibilities

```python
# if you must exceed 60 lines, document why
def build_engagement_report(engagement: Engagement) -> str:
    # NOTE: exceeds 30 line guideline because report generation requires
    # assembling all sections in sequence. Splitting would obscure the
    # report structure. Each section has a single responsibility.
    ...
```

---

## Rule 5 — Assertions and validation

- Validate all inputs at the boundary of your system
- Use assertions for internal invariants that must always be true
- Never assume external data is well-formed
- Minimum one validation check per public function

```python
def scan_host(host: Host, ports: str) -> ScanResult:
    if not host.ip:
        raise RequiredFieldError("ip")
    if not ports:
        raise RequiredFieldError("ports")
    # internal invariant — should never happen if callers are correct
    assert host.engagement_id > 0, "host must belong to an engagement"
    ...
```

---

## Rule 6 — Minimal scope

- Declare variables as close to their use as possible
- No module-level mutable state unless absolutely necessary
- Avoid global variables — pass state explicitly through function arguments

```python
# wrong — variable declared far from use
def process():
    result = None
    data = load_data()
    processed = transform(data)
    filtered = filter_results(processed)
    result = filtered
    return result

# right — declared at point of use
def process():
    data = load_data()
    processed = transform(data)
    return filter_results(processed)
```

---

## Rule 7 — Check all return values

- Never ignore return values
- Never use bare except — always catch specific exceptions
- Always handle or explicitly re-raise exceptions
- Document what exceptions a function can raise

```python
# wrong — ignoring return value
scan_host(host)

# wrong — bare except, silent failure
try:
    result = scan_host(host)
except:
    pass

# right — specific exception, explicit handling
try:
    result = scan_host(host)
except ScanError as e:
    logger.error("Scan failed for %s: %s", host.ip, e)
    raise
except TimeoutError as e:
    logger.warning("Scan timed out for %s", host.ip)
    return ScanResult.empty(host)
```

---

## Rule 8 — No macro equivalents

- No monkey patching
- No dynamic attribute setting with `setattr` unless explicitly justified
- No `eval`, no `exec`
- No `importlib` dynamic imports outside the plugin system

```python
# wrong
setattr(host, field_name, value)    # dynamic attribute — avoid
eval(user_input)                    # never

# right — explicit attribute access
host.hostname = value
```

---

## Rule 9 — Limit indirection

- Maximum one level of abstraction per function call
- Avoid chains of wrappers that obscure what actually happens
- If tracing execution requires more than 3 hops — simplify

```python
# wrong — too many hops to find what actually runs
def scan(host):
    return _do_scan(host)

def _do_scan(host):
    return _run_scanner(host)

def _run_scanner(host):
    return _execute(host)       # what actually happens is buried 3 levels deep

# right — clear and direct
def scan(host: Host) -> ScanResult:
    return self.executor.run_nmap(host)    # one hop, clear what happens
```

---

## Rule 10 — Zero tolerance

- Mypy strict mode — zero type errors accepted
- Ruff — zero lint warnings accepted
- Bandit — zero unreviewed security findings
- Pre-commit must pass before every commit
- CI must pass before merging to main

```bash
# these must all pass before pushing
make lint
make type-check
make test
```
