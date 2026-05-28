# Commit Messages

Conventional commits format enforced automatically by commitizen.
Invalid messages are rejected before the commit completes.

---

## Format

```
type(scope): short description
```

```
feat(scan): add async nmap wrapper
fix(creds): handle duplicate domain entries
docs(api): add docstrings to Host model
test(spray): add unit tests for password spray
scan(nmap): add service version detection
creds(sqlite): add domain filtering query
chore(deps): update textual to latest
```

---

## Standard types

| Type | When to use |
|---|---|
| `feat` | new feature |
| `fix` | bug fix |
| `docs` | documentation only |
| `test` | adding or updating tests |
| `refactor` | code change, no bug fix or feature |
| `chore` | dependency updates, config changes |
| `perf` | performance improvement |
| `ci` | CI/CD pipeline changes |
| `build` | build system changes |
| `style` | formatting changes, no logic change |
| `revert` | reverting a previous commit |

---

## StrafeKit domain types

| Type | When to use |
|---|---|
| `scan` | scanning infrastructure — nmap, masscan, gobuster wrappers and scan logic |
| `creds` | credential management — storage, spray logic, hash handling, export |

---

## Rules

- Type is required
- Scope is optional but recommended — use the component name
- Description is required, lowercase, no period at end
- No ticket numbers in the message — use the commit body for that
- Keep description under 72 characters

---

## Multi-line commits

For significant changes add a body explaining why:

```
feat(scan): add async nmap wrapper

Previously ServiceScan blocked the UI thread while nmap ran.
This wraps nmap in asyncio.create_subprocess_exec so the UI
stays responsive during long scans. Results stream line by line
into the hosts panel via message passing.

Closes #14
```

---

## Breaking changes

Add `!` after the type and a footer:

```
feat(db)!: migrate credential storage to SQLCipher

BREAKING CHANGE: existing engagement databases must be re-imported.
Run `strafekit migrate --engagement corp-pentest-05` to convert.
```
