# Security Rules

Non-negotiable requirements for a penetration testing framework.
StrafeKit handles sensitive engagement data — these rules protect it.

---

## Credentials and secrets

- Never hardcode credentials, tokens, or API keys in source code
- Never commit `.env` files or `user.toml` to version control
- Store API keys in the OS keyring via `KeyringSecretStore`
- Store engagement database encryption key in the OS keyring

```python
# wrong — hardcoded credential
SHODAN_API_KEY = "abc123xyz"

# right — read from keyring at runtime
api_key = secret_store.get_secret("shodan_api_key")
```

---

## Subprocess calls

Never use `shell=True` without explicit justification in a comment.
Always use explicit argument lists — never shell strings.

```python
# wrong — shell injection possible
subprocess.run(f"nmap {target}", shell=True)
subprocess.run("nmap " + target, shell=True)

# right — explicit argument list, no shell injection possible
subprocess.run(["nmap", target], capture_output=True)
subprocess.run(["nmap", "-sV", "-sC", host.ip], capture_output=True)
```

---

## File paths

Always use `Path()` — never string concatenation.
Always validate that paths stay within the engagement directory.

```python
# wrong — path traversal possible
open(f"/engagements/{user_input}/results.txt")
path = "/engagements/" + engagement_name + "/results.txt"

# right — Path validates and resolves
engagement_path = Path("/engagements") / engagement_name
results_file = engagement_path / "results.txt"

# validate path stays within engagements directory
results_file.resolve().relative_to(Path("/engagements"))
```

---

## Input validation

Always validate external input at the boundary of your system.
External input includes: user input, database reads, API responses, file contents.

```python
# validate at the boundary — __post_init__ on dataclasses
@dataclass
class Host:
    ip: str
    engagement_id: int

    def __post_init__(self) -> None:
        if not self.ip:
            raise RequiredFieldError("ip")
        if not self.engagement_id:
            raise RequiredFieldError("engagement_id")
```

---

## Audit logging

All credential operations must be logged through the audit log.
Who accessed what credential, when, and from where.

```python
# every credential read/write goes through audit log
credential_store.save(credential)      # logged
credential_store.find_by_domain(domain)  # logged
```

---

## Database encryption

Engagement databases are encrypted at rest using SQLCipher.
The encryption key lives in the OS keyring — never on disk as plaintext.

```python
# connection always uses key from keyring
key = secret_store.get_secret("engagement_db_key")
engine = create_engine(f"sqlite+pysqlcipher://:{key}@/engagement.db")
```

---

## Summary checklist

- [ ] No hardcoded credentials or API keys
- [ ] No `shell=True` without justification comment
- [ ] All paths use `Path()` and stay within engagement directory
- [ ] All external input validated at boundaries
- [ ] All credential operations logged
- [ ] Secrets stored in OS keyring not plaintext files
