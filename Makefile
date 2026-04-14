# Put user-local bins first so a freshly installed uv is visible in the same session.
export PATH := $(HOME)/.local/bin:$(PATH)

UV_INSTALL_URL := https://astral.sh/uv/install.sh

FOLD ?= 0
MODEL ?= rf

.PHONY: ensure-uv sync fmt lint mypy test all train train-all

all: fmt lint mypy test

# Install uv if it is not already available (writes to ~/.local/bin by default).
ensure-uv:
	@command -v uv >/dev/null 2>&1 || { \
		echo "uv not found; installing from $(UV_INSTALL_URL) ..."; \
		curl -LsSf $(UV_INSTALL_URL) | sh; \
	}
	@command -v uv >/dev/null 2>&1 || { \
		echo "error: uv is still not on PATH. Add $(HOME)/.local/bin to PATH and retry."; \
		exit 1; \
	}

sync: ensure-uv
	uv sync --all-groups

fmt: ensure-uv
	uv run ruff format .
	uv run black .

lint: ensure-uv
	uv run ruff check . --fix

mypy: ensure-uv
	uv run mypy src

test: ensure-uv
	uv run pytest tests

# Train one fold (override: make train FOLD=2 MODEL=log_reg).
train: ensure-uv
	cd src && uv run python train.py --fold $(FOLD) --model $(MODEL)

# Train folds 0–4 with the same model (override MODEL=...).
train-all: ensure-uv
	cd src && for fold in 0 1 2 3 4; do \
		uv run python train.py --fold $$fold --model $(MODEL); \
	done
