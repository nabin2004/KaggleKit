# Optuna: tune HistGradientBoosting on a subset.
# Objective = validation balanced_accuracy_score.
# Re-run after changing OPTUNA_TRIALS / OPTUNA_SAMPLE.
# Then re-run the pipeline + training cells.
import numpy as np
import optuna
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Define constants
OPTUNA_SAMPLE = 120_000
OPTUNA_TRIALS = 25

# Placeholder for X and y (to be replaced with actual data)
X = np.random.rand(1000, 10)  # Example feature DataFrame
y = np.random.randint(0, 2, size=1000)  # Example target Series

# Sample data for tuning
rng = np.random.default_rng(0)
idx = rng.choice(len(X), size=min(OPTUNA_SAMPLE, len(X)), replace=False)
X_t, y_t = X[idx], y[idx]
X_tr, X_va, y_tr, y_va = train_test_split(
    X_t, y_t, test_size=0.2, random_state=0, stratify=y_t
)


def _make_prep(
    numeric_features: list[str], categorical_features: list[str]
) -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
        ],
    )


def _objective(trial: optuna.Trial) -> float:
    clf = HistGradientBoostingClassifier(
        max_iter=trial.suggest_int("max_iter", 50, 200),
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        max_depth=trial.suggest_int("max_depth", 3, 10),
        random_state=42,
        class_weight="balanced",
    )

    prep = _make_prep(
        numeric_features=["feature_" + str(i) for i in range(5)],
        categorical_features=["feature_" + str(i) for i in range(5, 10)],
    )
    pipeline = Pipeline(
        [
            ("prep", prep),
            ("clf", clf),
        ]
    )

    pipeline.fit(X_tr, y_tr)
    preds = pipeline.predict(X_va)
    return float(balanced_accuracy_score(y_va, preds))


study = optuna.create_study(direction="maximize")
study.optimize(_objective, n_trials=OPTUNA_TRIALS)

print("Best trial:", study.best_trial)
