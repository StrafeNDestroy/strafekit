# Error Handling

StrafeKit uses a structured exception hierarchy.
All exceptions live in `strafekit/core/domain/exceptions.py`.

---

## The exception hierarchy

```
Exception                       ← Python built-in root
    └── StrafekitError          ← catches any StrafeKit error
            ├── CredentialError
            ├── EngagementError
            ├── ScanError
            ├── SecretError
            ├── StorageError
            ├── ToolNotFoundError
            └── ValidationError
                    ├── InvalidFieldError
                    └── RequiredFieldError
```

The base `StrafekitError` catches all children.
Specific exceptions give targeted handling.

---

## Pattern — one base, children inherit

```python
# exceptions.py
class StrafekitError(Exception):
    """Base exception for all StrafeKit errors."""
    pass

class ScanError(StrafekitError):
    """Raised when a scan fails to complete."""
    pass

class ValidationError(StrafekitError):
    """Raised when input validation fails."""
    pass

class RequiredFieldError(ValidationError):
    """Raised when a required field is missing or empty."""
    pass
```

---

## Raising exceptions

Always include a descriptive message. Never raise generic `Exception`.

```python
# wrong
raise Exception("something went wrong")

# right
raise ScanError(f"nmap failed on {host.ip}: {e}")
raise RequiredFieldError("ip")
raise ToolNotFoundError("nmap is not installed")
```

---

## Catching exceptions

Specific exceptions before broad ones. Never use bare `except`.

```python
# wrong — bare except, silent failure
try:
    scan_host(host)
except:
    pass

# right — specific first, broad as fallback
try:
    scan_and_save(host)
except ScanError as e:
    log.error("scan failed: %s", e)
    retry_scan(host)
except StorageError as e:
    log.error("database failed: %s", e)
except StrafekitError as e:
    log.error("unexpected error: %s", e)
```

---

## Chaining exceptions

Preserve the original cause when wrapping exceptions:

```python
try:
    subprocess.run(["nmap", host.ip], check=True)
except FileNotFoundError as e:
    raise ToolNotFoundError("nmap is not installed") from e
#                                                    ↑
#                           preserves original FileNotFoundError as context
```

---

## The `finally` clause — cleanup

`finally` always runs regardless of whether an exception occurred:

```python
def save_results(host: Host) -> None:
    db = open_database()
    try:
        result = scan_host(host)
        db.save(result)
    except ScanError as e:
        log.error("scan failed: %s", e)
    finally:
        db.close()    # always runs — connection never leaks
```

---

## Rules

- Never raise generic `Exception` — always a specific type
- Never use bare `except:` — always catch specific types
- Never ignore exceptions silently — always handle or re-raise
- Specific exceptions before broad ones in except blocks
- Use `raise X from e` to chain and preserve original cause
- Always include a message when raising
- Add new exceptions to `exceptions.py` — never define them inline
