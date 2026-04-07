# SwissKit (Kagglebase)

A robust, structural machine learning boilerplate for Kaggle competitions and fast experimentation. It features automated fold generation, dynamic model dispatching, training pipelines, and a lightweight FastAPI-based serving layer.

## Project Structure

- `input/`: Datasets (e.g., CSV files).
- `src/`: Core Python source files (`train.py`, `config.py`, `model_dispatcher.py`).
- `models/`: Saved model artifacts.
- `notebook/`: Jupyter notebooks for exploratory data analysis (EDA).
- `server.py`: FastAPI server skeleton for exposing models.

## Setup

Ensure you have Python 3.11+ installed. Install dependencies using your preferred package manager (e.g., `uv`, `pip`):

```bash
uv pip install -e .
```
*(Dependencies are defined in `pyproject.toml`)*

## Usage

1. **Configure Parameters**: Update file paths in `src/config.py`.
2. **Train a Model**: Run the training script specifying the fold and model.

```bash
cd src
python train.py --fold 0 --model rf
```

Valid models (defined in `src/model_dispatcher.py`):
- `decision_tree_gini`
- `decision_tree_entropy`
- `rf` (Random Forest)
- `log_reg`
- `line_reg`

## Note to AI Agents
AI assistants and automated coding agents should refer to `agents.md` for specific architectural guidelines and commands to follow in this workspace.
