# SwissKit (Kagglebase)

A robust, structural machine learning boilerplate for Kaggle competitions and fast experimentation. It features automated fold generation, dynamic model dispatching, training pipelines, and a lightweight FastAPI-based serving layer.

## Project Structure

- `input/`: Datasets (e.g., CSV files).
- `src/`: Core Python source files (`train.py`, `config.py`, `model_dispatcher.py`).
- `models/`: Saved model artifacts.
- `notebook/`: Jupyter notebooks for exploratory data analysis (EDA).
- `server.py`: FastAPI server skeleton for exposing models.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/). This repository standardizes on uv (not hand-maintained `requirements.txt` or ad hoc `pip install` workflows).

From the repository root, create the virtual environment and install dependencies from the lockfile:

```bash
uv sync
```

That installs runtime dependencies from `pyproject.toml` / `uv.lock` into `.venv/`. For local development (formatters, linters, tests, pre-commit), include the `dev` dependency group:

```bash
uv sync --all-groups
```

Run tools and scripts through uv so they use that environment (for example `uv run python …`, `uv run pytest`, or the `Makefile` targets, which call `uv run`).

The Makefile installs uv automatically if it is missing (via the official install script; requires `curl`). Discover targets anytime with:

```bash
make help          # default goal: lists targets and tips
make preview       # show FOLD/MODEL/FOLDS and the exact train command line
make -n train      # print the train recipe without executing (GNU Make dry run)
```

Sync everything including dev tools with:

```bash
make sync
```

Reproducible installs (fail if `uv.lock` is out of date): `make sync LOCKED=1`. Runtime-only (no dev groups): `make sync-prod`.

CI-style checks without modifying files: `make check` (format/lint check + mypy + tests). Local auto-fix pipeline: `make all`. API preview: `make serve` (uvicorn with reload on port 8000). Clear tool caches: `make clean-cache`.

Commit `uv.lock` when you change dependencies. Add or upgrade packages with `uv add <package>` or `uv add --dev <package>` rather than editing lock metadata by hand.

## Usage

1. **Configure Parameters**: Update file paths in `src/config.py`.
2. **Train a Model**: Run the training script specifying the fold and model.

```bash
cd src
uv run python train.py --fold 0 --model rf
```

From the repository root you can use Make (it ensures `uv` exists, then runs training in `src/`):

```bash
make train                  # default: fold 0, model rf
make train FOLD=2 MODEL=log_reg
make train-all              # folds 0–4, same MODEL (default rf)
make train-all FOLDS="0 1 2" MODEL=rf   # custom fold list
```

Valid models (defined in `src/model_dispatcher.py`):
- `decision_tree_gini`
- `decision_tree_entropy`
- `rf` (Random Forest)
- `log_reg`
- `line_reg`

## Note to AI Agents
AI assistants and automated coding agents should refer to `agents.md` for specific architectural guidelines and commands to follow in this workspace.
