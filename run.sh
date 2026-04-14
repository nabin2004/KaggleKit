#!/bin/sh
cd src

uv run python train.py --fold 0
uv run python train.py --fold 1
uv run python train.py --fold 2
uv run python train.py --fold 3
uv run python train.py --fold 4
