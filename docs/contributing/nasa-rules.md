# NASA Power of 10 Rules

1. Simple control flow — max 2 nesting levels, prefer early returns
2. Bounded loops — all external data loops have a documented limit
3. No dynamic allocation in hot paths
4. Function length — aim 30 lines, hard limit 60
5. Assertions and validation at every boundary
6. Minimal scope — variables declared close to use
7. Check all return values — never bare except
8. No macro equivalents — no eval, exec, setattr
9. Limit indirection — max 3 hops to find what runs
10. Zero tolerance — mypy strict, ruff clean, bandit clean
