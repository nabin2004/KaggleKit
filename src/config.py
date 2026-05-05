import os

IS_KAGGLE = os.path.exists("/kaggle/working")

if IS_KAGGLE:
    DATASET_DIR = os.environ.get(
        "KAGGLE_DATASET_DIR", "/kaggle/input/your-dataset-name"
    )
    RAW_DATA_FILE = os.path.join(DATASET_DIR, "train.csv")
    WORKING_DIR = "/kaggle/working"
    TRAINING_FILE = os.path.join(WORKING_DIR, "train_folds.csv")
    MODEL_OUTPUT = os.path.join(WORKING_DIR, "models")
    os.makedirs(MODEL_OUTPUT, exist_ok=True)
else:
    RAW_DATA_FILE = "../input/train.csv"
    TRAINING_FILE = "../input/train_folds.csv"
    MODEL_OUTPUT = "../models/"

TARGET_COLUMN = "PitNextLap"
KFOLD_COLUMN = "kfold"
METADATA_COLUMNS: tuple[str, ...] = ("kfold",)
DROP_FROM_FEATURES: tuple[str, ...] = ()
