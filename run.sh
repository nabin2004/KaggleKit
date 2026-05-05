#!/bin/sh
cd src

uv run python train.py --fold 0 --model rf
uv run python train.py --fold 1 --model rf
uv run python train.py --fold 2 --model rf
uv run python train.py --fold 3 --model rf
uv run python train.py --fold 4 --model rf
