# train.py
from __future__ import annotations

import argparse
import os

import joblib
import pandas as pd
from sklearn import metrics
from sklearn.base import clone

import config
import data_cleaning
import model_dispatcher
import model_pipelines


def run(fold: int, model: str) -> float:
    df = pd.read_csv(config.TRAINING_FILE)

    if model == "rf":
        x_train, x_valid, y_train, y_valid = data_cleaning.train_valid_arrays(
            df, fold, config.TARGET_COLUMN
        )
        num_feats, cat_feats = data_cleaning.infer_numeric_and_categorical(
            x_train, list(x_train.columns)
        )

        clf = clone(model_dispatcher.models["rf"])
        fitted = model_pipelines.build_rf_pipeline(
            clf,
            numeric_features=num_feats,
            categorical_features=cat_feats,
        )
        fitted.fit(x_train, y_train)
        preds = fitted.predict(x_valid)
        accuracy = float(metrics.accuracy_score(y_valid, preds))
        print(f"Fold={fold}, Accuracy={accuracy}")

        fname = os.path.join(
            config.MODEL_OUTPUT,
            f"rf_fold_{fold}.bin",
        )
        joblib.dump(fitted, fname)
        return accuracy

    kcol = config.KFOLD_COLUMN
    df_train = df[df[kcol] != fold].reset_index(drop=True)
    df_valid = df[df[kcol] == fold].reset_index(drop=True)
    xm_train = df_train.drop(config.TARGET_COLUMN, axis=1).values
    ym_train = df_train[config.TARGET_COLUMN].values
    xm_valid = df_valid.drop(config.TARGET_COLUMN, axis=1).values
    ym_valid = df_valid[config.TARGET_COLUMN].values

    clf = model_dispatcher.models[model]
    clf.fit(xm_train, ym_train)
    preds = clf.predict(xm_valid)
    accuracy = float(metrics.accuracy_score(ym_valid, preds))
    print(f"Fold={fold}, Accuracy={accuracy}")
    joblib.dump(clf, os.path.join(config.MODEL_OUTPUT, f"dt_{fold}.bin"))

    return accuracy


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fold", type=int)
    parser.add_argument("--model", type=str)
    args = parser.parse_args()
    run(fold=args.fold, model=args.model)
