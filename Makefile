# =============================================================================
# SwissKit — Makefile (uv-first, CI-friendly)
# =============================================================================
#  Default goal: help. Preview commands: make -n <target>  or  make preview
# =============================================================================

MAKEFLAGS += --no-print-directory

SHELL := bash
.SHELLFLAGS := -eo pipefail -c

.DELETE_ON_ERROR:

export PATH := $(HOME)/.local/bin:$(abspath $(CURDIR)/.venv/bin):$(PATH)

UV_INSTALL_URL ?= https://astral.sh/uv/install.sh

FOLD ?= 0
MODEL ?= rf
FOLDS ?= 0 1 2 3 4

LOCKED ?=
_UV_SYNC_FLAGS := $(if $(filter 1,$(LOCKED)),--frozen --locked,)

.PHONY: default help preview vars doctor
.PHONY: ensure-uv sync sync-prod
.PHONY: fmt fmt-check lint lint-check mypy test all check
.PHONY: clean clean-cache validate-train validate-model train train-all serve

default: help

# -----------------------------------------------------------------------------
# Help & preview (targets below use "name: ## description" with no prereqs)
# -----------------------------------------------------------------------------

help: ## List targets (default goal); use "make -n train" to preview shell commands
	@echo ""
	@echo "SwissKit — targets"
	@echo "------------------"
	@grep -hE '^[a-z][a-z0-9_.-]*: ## ' $(MAKEFILE_LIST) \
		| awk -F': ## ' '{printf "  %-22s %s\n", $$1, $$2}' | LC_ALL=C sort -k1,1 -b
	@echo ""
	@echo "Composition:"
	@echo "  all                  fmt → lint → mypy → test (may modify files)"
	@echo "  check                fmt-check → lint-check → mypy → test (CI-safe)"
	@echo "Tips:  make preview     show vars + train command line"
	@echo "       make -n train     print recipe without running"
	@echo "       make sync LOCKED=1    sync with --frozen --locked"
	@echo ""

preview: vars ## Show variables and exact train command (does not run training)
	@echo ""
	@echo "Single-fold train:"
	@echo "  cd src && uv run python train.py --fold $(FOLD) --model $(MODEL)"
	@echo ""
	@echo "train-all uses MODEL=$(MODEL) for folds: $(FOLDS)"
	@echo ""

vars: ## Print repo path, training vars, and uv/Python when available
	@echo "REPO:      $(CURDIR)"
	@echo "FOLD:      $(FOLD)"
	@echo "MODEL:     $(MODEL)"
	@echo "FOLDS:     $(FOLDS)"
	@echo "LOCKED:    $(LOCKED)"
	@echo "uv:        $$(command -v uv 2>/dev/null || echo '(not on PATH)')"
	@command -v uv >/dev/null 2>&1 && uv --version || true
	@command -v uv >/dev/null 2>&1 && uv run python -V 2>/dev/null || true

doctor: ## Verify uv and import sklearn in the project environment
	@$(MAKE) --no-print-directory ensure-uv
	uv --version
	uv run python -V
	uv run python -c "import sklearn; print('sklearn:', sklearn.__version__)"

# -----------------------------------------------------------------------------
# Toolchain bootstrap & sync
# -----------------------------------------------------------------------------

ensure-uv: ## Install uv via official script if missing (requires curl)
	@export PATH="$(HOME)/.local/bin:$(abspath $(CURDIR)/.venv/bin):$$PATH"; \
	if command -v uv >/dev/null 2>&1; then \
		exit 0; \
	fi; \
	command -v curl >/dev/null 2>&1 || { echo "error: curl is required to install uv" >&2; exit 1; }; \
	echo "uv not found; installing from $(UV_INSTALL_URL) ..."; \
	curl -LsSf "$(UV_INSTALL_URL)" | sh; \
	command -v uv >/dev/null 2>&1 || { \
		echo "error: uv is still not on PATH. export PATH=\"$$HOME/.local/bin:$$PATH\"" >&2; \
		exit 1; \
	}

sync: ## Sync runtime + dev groups (set LOCKED=1 for --frozen --locked)
	@$(MAKE) --no-print-directory ensure-uv
	uv sync --all-groups $(_UV_SYNC_FLAGS)

sync-prod: ## Sync runtime only (--no-dev); optional LOCKED=1
	@$(MAKE) --no-print-directory ensure-uv
	uv sync --no-dev $(_UV_SYNC_FLAGS)

# -----------------------------------------------------------------------------
# Quality
# -----------------------------------------------------------------------------

fmt: ## Format with Ruff and Black
	@$(MAKE) --no-print-directory ensure-uv
	uv run ruff format .
	uv run black .

fmt-check: ## Check formatting (no writes)
	@$(MAKE) --no-print-directory ensure-uv
	uv run ruff format --check .
	uv run black --check .

lint: ## Lint with Ruff (auto-fix where safe)
	@$(MAKE) --no-print-directory ensure-uv
	uv run ruff check . --fix

lint-check: ## Lint with Ruff (no fixes; CI-style)
	@$(MAKE) --no-print-directory ensure-uv
	uv run ruff check .

mypy: ## Type-check src/
	@$(MAKE) --no-print-directory ensure-uv
	uv run mypy src

test: ## Run tests
	@$(MAKE) --no-print-directory ensure-uv
	uv run pytest tests

all: fmt lint mypy test

check: fmt-check lint-check mypy test

# -----------------------------------------------------------------------------
# Training
# -----------------------------------------------------------------------------

validate-train: ## Validate FOLD/MODEL for single-fold training
	@test -n "$(strip $(FOLD))" || { echo "error: FOLD is empty" >&2; exit 1; }
	@test -n "$(strip $(MODEL))" || { echo "error: MODEL is empty" >&2; exit 1; }
	@if ! printf '%s' "$(FOLD)" | grep -Eq '^[0-9]+$$'; then \
		echo "error: FOLD must be a non-negative integer (got: $(FOLD))" >&2; \
		exit 1; \
	fi

validate-model: ## Validate MODEL is set (for train-all)
	@test -n "$(strip $(MODEL))" || { echo "error: MODEL is empty" >&2; exit 1; }

train: ## Train one fold (FOLD=0 MODEL=rf by default)
	@$(MAKE) --no-print-directory ensure-uv
	@$(MAKE) --no-print-directory validate-train
	cd src && uv run python train.py --fold $(FOLD) --model $(MODEL)

train-all: ## Train each fold in FOLDS with MODEL (default folds 0–4)
	@$(MAKE) --no-print-directory ensure-uv
	@$(MAKE) --no-print-directory validate-model
	cd src && for fold in $(FOLDS); do \
		uv run python train.py --fold $$fold --model $(MODEL); \
	done

# -----------------------------------------------------------------------------
# App & maintenance
# -----------------------------------------------------------------------------

serve: ## Run FastAPI with uvicorn --reload on 127.0.0.1:8000
	@$(MAKE) --no-print-directory ensure-uv
	uv run uvicorn server:app --host 127.0.0.1 --port 8000 --reload

clean-cache: ## Remove __pycache__ and tool caches (keeps .venv)
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage 2>/dev/null || true

clean: ## Remove caches (runs clean-cache; extend later for other artifacts)
	@$(MAKE) --no-print-directory clean-cache
