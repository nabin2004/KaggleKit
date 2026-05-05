TRAINING_FILE = "../input/train_folds.csv"
MODEL_OUTPUT = "../models/"

TARGET_COLUMN = "PitNextLap"
KFOLD_COLUMN = "kfold"
METADATA_COLUMNS: tuple[str, ...] = ("kfold",)
DROP_FROM_FEATURES: tuple[str, ...] = ()
