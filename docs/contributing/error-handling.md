# Error Handling

## Hierarchy

```
StrafekitError
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

## Catching

```python
try:
    scan_and_save(host)
except ScanError as e:
    retry_scan(host)
except StorageError as e:
    alert_db_failure(e)
except StrafekitError as e:
    log.error("unexpected: %s", e)
```

## Chaining

```python
except FileNotFoundError as e:
    raise ToolNotFoundError("nmap not installed") from e
```
