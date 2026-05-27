.PHONY: test lint type-check docs clean check format

format:
	uv run ruff format strafekit/

lint:
	uv run ruff format --check strafekit/
	uv run ruff check strafekit/
	uv run bandit -r strafekit/

type-check:
	uv run mypy strafekit/

test:
	uv run pytest --cov=strafekit --cov-report=term-missing

docs:
	uv run mkdocs serve --dev-addr 127.0.0.1:9000

check: format lint type-check test
	@echo "All checks passed"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	rm -rf site/ dist/ build/
