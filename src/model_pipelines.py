from __future__ import annotations

from collections.abc import Sequence

from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def build_rf_pipeline(
    classifier: BaseEstimator,
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
) -> Pipeline:
    transformers: list[tuple[str, Pipeline, Sequence[str]]] = []
    if numeric_features:
        num_pipe = Pipeline(
            steps=[("imputer", SimpleImputer(strategy="median"))],
        )
        transformers.append(("num", num_pipe, list(numeric_features)))
    if categorical_features:
        cat_pipe = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "ohe",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        sparse_output=False,
                    ),
                ),
            ],
        )
        transformers.append(("cat", cat_pipe, list(categorical_features)))

    preprocessor = ColumnTransformer(transformers=transformers)

    return Pipeline(
        steps=[
            ("prep", preprocessor),
            ("clf", classifier),
        ],
    )
