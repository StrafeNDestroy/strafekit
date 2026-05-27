# Security Rules

- Never hardcode credentials or API keys
- Never use `shell=True` without justification
- Always use `Path()` not string concatenation
- Validate all external input at boundaries
- Store secrets in OS keyring

```python
# wrong
subprocess.run(f"nmap {target}", shell=True)

# right
subprocess.run(["nmap", target], capture_output=True)
```
