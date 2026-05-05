from __future__ import annotations

import pandas as pd

import config


def feature_columns(df: pd.DataFrame) -> list[str]:
    exclude = {
        config.TARGET_COLUMN,
        *config.METADATA_COLUMNS,
        *config.DROP_FROM_FEATURES,
    }
    return [c for c in df.columns if c not in exclude]


def infer_numeric_and_categorical(
    df: pd.DataFrame, feature_cols: list[str]
) -> tuple[list[str], list[str]]:
    subset = df[feature_cols]
    numeric_cols = subset.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in feature_cols if c not in numeric_cols]
    return numeric_cols, categorical


def train_valid_arrays(
    df: pd.DataFrame, fold: int, target_column: str
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Train/validation feature matrices as DataFrames and target as Series."""
    fold_column = config.KFOLD_COLUMN
    df_train = df[df[fold_column] != fold].reset_index(drop=True)
    df_valid = df[df[fold_column] == fold].reset_index(drop=True)

    feats = feature_columns(df)
    x_train = df_train.loc[:, feats]
    x_valid = df_valid.loc[:, feats]
    y_train = df_train[target_column]
    y_valid = df_valid[target_column]
    return x_train, x_valid, y_train, y_valid
