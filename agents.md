# Agent Instructions for SwissKit (Kagglebase)

This file contains the context and guidelines for AI agents working on this codebase.

## 1. Project Overview
**Name**: SwissKit (also referred to as Kagglebase)
**Description**: A structured and scalable machine learning project skeleton, primarily designed for tabular data, cross-validation, and quick algorithm testing. It includes a basic FastAPI server for deployment.
**Language**: Python >= 3.11
**Core Dependencies**: `scikit-learn`, `pandas`, `joblib`, `fastapi`

## 2. Directory Structure
- `input/`: Directory for raw and processed datasets (e.g., CSV files containing folds).
- `models/`: Directory where trained model artifacts (.bin files) are saved.
- `notebook/`: Jupyter notebooks for data exploration and sanity checks.
- `src/`: Contains all production source code.
  - `config.py`: Hardcoded paths and global configuration variables.
  - `create_folds.py`: Script to generate cross-validation folds from raw data.
  - `model_dispatcher.py`: A dictionary mapping string names to instantiated Scikit-Learn models.
  - `train.py`: The main training script that loads data, trains a specified model on a specific fold, evaluates it, and saves the model.
  - `inference.py`: Script for loading a saved model and generating predictions.
  - `models.py`: Custom PyTorch or advanced model architectures (if applicable).
- `main.py` / `server.py`: Entry points for the application, including a skeleton FastAPI server.
- `run.sh`: Bash script to execute training across multiple folds.

## 3. Workflows and Standard Procedures

### Adding a New Model
1. Open `src/model_dispatcher.py`.
2. Import the required class from `sklearn` (or other libraries like `xgboost`, `lightgbm`).
3. Add a new key-value pair to the `models` dictionary, where the key is the string argument passed from the command line, and the value is the instantiated model object.

### Training a Model
To run training, use the `train.py` script from inside the `src` directory (with `uv run` so the project environment is used):
```bash
cd src
uv run python train.py --fold <fold_number> --model <model_name>
```
Alternatively, `run.sh` can be executed to train across multiple folds. Note: ensure `run.sh` specifies the `--model` argument if updated.

### Environment and dependencies
- Use **uv** only: sync with `uv sync` (add `--all-groups` when you need dev tools such as Ruff, Black, Mypy, and Pytest).
- Declare packages in `pyproject.toml`; refresh the lockfile with `uv lock` after edits, or use `uv add <pkg>` / `uv add --group dev <pkg>` so `uv.lock` stays consistent.
- Run Python and CLIs with `uv run …` (or the `Makefile`, which wraps `uv run`) so the correct `.venv` is used.

## 4. Coding Standards & Quality Tools
- **Ruff**: Primary linter and automated fixer. Run matching scripts via `Makefile`.
- **Black**: Standard formatter for Python code.
- **Mypy**: Static type checking to ensure type safety.
- **Pytest**: Used for unit and integration testing.

### Quality Workflow
Use the provided `Makefile` to maintain high code standards (default goal is `make help`; recipes install uv via the official script when it is missing):
```bash
make help       # list targets and usage tips
make preview    # print training variables and command line (no training run)
make sync       # uv sync --all-groups (use LOCKED=1 for --frozen --locked)
make sync-prod  # runtime dependencies only (--no-dev)
make fmt / make lint   # may modify files (Ruff + Black)
make fmt-check / make lint-check   # no writes (CI-style)
make mypy
make test
make check      # fmt-check + lint-check + mypy + test (preferred for CI)
make all        # fmt + lint + mypy + test (local pipeline with auto-fix)
make train      # default FOLD=0 MODEL=rf
make train-all  # folds in FOLDS (default 0–4), same MODEL
make serve      # uvicorn with reload (local API)
make doctor     # sanity-check uv + sklearn in the venv
make clean-cache
```
Use `make -n <target>` to preview shell commands without running them.
- Follow standard PEP 8 naming conventions.
- Keep the `config.py` as the single source of truth for file paths; avoid hardcoding relative paths directly into worker scripts.
- Every new script interacting with data or models must support running from the command line with `argparse`.
- Maintain modularity: data processing, model definition, training, and inference should remain separated.

## 5. Security & Best Practices
- Never commit actual data files inside the `input/` directory to version control (ensure `.gitignore` ignores `input/*.csv`).
- Never commit trained models inside the `models/` directory to version control.
- Ensure all PRs pass `make check` before being merged (non-destructive). Use `make all` locally when you intend Ruff/Black auto-fixes.
