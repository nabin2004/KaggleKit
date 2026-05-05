from __future__ import annotations

import pandas as pd
import pytest
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier

import config
import data_cleaning
import model_dispatcher
import model_pipelines


@pytest.fixture(autouse=True)
def reset_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "TARGET_COLUMN", "PitNextLap", raising=False)
    monkeypatch.setattr(config, "KFOLD_COLUMN", "kfold", raising=False)
    monkeypatch.setattr(config, "METADATA_COLUMNS", ("kfold",), raising=False)
    monkeypatch.setattr(config, "DROP_FROM_FEATURES", (), raising=False)


def test_feature_columns_excludes_metadata_and_target() -> None:
    df = pd.DataFrame(
        {
            "kfold": [0, 1],
            "PitNextLap": [0, 1],
            "feat_num": [1.0, 2.0],
            "feat_cat": ["a", "b"],
        },
    )
    feats = data_cleaning.feature_columns(df)
    assert "kfold" not in feats
    assert "PitNextLap" not in feats
    assert set(feats) == {"feat_num", "feat_cat"}


def test_train_valid_arrays_excludes_kfold_from_features() -> None:
    df = pd.DataFrame(
        {
            "kfold": [0, 0, 1, 1],
            "PitNextLap": [0, 1, 0, 1],
            "x": [1.0, 2.0, 3.0, 4.0],
            "c": ["a", "b", "c", "a"],
        },
    )
    xt, xv, yt, yv = data_cleaning.train_valid_arrays(
        df, fold=1, target_column="PitNextLap"
    )
    assert list(xt.columns) == ["x", "c"]
    assert len(xv) == 2
    assert len(xt) == 2


def test_rf_pipeline_fit_predict_smoke() -> None:
    df_train = pd.DataFrame(
        {
            "num": [1.0, 2.0, 3.0],
            "cat": ["y", "n", None],
        },
    )
    x_valid = pd.DataFrame(
        {
            "num": [4.0],
            "cat": ["y"],
        },
    )
    clf = RandomForestClassifier(n_estimators=2, random_state=0)
    num, cat = data_cleaning.infer_numeric_and_categorical(
        df_train, list(df_train.columns)
    )
    pipe = model_pipelines.build_rf_pipeline(clone(clf), num, cat)
    y_train = pd.Series([0, 1, 0])
    pipe.fit(df_train, y_train)

    preds = pipe.predict(x_valid)
    assert preds.shape == (1,)


def test_rf_dispatcher_pipeline_save_shape() -> None:
    xt = pd.DataFrame({"n": [0.1, 0.2], "g": ["a", "b"]})
    xv = pd.DataFrame({"n": [0.3], "g": ["z"]})
    yt = pd.Series([0, 1])
    yv = pd.Series([1])
    num, cat = data_cleaning.infer_numeric_and_categorical(xt, list(xt.columns))
    pipe = model_pipelines.build_rf_pipeline(
        clone(model_dispatcher.models["rf"]),
        numeric_features=num,
        categorical_features=cat,
    )
    pipe.fit(xt, yt)
    assert pipe.predict(xv).shape == yv.shape
