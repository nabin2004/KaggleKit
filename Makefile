.PHONY: fmt lint mypy test all

all: fmt lint mypy test

fmt:
	uv run ruff format .
	uv run black .

lint:
	uv run ruff check . --fix

mypy:
	uv run mypy src

test:
	uv run pytest tests
