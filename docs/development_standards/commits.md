# Commit Messages

Conventional commits format enforced automatically by commitizen.
Invalid messages are rejected before the commit completes.

---

## Format
type(scope): short description
blog(post): add infrastructure setup post
chore(deps): update textual to latest
creds(sqlite): add domain filtering query
docs(api): add docstrings to Host model
feat(scan): add async nmap wrapper
fix(creds): handle duplicate domain entries
scan(nmap): add service version detection
test(spray): add unit tests for password spray

---

## All types

| Type | When to use |
|---|---|
| `blog` | blog posts and writing |
| `build` | build system changes |
| `chore` | dependency updates, config changes |
| `ci` | CI/CD pipeline changes |
| `creds` | credential management — storage, spray logic, hash handling |
| `docs` | documentation only |
| `feat` | new feature |
| `fix` | bug fix |
| `perf` | performance improvement |
| `refactor` | code change, no bug fix or feature |
| `revert` | reverting a previous commit |
| `scan` | scanning infrastructure — nmap, gobuster, masscan wrappers |
| `style` | formatting changes, no logic change |
| `test` | adding or updating tests |

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
```

